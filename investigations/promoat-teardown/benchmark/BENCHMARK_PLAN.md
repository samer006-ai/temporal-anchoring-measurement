# Benchmark plan (pre-registered before any generation)

Written: 2026-10-31 (UTC), before any Promoat account existed and before any output was seen.
Locked by the git commit that first adds this file. Any later change to cases or criteria must be
added as an "Amendment" section with a reason, never by editing the text above it.

## Scope and constraints
- Service under test: Promoat Partner API, https://platform.promoat.ai/api/partner/v1/ (API docs v1.3, price table 2026-10-11).
- Same pipeline as the Promoat app per the vendor's docs (claim, not verified).
- Budget: total engagement cap USD 100. Planned spend: 25 free trial credits, then the smallest plan
  (Weekly, USD 9.99 for 559 credits) only if the free credits cannot answer the questions. No annual
  plan, no auto top-up. Cancel renewal immediately after purchase (plan stays active to period end).
- Every paid call is preceded by the free `POST /videos/estimate` (or `dry_run`) and sent with
  `expected_credits` and an `Idempotency-Key`, so a retry cannot double-charge.
- Balance (`GET /usage/summary`) is recorded before and after every paid call.
- Real face / real voice only from material the owner explicitly authorises for this test.
  A synthetic-face result is never used as evidence for the real-face path.

## Cases (fixed now)

| ID | What it tests | Mode | Language | Input | Repeats |
|----|---------------|------|----------|-------|---------|
| B1 | Synthetic presenter, Modern Standard Arabic | talking_head, script mode, studio voice | MSA | S1 | 1 |
| B2 | Levantine (Shami) with names and numbers, natural intonation | talking_head, script mode, studio voice | Shami | S2 | 2 (critical) |
| B3 | Real face + reference voice (authorised adult) | talking_head, script mode, cloned voice, photo-mode character | Shami (S2) | owner's selfie(s) + 30–60 s voice note | 2 (critical) |
| B4 | Same character across scenes/videos | talking_head, same character as B1, different setting | MSA | S3 | 1 |
| B5 | Product ad: product photo + brand name/logo must survive | scenes, reference mode, 1 product photo | MSA | S4 + synthetic product image P1 | 1 |
| B6 | Multi-shot video with a clear opening hook and transitions | scenes, 4 scene_lines, ~30 s | MSA | S5 | 1 |
| B7 | Edit one part, keep the approved parts | fix-scene on B6 (one scene) | — | edit text E1 | 1 |
| B8 | Safe failure / invalid input, credit effect | QUOTE_MISMATCH, duplicate idempotency key, unreachable URL, unknown voice | — | — | 1 each |

Order of execution if budget is short (most decision-relevant first): B8 (free parts), B2, B3, B1, B5, B6, B7, B4.
Free-trial-only fallback (25 credits): character (free) + studio voice (free) + TTS of S2 (10) + one
5 s talking head with its own first frame (first frame 4 + video ~9) = ~23 credits.

## Inputs
- S1 (MSA, ~15 s): «مرحباً بكم. في هذا الفيديو القصير نشرح كيف يمكن لمتجرك الصغير أن يصل إلى عملاء جدد كل يوم، من دون تصوير ومن دون استوديو. الفكرة بسيطة: تكتب سطراً واحداً، ونحن نحوّله إلى فيديو جاهز للنشر.»
- S2 (Shami, names + numbers, ~15 s): «أهلين فيكن! أنا رامي من محل أبو خليل بالشعلان. من بكرا الساعة تسعة الصبح، عنا عرض على المناقيش: تلاتة بعشرين ألف ليرة. وإذا جبت رفيقك، التانية علينا. ناطرينكن، لا تتأخروا!»
- S3 (MSA, ~12 s, B4): «هذه هي المرة الثانية التي نلتقي فيها. اليوم أحدثكم من الشارع، والسؤال نفسه: كيف تبيع أكثر بوقت أقل؟»
- S4 (MSA, ~15 s, B5): «تعرّفوا على زيتون، زيت الزيتون البكر الممتاز من حقول الشمال. عصرة أولى على البارد، بطعم غني ورائحة طازجة. اطلبوه اليوم واحصلوا على خصم عشرين بالمئة.»
- S5 (MSA, 4 lines, ~30 s, B6):
  1. «هل تعلم أن ثلاثة من كل أربعة زبائن يقررون الشراء في أول ثلاث ثوانٍ؟»
  2. «لهذا نبدأ كل فيديو بجملة تشد الانتباه، ثم نعرض المنتج بوضوح.»
  3. «بعدها نضيف دليلاً بسيطاً: تجربة زبون حقيقي، أو رقماً يمكن التحقق منه.»
  4. «وفي النهاية دعوة واضحة: اطلب الآن، والرابط في الوصف.»
- E1 (B7): redo scene index 1 with description «نفس الشخص، لكن يمسك المنتج بيده ويبتسم» — all other scenes must stay identical.
- P1: synthetic product image generated locally (olive-oil bottle, Latin label "ZAYTOON", leaf logo). No third-party marks.

Default settings: resolution 768P (vendor default), captions off (except where noted), voice_settings untouched
(vendor defaults) for the "raw" run. Any manually tuned re-run is reported separately as "tuned".

## Measurements per run
Input files + settings + API version/price_table_version + UTC time; queue→start→complete timestamps
from polling (8–10 s interval) and total time to downloaded file; first result vs. retries/edits;
credits quoted / reserved / consumed and balance delta; cash cost = credits × USD per credit of the plan used;
ffprobe: resolution, duration, fps, codec, bitrate, audio sample rate; watermark presence (visual check);
automatic: ASR transcript vs. script (word error rate, names/numbers correct y/n) if a local ASR model can run;
human (self-review, NOT blind, NOT customer evaluation): pronunciation, dialect, voice naturalness,
lip-sync, identity stability, artefacts, transitions, publishability (1–5 each).

## Definition of "acceptable for publishing" (fixed now)
A run is acceptable only if ALL hold:
1. Script delivered verbatim (no dropped/added words that change meaning); names and numbers correct.
2. Pronunciation score ≥ 4/5; for Shami cases the dialect is recognisably Levantine (≥ 4/5).
3. Lip-sync ≥ 4/5 (no visible drift; no mouth moving during silence).
4. Identity: same person throughout and across clips (≥ 4/5); for B3 the owner confirms it looks like them.
5. No severe artefact (face/hand/teeth distortion, unwanted on-screen text, broken frames) — any severe artefact = fail.
6. Output ≥ 720 px short side, 9:16, no third-party watermark, plays in standard players.
7. For B5: brand name "ZAYTOON" legible and product shape preserved in at least one clear shot.

Cost to an acceptable video = total credits of all attempts for that case (including rejected attempts and edits)
÷ number of acceptable outputs, converted to USD at the plan's per-credit price.
