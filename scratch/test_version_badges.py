#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_version_presence():
    version_file = os.path.join(BASE_DIR, "VERSION")
    assert os.path.exists(version_file), "VERSION file must exist"
    with open(version_file, "r", encoding="utf-8") as vf:
        ver = vf.read().strip()
    assert re.match(r"^v\d+\.\d+\.\d+", ver), f"VERSION '{ver}' must match vX.Y.Z format"

    files_to_check = [
        ("index.html", [
            'id="appFooterVersionBadge"',
            f"🏷️ {ver}",
            f"window.APP_VERSION = '{ver}';"
        ]),
        ("dist/index.html", [
            'id="appFooterVersionBadge"',
            f"🏷️ {ver}",
            f"window.APP_VERSION = '{ver}';"
        ]),
        ("login.html", [
            'id="loginCardVersionBadge"',
            'id="loginFooterVersionBadge"',
            f"🏷️ {ver}",
            f"window.APP_VERSION = '{ver}';"
        ]),
        ("dist/login.html", [
            'id="loginCardVersionBadge"',
            'id="loginFooterVersionBadge"',
            f"🏷️ {ver}",
            f"window.APP_VERSION = '{ver}';"
        ]),
    ]

    for filename, assertions in files_to_check:
        filepath = os.path.join(BASE_DIR, filename)
        assert os.path.exists(filepath), f"{filename} must exist"
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        for token in assertions:
            assert token in content, f"Missing '{token}' in {filename}"
        print(f"✓ {filename} contains all version elements for {ver}")

if __name__ == "__main__":
    test_version_presence()
    print("✨ All version checks passed successfully!")
