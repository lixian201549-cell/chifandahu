#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import os
import secrets
import shutil
import sqlite3
import threading
import time
from http.cookies import SimpleCookie
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "work_platform.db")
AUTH_PATH = os.path.join(DATA_DIR, "auth_config.json")
INITIAL_PASSWORD_PATH = os.path.join(DATA_DIR, "initial_login.txt")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
VERSION_PATH = os.path.join(BASE_DIR, "VERSION")


def get_app_version():
    if os.path.exists(VERSION_PATH):
        try:
            with open(VERSION_PATH, "r", encoding="utf-8") as vf:
                v = vf.read().strip()
                if v:
                    return v if v.startswith("v") else f"v{v}"
        except Exception:
            pass
    return "v1.0.0"

MAX_REQUEST_BYTES = 8 * 1024 * 1024
SESSION_TTL_SECONDS = 12 * 60 * 60
PASSWORD_ITERATIONS = 310_000
MAX_LOGIN_FAILURES = 5
LOGIN_BLOCK_SECONDS = 15 * 60
ALLOWED_KEY_PREFIX = "snoopy_"

_sessions = {}
_login_failures = {}
_state_lock = threading.Lock()
_backup_lock = threading.Lock()
_last_backup_at = 0.0
_password_salt = b""
_password_hash = b""


def _hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS)


def init_auth():
    global _password_salt, _password_hash
    os.makedirs(DATA_DIR, exist_ok=True)
    configured_password = os.environ.get("PLATFORM_PASSWORD", "").strip()
    if configured_password:
        _password_salt = hashlib.sha256((BASE_DIR + "|env").encode("utf-8")).digest()[:16]
        _password_hash = _hash_password(configured_password, _password_salt)
        print("Login password loaded from PLATFORM_PASSWORD.")
        return

    if os.path.exists(AUTH_PATH):
        with open(AUTH_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        _password_salt = bytes.fromhex(config["salt"])
        _password_hash = bytes.fromhex(config["hash"])
        return

    password = "Snoopy-" + secrets.token_urlsafe(9)
    _password_salt = secrets.token_bytes(16)
    _password_hash = _hash_password(password, _password_salt)
    with open(AUTH_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "salt": _password_salt.hex(),
            "hash": _password_hash.hex(),
            "iterations": PASSWORD_ITERATIONS,
        }, f, ensure_ascii=False, indent=2)
    os.chmod(AUTH_PATH, 0o600)
    with open(INITIAL_PASSWORD_PATH, "w", encoding="utf-8") as f:
        f.write("Snoopy's Little Lab\n")
        f.write("Username: Sanyli\n")
        f.write("Password: " + password + "\n")
        f.write("This file is local-only and ignored by Git. Delete it after saving the password.\n")
    os.chmod(INITIAL_PASSWORD_PATH, 0o600)
    print(f"Initial login password saved to: {INITIAL_PASSWORD_PATH}")


def verify_password(password):
    candidate = _hash_password(password, _password_salt)
    return hmac.compare_digest(candidate, _password_hash)


def valid_new_password(password):
    if not isinstance(password, str) or len(password) > 256:
        return False
    return (len(password) == 6 and password.isascii() and password.isdigit()) or len(password) >= 10


def update_password(password):
    global _password_salt, _password_hash
    salt = secrets.token_bytes(16)
    password_hash = _hash_password(password, salt)
    temp_path = AUTH_PATH + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump({
            "salt": salt.hex(),
            "hash": password_hash.hex(),
            "iterations": PASSWORD_ITERATIONS,
        }, f, ensure_ascii=False, indent=2)
    os.chmod(temp_path, 0o600)
    os.replace(temp_path, AUTH_PATH)
    if os.path.exists(INITIAL_PASSWORD_PATH):
        os.remove(INITIAL_PASSWORD_PATH)
    _password_salt = salt
    _password_hash = password_hash


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=10000;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS platform_storage (
                key TEXT PRIMARY KEY,
                val TEXT,
                updated_at REAL NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sync_meta (
                id INTEGER PRIMARY KEY,
                last_modified REAL NOT NULL
            );
        """)
        conn.execute("INSERT OR IGNORE INTO sync_meta (id, last_modified) VALUES (1, ?)", (time.time(),))
        conn.execute("PRAGMA optimize;")


def maybe_backup_db():
    global _last_backup_at
    now = time.time()
    if now - _last_backup_at < 6 * 60 * 60 or not os.path.exists(DB_PATH):
        return
    with _backup_lock:
        if now - _last_backup_at < 6 * 60 * 60:
            return
        os.makedirs(BACKUP_DIR, exist_ok=True)
        backup_path = os.path.join(BACKUP_DIR, time.strftime("work_platform-%Y%m%d-%H%M%S.db"))
        source = sqlite3.connect(DB_PATH, timeout=10)
        target = sqlite3.connect(backup_path)
        try:
            source.backup(target)
        finally:
            target.close()
            source.close()
        _last_backup_at = now
        backups = sorted(
            (os.path.join(BACKUP_DIR, name) for name in os.listdir(BACKUP_DIR) if name.endswith(".db")),
            key=os.path.getmtime,
            reverse=True,
        )
        for old_backup in backups[10:]:
            os.remove(old_backup)


def db_get_all_data(since=None):
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        if since is not None:
            rows = conn.execute(
                "SELECT key, val, updated_at FROM platform_storage WHERE updated_at > ?",
                (since,),
            ).fetchall()
        else:
            rows = conn.execute("SELECT key, val, updated_at FROM platform_storage").fetchall()
        meta_row = conn.execute("SELECT last_modified FROM sync_meta WHERE id = 1").fetchone()
    last_mod = meta_row[0] if meta_row else time.time()
    data = {}
    versions = {}
    for key, raw_value, updated_at in rows:
        try:
            data[key] = json.loads(raw_value)
        except Exception:
            data[key] = raw_value
        versions[key] = updated_at
    return data, versions, last_mod


def db_set_key(key, value, expected_updated_at=None):
    now = time.time()
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        conn.execute("BEGIN IMMEDIATE")
        current = conn.execute("SELECT val, updated_at FROM platform_storage WHERE key = ?", (key,)).fetchone()
        if expected_updated_at is not None and current and abs(current[1] - expected_updated_at) > 0.000001:
            conn.rollback()
            try:
                current_value = json.loads(current[0])
            except Exception:
                current_value = current[0]
            return False, current[1], current_value
        conn.execute("""
            INSERT INTO platform_storage (key, val, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET val=excluded.val, updated_at=excluded.updated_at
        """, (key, json.dumps(value, ensure_ascii=False), now))
        conn.execute("UPDATE sync_meta SET last_modified = ? WHERE id = 1", (now,))
    maybe_backup_db()
    return True, now, None


def db_batch_set(data_dict):
    now = time.time()
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        conn.execute("BEGIN IMMEDIATE")
        for key, value in data_dict.items():
            conn.execute("""
                INSERT INTO platform_storage (key, val, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET val=excluded.val, updated_at=excluded.updated_at
            """, (key, json.dumps(value, ensure_ascii=False), now))
        conn.execute("UPDATE sync_meta SET last_modified = ? WHERE id = 1", (now,))
    maybe_backup_db()
    return now


def _valid_storage_key(key):
    return isinstance(key, str) and key.startswith(ALLOWED_KEY_PREFIX) and len(key) <= 128


class PlatformHTTPHandler(SimpleHTTPRequestHandler):
    server_version = "SnoopyLab/2.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST_DIR, **kwargs)

    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self' data:; script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
            "connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'",
        )
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def _json_response(self, status, payload, extra_headers=None):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        for name, value in (extra_headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def _redirect(self, location):
        self.send_response(303)
        self.send_header("Location", location)
        self.end_headers()

    def _client_ip(self):
        return self.headers.get("CF-Connecting-IP") or self.client_address[0]

    def _same_origin(self):
        origin = self.headers.get("Origin")
        if not origin:
            return True
        parsed = urlparse(origin)
        return parsed.netloc == self.headers.get("Host") and parsed.scheme in ("http", "https")

    def _session_token(self):
        cookie_header = self.headers.get("Cookie", "")
        cookie = SimpleCookie()
        try:
            cookie.load(cookie_header)
        except Exception:
            return ""
        morsel = cookie.get("snoopy_session")
        return morsel.value if morsel else ""

    def _is_authenticated(self):
        token = self._session_token()
        if not token:
            return False
        now = time.time()
        with _state_lock:
            expiry = _sessions.get(token, 0)
            if expiry <= now:
                _sessions.pop(token, None)
                return False
            _sessions[token] = now + SESSION_TTL_SECONDS
        return True

    def _require_api_auth(self):
        if self._is_authenticated():
            return True
        self._json_response(401, {"success": False, "error": "AUTH_REQUIRED"})
        return False

    def _read_json(self):
        raw_length = self.headers.get("Content-Length", "0")
        try:
            content_length = int(raw_length)
        except ValueError:
            raise ValueError("Invalid Content-Length")
        if content_length < 0 or content_length > MAX_REQUEST_BYTES:
            raise OverflowError("Request body too large")
        raw_body = self.rfile.read(content_length) if content_length else b"{}"
        return json.loads(raw_body.decode("utf-8"))

    def do_OPTIONS(self):
        if not self._same_origin():
            self.send_error(403)
            return
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/session":
            self._json_response(200, {"success": True, "authenticated": self._is_authenticated()})
            return

        if path == "/login":
            if self._is_authenticated():
                self._redirect("/")
                return
            self.path = "/login.html"
            super().do_GET()
            return

        if path == "/login.html":
            self._redirect("/login")
            return

        if path in ("/favicon.ico", "/favicon.png"):
            self.path = path
            super().do_GET()
            return

        if path.startswith("/api/"):
            if not self._require_api_auth():
                return
            if path == "/api/status":
                self._json_response(200, {
                    "status": "online",
                    "database": "SQLite",
                    "serverTime": time.time(),
                    "appVersion": get_app_version(),
                })
                return
            if path == "/api/data":
                query = parse_qs(parsed.query)
                try:
                    since = float(query["since"][0]) if query.get("since") else None
                except (TypeError, ValueError):
                    self._json_response(400, {"success": False, "error": "Invalid since value"})
                    return
                data, versions, last_mod = db_get_all_data(since)
                self._json_response(200, {
                    "success": True,
                    "data": data,
                    "versions": versions,
                    "lastModified": last_mod,
                    "count": len(data),
                })
                return
            self._json_response(404, {"success": False, "error": "Not found"})
            return

        if not self._is_authenticated():
            self._redirect("/login")
            return
        if path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if not self._same_origin():
            self._json_response(403, {"success": False, "error": "Invalid origin"})
            return
        try:
            request_data = self._read_json()
        except OverflowError as exc:
            self._json_response(413, {"success": False, "error": str(exc)})
            return
        except Exception:
            self._json_response(400, {"success": False, "error": "Invalid JSON body"})
            return

        if path == "/api/login":
            self._handle_login(request_data)
            return

        if path == "/api/logout":
            token = self._session_token()
            with _state_lock:
                _sessions.pop(token, None)
            self._json_response(200, {"success": True}, {
                "Set-Cookie": "snoopy_session=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0",
            })
            return

        if not self._require_api_auth():
            return

        if path == "/api/change-password":
            if os.environ.get("PLATFORM_PASSWORD", "").strip():
                self._json_response(409, {
                    "success": False,
                    "error": "PASSWORD_MANAGED_BY_ENV",
                })
                return
            current_password = request_data.get("currentPassword")
            new_password = request_data.get("newPassword")
            if not isinstance(current_password, str) or not verify_password(current_password):
                self._json_response(401, {
                    "success": False,
                    "error": "CURRENT_PASSWORD_INCORRECT",
                })
                return
            if not valid_new_password(new_password):
                self._json_response(400, {
                    "success": False,
                    "error": "INVALID_NEW_PASSWORD",
                })
                return
            if hmac.compare_digest(current_password, new_password):
                self._json_response(400, {
                    "success": False,
                    "error": "PASSWORD_UNCHANGED",
                })
                return
            update_password(new_password)
            with _state_lock:
                _sessions.clear()
            self._json_response(200, {"success": True}, {
                "Set-Cookie": "snoopy_session=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0",
            })
            return

        if path == "/api/set":
            key = request_data.get("key")
            if not _valid_storage_key(key):
                self._json_response(400, {"success": False, "error": "Invalid storage key"})
                return
            expected = request_data.get("expectedUpdatedAt")
            # Blackboard is a live personal scratchpad; always allow direct save without conflict collision
            if key == "snoopy_blackboard_records_v1":
                expected = None
            elif expected is not None and not isinstance(expected, (int, float)):
                self._json_response(400, {"success": False, "error": "Invalid version"})
                return
            success, version, current_value = db_set_key(key, request_data.get("val"), expected)
            if not success:
                self._json_response(409, {
                    "success": False,
                    "error": "SYNC_CONFLICT",
                    "key": key,
                    "currentValue": current_value,
                    "currentVersion": version,
                })
                return
            self._json_response(200, {"success": True, "lastModified": version, "version": version})
            return

        if path == "/api/batch":
            data_dict = request_data.get("data")
            if not isinstance(data_dict, dict) or len(data_dict) > 100:
                self._json_response(400, {"success": False, "error": "Invalid batch data"})
                return
            if any(not _valid_storage_key(key) for key in data_dict):
                self._json_response(400, {"success": False, "error": "Invalid storage key"})
                return
            last_mod = db_batch_set(data_dict)
            self._json_response(200, {
                "success": True,
                "lastModified": last_mod,
                "keys": len(data_dict),
            })
            return

        self._json_response(404, {"success": False, "error": "Not found"})

    def _handle_login(self, request_data):
        ip = self._client_ip()
        now = time.time()
        with _state_lock:
            attempts, blocked_until = _login_failures.get(ip, (0, 0))
        if blocked_until > now:
            retry_after = max(1, int(blocked_until - now))
            self._json_response(429, {
                "success": False,
                "error": "TOO_MANY_ATTEMPTS",
                "retryAfter": retry_after,
            }, {"Retry-After": str(retry_after)})
            return

        password = request_data.get("password")
        if not isinstance(password, str) or not verify_password(password):
            with _state_lock:
                attempts += 1
                blocked_until = now + LOGIN_BLOCK_SECONDS if attempts >= MAX_LOGIN_FAILURES else 0
                _login_failures[ip] = (attempts, blocked_until)
            self._json_response(401, {"success": False, "error": "INVALID_CREDENTIALS"})
            return

        token = secrets.token_urlsafe(32)
        with _state_lock:
            _login_failures.pop(ip, None)
            _sessions[token] = now + SESSION_TTL_SECONDS
        forwarded_proto = self.headers.get("X-Forwarded-Proto", "")
        secure = "; Secure" if forwarded_proto == "https" else ""
        cookie = (
            f"snoopy_session={token}; Path=/; HttpOnly; SameSite=Strict; "
            f"Max-Age={SESSION_TTL_SECONDS}{secure}"
        )
        self._json_response(200, {"success": True}, {"Set-Cookie": cookie})


def run_server(port=8787):
    init_auth()
    init_db()
    server_address = ("127.0.0.1", port)
    httpd = ThreadingHTTPServer(server_address, PlatformHTTPHandler)
    print(f"Snoopy's Little Lab server running on http://127.0.0.1:{port}")
    print("The app and all data APIs are protected by password login.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8787"))
    if len(os.sys.argv) > 1:
        port = int(os.sys.argv[1])
    run_server(port)
