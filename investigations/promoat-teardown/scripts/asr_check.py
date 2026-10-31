"""Transcribe an audio/video file with faster-whisper (local, CPU) and compare with the reference script.
Usage: python asr_check.py <media> <reference_text> [model]
Prints transcript, WER and CER after light Arabic normalisation (diacritics, alef/ya/ta-marbuta forms, punctuation).
Automatic measure only: Whisper is itself imperfect on Levantine dialect, so WER is an upper bound on errors."""
import re, sys, json
from faster_whisper import WhisperModel
import jiwer, subprocess, numpy as np
def norm(t):
    t = re.sub(r"[ً-ْٰـ]", "", t)          # tashkeel + tatweel
    t = re.sub(r"[إأآا]", "ا", t); t = t.replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي")
    t = re.sub(r"[^\w\s]", " ", t); t = re.sub(r"\s+", " ", t).strip()
    return t
media, ref = sys.argv[1], sys.argv[2]
model_name = sys.argv[3] if len(sys.argv) > 3 else "large-v3"
m = WhisperModel(model_name, device="cpu", compute_type="int8")
pcm = subprocess.run(["ffmpeg","-v","error","-i",media,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True,check=True).stdout
audio = np.frombuffer(pcm, dtype=np.float32)
segs, info = m.transcribe(audio, language="ar", beam_size=5, vad_filter=False)
segs = list(segs)
hyp = " ".join(s.text.strip() for s in segs)
out = {"model": model_name, "transcript": hyp, "ref": ref,
       "wer": round(jiwer.wer(norm(ref), norm(hyp)), 3), "cer": round(jiwer.cer(norm(ref), norm(hyp)), 3),
       "segments": [[round(s.start, 2), round(s.end, 2), s.text.strip()] for s in segs]}
print(json.dumps(out, ensure_ascii=False, indent=1))
