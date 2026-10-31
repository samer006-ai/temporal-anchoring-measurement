// Usage: node capture_pages.js <outdir> <url1> [url2 ...]
// Renders pages in headless Chromium, saves full-page screenshot, visible text,
// and the list of third-party hosts contacted (no cookies/tokens/query strings saved).
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const [outdir, ...urls] = process.argv.slice(2);
  fs.mkdirSync(outdir, { recursive: true });
  const browser = await chromium.launch();
  for (const url of urls) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, locale: 'en-US' });
    const page = await ctx.newPage();
    const hosts = {};
    page.on('request', r => { try { const u = new URL(r.url()); const k = u.host + ' ' + r.resourceType(); hosts[k] = (hosts[k] || 0) + 1; } catch (e) {} });
    const slug = url.replace(/^https?:\/\//, '').replace(/[^a-zA-Z0-9]+/g, '_').slice(0, 80);
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    } catch (e) { console.log('WARN', url, e.message.split('\n')[0]); }
    await page.waitForTimeout(2500);
    await page.screenshot({ path: path.join(outdir, slug + '.png'), fullPage: true });
    const text = await page.evaluate(() => document.body.innerText);
    fs.writeFileSync(path.join(outdir, slug + '.rendered.txt'), `URL: ${url}\nCAPTURED_UTC: ${new Date().toISOString()}\n\n` + text);
    fs.writeFileSync(path.join(outdir, slug + '.hosts.json'), JSON.stringify(hosts, null, 1));
    console.log('OK', url, '->', slug, Object.keys(hosts).length, 'host/type pairs');
    await ctx.close();
  }
  await browser.close();
})();
