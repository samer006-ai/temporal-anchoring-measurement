# Handover: Promoat teardown

Last updated: 2026-11-07 (UTC). Read this first if you resume the work in a new session.

## Remaining items (status on 2026-11-07)
- Paid benchmark matrix (B1, B2×2, B4, B5, B6, B7, idempotency duplicate): **blocked, waiting for the owner's payment**. Balance is still 2 credits (free `GET /usage/summary`, 2026-11-07 13:13Z); the 2026-10-31 Checkout link has expired, so a new one is needed; inputs ready in `benchmark/inputs/`.
- Human audio evaluation (Levantine TTS sample and the B0 clip): **waiting for the owner's listening** against `benchmark/BENCHMARK_PLAN.md`; open point: Whisper heard «تلاتة بعشرين ألف» as «23 ألف».
- Private report page https://claude.ai/artifact/NDgnVsKKyDPtnobqWp2gpc: **live and private**; holds the deliverables and withheld evidence as of 2026-11-01; `UI_PATTERNS_AR.md` and this update are not on it yet.
- Android app: **not testable here** (no KVM); needs a real device, about 30 minutes.
- Real-face path: **skipped by the owner**; synthetic-face results do not replace it.

## Scope changes from the owner (binding)
- **The comparison with the owner's own product was cancelled.** Do not read, use or mention that product or its
  repositories in this work. Earlier notes about it were removed from the workspace and are not part of any deliverable.
- **Purpose:** understand how Promoat works and which of its patterns are worth rebuilding originally. Promoat will
  **not** be used as a provider, so no provider recommendation is needed.
- **Real-face path:** skipped by the owner. Do not substitute synthetic-face results for it.
- Rules that still apply: no copying of Promoat code/assets/text, no bypassing auth/limits/protections, no load tests,
  no third-party data, secrets never in files or reports.
- **2026-11-07:** the launch coordinator session, acting on the owner's order of that day, asked for original, generic
  UI patterns from this teardown. Being written as `UI_PATTERNS_AR.md` (committed separately once checked): it names
  no other product, copies no Promoat text, code or assets, and no paid case is run for it. No conflict with the
  owner's rulings above was found.

## State
| Area | Status |
|---|---|
| Public sources, docs (17 pages), OpenAPI, SKILL.md, JS bundles, headers | Done (`evidence/web`, `evidence/docs`) |
| OSINT company/founders/timeline/reviews | Done (`evidence/osint/OSINT_FINDINGS.md`, IDs OS-01..52) |
| Research account | Created 2026-10-31 17:21Z with the owner-approved e-mail. 25 trial credits used (balance 2, re-read 2026-11-07) |
| Free tests | B8 failure tests (0 credits), TTS Shami (10), first frame + 5 s talking head B0 (13) |
| Paid plan | **Stripe Checkout link for Weekly $9.99 handed to the owner on 2026-10-31; no payment received by 2026-11-07; the link has expired** |
| Paid benchmark matrix (B1, B2×2, B4, B5, B6, B7, idempotency duplicate) | Pending payment. Inputs ready in `benchmark/inputs/` |
| Android | Not testable here (no KVM, no official APK without a signed-in device). Documented in AND-01 |
| Deliverables | `PROMOAT_DOSSIER.md`, `EVIDENCE_INDEX.csv`, `COST_LEDGER.csv`, `BENCHMARK_RESULTS.csv`, `EXECUTIVE_SUMMARY_AR.md`, `OPEN_MODELS_SHORTLIST.md` (2026-11-01), `UI_PATTERNS_AR.md` (2026-11-07, in progress), this file |

## Where things are
- Pre-registered plan: `benchmark/BENCHMARK_PLAN.md` (first commit, before any generation).
- Scripts: `scripts/pm.py` (API client + call log), `scripts/run_job.py` (estimate → idempotent submit → poll →
  download → balance), `scripts/av_analyze.py` (ffprobe, cuts, lip-sync and identity proxies, contact sheet),
  `scripts/asr_check.py` (Whisper large-v3 transcript + WER/CER), `scripts/build_results.py` (rebuilds the CSV),
  `scripts/capture_pages.js`, `scripts/dash_explore.js`, `scripts/signup.js`, `scripts/provision.js`, `scripts/checkout_link.js`.
- Every API call is logged (redacted) in `evidence/api/calls.jsonl`.
- Inputs that the API must fetch by URL are hosted (synthetic only) at
  `https://raw.githubusercontent.com/samer006-ai/temporal-anchoring-measurement/faf0619/bench-inputs/` (product mock-up P1, 3.6 s TTS clip).
- Promoat ids: character C1 `8cf7c5cb-e5a6-45ea-bece-6cb1dafe65bd`; studio voice `sv_daniel_42d444368f71`;
  B0 job `partner_h3t_384448654930f1e5699f430738e01b94`.

## Public vs private storage
- Public branch (GitHub, public repo): deliverables, scripts, pre-registered plan, synthetic inputs/outputs, API call log,
  fingerprints, OSINT findings (no personal e-mails/addresses), and `evidence/WITHHELD_MANIFEST.csv` (SHA-256 of every
  withheld file).
- Private only: third-party page captures (Promoat docs/site/JS bundles, store listings, registries, search snippets),
  rendered page texts, and screenshots showing the research account. They are attached to the private report page
  https://claude.ai/artifact/NDgnVsKKyDPtnobqWp2gpc under the same paths (HTML/JS saved as plain text; two JS files as
  base64 because they contain U+FFFD). Verify them against the manifest hashes.

## Secrets (values never stored in the repository)
- Session-private file `secrets/promoat.env` in the session scratchpad holds `PROMOAT_EMAIL`, `PROMOAT_PASSWORD`,
  `PROMOAT_KEY`; `secrets/promoat_state.json` holds the browser session; `secrets/stripe_checkout_url.txt` the
  checkout link. **These disappear with the container.**
- To resume in a new session: sign in at https://platform.promoat.ai/sign-in (use "forgot password" with the research
  e-mail if needed), copy the key from the dashboard, and add it as an environment variable `PROMOAT_KEY` in the cloud
  environment settings. Do not paste it in chat.

## How to resume the paid matrix (no double spend)
1. `GET /usage/summary` → confirm balance ≥ 300.
2. Before re-running any case, check `evidence/api/calls.jsonl` and `benchmark/outputs/<run_id>/run.json`: if a submit
   exists for that run id, poll `GET /jobs/{workflow_id}/status` instead of resubmitting. `run_job.py` uses the run id
   as the Idempotency-Key, so a resubmit with the same run id returns the same job (`duplicate: true`).
3. Run in this order (most decision-relevant first): B2_a, B2_b, B1, B5, B6, B7 (fix-scene on B6), B4, then the
   idempotency duplicate test (resubmit B1 body with the B1 key, expect `duplicate: true` and no charge).
4. For each finished run: `av_analyze.py`, `asr_check.py`, write `review.json`, then `build_results.py`.
5. Then cancel renewal in Dashboard → Manage subscription (plan stays active to period end) and record the period end
   in `COST_LEDGER.csv`.

## Open questions
- Which video model(s) Promoat runs since Sep-Oct 2026 (FP-04). Image = Gemini image family (FP-01, medium-high);
  voice = ElevenLabs (FP-02, high).
- Real-face quality (skipped by the owner).
- Data retention/deletion for faces and voices; licence for outputs (no ToS exists).
- Android behaviour; whether app and API share balances.
- Scale/capacity: not testable without load tests (out of scope).
