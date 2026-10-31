"""Automatic (non-human) measurements for a generated video.

Usage: python av_analyze.py <video.mp4> <outdir> [--ref-face ref.jpg] [--models DIR]

Outputs <outdir>/<stem>.av.json and <stem>.contact.jpg (12 evenly spaced frames for visual review).
Measures:
  - container/stream metadata (ffprobe): resolution, fps, duration, codecs, bitrates, encoder tags
  - shot cuts (ffmpeg scene score > 0.3)
  - lip-sync proxy: per-frame jawOpen blendshape (MediaPipe FaceLandmarker) vs. audio RMS envelope;
    best cross-correlation lag in ms (+ = mouth lags audio) and correlation at best lag / at 0;
    share of silent frames with an open mouth ("talking during silence")
  - identity proxy: SFace cosine similarity of sampled frames vs. a reference face (and frame-to-frame);
    OpenCV's documented same-identity threshold for SFace cosine is 0.363.
These are proxies, not perceptual scores; they flag problems for human review.
"""
import argparse, json, os, subprocess, sys
import numpy as np, cv2

def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout

def probe(path):
    j = json.loads(sh(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", path]))
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), {})
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), {})
    num, den = (v.get("avg_frame_rate", "0/1").split("/") + ["1"])[:2]
    return {
        "width": v.get("width"), "height": v.get("height"), "fps": round(float(num) / float(den or 1), 3) if float(den or 1) else None,
        "duration_s": float(j["format"].get("duration", 0)), "video_codec": v.get("codec_name"), "profile": v.get("profile"),
        "pix_fmt": v.get("pix_fmt"), "video_bitrate": v.get("bit_rate"), "audio_codec": a.get("codec_name"),
        "audio_sample_rate": a.get("sample_rate"), "audio_channels": a.get("channels"), "audio_bitrate": a.get("bit_rate"),
        "format_tags": j["format"].get("tags", {}), "video_tags": v.get("tags", {}), "audio_tags": a.get("tags", {}),
        "size_bytes": int(j["format"].get("size", 0)),
    }

def scene_cuts(path):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-vf", "select='gt(scene,0.3)',showinfo", "-an", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    ts = []
    for line in out.splitlines():
        if "showinfo" in line and "pts_time:" in line:
            ts.append(round(float(line.split("pts_time:")[1].split()[0]), 2))
    return ts

def audio_rms_per_frame(path, fps, n_frames):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
    a = np.frombuffer(pcm, dtype=np.float32)
    if a.size == 0:
        return np.zeros(n_frames)
    hop = 16000.0 / fps
    rms = np.array([np.sqrt(np.mean(a[int(i * hop): int((i + 1) * hop)] ** 2) + 1e-12) if int(i * hop) < a.size else 0.0 for i in range(n_frames)])
    return rms

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("outdir")
    ap.add_argument("--ref-face"); ap.add_argument("--models", default=os.environ.get("MODELS_DIR", "."))
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(args.video))[0]
    res = {"file": os.path.basename(args.video), "probe": probe(args.video)}
    res["scene_cuts_s"] = scene_cuts(args.video)

    from mediapipe.tasks.python import vision, BaseOptions
    import mediapipe as mp
    lm = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=os.path.join(args.models, "face_landmarker.task")),
        output_face_blendshapes=True, num_faces=1))
    det = cv2.FaceDetectorYN.create(os.path.join(args.models, "face_detection_yunet_2023mar.onnx"), "", (320, 320), 0.8)
    rec = cv2.FaceRecognizerSF.create(os.path.join(args.models, "face_recognition_sface_2021dec.onnx"), "")

    def embed(img):
        h, w = img.shape[:2]; det.setInputSize((w, h)); _, faces = det.detect(img)
        if faces is None or len(faces) == 0: return None
        f = max(faces, key=lambda x: x[2] * x[3])
        return rec.feature(rec.alignCrop(img, f))

    ref_emb = None
    if args.ref_face:
        ref_img = cv2.imread(args.ref_face); ref_emb = embed(ref_img)

    cap = cv2.VideoCapture(args.video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    jaw, frames_for_sheet, embs = [], [], []
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    sheet_idx = set(np.linspace(0, max(n - 1, 0), 12).astype(int).tolist())
    emb_idx = set(np.linspace(0, max(n - 1, 0), 24).astype(int).tolist())
    i = 0
    while True:
        ok, fr = cap.read()
        if not ok: break
        rgb = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)
        r = lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
        val = np.nan
        if r.face_blendshapes:
            val = next((b.score for b in r.face_blendshapes[0] if b.category_name == "jawOpen"), np.nan)
        jaw.append(val)
        if i in sheet_idx: frames_for_sheet.append((i, fr.copy()))
        if i in emb_idx:
            e = embed(fr); embs.append((i, e))
        i += 1
    n = i
    jaw = np.array(jaw, dtype=float)
    rms = audio_rms_per_frame(args.video, fps, n)
    face_cov = float(np.mean(~np.isnan(jaw))) if n else 0.0
    res["face_detected_share"] = round(face_cov, 3)
    lip = {}
    if n > 10 and face_cov > 0.3 and rms.max() > 0:
        j = np.where(np.isnan(jaw), np.nanmean(jaw), jaw)
        z = lambda x: (x - x.mean()) / (x.std() + 1e-9)
        jz, az = z(j), z(rms)
        lags = range(-12, 13)
        cc = {L: float(np.corrcoef(jz[max(0, L):n + min(0, L)], az[max(0, -L):n - max(0, L)])[0, 1]) for L in lags}
        best = max(cc, key=cc.get)
        silent = rms < (0.1 * np.percentile(rms, 95))
        open_mouth = j > max(0.15, np.percentile(j, 60))
        lip = {"best_lag_frames": best, "best_lag_ms": round(1000 * best / fps), "corr_at_best": round(cc[best], 3),
               "corr_at_0": round(cc[0], 3), "silent_frame_share": round(float(silent.mean()), 3),
               "open_mouth_during_silence_share": round(float((silent & open_mouth).sum() / max(silent.sum(), 1)), 3)}
    res["lipsync_proxy"] = lip
    ident = {}
    good = [(k, e) for k, e in embs if e is not None]
    if good:
        if ref_emb is not None:
            sims = [float(rec.match(ref_emb, e, cv2.FaceRecognizerSF_FR_COSINE)) for _, e in good]
            ident.update({"vs_ref_mean": round(np.mean(sims), 3), "vs_ref_min": round(np.min(sims), 3), "frames": len(sims)})
        base = good[0][1]
        within = [float(rec.match(base, e, cv2.FaceRecognizerSF_FR_COSINE)) for _, e in good[1:]]
        if within: ident.update({"vs_first_frame_mean": round(np.mean(within), 3), "vs_first_frame_min": round(np.min(within), 3)})
        ident["frames_with_face_of_24"] = len(good)
    res["identity_proxy"] = ident
    if frames_for_sheet:
        th = []
        for k, fr in frames_for_sheet:
            h, w = fr.shape[:2]; s = 360 / h; t = cv2.resize(fr, (int(w * s), 360))
            cv2.putText(t, f"{k / fps:.1f}s", (8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2); th.append(t)
        rows = [np.hstack(th[r:r + 6]) for r in range(0, len(th), 6)]
        wmax = max(r.shape[1] for r in rows); rows = [np.pad(r, ((0, 0), (0, wmax - r.shape[1]), (0, 0))) for r in rows]
        cv2.imwrite(os.path.join(args.outdir, stem + ".contact.jpg"), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
    lm.close()
    json.dump(res, open(os.path.join(args.outdir, stem + ".av.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main()
