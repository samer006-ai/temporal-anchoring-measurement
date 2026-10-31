"""Build the private report page (Arabic, RTL) from EXECUTIVE_SUMMARY_AR.md.
The deliverable files are published next to the page and shown in an in-page viewer (fetched by relative URL).
Usage: python build_artifact.py <out.html>"""
import sys, pathlib, markdown, html, json
ROOT = pathlib.Path(__file__).resolve().parent.parent
summary = markdown.markdown((ROOT / "EXECUTIVE_SUMMARY_AR.md").read_text(encoding="utf-8"), extensions=["tables"])
FILES = [("EXECUTIVE_SUMMARY_AR.md", "الخلاصة التنفيذية"), ("PROMOAT_DOSSIER.md", "ملف بروموت الكامل"),
         ("BENCHMARK_RESULTS.csv", "نتائج التجارب"), ("EVIDENCE_INDEX.csv", "فهرس الأدلة"),
         ("COST_LEDGER.csv", "سجل التكاليف"), ("HANDOVER.md", "ملف التسليم"), ("BENCHMARK_PLAN.md", "خطة الاختبار المسجلة مسبقاً")]
media = [m for m in json.loads((ROOT / "benchmark" / "media_manifest.json").read_text(encoding="utf-8"))] if (ROOT / "benchmark" / "media_manifest.json").exists() else []
media_html = "".join(
    f'<figure class="clip"><figcaption><b>{html.escape(m["label"])}</b><span>{html.escape(m["note"])}</span></figcaption>'
    + (f'<video controls preload="metadata" playsinline src="{m["path"]}"></video>' if m["path"].endswith(".mp4") else
       f'<audio controls preload="metadata" src="{m["path"]}"></audio>' if m["path"].endswith(".mp3") else
       f'<img src="{m["path"]}" alt="{html.escape(m["label"])}">')
    + "</figure>" for m in media)
tabs = "".join(f'<button type="button" class="tab" role="tab" id="tab-{i}" data-file="files/{f}" aria-selected="{str(i==0).lower()}">{html.escape(t)}<small>{f}</small></button>' for i, (f, t) in enumerate(FILES))
page = f"""<title>تشريح منصة بروموت</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=Reem+Kufi:wght@500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: one reading column (RTL) for the summary, then a media strip and a file viewer with tabs. */
:root {{
  --bg: #f4f6f3; --surface: #ffffff; --fg: #1b2420; --muted: #5a6661; --line: #d6ddd7;
  --accent: #0d6b5f; --accent-soft: #e2efeb; --warn: #8f5600;
  --display: "Reem Kufi", "IBM Plex Sans Arabic", "Noto Kufi Arabic", Tahoma, sans-serif;
  --body: "IBM Plex Sans Arabic", "Noto Sans Arabic", Tahoma, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #111715; --surface: #18201d; --fg: #e5ece8; --muted: #9ba8a2; --line: #2b3632;
  --accent: #53c2ae; --accent-soft: #1d2f2a; --warn: #e3a64c; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #111715; --surface: #18201d; --fg: #e5ece8; --muted: #9ba8a2; --line: #2b3632;
  --accent: #53c2ae; --accent-soft: #1d2f2a; --warn: #e3a64c; color-scheme: dark; }}
body {{ background: var(--bg); color: var(--fg); font-family: var(--body); font-size: 16px; line-height: 1.75;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 28px 56px; }}
.wrap {{ max-width: 860px; margin: 0 auto; display: grid; gap: 40px; }}
header.top {{ display: grid; gap: 6px; border-bottom: 1px solid var(--line); padding-block: 0 18px; }}
.eyebrow {{ font-size: 13px; color: var(--muted); letter-spacing: .02em; }}
h1, h2, h3 {{ font-family: var(--display); text-wrap: balance; line-height: 1.35; margin: 0; }}
h1 {{ font-size: clamp(28px, 5vw, 40px); color: var(--accent); }}
.doc h1 {{ display: none; }}
.doc h2 {{ font-size: 22px; margin-top: 36px; margin-bottom: 10px; padding-top: 14px; border-top: 1px solid var(--line); }}
.doc h3 {{ font-size: 18px; margin-top: 20px; }}
.doc p, .doc li {{ max-width: 68ch; }}
.doc p {{ margin: 10px 0; }}
.doc ol, .doc ul {{ padding-inline-start: 22px; display: grid; gap: 6px; }}
.doc strong {{ font-weight: 600; }}
.doc p:has(> :only-child), .doc p {{ unicode-bidi: plaintext; }}
.doc hr {{ border: 0; border-top: 1px solid var(--line); }}
.tablebox {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 6px; background: var(--surface); margin: 12px 0; }}
table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
th, td {{ text-align: start; vertical-align: top; padding: 8px 10px; border-bottom: 1px solid var(--line); min-width: 90px; }}
th {{ background: var(--accent-soft); font-weight: 600; }}
tr:last-child td {{ border-bottom: 0; }}
.ids {{ font-family: var(--mono); font-size: 12.5px; color: var(--muted); direction: ltr; text-align: right; }}
section.block {{ display: grid; gap: 14px; min-width: 0; }}
section.block > h2 {{ font-size: 22px; }}
.lede {{ color: var(--muted); max-width: 68ch; margin: 0; }}
.clips {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }}
.clip {{ margin: 0; display: grid; gap: 8px; background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 10px; min-width: 0; }}
.clip figcaption {{ display: grid; gap: 2px; font-size: 13.5px; }}
.clip figcaption span {{ color: var(--muted); }}
.clip video, .clip img {{ width: 100%; max-width: 100%; border-radius: 4px; background: #000; }}
.clip audio {{ width: 100%; }}
.tabs {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.tab {{ font: inherit; font-size: 14px; color: var(--fg); background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 6px 12px; cursor: pointer; display: grid; text-align: start; }}
.tab small {{ font-family: var(--mono); font-size: 11px; color: var(--muted); direction: ltr; }}
.tab[aria-selected="true"] {{ border-color: var(--accent); background: var(--accent-soft); }}
.tab:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
#viewer {{ background: var(--surface); border: 1px solid var(--line); border-radius: 6px; min-height: 160px; min-width: 0; overflow: auto; max-height: 70vh; }}
#viewer pre {{ margin: 0; padding: 14px; font-family: var(--mono); font-size: 12.5px; line-height: 1.6; white-space: pre-wrap; word-break: break-word; direction: ltr; text-align: left; unicode-bidi: plaintext; }}
#viewer table {{ font-size: 12.5px; direction: ltr; }}
#viewer td, #viewer th {{ text-align: left; unicode-bidi: plaintext; min-width: 70px; max-width: 420px; }}
.status {{ color: var(--muted); padding: 14px; }}
footer {{ color: var(--muted); font-size: 13px; border-top: 1px solid var(--line); padding-block: 14px 0; }}
@media (prefers-reduced-motion: reduce) {{ * {{ scroll-behavior: auto; }} }}
</style>
<div class="wrap" dir="rtl" lang="ar">
  <header class="top">
    <span class="eyebrow">تحقيق تقني وتجاري خاص · آخر تحديث 31 أكتوبر 2026</span>
    <h1>تشريح منصة بروموت</h1>
  </header>
  <article class="doc">{summary}</article>
  <section class="block" aria-labelledby="media-h">
    <h2 id="media-h">مخرجات التجارب</h2>
    <p class="lede">ملفات خام كما خرجت من المنصة. التقييم الصوتي يحتاج سماعك وفق معايير خطة الاختبار.</p>
    <div class="clips">{media_html or '<p class="lede">لا توجد مخرجات منشورة بعد.</p>'}</div>
  </section>
  <section class="block" aria-labelledby="files-h">
    <h2 id="files-h">الملفات المسلَّمة</h2>
    <div class="tabs" role="tablist">{tabs}</div>
    <div id="viewer" role="tabpanel" aria-live="polite"><p class="status">جارٍ التحميل…</p></div>
  </section>
  <footer>المحتوى خاص. المفاتيح وكلمات المرور وروابط الدفع غير مضمنة في أي ملف.</footer>
</div>
<script>
(function () {{
  function wrapTables(root) {{ root.querySelectorAll('table').forEach(function (t) {{ if (t.parentElement.classList.contains('tablebox')) return; var d = document.createElement('div'); d.className = 'tablebox'; t.parentNode.insertBefore(d, t); d.appendChild(t); }}); }}
  wrapTables(document.querySelector('.doc'));
  document.querySelectorAll('.doc p').forEach(function (p) {{ if (/^[A-Z]{{1,3}}-[A-Z0-9]+(\\s+[A-Z]{{1,3}}-[A-Z0-9]+)*$/.test(p.textContent.trim())) p.className = 'ids'; }});
  function parseCSV(text) {{
    var rows = [], row = [], f = '', q = false;
    for (var i = 0; i < text.length; i++) {{ var c = text[i];
      if (q) {{ if (c === '"') {{ if (text[i + 1] === '"') {{ f += '"'; i++; }} else q = false; }} else f += c; }}
      else if (c === '"') q = true; else if (c === ',') {{ row.push(f); f = ''; }}
      else if (c === '\\n') {{ row.push(f); rows.push(row); row = []; f = ''; }} else if (c !== '\\r') f += c; }}
    if (f || row.length) {{ row.push(f); rows.push(row); }}
    return rows;
  }}
  var viewer = document.getElementById('viewer');
  function show(btn) {{
    document.querySelectorAll('.tab').forEach(function (b) {{ b.setAttribute('aria-selected', String(b === btn)); }});
    var path = btn.getAttribute('data-file'); viewer.innerHTML = '<p class="status">جارٍ التحميل…</p>';
    fetch(path).then(function (r) {{ if (!r.ok) throw new Error(r.status); return r.text(); }}).then(function (t) {{
      viewer.textContent = '';
      if (/\\.csv$/.test(path)) {{
        var rows = parseCSV(t), tb = document.createElement('table');
        rows.forEach(function (r, i) {{ var tr = document.createElement('tr'); r.forEach(function (c) {{ var td = document.createElement(i ? 'td' : 'th'); td.textContent = c; tr.appendChild(td); }}); tb.appendChild(tr); }});
        viewer.appendChild(tb);
      }} else {{ var pre = document.createElement('pre'); pre.textContent = t; viewer.appendChild(pre); }}
    }}).catch(function (e) {{ viewer.innerHTML = '<p class="status">تعذر تحميل الملف (' + e.message + '). أعد تحميل الصفحة.</p>'; }});
  }}
  document.querySelectorAll('.tab').forEach(function (b) {{ b.addEventListener('click', function () {{ show(b); }}); }});
  var first = document.querySelector('.tab'); if (first) show(first);
}})();
</script>
"""
pathlib.Path(sys.argv[1]).write_text(page, encoding="utf-8")
print("written", sys.argv[1], len(page))
