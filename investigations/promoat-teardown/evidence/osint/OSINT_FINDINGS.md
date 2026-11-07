# OSINT findings: ProMoat / Promoat (AI video app)

- Scope: the company behind ProMoat (https://www.promoat.ai/, https://platform.promoat.ai/, iOS id6754813873, Android `com.hexaflow_ai.expoai`).
- Collected: 2026-10-31. All "Accessed" dates below are 2026-10-31 unless stated otherwise.
- Raw captures: this directory (`evidence/osint/`). File names give the source (`official_*` = ProMoat-controlled pages, `appstore_*` / `googleplay_*` = store listings, `rdap_*` / `dns_*` / `crtsh_*` = measurements, `related_*` = affiliated domains, `thirdparty_*` = directories and trackers, `disambiguation_*` = unrelated look-alikes, `websearch_snippets_2026-10-31.txt` = search-result summaries for pages that blocked direct capture).
- Evidence types:
  - OFFICIAL_SOURCE: the company or its own store listing says it.
  - INDEPENDENT_SOURCE: a third party says it.
  - OBSERVED: measured directly here (DNS, RDAP, CT, page content, counts).
  - INFERENCE: a conclusion drawn from clues. The clues and a confidence level are stated.
  - UNKNOWN: not found, or not accessible.
- Every link was verified back to `promoat.ai`, App Store id `6754813873` / developer id `6814774031`, or Play package `com.hexaflow_ai.expoai` before it was attributed to this ProMoat. Look-alikes are listed in OS-09.
- Privacy handling:
  - Store pages show a personal Gmail address and a street address for the developer account, and the registry shows a unit-level registered address. These are kept in the raw captures and are only summarised here, at city or postcode level.
  - The founder's family and personal details are not collected.

---

## 1. Identity and legal entity

**OS-01: The brand is "ProMoat" (also written "Promoat"), and the website does not name any legal entity.** The homepage schema.org `Organization.name` is "ProMoat", and the footer says "© 2026 ProMoat". No company name, registration number or address appears on any promoat.ai page, and there are no About or Contact pages (both return 404).
- Source: https://www.promoat.ai/ (`official_promoat.ai_home.html`), https://www.promoat.ai/sitemap.xml (`official_promoat.ai_sitemap.xml`)
- Source date: sitemap lastmod 2026-10-03
- Accessed: 2026-10-31
- Type: OFFICIAL_SOURCE + OBSERVED

**OS-02: The privacy policy names no data controller or company.** It says "Last updated: February 16, 2026" and refers to "the Company" and "We", but its "Interpretation and Definitions" heading has no content. It gives no address, governing law or GDPR basis. The only contact is **a free Gmail address under the developer-brand name** (address withheld here). promoat.ai has no Terms of Service page (`/terms` and `/terms-of-service` return 404). The iOS listing links Apple's standard EULA.
- Source: https://www.promoat.ai/privacy-policy (`official_promoat.ai_privacy-policy.html`)
- Source date: 2026-02-16
- Accessed: 2026-10-31
- Type: OFFICIAL_SOURCE + OBSERVED

**OS-03: On the App Store, the seller is "APPASAP, UAB" and the developer is "ProMoat.ai".**
- Details from the listing:
  - Title: "AI Video Generator - ProMoat".
  - Seller (the contracting party): **APPASAP, UAB**. "UAB" is the Lithuanian private limited company form.
  - Developer/artist name: "ProMoat.ai" (artistId 6814774031).
  - Bundle id: `com.hexaflow-ai.promoat`.
  - Developer website: http://promoat.ai.
  - Copyright line: "© 2025 Uab appasap".
- This is the only app under developer 6814774031.
- Sources: https://itunes.apple.com/lookup?id=6754813873 (`appstore_itunes_lookup_id6754813873_{us,ae,sa,gb,eg}.json`), https://apps.apple.com/us/app/id6754813873 (`appstore_web_id6754813873_us.html`), developer lookup (`appstore_itunes_lookup_artist6814774031_us.json`)
- Source date: listing current version date 2026-10-29
- Accessed: 2026-10-31
- Type: OFFICIAL_SOURCE

**OS-04: In EU storefronts, the App Store shows that APPASAP, UAB has not declared trader status for this app.** The LT and DE pages say: "APPASAP, UAB has not identified itself as a trader for this app. If you are a consumer in the European Economic Area, consumer rights do not apply to agreements between you and the provider."
- Source: https://apps.apple.com/lt/app/id6754813873, https://apps.apple.com/de/app/id6754813873 (`appstore_web_id6754813873_{lt,de}.html`)
- Accessed: 2026-10-31
- Type: OBSERVED

**OS-05: On Google Play, the developer is "HexaFlow AI", and the account is in an individual's name with a Lithuanian address.**
- Listing details:
  - Developer name: **HexaFlow AI**.
  - Package: `com.hexaflow_ai.expoai`.
  - Website: https://www.promoat.ai/.
  - Support email: **a named person's address at the affiliated agency's domain** (address withheld here).
- "About the developer" shows:
  - An individual's name: "abdelhaleem moatassem desouky ahmed mohamed".
  - A personal Gmail address (not reproduced here).
  - A street address in **Vilnius, Lithuania**, postcode 04310. The building also has residential units, so the street is not reproduced.
- No company name or D-U-N-S number appears.
- This is the only app on the HexaFlow AI developer page.
- Sources: https://play.google.com/store/apps/details?id=com.hexaflow_ai.expoai (`googleplay_com.hexaflow_ai.expoai_en_us.html`, `googleplay_scraper_app_and_reviews.json`), https://play.google.com/store/apps/developer?id=HexaFlow+AI (`googleplay_developer_HexaFlow_AI.html`)
- Source date: listing updated 2026-10-13
- Accessed: 2026-10-31
- Type: OFFICIAL_SOURCE

**OS-06: hexaflow.ai, an affiliated AI-agency site, links HexaFlow to UAB Appasap and to Moatassem.**
- Site title: "HexaFlow - AI Solutions Agency". It offers workflow automation and custom AI on a subscription.
- Contact block: "Office LT-44319, Kaunas, Lithuania, **UAB Appasap**". E-mail: a named person's address at the same domain (withheld here). WhatsApp number with the **+20 (Egypt)** country code.
- "Meet the team":
  - **Moatassem D.**, CEO (linkedin.com/in/moatassem-abdelhaleem)
  - **M. Rashad**, CTO (linkedin.com/in/rashaddism)
  - **Jasmin A.**, Solutions Architect
- Source: https://www.hexaflow.ai/ (`related_hexaflow.ai.html`)
- Source date: undated
- Accessed: 2026-10-31
- Type: OFFICIAL_SOURCE (affiliated site)

**OS-07: A registry aggregator shows UAB Appasap as a small Kaunas company managed by Moatassem.** The data comes from okredo.com, which republishes the Lithuanian Centre of Registers.
- Company: UAB Appasap, company code **307090149**.
- Registered **2025-02-07**. Status: active.
- Share capital: EUR 2,500.
- Registered address: Gedimino g., **Kaunas LT-44319**. This postcode matches hexaflow.ai.
- Activity: "other computer programming". No VAT registration.
- Manager and sole representative: **Moatassem Desouky Ahmed Mohamed Abdelhaleem**.
- Employees: 1.
- Limits on this evidence:
  - The okredo page returned HTTP 403, so it was captured only through search-result summaries (`websearch_snippets_2026-10-31.txt`).
  - The official register (registrucentras.lt / get.data.gov.lt), rekvizitai.vz.lt, scoris.lt and OpenCorporates could not be reached (see Unknowns).
  - **None of this has been checked against the official register.**
- Source: https://okredo.com/en-lt/company/uab-appasap-307090149 (and its `/manager/...` subpage)
- Accessed: 2026-10-31
- Type: INDEPENDENT_SOURCE (secondary, unverified)

**OS-08: Inferred operating structure: UAB Appasap (Kaunas, Lithuania) is the legal and contracting entity, "HexaFlow AI" is a trade or developer-account name, "ProMoat" is the product brand, and Moatassem D. A. M. Abdelhaleem is the person behind all three.**
- Clues:
  - App Store seller is APPASAP, UAB (OS-03).
  - hexaflow.ai names UAB Appasap in its office block, with the same LT-44319 postcode (OS-06, OS-07).
  - Bundle ids use `com.hexaflow-ai.*` / `com.hexaflow_ai.*`.
  - The privacy contact is `hexaflowai@` (OS-02).
  - The same individual appears as Play account holder, UAB Appasap manager, HexaFlow CEO and the person answering reviews (OS-05, OS-07, OS-10).
- Contradictions:
  - The Play account shows an individual's name and a **Vilnius** address. The registry shows a **Kaunas** address.
  - No registered entity named "HexaFlow" was found.
- Confidence:
  - **High** that UAB Appasap is the App Store contracting party (stated directly by Apple).
  - **Medium-high** that HexaFlow AI is a brand of the same person or entity, not a separate company.
  - **Medium** that UAB Appasap is also the contracting party for Play and the web/API billing, since neither names a company.
- Declared country: **Lithuania**, on both stores and the affiliated site. Operational ties to **Egypt** (+20 WhatsApp, Egyptian-Arabic review base, and an Alexandria background on the founder's LinkedIn per a search snippet) are inferred with medium confidence.
- Type: INFERENCE

**OS-09: Several similarly named companies and domains are unrelated or unconfirmed.**
- `promoat.com` redirects to Lantmännen Biorefineries "PromOat" (oat beta-glucan). It is unrelated (`disambiguation_promoat.com_lantmannen.html`; RDAP: registered 2004, CSC registrar).
- G2 seller "HexaFlow": London HQ, founded 2017, offices in Dubai, Riyadh and Muscat. It is a different firm, and no link was found.
- `hexaflow.io` is a different HexaFlow, per a search snippet.
- `hexaflowai.com` was registered 2025-04-11 through DNSPod and did not resolve to content. Its relation is **unknown**.
- "Techhive.IO" (Beirut) is not the same as `techhive.dev`.
- G2 seller "ProMoat" is described as "AI-driven solutions for optimizing promotional strategies in the retail and consumer goods sectors". That description does not fit the video app. It may be auto-generated, or it may describe a previous holder of promoat.ai (see OS-17). Unverified.
- Also unrelated: Promo.com, Promo.ai (Sydney), PromoAI (Cognira), PromoGoat, Promoty and Promoto AI.
- Sources: `websearch_snippets_2026-10-31.txt`, `rdap_*.json`
- Accessed: 2026-10-31
- Type: OBSERVED + INFERENCE

## 2. Founders and team

**OS-10: Moatassem personally handles customer contact.**
- App Store developer reply (≈2026-10-28): "...let me know what happened on the support email, I'll personally look into the matter: **[a named person's address at promoat.ai, withheld here]**".
- Play replies dated 2026-10-28: "Unfortunately I can't afford to create free videos for everyone **as a small business owner**...".
- The Play support email is the same named address at the agency's domain (withheld here).
- Sources: App Store US page and RSS (`appstore_web_id6754813873_us.html`, `appstore_rss_reviews_us.json`), `googleplay_scraper_app_and_reviews.json`
- Source date: 2026-10-28
- Accessed: 2026-10-31
- Type: OFFICIAL_SOURCE

**OS-11: Founder background comes only from a self-reported LinkedIn profile.** The profile is "Moatassem Abdelhaleem" (lt.linkedin.com/in/moatassem-abdelhaleem), and hexaflow.ai links to it as "Moatassem D., CEO". According to search-result summaries, it says:
- Based in Lithuania, with an Alexandria, Egypt background.
- "Entrepreneur, consultant, project manager", with about a decade of experience.
- About 4K followers.
- A second-place finish in a robotics competition.
- Specific employers and education could not be read because LinkedIn returned HTTP 999.
- Source: `websearch_snippets_2026-10-31.txt` (Q3, Q4)
- Accessed: 2026-10-31
- Type: OFFICIAL_SOURCE (self-reported), unverified

**OS-12: Other named people are listed for the HexaFlow agency, not explicitly for ProMoat.** "M. Rashad" (CTO, linkedin.com/in/rashaddism) and "Jasmin A." (Solutions Architect) are on hexaflow.ai. Whether they work on ProMoat is an inference with low-to-medium confidence.
- Source: `related_hexaflow.ai.html`
- Type: OFFICIAL_SOURCE (for the listing) / INFERENCE (for the ProMoat role)

**OS-13: The blog claims several co-founders and a MENA founder, but names none.**
- "Why We Built ProMoat" says: "I have lived all three, which is why **my co-founders and I** built ProMoat.ai".
- The Arabic lip-sync article says: "**I founded a company in MENA**."
- Article bylines are "By ProMoat.ai" or "By ProMoat Founders", and the JSON-LD author is an Organization.
- The co-founders' identities are unknown.
- Sources: https://www.promoat.ai/synthesia-alternative-for-founders-in-2026, https://www.promoat.ai/native-arabic-lip-sync-for-founders
- Source date: published 2026-05-12
- Accessed: 2026-10-31
- Type: OFFICIAL_SOURCE

**OS-14: techhive.dev shows a software-agency footprint that predates ProMoat.**
- The domain was registered **2022-01-18** (GoDaddy).
- Certificate Transparency shows dozens of client and project subdomains (evicare, ingenium, sal/sal125, sotech, easypass, zzabbat, wedding-planner, and others), plus self-hosting tools (Coolify, Dokploy, Grafana, Uptime Kuma).
- It also includes **`appasap.techhive.dev`** (certificates 2023-02-05 and 2023-05-07).
- The founder uses @techhive.dev email (OS-05, OS-06).
- Inference: the founder also runs a dev agency or studio, and the "Appasap" name was in use by early 2023. Confidence: medium.
- Sources: `crtsh_techhive.dev.json`, `rdap_techhive.dev.json`
- Type: OBSERVED + INFERENCE

## 3. Timeline (dated events only)

| Date | Event | Evidence |
|---|---|---|
| 2022-01-18 | techhive.dev registered | OS-14 (OBSERVED) |
| 2023-02-05 | First certificate for `appasap.techhive.dev` | OS-14 (OBSERVED) |
| 2023-03-21 | `appasap.ai` registered (Namecheap, privacy proxy). A third-party listing describes an "AppAsap" chat-to-build-app no-code platform, "launched 2025-02-18". The site is currently down (Cloudflare 522). The link to UAB Appasap rests on the name only. | OS-15 |
| 2023-10-05 to 2025-04-28 | GoDaddy-issued certificates for promoat.ai / www.promoat.ai, likely a **previous holder** of the domain | OS-17 |
| 2025-01-19 | hexaflow.ai registered (certificates from 2025-02-12) | OS-16 |
| 2025-02-07 | UAB Appasap registered in Kaunas (aggregator data, unverified) | OS-07 |
| 2025-11-12 | promoat.ai registered, per RDAP's current creation date (Namecheap, privacy proxy) | OS-17 |
| 2025-11-20/25 | New certificates for promoat.ai (DigiCert, then Let's Encrypt) | OS-17 |
| 2025-11-26 | iOS and Android apps first released | OS-18 |
| 2026-01-21 to 2026-10-29 | iOS versions 1.2.0 to 2.3.1 (detail in OS-19) | OS-19 |
| 2026-02-13/16 | `*.promoat.ai`, `forget-password.`, `cdn.` certificates. Privacy policy dated 2026-02-16 | OS-49, OS-02 |
| 2026-03-01 | iOS 1.6.9 release note: "**Name change**". The previous name is unknown | OS-19 |
| 2026-05-09 / 05-17 | First certificates for `docs.promoat.ai` (how-to wiki) and `platform.promoat.ai` (Partner API and dashboard) | OS-21 |
| 2026-05-11 | iOS 2.0.0: "ProMoat 2.0 - Multiscene videos, better viral edits" | OS-19 |
| 2026-05-12 | 15 blog/GEO articles all published on this one day | OS-22 |
| 2026-09-30 | API price table for Partner API v1.1.0 (new video engines) | OS-21 |
| 2026-10-03 | iOS 2.2.1: about 250 credits for a 30 s scene video ("less than half the old price"). "**Social posting and scheduling are gone**". Comparison pages updated the same day | OS-19, OS-22 |
| 2026-10-11 | API price table for v1.2.0: 15 s = 30 credits. v1.3.0 (weekly/monthly plans) came after this date; its exact date is unknown | OS-21 |
| 2026-10-13 | iOS 2.3.0 ("a 30-second video uses about 44 credits"). Play updated (v2.3.0) | OS-19, OS-05 |
| 2026-10-28 | Bulk developer replies to negative reviews ("reduced our pricing by 6x") | OS-46 |
| 2026-10-29 | iOS 2.3.1 | OS-19 |

**OS-15: appasap.ai.** Registered 2023-03-21 (Namecheap, Withheld for Privacy). Cloudflare nameservers. ImprovMX mail forwarding. HTTP 522 on 2026-10-31. SimilarLabs lists "AppAsap", an AI chat-to-app no-code builder, as launched on 2025-02-18. Connecting it to UAB Appasap is an inference from the name only, with low-to-medium confidence.
- Sources: `rdap_appasap.ai.json`, `dns_doh_promoat.ai_and_related.txt`, https://similarlabs.com/zh/p/appasap (`thirdparty_similarlabs.com_zh_p_appasap.html`)
- Type: OBSERVED + INDEPENDENT_SOURCE + INFERENCE

**OS-16: hexaflow.ai** was registered 2025-01-19 (Namecheap, privacy proxy, expires 2027-01-19). It is hosted on Vercel and uses Namecheap Private Email MX. Certificate Transparency shows subdomains `serfa.`, `jobkey.`, `girlfromlinkedin.` and `ramadanmeals.`, which look like client or side projects.
- Sources: `rdap_hexaflow.ai.json`, `crtsh_hexaflow.ai.json`
- Type: OBSERVED

**OS-17: promoat.ai registration history.**
- RDAP:
  - Registered **2025-11-12T10:49:55Z** and expires 2027-11-12.
  - Registrar: NameCheap. Registrant: "Redacted for Privacy / Withheld for Privacy LLC" (US proxy).
  - Nameservers: Cloudflare bowen/ollie. Status: clientTransferProhibited. Last changed 2026-08-12.
- Certificate Transparency also shows **GoDaddy-issued certificates for promoat.ai from 2023-10-05 to 2025-04-28**, then a gap until 2025-11-20.
- Inference: the domain was held and used by an **earlier registrant**, lapsed, and was re-registered on 2025-11-12. A registrar transfer would not reset the creation date, but a drop and re-registration would. The current operator has held the domain since about November 2025. Whether the previous holder was related (for example, the G2 "ProMoat" retail-promotions entry) is unknown. Confidence: medium-high.
- Sources: https://rdap.org/domain/promoat.ai (`rdap_promoat.ai.json`), https://crt.sh/?q=%25.promoat.ai (`crtsh_promoat.ai.json`)
- Type: OBSERVED + INFERENCE

**OS-18: Both apps launched on 2025-11-26.** iTunes `releaseDate` is 2025-11-26T08:00:00Z. Play shows "Nov 26, 2025" (epoch 1764183271 = 2025-11-26 18:54 UTC).
- Sources: `appstore_itunes_lookup_id6754813873_us.json`, `googleplay_com.hexaflow_ai.expoai_en_us.html`
- Type: OFFICIAL_SOURCE

**OS-19: iOS version history, as shown on the App Store.** It starts at 1.2.0 because Apple truncates older entries. The full list is in `appstore_ios_version_history_extracted_from_appstore_web_us.tsv`. Key entries:

| Version | Date | Release note |
|---|---|---|
| 1.2.0 | 2026-01-21 | (earliest shown) |
| 1.3.0 | 2026-02-02 | "Better AI models, Cheaper prices" |
| 1.6.4 | 2026-02-19 | "New offer." |
| 1.6.9 | 2026-03-01 | "Name change" |
| 1.7.6 | 2026-04-14 | "record up to 1 minute" |
| 2.0.0 | 2026-05-11 | "ProMoat 2.0 - Multiscene videos..." |
| 2.1.0 | 2026-07-17 | Better moving-scene video and AI voice options |
| 2.2.1 | 2026-10-03 | Price cut; social posting and scheduling removed; voice-clone and "Fix the sound" features |
| 2.2.2 | 2026-10-04 | AI voice in onboarding |
| 2.3.0 | 2026-10-13 | "A 30-second video uses about 44 credits" |
| 2.3.1 | 2026-10-29 | Voice-clone reset fixes |

- Source: https://apps.apple.com/us/app/id6754813873
- Accessed: 2026-10-31
- Type: OFFICIAL_SOURCE

**OS-20: The product pivoted from a content-marketing and scheduling app to an AI-clone video generator.**
- Earlier positioning:
  - AppGoblin's cached Play description: "Promoat - AI clone videos", with short description "Create videos. Get leads." It calls the app "an AI-powered content marketing app built for founders, creators, and small teams".
  - GetApp: "AI content marketing platform ... multi-platform publishing".
  - An older Capterra snippet: "designed for LinkedIn creators".
  - docs.promoat.ai still documents connecting TikTok, Instagram, YouTube and LinkedIn, plus "Calendar and scheduling".
- The app removed social posting and scheduling in 2.2.1 (2026-10-03), but the `/heygen-alternative` page still claims "built-in Social Media Scheduling".
- The app's name before the 2026-03-01 "Name change" is **unknown**.
- Sources: `thirdparty_appgoblin.info_apps_com.hexaflow_ai.expoai.html`, `thirdparty_www.getapp.com.au_software_2108729_promoat.html`, `official_docs.promoat.ai_{home,connect-social-accounts}.html`, `official_promoat.ai_heygen-alternative.html`
- Type: INDEPENDENT_SOURCE + OFFICIAL_SOURCE + OBSERVED

**OS-21: Partner API (platform.promoat.ai).**
- What it offers:
  - REST endpoints under `/api/partner/v1/`, authenticated with `pmat_` bearer keys.
  - Characters, voices, TTS, first-frame images, talking-head and scene videos, and scene-level edits.
  - An OpenAPI spec, a Swagger playground, and a Claude agent skill (`/skill/SKILL.md`, v1.1.1).
- Versions and dates:
  - The docs show "What's new in 1.3". `openapi.yaml` says `version: "1.2.1"`, so the two are inconsistent.
  - Changelog: 1.1.0 (price table 2026-09-30), 1.1.1, 1.2.0 (price table 2026-10-11), 1.2.1, and 1.3.0 ("credits now come from a plan").
  - No public launch announcement was found.
  - The first certificate for platform.promoat.ai is dated 2026-05-17.
- Inference: the API went live around mid-May 2026 at the earliest, and 1.3.0 followed 2026-10-11. Confidence: medium.
- Sources: `official_platform.promoat.ai_docs*.html`, `official_platform.promoat.ai_openapi.yaml`, `official_platform.promoat.ai_skill_SKILL.md`, `crtsh_promoat.ai.json`
- Type: OFFICIAL_SOURCE + OBSERVED + INFERENCE

**OS-22: All 15 blog articles carry the same publication date.**
- Every article has `datePublished` 2026-05-12. Several have `dateModified` 2026-10-03.
- The author is the Organization.
- Articles include the line "This article is part of ProMoat's **GEO content series**", i.e. content written to be cited by AI chatbots.
- Sources: https://www.promoat.ai/blog and article pages (`official_promoat.ai_*.html`)
- Type: OBSERVED + OFFICIAL_SOURCE

## 4. Funding and partnerships

**OS-23: No funding, investors, accelerator place or commercial partnership was found.** Searches covered official pages and the web (standard and extended modes). Crunchbase returned 403 and no LinkedIn company page exists. No funding claim appears on any official page either. Funding status: **unknown / not available**.
- Source: `websearch_snippets_2026-10-31.txt` (Q8)
- Type: UNKNOWN

**OS-24: The company names its AI model and API vendors, but these are not documented partnerships.**
- Self-disclosed suppliers (blog, May 2026): **Seedream** for the identity bank, a **Kling** video model, **FAL** lip-sync, and **Revid/Submagic** captions. The changelog later mentions unnamed "new video engines" (Sept–Oct 2026).
- AI-agent integration with Claude is via a skill file (OS-38).
- The API docs mention "embedded partners" (a signed `/partner/billing` link and checkout-session endpoint). No partners are named.
- Sources: `official_promoat.ai_synthesia-alternative-for-founders-in-2026.html`, `official_promoat.ai_personalized-ai-video-at-scale.html`, `official_platform.promoat.ai_docs_credits-and-pricing.html`
- Type: OFFICIAL_SOURCE (vendor-usage claims; no independent confirmation)

**OS-25: The blog's performance claims are unverified.** Examples:
- "~94% viseme accuracy" for Arabic
- "matched tests across 12 DTC brands in MENA and the US: +2.4x hold rate, -31% CPM, +1.7x meta-ROAS"
- "2.1x to 3.4x higher CTR"
- "~38% of the per-seat cost of Synthesia's Creator plan"
- "~90 seconds per clip"

No method, data or third-party confirmation is given.
- Source: blog articles dated 2026-05-12
- Type: OFFICIAL_SOURCE (claims only)

## 5. Audience, pricing and policies

**OS-26: Target audience: founders, creators and small businesses, with an Arabic/MENA emphasis.**
- Use cases: UGC ads, talking-head reels, product videos, "faceless" content with an AI avatar or influencer, trend templates, and an invented character reused across videos.
- Language: "English, Arabic and 99+ dialects".
- MENA focus: dedicated MENA and Arabic lip-sync articles.
- Ratings by storefront (OBSERVED): EG 44, US 28, SA 11, AE 5, GB 2.
- Play reviews are dominated by Egyptian-Arabic text.
- Sources: homepage, store descriptions, blog, `appstore_itunes_lookup_*.json`
- Type: OFFICIAL_SOURCE + OBSERVED

**OS-27: iOS in-app purchases (US storefront).**

| Product | Price |
|---|---|
| Trial | $0.99 |
| Weekly1 | $9.99 |
| Starter | $14.99 |
| Growth | $29.99 |
| Pro | $99.99 |
| Influencer | $499.99 |
| Small credit pack | $12.99 |
| Medium Credits pack | $24.99 |
| Large credits pack | $96.90 ("9746 credits - at least 22 PRO videos") |

- The listing does not show which products are subscriptions or what their periods are.
- Source: `appstore_web_id6754813873_us.html`
- Type: OFFICIAL_SOURCE

**OS-28: Google Play shows in-app products from $1.49 to $599.99 per item.**
- Source: `googleplay_com.hexaflow_ai.expoai_en_us.html`
- Type: OFFICIAL_SOURCE

**OS-29: Web and API plans (Partner API v1.3).**
- Plans (sold "at the Promoat app's prices"):

| Plan | Price | Credits |
|---|---|---|
| Weekly | $9.99/week | 559 |
| Monthly | $29.99/month | 2,219 |
| Monthly 3.6× | $99.99/month | 7,999 |

- One-off packs, for subscribers only: Small $12.99 for 779 credits, Medium $24.99 for 1,499 credits.
- Trial: 25 credits, no card needed.
- Credit rules: 1 credit = $0.01. Credits "never expire".
- Prices by length: 15 s = 30 credits and 60 s = 73 credits. Voice clone: first one free, then 30 credits.
- Limits:
  - Voiced audio up to 59.5 s; scripts up to 4,000 characters.
  - Output is vertical 9:16 only, at 480P, 768P or 1080P.
  - Caps on active jobs and on voices (`429 TOO_MANY_ACTIVE_JOBS`, `409 VOICE_LIMIT_REACHED`).
- Sources: `official_platform.promoat.ai_docs_credits-and-pricing.html`, `..._changelog.html`, `..._skill_SKILL.md`, `official_platform.promoat.ai_home.html`
- Source date: price table 2026-10-11
- Type: OFFICIAL_SOURCE

**OS-30: Earlier consumer pricing, as reported by users.**
- A Play review on 2026-03-07 (Egypt) says the price was "1600 [EGP] a month, max 8 videos, max 30 s, no trial even for one video".
- An App Store EG review on 2026-08-23 says "I paid 1499 Egyptian pound".
- The developer replied on 2026-10-28: "we have reduced our pricing by 6x now, and you can create videos up to 1 min".
- Sources: `googleplay_scraper_app_and_reviews.json`, `appstore_rss_reviews_eg.json`
- Type: INDEPENDENT_SOURCE (users) + OFFICIAL_SOURCE (developer reply)

**OS-31: Directory listings make pricing claims that conflict with user reports.** GetApp, Capterra and Software Advice (all G2 network) say "Starting from USD 7.00/month", "Free Trial: Available", typical users "Self Employed, 2-10", and list 0 reviews. These are vendor-maintained, and the free-trial claim conflicts with user reports (OS-42).
- Sources: `thirdparty_www.getapp.com.au_*`, `thirdparty_www.softwareadvice.*`, `thirdparty_www.capterra.in_*`
- Type: OBSERVED (vendor-supplied listing data)

**OS-32: The official onboarding docs put the paywall near the end of setup.** They describe a 12-step activation flow with "Step 11 - Paywall. Pick a plan to render and post. Free / trial users hit this gate; paid users skip it."
- Source: https://docs.promoat.ai/onboarding (`official_docs.promoat.ai_onboarding.html`)
- Type: OFFICIAL_SOURCE

**OS-33: Cancellation and refunds.**
- **Web/API:**
  - "Cancel in Manage subscription on the dashboard. Your plan runs to the end of the period, then stops. Your credits stay".
  - Upgrades start immediately with proration. Downgrades take effect at the end of the period.
  - Billing runs through a "Promoat billing portal". Stripe is observed in the client code (OS-50).
  - **No money-refund policy is published** on promoat.ai, docs or platform. There are no ToS and the sign-up page has no terms link. Only API **credit** refunds for failed jobs are documented.
- **iOS/Android:** purchases are in-app, so subscriptions and refunds run through Apple and Google. This is an inference from the IAP model. The iOS listing links Apple's standard EULA.
- **EU:** no trader declaration on the App Store (OS-04).
- Sources: `official_platform.promoat.ai_docs_credits-and-pricing.html`, `official_platform.promoat.ai_sign-up.html`
- Type: OFFICIAL_SOURCE + OBSERVED + INFERENCE (store mechanics)

**OS-34: Gaps between the privacy policy, the store disclosures and the age ratings.**
- **Privacy policy:**
  - Lists email, phone, usage data and IDFA, and says the Meta SDK is used for personalised ads and attribution, with an ATT prompt.
  - Does **not** mention selfies/photos, voice recordings, biometric or likeness data, GDPR, a data controller or international transfers.
- **Store disclosures:**
  - App Store privacy label: "Data Used to Track You: Identifiers". Data linked to the user includes Photos or Videos, Audio Data, email, and other contact info.
  - Play data safety: Photos (optional), voice recordings (optional), email, in-app messages and IDs are collected. **Videos, device IDs, app activity and crash data are "shared"** with third parties.
- **Age ratings conflict:** App Store 18+ (iTunes field "17+") versus Play "Everyone".
- Sources: `official_promoat.ai_privacy-policy.html`, `appstore_web_id6754813873_us.html`, `googleplay_datasafety_com.hexaflow_ai.expoai.html`
- Type: OBSERVED

## 6. Acquisition channels

**OS-35: SEO and "GEO" (content aimed at AI-chatbot answers) is the main visible owned channel.**
- 4 "alternative" landing pages: HeyGen, Synthesia, D-ID, Colossyan.
- 3 "ProMoat vs X" pages: Synthesia, HeyGen, Arcads.
- 15 long-form "Direct Answer" articles, explicitly labelled a "GEO content series", all listed in the sitemap.
- Sources: `official_promoat.ai_sitemap.xml`, comparison pages
- Type: OFFICIAL_SOURCE + OBSERVED

**OS-36: Paid social and attribution infrastructure is in place, but spend and creatives could not be seen.**
- The privacy policy says the Meta SDK is used "to improve our marketing and user acquisition efforts" and to measure ad campaigns.
- The iOS label declares tracking identifiers.
- The website runs Microsoft Clarity.
- The Meta Ad Library returned HTTP 403 and the TikTok ad library is JS-only, so creatives and spend are **unknown**.
- Sources: `official_promoat.ai_privacy-policy.html`, `official_promoat.ai_home.html`
- Type: OFFICIAL_SOURCE + OBSERVED

**OS-37: There is a weak signal of influencer or YouTube word of mouth.**
- Two Play reviews from February 2026 (Egypt) say users found the app through a YouTuber they call "بيسو" (Beso) and address "Moatassem" by name.
- The YouTuber's identity, and whether the promotion was paid, were not verified. Two reviews are not enough to call this a pattern.
- Source: `googleplay_scraper_app_and_reviews.json`
- Type: INDEPENDENT_SOURCE

**OS-38: AI-agent and B2B channel.**
- The homepage offers "For AI agents", "Use Promoat in your AI agent" and "Connect Promoat to Claude or any AI agent".
- The Partner API, a SKILL.md file for Claude Code, and embedded-partner billing links are all published.
- Type: OFFICIAL_SOURCE

**OS-39: Software directory listings exist but have no reviews.** ProMoat is listed on G2, Capterra, GetApp and Software Advice, all with 0 reviews. A search snippet says the G2 profile is flagged "hasn't been active for over a year".
- Type: OBSERVED

**OS-40: No official social media accounts were found.** The site links no Instagram, TikTok, X, YouTube or LinkedIn account. `linkedin.com/company/promoat` returns 404, and searches for handles found nothing.
- Type: OBSERVED / UNKNOWN

## 7. Customer feedback

**OS-41: Ratings and download counts (do not use these as active users or revenue).**
- App Store:

| Storefront | Average | Ratings |
|---|---|---|
| US | 3.96 | 28 |
| EG | 4.52 | 44 |
| SA | 4.18 | 11 |
| AE | 3.40 | 5 |
| GB | 4.0 | 2 |

- Google Play: 4.70 from **505 ratings**. Histogram: 1★ 15, 2★ 15, 3★ 0, 4★ 45, 5★ 428.
- Play downloads band: **10K+**. Play's embedded install counter shows 17,469, which counts installs, not active users.
- Active users and revenue: **not available**. AppGoblin publishes modelled MAU and revenue estimates. They are not used here as evidence.
- Type: OBSERVED

**OS-42: Pattern A, seen across several sources: the paywall appears only at the end of onboarding, with no free preview.**
- Sources:
  - At least 10 Play reviews (2026-01-22 to 2026-10-26), for example "lets you do everything but blocks you at the final step and asks for payment before even showing the result" (2026-05-06, 6 helpful votes).
  - Arabic reviews saying you only learn it isn't free at "step nine" or "the last step".
  - App Store SA (2026-10-07): "marketed as completely free, forces me to subscribe".
- Corroborated by the official docs (OS-32) and by the developer's templated replies ("I can't afford to create free videos for everyone").
- Type: INDEPENDENT_SOURCE (pattern) + OFFICIAL_SOURCE (corroboration)

**OS-43: Pattern B, seen across several storefronts: "scam" or "took my money and nothing works".**
- App Store US 2026-03-15: "this app is a scam".
- App Store AE 2026-02-21: "they just take your money and it's not working".
- App Store AE 2026-05-19: "just takes the money and then doesn't give you any access".
- Play 2026-02-23: "it's a scam, i subscribe and request refund after less than 1 hour".
- Play 2026-02-22: "liers".
- That is at least 5 reviews across 3 storefronts plus Play. The volume is low and the root cause is unverified: it could be render failures, the paywall model, or billing.
- Type: INDEPENDENT_SOURCE (pattern, low volume)

**OS-44: Pattern C: users find the app too expensive.**
- Play EG reviews on 2026-01-26 (12 helpful votes), 2026-03-07 (8 helpful votes) and 2026-10-06.
- App Store EG on 2026-08-23 (paid 1,499 EGP, "not able to sing [sign] in").
- The developer says prices were cut 6x. This matches iOS 2.2.1 and 2.3.0 notes and the API price-table change from 125 to 30 credits for 15 s.
- Type: INDEPENDENT_SOURCE + OFFICIAL_SOURCE

**OS-45: Positive feedback, including a burst of very short 5★ reviews.**
- Substantive positives: video quality, ease of use, and suitability for camera-shy users (App Store EG 2026-04-02, Play 2026-03-26 and 2026-04-19).
- Between 2026-10-05 and 2026-10-26, about 24 5★ reviews of five words or fewer appeared, mostly in Egyptian Arabic or very short English ("good", "nice", "perfect", "ممتاز"). This coincides with versions 2.2.x and 2.3.0.
- This is noted as an observation only. The authenticity of these reviews was not assessed.
- Type: OBSERVED

**OS-46: Developer responses.** Most negative Play reviews received a templated reply on 2026-10-28, and the App Store US reply was around the same date. Earlier replies are dated 2026-03-12. The tone is personal and first-person, and replies point to a named person's address at promoat.ai (withheld here).
- Type: OBSERVED

**OS-47: No Trustpilot or Reddit feedback was found.** Trustpilot has no page for promoat.ai (WebFetch returned 404). No Reddit discussion turned up in search, and direct Reddit and Product Hunt access returned 403.
- Type: OBSERVED / UNKNOWN

## 8. Infrastructure hints (DNS / CT)

DNS was resolved over DNS-over-HTTPS (dns.google) because `dig`/`whois` are not installed.

**OS-48: promoat.ai DNS records.**

| Record | Value | What it suggests |
|---|---|---|
| NS | `bowen.ns.cloudflare.com`, `ollie.ns.cloudflare.com` | DNS on Cloudflare |
| A (apex) | 216.150.1.1 / 216.150.16.1 | Vercel (ARIN "VERCEL-09") |
| `www`, `platform`, `docs` | CNAME to `*.vercel-dns-016.com` | Hosted on Vercel |
| MX | `mx.zoho.com`, `mx2.zoho.com`, `mx3.zoho.com` | Zoho Mail |
| TXT (SPF) | `v=spf1 include:zohomail.com ~all` | Only Zoho authorised to send; no Stripe, Resend, SendGrid or RevenueCat includes |
| TXT (other) | `zoho-verification`, two `google-site-verification` tokens | Search Console / Workspace-style verification |
| DMARC | none found | No `_dmarc` record |
| DKIM | none found at common selectors | |

- Source: `dns_doh_promoat.ai_and_related.txt`
- Type: OBSERVED

**OS-49: promoat.ai subdomains seen in Certificate Transparency (crt.sh).**

| Subdomain | First certificate | Notes |
|---|---|---|
| `promoat.ai`, `www` | 2025-11 (plus pre-2025 GoDaddy certificates, OS-17) | |
| `*.promoat.ai` | 2026-02-13 | Wildcard |
| `forget-password.` | 2026-02-13 | Password-reset page; resolves to 76.76.21.21 (Vercel) |
| `cdn.` | 2026-02-16 | Google Trust Services certificate; resolves to Cloudflare 104.18.x; serves `/app-assets` and `/user-images/...` |
| `docs.` | 2026-05-09 | How-to wiki on Vercel |
| `platform.` | 2026-05-17 | Partner API and dashboard on Vercel |

- No staging or dev subdomains are exposed.
- Inference: `cdn.` is a Cloudflare-fronted bucket, possibly R2. Confidence: low-medium.
- Source: `crtsh_promoat.ai.json`
- Type: OBSERVED + INFERENCE

**OS-50: The application stack, from public client code.**
- Both sites are Next.js on Vercel (`dpl_` deployment ids, Turbopack chunks).
- The platform's client bundle references a **Supabase** project (`*.supabase.co`) and calls `/api/partner/dashboard/ensure-stripe-customer`, so **Stripe** handles web billing.
- The blog mentions "edge functions" and tables `ugc_videos` / `video_postproduction`, which is consistent with Supabase. Confidence: medium.
- The website uses Microsoft Clarity.
- The Android package `expoai` suggests an Expo/React Native app. Confidence: medium.
- Sources: `official_platform.promoat.ai_home.html` (chunk analysis done in scratch, not stored), `official_promoat.ai_the-two-rail-architecture.html`
- Type: OBSERVED + INFERENCE

**OS-51: Infrastructure of related domains.**
- techhive.dev: GoDaddy DNS, Zoho MX, A record 38.242.147.23 (a Cogent-allocated block; the end customer is unknown). Certificate Transparency shows Coolify/Dokploy PaaS, Grafana, Uptime Kuma and pgAdmin/phpMyAdmin hosts.
- hexaflow.ai: Vercel and Namecheap Private Email.
- appasap.ai: Cloudflare and ImprovMX.
- No shared IP with promoat.ai. The shared elements are the Zoho mail provider (promoat.ai and techhive.dev) and the Namecheap registrar with Withheld for Privacy (promoat.ai, hexaflow.ai, appasap.ai).
- Type: OBSERVED

**OS-52: Mobile app technical facts.**
- iOS: 72.6 MB, requires iOS 15.1+, English UI listed.
- Play: version 2.3.0, updated 2026-10-13. "Contains ads": no. In-app purchases: yes.
- Type: OFFICIAL_SOURCE

## 9. Unknowns, gaps and blocked sources

- **Official registry confirmation is missing for UAB Appasap.** The company code, directors, beneficial owners, shareholders, filed financials and any link to "HexaFlow AI" are all unconfirmed. Blocked or unreachable sources:
  - registrucentras.lt and get.data.gov.lt (HTTP 403, connection reset, HTTP 500)
  - rekvizitai.vz.lt, scoris.lt and okredo.com (Cloudflare challenge / HTTP 403)
  - OpenCorporates (reCAPTCHA; the API needs a token)
  - The turnover band in OS-07's source (EUR 50–100k, from a similar-companies table, entity-level, period not stated) is **not** treated as ProMoat revenue.
- **Revenue and active users: not available.** Downloads, ratings and AppGoblin model estimates are deliberately not converted into revenue or user numbers.
- **Funding, investors and partnerships:** none found (OS-23). Crunchbase, G2, Product Hunt and LinkedIn were blocked.
- **Co-founders:** the blog says "co-founders" but none are named. The roles of M. Rashad and Jasmin A. in ProMoat (as opposed to the HexaFlow agency) are unconfirmed. The founder's employers and education could not be read (LinkedIn HTTP 999).
- **Earlier app name** before the "Name change" (iOS 1.6.9, 2026-03-01), and iOS versions before 1.2.0: unknown. The Wayback Machine (web.archive.org) was **blocked**: the egress proxy reset the connection, and WebFetch was refused.
- **Previous holder of promoat.ai (2023–2025)** and whether it is connected to the current operator: unknown.
- **Partner API launch date and any named partners or customers:** not published.
- **Paid acquisition:** the Meta Ad Library returned 403 and the TikTok ad library needs JavaScript. Spend, creatives and geo-targeting are unknown.
- **Official social accounts (IG/TikTok/X/YouTube/LinkedIn):** none found.
- **Third-party review sites:** no Trustpilot page exists. Reddit, Product Hunt, G2 and Clutch returned 403.
- **Refund behaviour in practice,** for example whether refunds requested through Apple or Google were granted: unknown.
- **Which video and voice models run today:** the blog named Seedream, Kling, FAL and Revid/Submagic in May 2026. The engines introduced in September–October 2026 are unnamed.
- **Unconfirmed related domains:** whether the AppAsap no-code platform (appasap.ai, launched 2025-02-18 per SimilarLabs) belongs to UAB Appasap, and who owns hexaflowai.com, are both unverified.
