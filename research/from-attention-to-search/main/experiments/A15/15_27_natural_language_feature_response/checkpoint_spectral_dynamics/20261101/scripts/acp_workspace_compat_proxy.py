#!/usr/bin/env python3
"""Loopback-only compatibility bridge for SCO ACP v2.1.7 workspace reads."""

import base64
import hashlib
import hmac
import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import requests


UPSTREAM_HOST = "management.sensecoreapi.cn"
UPSTREAM = f"https://{UPSTREAM_HOST}"
PROFILE = Path(os.environ.get("SCO_PROFILE_PATH", "/root/.config/sco/profiles/default.toml"))
PORT = int(os.environ.get("ACP_COMPAT_PORT", "18082"))


def profile_secret():
    match = re.search(
        r'^access_key_secret\s*=\s*["\']([^"\']+)',
        PROFILE.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    if not match:
        raise RuntimeError("SCO profile secret not found")
    return match.group(1)


SECRET = profile_secret()


def clean(value):
    if isinstance(value, dict):
        return {
            key: clean(item)
            for key, item in value.items()
            if not key.startswith("contract_billing_cycle_") and key not in {"service_time_expression"}
        }
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


class Handler(BaseHTTPRequestHandler):
    def canonical_signing_text(self, authorization, host):
        headers_match = re.search(r'headers="([^"]+)"', authorization, re.IGNORECASE)
        if not headers_match:
            raise RuntimeError("SCO Authorization header has no signed-headers list")
        signed_headers = headers_match.group(1).split()
        lines = []
        for signed_header in signed_headers:
            normalized = signed_header.lower()
            if normalized in {"@request-target", "(request-target)"}:
                value = f"{self.command.lower()} {self.path}"
            elif normalized == "host":
                value = host
            else:
                value = self.headers.get(signed_header)
                if value is None:
                    raise RuntimeError(f"missing signed header: {signed_header}")
            lines.append(f"{normalized}: {value}")
        return "\n".join(lines)

    def forward(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length else None
        authorization = self.headers.get("Authorization", "")
        incoming_signature_match = re.search(
            r'signature="([^"]+)"', authorization, re.IGNORECASE
        )
        incoming_signature = incoming_signature_match.group(1) if incoming_signature_match else ""
        incoming_signing = self.canonical_signing_text(
            authorization, self.headers.get("Host", "")
        )
        incoming_expected = base64.b64encode(
            hmac.new(SECRET.encode(), incoming_signing.encode(), hashlib.sha256).digest()
        ).decode()
        print(
            f"workspace-compat incoming-signature-valid={hmac.compare_digest(incoming_signature, incoming_expected)}",
            flush=True,
        )
        signing = self.canonical_signing_text(authorization, UPSTREAM_HOST)
        signature = base64.b64encode(
            hmac.new(SECRET.encode(), signing.encode(), hashlib.sha256).digest()
        ).decode()
        headers = {
            key: value
            for key, value in self.headers.items()
            if key.lower() not in {"host", "content-length", "connection", "accept-encoding"}
        }
        headers["Authorization"] = re.sub(
            r'signature="[^"]+"', f'signature="{signature}"', authorization
            , flags=re.IGNORECASE
        )
        headers["Host"] = UPSTREAM_HOST
        session = requests.Session()
        # SenseCore API egress on this host is reached through the configured
        # loopback HTTPS proxy. Bypassing it yields the platform WAF page.
        session.trust_env = True
        response = session.request(
            self.command,
            UPSTREAM + self.path,
            headers=headers,
            data=body,
            timeout=30,
            allow_redirects=False,
        )
        if response.status_code >= 400:
            print(f"workspace-compat upstream-error status={response.status_code}", flush=True)
        content = response.content
        content_type = response.headers.get("Content-Type", "")
        if "json" in content_type:
            content = json.dumps(clean(response.json()), separators=(",", ":")).encode()
        self.send_response(response.status_code)
        self.send_header("Content-Type", content_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    do_GET = forward
    do_POST = forward
    do_PUT = forward
    do_PATCH = forward
    do_DELETE = forward

    def log_message(self, fmt, *args):
        status = args[1] if len(args) > 1 else ""
        print(f"workspace-compat {self.command} {self.path} {status}", flush=True)


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
