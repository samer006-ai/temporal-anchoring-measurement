#!/usr/bin/env python3
"""Rebuild BENCHMARK_RESULTS.csv from benchmark/outputs/<run>/ files.
Per run: run.json (from run_job.py), video.av.json (av_analyze.py), asr.json (asr_check.py), review.json (manual review).
USD values use the Weekly plan rate (9.99 / 559 credits)."""
import csv, json, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "benchmark" / "outputs"
RATE = 9.99 / 559
def load(p):
    try: return json.load(open(p, encoding="utf-8"))
    except Exception: return {}
def ts(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None
cols = ["run_id", "case", "attempt", "raw_or_tuned", "mode", "language", "input_summary", "submitted_utc",
        "queue_wait_s_upper", "server_time_s", "submit_to_download_s", "status", "error_code",
        "credits_quoted", "credits_consumed", "extra_credits_same_case", "usd_at_weekly_rate",
        "width", "height", "fps", "duration_s", "loudness_note", "scene_cuts", "watermark_visible",
        "asr_wer", "asr_cer", "lipsync_lag_ms", "lipsync_corr", "mouth_open_in_silence", "identity_vs_sheet_mean",
        "identity_within_min", "visual_review", "audio_review", "acceptable", "output_path", "notes"]
rows = []
for d in sorted(p for p in OUT.iterdir() if p.is_dir()):
    run, av, asr, rv = load(d / "run.json"), load(d / "video.av.json"), load(d / "asr.json"), load(d / "review.json")
    if not run and not rv: continue
    st = run.get("final_status", {}).get("status") if "final_status" in run else None
    fs = run.get("final_status") or load(d / "final_status.json").get("status", {})
    q, c = ts(fs.get("queued_at")), ts(fs.get("completed_at"))
    pr = av.get("probe", {}); lp = av.get("lipsync_proxy", {}); idp = av.get("identity_proxy", {})
    consumed = fs.get("credits_consumed", run.get("credits_consumed"))
    quoted = (run.get("estimate") or {}).get("credits_required", run.get("estimate_credits"))
    extra = rv.get("extra_credits_same_case", 0)
    usd = round(((consumed or 0) + extra) * RATE, 3) if consumed is not None else ""
    rows.append({
        "run_id": d.name, "case": rv.get("case", d.name.split("_")[0]), "attempt": rv.get("attempt", 1),
        "raw_or_tuned": rv.get("raw_or_tuned", "raw"), "mode": rv.get("mode", (run.get("request") or {}).get("mode")),
        "language": rv.get("language", ""), "input_summary": rv.get("input_summary", ""),
        "submitted_utc": run.get("submitted_utc", ""), "queue_wait_s_upper": run.get("queue_wait_s", run.get("queue_wait_s_upper_bound", "")),
        "server_time_s": round((c - q).total_seconds(), 1) if q and c else "",
        "submit_to_download_s": run.get("submit_to_downloaded_s", run.get("submit_to_terminal_s_polled", "")),
        "status": fs.get("status", st or run.get("aborted", "")), "error_code": fs.get("error_code") or "",
        "credits_quoted": quoted, "credits_consumed": consumed, "extra_credits_same_case": extra, "usd_at_weekly_rate": usd,
        "width": pr.get("width", ""), "height": pr.get("height", ""), "fps": pr.get("fps", ""), "duration_s": pr.get("duration_s", ""),
        "loudness_note": rv.get("loudness_note", ""), "scene_cuts": len(av.get("scene_cuts_s", [])) if av else "",
        "watermark_visible": rv.get("watermark_visible", ""), "asr_wer": asr.get("wer", ""), "asr_cer": asr.get("cer", ""),
        "lipsync_lag_ms": lp.get("best_lag_ms", ""), "lipsync_corr": lp.get("corr_at_best", ""),
        "mouth_open_in_silence": lp.get("open_mouth_during_silence_share", ""),
        "identity_vs_sheet_mean": idp.get("vs_ref_mean", ""), "identity_within_min": idp.get("vs_first_frame_min", ""),
        "visual_review": rv.get("visual_review", ""), "audio_review": rv.get("audio_review", "pending owner listening"),
        "acceptable": rv.get("acceptable", "pending"), "output_path": f"benchmark/outputs/{d.name}/", "notes": rv.get("notes", ""),
    })
with open(ROOT / "BENCHMARK_RESULTS.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); [w.writerow(r) for r in rows]
print(len(rows), "rows")
