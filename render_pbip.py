#!/usr/bin/env python3
"""Renders the GENERATED project to HTML, straight from the visual.json files.

Nothing here is hand-drawn: page size, every visual's type, title, x/y/width/height and
field wells are read out of /home/ubuntu/pbip. Numbers are synthetic. This is a rendering
of the project file, not a Power BI Desktop screenshot.
"""
import hashlib, html, json, math, pathlib

PBIP = pathlib.Path("/home/ubuntu/pbip/Inventory Report.Report/definition")
OUT = pathlib.Path("/home/ubuntu/pbip_preview")
GREEN, DARK, LIGHT, RED = "#4FA45F", "#1E6B3A", "#8CC63F", "#C0504D"
SERIES = ["#1E6B3A", "#4FA45F", "#8CC63F", "#2E7D6B", "#155E38", "#A7CE7A"]
MONTHS = ["Apr'26", "May'26", "Jun'26", "Jul'26"]
PLANTS = ["1900 Jaipur Module", "1902 Dholera Module", "1905 Dholera Cell"]
CATS = ["RM", "FG", "Consumables"]
NATURES = ["M10 Mono PERC", "G12R TOPCon", "M10 TOPCon", "Cell M10", "Encapsulant"]
# nature means module technology on the FG side and material family on the RM side, so a
# visual filtered to one category must not show the other's members
FG_NATURES = ["M10 Mono PERC", "G12R TOPCon", "M10 TOPCon", "M10 Bifacial", "G12 Mono PERC"]
RM_NATURES = ["Cell", "Glass", "Frame", "POE", "Wafer"]
METRICS = ["Inventory (TB)", "Inventory (MB5B)", "Difference"]
UNITS = ["MW", "In ₹ Cr", "In Days"]


def num(*key, lo=5, hi=400):
    h = int(hashlib.md5("|".join(map(str, key)).encode()).hexdigest()[:8], 16)
    return lo + (h % 1000) / 1000 * (hi - lo)


def esc(s):
    return html.escape(str(s))


def literal(o, *path):
    for p in path:
        o = o[p] if isinstance(o, dict) else o[0]
    return o


def title_of(v):
    try:
        t = v["visual"]["visualContainerObjects"]["title"][0]["properties"]["text"]
        return t["expr"]["Literal"]["Value"].strip("'").replace("''", "'")
    except Exception:
        return ""


def fields(v, role):
    q = v["visual"].get("query", {}).get("queryState", {}).get(role)
    if not q:
        return []
    out = []
    for p in q["projections"]:
        f = p["field"]
        kind = "Column" if "Column" in f else "Measure"
        out.append((f[kind]["Expression"]["SourceRef"]["Entity"],
                    f[kind]["Property"], kind))
    return out


def excluded(v, prop):
    """values this visual's own filters take out (e.g. RM tables hide MW)"""
    out = []
    for f in v.get("filterConfig", {}).get("filters", []):
        fld = f.get("field", {})
        p = (fld.get("Column") or fld.get("Measure") or {}).get("Property")
        if p != prop:
            continue
        where = f.get("filter", {}).get("Where", [{}])[0].get("Condition", {})
        node = where.get("Not", {}).get("Expression", {}).get("In")
        if node:
            out += [lit[0]["Literal"]["Value"].strip("'") for lit in node["Values"]]
    return out


def category_of(v):
    """'FG', 'RM' or None: the single category this visual is pinned to by its own filters"""
    for f in v.get("filterConfig", {}).get("filters", []):
        fld = f.get("field", {})
        if (fld.get("Column") or {}).get("Property") != "Category":
            continue
        node = f.get("filter", {}).get("Where", [{}])[0].get("Condition", {}).get("In")
        if node and len(node["Values"]) == 1:
            return node["Values"][0][0]["Literal"]["Value"].strip("'")
    return None


def kept(v, prop):
    drop = excluded(v, prop)
    keep = [x for x in values_for(prop, category_of(v)) if x not in drop]
    inc = []
    for f in v.get("filterConfig", {}).get("filters", []):
        fld = f.get("field", {})
        p = (fld.get("Column") or fld.get("Measure") or {}).get("Property")
        node = f.get("filter", {}).get("Where", [{}])[0].get("Condition", {}).get("In")
        if p == prop and node:
            inc += [lit[0]["Literal"]["Value"].strip("'") for lit in node["Values"]]
    return [x for x in keep if x in inc] if inc else keep


def values_for(prop, cat=None):
    """what a member list looks like for a given column, in the category the visual is pinned to"""
    natures = FG_NATURES if cat == "FG" else RM_NATURES if cat == "RM" else NATURES
    return {"MonthName": MONTHS, "Plant": PLANTS, "Category": CATS, "Nature": natures,
            "Metric": METRICS, "Measure": UNITS, "Quarter": ["Q1 FY 2026-27"],
            "GroupNature": ["Cells", "Glass", "Encapsulant", "Frames"],
            "Material": ["1010203", "1010311", "1010422"],
            "MaterialDesc": ["M10 cell 5BB", "Front glass 2.0mm", "EVA film 0.5mm"],
            }.get(prop, [f"{prop} {i}" for i in range(1, 4)])


def fmt(measure, x):
    if "%" in measure:
        return f"{x/100:.1%}"
    if "Days" in measure:
        return f"{x:,.1f}"
    if measure == "MW" or measure.endswith(" MW"):
        return f"{x:,.1f}"
    return f"{x:,.2f}"


# ------------------------------------------------------------------ visual renderers ------
def r_card(v):
    f = fields(v, "Values")
    if not f:
        return ""
    name = f[0][1]
    val = num("card", name, lo=2, hi=900)
    if "%" in name:
        txt, col = f"{val/1000:+.1%}", (GREEN if val > 400 else RED)
    else:
        txt, col = fmt(name, val), DARK
    return f"<div class='card'><div class='cv' style='color:{col}'>{esc(txt)}</div></div>"


def r_slicer(v):
    f = fields(v, "Values")
    lbl = f[0][1] if f else ""
    vals = kept(v, lbl)
    return (f"<div class='slicer'><span class='sl'>{esc(lbl)}</span>"
            f"<span class='sv'>{esc(vals[0])}{'  +' + str(len(vals)-1) if len(vals)>1 else ''}"
            f" <b>▾</b></span></div>")


def subtotals_on(v):
    """Whether the project asks this matrix for a Total row."""
    try:
        props = v["visual"]["objects"]["subTotals"][0]["properties"]
        return props["rowSubtotals"]["expr"]["Literal"]["Value"] == "true"
    except (KeyError, IndexError, TypeError):
        return True


def r_matrix(v):
    rows = fields(v, "Rows")
    colf = fields(v, "Columns")
    vals = fields(v, "Values")
    mname = vals[0][1] if vals else ""
    lvl1 = kept(v, rows[0][1]) if rows else ["Total"]
    lvl2 = kept(v, rows[1][1]) if len(rows) > 1 else []
    lvl3 = kept(v, rows[2][1]) if len(rows) > 2 else []
    if colf:
        outer = kept(v, colf[0][1])
        inner = kept(v, colf[1][1]) if len(colf) > 1 else [""]
    else:
        outer, inner = [m[1] for m in vals] or [""], [""]
    if len(outer) * len(inner) > 12:
        inner = inner[:4]
    h = ["<table class='mx'><thead>"]
    if colf and len(colf) > 1:
        h.append("<tr><th class='rh' rowspan='2'>" +
                 " / ".join(esc(r[1]) for r in rows) + "</th>")
        for o in outer:
            h.append(f"<th colspan='{len(inner)}' class='og'>{esc(o)}</th>")
        h.append("</tr><tr>")
        for o in outer:
            for i in inner:
                h.append(f"<th>{esc(i)}</th>")
        h.append("</tr>")
    else:
        h.append("<tr><th class='rh'>" + " / ".join(esc(r[1]) for r in rows) + "</th>")
        for o in outer:
            h.append(f"<th>{esc(o or mname)}</th>")
        h.append("</tr>")
    h.append("</thead><tbody>")

    def cells(rk):
        out = []
        for o in outer:
            for i in inner:
                mname = o if not colf else (vals[0][1] if vals else "")
                x = num(rk, o, i, mname)
                cls = ""
                if o == "Difference":
                    x = num(rk, o, i, lo=-9, hi=9)
                    cls = " neg" if abs(x) > 1 else ""
                out.append(f"<td class='n{cls}'>{esc(fmt(mname, x))}</td>")
        return "".join(out)

    for a in lvl1:
        h.append(f"<tr class='l1'><td class='rh'>{'− ' if lvl2 else ''}{esc(a)}</td>"
                 f"{cells(a)}</tr>")
        for b in lvl2:
            h.append(f"<tr class='l2'><td class='rh'>{'− ' if lvl3 else ''}{esc(b)}</td>"
                     f"{cells(a+b)}</tr>")
            for c in lvl3:
                h.append(f"<tr class='l3'><td class='rh'>{esc(c)}</td>{cells(a+b+c)}</tr>")
    if subtotals_on(v):
        h.append(f"<tr class='tot'><td class='rh'>Total</td>{cells('TOTAL')}</tr>")
    h.append("</tbody></table>")
    return f"<div class='mxwrap'>{''.join(h)}</div>"


def bars(v, stacked=False, combo=False):
    cat = fields(v, "Category")
    ys = fields(v, "Y")
    y2 = fields(v, "Y2")
    ser = fields(v, "Series")
    cats = kept(v, cat[0][1]) if cat else ["-"]
    if len(cats) > 6:
        cats = cats[:6]
    groups = [s[1] for s in ser] and kept(v, ser[0][1]) if ser else [y[1] for y in ys]
    W, H = 100, 100
    out, legend = [], []
    maxv = max(num(c, g, "bar", lo=20, hi=380) for c in cats for g in groups) * 1.15
    gw = W / max(len(cats), 1)
    for ci, c in enumerate(cats):
        base = 0.0
        n = len(groups)
        for gi, g in enumerate(groups):
            val = num(c, g, "bar", lo=20, hi=380)
            hh = val / maxv * (H - 14)
            if stacked:
                x = ci * gw + gw * .18
                w = gw * .64
                y = H - 12 - base - hh
                base += hh
            else:
                w = gw * .64 / n
                x = ci * gw + gw * .18 + gi * w
                y = H - 12 - hh
            out.append(f"<rect x='{x:.2f}' y='{y:.2f}' width='{w:.2f}' height='{hh:.2f}' "
                       f"fill='{SERIES[gi % len(SERIES)]}' rx='0.6'/>")

    if combo and y2:
        pts = []
        for ci, c in enumerate(cats):
            val = num(c, y2[0][1], "line", lo=20, hi=380)
            pts.append(f"{ci*gw+gw/2:.2f},{H-12-val/maxv*(H-14):.2f}")
        out.append(f"<polyline points='{' '.join(pts)}' fill='none' stroke='{RED}' "
                   f"stroke-width='1.1'/>")
        for p in pts:
            x, y = p.split(",")
            out.append(f"<circle cx='{x}' cy='{y}' r='1.2' fill='{RED}'/>")
        groups = groups + [y2[0][1]]
    for gi, g in enumerate(groups):
        col = RED if (combo and y2 and gi == len(groups) - 1) else SERIES[gi % len(SERIES)]
        legend.append(f"<span class='lg'><i style='background:{col}'></i>{esc(g)}</span>")
    axis = "".join(f"<span style='width:{100/len(cats):.3f}%'>{esc(c)}</span>"
                   for c in cats)
    return (f"<div class='legend'>{''.join(legend)}</div>"
            f"<svg viewBox='0 0 {W} {H-12}' preserveAspectRatio='none' class='chart'>"
            f"<g transform='translate(0,12)'>{''.join(out)}</g></svg>"
            f"<div class='axis'>{axis}</div>")


def r_pie(v, donut):
    cat = fields(v, "Category")
    ys = fields(v, "Y")
    cats = kept(v, cat[0][1])[:5] if cat else ["-"]
    mname = ys[0][1] if ys else ""
    vals = [num(c, mname, "pie", lo=10, hi=200) for c in cats]
    tot = sum(vals)
    out, ang = [], -90.0
    for i, (c, val) in enumerate(zip(cats, vals)):
        sweep = val / tot * 360
        large = 1 if sweep > 180 else 0
        a0, a1 = math.radians(ang), math.radians(ang + sweep)
        x0, y0 = 50 + 34 * math.cos(a0), 50 + 34 * math.sin(a0)
        x1, y1 = 50 + 34 * math.cos(a1), 50 + 34 * math.sin(a1)
        out.append(f"<path d='M50,50 L{x0:.2f},{y0:.2f} A34,34 0 {large} 1 {x1:.2f},{y1:.2f} Z'"
                   f" fill='{SERIES[i % len(SERIES)]}'/>")
        ang += sweep
    if donut:
        out.append("<circle cx='50' cy='50' r='17' fill='#fff'/>")
    legend = "".join(f"<span class='lg'><i style='background:{SERIES[i%len(SERIES)]}'></i>"
                     f"{esc(c)}</span>" for i, c in enumerate(cats))
    return (f"<div class='legend'>{legend}</div>"
            f"<svg viewBox='0 0 100 100' class='chart pie'>{''.join(out)}</svg>")


def r_tree(v):
    an = fields(v, "Analyze")
    ex = fields(v, "Explain")
    mname = an[0][1] if an else ""
    lvls = [("Total", fmt(mname, num("tree", mname, lo=300, hi=900)))]
    boxes = [f"<div class='tn root'><b>{esc(mname)}</b><span>{lvls[0][1]}</span></div>"]
    for e in ex[:3]:
        vals = kept(v, e[1])[:3]
        inner = "".join(
            f"<div class='tn'><b>{esc(x[:16])}</b>"
            f"<span>{esc(fmt(mname, num('tree', e[1], x, lo=20, hi=400)))}</span></div>"
            for x in vals)
        boxes.append(f"<div class='tcol'><div class='tl'>{esc(e[1])}</div>{inner}</div>")
    return f"<div class='tree'>{''.join(boxes)}</div>"


def r_line(v):
    """A plain line chart: one polyline per Y series across the category axis, with the same
    axis labels and legend the column charts use."""
    cat = fields(v, "Category")
    ys = fields(v, "Y")
    cats = kept(v, cat[0][1]) if cat else ["-"]
    if len(cats) > 12:
        cats = cats[:12]
    names = [y[1] for y in ys] or ["value"]
    W, H = 100, 100
    series = {g: [num(c, g, "line", lo=20, hi=380) for c in cats] for g in names}
    maxv = max(max(vals) for vals in series.values()) * 1.15
    gw = W / max(len(cats), 1)
    out = []
    for gi, g in enumerate(names):
        col = SERIES[gi % len(SERIES)]
        pts = [f"{ci * gw + gw / 2:.2f},{H - 12 - series[g][ci] / maxv * (H - 14):.2f}"
               for ci in range(len(cats))]
        out.append(f"<polyline points='{' '.join(pts)}' fill='none' stroke='{col}' "
                   f"stroke-width='1.2'/>")
        for pt in pts:
            x, y = pt.split(",")
            out.append(f"<circle cx='{x}' cy='{y}' r='1.1' fill='{col}'/>")
    legend = "".join(f"<span class='lg'><i style='background:{SERIES[i % len(SERIES)]}'></i>"
                     f"{esc(g)}</span>" for i, g in enumerate(names))
    axis = "".join(f"<span style='width:{100 / len(cats):.3f}%'>{esc(c)}</span>" for c in cats)
    return (f"<div class='legend'>{legend}</div>"
            f"<svg viewBox='0 0 {W} {H - 12}' preserveAspectRatio='none' class='chart'>"
            f"<g transform='translate(0,12)'>{''.join(out)}</g></svg>"
            f"<div class='axis'>{axis}</div>")


def prop(v, obj, name):
    """one formatting property off a generated visual, or None"""
    try:
        val = v["visual"]["objects"][obj][0]["properties"][name]
    except Exception:
        return None
    if isinstance(val, dict) and "solid" in val:
        val = val["solid"]["color"]
    if isinstance(val, dict) and "expr" in val:
        v = val["expr"]["Literal"]["Value"].strip("'")
        # '8D' is the number eight; '#14532D' is a colour that happens to end in D
        return v[:-1] if v.endswith("D") and not v.startswith("#") else v
    return val


def shape_div(v):
    """The green panel, the white boxes and the panel wording, drawn from the shape visual's
    own fill and text properties, so the preview shows what the project file actually says."""
    p = v["position"]
    fill = prop(v, "fill", "fillColor") if prop(v, "fill", "show") == "true" else None
    radius = prop(v, "shape", "rectangleRoundedCurve") or "0"
    text = prop(v, "text", "text") or ""
    colour = prop(v, "text", "fontColor") or "#FFFFFF"
    size = prop(v, "text", "fontSize") or "10"
    bold = "bold" if prop(v, "text", "bold") == "true" else "normal"
    border = ("border:1px dashed rgba(191,227,198,.6);"
              if prop(v, "outline", "show") == "true" else "")
    return (f"<div style='position:absolute;left:{p['x']}px;top:{p['y']}px;"
            f"width:{p['width']}px;height:{p['height']}px;border-radius:{radius}px;"
            f"background:{fill or 'transparent'};{border}display:flex;align-items:center;"
            f"padding:0 6px;font-size:{size}px;font-weight:{bold};color:{colour}'>"
            f"{esc(text)}</div>")


RENDER = {
    "card": r_card, "slicer": r_slicer, "pivotTable": r_matrix, "tableEx": r_matrix,
    "columnChart": lambda v: bars(v, stacked=True), "lineChart": r_line,
    "clusteredColumnChart": lambda v: bars(v),
    "lineClusteredColumnComboChart": lambda v: bars(v, combo=True),
    "pieChart": lambda v: r_pie(v, False), "donutChart": lambda v: r_pie(v, True),
    "decompositionTreeVisual": r_tree,
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,Helvetica,sans-serif;background:#dfe6df;color:#22302a}
.page{position:relative;width:1280px;height:720px;background:#F4F7F4;overflow:hidden}
.v{position:absolute;background:#fff;border:1px solid #DCE5DC;border-radius:4px;
   padding:4px 6px;overflow:hidden;display:flex;flex-direction:column}
.vt{font-size:11px;font-weight:bold;color:#1E6B3A;margin-bottom:2px;white-space:nowrap;
    overflow:hidden;text-overflow:ellipsis}
.vb{flex:1;min-height:0;overflow:hidden;display:flex;flex-direction:column}
.card{display:flex;flex-direction:column;justify-content:center;height:100%}
.cv{font-size:30px;font-weight:bold;line-height:1.1}
.cl{font-size:9px;color:#5A6B5F;margin-top:2px}
.slicer{display:flex;flex-direction:column;justify-content:center;height:100%;gap:2px}
.sl{font-size:9px;color:#1E6B3A;font-weight:bold}
.sv{font-size:10px;border:1px solid #DCE5DC;border-radius:3px;padding:2px 5px;
    background:#FAFCFA;display:flex;justify-content:space-between}
.mxwrap{flex:1;overflow:hidden}
table.mx{border-collapse:collapse;width:100%;font-size:9px}
table.mx th{background:#EEF3EF;color:#1E6B3A;font-weight:bold;border:1px solid #E6EDE6;
  padding:2px 4px;text-align:right;white-space:nowrap}
table.mx th.rh,table.mx td.rh{text-align:left}
table.mx th.og{background:#E2EBE3;text-align:center}
table.mx td{border:1px solid #E6EDE6;padding:2px 4px;white-space:nowrap}
table.mx td.n{text-align:right;font-variant-numeric:tabular-nums}
table.mx td.neg{color:#C0504D;font-weight:bold}
table.mx tr.l1 td{background:#fff;font-weight:bold}
table.mx tr.l2 td{background:#F7FAF7;font-weight:normal}
table.mx tr.l2 td.rh{padding-left:16px;color:#42544a}
table.mx tr.l3 td{background:#FCFDFC}
table.mx tr.l3 td.rh{padding-left:32px;color:#5A6B5F}
table.mx tr.tot td{background:#EEF3EF;font-weight:bold}
.chart{flex:1;width:100%;min-height:0}
.axis{display:flex;font-size:9px;color:#3A4A3F;padding-top:2px}
.axis span{text-align:center;overflow:hidden;white-space:nowrap}
.pie{height:100%;width:100%}
.legend{display:flex;flex-wrap:wrap;gap:6px;font-size:8px;color:#3A4A3F;margin-bottom:2px}
.legend i{display:inline-block;width:7px;height:7px;border-radius:1px;margin-right:3px}
.tree{display:flex;gap:8px;align-items:flex-start;font-size:9px;flex:1}
.tn{border:1px solid #DCE5DC;border-radius:3px;padding:3px 5px;margin-bottom:4px;
    background:#FAFCFA;display:flex;flex-direction:column;min-width:86px}
.tn.root{background:#EEF3EF}
.tn b{color:#1E6B3A;font-size:9px}
.tn span{font-variant-numeric:tabular-nums}
.tcol .tl{font-size:8px;color:#5A6B5F;margin-bottom:2px}
.tabs{display:flex;gap:4px;padding:8px 0 4px;font-size:12px}
.tabs a{padding:4px 12px;background:#fff;border:1px solid #DCE5DC;border-radius:4px 4px 0 0;
  color:#1E6B3A;text-decoration:none;font-weight:bold}
.tabs a.on{background:#1E6B3A;color:#fff}
.note{font-size:11px;color:#3A4A3F;padding:6px 0}
"""


def render_page(pdir, pages_order, names):
    page = json.loads((pdir / "page.json").read_text())
    vis = []
    for vf in sorted((pdir / "visuals").glob("*/visual.json")):
        v = json.loads(vf.read_text())
        vis.append(v)
    vis.sort(key=lambda v: v["position"].get("z", 0))
    body = []
    for v in vis:
        p = v["position"]
        vt = v["visual"]["visualType"]
        if vt == "shape":                       # furniture: paint it, no card chrome
            body.append(shape_div(v))
            continue
        inner = RENDER[vt](v) if vt in RENDER else f"<i>{esc(vt)}</i>"
        t = title_of(v)
        pad = "" if vt == "slicer" else f"<div class='vt'>{esc(t)}</div>"
        body.append(f"<div class='v' style='left:{p['x']}px;top:{p['y']}px;"
                    f"width:{p['width']}px;height:{p['height']}px'>{pad}"
                    f"<div class='vb'>{inner}</div></div>")
    tabs = "".join(
        f"<a href='{names[q]}.html' class='{'on' if q == page['displayName'] else ''}'>"
        f"{esc(q)}</a>" for q in pages_order)
    return (f"<!doctype html><meta charset='utf-8'><title>{esc(page['displayName'])}</title>"
            f"<style>{CSS}</style><body><div style='width:1280px;margin:0 auto'>"
            f"<div class='tabs'>{tabs}</div>"
            f"<div class='page'>{''.join(body)}</div>"
            f"<div class='note'>Rendered from the generated Power BI project "
            f"(page size, visual types, titles, positions and fields come from the "
            f"project file). Numbers are synthetic.</div></div></body>")


def main():
    OUT.mkdir(exist_ok=True)
    meta = json.loads((PBIP / "pages" / "pages.json").read_text())
    dirs = {d.name: d for d in (PBIP / "pages").iterdir() if d.is_dir()}
    order, names = [], {}
    for pn in meta["pageOrder"]:
        disp = json.loads((dirs[pn] / "page.json").read_text())["displayName"]
        order.append(disp)
        names[disp] = disp.lower()
    for pn in meta["pageOrder"]:
        d = dirs[pn]
        disp = json.loads((d / "page.json").read_text())["displayName"]
        (OUT / f"{names[disp]}.html").write_text(render_page(d, order, names))
    print("rendered", ", ".join(f"{OUT}/{names[p]}.html" for p in order))


if __name__ == "__main__":
    main()
