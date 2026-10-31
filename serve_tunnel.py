import os
import sys
import time
import subprocess
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")
PORT = 8787
CLOUDFLARED = os.path.join(BASE_DIR, "bin/cloudflared")
BACKEND_SCRIPT = os.path.join(BASE_DIR, "backend_server.py")

# 1. Start Host SQLite Backend Server
print(f"Starting Host SQLite Backend Server on port {PORT}...")
http_proc = subprocess.Popen(
    [sys.executable, BACKEND_SCRIPT, str(PORT)],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# 2. Start Cloudflare Quick Tunnel (立即生效的免费即时隧道，用于多设备联调测试)
print("Connecting Cloudflare Quick Tunnel (trycloudflare.com)...")
cf_proc = subprocess.Popen(
    [CLOUDFLARED, "tunnel", "--url", f"http://127.0.0.1:{PORT}"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

tunnel_url = None
start_time = time.time()

for line in iter(cf_proc.stdout.readline, ''):
    sys.stdout.write(line)
    sys.stdout.flush()
    match = re.search(r'(https://[a-zA-Z0-9-]+\.trycloudflare\.com)', line)
    if match:
        tunnel_url = match.group(1)
        with open(os.path.join(BASE_DIR, "tunnel_url.txt"), "w", encoding="utf-8") as f:
            f.write(tunnel_url)
        print("\n" + "="*60)
        print(f"PUBLIC TEST TUNNEL READY: {tunnel_url}")
        print("Connected directly to Host SQLite Database (data/work_platform.db)")
        print("="*60 + "\n")
        break
    if time.time() - start_time > 30:
        print("Timeout waiting for tunnel URL")
        break

try:
    while True:
        time.sleep(1)
        if http_proc.poll() is not None or cf_proc.poll() is not None:
            break
except KeyboardInterrupt:
    pass
finally:
    http_proc.terminate()
    cf_proc.terminate()
