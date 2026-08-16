#!/usr/bin/env python3
"""Builds the download zip: two project variants, a Tabular Editor script, a pRoot
setter, and the raw query/measure text. No instructions inside the zip — those live
on the Auto tab of the guide.

    python3 pbip.py            # writes /home/ubuntu/pbip        (full, 55 visuals)
    PBIP_EMPTY=1 python3 pbip.py   # writes /home/ubuntu/pbip-empty  (model only)
    python3 bundle.py          # zips both into InventoryReport-pbip.zip
"""
import json, pathlib, shutil, subprocess, sys, zipfile

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402

GUIDE = pathlib.Path("/home/ubuntu/BUILD_GUIDE.md")
STAGE = pathlib.Path("/home/ubuntu/bundle")
ZIP = HERE / "InventoryReport-pbip.zip"
# bumped on every published fix, and used as the folder name inside the zip so an old
# extraction can never be mistaken for a new one
BUILD = 26

md = GUIDE.read_text()
queries = build.parse_queries(md[md.index("# Appendix A"):md.index("# Appendix B")])
measures = build.parse_measures(md[md.index("# Appendix B"):])


def csx():
    """Tabular Editor 2 C# script: creates every measure in one paste."""
    lines = ["// Tabular Editor 2 -> C# Script tab -> paste -> F5, then Ctrl+S.",
             "// Creates or overwrites every report measure on factInventory.",
             'var t = Model.Tables["factInventory"];',
             "int made = 0, updated = 0;"]
    for m in measures:
        expr = m["code"].split("=", 1)[1].strip()
        name = m["name"].replace('"', '\\"')
        lit = '@"' + expr.replace('"', '""') + '"'
        lines += [f'if (t.Measures.Contains("{name}")) '
                  f'{{ t.Measures["{name}"].Expression = {lit}; updated++; }}',
                  f'else {{ var m = t.AddMeasure("{name}", {lit}); '
                  f'm.DisplayFolder = "Report measures"; made++; }}']
    lines += ['Info(made + " measures created, " + updated + " updated.");']
    return "\n".join(lines) + "\n"


PS1 = r'''# Sets pRoot inside an extracted project folder, so nothing is typed in Power BI.
#   Right-click this file -> Run with PowerShell, or:
#   powershell -ExecutionPolicy Bypass -File .\set-proot.ps1 -Root "C:\Users\me\Desktop\Inventory Report"
param([Parameter(Mandatory=$true)][string]$Root)

if (-not (Test-Path -LiteralPath $Root)) { throw "That folder does not exist: $Root" }
foreach ($sub in 'RM Raw','FG Raw','Consble Raw','TB') {
  if (-not (Test-Path -LiteralPath (Join-Path $Root $sub))) {
    Write-Warning "No '$sub' sub-folder inside $Root - refresh will fail until it exists."
  }
}
$Root = $Root.TrimEnd('\')
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$hits = Get-ChildItem -LiteralPath $here -Recurse -Filter model.bim
if (-not $hits) { throw "No model.bim found under $here - extract the zip first." }

foreach ($f in $hits) {
  $json = Get-Content -LiteralPath $f.FullName -Raw | ConvertFrom-Json
  $p = $json.model.expressions | Where-Object { $_.name -eq 'pRoot' }
  if (-not $p) { Write-Warning "no pRoot in $($f.FullName)"; continue }
  $esc = $Root -replace '\\', '\\'
  $p.expression = '"' + $esc + '" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'
  $json | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $f.FullName -Encoding UTF8
  Write-Host "pRoot set to $Root in $($f.Directory.Name)"
}
Write-Host "Done. Open the .pbip and press Refresh."
'''


def main():
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)

    subprocess.run([sys.executable, "pbip.py"], cwd=HERE, check=True,
                   stdout=subprocess.DEVNULL)
    shutil.copytree("/home/ubuntu/pbip", STAGE / "1 - full report")
    subprocess.run([sys.executable, "pbip.py"], cwd=HERE, check=True,
                   env={"PBIP_LEGACY": "1", "PATH": "/usr/bin:/bin"},
                   stdout=subprocess.DEVNULL)
    shutil.copytree("/home/ubuntu/pbip-legacy", STAGE / "2 - older power bi")

    subprocess.run([sys.executable, "pbip.py"], cwd=HERE, check=True,
                   env={"PBIP_EMPTY": "1", "PATH": "/usr/bin:/bin"},
                   stdout=subprocess.DEVNULL)
    shutil.copytree("/home/ubuntu/pbip-empty", STAGE / "3 - model only")

    (STAGE / "4 - tabular editor").mkdir()
    (STAGE / "4 - tabular editor" / "add-all-measures.csx").write_text(csx())

    (STAGE / "set-proot.ps1").write_text(PS1)
    shutil.copy(HERE / "inventory-theme.json", STAGE / "inventory-theme.json")

    q = STAGE / "5 - plain text" / "queries"
    m = STAGE / "5 - plain text" / "measures"
    q.mkdir(parents=True)
    m.mkdir(parents=True)
    for i, item in enumerate(queries, 1):
        (q / f"{i:02d} {item['name']}.m").write_text(item["code"] + "\n")
    for i, item in enumerate(measures, 1):
        safe = item["name"].replace("/", "-").replace("%", "pct")
        (m / f"{i:02d} {safe}.dax").write_text(item["code"] + "\n")

    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(STAGE.rglob("*")):
            if f.is_file():
                z.write(f, f"InventoryReport build {BUILD}/"
                           + f.relative_to(STAGE).as_posix())
    n = len(zipfile.ZipFile(ZIP).namelist())
    print(f"wrote build {BUILD} {ZIP} ({ZIP.stat().st_size // 1024} KB, {n} files): "
          f"{len(queries)} queries, {len(measures)} measures")


if __name__ == "__main__":
    main()
