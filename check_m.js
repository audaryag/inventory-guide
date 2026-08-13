// Parses every Power Query expression in a model.bim with Microsoft's M parser. A syntax
// slip here would otherwise only surface as a red banner in Power BI Desktop on Windows.
const fs = require("fs");
const PQP = require("@microsoft/powerquery-parser");

const text = (x) => (Array.isArray(x) ? x.join("\n") : x);

(async () => {
  const model = JSON.parse(fs.readFileSync(process.argv[2], "utf8")).model;
  const items = [];
  for (const e of model.expressions || []) items.push([e.name, text(e.expression)]);
  for (const t of model.tables || [])
    for (const p of t.partitions || [])
      if (p.source && p.source.type === "m")
        items.push([`${t.name} partition`, text(p.source.expression)]);

  let bad = 0;
  for (const [name, src] of items) {
    const r = await PQP.TaskUtils.tryLexParse(PQP.DefaultSettings, src);
    if (!PQP.TaskUtils.isParseStageOk(r)) {
      bad++;
      console.log("FAIL", name, "-", r.error && r.error.message);
    }
  }
  console.log("M PARSE FAILURES:", bad, "of", items.length);
  process.exit(bad ? 1 : 0);
})();
