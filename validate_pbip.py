#!/usr/bin/env python3
"""Validates the generated .pbip against Microsoft's published JSON schemas."""
import json, pathlib, sys
from jsonschema import Draft7Validator, RefResolver

SCHEMAS = pathlib.Path("/tmp/jsch")
OUT = pathlib.Path("/home/ubuntu/pbip")

store = {}
for p in SCHEMAS.rglob("schema.json"):
    try:
        s = json.loads(p.read_text())
    except Exception:
        continue
    if "$id" in s:
        store[s["$id"]] = s
        store[str(p)] = s
print(f"{len(store)} schemas loaded")

errors = 0
for f in sorted(OUT.rglob("*")):
    if f.is_dir() or (f.name != ".platform"
                      and f.suffix not in (".json", ".pbip", ".pbism", ".pbir")):
        continue
    doc = json.loads(f.read_text())
    sid = doc.get("$schema")
    if sid not in store:
        print(f"SKIP (schema not found) {f.relative_to(OUT)}  {sid}")
        continue
    schema = store[sid]
    resolver = RefResolver(base_uri=sid, referrer=schema, store=store)
    v = Draft7Validator(schema, resolver=resolver)
    errs = sorted(v.iter_errors(doc), key=lambda e: list(e.path))
    if errs:
        print(f"FAIL {f.relative_to(OUT)}")
        for e in errs[:6]:
            print("   ", list(e.path), e.message[:300])
        errors += len(errs)
print("model.bim: not schema-checked here (TMSL); structure checked separately")
print("ERRORS:", errors)
sys.exit(1 if errors else 0)
