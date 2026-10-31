#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WATCH_TARGETS = [
    os.path.join(BASE_DIR, "assemble_final_app.py")
]

def get_mtimes():
    return {f: os.path.getmtime(f) for f in WATCH_TARGETS if os.path.exists(f)}

def build():
    print(f"[{time.strftime('%H:%M:%S')}] Detected code changes. Auto-recompiling...")
    res = subprocess.run([sys.executable, "assemble_final_app.py"], cwd=BASE_DIR, capture_output=True, text=True)
    if res.returncode == 0:
        subprocess.run(["cp", "index.html", "dist/index.html"], cwd=BASE_DIR)
        print(f"[{time.strftime('%H:%M:%S')}] ✓ Recompile succeeded! dist/index.html updated. Live immediately!")
    else:
        print(f"[{time.strftime('%H:%M:%S')}] ❌ Recompile error:\n", res.stderr)

def main():
    print("Auto-compiler started. Watching assemble_final_app.py for instant live updates...")
    last_mtimes = get_mtimes()
    while True:
        time.sleep(1)
        cur_mtimes = get_mtimes()
        if cur_mtimes != last_mtimes:
            last_mtimes = cur_mtimes
            build()

if __name__ == '__main__':
    main()
