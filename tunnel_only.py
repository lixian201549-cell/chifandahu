#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Keep the Cloudflare Quick Tunnel independent from backend restarts."""
import os
import re
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8787"))
CLOUDFLARED = os.path.join(BASE_DIR, "bin", "cloudflared")
URL_FILE = os.path.join(BASE_DIR, "tunnel_url.txt")


def main():
    if not os.path.isfile(CLOUDFLARED):
        raise SystemExit(f"cloudflared not found: {CLOUDFLARED}")
    print(f"Starting independent Cloudflare Quick Tunnel for 127.0.0.1:{PORT}...")
    process = subprocess.Popen(
        [CLOUDFLARED, "tunnel", "--no-autoupdate", "--url", f"http://127.0.0.1:{PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    try:
        for line in iter(process.stdout.readline, ""):
            sys.stdout.write(line)
            sys.stdout.flush()
            match = re.search(r"(https://[a-zA-Z0-9-]+\.trycloudflare\.com)", line)
            if match:
                with open(URL_FILE, "w", encoding="utf-8") as f:
                    f.write(match.group(1))
            if "Tunnel not found" in line:
                print("Cloudflare quick tunnel expired. Exiting so PM2 restarts with a fresh tunnel...")
                process.terminate()
                break
        return process.wait()
    except KeyboardInterrupt:
        return 0
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


if __name__ == "__main__":
    raise SystemExit(main())
