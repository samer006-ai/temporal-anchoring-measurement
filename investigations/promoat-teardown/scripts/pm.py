#!/usr/bin/env python3
"""Minimal Promoat Partner API client for the research account (stdlib only).

Key is read from env PROMOAT_KEY (never written to disk by this script).
Every call is appended to evidence/api/calls.jsonl with timing, status and a redacted body
(signed-URL query strings stripped, keys redacted).

Usage:
  pm.py GET  /usage/summary
  pm.py POST /videos/estimate body.json [--idem KEY]
  pm.py DELETE /voices/ID
"""
import json, os, re, sys, time, urllib.request, urllib.error, datetime, pathlib
BASE = "https://platform.promoat.ai/api/partner/v1"
LOG = pathlib.Path(__file__).resolve().parent.parent / "evidence" / "api" / "calls.jsonl"

def redact(s: str) -> str:
    s = re.sub(r"pmat_[A-Za-z0-9_-]+", "pmat_<REDACTED>", s)
    # strip query strings from URLs (signed links), keep host+path
    s = re.sub(r"(https://[^\s\"'?]+)\?[^\s\"']*", r"\1?<QUERY_REDACTED>", s)
    return s

def call(method, path, body=None, idem=None, timeout=180):
    key = os.environ["PROMOAT_KEY"]
    data = json.dumps(body, ensure_ascii=False).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header("Authorization", "Bearer " + key)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    if idem:
        req.add_header("Idempotency-Key", idem)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status, raw = r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        status, raw = e.code, e.read().decode("utf-8", "replace")
    dt = round(time.time() - t0, 3)
    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = raw
    LOG.parent.mkdir(parents=True, exist_ok=True)
    rec = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "method": method, "path": path, "idempotency_key": idem, "status": status, "elapsed_s": dt,
           "request": body, "response": parsed}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(redact(json.dumps(rec, ensure_ascii=False)) + "\n")
    return status, parsed, raw, dt

if __name__ == "__main__":
    m, p = sys.argv[1], sys.argv[2]
    body = None; idem = None
    rest = sys.argv[3:]
    if "--idem" in rest:
        i = rest.index("--idem"); idem = rest[i + 1]; rest = rest[:i] + rest[i + 2:]
    if rest:
        body = json.load(open(rest[0], encoding="utf-8"))
    st, parsed, raw, dt = call(m, p, body, idem)
    print(st, f"{dt}s")
    print(redact(json.dumps(parsed, ensure_ascii=False, indent=1) if not isinstance(parsed, str) else raw)[:6000])
