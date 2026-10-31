// Follow the public "Start now" onboarding entry while signed in; record what the official UI does.
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ storageState: process.env.STATE, viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const net = [];
  page.on('response', r => { const u = new URL(r.url()); if (!/\.(js|css|woff2|png|jpg|jpeg|svg|mp4|webp)$/.test(u.pathname) && !/clarity|bing/.test(u.host)) net.push(`${r.request().method()} ${u.host}${u.pathname} -> ${r.status()}`); });
  await page.goto('https://platform.promoat.ai/', { waitUntil: 'networkidle' });
  await page.getByText('Start now', { exact: true }).first().click();
  await page.waitForTimeout(5000);
  await page.screenshot({ path: process.env.OUT + '/onboarding_start.png', fullPage: true });
  const t = (await page.evaluate(() => document.body.innerText)).replace(/pmat_[A-Za-z0-9_-]+/g, 'pmat_<REDACTED>');
  console.log('URL', new URL(page.url()).pathname, '\n', t.slice(0, 2500), '\nNET', [...new Set(net)].join(' | '));
  await browser.close();
})();
