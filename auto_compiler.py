#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WATCH_TARGETS = [
    os.path.join(BASE_DIR, "assemble_final_app.py"),
    os.path.join(BASE_DIR, "backend_server.py"),
    os.path.join(BASE_DIR, "serve_tunnel.py")
]

def get_mtimes():
    return {f: os.path.getmtime(f) for f in WATCH_TARGETS if os.path.exists(f)}

def git_auto_commit_and_push():
    try:
        # Check if git repo exists
        if not os.path.exists(os.path.join(BASE_DIR, ".git")):
            return
        status = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR, capture_output=True, text=True)
        if status.stdout.strip():
            subprocess.run(["git", "add", "."], cwd=BASE_DIR)
            commit_msg = f"auto-update: code change at {time.strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=BASE_DIR, capture_output=True)
            print(f"[{time.strftime('%H:%M:%S')}] ✓ Git auto-committed locally: {commit_msg}")
            
            # Check if remote origin is configured
            remotes = subprocess.run(["git", "remote"], cwd=BASE_DIR, capture_output=True, text=True).stdout
            if "origin" in remotes.split():
                push_res = subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True)
                if push_res.returncode == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] 🚀 Successfully auto-pushed to remote Git repository!")
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Git push skipped/error: {push_res.stderr.strip()}")
    except Exception as e:
        print(f"Git auto-sync warning: {e}")

def build():
    print(f"[{time.strftime('%H:%M:%S')}] Detected code changes. Auto-recompiling...")
    res = subprocess.run([sys.executable, "assemble_final_app.py"], cwd=BASE_DIR, capture_output=True, text=True)
    if res.returncode == 0:
        subprocess.run(["cp", "index.html", "dist/index.html"], cwd=BASE_DIR)
        print(f"[{time.strftime('%H:%M:%S')}] ✓ Recompile succeeded! dist/index.html updated. Live immediately!")
        git_auto_commit_and_push()
    else:
        print(f"[{time.strftime('%H:%M:%S')}] ❌ Recompile error:\n", res.stderr)

def main():
    print("Auto-compiler & Git Sync started. Watching source code for instant updates & auto-push...")
    last_mtimes = get_mtimes()
    while True:
        time.sleep(1)
        cur_mtimes = get_mtimes()
        if cur_mtimes != last_mtimes:
            last_mtimes = cur_mtimes
            build()

if __name__ == '__main__':
    main()
