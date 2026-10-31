"""Portable working-state packages; standard library only, no model calls or execution."""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from uuid import UUID, uuid4

FORMAT = "agentcontinuity.resume.v1"
MAX_BYTES = 16_384
KEY = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:\-]{0,199}\Z")
HEX = re.compile(r"[0-9a-f]{64}\Z")
AGENT_KEY = re.compile(r"ac_[0-9a-f]{12}_[A-Za-z0-9_-]{43}\Z")


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON field")
        result[key] = value
    return result


def decode(data):
    if len(data) > MAX_BYTES:
        raise ValueError("Resume package exceeds 16 KiB")
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique_object,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Non-finite JSON value")))


def text(value, limit, name):
    if not isinstance(value, str) or not value.strip() or len(value.encode("utf-8")) > limit:
        raise ValueError(f"{name}: nonblank text up to {limit} UTF-8 bytes required")


def state_checked(state):
    if not isinstance(state, dict):
        raise ValueError("state must be an object")
    required = {"goal", "next_action", "status", "decisions", "rejected_approaches",
                "open_questions", "constraints", "artifacts"}
    if set(state) != required:
        raise ValueError("Unexpected or missing state fields")
    text(state["goal"], 2048, "goal")
    text(state["next_action"], 2048, "next_action")
    if state["status"] not in ("active", "blocked", "complete"):
        raise ValueError("Unsupported task status")
    for name in ("decisions", "open_questions", "constraints"):
        values = state[name]
        if not isinstance(values, list) or len(values) > 20:
            raise ValueError(f"{name}: at most 20 entries")
        for value in values:
            text(value, 1024, name)
    for name, fields in (("rejected_approaches", {"approach", "reason"}),
                         ("artifacts", {"label", "reference"})):
        values = state[name]
        if not isinstance(values, list) or len(values) > 20:
            raise ValueError(f"{name}: at most 20 entries")
        for value in values:
            if not isinstance(value, dict) or set(value) != fields:
                raise ValueError(f"{name}: unexpected or missing entry fields")
            for field in fields:
                text(value[field], 1024, f"{name}.{field}")


def make_package(state):
    if not isinstance(state, dict):
        raise ValueError("state must be an object")
    state = {"status": "active", "decisions": [], "rejected_approaches": [],
             "open_questions": [], "constraints": [], "artifacts": [], **state}
    state_checked(state)
    data = {"format": FORMAT, "created_at": datetime.now(timezone.utc).isoformat(),
            "untrusted_content": True, "state": state}
    data["package_sha256"] = hashlib.sha256(canonical(data).encode()).hexdigest()
    return validate(data)


def validate(data, expected_sha256=None):
    if not isinstance(data, dict) or set(data) != {"format", "created_at", "untrusted_content", "state", "package_sha256"}:
        raise ValueError("Unexpected or missing package fields")
    if data["format"] != FORMAT or data["untrusted_content"] is not True:
        raise ValueError("Unsupported format or missing untrusted-content marker")
    if not isinstance(data["created_at"], str):
        raise ValueError("created_at must be a timezone-aware timestamp")
    stamp = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        raise ValueError("created_at must include a timezone")
    state_checked(data["state"])
    digest = data["package_sha256"]
    if not isinstance(digest, str) or not HEX.fullmatch(digest):
        raise ValueError("Invalid package hash")
    unsigned = {k: v for k, v in data.items() if k != "package_sha256"}
    expected = hashlib.sha256(canonical(unsigned).encode()).hexdigest()
    if not hmac.compare_digest(digest, expected):
        raise ValueError("Package hash mismatch")
    if expected_sha256 is not None and (not isinstance(expected_sha256, str) or not HEX.fullmatch(expected_sha256)
                                      or not hmac.compare_digest(digest, expected_sha256)):
        raise ValueError("Package differs from the supplied expected hash")
    if len(canonical(data).encode()) > MAX_BYTES:
        raise ValueError("Resume package exceeds 16 KiB")
    return data


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward a bearer key to a redirect destination.


class Client:
    def __init__(self, token, base_url="https://api.agentcontinuity.net"):
        parts = urlsplit(base_url)
        local = parts.hostname in ("127.0.0.1", "::1", "localhost")
        if not parts.hostname or parts.username or parts.password or parts.query or parts.fragment \
                or parts.path not in ("", "/") or not (parts.scheme == "https" or parts.scheme == "http" and local):
            raise ValueError("Use an HTTPS API origin; HTTP is allowed only for loopback testing")
        if not isinstance(token, str) or not AGENT_KEY.fullmatch(token):
            raise ValueError("A scoped AgentContinuity key is required")
        self.token, self.base = token, base_url.rstrip("/")
        self.opener = build_opener(NoRedirect())

    def request(self, path, body=None, idempotency_key=None):
        headers = {"Authorization": "Bearer " + self.token, "Accept": "application/json"}
        raw = None
        if body is not None:
            raw = canonical(body).encode()
            headers.update({"Content-Type": "application/json", "Idempotency-Key": idempotency_key or str(uuid4())})
        request = Request(self.base + path, data=raw, headers=headers)
        try:
            with self.opener.open(request, timeout=20) as response:
                data = response.read(131_073)
        except HTTPError as error:
            raise ValueError(f"API returned HTTP {error.code}; no redirect or automatic retry performed") from None
        except URLError:
            raise ValueError("API request failed; check access before retrying with the same idempotency key") from None
        if len(data) > 131_072:
            raise ValueError("API response too large")
        result = json.loads(data.decode("utf-8"), object_pairs_hook=unique_object)
        if not isinstance(result, dict):
            raise ValueError("API response must be an object")
        return result

    @staticmethod
    def path(workspace, key=None):
        workspace = str(UUID(workspace))
        if key is not None and not KEY.fullmatch(key):
            raise ValueError("Invalid memory key")
        return f"/v1/workspaces/{workspace}/memories" + ("/" + quote(key, safe="") if key is not None else "")

    def save(self, workspace, key, package, expected_version=0, idempotency_key=None):
        validate(package)
        if not isinstance(key, str) or not KEY.fullmatch(key):
            raise ValueError("Invalid memory key")
        if type(expected_version) is not int or expected_version < 0:
            raise ValueError("Expected version must be a nonnegative integer")
        content = canonical(package)
        result = self.request(self.path(workspace), {
            "key": key, "content": content, "content_type": "application/json", "kind": "memory",
            "mode": "replace", "if_version": expected_version, "tags": ["resume-package", "resume-v1"]
        }, idempotency_key)
        if result.get("content_sha256") != hashlib.sha256(content.encode()).hexdigest():
            raise ValueError("Memory receipt hash mismatch; inspect the stored record before retrying")
        return result

    def load(self, workspace, key):
        result = self.request(self.path(workspace, key))
        memory = result.get("memory", {})
        if not isinstance(memory, dict) or type(memory.get("version")) is not int or memory["version"] < 1:
            raise ValueError("Invalid memory response")
        content = memory.get("content")
        if memory.get("client_encrypted") or not isinstance(content, str):
            raise ValueError("Use a compatible client-side encryption client for encrypted records")
        if memory.get("content_sha256") != hashlib.sha256(content.encode()).hexdigest():
            raise ValueError("Stored memory hash mismatch")
        package = validate(decode(content.encode()))
        return {"package": package, "memory_version": memory["version"], "expires_at": memory.get("expires_at"),
                "untrusted_content": True}


def write_new(path, value):
    encoded = (canonical(value) + "\n").encode()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(encoded)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("pack", "verify", "save", "load"))
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--workspace")
    parser.add_argument("--key")
    parser.add_argument("--expected-version", type=int, default=0)
    parser.add_argument("--idempotency-key")
    parser.add_argument("--expected-sha256", help="Package hash obtained through a separately trusted channel")
    parser.add_argument("--base-url", default="https://api.agentcontinuity.net")
    args = parser.parse_args(argv)
    try:
        package = None
        if args.command != "load":
            if not args.input:
                raise ValueError("--input required")
            with args.input.open("rb") as stream:
                data = decode(stream.read(MAX_BYTES + 1))
            package = make_package(data) if args.command == "pack" else validate(data, args.expected_sha256)
        if args.command in ("pack", "load") and not args.output:
            raise ValueError("--output required; output files must be new")
        if args.command in ("save", "load"):
            if not args.workspace or not args.key or not KEY.fullmatch(args.key):
                raise ValueError("--workspace and a valid --key required")
            client = Client(os.environ.get("AGENTCONTINUITY_API_KEY", ""), args.base_url)
            if args.command == "save":
                if not args.idempotency_key:
                    raise ValueError("save requires a stable --idempotency-key")
                receipt = client.save(args.workspace, args.key, package, args.expected_version, args.idempotency_key)
                print(canonical({"saved": True, "version": receipt["version"], "expires_at": receipt.get("expires_at")}))
            else:
                loaded = client.load(args.workspace, args.key)
                validate(loaded["package"], args.expected_sha256)
                write_new(args.output, loaded["package"])
                print(canonical({"loaded": True, "memory_version": loaded["memory_version"],
                                 "expires_at": loaded["expires_at"], "untrusted_content": True}))
        elif args.command == "pack":
            write_new(args.output, package)
            print(canonical({"packed": True, "package_sha256": package["package_sha256"]}))
        else:
            print(canonical({"valid": True, "untrusted_content": True, "signature_verified": False}))
        return 0
    except (ValueError, OSError, KeyError, TypeError):
        # Do not print file contents, server response bodies, request headers or credentials.
        print("Resume operation failed: check format, size, output path, API access and expected version.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
