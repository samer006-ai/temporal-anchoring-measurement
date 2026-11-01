# Open-weights audio-driven talking-video models: shortlist for local testing

Checked 2026-11-01 from each model's own card / licence (Hugging Face API + repository files).
Criteria from the owner: open weights; takes an uploaded speech file and lip-syncs **during** generation; generates the
person from a reference image; 720p or higher; commercial use allowed; usable in the UAE.
Test machine (owner's DxDiag): Windows 11 Pro, Ryzen 7 5800X, 32 GB RAM, NVIDIA RTX 3090 24 GB (DxDiag shows two
display tabs with an RTX 3090; whether that is one card with two monitors or two cards is to be confirmed with `nvidia-smi -L`).

## A. Meets every criterion

| Model (HF id) | Released | Resolution | Licence (commercial, UAE) | Local route on a 24 GB card | Notes |
|---|---|---|---|---|---|
| `meituan-longcat/LongCat-Video-Avatar-1.5` | 2026-05-21 | 480P / 720P | MIT | WanGP (`longcat_avatar_v1_5`); `--use_int8` in the official code | Whisper-Large audio encoder (multilingual): best a-priori fit for Arabic; official examples use 2 GPUs |
| `MeiGen-AI/InfiniteTalk` | 2025-08-18 | 480P / 720P | Apache-2.0 (base Wan2.1 Apache-2.0; audio encoder chinese-wav2vec2 MIT) | WanGP (`infinitetalk`), ComfyUI (kijai WanVideoWrapper), official low-VRAM flag | Audio encoder trained on Chinese: Arabic lip accuracy must be tested |
| `Wan-AI/Wan2.2-S2V-14B` | 2025-08-25 | 480P / 720P (size = area, e.g. 1024*704) | Apache-2.0 | ComfyUI native support / GGUF quants; official single-GPU command needs 80 GB | Cinematic speech-to-video from image + audio; pose-driven option |
| `GAIR/daVinci-MagiHuman` | 2026-03-21 | up to 1080p via latent super-resolution | Apache-2.0 | WanGP (`magi_human`, `magi_human_distill`) "follows supplied audio" | 15B single-stream audio-video model; can also generate its own speech; fastest in its own report (5 s 1080p in 38 s on H100) |
| `Lightricks/LTX-2.5` (A2VidPipelineTwoStage) | 2026-07-23 | 720p+ (two-stage upsampling) | LTX-2.x Community Licence: free incl. commercial for entities under USD 10M annual revenue; paid licence above; no territorial exclusion found | WanGP (LTX 2.5), official pipelines; fp8 / GGUF builds exist | Audio-to-video conditioned on an input audio file plus image conditioning (verified in pipeline code) |
| `Skywork/SkyReels-V3-A2V-19B` | 2026-01-19 | 720P default (540P/480P options), 24 fps, 5-30 s per shot, minute-level with extension | Skywork Community Licence: worldwide, royalty-free, commercial allowed, revocable; no military use; PRC law | Official code with `--low_vram` (FP8 weight-only + block offload); likely Linux/WSL | `--task_type talking_avatar` with input image + audio; up to 4 reference images |

## B. Allowed in the UAE but with restrictions that matter for a public video product

| Model | Released | Resolution | Licence | Local route | Why conditional |
|---|---|---|---|---|---|
| `MiniMaxAI/MiniMax-H3` (Ref2VA) | 2026-07-28 | 768p default, 2K via Regenerate | MiniMax H3 Community Licence | WanGP (`minimax_h3_ref2va_pruned`, "Soundtrack Kept"); WanGP claims 5-6 GB VRAM for 15 s at 480p | Excludes EU/UK/US/South Korea and forbids using or **displaying outputs** there; must show "MiniMax H3" in the product UI; written authorisation above USD 20M revenue. Strongest candidate for Promoat's engine (FP-06) |
| `tencent/HunyuanVideo-Avatar` | 2025-05-26 | 704 px | Tencent Hunyuan Community Licence | Official code, fp8, "very low VRAM" mode | Excludes EU/UK/South Korea including display of outputs; separate licence above 100M MAU; older generation |

Customer videos posted on public social media are viewable in the excluded territories, so B-models need legal review
before commercial use even though the UAE itself is inside the licensed territory.

## C. Secondary (meet the rules but weaker for this use)
- `bytedance-research/HuMo` (Apache-2.0, 480P/720P): trained on 97 frames at 25 fps (~4 s per generation).
- `BadToBest/EchoMimicV3` (Apache-2.0, 720P models): 1.3B, lighter and lower quality.
- `acvlab/FantasyTalking` (Apache-2.0): Wan2.1-720P based, tested at 512x512, April 2025.

## D. Excluded
- `OmniAvatar/OmniAvatar-14B`: "480p only for now". `FrancisRing/StableAvatar`: 480x832. `MeiGen-AI/MeiGen-MultiTalk`: superseded by InfiniteTalk.
- `Soul-AILab/SoulX-FlashTalk-14B` (>64 GB single GPU) and `Quark-Vision/Live-Avatar` (80 GB; 5xH800 for real time): real-time streaming systems, not runnable on one 24 GB card.
- `chetwinlow1/Ovi`, Kandinsky 6: generate their own speech; no uploaded speech file.
- Post-hoc lip-sync tools (LatentSync, MuseTalk, Wav2Lip family): not lip-sync during generation.
- Kling 4.0 / Kling Avatar, OmniHuman, Seedance, Wan 2.5/2.6, HeyGen, Hedra: closed weights.

## Fair test protocol (same for every model)
1. Inputs: the same first-frame image and the same Levantine clips used on Promoat (3.6 s opening line; 13.6 s full S2),
   plus one MSA clip. All synthetic, in the private report page.
2. 720p, default settings first ("raw"), then one tuned run per model ("tuned"), reported separately.
3. Record per run: seconds of compute per second of video, peak VRAM, any crash/OOM, output resolution/fps.
4. Automatic measures with `scripts/av_analyze.py` and `scripts/asr_check.py` (lip-sync lag/correlation, identity vs.
   reference, mouth open in silence, ASR word error rate); human listening for Arabic/Levantine pronunciation.
5. Order: WanGP models first (one install: LongCat Avatar 1.5, InfiniteTalk, Magi Human, LTX 2.5, H3 Ref2VA),
   then ComfyUI for Wan2.2-S2V, then the official SkyReels-V3 and HunyuanVideo-Avatar code.

## Sources
- Model cards and licences: huggingface.co/{each id above}; LTX licence github.com/Lightricks/LTX-2/blob/main/LICENSE-2;
  A2Vid pipeline github.com/Lightricks/LTX-2 (packages/ltx-pipelines/src/ltx_pipelines/a2vid_two_stage.py);
  Skywork Community Licence (github.com/SkyworkAI/Skywork); Hunyuan licence github.com/Tencent-Hunyuan/HunyuanVideo-Avatar/blob/main/LICENSE;
  MiniMax H3 LICENSE on its HF repo; WanGP model guide github.com/deepbeepmeep/Wan2GP/blob/main/docs/MODELS.md.
