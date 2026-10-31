#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WATCH_TARGETS = [
    os.path.join(BASE_DIR, "assemble_final_app.py"),
    os.path.join(BASE_DIR, "backend_server.py"),
    os.path.join(BASE_DIR, "serve_tunnel.py")
]

def get_mtimes():
    return {f: os.path.getmtime(f) for f in WATCH_TARGETS if os.path.exists(f)}

def build():
    print(f"[{time.strftime('%H:%M:%S')}] Detected code changes. Auto-recompiling...")
    res = subprocess.run([sys.executable, "assemble_final_app.py"], cwd=BASE_DIR, capture_output=True, text=True)
    if res.returncode == 0:
        os.makedirs(os.path.join(BASE_DIR, "dist"), exist_ok=True)
        shutil.copy2(os.path.join(BASE_DIR, "index.html"), os.path.join(BASE_DIR, "dist/index.html"))
        shutil.copy2(os.path.join(BASE_DIR, "login.html"), os.path.join(BASE_DIR, "dist/login.html"))
        shutil.copy2(os.path.join(BASE_DIR, "favicon.ico"), os.path.join(BASE_DIR, "dist/favicon.ico"))
        shutil.copy2(os.path.join(BASE_DIR, "favicon.png"), os.path.join(BASE_DIR, "dist/favicon.png"))
        print(f"[{time.strftime('%H:%M:%S')}] ✓ Recompile succeeded. Login page and app are live.")
    else:
        print(f"[{time.strftime('%H:%M:%S')}] ❌ Recompile error:\n", res.stderr)

def main():
    print("Auto-compiler started. Watching source code for local rebuilds (Git is never changed automatically).")
    last_mtimes = get_mtimes()
    while True:
        time.sleep(1)
        cur_mtimes = get_mtimes()
        if cur_mtimes != last_mtimes:
            last_mtimes = cur_mtimes
            build()

if __name__ == '__main__':
    main()
