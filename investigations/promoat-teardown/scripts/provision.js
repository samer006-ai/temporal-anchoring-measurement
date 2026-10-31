// Calls the same endpoint the official onboarding UI calls right after sign-up (POST /api/partner/onboarding/provision),
// from the signed-in research session. Stores any returned API key in the secrets file; prints only redacted output.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ storageState: process.env.STATE });
  const page = await ctx.newPage();
  await page.goto('https://platform.promoat.ai/partner', { waitUntil: 'networkidle' });
  const res = await page.evaluate(async () => { const r = await fetch('/api/partner/onboarding/provision', { method: 'POST' }); return { status: r.status, body: await r.text() }; });
  let body = res.body; const m = body.match(/pmat_[A-Za-z0-9_-]+/);
  if (m) { fs.appendFileSync(process.env.SECRETS, `PROMOAT_KEY=${m[0]}\n`, { mode: 0o600 }); }
  console.log('STATUS', res.status, 'BODY', body.replace(/pmat_[A-Za-z0-9_-]+/g, 'pmat_<REDACTED>').slice(0, 800));
  await browser.close();
})();
