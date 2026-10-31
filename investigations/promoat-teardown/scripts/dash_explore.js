// Visit dashboard pages with the saved research-account session; save screenshot + visible text + links.
// Usage: STATE=... OUT=... node dash_explore.js /partner /partner/plans ...
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ storageState: process.env.STATE, viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const net = [];
  page.on('response', r => { const u = new URL(r.url()); if (!/\.(js|css|woff2|png|jpg|jpeg|svg|mp4|webp)$/.test(u.pathname) && !/clarity|bing/.test(u.host)) net.push(`${r.request().method()} ${u.host}${u.pathname} -> ${r.status()}`); });
  for (const p of process.argv.slice(2)) {
    net.length = 0;
    await page.goto('https://platform.promoat.ai' + p, { waitUntil: 'networkidle', timeout: 60000 }).catch(e => console.log('WARN', e.message.split('\n')[0]));
    await page.waitForTimeout(2500);
    const slug = 'dash' + p.replace(/[^a-z0-9]+/gi, '_');
    await page.screenshot({ path: path.join(process.env.OUT, slug + '.png'), fullPage: true });
    let text = await page.evaluate(() => document.body.innerText);
    text = text.replace(/pmat_[A-Za-z0-9_-]+/g, 'pmat_<REDACTED>');
    const links = await page.$$eval('a', as => [...new Set(as.map(a => a.getAttribute('href')).filter(Boolean))]);
    fs.writeFileSync(path.join(process.env.OUT, slug + '.txt'), `PATH ${p}\nFINAL ${new URL(page.url()).pathname}\nCAPTURED ${new Date().toISOString()}\n\n${text}\n\nLINKS ${JSON.stringify(links)}\n\nNET\n${[...new Set(net)].join('\n')}\n`);
    console.log('=== ' + p + ' -> ' + new URL(page.url()).pathname + '\n' + text.slice(0, 2500) + '\nLINKS ' + JSON.stringify(links) + '\nNET ' + [...new Set(net)].join(' | '));
  }
  await ctx.storageState({ path: process.env.STATE });
  await browser.close();
})();
