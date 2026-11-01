# Promoat (ProMoat): technical and commercial teardown

Investigation date: 2026-10-31 (UTC). Every claim carries an evidence ID that resolves in `EVIDENCE_INDEX.csv`.
Evidence types: **OBSERVED** (we saw or measured it), **OFFICIAL** (the company says it; not independently verified),
**INDEPENDENT** (third party), **INFERENCE** (clues, alternatives and confidence stated), **UNKNOWN**.
OSINT details (company, founders, timeline, reviews) are in `evidence/osint/OSINT_FINDINGS.md` (IDs `OS-xx`).

Scope note: this document studies Promoat only, to learn how it works and which of its patterns are worth rebuilding
originally. It contains no information about any other product. Nothing here copies Promoat code, assets or text;
"patterns worth rebuilding" means ideas re-implemented from scratch.

---

## 1. Identity check (is this the right Promoat?)

| Check | Result | Evidence |
|---|---|---|
| promoat.ai links the Play package `com.hexaflow_ai.expoai` and iOS app `id6754813873` | Yes, in the header, footer and download section | W-01 (OBSERVED) |
| Play listing points back to promoat.ai | Yes | OS-05 (OFFICIAL) |
| platform.promoat.ai is the same company's API | Linked from promoat.ai ("For AI agents"); its client code embeds the same Play/App Store URLs | W-01, W-02 (OBSERVED) |
| Who takes the money on the web/API | Stripe Checkout shows merchant **UAB Appasap**, live mode | W-06 (OBSERVED) |
| App Store seller | APPASAP, UAB | OS-03 (OFFICIAL) |
| Play developer | "HexaFlow AI", an individual's developer account with a Lithuanian address | OS-05 (OFFICIAL) |
| Look-alikes ruled out | promoat.com (Lantmännen PromOat, oat fibre), Promo.com, Promoty, a G2 "HexaFlow" (London) and others | OS-09 |

**Conclusion (high confidence):** ProMoat is a brand of **UAB Appasap**, a small Lithuanian company (Kaunas;
registered 2025-02-07 per an aggregator, not the official register; 1 employee; EUR 2,500 capital) run by its founder,
who also appears as CEO of the affiliated agency "HexaFlow". Operational ties to Egypt are inferred (medium).
Our own Stripe observation upgrades the OSINT inference: UAB Appasap is the contracting party for **web/API billing**
too, not only on the App Store (W-06 + OS-08).

## 2. Company, team, and commercial base

- **Team:** a founder-led micro-company. Named people: the founder/manager (OS-07), a CTO "M. Rashad" and a solutions
  architect on the affiliated agency site (OS-06). The blog mentions unnamed co-founders (OS-13). No hiring pages.
- **Funding / partnerships:** none found (OS-23). The vendors it names (Seedream, Kling, FAL, Revid/Submagic) are
  suppliers it says it uses, not partnerships (OS-24).
- **Timeline:** domain re-registered 2025-11-12; iOS + Android launched **2025-11-26** (OS-18); name change 2026-03-01;
  "ProMoat 2.0" multi-scene 2026-05-11; Partner API subdomain first seen 2026-05-17 (OS-21); new video engines
  (2026-09-30), a ~4× credit price cut (2026-10-11), and removal of social posting/scheduling (2026-10-03) (OS-19).
  The product **pivoted** from a content-marketing/scheduling app to an "AI clone" video generator (OS-20).
- **Audience and use cases:** founders, creators, small shops; MENA/Arabic emphasis; short vertical promo videos
  (OS-26, W-01).
- **Pricing (web/API, observed on our account):** Weekly $9.99 → 559 credits; Monthly $29.99 → 2,219; Monthly 3.6×
  $99.99 → 7,999; packs for subscribers only ($12.99 → 779, $24.99 → 1,499); credits never expire (W-10, W-06).
  Apps sell in-app products from $0.99/$1.49 up to $499.99/$599.99 (OS-27, OS-28).
- **Policies:** **no Terms of Service page exists** on any Promoat domain we checked, and sign-up shows no terms link
  (W-07, OS-02, OS-33). No money-refund policy; only credit refunds for failed jobs (OS-33). The privacy policy
  (2026-02-16) names no data controller and says nothing about selfies, voice samples, biometric data, AI
  sub-processors or retention periods (W-07, OS-34). EU App Store pages say the seller has not declared trader status (OS-04).
- **Acquisition channels (visible):** SEO/"GEO" comparison pages and 15 blog posts all published on one day
  (OS-22, OS-35); Meta SDK attribution in the apps (OS-36); Microsoft Clarity on the websites (W-01); an AI-agent
  channel via OpenAPI + a Claude `SKILL.md` (W-09, OS-38). No official social accounts found (OS-40).
- **Customer experience:** Play 4.70 from 505 ratings, 10K+ downloads (not a proxy for users or revenue) (OS-41).
  Patterns across several sources: paywall only at the end of onboarding (OS-42, confirmed by their own onboarding
  docs, OS-32); "took my money / nothing works" complaints (OS-43, low volume, cause unknown); "too expensive" before
  the October price cut (OS-44).
- **Revenue, active users, funding:** **not available**. Not inferred from downloads or ratings.

## 3. What the client code and our session show (web)

### 3.1 Public web (www.promoat.ai)
- Next.js on Vercel, statically pre-rendered pages, Microsoft Clarity (+ Bing pixel) analytics (W-01).
- Sample videos are hosted on the same origin (`/media/*.mp4`), all re-encoded by FFmpeg 7.x (`Lavf62.3.100`) at
  432×756 to 1280×720. They are marketing cuts, not raw outputs (W-11).

### 3.2 Partner platform (platform.promoat.ai)
- **Front end:** Next.js (App Router) on Vercel (`x-powered-by: Next.js`, `server: Vercel`), deployment id visible in
  asset URLs (W-02). **No source maps are published** (W-03), so code reading is limited to minified bundles.
- **Auth:** Supabase Auth (`@supabase/ssr` 0.5.2) with email + password. Our sign-up returned a session at once:
  **no e-mail ownership check** (W-04). The client code has a "Check your email to confirm" branch, but it was not
  triggered.
- **Workspace bootstrap:** the browser calls a Supabase Postgres function directly (`rpc/partner_bootstrap_workspace`,
  via PostgREST), then Next.js routes `/api/partner/dashboard/ensure-stripe-customer` (creates a Stripe customer at
  sign-up) and `/api/partner/onboarding/provision` (returns `{apiKey, credits: 25}`) (W-04, W-05).
- **Dashboard routes seen in the bundle:** `/api/partner/dashboard/api-key`, `subscription/checkout`,
  `subscription/change`, `billing/portal`, `credit-pack/checkout` (W-02).
- **Billing:** Stripe Checkout (live), merchant UAB Appasap, Stripe Link (W-06). A "Limited offer ends Oct 31 ·
  hh:mm:ss" countdown sits on the plan picker (W-08).
- **Docs:** each guide has "Try it" boxes that call the live API from the browser with a key saved in that browser
  only; Microsoft Clarity also runs on the docs pages (W-09).

What we cannot see: the server code, database schema, queues, workers and provider calls. Nothing below about the
back end is "extracted"; it is inferred from API behaviour, file fingerprints and the company's own statements.

## 4. Architecture (probable), with every box labelled

```
 [Mobile apps iOS/Android]      [Partner dashboard + docs]        [Partner API /api/partner/v1]
   Expo/RN? (INFERENCE, med)      Next.js on Vercel (OBSERVED)      Next.js route handlers on Vercel (OBSERVED)
          |                               |                                   |
          |  "same pipeline" (OFFICIAL)   |  Supabase Auth + Postgres RPC     |  Bearer pmat_ key (OBSERVED)
          v                               v  (OBSERVED)                       v
   +----------------------------------------------------------------------------------------+
   | Orchestrator: "workflow" per job, phases queued > generating > finalizing > completed, |
   | progress %, 75-min stale timeout + refund (OBSERVED via API/docs).                      |
   | Engine: UNKNOWN (job table + workers, or a durable-workflow service). The company      |
   | wrote in May 2026 that edge functions ran lip-sync/captions (OFFICIAL, may be stale).   |
   +----------------------------------------------------------------------------------------+
        |              |                 |                     |                   |
        v              v                 v                     v                   v
  Character sheet   First frame      Speech (TTS/clone)    Speech timing        Video clips + lip-sync
  4-view 2400x1792  9:16 1536x2752   ElevenLabs            "transcription"      UNKNOWN model(s); windows of
  Gemini image 2K   Gemini image 2K  (INFERENCE, high)     ASR/alignment        5-14.5 s cut at pauses;
  (INFERENCE,       (INFERENCE,                            (UNKNOWN provider)   scene clips ~7-8 s; 24 fps
   med-high)         med-high)                                                  (OBSERVED behaviour)
        \              \                 |                     |                   /
         \______________\________________|_____________________|__________________/
                                         v
                    Merge/mux: FFmpeg 4.4 + x264 crf 18 on a big multi-core box (OBSERVED fingerprint);
                    captions burned in when asked (OBSERVED in docs)
                                         v
                    Storage/delivery: Cloudflare R2 public bucket (pub-*.r2.dev), unsigned URLs (OBSERVED)
                    Billing ledger: credits reserve > settle > refund (OBSERVED via API)
                    Payments: Stripe (OBSERVED); Email: Zoho (OS-48); Analytics: Clarity, Meta SDK (W-01, OS-36)
```

### 4.1 Stage table

| Stage | Function | Provider | Evidence | Confidence | Alternatives |
|---|---|---|---|---|---|
| Script | Writes script / plans shots from a one-line idea (app); API takes the script verbatim | UNKNOWN LLM | W-01, docs | — | any LLM |
| Scene plan | Splits script into clip lines (free endpoint) | UNKNOWN (LLM or rules) | API-11 | — | — |
| Character identity | 4-view "character sheet" image + long text description, made once, reused | Image: Gemini image family at 2K | FP-01, API-08 | Medium-high | Another model with identical size tables; Seedream (named in May 2026 blog, OS-24) |
| First frame | 9:16 still of the character in the scene | Same image model | FP-01, BM-B0 | Medium-high | same |
| Voice / TTS / cloning | 8 studio voices, clone from 25-60 s samples, voice_settings | **ElevenLabs** (direct or via reseller) | FP-02 | High | A reseller exposing ElevenLabs |
| Speech timing | "transcription" line on every voiced video | UNKNOWN ASR / forced alignment | API-06 | — | ElevenLabs alignment, Whisper-type ASR |
| Lip-sync / talking head | Lip-sync happens **inside** video generation: first frame + speech audio go into one audio-driven generator, in 5-14.5 s windows, then merged. No separate lip-sync pass | Mechanism: INFERENCE (medium-high). Model: UNKNOWN | API-13, FP-04, BM-B0 | Mechanism medium-high; model none | Until May 2026 the company described a separate post-pass ("FAL lipsync" on Kling clips, OS-24); the legacy `lipsync` switch from that era is now ignored |
| Scene video | Character acts across ~7-8 s clips, optional product/setting photos | UNKNOWN video model | API-10 | Low | same |
| Captions | Word-by-word burned captions, Latin + Arabic | UNKNOWN (in-house render or Submagic-type tool) | docs, OS-24 | Low | — |
| Assembly / export | Concatenate windows, mux 48 kHz AAC, x264 crf 18 | FFmpeg 4.4 (Ubuntu-22.04-style build) on a ~26-core machine | FP-05 | Medium | — |
| Storage / CDN | All assets on a public R2 bucket, unguessable paths | Cloudflare R2 (`r2.dev`) | API-04 | High (observed) | — |
| Auth / DB | Accounts, workspaces, keys | Supabase | W-02, W-04 | High (observed) | — |
| Payments | Plans, packs, portal | Stripe | W-06 | High (observed) | — |
| Analytics / ads | Session replay/heatmaps; ad attribution | Microsoft Clarity; Meta SDK in apps | W-01, OS-36 | High / Official | — |
| Notifications / support | No webhooks (poll only); support by e-mail; review replies by founder | — | API-09, OS-46 | Observed / Official | — |

### 4.2 Fingerprint details
- **FP-01 image model.** Character sheet = 2400×1792; first frame = 1536×2752. Google's official size table gives exactly
  these as the **2K** sizes for 4:3 and 9:16 in Nano Banana 2.1, 3.1 Flash Image and 3.1 Pro Image (and not for
  Gemini 2.5 Flash Image: 1184×864 / 768×1344) (`evidence/fingerprints/gemini_image_size_tables.txt`).
  We did not check other vendors' size tables, so a coincidence cannot be excluded.
- **FP-02 TTS.** The eight studio voices (Brian, Daniel, George, Chris, Sarah, Laura, Alice, Jessica) are ElevenLabs'
  default voice names; `voice_settings` uses ElevenLabs' parameter names and ranges (stability, similarity_boost,
  style, speed 0.7-1.2); TTS output is MP3 44.1 kHz mono 128 kbps (ElevenLabs' default format), re-muxed by FFmpeg 8.x.
- **API-13 lip-sync mechanism.** Four independent clues say the talking-head engine generates the whole clip from the
  first frame **and** the audio, rather than generating motion first and patching the mouth afterwards:
  (1) replacing the sound of a talking head re-generates the video at the new take's length (plan `regenerate`, paid);
  only a scene video with nobody speaking on camera gets a free audio swap (docs, video-edits);
  (2) `lipsync_credits` is always 0 and the old `lipsync` on/off switch is ignored, so there is no separately billed
  lip-sync stage (OpenAPI, changelog 1.1.0); (3) changelog 1.2.1 fixed the engine changing outfit, hair, place and
  framing and "drawing captions" on talking heads, which a mouth-only lip-sync model cannot do; (4) in B0 the head,
  hands, expression and background all move, and the mouth closes when the audio goes silent. Alternative that is not
  excluded: an image-to-video model driven by a motion prompt plus a lip-sync model re-run from scratch on every audio
  change; the free/paid split in (1) makes this less likely. Decisive test (not run, needs credits): feed one window of
  non-speech audio (music, then silence) and see whether head/body motion follows the audio.
- **FP-04 video model.** Not identified. Observed: 720×1264 at 24 fps for "768P"; talking heads lip-synced in 5-14.5 s
  windows; scene clips planned at 7-8 s; job-id prefixes `partner_h3t_` (talking head), `partner_h3v_`, `partner_se_`
  (scene edits), `partner_fs_` (fix sound). Price per second is the same at every resolution, which hints that
  resolution does not change their provider cost much, or that they absorb it.
- **FP-05 assembly.** Final MP4: H.264 High, x264 core 163 r3060, `crf=18`, `threads=39`, muxer `Lavf58.76.100`
  (FFmpeg 4.4.x, as shipped by Ubuntu 22.04). TTS files show `Lavf63` (FFmpeg 8.x). Two different processing environments.

## 5. Partner API (what we tested)

**Surface (OpenAPI 1.2.1 file, docs say 1.3):** characters (create/regenerate/list/delete), voices (studio, clone,
re-clone, delete), TTS, first-frame images, videos (talking head; scenes with reference/text/silent modes),
scene-plan, estimate, edits (fix-scene, edit-script, fix-sound with `dry_run`), jobs status, assets ledger, usage.
Plain JSON over HTTPS, bearer keys `pmat_<id>_<secret>`, no SDK, **no webhooks** (poll every 8-10 s) (W-09, API-09).

**Money mechanics (observed or documented):**
- Price depends only on output length (5 s = 21 … 60 s = 73 credits with your own audio, incl. first frame 12 and
  timing 3); TTS 10 credits per started 1,000 characters; captions +10; character creation free; first clone free.
- `POST /videos/estimate` is free and returns the exact reserve; the quote is a ceiling; jobs reserve then settle at
  `min(actual, reserved)`; failed jobs refunded once; stale jobs (75 min) failed and refunded (docs, API-02).
- `expected_credits` locks the price: a higher quote returns **409 QUOTE_MISMATCH**, and this check runs **before** the
  balance check (observed, BM-B8a).
- Idempotency keys on videos (optional) and edits (required); same key + same body returns the original job.
- Bad inputs fail fast and free: unreachable audio URL → 422 `INVALID_URL`; unknown voice → 404; bad resolution →
  400; balance unchanged (BM-B8, API-03). The estimate endpoint does **not** validate ids (documented, observed).
- Limits: 5 active jobs, 3 cloned + 10 library voices, 4,000-char scripts, 59.5 s voiced audio, 1 open edit per video.

**Security observations (our own account only):**
- Asset URLs (character sheets, frames, audio, videos) are **public, unsigned** `pub-…r2.dev` links whose paths
  contain the workspace UUID and job id (API-04). For photo-mode characters this means sheets derived from a real
  person's selfies sit at public URLs for as long as Promoat keeps them. Docs say this is by design ("unguessable
  paths"). `r2.dev` is Cloudflare's development endpoint, which Cloudflare does not recommend for production traffic.
- Keys can be **revealed again** in the dashboard and rotation is not self-serve (API-01), so keys are stored in a
  recoverable form rather than as one-way hashes.
- Sign-up grants 25 credits without verifying the e-mail address (W-04, W-05).

**Commercial-use terms:** there is no ToS, no licence for outputs, no white-label or resale clause, no data-retention
or deletion statement beyond `DELETE` endpoints, and no consent framework beyond one sentence in the docs ("You're
responsible for having that consent for any likeness you clone"). Using Promoat as a provider was ruled out by the
requester, so no provider recommendation is made; the gap is recorded because it matters for anyone who copies the
model: a paid face/voice cloning API without terms is a legal risk, not a feature.

## 6. Android app

- **Not installed and not tested.** The container has no KVM (no usable Android emulator), and the official APK can
  only be obtained through Google Play on a signed-in device. We did not use third-party APK mirrors, because the
  task required the official source. Statement "we tested Android" would therefore be false (AND-01).
- From the official listing only: package `com.hexaflow_ai.expoai`, developer "HexaFlow AI", v2.3.0 updated
  2026-10-13, 10K+ downloads, Play data safety lists photos, voice recordings, e-mail, messages and IDs; videos,
  device IDs, app activity and crash data are shared with third parties (OS-05, OS-34, OS-41, OS-52).
- The package name containing `expoai` suggests Expo/React Native (INFERENCE, medium). Not verified.
- Whether app and API share accounts/credits: UNKNOWN. The API docs say the plans and prices are "the same as the app";
  they do not say balances are shared.

## 7. Video quality and real-world behaviour

See `BENCHMARK_RESULTS.csv` and section 7 of this file once runs complete. Pre-registered plan and acceptance
criteria: `benchmark/BENCHMARK_PLAN.md` (committed before any generation).

<!-- BENCHMARK_SECTION -->

## 8. Patterns worth rebuilding (originally) vs. not worth copying

### Worth rebuilding
1. **Identity anchor made once, reused everywhere.** A multi-view character sheet (front, 3/4, profile, full body)
   plus a long, locked text description, created free at onboarding and passed to every image/video call (API-08).
   It turns "keep the same face" from a prompt problem into a data object the customer owns and can regenerate.
2. **First frame as a cheap, approvable checkpoint.** A 9:16 still (4 credits) before the expensive video. Customers
   approve the look before spending; the job reuses the approved still (BM-B0).
3. **Talking-head assembly from short lip-sync windows** (5-14.5 s, cut at natural pauses) merged into one video. This
   is how they get up to 59.5 s from models that produce short clips, and it also makes per-scene edits possible.
4. **Edits as new versions, scene by scene** (fix-scene, edit-script, fix-sound), never destructive; a dry-run quote
   first; one open edit per video (docs).
5. **Billing contract that removes fear of paying:** price by output length only; free estimate = exact reserve;
   quote is a ceiling; settle at actual; automatic refund on failure or stale timeout; `expected_credits` lock;
   idempotency keys; `price_table_version` on every response (API-02).
6. **Agent-ready distribution:** OpenAPI + a one-file agent skill + "Try it" docs. Cheap to build, opens the
   "AI agents make videos" channel (W-09, OS-38).
7. **Onboarding promise in one line:** one selfie + a 25-second voice note, 25 free credits, no card (W-01). (But see
   the paywall complaints below: the free credits must produce a visible result.)

### Not worth copying
- Public unsigned URLs for face-derived assets; no ToS; no e-mail verification on a credit-granting sign-up; keys
  stored recoverably; no webhooks (W-04, API-01, API-04).
- Unverifiable marketing claims (e.g. "~94% Arabic viseme accuracy", CTR multipliers) (OS-25), countdown urgency
  (W-08), paywall revealed only at the last onboarding step (OS-42).
- Repricing several times a month (125 → 30 credits for 15 s within 11 days, API-06): good for growth tests,
  bad for customer trust and for anyone budgeting on top of you.

## 9. Unit economics (customer side; Promoat's own costs are unknown)

| Plan | USD per credit | 5 s talking head, own audio + own frame (9 cr) | 15 s, script mode (43-48 cr quoted) | 60 s, own audio (73 cr) |
|---|---|---|---|---|
| Weekly $9.99 / 559 | $0.0179 | $0.16 | $0.77-0.86 | $1.30 |
| Monthly $29.99 / 2,219 | $0.0135 | $0.12 | $0.58-0.65 | $0.99 |
| Monthly 3.6× $99.99 / 7,999 | $0.0125 | $0.11 | $0.54-0.60 | $0.91 |

- Script-mode quotes include TTS and a headroom margin (35% for non-Latin scripts); the job settles at the measured
  length, so the charged amount can be lower (docs). Measured settlements are in `BENCHMARK_RESULTS.csv`.
- Promoat's **internal** cost and margin are **unknown**. Their May 2026 blog claimed "~$0.45 per clip (one Seedream
  image plus a 10-second Kling video)" for the older engines (OS-24, OFFICIAL, unverified). The 4× price cut in
  October 2026 means either cheaper engines or a deliberate subsidy; we cannot tell which.
- Cost per **acceptable** video (including rejected attempts) is computed in section 7 from our runs.

### 9.1 Market reference: wholesale prices of audio-driven talking-video models (checked 2026-11-01)

Promoat's retail price for video seconds is about **$0.013-0.022 per second** (60 s with own audio = 73 credits;
generation line alone 58 credits). Public per-second API prices of models that take an image **plus an audio file**
and lip-sync during generation:

| Model (audio in, lip-sync in generation) | Wholesale price / s | Source (checked 2026-11-01) |
|---|---|---|
| ByteDance OmniHuman 1.5 | $0.16 | fal.ai model page |
| Kling AI Avatar v2 Pro / Standard | $0.115 / $0.0562 | fal.ai model pages |
| HeyGen Avatar IV (photo) API | ~$0.05 (resellers up to $0.085-0.10) | HeyGen blog, reseller listings |
| Hedra Character-3 API | $0.025 (540p) / $0.05 (720p) / $0.0625 (1080p) | third-party read of Hedra price list, 2026-10-21 |
| InfiniteTalk (open weights, Wan-based) hosted | $0.015 (Fast) / $0.03-0.06 (standard 480p-720p) | WaveSpeed model page |
| LongCat-Video-Avatar 1.5 (open weights, Meituan, May 2026) | self-host only (GPU cost) | arXiv 2605.26486 |
| Seedance 2.0 (accepts up to 3 audio references) / Wan 2.6 i2v (WAV/MP3 drives lip-sync) | not verified for the audio mode | third-party guides |

Reading (INFERENCE): Promoat's video seconds are 3-10x cheaper than the closed premium models but in the range of a
hosted open-weights model, and cheaper than that if self-hosted. The October price cut arrived **together with** a
"new video engine" (changelog 1.2.0), and the final MP4 carries the fingerprint of a machine they or a GPU host
control (FP-05). Most likely: a switch to a cheaper (probably open-weights) audio-driven engine, possibly plus some
growth subsidy. Not proven; the engine is still unidentified.

- **W-12 (OBSERVED 2026-11-01 07:22Z):** the "Limited offer ends Oct 31" countdown is gone from the plans page and
  the prices are unchanged (Monthly $29.99 / 2,219; Weekly $9.99 / 559; Monthly 3.6× still offered). The deadline
  changed nothing visible.

## 10. Unknowns that matter

| Unknown | Why it matters | How it could be resolved |
|---|---|---|
| Video model(s) since Sep-Oct 2026 | Determines quality ceiling and cost floor | Ask support (they may not answer); compare output fingerprints against candidate models side by side |
| Real-face (photo-mode) quality | Their core promise; not tested (owner chose to skip) | One authorised selfie + voice sample, 2 runs, same scripts |
| Android app behaviour | Not installable here | A real device with the Play app, 30 minutes |
| Capacity, queueing, concurrency beyond 5 jobs | We ran a handful of jobs only; says nothing about scale | Not testable ethically (no load tests) |
| Data retention / deletion of faces and voices | Legal exposure | Written answer from the company |
| Revenue, active users, funding | Commercial strength | Not public |
