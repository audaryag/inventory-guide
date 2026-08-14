#!/usr/bin/env python3
"""Checks every formatting property the generated report writes against Power BI's own
capability catalogue (the installed powerbi-report-author CLI).

A property Power BI does not know is silently ignored by Desktop, which is exactly how the
green panel came out grey and a matrix came out with no Total: the JSON was valid, the
property name was not. Run after pbip.py.
"""
import json, os, pathlib, subprocess, sys

REPORT = pathlib.Path("/home/ubuntu/pbip/Inventory Report.Report/definition/pages")
CLI = os.path.expanduser("~/.npm-global/bin/powerbi-report-author")
CACHE = {}


def describe(vt, obj):
    key = (vt, obj)
    if key not in CACHE:
        r = subprocess.run([CLI, "formatting", "describe-object", vt, obj],
                           capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
        except json.JSONDecodeError:
            d = {}
        CACHE[key] = d.get("data") if isinstance(d.get("data"), dict) else None
    return CACHE[key]


def objects_for(vt):
    if ("__list__", vt) not in CACHE:
        r = subprocess.run([CLI, "formatting", "list-objects", vt],
                           capture_output=True, text=True)
        try:
            CACHE[("__list__", vt)] = json.loads(r.stdout).get("data")
        except json.JSONDecodeError:
            CACHE[("__list__", vt)] = None
    return CACHE[("__list__", vt)]


def main():
    problems, checked = [], 0
    for f in sorted(REPORT.glob("*/visuals/*/visual.json")):
        v = json.loads(f.read_text())
        vis = v.get("visual", {})
        vt = vis.get("visualType")
        if not vt:
            continue
        cat = objects_for(vt)
        if cat:                     # the catalogue names carry a ' (selector: default)' note
            cat = {k: [n.split(" (")[0] for n in (v or [])] for k, v in cat.items()}
        where = f"{f.parent.name} ({vt})"
        for group, allowed_key in (("objects", "objects"),
                                   ("visualContainerObjects", "visualContainerObjects")):
            for obj, entries in (vis.get(group) or {}).items():
                if cat and obj not in (cat.get(allowed_key) or []):
                    problems.append(f"{where}: {group}.{obj} is not an object of {vt}")
                    continue
                spec = describe(vt, obj)
                if not spec:
                    continue
                hint = spec.get("_selectorHint")
                for e in entries:
                    if hint and "default" in hint and "selector" not in e:
                        problems.append(f"{where}: {obj} needs a default selector")
                    for p in (e.get("properties") or {}):
                        checked += 1
                        if p not in spec:
                            problems.append(f"{where}: {obj}.{p} is not a property of "
                                            f"{vt}.{obj}")
    for p in problems:
        print("  !", p)
    print(f"{checked} formatting properties checked against the capability catalogue")
    print("FORMAT PROBLEMS:", len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
