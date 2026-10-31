#!/usr/bin/env python3
import http.cookiejar
import json
import pathlib
import urllib.error
import urllib.request

BASE_URL = "http://127.0.0.1:8787"
password_lines = pathlib.Path("data/initial_login.txt").read_text(encoding="utf-8").splitlines()
password = next(line.split(": ", 1)[1] for line in password_lines if line.startswith("Password: "))

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

login_request = urllib.request.Request(
    BASE_URL + "/api/login",
    data=json.dumps({"password": password}).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with opener.open(login_request) as response:
    assert response.status == 200
assert len(cookie_jar) == 1

change_request = urllib.request.Request(
    BASE_URL + "/api/change-password",
    data=json.dumps({
        "currentPassword": "definitely-wrong",
        "newPassword": "A-valid-new-password-123!",
    }).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)
try:
    opener.open(change_request)
    raise AssertionError("Wrong current password was accepted")
except urllib.error.HTTPError as exc:
    assert exc.code == 401
    assert json.load(exc)["error"] == "CURRENT_PASSWORD_INCORRECT"

print("Authentication and password-management checks passed.")
