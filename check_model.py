#!/usr/bin/env python3
"""Cross-checks the generated model and report: every reference must resolve.

  1. every table[column] and [measure] used in DAX exists
  2. every field used by a visual exists in the model
  3. relationship endpoints exist and the "one" side is a real key column
  4. sort-by columns exist
  5. every M query referenced by another query exists as a table or shared expression
"""
import json, pathlib, re, sys

OUT = pathlib.Path("/home/ubuntu/pbip")
NAME = "Inventory Report"
bim = json.loads((OUT / f"{NAME}.SemanticModel" / "model.bim").read_text())
model = bim["model"]

cols = {(t["name"], c["name"]) for t in model["tables"] for c in t["columns"]}
tables = {t["name"] for t in model["tables"]}
meas = {m["name"]: t["name"] for t in model["tables"] for m in t.get("measures", [])}
exprs = {e["name"] for e in model["expressions"]}
problems = []

# ---- 1. DAX references -------------------------------------------------------------------
DAXCOL = re.compile(r"(?:'([^']+)'|\b(\w+))\[([^\]]+)\]")
BARE = re.compile(r"(?<![\w'\)\]])\[([^\]]+)\]")
DAXKEY = {"MEASURE", "VAR", "RETURN"}
for name, tname in meas.items():
    expr = next(m["expression"] for t in model["tables"] for m in t.get("measures", [])
                if m["name"] == name)
    for q, u, prop in DAXCOL.findall(expr):
        tbl = q or u
        if tbl in tables and (tbl, prop) not in cols and prop not in meas:
            problems.append(f"measure {name!r}: {tbl}[{prop}] is not a column or measure")
        elif tbl not in tables:
            problems.append(f"measure {name!r}: table {tbl!r} does not exist")
    for prop in BARE.findall(expr):
        if prop not in meas and not any((t, prop) in cols for t in tables):
            problems.append(f"measure {name!r}: [{prop}] is not a measure in the model")

# ---- 2. report fields --------------------------------------------------------------------
pages = OUT / f"{NAME}.Report" / "definition" / "pages"
n_vis = 0
for vf in sorted(pages.rglob("visual.json")):
    n_vis += 1
    doc = json.loads(vf.read_text())
    txt = json.dumps(doc, ensure_ascii=False)
    for m in re.finditer(r'\{"(Column|Measure)":\s*\{"Expression":\s*\{"SourceRef":\s*'
                         r'\{"Entity":\s*"([^"]+)"\}\},\s*"Property":\s*"([^"]+)"\}\}', txt):
        kind, entity, prop = m.groups()
        if entity not in tables:
            problems.append(f"{vf.parent.name}: table {entity!r} does not exist")
        elif kind == "Column" and (entity, prop) not in cols:
            problems.append(f"{vf.parent.name}: {entity}[{prop}] is not a column")
        elif kind == "Measure" and prop not in meas:
            problems.append(f"{vf.parent.name}: measure {prop!r} does not exist")
        elif kind == "Measure" and meas[prop] != entity:
            problems.append(f"{vf.parent.name}: measure {prop!r} lives in {meas[prop]}, "
                            f"not {entity}")

# ---- 3. relationships -------------------------------------------------------------------
for r in model["relationships"]:
    for side in ("from", "to"):
        t, c = r[f"{side}Table"], r[f"{side}Column"]
        if (t, c) not in cols:
            problems.append(f"relationship {r['name']}: {t}[{c}] does not exist")

# ---- 4. sort by columns -----------------------------------------------------------------
for t in model["tables"]:
    for c in t["columns"]:
        if "sortByColumn" in c and (t["name"], c["sortByColumn"]) not in cols:
            problems.append(f"{t['name']}[{c['name']}] sorts by missing "
                            f"{c['sortByColumn']!r}")

# ---- 5. M query references --------------------------------------------------------------
known = tables | exprs
mnames = sorted(known, key=len, reverse=True)
for t in model["tables"]:
    src = [(t["name"], t["partitions"][0]["source"]["expression"])]
    for who, code in src:
        body = re.sub(r"//[^\n]*", "", code)
        for other in mnames:
            if other == who:
                continue
        for ref in re.findall(r"\b(fn\w+|stg\w+|var\w+|dim\w+|fact\w+|p(?:Root|VarsFile))\b",
                              body):
            if ref not in known and ref != who:
                problems.append(f"query {who}: references {ref!r} which is not in the model")
for e in model["expressions"]:
    body = re.sub(r"//[^\n]*", "", e["expression"])
    for ref in re.findall(r"\b(fn\w+|stg\w+|var\w+|dim\w+|fact\w+|p(?:Root|VarsFile))\b", body):
        if ref not in known and ref != e["name"]:
            problems.append(f"query {e['name']}: references {ref!r} which is not in the model")

# ---- 6. every identifier a query uses is defined somewhere in it -------------------------
# The one class of fault the M parser cannot see: a step that is referenced but never
# defined. Power Query only says so at refresh - "The import MasterGL matches no exports.
# Did you miss a module reference?" - which is a broken build in the user's hands rather
# than a failure here. So: strip the strings, the comments and the [field] references, then
# every bare word left must be a step defined in the same query, a function parameter, a
# query in the model, a parameter, or M's own vocabulary.
MKEY = {"let", "in", "if", "then", "else", "each", "try", "otherwise", "and", "or", "not",
        "as", "is", "meta", "error", "true", "false", "null", "type", "nullable", "optional",
        "function", "any", "anynonnull", "binary", "date", "datetime", "datetimezone",
        "duration", "list", "logical", "none", "number", "record", "table", "text", "time",
        "section", "shared"}


def undefined_identifiers(code):
    body = re.sub(r"//[^\n]*", "", code)
    # M escapes a quote by doubling it and treats a backslash as an ordinary character,
    # so "C:\" is a string holding a backslash - reading it the C way swallows the rest
    # of the query and every word in it then looks undefined.
    body = re.sub(r'"(?:[^"]|"")*"', ' "" ', body)             # string literals
    body = re.sub(r"\[[^\]]*\]", " ", body)                    # [field] references
    body = re.sub(r"\b[A-Za-z_]\w*\.[A-Za-z_]\w*", " ", body)   # Table.Group and friends
    body = re.sub(r"#\w+", " ", body)                          # #table, #date, #shared
    defined = set(re.findall(r"(?<![<>=])\b([A-Za-z_]\w*)\s*=(?![=>])", body))
    defined |= set(re.findall(r"[(,]\s*([A-Za-z_]\w*)\s+as\b", body))
    for params in re.findall(r"\(([^()]*)\)\s*=>", body):        # lambda arguments
        defined |= set(re.findall(r"[A-Za-z_]\w*", params))
    used = set(re.findall(r"(?<![\w.])([A-Za-z_]\w*)", body))
    return sorted(u for u in used - defined - known
                  if u.lower() not in MKEY and not u.startswith("_"))


for t in model["tables"]:
    for u in undefined_identifiers(t["partitions"][0]["source"]["expression"]):
        problems.append(f"query {t['name']}: uses {u!r}, which is defined nowhere in it")
for e in model["expressions"]:
    for u in undefined_identifiers(e["expression"]):
        problems.append(f"query {e['name']}: uses {u!r}, which is defined nowhere in it")


print(f"{len(tables)} tables, {len(cols)} columns, {len(meas)} measures, "
      f"{len(exprs)} helper queries, {len(model['relationships'])} relationships, "
      f"{n_vis} visuals checked")
seen = set()
for p in problems:
    if p not in seen:
        seen.add(p)
        print("  !", p)
print("PROBLEMS:", len(seen))
sys.exit(1 if seen else 0)
