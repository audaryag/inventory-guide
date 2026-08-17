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
appC = ""              # the field-parameter table went with the toggle; nothing is left here
appB = md[md.index("# Appendix B"):]
appB_old, appB_new = appB.split("## New in this update")
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
new_measures = parse_measures(appB_new)
new_tables = parse_queries(appC)
STEPS = steps()


from edits import EDITS, HOWTO, edit_cards


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
.card ul.elist{margin:10px 14px 4px 30px;font-size:13px;color:var(--dim)}
.card ul.elist li{margin:5px 0}
.card h4{margin:14px 14px 6px;font-size:13px;color:var(--acc);letter-spacing:.02em}
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
  const pos=['Horizontal (X)','Vertical (Y)','Width','Height'];
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
<li>Double-click <strong>Inventory Report.pbip</strong>. Power BI Desktop opens with all six
pages already made (Overview, Summary, FG, RM, Detail, Checks).</li>
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
<li>If anything looks empty, go to the <strong>Checks</strong> page before changing anything: it
names the files that were read, the sheets found in the variables workbook, and the rows the master
sheets do not cover.</li>
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

AUTO = r"""
<h2>Automatic routes — try them in this order</h2>
<p class="sub">Nothing here is typed by hand. One download holds four folders; you only ever open
one of them. If a route fails, close Power BI, open the next route, and lose nothing — the manual
tabs stay exactly as they are.</p>

<p><a href="Variables and Calculations.xlsx"><strong>Download Variables and Calculations.xlsx</strong></a>
&nbsp; the master workbook, on its own and not inside the zip: all six sheets in the shapes the queries read,
the three plants and <code>RM_MW_FACTOR</code> filled in, <code>MW Capacity</code> as a month per column, and the
three master sheets as headings for your own rows to be pasted under. Its first tab says what each sheet is.</p>

<p><a href="InventoryReport-pbip.zip"><strong>Download InventoryReport-pbip.zip</strong></a> &nbsp;
Right-click it &rarr; <strong>Extract All&hellip;</strong> &rarr; put the extracted folder on your
<strong>Desktop</strong>. Open the extracted folder and you will see:</p>
<pre>1 - full report\        the whole thing, five pages of visuals already drawn
2 - model only\         same queries and measures, blank pages
3 - tabular editor\     add-all-measures.csx
4 - plain text\         every query as .m, every measure as .dax
set-proot.ps1           sets your folder path for you
inventory-theme.json    the theme, if you ever need to re-import it</pre>

<h3>Before anything: one Power BI setting, once</h3>
<ol>
<li>Open Power BI Desktop &rarr; <strong>File &rarr; Options and settings &rarr; Options</strong>.</li>
<li>Left list, under GLOBAL, click <strong>Preview features</strong>.</li>
<li>Tick <strong>every</strong> box whose name mentions <em>pbip</em>, <em>Power BI Project</em> or
<em>enhanced report format (PBIR)</em>. Which ones exist depends on your version — tick whatever is
there.</li>
<li><strong>OK</strong>, then close Power BI Desktop completely and reopen it. The ticks do nothing
until you restart.</li>
<li>One more, after the project is open: <strong>File &rarr; Options and settings &rarr; Options
&rarr; CURRENT FILE &rarr; Privacy</strong> &rarr; tick <strong>Always ignore Privacy Level
settings</strong> &rarr; <strong>OK</strong>. Without it Power Query can refuse to combine your own
folders and the refresh stops with <em>&ldquo;may not directly access a data source&rdquo;</em>.</li>
</ol>

<blockquote><strong>Build 35 &mdash; the profit centre matches however it is written:</strong> the export writes it with
two leading zeros the sheet does not have, and Excel holds one side as a number and the other as text. The key now
takes the digits and letters, drops spaces, punctuation and leading zeros, and upper-cases what is left, on both
sides &mdash; so <code>001902001</code>, <code>1902001</code>, <code>1902001.0</code> and <code>1902-001</code> all
meet, while a genuinely different code still does not. The unmatched-pairs table on Checks shows that key beside the
raw value, so a mismatch is something you can see rather than deduce.</blockquote>

<blockquote><strong>Build 34 &mdash; one rule for the trial balance, and a finite list of what is missing:</strong>
build 33 kept the old profit-centre reading as a fallback, so while <code>TB Master</code> was half filled two rules
ran at once and the figures moved further off rather than closer. There is one rule now: a TB line takes its
<strong>Plant</strong> and <strong>Nature</strong> from the row <code>TB Master</code> holds for its
<strong>GL account and profit centre together</strong>, and a pair with no row is in no figure anywhere &mdash; not on
a wrong plant, not in a total. Checks gains <em>GL and profit centre pairs TB Master has no row for</em>, biggest
amount first, which is the whole of what the TB side is missing: type those pairs onto the sheet with their Plant and
Nature and the trial balance is right by construction rather than by luck.</blockquote>

<blockquote><strong>Build 33 &mdash; the trial balance is matched on GL <em>and</em> profit centre, and the FG
technology chart stops drawing RM:</strong> <code>TB Master</code> lists the same GL against all three plants, so the
GL alone is a whitelist and nothing more &mdash; the pair identifies one row of that sheet, and only then do its
<strong>Plant</strong>, <strong>Nature</strong> and <strong>Sort</strong> belong to the trial-balance line. Add a
<strong>Profit Center</strong> column (F) to <code>TB Master</code> and fill the Plant beside it, and Dholera Cell
separates from Module for good. The type comes from the sheet&rsquo;s <strong>Nature</strong> column now &mdash;
Consumables &amp; Spares, Raw Materials &amp; Packing, Finished Goods &mdash; and the account name is read only where
that column is empty, which is what put consumables on the FG row. A pair the sheet does not carry keeps the old
profit-centre reading rather than disappearing, and <code>qcTBPlants</code> shows how many of each profit centre&rsquo;s
rows found their pair, so what is still to be typed is visible. Separately: charts no longer show categories with no
data, which is why <em>FG by Technology</em> was drawing an axis of RM natures with no bars.</blockquote>

<blockquote><strong>Build 32 &mdash; the trial balance takes its plant from the GL, which is what brings Dholera Cell
back:</strong> column C of the TB export against column D of <code>TB Master</code>. That mapping was only ever a last
resort before, tried after the profit centre &mdash; and 1905's profit centre carries no code, so its rows resolved to
nothing and Dholera Cell simply had no trial balance. It is the first thing consulted now, with the profit centre as
the fallback. One guard on it, because it decides whether this is safe rather than merely convenient: a GL that
<code>TB Master</code> gives to <em>two</em> plants cannot name a plant by itself &mdash; the profit centre is then the
only thing separating them &mdash; so a GL is trusted only where the sheet is unanimous about it, and an ambiguous one
falls back rather than moving money to the wrong plant. <code>qcTBByGL</code> on Checks now shows the plant each GL
landed under, so an account under the wrong one is visible in a glance.</blockquote>

<blockquote><strong>Build 31 &mdash; capacity can be typed per plant, which is what 1905 was missing:</strong>
a row on the MW sheet labelled <code>Total</code> is that plant's whole capacity &mdash; the
<em>March&rsquo;26 | MW(S)</em> block on your working, 8.28 against 1902, 6.17 against 1900, 5.63 against 1905.
Days of cover uses it where you have typed one and adds the technology rows up where you have not, so a plant with
both cannot count its capacity twice, and 1905 &mdash; which has no technology rows at all &mdash; gets days of cover
the moment its total is typed. Your existing sheet layout is untouched: this is one more row on it, and
<code>Total</code>, <code>All</code>, <code>All Plants</code> and <code>MW(S)</code> are all read as meaning the same
thing. It never appears as a technology: it is left out of the nature list, so it cannot be sliced or drawn as a slice,
and a technology's own days still divide by its own row.</blockquote>

<blockquote><strong>Build 30 &mdash; the MW sheet is a month per column now:</strong> a plant per row and a column per month,
headed with that month's date, the way your black-and-white table on the FG sheet has it &mdash; a new month is a new
column and nothing already typed is touched. <code>varMWCapacity</code> unpivots it itself and reads three layouts, so
whichever way your sheet is written today it still loads: this new one, the long <em>Effective From | Tech | Valuation
Area | MW</em> one, and the original wide one. A date column is an <em>effective from</em>, so a month with no column of
its own keeps the last figure typed before it; an empty cell stays empty rather than being read as nought, which would
wipe out the figure before it; a dash is nought. The <strong>Techno</strong> column is optional &mdash; leave it out and
the row is that plant's whole capacity, and days of cover then reads per plant with the per-technology figure left blank
rather than invented. A revised <code>Variables and Calculations.xlsx</code> is in the download as
<code>Variables and Calculations - sheet layout.xlsx</code>: all six sheets in the shapes the queries read, the plants
and <code>RM_MW_FACTOR</code> filled in, the masters headers-only for your own rows to go under, and a read-me tab
saying what each sheet is and the one rule for keeping it.</blockquote>

<blockquote><strong>Build 29 &mdash; the plant codes as your workbook has them, and the expandable plant row back:</strong>
1902 is Jaipur Module, 1900 is Dholera Module, 1905 is Dholera Cell. Build 28 had the first two the other way
round, which is why Jaipur and Dholera read each other's figures: the codes were fixed in the code from an
instruction, and your own Summary workbook labels its rows 1902 Jaipur / 1900 Dholera Module &mdash; the figures
against 1902 here (Mar: RM 212.86, FG 209.45, Consumables 19.78) are the figures that sheet prints on the Jaipur
row. The three names are still decided in one place, <code>dimPlant</code>, and read by every page, slicer, legend,
card and row label, and the trial balance now reads a spelled-out profit centre the same way (JAIPUR &rarr; 1902,
CELL &rarr; 1905, DHOLERA &rarr; 1900).
<br><br><strong>Summary's rows are a plant again</strong>, expanding into RM, FG and Consumables, as they were
before build 28: <code>dimPlant[Plant]</code> then <code>dimCategory[Category]</code>, so the table opens on three
plant rows carrying that plant's whole inventory for the month and the + opens the three types underneath.
Flattening them was my answer to Desktop opening things collapsed, and it was the wrong answer: collapsed is what
a plant row should be. The columns stay flat &mdash; the months are the only column field in each of the three
blocks, which is the hierarchy that was actually hiding the history.</blockquote>

<blockquote><strong>Build 28 &mdash; nothing left to expand, and the three plants are now decided in one place:</strong>
your Desktop opens every hierarchy collapsed however the file is saved &mdash; the three metric headings with no
months under them, the plants with no RM / FG / Consumables under them &mdash; so Summary no longer uses one.
Rows are a single flat field, <code>dimPlantType[Plant and Type]</code>, reading <em>1900 Jaipur Module &mdash; RM</em>:
nine rows that are simply there. The three master columns are three matrices sitting flush across one box, headed
<strong>Inventory (TB)</strong>, <strong>Inventory (MB5B)</strong> and <strong>Difference</strong>, each with the months
as its only columns &mdash; the newest March plus the three most recent by default, the slicer overriding that. The
layout you asked for, with no expanding and nothing that can hide.
<br><br>Four faults with it. <strong>The plant names are fixed in the code</strong>: 1900 Jaipur Module, 1902 Dholera
Module, 1905 Dholera Cell, decided in <code>dimPlant</code> and read by every page, slicer, legend, card and row label,
so a swapped pair of rows on the <em>Plant Master</em> sheet can no longer rename a plant anywhere &mdash; that sheet
may still set the sort order, never the name. <strong>1905 in the trial balance</strong>: its profit centre spells the
plant out, and &ldquo;Dholera Cell&rdquo; carries no 1905 to find, so the row was dropped; the plant is now read from
the name as well as the code, in the profit centre, its description and the plant written against that GL on
<em>TB Master</em> &mdash; the GL account being the one key the two sides certainly share. <strong>A plant with no
capacity no longer vanishes</strong>: days of cover is megawatts over the <em>MW Capacity</em> sheet, 1905's
technologies have no row there, and a matrix quietly drops a row whose only figure is blank &mdash; those matrices now
list every plant, blank rather than absent, and <code>qcNatureNoCapacity</code> on Checks names the technologies to add.
<strong>Share of Total % read 100% on every row</strong>: its denominator only dropped the category filter, so on the
Detail matrix each material was divided by itself; it now divides by the visual's own total. The empty
<em>FG by Technology</em> chart is fixed the same way &mdash; it names finished goods inside its measures instead of
leaning on a filter, so an RM nature returns blank and leaves the axis by itself.</blockquote>

<blockquote><strong>Build 27 &mdash; nothing can add two month-ends together any more:</strong> seven measures
used to ask the visual whether a month was on show (<em>ISINSCOPE</em>) and only then return a closing level. A
matrix whose column hierarchy is sitting collapsed does not always answer that truthfully, and the figure came
back as the plain sum over every month in the window &mdash; which is exactly the adding-up you saw when you
ticked four months. They no longer ask: each works out the last month that has rows in the current filter and
returns that month's level unconditionally. A month column is unchanged; a collapsed heading, a quarter, a Total
row or a four-month window all show the newest month's stock. Summary's layout is unchanged from build 26 &mdash;
<strong>Inventory (TB)</strong>, <strong>Inventory (MB5B)</strong> and <strong>Difference</strong> are the master
columns with the months underneath each of them.</blockquote>

<blockquote><strong>Build 26 &mdash; Summary the way you specified it, and two more reasons the TB read high:</strong>
one table, with <strong>Inventory (TB)</strong>, <strong>Inventory (MB5B)</strong> and <strong>Difference</strong> as
the three <em>master</em> columns and the months underneath each of them &mdash; not the other way round, which was
my mistake in build 24. Both column levels are written out open, and the expand arrows are on the column headers
in case a version of Desktop still opens the metric level collapsed. On the figures: SAP writes subtotal and
<em>Result</em> lines into the same column as the accounts, and each one carries the sum of the lines above it, so
a single one left in counts that money twice &mdash; those lines are dropped now. And a TB line arriving twice is
counted once, on the same rule the stock files use: same month, account, profit centre and amount is the same
line, whatever the file was called. The master sheet's plant is also no longer used to rescue a line that has no
profit centre at all, because that line is usually a subtotal.</blockquote>

<blockquote><strong>Build 25 &mdash; Summary is one table:</strong> the six blocks are gone and in their place is a
single matrix across the full width &mdash; a row per plant opening into RM / FG / Consumables, a column per month,
and under each month the three figures side by side: <strong>TB</strong>, <strong>MB5B</strong>,
<strong>Check</strong>. Those three are measures, not a field above the month, which is what keeps it a
one-level column hierarchy and out of the trouble that emptied the page before. The Total row under each plant is
that plant across its three types and the Grand Total row at the foot is every plant added together &mdash; which
is exactly what the three Total Overall blocks used to say, so they are no longer needed. Column subtotals stay
off: there is no Total column adding March to July. The matrix is only as tall as its rows, and the space that
used to sit blank under it has gone to the three charts, which are half again as tall as they were.</blockquote>

<blockquote><strong>Build 23 &mdash; Summary, TB side only:</strong> plant <strong>1905</strong> is back and so is
the <strong>Raw Material</strong> row, and both were mapping faults rather than arithmetic. A trial balance row
carries a profit centre, not a plant, and the plant was read out of characters 3&ndash;6 of it and nowhere else
&mdash; so a profit centre written to any other pattern resolved to no plant and the row was dropped, which is
how a plant goes missing from Inventory (TB) while MB5B still has it. It is now read from those four characters,
then from the first of 1900 / 1902 / 1905 appearing anywhere in the profit centre, then in its description, then
from the Plant or Nature written against that GL on your <strong>TB Master</strong> sheet. Separately, the
RM / FG / Consumables test asked about consumables before raw material, and an account called &ldquo;Raw Material
&amp; Packing&rdquo; holds the word PACK &mdash; so all of RM was filed as Consumables: the RM row vanished and
Consumables read far too high. Raw material is tested first now. Nothing is dropped quietly any more:
<strong>qcTBPlants</strong> on Checks lists every profit centre, what it resolved to and what it is worth, so an
unresolved one can be read off the screen. MB5B, Overview, Detail and the FG and RM layouts are untouched.</blockquote>

<blockquote><strong>Build 21 &mdash; 14 Aug:</strong> no matrix has a two-level column hierarchy any
more. A metric field above a month field opens on the metric level &mdash; one figure per metric, no months
&mdash; and pre-opening it in the file made Desktop draw the visual as an empty card, which is what took
Summary's lower block and the FG and RM tables off the page. The month is now the only column field, with the
metrics as measures underneath named <code>TB</code>, <code>MB5B</code>, <code>Difference</code> and
<code>MW</code>, <code>Rs Cr.</code>, <code>Days</code>: the same grid read the other way, with nothing to
expand. FG by technology now shows money as bars with megawatts as a line, because a technology only has a
megawatt figure where the MW Capacity sheet covers it and as bars that left the chart looking
empty.</blockquote>

<blockquote><strong>Build 20 &mdash; 14 Aug:</strong> <em>Errors in dimTBMaster</em> on all eight rows
was a forced type cast &mdash; <code>Int64.Type</code> on the sort column errors the whole row when a cell
holds a blank, a dash, 1.5 or a number stored as text, and what is lost is the whitelist of inventory GL
accounts, so Inventory (TB) reads empty. Every master column in <code>dimTBMaster</code>,
<code>dimMaterialAttr</code>, <code>varConstants</code> and the trial balance's amount is now converted cell
by cell with a fallback, so an untidy cell becomes a blank instead of an error. There is also a new
<strong>Edits</strong> tab: every fix as find-this / replace-with-this inside one named query, with copy
buttons, so a report you have already built can be corrected in place without downloading anything.</blockquote>

<blockquote><strong>Build 19 &mdash; 14 Aug:</strong> the refresh error is the privacy firewall.
<em>"Query 'factTB' (step 'Typed') references other queries or steps, so it may not directly access a data
source"</em> is Power Query refusing to let a folder source and the workbook meet &mdash; which is the whole
point of the report, since the figures come from the folders and the names from Variables and Calculations.
It surfaced only now because TB Master finally has rows, so the join actually runs. Fix it once:
<strong>File &rarr; Options &rarr; GLOBAL &rarr; Privacy &rarr; "Always ignore Privacy Level settings"</strong>,
then the same under <strong>CURRENT FILE</strong>, then Refresh. Also in this build: the trial balance no
longer needs that pairing at all &mdash; <code>factTB_Staged</code> reads the TB folder and the TB Master
whitelist in one query, and <code>factTB</code> / <code>factTB_Unmapped</code> read nothing but its
<code>Whitelisted</code> flag.</blockquote>

<blockquote><strong>Build 18 &mdash; 14 Aug:</strong> repeated data, now that the master sheets are
filled in. <strong>A stock line that arrives twice is counted once</strong> &mdash; two rows are the same
line when the plant, material, month, special stock, unit and every figure agree, and the file they came
from is deliberately ignored, which catches the same month exported twice into one folder; two genuinely
different lines for a material in a month differ in at least one figure and are both kept.
<strong>One master row per material on FG as well as RM</strong>, so a material written twice on the sheet
cannot multiply its stock. <strong>Two new checks</strong>: <code>qcMasterDupes</code> lists any material
carrying two different natures on a master sheet (only the first can be used, so the sheet decides by
accident which one wins), and <code>qcMonthFiles</code> says whether a month arrived from more than one
file.</blockquote>

<blockquote><strong>Build 17 &mdash; 14 Aug:</strong> read straight off your Checks page.
<strong>The month columns now open under TB / MB5B / Difference</strong> &mdash; a matrix opens on the
outer level of its column hierarchy, so each master column was showing one figure for the whole window,
which is what looked like months being added; both hierarchies are now written out expanded with the
<code>root</code> that build 12 left out. Summary is three plants as rows, each opening into RM / FG /
Consumables, TB / MB5B / Difference as the master columns, and the newest March plus the three months
after it under each. <strong>The plants come from your Plant Master sheet</strong> through
<code>dimPlantMaster</code>, so the plant list is master data like everything else.
<strong>The trial balance stops counting fixed assets as inventory</strong>: TB Master matched none of
your GL accounts and the old fallback kept every row, so Buildings (&#8377;1,977.80 Cr) and Plant &amp;
Machinery were being read as raw material &mdash; Inventory (TB) is now empty until TB Master lists your
inventory GLs, and qcTBByGL names every account that fell out. <strong>Value with No Nature (%)</strong>
is weighted by value rather than rows, because 2.6% of rows was 96% of the money.</blockquote>

<blockquote><strong>Build 16 &mdash; 14 Aug:</strong> <strong>There is no Unallocated plant</strong> &mdash;
not in <code>dimPlant</code>, not in the facts, nowhere. A stock row whose valuation area is blank, or is a
code that is not 1900 / 1902 / 1905, is left out rather than parked on a plant that does not exist, and a
trial-balance row whose profit centre does not resolve to one of the three goes the same way.
<strong>Nothing is dropped silently</strong>: the new <code>qcPlantCodes</code> table on Checks lists every
valuation area the stock files contained, its rows, its value in &#8377; Cr, and whether the report kept it
&mdash; so if a code outside the three is carrying real money, that line says so. <strong>And the by-plant
tables open on March plus the last three months</strong>: <code>In Summary Window</code> pins the newest
March that has data and adds the three most recent months, the rule Overview already used, so Summary, FG
and RM all open on four columns beginning with the year-end close.</blockquote>

<blockquote><strong>Build 15 &mdash; 14 Aug:</strong> built against the real workbook. Its sheets are
<code>RM Nature</code> and <code>TB Master</code>, and <strong>every header in them is now recognised</strong>
&mdash; including <code>NaturePlant</code>, which the guide had been looking for as two separate columns, so
the trial balance's nature was read as missing. <strong>A missing master sheet now loads empty instead of
failing the refresh</strong> (the new <code>fnVarSheetSafe</code> helper): the workbook has no
<code>FG Master</code> sheet at all, and the old code would have stopped dead on it. <strong>And
<code>qcVarHeaders</code> on the Checks page is the line that settles the Unassigned question</strong>: it
prints every sheet, its exact headers and its <strong>DataRows</strong>. The copy sent to me has a header row
and nothing under it &mdash; if your own <code>RM Nature</code> reads DataRows 0, no report can name a
material, because there is nothing to name it from.</blockquote>

<blockquote><strong>Build 14 &mdash; 14 Aug:</strong> one thing only &mdash; the workbook is the master and
the MB5B export has to meet it. <strong>The material key now keeps only letters and digits</strong> and
discards everything else, which covers the non-breaking spaces, tabs, commas and brackets Excel and SAP put
in a cell without showing them; leading zeros are still stripped, and a material that genuinely is
<code>0</code> stays <code>0</code> instead of becoming empty. <strong>A third match, on the material
description</strong>, for the case where the master sheet keys its rows by description rather than by number
&mdash; it only fills a row the first two passes left empty, so it can never overwrite a proper match.
<strong>And <code>qcAttrMatch</code> on the Checks page now asks the same question about descriptions</strong>,
so it tells you whether the two sides meet on the number, on the description, or on neither. That single
line is what decides the rest.</blockquote>

<blockquote><strong>Build 13 &mdash; 14 Aug:</strong> five of these are build 12's own damage and I
would rather say so plainly. <strong>The four matrices that went missing are back</strong> &mdash; Summary's
<code>Total Across All Plants</code>, both FG tables and <code>RM Inventory by Plant</code>: build 12 wrote
an expansion state on to the column hierarchy, and on a matrix whose rows are a single level Desktop
answered by drawing an empty white card. <strong>The Total column now appears only where the columns are
months</strong>: on Summary it was adding Inventory (TB) + Inventory (MB5B) + Difference into one number,
which means nothing; Overview keeps its Total. <strong>There are three plants</strong> &mdash; 1903, 1904 and
1908 come out of the exports and are not plants, so those rows sit on <em>Unallocated</em> with their value
intact, and each plant is labelled with its code (<code>1900 Jaipur Module</code>) so slicer, legend and
ticker read alike. <strong><code>dimNature</code> now carries <em>Consumables</em> and <em>Unassigned</em></strong>,
which is where Detail's <code>(Blank)</code> slice came from. <strong>The megawatt figures sit above their
bars</strong>, not on them, and the <em>% vs last month</em> line you never asked for is off that chart.
<strong>Detail averages instead of adding</strong>: its cards, pies and matrix read
<code>Inventory Rs Cr</code> and <code>Inventory MW</code>, so the page no longer reads 5,393 on a 1,433
report. <strong>And the trial balance stops printing 3.8E-13</strong>: TB is rounded to the paisa and the
difference percentage is blank while the books side is zero &mdash; which it is until TB Master matches your
GL accounts, and that is still the one thing the Checks page has to tell us.</blockquote>

<blockquote><strong>Build 12 &mdash; 14 Aug:</strong> everything you photographed, fixed at its cause.
<strong>Why every nature, technology and group came out <em>Unassigned</em>:</strong> the RM Nature and
FG Master sheets give the material with its leading zeros gone, the MB5B files keep them, so
<code>000000001010203</code> never met <code>1010203</code>. Both sides are now stripped the same way
before the key is built &mdash; which also brings RM's MW and In&nbsp;Days back, because those come from
the BOM quantity on the sheet that never matched. Consumables are labelled
<em>Consumables</em> instead of blank, and anything still unmatched says <em>Unassigned</em> out loud.
<strong>The missing Total:</strong> Inventory by Month had its subtotal switch written Off &mdash; every
matrix now carries a Total row and a Total column, and both hierarchies are written out expanded so the
month columns are open when the page loads. <strong>Figures three and four times too high</strong> on the
two Overview donuts, the FG technology bars and the FG plant donut: a filter that reads a measure is
evaluated once for the whole visual, so all four months still landed in it; those four visuals now use
<code>Latest Month&nbsp;&hellip;</code> measures that set the month themselves. <strong>INR per Wp</strong>
is a measure with <code>DIVIDE</code>, so it is blank rather than <code>NaN</code> where there are no
megawatts. <strong>The Plant slicer</strong> lists each plant once, drops a named plant with nothing behind
it, and shows an unnamed code as <em>Plant 1904</em>. <strong>The panel is green:</strong> Power BI's shape
fill takes a <code>default</code> selector and without one Desktop ignored the colour and drew grey boxes,
which is also why the headings looked invisible. <strong>Cosmetic:</strong> the clipped third line in each
ticker card is gone (it was the measure's name), slicers no longer print <code>MonthName</code> under your
own heading, the axis scales are off with the figures on the visuals instead, stacked columns show the
month's total above the column, the donut legend is off so its labels stop colliding, and the palette
starts at mid green so a stack reads as separate bands. <strong>Two new self-checks</strong> on
<code>Checks</code>: how many materials in each sheet meet the stock files, and the trial balance by GL
account with its sign &mdash; that second one is what will settle the TB question.</blockquote>

<blockquote><strong>Build 11 &mdash; 14 Aug:</strong> the layout scrutinised page by page, and
one thing that was genuinely broken in my own preview: the twelve-month days chart at the foot of
Summary is a plain line chart, and my renderer had no code for that type, so it printed the words
&ldquo;line chart&rdquo; instead of drawing it. It draws now &mdash; three lines, RM, FG and the two added
together &mdash; and the pictures below are the redrawn ones. The report file always had the real
visual; it was the picture that was wrong. While I was in there: the Summary reconciliation matrix is
20 pixels taller so twelve expanded rows fit without scrolling, the plant matrices on FG and RM are
tighter (they only ever hold three rows) and the charts underneath took the space &mdash; 292 tall on
FG, 200 on RM &mdash; because you asked for this to be mostly visual; the RM nature matrix is deeper,
which is where the rows actually are; and the FG days chart's title is shortened so it stops being cut
off in a 428-wide card.</blockquote>

<blockquote><strong>Build 10 &mdash; 14 Aug:</strong> the green panel is now on every page,
in the same place. It was only ever built on <code>Overview</code>, and the generated project drew no
panel at all &mdash; the nine figures floated on the page background, which is why the ticker looked
nothing like the design. The green rectangle, the logo strip, the two heading lines, the two section
labels and the three white boxes are now generated as real Shape visuals at Horizontal 0, Vertical 0,
184 &times; 720 on all six pages, with the nine figures on top of them, identical coordinates
throughout; only the second heading line changes, to the page's own name, so the panel doubles as a
page label. Everything else on <code>Summary</code>, <code>FG</code>, <code>RM</code>,
<code>Detail</code> and <code>Checks</code> has moved to the right of it &mdash; Horizontal 192
rather than 16, narrower in the same proportion &mdash; so nothing sits under the green. The As-on
line is 44 tall instead of 28, which stops the sentence being cut in half. If you are building by
hand, build the panel once and copy it: select the strip on <code>Overview</code>, <strong>Ctrl+C</strong>,
<strong>Ctrl+V</strong> on each of the other five pages.</blockquote>

<blockquote><strong>Build 9 &mdash; 14 Aug:</strong> three changes, all things you asked for.
<br><br><strong>The slicers list only the months you have loaded.</strong> <code>dimDate</code> was
a continuous April-to-March calendar, so every month of the year appeared in the pickers whether or
not a file existed for it. It is now built from the months actually present in the stock files and
the trial balance: put July 2025's MB5B in the folder and Jul'25 becomes an option; until then it
does not exist in the model, and the quarter picker lists only quarters that have data.
<br><br><strong>The newest March is genuinely the first column.</strong> The default window was the
newest March plus the four most recent months, but nothing stopped January and February of the same
year slipping in ahead of it. It now ignores everything before that March, so in August you get Mar,
May, Jun, Jul, Aug and in April just Mar and Apr, March first. Ticking months yourself still
overrides it.
<br><br><strong>The ticker figures are no longer clipped.</strong> The callout size is now worked
out from the box the card has to fit in rather than fixed: 11pt in the 156-wide panel cards, 13pt on
the Total, 14pt on the wide cards on Detail and Checks. Nothing is cut off mid-figure.</blockquote>

<blockquote><strong>Build 8 &mdash; 14 Aug:</strong> build 7 refused to refresh with
<em>&ldquo;14 queries are blocked &hellip; Query 'factTB_Staged' references other queries or steps,
so it may not directly access a data source&rdquo;</em>. That is Power Query's firewall, and it was
my mistake in build 7: I made <code>dimPlant</code> collect the plant codes out of the data, and
<code>factTB_Staged</code> read <code>dimPlant</code> back &mdash; but a query that opens a folder
itself is not allowed to read another query's table. The lookup has moved: the three plant codes are
written inside <code>factTB_Staged</code>, and <code>dimPlant</code> collects the unnamed codes from
both facts while opening nothing. The checker now tests this rule on every query, so no future build
can break the refresh this way.
<br><br>Also do this once, it prevents the whole family of firewall errors:
<strong>File &rarr; Options and settings &rarr; Options &rarr; CURRENT FILE &rarr; Privacy</strong>
&rarr; tick <strong>Always ignore Privacy Level settings</strong> &rarr; OK. All your files are the
same folder on your own machine, so there is nothing to protect from itself.</blockquote>

<blockquote><strong>Build 7 &mdash; 14 Aug:</strong> the month axis is now a real month
column. Build 5 and 6 put the <code>Period</code> field parameter on every axis and asked Power BI
to swap the months in behind it; on your machine it drew the parameter's own two rows instead,
which is why the monthly charts only worked after you changed the axis to <code>MonthName</code> by
hand. The parameter and the two-button toggle are gone: every chart is bound to
<code>dimDate[MonthName]</code>, sorted by month, and every matrix has real month columns. The
measures no longer read the toggle either &mdash; they look at the grain of the visual itself
(<code>ISINSCOPE</code>), so a month column still shows that month's closing stock and a quarter or
a total still averages the month-ends instead of adding them up.
<br><br>Also in build 7: <strong>March is the default first column</strong> &mdash; the newest March
that has data, then the four newest months, and ticking your own months overrides it completely;
<strong>the ticker numbers are 16pt</strong> with one decimal and no longer clipped by the card;
<strong>nothing lands in a blank row any more</strong> &mdash; a material the master sheets do not
cover is labelled <em>Unassigned</em>, a plant code the sheets do not name appears as
<em>Plant 1907</em> rather than a blank slicer entry; <strong>the trial balance survives a TB Master
that does not match</strong> &mdash; if the whitelist matches nothing the report keeps every TB row
rather than showing an empty Inventory (TB); and there is a new <strong>Checks</strong> page listing
every file that was read, every sheet found in the variables workbook, the GL accounts TB Master
does not cover, and the share of rows with no nature &mdash; that page tells you which of your
source files is the problem, without guessing.</blockquote>

<blockquote><strong>Build 6 &mdash; 13 Aug:</strong> three fixes on top of build 5. Every
slicer except the two-button toggle now multi-selects on a plain click, so several months can be
ticked without holding CTRL. Every slicer also carries an <em>is not blank</em> filter, so the
empty row no longer appears in the Plant, Technology and Group Nature lists. And the material
attributes (nature, group nature, technology, BOM std qty) are now matched a second time on the
material number alone: matching on plant <em>and</em> material misses every row when the master
sheet has no valuation area column or writes the plant differently, which is what left the nature
donuts blank and every technology row empty.</blockquote>

<blockquote><strong>Build 5 &mdash; 13 Aug:</strong> the project opens and refreshes. One thing
was wrong in the generated model: the <code>Period</code> field parameter was missing the
<em>group by</em> link between its visible label and its hidden <code>NAMEOF</code> column, so every
chart and matrix drew &ldquo;By Month / By Quarter&rdquo; as two categories instead of swapping in
the months. Fixed, and the checker now tests for it. Nothing to redo by hand if you built the
parameter through <strong>Modeling &rarr; New parameter &rarr; Fields</strong> &mdash; that route
sets it correctly.</blockquote>

<blockquote><strong>Build 4 &mdash; 13 Aug:</strong> the ten measures that read the latest month
no longer use a filter <em>condition</em> at all; they use an explicit table filter
(<code>FILTER(ALL(dimDate), dimDate[MonthIndex] = LastIdx)</code>), which no engine version can
read as a measure-bearing true/false expression. The zip now extracts into a folder called
<strong>InventoryReport build 4</strong>, so an old extraction can never be confused with a new
one &mdash; if Power BI's error names a path without &ldquo;build 4&rdquo; in it, you are opening
the old copy.</blockquote>

<blockquote><strong>Fixed 13 Aug (third fix):</strong> next came
<em>&ldquo;a function placeholder has been used in a true/false expression that is used as a table
filter expression&rdquo;</em>. DAX will not let a measure be used directly as a filter condition, and
ten measures did that with <code>dimDate[MonthIndex] = [Latest Month Index]</code>. Each now reads
<code>VAR LastIdx = [Latest Month Index]</code> first and filters on <code>LastIdx</code> &mdash;
same answer, legal DAX. The ten are <code>As On Text</code>, the eight <code>Ticker &hellip;</code>
measures and <code>In Window</code>; if you pasted them by hand, re-copy those from the
<strong>Measures</strong> tab.</blockquote>

<blockquote><strong>Fixed 13 Aug (second fix):</strong> the model then failed with
<em>&ldquo;The 'MW' measure cannot be created because a column with the same name already
exists&rdquo;</em> &mdash; Power BI will not hold a column and a measure of the same name in one
table. The megawatt column in <code>factInventory</code> is now called <code>MW Qty</code>
(last step of that query renames it) and the <code>MW</code> measure reads
<code>SUM(factInventory[MW Qty])</code>. If you built the model by hand, make those two edits.
Nothing else changes &mdash; the measure is still called <code>MW</code> everywhere.</blockquote>

<blockquote><strong>Fixed 13 Aug:</strong> the first build of Route A failed with
<em>&ldquo;ReportDefinition: Required artifact is missing&rdquo;</em>. The cause was in my files, not
your Power BI &mdash; the report was written against the 2023 file-format versions, and one property
in <code>report.json</code> is no longer allowed. It is now generated at the current versions and
checked with Microsoft's own <code>powerbi-report-author</code> validator, which reports
<strong>0 errors and 0 warnings</strong> across all five pages and 55 visuals. Re-download the zip
before trying again.</blockquote>

<h3>Route A &mdash; the full report (try this first)</h3>
<ol>
<li>Open the <code>1 - full report</code> folder and double-click
<strong>Inventory Report.pbip</strong>.</li>
<li>Blank visuals and red errors at this point are expected: it has not read your files yet.</li>
<li><strong>Home</strong> &rarr; small arrow under <strong>Transform data</strong> &rarr;
<strong>Edit parameters</strong> &rarr; put your folder path in <strong>pRoot</strong>, with no
backslash on the end, e.g. <code>C:\Users\alisha\Desktop\Inventory Report</code>. Copy it from
the File Explorer address bar rather than typing it.</li>
<li><strong>Home &rarr; Refresh</strong>, wait, then <strong>Ctrl+S</strong>.</li>
<li>Overview showing numbers means you are finished. <strong>File &rarr; Save as</strong> &rarr;
<strong>Power BI files (*.pbix)</strong> if you want a single file to share.</li>
</ol>
<p class="sub">Prefer not to type the path at all? Before step 1, right-click
<strong>set-proot.ps1</strong> &rarr; <strong>Run with PowerShell</strong>, paste your folder path
when it asks, and it writes <code>pRoot</code> into both project folders for you. If Windows blocks
it, open PowerShell in the extracted folder and run:
<code>powershell -ExecutionPolicy Bypass -File .\set-proot.ps1 -Root "C:\Users\alisha\Desktop\Inventory Report"</code></p>

<h3>Route B &mdash; older Power BI (use this if A gave you an error)</h3>
<p class="sub">If Route A said <em>&ldquo;ReportDefinition: Required artifact is missing&rdquo;</em>,
that is your Power BI build refusing the new report format &mdash; nothing you ticked is wrong, and
no amount of retrying fixes it. This folder is written in the old format instead: one
<code>report.json</code>, no <code>definition</code> folder, and both the old and new semantic-model
files, so whichever your version looks for is there. No preview feature is needed for it.</p>
<ol>
<li>Open <code>2 - older power bi</code> &rarr; double-click
<strong>Inventory Report.pbip</strong>.</li>
<li>Set <code>pRoot</code> and <strong>Refresh</strong> exactly as in Route A, steps 3&ndash;4.</li>
<li>All 32 queries, 72 measures, 11 relationships and the five named pages are then in the file
with your real data behind them. The pages are blank, so draw the visuals with the
<strong>Build it</strong> tab &mdash; that part is clicking, not typing, and it is the only part
left.</li>
</ol>
<p class="sub">Why the pages are blank here and not in Route A: the old format stores each visual as
a block of hand-written query JSON, and I have no Power BI Desktop to verify it against, so
shipping guessed visuals would risk a file that opens and then shows errors on every chart. The
model &mdash; which is the part that takes hours by hand &mdash; is complete either way.</p>

<h3>Route C &mdash; model only, new format (if A errored but B also refuses)</h3>
<ol>
<li>Open <code>3 - model only</code> &rarr; double-click <strong>Inventory Report.pbip</strong>.</li>
<li>Set <code>pRoot</code> and <strong>Refresh</strong> as in Route A.</li>
<li>Same result as B: full model, blank pages.</li>
</ol>

<h3>Route D &mdash; Tabular Editor, one paste for all 72 measures</h3>
<p class="sub">Use this if you already have a working .pbix and only the measures are missing or out
of date. It cannot create the queries — Power Query is not scriptable from outside — so it pairs
with the <strong>Queries</strong> tab, not with Route A.</p>
<ol>
<li>Install <strong>Tabular Editor 2</strong> (free): <a href="https://github.com/TabularEditor/TabularEditor/releases/latest" target="_blank" rel="noopener">github.com/TabularEditor/TabularEditor/releases/latest</a>
&rarr; download <code>TabularEditor.Installer.msi</code> &rarr; run it.</li>
<li>Open your .pbix in Power BI Desktop and leave it open.</li>
<li>In Power BI Desktop: <strong>External Tools</strong> tab &rarr; <strong>Tabular Editor</strong>.
(No External Tools tab? Then Tabular Editor is not installed, or Power BI needs a restart.)</li>
<li>In Tabular Editor: the <strong>C# Script</strong> tab at the top of the big pane.</li>
<li>Open <code>3 - tabular editor\add-all-measures.csx</code> in Notepad, Ctrl+A, Ctrl+C, and paste
it into that C# Script tab.</li>
<li>Press <strong>F5</strong>. A box reports how many were created and how many updated.</li>
<li><strong>Ctrl+S</strong> in Tabular Editor, then switch back to Power BI Desktop and
<strong>Ctrl+S</strong> there too.</li>
</ol>
<p class="sub">It is safe to run twice: a measure that already exists is overwritten with the same
formula rather than duplicated.</p>

<h3>Route F &mdash; plain text, if you end up doing it by hand</h3>
<p class="sub"><code>5 - plain text</code> holds each query as its own <code>.m</code> file and each
measure as its own <code>.dax</code> file, numbered in the order they must be added, so you can open
them in Notepad and copy without hunting through a web page. Same content as the
<strong>Queries</strong> and <strong>Measures</strong> tabs.</p>

<h3>Route E &mdash; let Microsoft open it for you, in the cloud (free 60-day trial)</h3>
<p class="sub">This is the route that gets round the fact that these files were generated on Linux:
Microsoft Fabric reads the project straight out of the GitHub repo and builds the report on its own
servers, so no Power BI Desktop version can refuse it. You need no purchase &mdash; the Fabric trial
is free for 60 days and asks for no card.</p>
<ol>
<li>Go to <a href="https://app.powerbi.com" target="_blank" rel="noopener">app.powerbi.com</a> and
sign in with your work account.</li>
<li>Bottom-left, click your account name &rarr; <strong>Free trial</strong> (or
<strong>Start trial</strong>) and accept. If you see no such option, your IT admin has trials
switched off &mdash; ask them for a Fabric trial capacity.</li>
<li><strong>Workspaces</strong> &rarr; <strong>New workspace</strong>. Name it
<code>Inventory</code>. Open <strong>Advanced</strong> and set the licence mode to
<strong>Trial</strong> (or Fabric capacity). Git integration does not appear on a workspace that is
still on the free shared capacity.</li>
<li>In the workspace: <strong>Workspace settings</strong> &rarr; <strong>Git integration</strong>
&rarr; <strong>GitHub</strong>. Sign in and authorise.</li>
<li>Repository <code>audaryag/inventory-guide</code>, branch <code>main</code>, folder
<code>pbip</code>. <strong>Connect and sync</strong>.</li>
<li>Wait for the sync to finish, then open the workspace. <strong>Inventory Report</strong> is now
there as a semantic model and a report.</li>
<li>It has no data yet, because the cloud cannot see your Desktop. Two ways to fix that, pick one:
  <ul>
  <li><strong>Move the folder to OneDrive or SharePoint</strong> (recommended anyway), then in the
  workspace open the semantic model &rarr; <strong>Settings</strong> &rarr; set
  <code>pRoot</code> to the SharePoint path and refresh in the cloud.</li>
  <li><strong>Keep the folder local</strong>: install the <strong>On-premises data gateway
  (personal mode)</strong> on your laptop, then the cloud refresh reads your Desktop folder through
  it whenever your laptop is on.</li>
  </ul>
</li>
<li>Want it back as one file on your laptop? Open the report &rarr; <strong>File &rarr; Download
this file</strong>. Note Microsoft sometimes greys that out for models deployed through Git &mdash;
if it is greyed out, use the report in the browser, or fall back to Route A or B.</li>
</ol>
<p class="sub">The <code>pbip</code> folder in the repo is kept in step with this guide, so a
<strong>Sync</strong> in the workspace is all it takes to pick up any change I publish later.</p>

<h3>Honest limits</h3>
<ul>
<li>Power BI Desktop is Windows-only. Every file here was generated and checked on Linux — the
model against Microsoft's own Analysis Services object model, the report against Microsoft's
published report schemas, and every field a visual names against the model — but
<strong>none of it has ever been opened in Power BI Desktop</strong>. Your first open is the first
real test.</li>
<li>Some Power BI builds refuse the new project format whatever is ticked &mdash; that is the
<em>Required artifact is missing</em> error, and it is a version limitation, not something in these
files. Route B is written in the old format for exactly that case; Route E sidesteps versions
altogether by letting Microsoft's own servers open it.</li>
<li>Knowing your version helps me aim: <strong>Help &rarr; About</strong> in Power BI Desktop, and
send me the version line.</li>
<li>There is no way to paste all the queries at once. Power Query has no import-many box, and no
external tool can write M into a .pbix. Routes A and B get around it by shipping the queries
already inside the file, which is as close as Power BI allows.</li>
<li>The report files are now validated with Microsoft's own PBIR validator, which is the closest
thing to Desktop that runs on Linux: it checks visual types, roles, formatting property names,
theme wiring and slicer sizing. It caught 48 real problems the first time round.</li>
<li>If anything goes red, send me the exact text. Every failure so far has been one line to
fix.</li>
</ul>
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
  <button data-tab="a">Auto</button>
  <button data-tab="e">Edits ({len(EDITS)})</button>
  <button data-tab="q">Queries ({len(queries)})</button>
  <button data-tab="m">Measures ({len(measures)})</button>
  <button data-tab="n">New ({len(new_tables) + len(new_measures)})</button>
  <button data-tab="b">Build it ({len(STEPS)})</button>
  <button data-tab="g">Walkthrough</button>
  <input id="search" placeholder="Search a query name or code…">
  <button id="reset" title="Clear progress">Reset</button>
</nav>

<div class="bar" id="qbar" style="display:none"><span id="ptext"></span><span class="track"><span class="fill" id="pfill"></span></span></div>

<div class="panel on" id="tab-f">{FAST}</div>

<div class="panel" id="tab-a">{AUTO}</div>

<div class="panel" id="tab-e">
  <p class="sub">{HOWTO}</p>
  {edit_cards({q["name"]: q["code"] for q in queries})}
</div>

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

<div class="panel" id="tab-n">
  <p class="sub">Everything added in this update, and nothing else — paste these on top of the
  model you already have. <strong>Order matters:</strong> the table first, then the measures
  top to bottom.</p>
  <h2>1 &mdash; the table (report view, not Power Query)</h2>
  {cards(new_tables, 'n')}
  <h2>2 &mdash; the measures ({len(new_measures)})</h2>
  <p class="sub">Report view → <strong>Home → New measure</strong>, paste, Enter. One per box.
  They are also in the Measures tab at the bottom, so do not paste them twice.</p>
  {cards(new_measures, 'nm')}
  <h2>3 &mdash; then rebuild the Overview, Summary, FG and RM pages</h2>
  <p class="sub">Go to <strong>Build it</strong> and work through the Overview steps, then
  Summary, then FG, then RM. On each of those four pages, delete what is there first — select
  everything on the page with <strong>Ctrl+A</strong> and press <strong>Delete</strong> —
  because all four are laid out differently now.</p>
  <p class="sub"><strong>Overview:</strong> green panel down the left, chart above table, two
  donuts on the right, twelve-month strip along the bottom.</p>
  <p class="sub"><strong>Summary:</strong> no header band of cards any more. It has its own five
  controls, then one matrix with <em>Inventory (TB)</em>, <em>Inventory (MB5B)</em> and
  <em>Difference</em> as master columns and the plants opening into RM / FG / Consumables, then
  the across-all-plants block, then the difference chart. It needs the two new measures
  <code>Summary Value Rs Cr</code> and <code>In Summary Window</code> from section 2 above, so
  paste those before you start.</p>
  <p class="sub"><strong>FG:</strong> also its own five controls now (toggle, Months, Quarters,
  Plant, Technology), then two matrices with <em>MW</em>, <em>Rs Cr.</em> and <em>Days</em> as
  master columns — the first by plant, the second by technology — then three visuals across the
  bottom: MW by technology, the Days trend, and a donut of the share by plant. It needs
  <code>Unit Value by Period</code> and <code>In Latest Month</code> from section 2.</p>
  <p class="sub"><strong>RM:</strong> rebuilt from the old Excel sheet — its own five controls
  (toggle, Months, Quarters, Plant, Group Nature), a matrix of plants with <em>Rs Cr.</em> and
  <em>Days</em> as master columns, a second matrix opening Module and Cell into their materials,
  then the two charts: RM inventory in Rs Cr. by plant and in days by plant, four periods side by
  side in each. It needs <code>Days by Period</code> as well as the two FG measures.</p>
  <p class="sub">The old header band of six cards and four dropdowns is gone from every page —
  all five now carry their own controls, so there is nothing to copy and nothing to sync. If you
  built it before, select those ten visuals on each page and delete them.</p>
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
