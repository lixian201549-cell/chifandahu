#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version bumper for Snoopy's Little Lab.
Usage:
    python3 bump_version.py             # Increments patch: v1.0.0 -> v1.0.1
    python3 bump_version.py patch       # Increments patch: v1.0.0 -> v1.0.1
    python3 bump_version.py minor       # Increments minor: v1.0.0 -> v1.1.0
    python3 bump_version.py major       # Increments major: v1.0.0 -> v2.0.0
    python3 bump_version.py 1.2.3       # Sets explicit version: v1.2.3
    python3 bump_version.py --current   # Prints current version
    python3 bump_version.py --push      # Bumps patch, recompiles, and pushes to git
"""

import os
import re
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.join(BASE_DIR, "VERSION")


def get_current_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            v = f.read().strip()
            if v:
                return v if v.startswith("v") else f"v{v}"
    return "v1.0.0"


def parse_version(v_str):
    m = re.match(r"^v?(\d+)\.(\d+)\.(\d+)(.*)$", v_str.strip())
    if not m:
        return 1, 0, 0, ""
    major, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
    suffix = m.group(4)
    return major, minor, patch, suffix


def compute_next_version(current_v, bump_type):
    major, minor, patch, _ = parse_version(current_v)
    bump = bump_type.lower().strip()

    if bump in ("patch", "p", ""):
        patch += 1
    elif bump in ("minor", "m"):
        minor += 1
        patch = 0
    elif bump in ("major", "M"):
        major += 1
        minor = 0
        patch = 0
    else:
        # User passed a custom version string
        clean = bump.lstrip("v")
        if re.match(r"^\d+\.\d+(\.\d+)?", clean):
            return f"v{clean}"
        else:
            print(f"Unknown bump argument '{bump_type}', defaulting to patch bump.")
            patch += 1

    return f"v{major}.{minor}.{patch}"


def main():
    args = sys.argv[1:]
    do_push = False
    bump_arg = "patch"

    if "--current" in args or "-c" in args:
        print(get_current_version())
        return

    filtered_args = []
    for a in args:
        if a in ("--push", "-p"):
            do_push = True
        else:
            filtered_args.append(a)

    if filtered_args:
        bump_arg = filtered_args[0]

    cur_v = get_current_version()
    new_v = compute_next_version(cur_v, bump_arg)

    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(new_v + "\n")

    print(f"🏷️  Bumping version: {cur_v} -> {new_v}")

    # Reassemble app
    print("🔨 Compiling index.html and login.html...")
    res = subprocess.run([sys.executable, "assemble_final_app.py"], cwd=BASE_DIR)
    if res.returncode != 0:
        print("❌ Recompilation failed!")
        sys.exit(1)

    print(f"✨ Successfully compiled pages with version {new_v}!")

    if do_push:
        print("🚀 Auto-committing and pushing to remote git repository...")
        subprocess.run(["git", "add", "VERSION", "index.html", "login.html", "dist/"], cwd=BASE_DIR)
        commit_msg = f"chore(release): bump version to {new_v}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=BASE_DIR)
        push_res = subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR)
        if push_res.returncode == 0:
            print(f"🎉 Pushed {new_v} to remote successfully!")
        else:
            print("⚠️ Push failed, please push manually.")


if __name__ == "__main__":
    main()
