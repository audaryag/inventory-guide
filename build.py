#!/usr/bin/env python3
"""Generates index.html from BUILD_GUIDE.md. Re-run after editing the guide."""
import json, re, html, pathlib, datetime, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from steps import steps, part4_markdown

SRC = pathlib.Path("/home/ubuntu/BUILD_GUIDE.md")
OUT = pathlib.Path(__file__).with_name("index.html")

md = SRC.read_text()

# PART 4 is generated from spec.py so the guided steps and the written guide cannot diverge
_p4s, _p4e = md.index("# PART 4 "), md.index("# PART 5 ")
md = md[:_p4s] + part4_markdown() + "\n" + md[_p4e:]
SRC.write_text(md)
appA = md[md.index("# Appendix A"):md.index("# Appendix B")]
appB = md[md.index("# Appendix B"):]
guide = md[:md.index("# Appendix A")].rstrip().rstrip("-").rstrip()


def parse_queries(txt):
    out = []
    for m in re.finditer(r"\n## (.+?)\n(.*?)```\n(.*?)\n```", txt, re.S):
        name, mid, code = m.group(1).strip(), m.group(2), m.group(3)
        note = " ".join(l.lstrip("> ").strip() for l in mid.splitlines()
                        if l.strip().startswith(">"))
        out.append({"name": name, "note": note, "code": code})
    return out


def parse_measures(txt):
    out = []
    for m in re.finditer(r"```\n(.*?)\n```", txt, re.S):
        for chunk in m.group(1).split("\n\n"):
            chunk = chunk.strip()
            if chunk:
                out.append({"name": chunk.split("=")[0].strip(), "note": "", "code": chunk})
    return out


def md_to_html(text):
    """Minimal markdown -> HTML for the walkthrough (headings, tables, lists, code)."""
    lines, out, in_tbl, in_ul = text.split("\n"), [], False, None

    def inline(s):
        s = html.escape(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        return s

    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            buf = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            out.append("<pre class='plain'>%s</pre>" % html.escape("\n".join(buf)))
            i += 1
            continue
        if ln.startswith("|"):
            cells = [c.strip() for c in ln.strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                i += 1
                continue
            if not in_tbl:
                out.append("<table>"); in_tbl = True
                out.append("<tr>%s</tr>" % "".join("<th>%s</th>" % inline(c) for c in cells))
            else:
                out.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in cells))
            i += 1
            continue
        if in_tbl:
            out.append("</table>"); in_tbl = False
        m = re.match(r"^(#{1,4}) (.*)", ln)
        if m:
            if in_ul:
                out.append("</%s>" % in_ul); in_ul = None
            lvl = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, inline(m.group(2)), lvl))
            i += 1
            continue
        m = re.match(r"^\s*(?:([-*])|\d+\.) (.*)", ln)
        if m:
            tag = "ul" if m.group(1) else "ol"
            if in_ul and in_ul != tag:
                out.append("</%s>" % in_ul); in_ul = None
            if not in_ul:
                out.append("<%s>" % tag); in_ul = tag
            out.append("<li>%s</li>" % inline(m.group(2)))
            i += 1
            continue
        if in_ul:
            out.append("</%s>" % in_ul); in_ul = None
        if ln.lstrip().startswith(">"):
            buf = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                buf.append(lines[i].lstrip().lstrip(">").strip()); i += 1
            out.append("<blockquote>%s</blockquote>" % inline(" ".join(buf)))
            continue
        if ln.strip() in ("", "---"):
            out.append("<hr>" if ln.strip() == "---" else "")
            i += 1
            continue
        # gather consecutive plain lines into one paragraph
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#{1,4} |\||```|>|\s*(?:[-*]|\d+\.) )", lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(para)))
    if in_tbl:
        out.append("</table>")
    if in_ul:
        out.append("</%s>" % in_ul)
    return "\n".join(x for x in out if x)


queries, measures = parse_queries(appA), parse_measures(appB)
STEPS = steps()


def cards(items, kind):
    h = []
    for n, it in enumerate(items, 1):
        note = "<p class='note'>%s</p>" % html.escape(it["note"]) if it["note"] else ""
        h.append(f"""
<section class="card" id="{kind}-{n}" data-name="{html.escape(it['name']).lower()}">
  <header>
    <span class="num">{n}</span>
    <h3>{html.escape(it['name'])}</h3>
    <button class="copy" data-text="{html.escape(it['name'], quote=True)}">Copy name</button>
    <button class="copy" data-target="{kind}code{n}">Copy code</button>
    <button class="done" data-key="{kind}-{n}">Done</button>
  </header>
  {note}
  <pre id="{kind}code{n}">{html.escape(it['code'])}</pre>
</section>""")
    return "\n".join(h)


CSS = """
:root{--bg:#0f1115;--panel:#171a21;--line:#262b36;--fg:#e6e9ef;--dim:#9aa4b2;--acc:#4FA45F;--ok:#8CC63F}
*{box-sizing:border-box}
body{margin:0;font:15px/1.55 Arial,Helvetica,sans-serif;background:var(--bg);color:var(--fg)}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px 80px}
h1{font-size:26px;margin:28px 0 6px}
.sub{color:var(--dim);margin:0 0 20px}
img{max-width:100%;border:1px solid var(--line);border-radius:6px;margin:8px 0}
ol,ul{margin:8px 0 8px 22px}li{margin:4px 0;line-height:1.5}
nav.tabs{position:sticky;top:0;z-index:20;background:var(--bg);border-bottom:1px solid var(--line);
  display:flex;gap:6px;padding:10px 0;flex-wrap:wrap}
nav.tabs button{background:var(--panel);color:var(--fg);border:1px solid var(--line);border-radius:7px;
  padding:8px 14px;cursor:pointer;font-size:14px}
nav.tabs button.on{background:var(--acc);border-color:var(--acc);color:#fff}
#search{flex:1;min-width:160px;background:var(--panel);border:1px solid var(--line);color:var(--fg);
  border-radius:7px;padding:8px 12px;font-size:14px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;margin:14px 0;overflow:hidden}
.card.done{opacity:.5}
.card.done .num{background:var(--ok)}
.card header{display:flex;align-items:center;gap:10px;padding:10px 14px;border-bottom:1px solid var(--line)}
.card h3{margin:0;font-size:15px;font-family:ui-monospace,Menlo,Consolas,monospace;flex:1;word-break:break-all}
.num{background:#39414f;color:#fff;border-radius:20px;min-width:26px;height:24px;display:grid;
  place-items:center;font-size:12px;padding:0 7px}
button.copy,button.done{border:1px solid var(--line);background:#232936;color:var(--fg);border-radius:6px;
  padding:6px 12px;font-size:13px;cursor:pointer;white-space:nowrap}
button.copy:hover,button.done:hover{border-color:var(--acc)}
button.copy.ok{background:var(--ok);border-color:var(--ok);color:#fff}
.note{margin:10px 14px 0;color:var(--dim);font-size:13px;border-left:2px solid var(--acc);padding-left:10px}
pre{margin:12px 14px 14px;padding:12px;background:#0c0e13;border:1px solid var(--line);border-radius:7px;
  overflow-x:auto;font:13px/1.5 ui-monospace,Menlo,Consolas,monospace;white-space:pre}
pre.plain{margin:12px 0}
.panel{display:none}
.panel.on{display:block}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:14px;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{background:#1c2130}
code{background:#0c0e13;border:1px solid var(--line);border-radius:4px;padding:1px 5px;font-size:.92em}
h2{margin:26px 0 8px;font-size:20px;border-bottom:1px solid var(--line);padding-bottom:6px}
h3{margin:18px 0 6px;font-size:16px}
hr{border:0;border-top:1px solid var(--line);margin:22px 0}
li{margin:3px 0}
blockquote{margin:12px 0;padding:8px 14px;border-left:3px solid var(--acc);background:#1b2030;
  color:var(--dim);border-radius:0 7px 7px 0}
.bar{display:flex;align-items:center;gap:12px;margin:16px 0 4px;color:var(--dim);font-size:13px}
.bar .track{flex:1;height:7px;background:#232936;border-radius:5px;overflow:hidden}
.bar .fill{height:100%;background:var(--ok);width:0}
footer{color:var(--dim);font-size:12px;margin-top:40px;text-align:center}
.step{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px 22px;margin:10px 0}
.step .pagetag{display:inline-block;background:#232936;border:1px solid var(--line);border-radius:20px;
  padding:3px 12px;font-size:12px;color:var(--dim);margin-bottom:10px}
.step h2{border:0;margin:0 0 14px;font-size:22px;padding:0}
.step ol{margin:0 0 4px;padding-left:22px}
.step ol li{margin:8px 0;font-size:16px}
.step .why{margin:16px 0 0;color:var(--dim);font-size:14px;border-left:2px solid var(--acc);padding-left:12px}
.step .check{margin:16px 0 0;padding:11px 14px;border:1px solid #2f6b45;background:#16241c;
  border-radius:9px;font-size:15px}
.step .check b{color:#8fd3a3}
.step .stuck{margin:10px 0 0;padding:11px 14px;border:1px solid #6b4a2f;background:#241d16;
  border-radius:9px;font-size:14px;color:#e0c9a8}
.step .stuck b{color:#f0b96b}
.kv{margin:16px 0 0;border:1px solid var(--line);border-radius:9px;overflow:hidden}
.kv .row{display:flex;align-items:center;gap:10px;padding:9px 12px;border-top:1px solid var(--line)}
.kv .row:first-child{border-top:0}
.kv .k{color:var(--dim);font-size:13px;min-width:104px}
.kv .v{flex:1;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:14px;word-break:break-all}
.kv .row.pos .v{color:#8fd3a3}
button.mini{border:1px solid var(--line);background:#232936;color:var(--fg);border-radius:6px;
  padding:4px 10px;font-size:12px;cursor:pointer}
button.mini:hover{border-color:var(--acc)}
button.mini.ok{background:var(--ok);border-color:var(--ok);color:#fff}
.navrow{display:flex;gap:10px;align-items:center;margin:16px 0 0;position:sticky;bottom:0;
  background:var(--bg);padding:12px 0}
.navrow button{border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:8px;
  padding:11px 20px;font-size:15px;cursor:pointer}
.navrow button.primary{background:var(--acc);border-color:var(--acc);color:#fff;font-weight:600}
.navrow button:disabled{opacity:.4;cursor:default}
.navrow #sreset{margin-left:auto;font-size:13px;padding:8px 12px}
a.dl{display:inline-block;margin:14px 0 0;background:#232936;border:1px solid var(--acc);
  border-radius:7px;padding:9px 14px;text-decoration:none;font-size:14px}
"""

STEPJS = """
const SKEY='invGuideStep';
let si=Math.min(parseInt(localStorage.getItem(SKEY)||'0',10)||0, STEPS.length-1);
function copyText(t,b){
  (async()=>{try{await navigator.clipboard.writeText(t);}
  catch(e){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);
    a.select();document.execCommand('copy');a.remove();}
  const o=b.textContent;b.textContent='Copied';b.classList.add('ok');
  setTimeout(()=>{b.textContent=o;b.classList.remove('ok');},1000);})();
}
function esc(s){return s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function drawStep(){
  const s=STEPS[si];
  const pos=['X','Y','Width','Height'];
  let rows='';
  for(const [k,v] of s.fields){
    rows+='<div class="row'+(pos.includes(k)?' pos':'')+'"><span class="k">'+esc(k)+'</span>'+
          '<span class="v">'+esc(v)+'</span>'+
          '<button class="mini" data-copy="'+esc(v)+'">Copy</button></div>';
  }
  document.getElementById('stepbox').innerHTML =
    (s.page && s.page!=='\u2014' ? '<span class="pagetag">Page: '+esc(s.page)+'</span>' : '')+
    '<h2>'+esc(s.title)+'</h2>'+
    '<ol>'+s.do.map(d=>'<li>'+esc(d)+'</li>').join('')+'</ol>'+
    (rows?'<div class="kv">'+rows+'</div>':'')+
    (s.link?'<p><a class="dl" href="'+s.link+'" download>Download '+esc(s.link)+'</a></p>':'')+
    (s.check?'<div class="check"><b>Check before moving on:</b> '+esc(s.check)+'</div>':'')+
    (s.stuck?'<div class="stuck"><b>If that is not what you see:</b> '+esc(s.stuck)+'</div>':'')+
    (s.note?'<p class="why">'+esc(s.note)+'</p>':'');
  document.querySelectorAll('#stepbox button.mini').forEach(b=>
    b.onclick=()=>copyText(b.dataset.copy,b));
  document.getElementById('sprev').disabled = si===0;
  document.getElementById('snext').disabled = si===STEPS.length-1;
  document.getElementById('snext').textContent = si===STEPS.length-1?'Finished':'Next \u2192';
  document.getElementById('stext').textContent='Step '+(si+1)+' of '+STEPS.length;
  document.getElementById('sfill').style.width=(100*(si+1)/STEPS.length)+'%';
  localStorage.setItem(SKEY,si);
}
document.getElementById('snext').onclick=()=>{if(si<STEPS.length-1){si++;drawStep();window.scrollTo(0,0);}};
document.getElementById('sprev').onclick=()=>{if(si>0){si--;drawStep();window.scrollTo(0,0);}};
document.getElementById('sreset').onclick=()=>{si=0;drawStep();window.scrollTo(0,0);};
drawStep();
"""

JS = """
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
$$('nav.tabs button[data-tab]').forEach(b=>b.onclick=()=>{
  $$('nav.tabs button[data-tab]').forEach(x=>x.classList.toggle('on',x===b));
  $$('.panel').forEach(p=>p.classList.toggle('on',p.id==='tab-'+b.dataset.tab));
  $('#qbar').style.display = (b.dataset.tab==='q'||b.dataset.tab==='m') ? '' : 'none';
  window.scrollTo(0,0);
});
$$('button.copy').forEach(b=>{const label=b.textContent;b.onclick=async()=>{
  const t = b.dataset.text!==undefined ? b.dataset.text
          : document.getElementById(b.dataset.target).textContent;
  try{await navigator.clipboard.writeText(t);}
  catch(e){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);
    a.select();document.execCommand('copy');a.remove();}
  b.textContent='Copied';b.classList.add('ok');
  setTimeout(()=>{b.textContent=label;b.classList.remove('ok');},1200);
};});
const KEY='invGuideDone';
const done=new Set(JSON.parse(localStorage.getItem(KEY)||'[]'));
function paint(){
  $$('.card').forEach(c=>c.classList.toggle('done',done.has(c.id)));
  $$('button.done').forEach(b=>b.textContent=done.has(b.dataset.key)?'Undo':'Done');
  const q=$$('.card[id^=q-]').length, d=$$('.card[id^=q-]').filter(c=>done.has(c.id)).length;
  $('#pfill').style.width=(q?100*d/q:0)+'%';
  $('#ptext').textContent=d+' of '+q+' queries done';
}
$$('button.done').forEach(b=>b.onclick=()=>{
  const k=b.dataset.key; done.has(k)?done.delete(k):done.add(k);
  localStorage.setItem(KEY,JSON.stringify([...done])); paint();
});
$('#search').oninput=e=>{
  const v=e.target.value.trim().toLowerCase();
  $$('.card').forEach(c=>{
    c.style.display=(!v||c.dataset.name.includes(v)||
      c.querySelector('pre').textContent.toLowerCase().includes(v))?'':'none';
  });
};
$('#reset').onclick=()=>{if(confirm('Clear all Done ticks?')){done.clear();
  localStorage.setItem(KEY,'[]');paint();}};
paint();
"""

FAST = """
<blockquote><strong>If the download will not open in your Power BI, stop trying.</strong>
Some Power BI builds refuse the project format no matter what is ticked. Go to the
<strong>Queries</strong>, <strong>Measures</strong> and <strong>Build it</strong> tabs and build it by
hand instead — that route is checked by a script every time this page is published, so the
queries, the 11 relationships, the 40 measures and all 64 visuals are guaranteed to agree with
each other. Every step there now also tells you what you should see on screen before you move
on, and Part 6 of the Walkthrough lists every error we have hit with its one-line fix.</blockquote>

<h2>Start here — the report is already built</h2>
<p class="sub">You do not have to make the tables, the measures, the relationships or the pages.
They are all inside one download. You open it, tell it where your folder is, and press Refresh.
The other tabs stay as a fallback if you ever want to rebuild a piece by hand.</p>

<h3>Before you start: your folder must look exactly like this</h3>
<pre>Inventory Report\\
    RM Raw\\          <- the MB5B raw-material files, untouched
    FG Raw\\          <- the MB5B finished-goods files, untouched
    Consble Raw\\     <- the MB5B consumables files, untouched
    TB\\              <- the TB files, named TB_YYYYMM.xlsx
    Variables and Calculations.xlsx</pre>
<p class="sub">Nothing is ever written back to those files. The report reads them and does the
work in memory, so the SAP downloads stay exactly as they came out of SAP.</p>

<h3>1. One setting, once</h3>
<ol>
<li>Open Power BI Desktop.</li>
<li><strong>File → Options and settings → Options</strong>.</li>
<li>Left-hand list, under GLOBAL, click <strong>Preview features</strong>.</li>
<li>Tick <strong>Store reports using enhanced metadata format (PBIR)</strong>. Click <strong>OK</strong>.</li>
<li>Close Power BI Desktop completely and open it again. (The tick only takes effect after a restart.)</li>
</ol>

<h3>2. Download and unzip</h3>
<ol>
<li>Download <a href="InventoryReport-pbip.zip"><strong>InventoryReport-pbip.zip</strong></a>.</li>
<li>Right-click the downloaded file → <strong>Extract All…</strong> → put it in
<code>Documents</code>. Do not leave it inside the zip, and do not put it in a folder that
OneDrive is still syncing — wait for the green tick if you use OneDrive.</li>
<li>Open the extracted folder. You will see <code>Inventory Report.pbip</code>,
<code>Inventory Report.Report</code> and <code>Inventory Report.SemanticModel</code>.
All three must stay together in the same folder.</li>
</ol>

<h3>3. Open it</h3>
<ol>
<li>Double-click <strong>Inventory Report.pbip</strong>. Power BI Desktop opens with all five
pages already made.</li>
<li>It will show errors or blank visuals at first — that is expected, it has not read your
files yet. Carry on.</li>
</ol>

<h3>4. Tell it where your folder is (the only thing you type)</h3>
<ol>
<li><strong>Home</strong> tab → click the small arrow under <strong>Transform data</strong> →
click <strong>Edit parameters</strong>.</li>
<li>A box appears with one parameter called <strong>pRoot</strong>.</li>
<li>Delete what is in it and type your real folder path, with no backslash on the end, e.g.
<code>C:\\Users\\alisha\\Documents\\Inventory Report</code>.
The quickest way to get it right: open the folder in File Explorer, click once in the address
bar, copy what appears, and paste it in.</li>
<li>Click <strong>OK</strong>.</li>
</ol>

<h3>5. Refresh and save</h3>
<ol>
<li><strong>Home</strong> tab → <strong>Refresh</strong>. Wait — the first refresh reads every file
and can take a few minutes.</li>
<li>Press <strong>Ctrl+S</strong>.</li>
<li>Look at the <strong>Overview</strong> page. If the cards show numbers, you are done.</li>
</ol>

<h3>6. Every month after that</h3>
<ol>
<li>Drop the new month's MB5B files into <code>RM Raw</code>, <code>FG Raw</code>,
<code>Consble Raw</code> and the new TB file into <code>TB</code> as
<code>TB_YYYYMM.xlsx</code>.</li>
<li>Open the report, press <strong>Refresh</strong>, press <strong>Ctrl+S</strong>. Nothing else.
The matrices already follow the last four months, so the new month appears and the oldest drops
off on its own.</li>
</ol>

<h3>7. To share it with people</h3>
<p class="sub"><strong>File → Save as</strong> → change the type to
<strong>Power BI files (*.pbix)</strong> → save that copy on SharePoint or OneDrive. Or
<strong>Home → Publish</strong> to put it in the Power BI service. The .pbip folder is the
master copy — keep it.</p>

<h3>What the five pages look like</h3>
<p class="sub">These are drawn from the project file itself — same page size, same visuals in the
same places, same fields — with made-up numbers. They are not screenshots of Power BI Desktop:
Power BI Desktop only runs on Windows, so it could not be opened and photographed on the machine
that generated the file.</p>
<p><img src="pbip-overview.png" alt="Overview"><img src="pbip-summary.png" alt="Summary">
<img src="pbip-fg.png" alt="FG"><img src="pbip-rm.png" alt="RM">
<img src="pbip-detail.png" alt="Detail"></p>

<h3>How the file was checked before you got it</h3>
<ul>
<li>The model was loaded with Microsoft's own Analysis Services library (the same object model
Power BI uses for tables, columns, relationships and measures) — 14 tables, 11 relationships,
40 measures, 17 helper queries, <strong>0 validation errors</strong>.</li>
<li>Every page and visual file was checked against Microsoft's published report schemas —
5 pages, 64 visuals, <strong>0 errors</strong>.</li>
<li>Every field and measure a visual refers to was checked to exist in the model, and every
query was checked to only depend on queries that exist — <strong>0 problems</strong>.</li>
<li>The manual route is checked separately and straight out of the guide text: the 31 query
code blocks are read step by step to work out which columns each one really produces, and every
measure, relationship, sort-by, hide and drag-this-field instruction is then checked against
those columns — 231 columns, 98 field references, <strong>0 problems</strong>. That is what stops
a step naming a field that does not exist.</li>
<li>What could <em>not</em> be checked here: Power BI Desktop itself only runs on Windows, so the
file was never opened, refreshed or photographed in Desktop. The first refresh on your laptop is
the first time it touches real files. If it complains, send me the exact red text.</li>
</ul>

<h3>If something goes wrong</h3>
<table>
<tr><th>What you see</th><th>What to do</th></tr>
<tr><td>It refuses to open the .pbip, or mentions an unsupported report format</td>
<td>Step 1 was skipped or Power BI was not restarted. Do step 1 again, close Power BI fully,
reopen.</td></tr>
<tr><td><em>DataSource.Error … could not find the folder</em></td>
<td>pRoot is wrong. Redo step 4 and check the four sub-folders are named exactly
<code>RM Raw</code>, <code>FG Raw</code>, <code>Consble Raw</code>, <code>TB</code>.</td></tr>
<tr><td>Everything refreshes but <code>Month</code> is blank on TB</td>
<td>A TB file is not named <code>TB_YYYYMM.xlsx</code>. Rename it and refresh.</td></tr>
<tr><td>Days is blank for 1905</td>
<td>Correct. 1905 has no module capacity in the Variables workbook, so a blank is shown rather
than an invented number.</td></tr>
<tr><td>One visual says something is missing</td>
<td>Send me the exact red text. Do not start rebuilding — it will be one line to fix.</td></tr>
</table>
"""

HTML = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Inventory Power BI — build guide</title>
<style>{CSS}</style></head><body>
<div class="wrap">
<h1>Inventory Power BI — build guide</h1>
<p class="sub">New here? <strong>Start here</strong> — the finished file is ready to download, so you
do not have to build anything by hand. The other tabs are the manual route, kept as a fallback.</p>
<p class="sub">On every block: <strong>Copy code</strong> for the Advanced Editor, and
<strong>Copy name</strong> for the rename box, so nothing is ever typed by hand.
Tick <strong>Done</strong> to keep your place — it is remembered in this browser.
Building the pages? Use <strong>Build it</strong> — one instruction per screen.</p>

<nav class="tabs">
  <button data-tab="f" class="on">Start here</button>
  <button data-tab="q">Queries ({len(queries)})</button>
  <button data-tab="m">Measures ({len(measures)})</button>
  <button data-tab="b">Build it ({len(STEPS)})</button>
  <button data-tab="g">Walkthrough</button>
  <input id="search" placeholder="Search a query name or code…">
  <button id="reset" title="Clear progress">Reset</button>
</nav>

<div class="bar" id="qbar" style="display:none"><span id="ptext"></span><span class="track"><span class="fill" id="pfill"></span></span></div>

<div class="panel on" id="tab-f">{FAST}</div>

<div class="panel" id="tab-q">
  <p class="sub">One query per box, in this order. For each: <strong>Home → New Source → Blank Query</strong>,
  then <strong>Home → Advanced Editor</strong>, Ctrl+A, Delete, paste, <strong>Done</strong>,
  then right-click the query → <strong>Rename</strong> and type the name shown.
  Never paste two boxes into one editor. Errors are normal until all {len(queries)} exist.</p>
  {cards(queries, 'q')}
</div>

<div class="panel" id="tab-m">
  <p class="sub">In report view: <strong>Home → New measure</strong>, paste, Enter. One per box.</p>
  {cards(measures, 'm')}
</div>

<div class="panel" id="tab-b">
  <div class="bar"><span id="stext"></span><span class="track"><span class="fill" id="sfill"></span></span></div>
  <section class="step" id="stepbox"></section>
  <div class="navrow">
    <button id="sprev">&larr; Back</button>
    <button id="snext" class="primary">Next &rarr;</button>
    <button id="sreset" title="Back to step 1">Start over</button>
  </div>
</div>

<div class="panel" id="tab-g">{md_to_html(guide)}</div>

<footer>Updated {datetime.datetime.utcnow():%d %b %Y %H:%M} UTC</footer>
</div>
<script>const STEPS = {json.dumps(STEPS)};</script>
<script>{JS}</script>
<script>{STEPJS}</script>
</body></html>
"""

OUT.write_text(HTML)
print("wrote", OUT, len(HTML), "bytes;", len(queries), "queries;", len(measures), "measures")
