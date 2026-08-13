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


def split_args(expr):
    """Split a DAX argument list on the commas that sit at bracket depth zero."""
    args, depth, current, quoted = [], 0, "", False
    for ch in expr:
        if ch == '"':
            quoted = not quoted
        if not quoted:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif ch == "," and depth == 0:
                args.append(current)
                current = ""
                continue
        current += ch
    args.append(current)
    return args


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

    # a measure inside a CALCULATE/FILTER boolean predicate is what Desktop reports as
    # "a function placeholder has been used in a true/false expression"
    for name, expr in [(m["name"], text(m["expression"]))
                       for t in tables.values() for m in t.get("measures", [])]:
        for fn in ("CALCULATE", "CALCULATETABLE", "FILTER"):
            for match in re.finditer(fn + r"\s*\(", expr, re.I):
                depth, j = 1, match.end()
                while j < len(expr) and depth:
                    depth += (expr[j] == "(") - (expr[j] == ")")
                    j += 1
                for arg in split_args(expr[match.end():j - 1])[1:]:
                    if not re.search(r"\[[^\]]+\]\s*(=|<>|<=|>=|<|>)", arg):
                        continue
                    for ref in re.findall(r"(?<![A-Za-z0-9_'\]])\[([^\]]+)\]", arg):
                        if ref in measures:
                            problems.append(
                                f"measure {name}: [{ref}] is used inside a {fn} filter "
                                f"condition; assign it to a VAR first")

    # a field parameter whose label column is not grouped by the NAMEOF column loads
    # cleanly and then behaves as an ordinary two-row category in every visual
    for name, t in tables.items():
        fields = [c for c in t.get("columns", [])
                  if any(e["name"] == "ParameterMetadata"
                         for e in c.get("extendedProperties", []))]
        for field in fields:
            labels = [c for c in t.get("columns", [])
                      if [g["groupingColumn"] for g in
                          c.get("relatedColumnDetails", {}).get("groupByColumns", [])]
                      == [field["name"]]]
            if not labels:
                problems.append(f"{name}: no column is grouped by {field['name']}, so the "
                                f"field parameter will not swap fields")

    # circular references stop the model loading outright
    deps = {}
    for t in tables.values():
        for m in t.get("measures", []):
            body = text(m["expression"])
            deps[m["name"]] = {r for r in re.findall(r"(?<![A-Za-z0-9_'\]])\[([^\]]+)\]", body)
                               if r in measures and r != m["name"]}
    for start in deps:
        seen, stack = set(), [start]
        while stack:
            cur = stack.pop()
            for nxt in deps.get(cur, ()):
                if nxt == start:
                    problems.append(f"measure {start}: circular reference through {cur}")
                    stack = []
                    break
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)

    print("TMSL PROBLEMS:", len(problems))
    for p in problems:
        print(" ", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
