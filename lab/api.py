#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local mock ad-platform API for the Performance Marketing Operator Lab.

Serves the kit's synthetic data on loopback only. Two "platforms" behind one port:
  * Meta-like:   GET /meta/v1/account,   GET /meta/v1/insights   (cursor pagination)
  * Google-like: GET /google/v1/account, GET /google/v1/reports  (pageToken pagination, cost_micros)

Run:  python3 lab/api.py [--port 8781] [--kit .]
Tokens: see data/lab_credentials.json (or `bash lab/status.sh`).
"""
import argparse, base64, json, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parents[1]
HITS = []


def load(root: Path):
    kit = json.loads((root / "kit.json").read_text())
    meta = json.loads((root / "data" / "ads" / "meta_insights.json").read_text())
    google = json.loads((root / "data" / "ads" / "google_insights.json").read_text())
    creds = json.loads((root / "data" / "lab_credentials.json").read_text())
    return kit, meta, google, creds


class Handler(BaseHTTPRequestHandler):
    root = None
    kit = meta = google = creds = None

    def log_message(self, *a):  # keep the terminal quiet
        pass

    def _send(self, code, payload, headers=None):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _auth(self, header_name, expected):
        got = self.headers.get("Authorization", "")
        return got == f"Bearer {expected}"

    def _rate_limited(self):
        now = time.time()
        HITS[:] = [t for t in HITS if now - t < 5.0]
        HITS.append(now)
        return len(HITS) > 25

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        if u.path == "/status":
            return self._send(200, dict(ok=True, window=dict(start=self.kit["window_start"],
                                                             end=self.kit["window_end"]),
                                        candidate_id=self.kit["candidate_id"]))
        if self._rate_limited():
            return self._send(429, dict(error="rate_limited", detail="slow down"),
                              {"Retry-After": "1"})

        if u.path == "/meta/v1/account":
            if not self._auth("Authorization", self.creds["meta_token"]):
                return self._send(401, dict(error="unauthorized"))
            return self._send(200, self.meta["account"])

        if u.path == "/meta/v1/insights":
            if not self._auth("Authorization", self.creds["meta_token"]):
                return self._send(401, dict(error="unauthorized"))
            level = q.get("level", "campaign")
            if level != "campaign":
                return self._send(400, dict(error="unsupported_level", detail="lab serves level=campaign"))
            try:
                limit = min(int(q.get("limit", "10")), 50)
            except ValueError:
                return self._send(400, dict(error="bad_limit"))
            since, until = q.get("since"), q.get("until")
            rows = []
            for c in self.meta["campaigns"]:
                for d in c["daily"]:
                    if since and d["date"] < since:
                        continue
                    if until and d["date"] > until:
                        continue
                    rows.append(dict(campaign_id=c["id"], campaign_name=c["name"], date=d["date"],
                                     spend=d["spend"], impressions=d["impressions"], clicks=d["clicks"],
                                     results=d["platform_leads"]))
            rows.sort(key=lambda r: (r["date"], r["campaign_id"]))
            offset = 0
            if q.get("cursor"):
                try:
                    offset = int(base64.urlsafe_b64decode(q["cursor"] + "==").decode())
                except Exception:
                    return self._send(400, dict(error="bad_cursor"))
            page = rows[offset: offset + limit]
            nxt = None
            if offset + limit < len(rows):
                nxt = base64.urlsafe_b64encode(str(offset + limit).encode()).decode().rstrip("=")
            return self._send(200, dict(data=page, next_cursor=nxt, total_count=len(rows)))

        if u.path == "/google/v1/account":
            if not self._auth("Authorization", self.creds["google_token"]):
                return self._send(401, dict(error="unauthorized"))
            return self._send(200, self.google["account"])

        if u.path == "/google/v1/reports":
            if not self._auth("Authorization", self.creds["google_token"]):
                return self._send(401, dict(error="unauthorized"))
            try:
                size = min(int(q.get("pageSize", "25")), 100)
            except ValueError:
                return self._send(400, dict(error="bad_page_size"))
            since, until = q.get("dateFrom"), q.get("dateTo")
            rows = []
            for c in self.google["campaigns"]:
                for d in c["daily"]:
                    if since and d["date"] < since:
                        continue
                    if until and d["date"] > until:
                        continue
                    rows.append(dict(campaign_id=c["id"], campaign_name=c["name"], date=d["date"],
                                     cost_micros=d["spend"] * 1_000_000, impressions=d["impressions"],
                                     clicks=d["clicks"], conversions=d["platform_leads"]))
            rows.sort(key=lambda r: (r["date"], r["campaign_id"]))
            page = 1
            if q.get("pageToken"):
                try:
                    page = int(base64.urlsafe_b64decode(q["pageToken"] + "==").decode())
                except Exception:
                    return self._send(400, dict(error="bad_page_token"))
            start = (page - 1) * size
            chunk = rows[start: start + size]
            nxt = None
            if start + size < len(rows):
                nxt = base64.urlsafe_b64encode(str(page + 1).encode()).decode().rstrip("=")
            return self._send(200, dict(rows=chunk, nextPageToken=nxt, totalRows=len(rows)))

        return self._send(404, dict(error="not_found", path=u.path))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8781)
    ap.add_argument("--kit", default=str(ROOT))
    a = ap.parse_args()
    root = Path(a.kit).resolve()
    kit, meta, google, creds = load(root)
    Handler.root, Handler.kit, Handler.meta, Handler.google, Handler.creds = root, kit, meta, google, creds
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    print(f"mock ad API on http://127.0.0.1:{a.port} (kit: {root.name}, window {kit['window_start']}..{kit['window_end']})")
    srv.serve_forever()


if __name__ == "__main__":
    main()
