#!/usr/bin/env python3
"""Run one benchmark video job safely and record everything.

Usage: run_job.py <run_id> <body.json> [--endpoint /videos | /videos/<wf>/fix-scene ...] [--max-credits N]

Steps: balance -> free estimate (or dry_run for edits) -> refuse if quote > --max-credits ->
POST with expected_credits + Idempotency-Key "<run_id>" -> poll every 9 s (status, phase, progress) ->
download video/poster -> balance. Writes benchmark/outputs/<run_id>/run.json and timeline.jsonl.
Re-running with the same run_id re-uses the idempotency key, so a crash/retry never creates a second job.
"""
import json, os, sys, time, subprocess, datetime, pathlib
sys.path.insert(0, os.path.dirname(__file__))
from pm import call, redact

ROOT = pathlib.Path(__file__).resolve().parent.parent / "benchmark" / "outputs"
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

def balance():
    return call("GET", "/usage/summary")[1]["credits_balance"]

def main():
    run_id, body_path = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]
    endpoint = args[args.index("--endpoint") + 1] if "--endpoint" in args else "/videos"
    max_credits = int(args[args.index("--max-credits") + 1]) if "--max-credits" in args else 80
    body = json.load(open(body_path, encoding="utf-8"))
    out = ROOT / run_id; out.mkdir(parents=True, exist_ok=True)
    rec = {"run_id": run_id, "endpoint": endpoint, "request": body, "started_utc": now()}
    rec["balance_before"] = balance()
    is_edit = endpoint != "/videos"
    if is_edit:
        st, q, _, _ = call("POST", endpoint, dict(body, dry_run=True))
        quote = q.get("credits_quoted") or q.get("credits_required") or q.get("credits_reserved")
    else:
        st, q, _, _ = call("POST", "/videos/estimate", body)
        quote = q.get("credits_required")
    rec["estimate_status"], rec["estimate"] = st, q
    print("quote", quote, "balance", rec["balance_before"])
    if st != 200 or quote is None or quote > max_credits or quote > rec["balance_before"]:
        rec["aborted"] = f"estimate status {st}, quote {quote}, cap {max_credits}, balance {rec['balance_before']}"
        json.dump(rec, open(out / "run.json", "w"), ensure_ascii=False, indent=1); print(rec["aborted"]); return
    t_submit = time.time(); rec["submitted_utc"] = now()
    st, r, _, _ = call("POST", endpoint, dict(body, expected_credits=quote), idem=run_id)
    rec["submit_status"], rec["submit_response"] = st, r
    print("submit", st, json.dumps(r, ensure_ascii=False)[:400])
    wf = r.get("workflow_id") if isinstance(r, dict) else None
    if st != 200 or not wf:
        rec["balance_after"] = balance(); json.dump(rec, open(out / "run.json", "w"), ensure_ascii=False, indent=1); return
    tl = open(out / "timeline.jsonl", "a", encoding="utf-8")
    first_running = None; last = None
    while True:
        st, s, _, dt = call("GET", f"/jobs/{wf}/status")
        el = round(time.time() - t_submit, 1)
        line = {"t_s": el, "status": s.get("status"), "phase": s.get("phase"), "progress": s.get("progress")}
        tl.write(json.dumps(line) + "\n"); tl.flush()
        if (line["status"], line["phase"], line["progress"]) != last:
            print(el, line); last = (line["status"], line["phase"], line["progress"])
        if s.get("status") == "running" and first_running is None: first_running = el
        if s.get("status") in ("completed", "failed", "cancelled"): break
        if el > 75 * 60: rec["note"] = "stopped polling after 75 min"; break
        time.sleep(9)
    rec["final_status"] = s
    rec["queue_wait_s"] = first_running
    rec["submit_to_terminal_s"] = round(time.time() - t_submit, 1)
    res = s.get("result") or s
    for key, fname in (("video_url", "video.mp4"), ("poster_url", "poster.jpg")):
        u = res.get(key) or s.get(key)
        if u:
            subprocess.run(["curl", "-sS", "-f", "-o", str(out / fname), u], check=True)
    rec["submit_to_downloaded_s"] = round(time.time() - t_submit, 1)
    rec["balance_after"] = balance()
    rec["balance_delta"] = rec["balance_after"] - rec["balance_before"]
    rec["finished_utc"] = now()
    open(out / "run.json", "w", encoding="utf-8").write(redact(json.dumps(rec, ensure_ascii=False, indent=1)))
    print("DONE", s.get("status"), "credits_consumed", s.get("credits_consumed"), "delta", rec["balance_delta"], "total_s", rec["submit_to_downloaded_s"])

if __name__ == "__main__":
    main()
