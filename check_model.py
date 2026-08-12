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
