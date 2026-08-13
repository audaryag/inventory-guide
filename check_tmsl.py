"""Catches the model errors Power BI Desktop only reports when it loads the project:
a measure sharing a name with a column in the same table, a DAX reference to something
that is not in the model, a sortByColumn that does not exist, and a relationship on a
missing column. Run it after pbip.py."""
import json
import pathlib
import re
import sys

MODEL = pathlib.Path("/home/ubuntu/pbip/Inventory Report.SemanticModel/model.bim")


def text(expr):
    return expr if isinstance(expr, str) else "".join(expr)


def main():
    model = json.loads(MODEL.read_text())["model"]
    tables = {t["name"]: t for t in model["tables"]}
    columns = {(n, c["name"]) for n, t in tables.items() for c in t.get("columns", [])}
    measures = {m["name"] for t in tables.values() for m in t.get("measures", [])}
    problems = []

    for name, t in tables.items():
        for m in t.get("measures", []):
            if (name, m["name"]) in columns:
                problems.append(f"{name}: measure '{m['name']}' collides with a column")

    def refs(expr, where):
        quoted = re.findall(r"'([^']+)'\[([^\]]+)\]", expr)
        plain = re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\[([^\]]+)\]", expr)
        for tbl, col in quoted + plain:
            if tbl in tables and (tbl, col) not in columns and col not in measures:
                problems.append(f"{where}: {tbl}[{col}] is not in the model")
        for ref in re.findall(r"(?<![A-Za-z0-9_'\]])\[([^\]]+)\]", expr):
            if ref not in measures and not any(c == ref for _, c in columns):
                problems.append(f"{where}: [{ref}] is not a measure or column")

    for name, t in tables.items():
        for m in t.get("measures", []):
            refs(text(m["expression"]), f"measure {m['name']}")
        for c in t.get("columns", []):
            sort = c.get("sortByColumn")
            if sort and (name, sort) not in columns:
                problems.append(f"{name}[{c['name']}]: sorts by missing column {sort}")
        for p in t.get("partitions", []):
            if p["source"].get("type") == "calculated":
                refs(text(p["source"]["expression"]), f"table {name}")

    for r in model["relationships"]:
        for side in ("from", "to"):
            key = (r[side + "Table"], r[side + "Column"])
            if key not in columns:
                problems.append(f"relationship: {key[0]}[{key[1]}] does not exist")

    print("TMSL PROBLEMS:", len(problems))
    for p in problems:
        print(" ", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
