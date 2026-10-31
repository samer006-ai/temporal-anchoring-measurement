// Sign up for the Promoat partner dashboard with credentials read from env.
// Logs only URLs paths/status of auth-related requests (no bodies, no tokens).
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const { PROMOAT_EMAIL: email, PROMOAT_PASSWORD: pw, OUT } = process.env;
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const log = [];
  page.on('response', r => { const u = new URL(r.url()); if (!/\.(js|css|woff2|png|jpg|svg)$/.test(u.pathname) && !/clarity|bing/.test(u.host)) log.push(`${r.request().method()} ${u.host}${u.pathname} -> ${r.status()}`); });
  await page.goto('https://platform.promoat.ai/sign-up', { waitUntil: 'networkidle' });
  const inputs = await page.$$eval('input', els => els.map(e => ({ name: e.name, type: e.type, placeholder: e.placeholder, id: e.id })));
  console.log('INPUTS', JSON.stringify(inputs));
  const labels = ['Full name', 'Organization', 'Email', 'Password', 'Confirm password'];
  const values = ['Samer', 'Independent research', email, pw, pw];
  for (let i = 0; i < labels.length; i++) await page.getByLabel(labels[i], { exact: true }).fill(values[i]);
  await page.getByRole('button', { name: /create account/i }).click();
  await page.waitForTimeout(8000);
  await page.screenshot({ path: OUT + '/signup_result.png', fullPage: true });
  const text = await page.evaluate(() => document.body.innerText);
  console.log('URL_AFTER', new URL(page.url()).pathname);
  console.log('TEXT_AFTER\n' + text.slice(0, 1500));
  console.log('NET\n' + log.join('\n'));
  await ctx.storageState({ path: process.env.STATE });
  await browser.close();
})();
