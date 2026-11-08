#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Change the local login password without storing plaintext in the project."""
import getpass
import hashlib
import json
import os
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
AUTH_PATH = os.path.join(DATA_DIR, "auth_config.json")
INITIAL_PASSWORD_PATH = os.path.join(DATA_DIR, "initial_login.txt")
ITERATIONS = 310_000


def main():
    print("Change Snoopy's Little Lab login password")
    password = getpass.getpass("New password (2 to 256 characters): ")
    confirm = getpass.getpass("Confirm new password: ")
    if password != confirm:
        raise SystemExit("Passwords do not match.")
    valid_password = 2 <= len(password) <= 256
    if not valid_password:
        raise SystemExit("Password must contain 2 to 256 characters.")
    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(AUTH_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "salt": salt.hex(),
            "hash": password_hash.hex(),
            "iterations": ITERATIONS,
        }, f, ensure_ascii=False, indent=2)
    os.chmod(AUTH_PATH, 0o600)
    if os.path.exists(INITIAL_PASSWORD_PATH):
        os.remove(INITIAL_PASSWORD_PATH)
    print("Password updated. Restart the service to apply it.")


if __name__ == "__main__":
    main()
