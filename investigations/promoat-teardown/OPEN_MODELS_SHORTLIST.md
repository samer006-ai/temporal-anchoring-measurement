# Open-weights audio-driven talking-video models: shortlist for local testing

Checked 2026-11-01 from each model's own card / licence (Hugging Face API + repository files).
Criteria from the owner: open weights; takes an uploaded speech file and lip-syncs **during** generation; generates the
person from a reference image; 720p or higher; commercial use allowed; usable in the UAE.
Test machine (owner's DxDiag): Windows 11 Pro, Ryzen 7 5800X, 32 GB RAM, NVIDIA RTX 3090 24 GB, **one GPU** (confirmed by
`nvidia-smi -L` on 2026-11-01; the two DxDiag display tabs are two monitors on the same card).
Consequences: LongCat's official 2-GPU context-parallel examples do not apply (use WanGP's single-GPU build); Ampere has
no native FP8 or NVFP4 compute, so fp8 files save memory but not time, and NVFP4 builds are not usable; INT8/GGUF builds
are the practical choice; with 32 GB RAM, enlarge the Windows page file before loading 19-33B models.

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
- Real-time streaming family (checked again 2026-11-01 against the GitHub READMEs, which are newer than the HF cards):
  - `Soul-AILab/SoulX-FlashTalk-14B` (Apache-2.0): single GPU needs >64 GB, or ~40 GB with `--cpu_offload`; real time needs 8xH800. Not runnable on 24 GB.
  - `Quark-Vision/Live-Avatar` (Apache-2.0): single GPU needs 80 GB, or 48 GB with FP8 (v1.1, 2026-01-20). Not runnable on 24 GB.
  - `Soul-AILab/LiveAct` (SoulX-LiveAct, Apache-2.0, 2026-03): consumer-GPU mode since 2026-03-18 (FP8 KV cache + CPU offload, ~6 fps on one RTX 4090), but output 416x720 / 480x832 / 512x512: fails the 720p rule. Untested on an RTX 3090 (no native FP8).
  - `Soul-AILab/SoulX-FlashHead-1_3B` (2026-02): real time on one RTX 4090, but 512x512 talking head and licence marked "other" with no licence file on HF: fails the 720p rule, licence unclear.
  Real time matters for live interactive avatars, not for producing finished reels, so this family is out of scope here.
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

## Hosting options (checked 2026-11-01)

Hetzner GPU line (official matrix, prices excl. VAT; locations HEL1 Helsinki and FSN1 Falkenstein, i.e. EU only):

| Server | GPU / VRAM | RAM | Monthly | Hourly | One-time setup |
|---|---|---|---|---|---|
| GEX45 | RTX PRO 4000 Blackwell SFF, 24 GB | 64 GB DDR4 | EUR 214 | EUR 0.3429 | EUR 209 |
| GEX63 | RTX PRO 6000 Blackwell Max-Q, 96 GB | 128 GB DDR5 | EUR 999 | EUR 1.6009 | EUR 999 |
| GEX131 | RTX PRO 6000 Blackwell Max-Q, 96 GB | from 256 GB DDR5 ECC | from EUR 1,499 | from EUR 2.4022 | EUR 1,499 |
| GEX430 | 4x RTX PRO 6000 Blackwell Max-Q, 4x96 GB | 128 GB DDR5 | EUR 3,599 | EUR 5.7676 | EUR 3,599 |

- Hardware does not change a model's output quality; it decides speed, whether full-precision weights fit (compressed
  builds can cost some quality), and how long / how high-resolution a clip fits in memory.
- GEX45 has the same VRAM as the local RTX 3090; its gain is native FP8/FP4 (Blackwell) and 64 GB RAM, not capacity.
- The setup fee equals one month and is charged even for hourly use: poor value for short tests, reasonable for
  always-on production.
- **Licence:** Hetzner servers are in the EU. MiniMax H3 and HunyuanVideo-Avatar licences exclude the EU, so they cannot
  be run there without a separate licence. Apache/MIT/LTX/Skywork models are not affected.
- Hourly clouds without setup fees for tests (third-party snapshots, Sep 2026, verify before use): H100 about USD 1.9-3.3/h,
  RTX 5090 about USD 0.69-0.99/h.
- Cost per video = GPU price per hour x compute time per video. Measure compute seconds per video second on the local
  3090 first, then on one rented large GPU for a day, before committing to monthly hosting.
