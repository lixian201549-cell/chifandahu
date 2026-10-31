#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import sqlite3
from http.server import HTTPServer, SimpleHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "work_platform.db")

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS platform_storage (
            key TEXT PRIMARY KEY,
            val TEXT,
            updated_at REAL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sync_meta (
            id INTEGER PRIMARY KEY,
            last_modified REAL
        );
    """)
    cursor.execute("INSERT OR IGNORE INTO sync_meta (id, last_modified) VALUES (1, ?)", (time.time(),))
    conn.commit()
    conn.close()

def db_get_all_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT key, val FROM platform_storage")
    rows = cursor.fetchall()
    cursor.execute("SELECT last_modified FROM sync_meta WHERE id = 1")
    meta_row = cursor.fetchone()
    last_mod = meta_row[0] if meta_row else time.time()
    conn.close()
    
    result = {}
    for k, v in rows:
        try:
            result[k] = json.loads(v)
        except Exception:
            result[k] = v
    return result, last_mod

def db_set_key(key, val):
    now = time.time()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    val_str = json.dumps(val, ensure_ascii=False)
    cursor.execute("""
        INSERT INTO platform_storage (key, val, updated_at) 
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET val=excluded.val, updated_at=excluded.updated_at
    """, (key, val_str, now))
    cursor.execute("UPDATE sync_meta SET last_modified = ? WHERE id = 1", (now,))
    conn.commit()
    conn.close()
    return now

def db_batch_set(data_dict):
    now = time.time()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for k, v in data_dict.items():
        val_str = json.dumps(v, ensure_ascii=False)
        cursor.execute("""
            INSERT INTO platform_storage (key, val, updated_at) 
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET val=excluded.val, updated_at=excluded.updated_at
        """, (k, val_str, now))
    cursor.execute("UPDATE sync_meta SET last_modified = ? WHERE id = 1", (now,))
    conn.commit()
    conn.close()
    return now

class PlatformHTTPHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS and disable aggressive caching for API
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # API Routes
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            resp = {
                "status": "online",
                "database": "SQLite",
                "dbPath": DB_PATH,
                "serverTime": time.time()
            }
            self.wfile.write(json.dumps(resp).encode('utf-8'))
            return

        if self.path.startswith('/api/data'):
            data_dict, last_mod = db_get_all_data()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            resp = {
                "success": True,
                "data": data_dict,
                "lastModified": last_mod,
                "count": len(data_dict)
            }
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
            return

        # Serve static assets from DIST_DIR
        super().do_GET()

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len).decode('utf-8') if content_len > 0 else '{}'
        
        try:
            req_data = json.loads(body)
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
            return

        if self.path == '/api/set':
            key = req_data.get('key')
            val = req_data.get('val')
            if not key:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"success": false, "error": "Missing key"}')
                return
            last_mod = db_set_key(key, val)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "lastModified": last_mod}).encode('utf-8'))
            return

        if self.path == '/api/batch':
            data_dict = req_data.get('data', {})
            last_mod = db_batch_set(data_dict)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "lastModified": last_mod, "keys": len(data_dict)}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

def run_server(port=8787):
    init_db()
    server_address = ('', port)
    httpd = HTTPServer(server_address, PlatformHTTPHandler)
    print(f"Host SQLite Backend Server running on port {port}...")
    print(f"Database File: {DB_PATH}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8787
    run_server(port)
