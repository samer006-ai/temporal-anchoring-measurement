// Select the Weekly plan in the official Plans UI, press Subscribe, and capture the Stripe Checkout page
// (text + screenshot) WITHOUT entering any payment data. The checkout URL is written to the secrets dir only.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ storageState: process.env.STATE, viewport: { width: 1280, height: 1000 } });
  const page = await ctx.newPage();
  const net = [];
  page.on('response', r => { const u = new URL(r.url()); if (/api\/partner/.test(u.pathname)) net.push(`${r.request().method()} ${u.pathname} -> ${r.status()}`); });
  await page.goto('https://platform.promoat.ai/partner/plans', { waitUntil: 'networkidle' });
  await page.getByText('$9.99/wk', { exact: false }).first().click();
  await page.waitForTimeout(800);
  await page.getByRole('button', { name: /subscribe/i }).click();
  await page.waitForURL(/checkout\.stripe\.com|stripe/, { timeout: 45000 }).catch(e => console.log('WARN no stripe nav', e.message.split('\n')[0]));
  await page.waitForTimeout(6000);
  const url = page.url();
  fs.writeFileSync(process.env.SECRETS_DIR + '/stripe_checkout_url.txt', url + '\n', { mode: 0o600 });
  await page.screenshot({ path: process.env.OUT + '/stripe_checkout_weekly.png', fullPage: true });
  const t = await page.evaluate(() => document.body.innerText);
  fs.writeFileSync(process.env.OUT + '/stripe_checkout_weekly.txt', `HOST ${new URL(url).host}\nCAPTURED ${new Date().toISOString()}\n\n${t}\n\nNET\n${net.join('\n')}\n`);
  console.log('HOST', new URL(url).host, '\n', t.slice(0, 2000), '\nNET', net.join(' | '));
  await browser.close();
})();
