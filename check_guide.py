#!/usr/bin/env python3
"""Cross-checks the MANUAL build route straight out of BUILD_GUIDE.md.

Nothing here looks at the generated .pbip — it reads the guide the way a person
following it would, so a step can never name a table, column or measure that the
queries in the same guide do not produce.

  1. every query's output columns, read out of its own M code
  2. every DAX column reference resolves to one of those columns
  3. every DAX measure reference resolves to a measure defined earlier in Appendix B
  4. relationship table endpoints exist; the pair count matches the prose
  5. sort-by and hide instructions name real columns
  6. every field and measure the page steps use exists
  7. query paste order: a query only leans on queries already pasted
  8. helper-query load list names real queries
"""
import pathlib
import re
import sys

import build
import spec

GUIDE = pathlib.Path("/home/ubuntu/BUILD_GUIDE.md")
txt = GUIDE.read_text()
app_a = txt.split("# Appendix A")[1].split("# Appendix B")[0]
app_c = ""
app_b = txt.split("# Appendix B")[1]
parts = txt.split("# Appendix A")[0]

queries = build.parse_queries(app_a)
measures = build.parse_measures(app_b)
qcode = {q["name"]: q["code"] for q in queries}
qorder = [q["name"] for q in queries]
problems = []


def note(msg):
    if msg not in problems:
        problems.append(msg)


# ---- 1. what each query actually outputs -------------------------------------------------
STEP = re.compile(r"""
    (?P<typetable>\#table\(\s*type\s+table\s*\[(?P<tt>[^\]]*)\])
  | (?P<table>\#table\(\s*\{(?P<tq>[^}]*)\})
  | (?P<select>Table\.SelectColumns\(\s*(?P<selsrc>[A-Za-z_]\w*)\s*,\s*(?:\{(?P<sel>[^}]*)\}|
        (?P<selvar>[A-Za-z_]\w*)))
  | (?P<combine>Table\.Combine\(\s*\{(?P<comb>[^}]*)\})
  | (?P<add>Table\.AddColumn\(\s*[^,]+,\s*"(?P<addname>[^"]+)")
  | (?P<rename>Table\.RenameColumns\(\s*[^,]+,\s*\{(?P<ren>.*?)\}\s*\))
  | (?P<remove>Table\.RemoveColumns\(\s*[^,]+,\s*\{(?P<rem>[^}]*)\})
  | (?P<group>Table\.Group\(\s*[^,]+,\s*\{(?P<gkeys>[^}]*)\}\s*,\s*\{(?P<gaggs>.*?)\}\s*\)\s*)
  | (?P<join>Table\.NestedJoin\(\s*(?P<jsrc>[A-Za-z_]\w*)\s*,[^)]*?"(?P<jcol>[^"]+)"\s*,\s*
        JoinKind)
  | (?P<expand>Table\.ExpandTableColumn\(\s*[^,]+,\s*"(?P<xcol>[^"]+)"\s*,\s*\{(?P<xold>[^}]*)\}
        (?:\s*,\s*\{(?P<xnew>[^}]*)\})?)
  | (?P<fromlist>Table\.FromList\(\s*[^,]+,\s*[^,]+,\s*\{(?P<fl>[^}]*)\})
  | (?P<from>Table\.FromRecords)
  | (?P<src>^\s*\w+\s*=\s*(?P<srcname>[A-Za-z_]\w*)\s*,?\s*$)
""", re.S | re.X | re.M)

QUOTED = re.compile(r'"[^"]*"')


def quoted_list(s):
    return [x.strip('"') for x in re.findall(r'"[^"]*"', s or "")]


def analyse(code, known):
    """Walk the M step by step and track which columns the table has.

    Returns the final column set, or None when the source is opaque (a workbook scan,
    a folder scan, a function) and the columns cannot be known without running it.
    """
    body = re.sub(r"//[^\n]*", "", code)
    if re.search(r"\bExcel\.Workbook\b|\bFolder\.Files\b|\bCsv\.Document\b", body) and \
            "Wanted" not in body and "Table.SelectColumns" not in body:
        return None
    cols, started = [], False

    def add(c):
        if c not in cols:
            cols.append(c)

    for m in STEP.finditer(body):
        g = m.groupdict()
        if g["typetable"]:
            cols = [c.split("=")[0].strip() for c in g["tt"].split(",") if c.strip()]
            started = True
        elif g["table"]:
            cols, started = quoted_list(g["tq"]), True
        elif g["select"]:
            named = quoted_list(g["sel"]) if g["sel"] else None
            if named is None and g["selvar"]:                 # Kept = SelectColumns(x, Wanted)
                w = re.search(r"%s\s*=\s*\{(.*?)\}" % re.escape(g["selvar"]), body, re.S)
                named = quoted_list(w.group(1)) if w else None
            if named:
                cols, started = named, True
            elif g["selsrc"] in known:
                cols, started = list(known[g["selsrc"]] or []), True
        elif g["combine"]:
            cols = []
            for t in re.findall(r"[A-Za-z_]\w*", g["comb"]):
                for c in known.get(t) or []:
                    add(c)
            started = True
        elif g["fromlist"]:
            cols, started = quoted_list(g["fl"]), True
        elif g["from"]:
            return None
        elif g["src"] and not started and g["srcname"] in known:
            cols, started = list(known[g["srcname"]] or []), True
        elif g["join"]:
            if not started and g["jsrc"] in known:
                cols = list(known[g["jsrc"]] or [])
            started = True
            add(g["jcol"])
        elif not started:
            continue
        elif g["add"]:
            add(g["addname"])
        elif g["rename"]:
            for old, new in re.findall(r'"([^"]+)"\s*,\s*"([^"]+)"', g["ren"]):
                cols = [new if c == old else c for c in cols]
        elif g["remove"]:
            cols = [c for c in cols if c not in quoted_list(g["rem"])]
        elif g["group"]:
            cols = quoted_list(g["gkeys"]) + [
                a for a in re.findall(r'\{\s*"([^"]+)"', g["gaggs"])]
        elif g["expand"]:
            cols = [c for c in cols if c != g["xcol"]]
            for c in (quoted_list(g["xnew"]) or quoted_list(g["xold"])):
                add(c)
    return set(cols) if started and cols else None


COLS = {}
for q in queries:                          # guide order is dependency order
    got = analyse(q["code"], COLS)
    if got:
        COLS[q["name"]] = got

# the two lists in step 1.5 decide which queries become tables; read them, don't assume
_off = re.search(r"untick \"Enable load\"\*\*:\s*```\n(.*?)\n```", parts, re.S)
_on = re.search(r"Leave these ticked[^`]*```\n(.*?)\n```", parts, re.S)
OFF = re.findall(r"[\w]+", _off.group(1)) if _off else []
ON = re.findall(r"[\w]+", _on.group(1)) if _on else []
if not OFF or not ON:
    note("step 1.5 no longer has both Enable-load lists in code blocks")
for n in OFF + ON:
    if n not in qorder:
        note(f"step 1.5 names {n!r}, which is not a query in the guide")
for n in qorder:
    if n in OFF and n in ON:
        note(f"step 1.5 puts {n!r} in both the load-off and the load-on list")
    elif n not in OFF and n not in ON:
        note(f"step 1.5 never says whether {n!r} should load")
# tables made in report view with DAX rather than in Power Query
DAX_TABLES = {q["name"]: ["Period", "Period Fields", "Period Order"]
              for q in build.parse_queries(app_c)}
PQ_TABLES = sorted(set(ON) & set(qorder))
MODEL_TABLES = PQ_TABLES + sorted(DAX_TABLES)

# the Part 1 checkpoint must name exactly the tables that load
_chk = re.search(r"Data pane on the right must list exactly these (\d+) tables:(.*?)\n\n",
                 parts, re.S)
if _chk:
    listed = set(re.findall(r"`([\w]+)`", _chk.group(2)))
    if int(_chk.group(1)) != len(listed):
        note(f"the Part 1 checkpoint says {_chk.group(1)} tables but lists {len(listed)}")
    for miss in sorted(set(PQ_TABLES) - listed):
        note(f"the Part 1 checkpoint does not list {miss!r}, which does load")
    for extra in sorted(listed - set(PQ_TABLES)):
        note(f"the Part 1 checkpoint lists {extra!r}, which does not load")
else:
    note("Part 1 has no checkpoint naming the tables that must appear")

# counts quoted in the prose must match reality
for claim, real, what in ((re.search(r"you will repeat this (\d+) times", parts), len(qorder),
                           "queries to paste"),
                          (re.search(r"shows \*\*(\d+)\*\* names", parts), len(qorder),
                           "names in the Queries list"),
                          (re.search(r"The (\d+) helper names", parts), len(OFF),
                           "helpers with load off")):
    if claim and int(claim.group(1)) != real:
        note(f"the guide says {claim.group(1)} {what}, but there are {real}")

for t, cs in DAX_TABLES.items():
    COLS[t] = set(cs)

OPAQUE = [t for t in MODEL_TABLES if t not in COLS]

# ---- 2 + 3. measures ---------------------------------------------------------------------
mnames = [m["name"] for m in measures]
if len(mnames) != len(set(mnames)):
    dup = {n for n in mnames if mnames.count(n) > 1}
    note(f"Appendix B defines the same measure twice: {sorted(dup)}")

DAXCOL = re.compile(r"(?:'([^']+)'|\b(\w+))\[([^\]]+)\]")
BARE = re.compile(r"(?<![\w'\)\]])\[([^\]]+)\]")
defined = set()
for m in measures:
    expr = m["code"]
    for quoted, plain, prop in DAXCOL.findall(expr):
        tbl = quoted or plain
        if tbl not in COLS and tbl in MODEL_TABLES:
            continue                                   # unknown shape, already reported
        if tbl not in MODEL_TABLES:
            note(f"measure {m['name']!r}: table {tbl!r} is not a loaded table")
        elif prop not in COLS.get(tbl, set()) and prop not in mnames:
            note(f"measure {m['name']!r}: {tbl}[{prop}] is not a column of {tbl}")
    for prop in BARE.findall(expr):
        if prop == m["name"]:
            continue
        if prop not in mnames:
            note(f"measure {m['name']!r}: [{prop}] is not a measure in Appendix B")
        elif prop not in defined:
            note(f"measure order: {m['name']!r} uses [{prop}] before it is defined — "
                 f"move [{prop}] above it")
    defined.add(m["name"])

# ---- 4. relationships --------------------------------------------------------------------
rels = re.findall(r"\|\s*`(\w+)\[(\w+)\]`\s*\|\s*`(\w+)\[(\w+)\]`\s*\|", parts)
claimed = re.search(r"Create these (\d+) relationships", parts)
if claimed and int(claimed.group(1)) != len(rels):
    note(f"Part 2 says {claimed.group(1)} relationships but the table lists {len(rels)}")
for ft, fc, tt, tc in rels:
    for t, c in ((ft, fc), (tt, tc)):
        if t not in MODEL_TABLES:
            note(f"relationship {ft}[{fc}] -> {tt}[{tc}]: {t} is not a loaded table")
        elif c not in COLS.get(t, {c}):
            note(f"relationship {ft}[{fc}] -> {tt}[{tc}]: {t}[{c}] does not exist")
for dis in ("dimMetric", "dimMeasure"):
    if any(dis in r for r in rels):
        note(f"{dis} must stay disconnected but appears in the relationship table")

# ---- 5. sort-by and hide -----------------------------------------------------------------
for tbl, col, sort in re.findall(r"`(\w+)\[(\w+)\]`\s*(?:→|->)\s*`(\w+)`", parts):
    for c in (col, sort):
        if tbl in COLS and c not in COLS[tbl]:
            note(f"Part 2 sort/hide step: {tbl}[{c}] does not exist")
hide = re.search(r"\*\*2\.7\*\*(.*?)\n\n", parts, re.S)
if hide:
    for tbl, col in re.findall(r"`(\w+)\[(\w+)\]`", hide.group(1)):
        if tbl in COLS and col not in COLS[tbl]:
            note(f"Part 2.7 hide step: {tbl}[{col}] does not exist")

# ---- 6. the page steps -------------------------------------------------------------------
fields = []
for name, *_ in spec.CARDS:
    fields.append(name)
for f, *_ in spec.SLICERS:
    fields.append(f)
for page, vtype, title, wells, pos, why, fmt in spec.VISUALS:
    for well, items in wells:
        fields += items if isinstance(items, list) else [items]
fields += spec.DRILL_FIELDS

for f in fields:
    f = spec.base(f)
    f = re.split(r"→|=|is ", f)[0].strip()
    if "[" in f:
        tbl, col = f.split("[")[0], f.split("[")[1].rstrip("]")
        if tbl not in MODEL_TABLES:
            note(f"a page step drags {f} but {tbl} is not a loaded table")
        elif tbl in COLS and col not in COLS[tbl] and col not in mnames:
            note(f"a page step drags {f} but {tbl} has no column {col!r}")
    elif f not in mnames:
        note(f"a page step drags the measure {f!r} but Appendix B does not define it")

# a measure named in backticks in the page steps must exist
SLICER_VALUES = {v for t in ("dimMetric", "dimMeasure", "dimCategory")
                 for v in re.findall(r'\{"([^"]+)"', qcode.get(t, ""))}
for m in re.findall(r"`([A-Z][^`\[\]]{2,30})`", parts.split("# PART 4")[-1]):
    m = m.strip()
    if m in mnames or m in MODEL_TABLES or m in SLICER_VALUES or " " not in m:
        continue
    if ("₹ Cr" in m or m.endswith(" MW") or m.startswith("Days of")) \
            and not any(m in n or n in m for n in mnames):
        note(f"Part 4 mentions the measure {m!r} which Appendix B does not define")

# ---- 6b. two steps with the same name ----------------------------------------------------
# "Duplicate initializer named 'Attr'" stops the query dead and every query downstream of it
# with it, and nothing else in this file would have caught it: the code parses, the model
# builds, and the refresh is where it appears. Top-level steps only - a name inside a nested
# let or a record belongs to its own scope and may repeat.
for name in qcode:
    steps = re.findall(r"^ {4}([A-Za-z_]\w*)\s+=", qcode[name], re.M)
    for step in {s for s in steps if steps.count(s) > 1}:
        note(f"query {name}: two steps are both named {step!r} — Power Query stops with "
             f"\"Duplicate initializer named '{step}'\"")

# ---- 7. query paste order ----------------------------------------------------------------
seen = []
REF = re.compile(r"\b(fn\w+|stg\w+|var\w+|dim\w+|fact\w+|qc\w+|pRoot|pVarsFile)\b")
for name in qorder:
    body = QUOTED.sub('""', re.sub(r"//[^\n]*", "", qcode[name]))
    for ref in REF.findall(body):
        if ref == name:
            continue
        if ref not in qorder:
            note(f"query {name}: uses {ref!r}, which the guide never creates")
        elif ref not in seen:
            note(f"paste order: {name} (#{qorder.index(name)+1}) uses {ref} "
                 f"(#{qorder.index(ref)+1}), which comes later — swap them")
    seen.append(name)

# ---- 7b. the Power Query firewall --------------------------------------------------------
# A query that opens a data source itself (a folder, a workbook, i.e. anything reached through
# pRoot or pVarsFile) may not also read another query's table, or the refresh stops with
# "references other queries or steps, so it may not directly access a data source". Functions
# and the two path parameters do not count: they carry no data of their own.
SOURCE = re.compile(r"\bFolder\.Files\b|\bExcel\.Workbook\b|\bCsv\.Document\b")
for name in qorder:
    body = QUOTED.sub('""', re.sub(r"//[^\n]*", "", qcode[name]))
    if not SOURCE.search(body):
        continue
    for ref in set(REF.findall(body)):
        if ref in (name, "pRoot", "pVarsFile") or ref.startswith("fn"):
            continue
        if ref in qorder:
            note(f"firewall: {name} opens a data source and also reads {ref} — "
                 f"move that lookup into a query that opens nothing")

# ---- 8. the Enable-load list -------------------------------------------------------------
OLD_NAMES = ["Closing Value", "Inv RM", "Inv FG", "Inv Consumables", "TB Value",
             "Prev Month"]
for old in OLD_NAMES:
    if old in mnames:
        note(f"Part 3.7 tells the reader to delete {old!r}, but Appendix B still defines it")
for claim, real, what in ((re.search(r"there must be \*\*(\d+)\*\*", parts), len(mnames),
                           "measures"),
                          (re.search(r"# PART 3 — Add the measures", parts) and
                           re.search(r"add all (\d+) from Appendix B", parts), len(mnames),
                           "measures to add")):
    if claim and int(claim.group(1)) != real:
        note(f"the guide says {claim.group(1)} {what}, but Appendix B has {real}")

if OPAQUE:
    print("  (columns not statically knowable, so unchecked: " + ", ".join(OPAQUE) + ")")
print(f"{len(qorder)} queries, {len(MODEL_TABLES)} loaded tables, "
      f"{sum(len(v) for v in COLS.values())} declared columns, {len(mnames)} measures, "
      f"{len(rels)} relationships, {len(fields)} page field references checked")
for p in problems:
    print("  !", p)
print("GUIDE PROBLEMS:", len(problems))
sys.exit(1 if problems else 0)
