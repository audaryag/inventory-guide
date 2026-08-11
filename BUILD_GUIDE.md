# Build guide — click by click

Follow top to bottom. Don't skip ahead; each query references the ones before it.
Every code block you need is in **Appendix A** at the end of this file, under the same
name as the step that asks for it.

Rough time: Part 1–3 about 40 minutes, Part 4 (visuals) about 2 hours.

---

# PART 0 — Set up the folders (10 min)

**0.1** In OneDrive, create this exact structure:

```
Inventory Report\
    RM Raw\
    FG Raw\
    Consble Raw\
    TB\
    Variables and Calculations.xlsx
```

**0.2** Put the `Variables and Calculations.xlsx` I sent you into `Inventory Report\`
(not into a subfolder). Fill in your data rows. Don't rename sheets or headers.

**0.3** Drop your SAP MB5B exports into the three Raw folders. Never edit these files.

**0.4** Rename your TB files to `TB_202601.xlsx`, `TB_202602.xlsx`, etc. (year then month).

**0.5** Get the folder path: open `Inventory Report` in File Explorer, click the address
bar once, copy the whole path. Keep it on your clipboard — you need it in step 1.3.

**0.6** Close every Excel file in these folders. A file open in Excel makes the refresh
fail with a file-lock error. This applies every time you refresh, forever.

---

# PART 1 — Create the queries (30 min)

**1.1** Open **Power BI Desktop** → **Blank report**.

**1.2** Ribbon: **Home** → **Transform data**. The Power Query Editor window opens.
Everything in Part 1 happens in this window.

### How to add each query (you will repeat this 31 times)

1. In Power Query, ribbon: **Home** → **New Source** → **Blank Query**.
2. Ribbon: **Home** → **Advanced Editor**.
3. Select everything in the box (Ctrl+A) and delete it.
4. Paste the code block from Appendix A.
5. Click **Done**.
6. In the **Queries** list on the left, right-click the new query → **Rename** → type the
   exact name from the appendix heading (e.g. `fnCleanMB5B`). **Names must match exactly** —
   the other queries call each other by name.

> You'll see errors like "pRoot not recognised" until the query it depends on exists.
> That's expected. Ignore errors until you've created all of them.

**1.3** Create the queries in **this order**:

| # | Query name | Note |
|---|---|---|
| 1 | `pRoot` | **Paste YOUR folder path** between the quote marks |
| 2 | `pVarsFile` |  |
| 3 | `fnCleanMB5B` |  |
| 4 | `stgRM` |  |
| 5 | `stgFG` |  |
| 6 | `stgConble` |  |
| 7 | `fnVarSheet` | helper — must exist before the next four |
| 8 | `dimPlant` | hardcoded, reads no sheet |
| 9 | `dimMaterialAttr` |  |
| 10 | `dimFGAttr` |  |
| 11 | `varConstants` | needs a `RM_MW_FACTOR` = 580 row |
| 12 | `fnConstantAsOf` |  |
| 13 | `factRM` |  |
| 14 | `factFG` |  |
| 15 | `factConble` |  |
| 16 | `factInventory` |  |
| 17 | `varMWCapacity` | reads the two-block MW sheet |
| 18 | `dimCapacity` |  |
| 19 | `dimNature` |  |
| 20 | `dimTBMaster` |  |
| 21 | `factTB_Staged` |  |
| 22 | `factTB` |  |
| 23 | `factTB_Unmapped` |  |
| 24 | `dimDate` |  |
| 25 | `qcHeaders` | self-check |
| 26 | `qcVarHeaders` | self-check |
| 27 | `qcNatureNoCapacity` | self-check |
| 28 | `qcMWSheet` | self-check — shows the MW sheet raw |
| 29 | `dimCategory` | lets TB and MB5B share one RM/FG/Consumables row |
| 30 | `dimMetric` | makes Inventory (TB) / Inventory (MB5B) / Difference into columns |
| 31 | `dimMeasure` | makes MW / In ₹ Cr / In Days into columns |

**1.4** If Power BI asks about **privacy levels** or **credentials**, choose
**Organizational** for OneDrive and click through. If it warns about combining data
sources, click **Ignore Privacy Levels** (it's all your own data).

**1.5 — Important.** Turn off loading for the helper queries. For **each** of these,
right-click the query in the left list and **untick "Enable load"**:

```
pRoot, pVarsFile, fnCleanMB5B, stgRM, stgFG, stgConble,
fnVarSheet, factRM, factFG, factConble, varConstants,
fnConstantAsOf, varMWCapacity, factTB_Staged
```

Leave these ticked (they become your tables):
```
factInventory, factTB, factTB_Unmapped, dimPlant, dimDate,
dimNature, dimCapacity, dimTBMaster, dimMaterialAttr, dimFGAttr,
dimCategory, dimMetric, dimMeasure,
qcHeaders, qcVarHeaders, qcNatureNoCapacity, qcMWSheet
```

**1.6** Ribbon: **Home** → **Close & Apply**. Wait for it to load.

### If something fails here

| Error message | What it means | Fix |
|---|---|---|
| "Column 'X' of the table wasn't found" | a header in Excel doesn't match the code | fix the spelling in Excel to match the code, or tell me and I'll change the code |
| "The key didn't match any rows" | a sheet name is wrong | check sheet names: `RM Nature`, `FG Master`, `MW Capacity`, `Constants`, `TB Master`, `Plant Master` |
| "We couldn't find folder" | `pRoot` path is wrong | recheck step 0.5; no trailing backslash |
| "The file is being used by another process" | an Excel file is open | close all Excel files; check Task Manager for a stray EXCEL.EXE; delete any `~$` file |
| "Illegal characters in path" | `pRoot` is not your real path | open the folder in File Explorer, click the address bar, copy it in — keep the quote marks |
| "Token Literal expected" | a text value lost its quote marks | `pRoot` must be `"C:\...\Inventory Report"`, quotes included |
| "Not enough elements in the enumeration" | a query assumed more columns than the sheet has | you are on an old version of the query — refresh the guide page and re-copy |
| "Expression.Syntax Error" right after pasting | the whole appendix went into one query | one query per Blank Query, 31 times |

Send me the exact error text and I'll tell you the one-line fix.

---

# PART 2 — Build the model (10 min)

**2.1** Left sidebar: click the **Model** icon (third one down, looks like a table diagram).

**2.2** Power BI will have guessed some relationships. **Delete all of them**: click each
connecting line and press Delete. Cleaner to start blank.

**2.3** Create these 11 relationships. To create one: click and drag the **from** field onto
the **to** field. Then double-click the line and confirm the settings.

| From (the "one" side) | To (the "many" side) | Cardinality | Direction |
|---|---|---|---|
| `dimDate[Month]` | `factInventory[Month]` | One to many | Single |
| `dimDate[Month]` | `factTB[Month]` | One to many | Single |
| `dimDate[Month]` | `dimCapacity[Month]` | One to many | Single |
| `dimPlant[ValuationArea]` | `factInventory[ValuationArea]` | One to many | Single |
| `dimPlant[ValuationArea]` | `factTB[ValuationArea]` | One to many | Single |
| `dimPlant[ValuationArea]` | `dimCapacity[ValuationArea]` | One to many | Single |
| `dimNature[Nature]` | `factInventory[Nature]` | One to many | Single |
| `dimNature[Nature]` | `dimCapacity[Tech]` | One to many | Single |
| `dimTBMaster[GLAccount]` | `factTB[GLAccount]` | One to many | Single |
| `dimCategory[Category]` | `factInventory[Category]` | One to many | Single |
| `dimCategory[Category]` | `factTB[Category]` | One to many | Single |

The last two are what let one matrix show the trial balance and MB5B on the **same**
RM / FG / Consumables row. Without them the TB column repeats the same total against every
row, which is the classic wrong-looking reconciliation.

`dimMetric` and `dimMeasure` get **no relationship at all** — they are deliberately
disconnected. They exist to give a matrix its master columns, and the measures read them
with `SELECTEDVALUE`. If you connect them, the matrix goes blank.

Every one is **Single** direction. If Power BI offers "Both", don't take it — bidirectional
relationships cause wrong totals in ways that are very hard to spot later.

**2.4** Skip "Mark as date table" — it needs one row per *day*, and `dimDate` is monthly on
purpose. None of the measures need it; `Value ₹ Cr LM` uses `MonthIndex` instead.

**2.5** Fix month sorting: click the `MonthName` column in `dimDate` → ribbon
**Column tools** → **Sort by column** → pick `MonthSort`. Without this, months sort
alphabetically (Apr, Aug, Dec…) and every chart reads as nonsense.

**2.6** Do the same for: `dimPlant[Plant]` → `PlantSort`, `dimCategory[Category]` →
`CategorySort`, `dimMetric[Metric]` → `MetricSort`, `dimMeasure[Measure]` → `MeasureSort`.
The last two matter — without them your master columns come out alphabetically
(Difference first), which reads backwards.

**2.7** Hide the plumbing so the Fields list stays usable. Right-click → **Hide** on:
`factInventory[MatKey]`, `factTB[PlantCode]`, `dimDate[MonthSort]`, `dimPlant[PlantSort]`.

---

# PART 3 — Add the measures (15 min)

**3.1** Left sidebar: click the **Report** icon (top one).

**3.2** In the Fields pane, click `factInventory` once to select it.

**3.3** Ribbon: **Home** → **New measure**. A formula bar appears at the top.

**3.4** Delete what's there, paste **one** measure from Appendix B, press **Enter**.

**3.5** Repeat 3.3–3.4 for every measure in Appendix B. One at a time — Power BI takes one
measure per box.

**3.6** Everything money is already in **crore rupees** and named to say so
(`Value ₹ Cr`, `TB ₹ Cr`, …), so no currency symbol is needed. Click each ₹ Cr measure →
ribbon **Measure tools** → **Format: Decimal number**, **Decimal places: 2**.
For `MW`, `FG MW`, `Capacity MW`, `Days of Inventory`, use **Decimal places: 1**.
For every `%` measure use **Format: Percentage**, 1 decimal.

**3.7** If you built an earlier version of this file, the old names are gone: `Closing Value`
became `Value ₹ Cr`, `Inv RM/FG/Consumables` became `RM/FG/Consumables ₹ Cr`, `TB Value`
became `TB ₹ Cr`, `Days` became `Days of Inventory`, `Prev Month` became `Value ₹ Cr LM`.
Delete the old measures (right-click → Delete) after the new ones exist, or visuals will
still point at the old ones.

---

# PART 4 — Build the pages

Each visual is spelled out the same way: what to insert, which field goes in which
well, and the four numbers that place it on a 1280 x 720 canvas.

> Prefer one instruction at a time? Use the **Build it** tab — same content, one step per screen, with a Next button.

**To place any visual:** select it → Format pane → General → Properties →
**Size and style** → type X, Y, Width, Height.

**4.0 Canvas and theme, before anything else.**

1. Click empty canvas → Format pane → Canvas settings → Type 16:9, Height 720, Width 1280.
2. Download [inventory-theme.json](inventory-theme.json) (right-click → Save link as).
3. Ribbon **View** → **Themes** → **Browse for themes** → pick that file.

Colours, fonts, borders and card styling all come from the theme, so nothing below
asks you to colour anything.

**Create the 6 pages** with the **+** at the bottom, named: `Overview` · `Summary` · `FG` · `RM` · `Detail` · `Data Quality`.

---

## The header band — build once on Overview, then copy

**4.1** 6 **Card** visuals (**Insert → Card**), one measure each:

| Card | Measure | X | Y | Width | Height |
|---|---|---|---|---|---|
| 1 — Total value ₹ Cr | `Value ₹ Cr` | 16 | 12 | 200 | 88 |
| 2 — Raw materials ₹ Cr | `RM ₹ Cr` | 224 | 12 | 200 | 88 |
| 3 — Finished goods ₹ Cr | `FG ₹ Cr` | 432 | 12 | 200 | 88 |
| 4 — Consumables ₹ Cr | `Consumables ₹ Cr` | 640 | 12 | 200 | 88 |
| 5 — Days of inventory | `Days of Inventory` | 848 | 12 | 200 | 88 |
| 6 — Change vs last month | `Value ₹ Cr % vs LM` | 1056 | 12 | 208 | 88 |

**4.2** 3 **Slicer** visuals (**Insert → Slicer**), each set to
**Format → Slicer settings → Style: Dropdown**:

| Slicer | Field | X | Y | Width | Height |
|---|---|---|---|---|---|
| Month | `dimDate[MonthName]` | 16 | 108 | 300 | 44 |
| Plant | `dimPlant[Plant]` | 324 | 108 | 300 | 44 |
| Category | `dimCategory[Category]` | 632 | 108 | 300 | 44 |

**4.3** Select all 9 → **Ctrl+C** → **Ctrl+V** on `Summary`, `FG`, `RM`. Positions come with them.

Not on `Detail` (it is filtered by whatever you clicked to get there) or `Data Quality` (a filtered check is not a check).

**4.4** Ribbon **View** → tick **Sync slicers**; for each slicer tick **Sync** and
**Visible** on `Overview`, `Summary`, `FG`, `RM`. Without it, two
pages can disagree about the same month.

---

## Page — Overview

**4.5** **Stacked column chart** — Every month side by side, split RM / FG / consumables. Click one segment and the rest of the page follows it; right-click → Drill through → Detail for the pies behind it.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `Value ₹ Cr` |
| Legend | `dimCategory[Category]` |

Title: `Value ₹ Cr by month and category`

Position: X 16, Y 168, W 764, H 264.

**4.6** **Clustered column chart** — Three fields in the X-axis makes it a hierarchy, so the little arrows appear in the visual's top-right corner: plant, then category inside a plant, then nature inside that. Clicking is the whole point — nobody has to build three charts.

| Well | Field |
|---|---|
| X-axis | `dimPlant[Plant]`, `dimCategory[Category]`, `dimNature[Nature]` |
| Y-axis | `Value ₹ Cr` |

Title: `Value ₹ Cr by plant — click to go deeper`

Position: X 788, Y 168, W 476, H 264.

- The double-down-arrow in the header turns on drill mode; after that a single click on a bar opens the next level, and the up-arrow goes back.
- Right-click a bar → Drill through → Detail for the pie-chart page instead.

**4.7** **Line and clustered column chart** — Bars compare the two months directly; the line is the percentage swing, which is what people argue about.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Column y-axis | `Value ₹ Cr`, `Value ₹ Cr LM` |
| Line y-axis | `Value ₹ Cr % vs LM` |

Title: `Value ₹ Cr — this month vs last month`

Position: X 16, Y 444, W 764, H 268.

**4.8** **Matrix** — The same numbers as a table, because some readers only trust a table.

| Well | Field |
|---|---|
| Rows | `dimCategory[Category]` |
| Columns | `dimDate[MonthName]` |
| Values | `Value ₹ Cr` |

Title: `Months side by side`

Position: X 788, Y 444, W 476, H 268.

- Format pane → Row headers → Stepped layout: Off.
- Turn Format pane → Subtotals → Row subtotals: On, so each column has a total.

---

## Page — Summary

**4.9** **Matrix** — The whole reconciliation in one grid, exactly as it is read out: three master columns (TB, MB5B, Difference), the last four months under each, one row per plant with RM, FG and consumables beneath it, and a Total row. Everything in crore rupees.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]`, `dimCategory[Category]` |
| Columns | `dimMetric[Metric]`, `dimDate[MonthName]` |
| Values | `Summary Value ₹ Cr` |
| Filters | `Last 4 Months  →  is 1` |

Title: `Inventory (TB) · Inventory (MB5B) · Difference — ₹ Cr`

Position: X 16, Y 168, W 1248, H 300.

- Order of the two Columns fields matters: dimMetric[Metric] FIRST, then dimDate[MonthName]. That is what makes TB / MB5B / Difference the master columns with months nested inside.
- Format pane → Row headers → Stepped layout: Off (so Plant and Category get their own columns).
- Format pane → Row headers → +/- icons: On (that is the click-to-expand control).
- Format pane → Subtotals → Row subtotals On, Column subtotals Off, and set 'Per row level' so each plant shows its own total. Grand total row = the Total row.
- In the Values well, arrow next to Summary Value ₹ Cr → Conditional formatting → Background color → Format style Diverging, centre 0, both ends red: a difference either direction is equally wrong.
- Expand all plants once with the arrow at the top-left of the matrix, then save — the expansion state is remembered.

**4.10** **Clustered column chart** — The reconciliation as a picture. Click a bar and the matrix above filters to that plant; right-click → Drill through → Detail for the materials behind it.

| Well | Field |
|---|---|
| X-axis | `dimPlant[Plant]` |
| Y-axis | `Difference ₹ Cr` |

Title: `Difference ₹ Cr by plant — click a bar`

Position: X 16, Y 480, W 620, H 232.

- Format pane → Columns → Colour → fx → Format style: Rules, and colour any negative value red. A difference either direction is equally wrong.

**4.11** **Clustered column chart** — Two bars per month, books against stock report — a gap that is opening up shows here before anyone notices it in the numbers.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `TB ₹ Cr`, `Value ₹ Cr` |

Title: `Inventory (TB) vs Inventory (MB5B) by month`

Position: X 644, Y 480, W 620, H 232.

---

## Page — FG

**4.12** **Matrix** — FG per plant in all three units at once — megawatts, crore rupees and days — with the last four months under each. Days is MW ÷ capacity MW, so 1905 is blank on purpose.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]` |
| Columns | `dimMeasure[Measure]`, `dimDate[MonthName]` |
| Values | `Unit Value` |
| Filters | `dimCategory[Category]  →  is FG`, `Last 4 Months  →  is 1` |

Title: `FG by plant — MW · In ₹ Cr · In Days`

Position: X 16, Y 168, W 1248, H 176.

- dimMeasure[Measure] goes in Columns FIRST, then dimDate[MonthName].
- Format pane → Row headers → Stepped layout: Off.
- Click a plant row to filter the technology table below it.

**4.13** **Matrix** — The same three units by technology rather than by plant, which is where a build-up in one technology shows up.

| Well | Field |
|---|---|
| Rows | `dimNature[Nature]` |
| Columns | `dimMeasure[Measure]`, `dimDate[MonthName]` |
| Values | `Unit Value` |
| Filters | `dimCategory[Category]  →  is FG`, `Last 4 Months  →  is 1` |

Title: `FG by technology — MW · In ₹ Cr · In Days`

Position: X 16, Y 356, W 620, H 356.

- Same column order: dimMeasure[Measure] then dimDate[MonthName].
- Format pane → Row headers → Stepped layout: Off.

**4.14** **Clustered column chart** — Clicking one technology filters both matrices to it; right-click drills through.

| Well | Field |
|---|---|
| X-axis | `dimNature[Nature]` |
| Y-axis | `MW` |
| Filters | `dimCategory[Category]  →  is FG` |

Title: `FG MW by technology — click a bar`

Position: X 644, Y 356, W 620, H 176.

**4.15** **Line and clustered column chart** — Days month by month with the change on a line. Right-click any bar → Drill through → Detail for the technology and material split behind it.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Column y-axis | `Days` |
| Line y-axis | `Days vs LM` |
| Filters | `dimCategory[Category]  →  is FG` |

Title: `Days of inventory by month — click a bar`

Position: X 644, Y 544, W 620, H 168.

---

## Page — RM

**4.16** **Matrix** — RM by plant in crore rupees and days of cover, last four months under each. MW is unticked here because an RM megawatt figure is a derived number, not a measured one.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]` |
| Columns | `dimMeasure[Measure]`, `dimDate[MonthName]` |
| Values | `Unit Value` |
| Filters | `dimCategory[Category]  →  is RM`, `Last 4 Months  →  is 1`, `dimMeasure[Measure]  →  untick MW` |

Title: `RM by plant — In ₹ Cr · In Days`

Position: X 16, Y 168, W 1248, H 176.

- dimMeasure[Measure] in Columns first, then dimDate[MonthName].
- In the Filters pane, drag dimMeasure[Measure] in and untick MW.
- Format pane → Row headers → Stepped layout: Off.

**4.17** **Matrix** — Then the same numbers down the material hierarchy: group nature, and nature inside it. The +/- arrow on each group row is the drill-in.

| Well | Field |
|---|---|
| Rows | `factInventory[GroupNature]`, `dimNature[Nature]` |
| Columns | `dimMeasure[Measure]`, `dimDate[MonthName]` |
| Values | `Unit Value` |
| Filters | `dimCategory[Category]  →  is RM`, `Last 4 Months  →  is 1`, `dimMeasure[Measure]  →  untick MW` |

Title: `RM by group nature and nature`

Position: X 16, Y 356, W 620, H 356.

- Format pane → Row headers → Stepped layout: Off, +/- icons: On.

**4.18** **Clustered column chart** — One click sets the whole page to a group nature; right-click drills through to the materials.

| Well | Field |
|---|---|
| X-axis | `factInventory[GroupNature]` |
| Y-axis | `Value ₹ Cr` |
| Filters | `dimCategory[Category]  →  is RM` |

Title: `RM ₹ Cr by group nature — click a bar`

Position: X 644, Y 356, W 620, H 176.

**4.19** **Decomposition tree** — The interactive one: click a box and it opens the next level, in whatever order you click. This is what replaces filtering the RM sheet by hand.

| Well | Field |
|---|---|
| Analyze | `Value ₹ Cr` |
| Explain by | `dimPlant[Plant]`, `factInventory[GroupNature]`, `dimNature[Nature]`, `factInventory[Material]` |
| Filters | `dimCategory[Category]  →  is RM` |

Title: `RM — click through any way you like`

Position: X 644, Y 544, W 620, H 168.

- Click the + on a node to choose which field to split by next.

---

## Page — Detail

**4.20** **Card** — The drill-through page opens already filtered to the bar or row you came from, so this card is that one number.

| Well | Field |
|---|---|
| Fields | `Value ₹ Cr` |

Title: `Value ₹ Cr of what you clicked`

Position: X 16, Y 16, W 296, H 92.

**4.21** **Card** — Same slice in megawatts.

| Well | Field |
|---|---|
| Fields | `MW` |

Title: `MW`

Position: X 320, Y 16, W 296, H 92.

**4.22** **Card** — Stock in MW divided by the MW capacity on the Variables sheet. Blank where the plant has no capacity row — 1905.

| Well | Field |
|---|---|
| Fields | `Days of Inventory` |

Title: `Days of inventory`

Position: X 624, Y 16, W 296, H 92.

**4.23** **Card** — How big this slice is against the whole.

| Well | Field |
|---|---|
| Fields | `Share of Total %` |

Title: `Share of the total`

Position: X 928, Y 16, W 336, H 92.

**4.24** **Pie chart** — RM / FG / consumables for exactly what you clicked.

| Well | Field |
|---|---|
| Legend | `dimCategory[Category]` |
| Values | `Value ₹ Cr` |

Title: `Split by category`

Position: X 16, Y 120, W 404, H 296.

- Format pane → Detail labels → Label contents: Category, percent of total.

**4.25** **Donut chart** — Which technology or material nature the slice is made of.

| Well | Field |
|---|---|
| Legend | `dimNature[Nature]` |
| Values | `Value ₹ Cr` |

Title: `Split by technology / nature`

Position: X 428, Y 120, W 404, H 296.

- Format pane → Detail labels → Label contents: Category, percent of total.

**4.26** **Pie chart** — Where the slice sits. A single-colour pie means it is one plant already.

| Well | Field |
|---|---|
| Legend | `dimPlant[Plant]` |
| Values | `Value ₹ Cr` |

Title: `Split by plant`

Position: X 840, Y 120, W 424, H 296.

- Format pane → Detail labels → Label contents: Category, percent of total.

**4.27** **Table** — The line-item detail: the question 'which materials is that made of?' answered by clicking, instead of by another Excel sheet.

| Well | Field |
|---|---|
| Columns | `factInventory[Material]`, `factInventory[MaterialDesc]`, `Value ₹ Cr`, `MW`, `INR per Wp`, `Share of Total %` |

Title: `Materials behind this number`

Position: X 16, Y 428, W 1248, H 284.

- Click the Value ₹ Cr column header twice so it sorts largest first.

---

## Page — Data Quality

**4.28** **Card** — Materials with no row in the master sheets.

| Well | Field |
|---|---|
| Fields | `Rows Missing Attr` |

Title: `Rows missing master attributes (want 0)`

Position: X 16, Y 168, W 300, H 100.

**4.29** **Card** — Opening + receipts - issues - closing. Anything but 0 means a file is duplicated, truncated or hand-edited.

| Well | Field |
|---|---|
| Fields | `Stock Recon ₹ Cr` |

Title: `Stock reconciliation ₹ Cr (must be 0)`

Position: X 324, Y 168, W 300, H 100.

**4.30** **Table** — Catches a new GL account nobody added to TB Master — otherwise it vanishes silently.

| Well | Field |
|---|---|
| Columns | `factTB_Unmapped[GLAccount]`, `factTB_Unmapped[GLDesc]`, `Unmapped TB ₹ Cr` |

Title: `GLs in TB but not in TB Master (want empty)`

Position: X 632, Y 168, W 632, H 100.

**4.31** **Table** — Anything listed here gets blank days. This is the check that catches a Nature/Tech typo.

| Well | Field |
|---|---|
| Columns | `qcNatureNoCapacity[Nature]` |

Title: `FG technologies with no capacity row (want empty)`

Position: X 16, Y 276, W 608, H 210.

**4.32** **Table** — Read this when a column comes through blank — it shows what the file really says.

| Well | Field |
|---|---|
| Columns | `qcHeaders[Folder]`, `qcHeaders[Name]`, `qcHeaders[SheetNames]`, `qcHeaders[Headers]` |

Title: `Actual headers of every source file`

Position: X 632, Y 276, W 632, H 210.

**4.33** **Table** — DataRows = 0 means a sheet is empty.

| Well | Field |
|---|---|
| Columns | `qcVarHeaders[SheetName]`, `qcVarHeaders[Headers]`, `qcVarHeaders[DataRows]` |

Title: `Variables workbook sheets`

Position: X 16, Y 494, W 608, H 218.

**4.34** **Table** — Check after every refresh: a missing month looks like a real fall in inventory, not like an error.

| Well | Field |
|---|---|
| Columns | `factInventory[SourceFile]`, `factInventory[Month]`, `factInventory[Category]`, `Value ₹ Cr` |

Title: `Files loaded this refresh`

Position: X 632, Y 494, W 632, H 218.

---

## Making it clickable

**4.35 Drill through.** On the `Detail` page click the empty area around the visuals so
nothing is selected, then drag these into the **Drill through** well of the
Visualizations pane (leave *Keep all filters* on):

- `dimPlant[Plant]`
- `dimDate[MonthName]`
- `dimCategory[Category]`
- `dimNature[Nature]`

That is the whole trick. A **Back** arrow appears on `Detail` by itself, and every bar,
row and slice on the other pages now offers **right-click → Drill through → `Detail`**,
which opens the pies filtered to whatever was clicked.

**4.36 Interactions.** A *left*-click needs no setup — it already cross-filters the rest
of the page. To change what it does: select a visual → ribbon **Format** →
**Edit interactions**, then on each other visual pick **filter** (funnel),
**highlight** (chart) or **none**.

Worth setting deliberately: matrices to **filter** (so their totals match the click),
and the header cards to **none** (so the band always shows the company total).

---

# PART 5 — Publish and hand over

**5.1** Ribbon **Home** → **Publish** → sign in → pick or create a workspace.

- If it lets you pick a workspace, you have Power BI Pro. Good.
- If it asks you to start a trial, you don't have Pro. Ask IT to assign a licence —
  otherwise you can only email the .pbix file and it won't refresh on its own.

**5.2** In the browser at app.powerbi.com, open the workspace → find the dataset →
**Settings** → **Scheduled refresh** → turn on, set a daily time.

**5.3** Give your successor access: workspace → **Access** → add their email as
**Member** (Member, not Viewer, so they can edit after you've gone).

**5.4** Tell them the two permanent rules:
1. Close all Excel files before refreshing.
2. On `MW Capacity` and `Constants`, never overwrite a number — add a new row with the
   date it takes effect. Overwriting silently rewrites past months.

---

# Monthly routine, once it's live

1. Drop the new MB5B exports into the three Raw folders.
2. Drop the new TB in as `TB_YYYYMM.xlsx`.
3. Add any new materials to `RM Nature` / `FG Master`.
4. If capacity or a constant changed, add a **new row** with the effective date.
5. Open the .pbix → **Refresh**. Check the Data Quality page.

That's it. No formulas to drag down, no SUMIFS to extend.


---

# Appendix A — all query code

Each heading below is ONE separate query. For each: **Home → New Source → Blank Query**, then **Home → Advanced Editor**, Ctrl+A, Delete, paste the block, **Done**, then right-click the query → **Rename** and type the heading name exactly.

Do not paste this whole appendix into one editor — that is a syntax error.

Errors are normal until every query exists, because they reference each other.

## pRoot

> Replace the whole path with YOUR real folder path. Keep the quote marks. No trailing backslash. No angle brackets.

```
"C:\Data\Inventory Report"
```

## pVarsFile

```
pRoot & "\Variables and Calculations.xlsx"
```

## fnCleanMB5B

> Matches headers ignoring case, spaces and punctuation; finds the header row itself; does not require the sheet to be named Sheet1. A genuinely missing column loads as blank rather than failing the refresh - qcHeaders is how you catch that.

```
let
    fnCleanMB5B = (content as binary) as table =>
    let
        Wb        = Excel.Workbook(content, null, true),
        // take the sheet named Sheet1 if it exists, otherwise the first sheet
        Sheets    = Table.SelectRows(Wb, each [Kind] = "Sheet"),
        Picked    = try Sheets{[Item="Sheet1", Kind="Sheet"]}[Data] otherwise Sheets{0}[Data],

        // strip out fully blank leading rows, then promote whichever row is the header.
        // SAP downloads often carry a title or a blank line above the real header.
        Norm      = (n as any) as text =>
                        Text.Upper(Text.Remove(Text.Trim(Text.From(n ?? "")),
                                               {" ", ".", "_", "-", "/", "(", ")"})),
        IsHdrRow  = (row as list) as logical =>
                        List.Contains(List.Transform(row, Norm), "MATERIAL"),
        AllRows   = Table.ToRows(Picked),
        HdrIndex  = List.PositionOf(List.Transform(AllRows, IsHdrRow), true),
        Trimmed   = if HdrIndex > 0 then Table.Skip(Picked, HdrIndex) else Picked,
        Promoted  = Table.PromoteHeaders(Trimmed, [PromoteAllScalars=true]),

        // map whatever the file calls a column onto our internal name.
        // matching is done on the normalised form, so case and spacing don't matter.
        Aliases   = {
            {"VALUATIONAREA",         "ValuationArea"},
            {"VALAREA",               "ValuationArea"},
            {"PLANT",                 "ValuationArea"},
            {"MATERIAL",              "Material"},
            {"MATERIALNO",            "Material"},
            {"MATERIALDESCRIPTION",   "MaterialDesc"},
            {"MATERIALDESC",          "MaterialDesc"},
            {"FROMDATE",              "FromDate"},
            {"TODATE",                "ToDate"},
            {"OPENINGSTOCK",          "OpenQty"},
            {"OPENINGVALUE",          "OpenVal"},
            {"TOTALRECEIPTQTIES",     "ReceiptQty"},
            {"TOTALRECEIPTQTY",       "ReceiptQty"},
            {"TOTALRECEIPTQUANTITY",  "ReceiptQty"},
            {"TOTALRECEIPTQUANTITIES","ReceiptQty"},
            {"TOTALRECEIPTVALUE",     "ReceiptVal"},
            {"TOTALRECEIPTVALUES",    "ReceiptVal"},
            {"TOTALISSUEQTIES",       "IssueQty"},
            {"TOTALISSUEQTY",         "IssueQty"},
            {"TOTALISSUEQUANTITY",    "IssueQty"},
            {"TOTALISSUEQUANTITIES",  "IssueQty"},
            {"TOTALISSUEVALUE",       "IssueVal"},
            {"TOTALISSUEVALUES",      "IssueVal"},
            {"CLOSINGSTOCK",          "CloseQty"},
            {"CLOSINGVALUE",          "CloseVal"},
            {"BASICUNITOFMEASURE",    "BaseUOM"},
            {"BASEUNITOFMEASURE",     "BaseUOM"},
            {"BASEUNITMEASURE",       "BaseUOM"},
            {"BUN",                   "BaseUOM"},
            {"SPECIALSTOCK",          "SpecialStock"},
            {"CURRENCY",              "Currency"}
        },
        LookupAlias = (n as text) as nullable text =>
            let hit = List.Select(Aliases, each _{0} = Norm(n))
            in  if List.Count(hit) > 0 then hit{0}{1} else null,

        Actual    = Table.ColumnNames(Promoted),
        RenamePrs = List.RemoveNulls(List.Transform(Actual,
                        each let t = LookupAlias(_) in if t = null then null else {_, t})),
        Renamed   = Table.RenameColumns(Promoted, RenamePrs),

        Wanted    = {"ValuationArea","Material","MaterialDesc","FromDate","ToDate",
                     "OpenQty","OpenVal","ReceiptQty","ReceiptVal","IssueQty","IssueVal",
                     "CloseQty","CloseVal","BaseUOM","SpecialStock","Currency"},
        Present   = Table.ColumnNames(Renamed),
        Missing   = List.Difference(Wanted, Present),
        // any column the file genuinely doesn't have is added as blank, so one odd
        // export can't stop the whole refresh
        Padded    = List.Accumulate(Missing, Renamed,
                        (tbl, col) => Table.AddColumn(tbl, col, each null)),
        Kept      = Table.SelectColumns(Padded, Wanted),

        Keys      = Table.TransformColumns(Kept, {
                        {"ValuationArea", each Text.Trim(Text.From(_ ?? "")), type text},
                        {"Material",      each Text.TrimStart(Text.Trim(Text.From(_ ?? "")), "0"), type text},
                        {"MaterialDesc",  each Text.Trim(Text.From(_ ?? "")), type text}}),
        Typed     = Table.TransformColumnTypes(Keys, {
                        {"FromDate", type date}, {"ToDate", type date},
                        {"OpenQty", type number},   {"OpenVal", type number},
                        {"ReceiptQty", type number},{"ReceiptVal", type number},
                        {"IssueQty", type number},  {"IssueVal", type number},
                        {"CloseQty", type number},  {"CloseVal", type number},
                        {"BaseUOM", type text}, {"SpecialStock", type text},
                        {"Currency", type text}}),
        NoJunk    = Table.SelectRows(Typed, each
                        [Material] <> null and [Material] <> ""
                        and not Text.StartsWith([MaterialDesc] ?? "", "Total", Comparer.OrdinalIgnoreCase)
                        and [FromDate] <> null),
        WithMonth = Table.AddColumn(NoJunk, "Month",
                        each Date.StartOfMonth([FromDate]), type date),
        MatKey    = Table.AddColumn(WithMonth, "MatKey",
                        each [ValuationArea] & "|" & [Material], type text)
    in
        MatKey
in
    fnCleanMB5B
```

## stgRM

```
let
    Files    = Folder.Files(pRoot & "\RM Raw"),
    OnlyXlsx = Table.SelectRows(Files, each
                   Text.Lower([Extension]) = ".xlsx"
                   and not Text.StartsWith([Name], "~$")
                   and not Text.StartsWith([Name], ".")),
    Cleaned  = Table.AddColumn(OnlyXlsx, "Data", each fnCleanMB5B([Content])),
    Slim     = Table.SelectColumns(Cleaned, {"Name","Data"}),
    Expanded = Table.ExpandTableColumn(Slim, "Data",
                   {"ValuationArea","Material","MatKey","MaterialDesc","FromDate","ToDate",
                    "OpenQty","OpenVal","ReceiptQty","ReceiptVal","IssueQty","IssueVal",
                    "CloseQty","CloseVal","BaseUOM","SpecialStock","Currency","Month"}),
    Tagged   = Table.AddColumn(Expanded, "Category", each "RM", type text),
    Renamed  = Table.RenameColumns(Tagged, {{"Name","SourceFile"}})
in
    Renamed
```

## stgFG

```
let
    Files    = Folder.Files(pRoot & "\FG Raw"),
    OnlyXlsx = Table.SelectRows(Files, each
                   Text.Lower([Extension]) = ".xlsx"
                   and not Text.StartsWith([Name], "~$")
                   and not Text.StartsWith([Name], ".")),
    Cleaned  = Table.AddColumn(OnlyXlsx, "Data", each fnCleanMB5B([Content])),
    Slim     = Table.SelectColumns(Cleaned, {"Name","Data"}),
    Expanded = Table.ExpandTableColumn(Slim, "Data",
                   {"ValuationArea","Material","MatKey","MaterialDesc","FromDate","ToDate",
                    "OpenQty","OpenVal","ReceiptQty","ReceiptVal","IssueQty","IssueVal",
                    "CloseQty","CloseVal","BaseUOM","SpecialStock","Currency","Month"}),
    Tagged   = Table.AddColumn(Expanded, "Category", each "FG", type text),
    Renamed  = Table.RenameColumns(Tagged, {{"Name","SourceFile"}})
in
    Renamed
```

## stgConble

```
let
    Files    = Folder.Files(pRoot & "\Consble Raw"),
    OnlyXlsx = Table.SelectRows(Files, each
                   Text.Lower([Extension]) = ".xlsx"
                   and not Text.StartsWith([Name], "~$")
                   and not Text.StartsWith([Name], ".")),
    Cleaned  = Table.AddColumn(OnlyXlsx, "Data", each fnCleanMB5B([Content])),
    Slim     = Table.SelectColumns(Cleaned, {"Name","Data"}),
    Expanded = Table.ExpandTableColumn(Slim, "Data",
                   {"ValuationArea","Material","MatKey","MaterialDesc","FromDate","ToDate",
                    "OpenQty","OpenVal","ReceiptQty","ReceiptVal","IssueQty","IssueVal",
                    "CloseQty","CloseVal","BaseUOM","SpecialStock","Currency","Month"}),
    Tagged   = Table.AddColumn(Expanded, "Category", each "Consumables", type text),
    Renamed  = Table.RenameColumns(Tagged, {{"Name","SourceFile"}})
in
    Renamed
```

## fnVarSheet

> Shared helper. Create this BEFORE dimMaterialAttr, dimFGAttr, varConstants and dimTBMaster, which all call it.

```
let
    // Reads a sheet from Variables and Calculations by fuzzy name, promotes the header
    // row, and renames columns using an alias list. Case, spaces, dots, underscores,
    // hyphens and brackets are all ignored on both sheet names and column names.
    fnVarSheet = (sheetAliases as list, columnAliases as list) as table =>
    let
        Norm     = (n as any) as text =>
                       Text.Upper(Text.Remove(Text.Trim(Text.From(n ?? "")),
                                  {" ", ".", "_", "-", "/", "(", ")", ",", "'"})),
        Wb       = Excel.Workbook(File.Contents(pVarsFile), null, true),
        Sheets   = Table.SelectRows(Wb, each [Kind] = "Sheet"),
        WantedNm = List.Transform(sheetAliases, Norm),
        Hit      = Table.SelectRows(Sheets, each List.Contains(WantedNm, Norm([Item]))),
        Data     = if Table.RowCount(Hit) = 0
                   then error "No sheet matching: " & Text.Combine(sheetAliases, " / ")
                        & ". Sheets present: "
                        & Text.Combine(List.Transform(Sheets[Item], Text.From), " | ")
                   else Hit{0}[Data],
        Promoted = Table.PromoteHeaders(Data, [PromoteAllScalars=true]),
        Actual   = Table.ColumnNames(Promoted),
        Pairs    = List.RemoveNulls(List.Transform(Actual, (a) =>
                       let hit = List.Select(columnAliases, each List.Contains(
                                     List.Transform(_{0}, Norm), Norm(a)))
                       in  if List.Count(hit) > 0 then {a, hit{0}{1}} else null)),
        Renamed  = Table.RenameColumns(Promoted, Pairs)
    in
        Renamed
in
    fnVarSheet
```

## dimPlant

> Hardcoded on purpose: no sheet, no header to mismatch. Add a plant by adding a line.

```
let
    Src = #table(
        type table [ValuationArea = text, Plant = text, PlantSort = Int64.Type],
        {
            {"1900", "Jaipur Module",  1},
            {"1902", "Dholera Module", 2},
            {"1905", "Dholera Cell",   3}
        })
in
    Src
```

## dimMaterialAttr

```
let
    Raw      = fnVarSheet(
                   {"RM Nature", "RM Master", "RMNature"},
                   {
                     {{"Valuation Area","Val Area","Plant","Valuation area"}, "ValuationArea"},
                     {{"Material","Material No","Material Number"},           "Material"},
                     {{"Material Description","Merterial Description","Material Desc",
                       "Material description"},                              "MaterialDescVar"},
                     {{"Nature"},                                             "Nature"},
                     {{"Group Nature","GroupNature","Nature Group"},           "GroupNature"},
                     {{"BOM Std Qty","BOM StdQty","BOMStdQty","Std Qty"},      "BOMStdQty"},
                     {{"Item"},                                               "Item"}
                   }),
    Keys     = Table.TransformColumns(Raw, {
                   {"ValuationArea", each Text.Trim(Text.From(_ ?? "")), type text},
                   {"Material",      each Text.TrimStart(Text.Trim(Text.From(_ ?? "")), "0"), type text}}),
    NoBlank  = Table.SelectRows(Keys, each [Material] <> null and [Material] <> ""),
    MatKey   = Table.AddColumn(NoBlank, "MatKey",
                   each [ValuationArea] & "|" & [Material], type text),
    Typed    = Table.TransformColumnTypes(MatKey, {
                   {"Nature", type text}, {"GroupNature", type text},
                   {"BOMStdQty", type number}, {"Item", type text}}),
    Slim     = Table.SelectColumns(Typed, {"MatKey","Nature","GroupNature","BOMStdQty","Item"}),
    Dedup    = Table.Distinct(Slim, {"MatKey"}),
    Buffered = Table.Buffer(Dedup)
in
    Buffered
```

## dimFGAttr

```
let
    Raw      = fnVarSheet(
                   {"FG Master", "FM Master", "FG Nature", "FGMaster"},
                   {
                     {{"Valuation Area","Val Area","Plant","Valuation area"}, "ValuationArea"},
                     {{"Material","Material No","Material Number"},           "Material"},
                     {{"Material Description","Merterial Description","Material Desc",
                       "Material description"},                              "MaterialDescVar"},
                     {{"Nature","Tech","Technology"},                         "Nature"}
                   }),
    Keys     = Table.TransformColumns(Raw, {
                   {"ValuationArea", each Text.Trim(Text.From(_ ?? "")), type text},
                   {"Material",      each Text.TrimStart(Text.Trim(Text.From(_ ?? "")), "0"), type text},
                   {"Nature",        each Text.Trim(Text.From(_ ?? "")), type text}}),
    NoBlank  = Table.SelectRows(Keys, each [Material] <> null and [Material] <> ""),
    MatKey   = Table.AddColumn(NoBlank, "MatKey",
                   each [ValuationArea] & "|" & [Material], type text),
    Slim     = Table.SelectColumns(MatKey, {"MatKey","Nature"}),
    Dedup    = Table.Distinct(Slim, {"MatKey"}),
    Buffered = Table.Buffer(Dedup)
in
    Buffered
```

## varConstants

> Works with or without an Effective From column. Needs a row named exactly RM_MW_FACTOR (value 580) or RM MW comes out blank.

```
let
    Raw      = fnVarSheet(
                   {"Constants", "Constant", "Variables"},
                   {
                     {{"Effective From","EffectiveFrom","Effective Date","From Date","Date"}, "EffectiveFrom"},
                     {{"Constant Name","ConstantName","Name","Constant"},                    "ConstantName"},
                     {{"Value","Amount","Number"},                                           "Value"}
                   }),
    Wanted   = {"EffectiveFrom","ConstantName","Value"},
    Padded   = List.Accumulate(List.Difference(Wanted, Table.ColumnNames(Raw)), Raw,
                   (t, c) => Table.AddColumn(t, c, each null)),
    Slim     = Table.SelectColumns(Padded, Wanted),
    // no date given = applies from the beginning of time
    Filled   = Table.TransformColumns(Slim, {
                   {"EffectiveFrom", each if _ = null then #date(1900,1,1) else DateTime.Date(DateTime.From(_)), type date}}),
    Typed    = Table.TransformColumnTypes(Filled, {
                   {"ConstantName", type text}, {"Value", type number}}),
    NoBlank  = Table.SelectRows(Typed, each [ConstantName] <> null and [ConstantName] <> ""),
    Buffered = Table.Buffer(NoBlank)
in
    Buffered
```

## fnConstantAsOf

```
let
    fnConstantAsOf = (name as text, asOf as date) as nullable number =>
    let
        Rows   = Table.SelectRows(varConstants,
                     each [ConstantName] = name and [EffectiveFrom] <= asOf),
        Sorted = Table.Sort(Rows, {{"EffectiveFrom", Order.Descending}}),
        Val    = try Sorted{0}[Value] otherwise null
    in
        Val
in
    fnConstantAsOf
```

## factRM

```
let
    Src      = stgRM,
    Merged   = Table.NestedJoin(Src, {"MatKey"}, dimMaterialAttr, {"MatKey"},
                   "attr", JoinKind.LeftOuter),
    Expanded = Table.ExpandTableColumn(Merged, "attr",
                   {"Nature","GroupNature","BOMStdQty","Item"}),
    Flag     = Table.AddColumn(Expanded, "AttrMissing",
                   each [Nature] = null, type logical),
    // RM MW = Closing Stock / BOM Std Qty * RM_MW_FACTOR / 10^6
    // (the 580 you had hardcoded, now read from the Constants sheet)
    MW       = Table.AddColumn(Flag, "MW", each
                   let f = fnConstantAsOf("RM_MW_FACTOR", [Month])
                   in  try [CloseQty] / [BOMStdQty] * f / 1000000 otherwise null,
                   type number)
in
    MW
```

## factFG

```
let
    Src      = stgFG,
    Merged   = Table.NestedJoin(Src, {"MatKey"}, dimFGAttr, {"MatKey"},
                   "attr", JoinKind.LeftOuter),
    Expanded = Table.ExpandTableColumn(Merged, "attr", {"Nature"}),
    Flag     = Table.AddColumn(Expanded, "AttrMissing", each [Nature] = null, type logical),

    // Rate = RIGHT(desc,3)
    RateTxt  = Table.AddColumn(Flag, "RateText",
                   each Text.End(Text.Trim([MaterialDesc] ?? ""), 3), type text),
    Rate     = Table.AddColumn(RateTxt, "Rate",
                   each try Number.From(Text.Select([RateText], {"0".."9","."})) otherwise null,
                   type number),
    RateBad  = Table.AddColumn(Rate, "RateParseFailed",
                   each [Rate] = null, type logical),

    // Mid = MID(desc,13,13)  -- M is 0-based, so start = 12
    MidCol   = Table.AddColumn(RateBad, "Mid",
                   each try Text.Middle(Text.Trim([MaterialDesc] ?? ""), 12, 13) otherwise null,
                   type text),
    // Base = LEFT(desc,6)
    BaseCol  = Table.AddColumn(MidCol, "Base",
                   each try Text.Start(Text.Trim([MaterialDesc] ?? ""), 6) otherwise null,
                   type text),

    // MW = Closing Stock * Rate / 10^6
    MW       = Table.AddColumn(BaseCol, "MW",
                   each try [CloseQty] * [Rate] / 1000000 otherwise null, type number),

    // Inr Wp = Closing Value / (MW * 10^6)
    INRwp    = Table.AddColumn(MW, "INR_WP",
                   each try [CloseVal] / ([MW] * 1000000) otherwise null, type number),

    Cleaned  = Table.RemoveColumns(INRwp, {"RateText"})
in
    Cleaned
```

## factConble

```
stgConble
```

## factInventory

> The single table every report visual uses.

```
let
    Combined = Table.Combine({factRM, factFG, factConble})
in
    Combined
```

## varMWCapacity

> Handles either MW sheet layout and picks automatically: the long one (`Effective From | Tech | Valuation Area | MW`, one row per combination) or the original wide one (a `Tech` column with 1900/1902/1905 across the top). Headers are matched ignoring case, spaces and punctuation. A missing `Effective From` defaults to 1900-01-01, `-` becomes 0, and plant codes are forced to text so they join to `dimPlant`.

```
let
    Wb      = Excel.Workbook(File.Contents(pVarsFile), null, true),
    Sh      = Table.SelectRows(Wb, each [Kind] = "Sheet"),
    Norm    = (n as any) as text =>
                  Text.Upper(Text.Remove(Text.Trim(Text.From(n ?? "")), {" ",".","_","-","/","(",")"})),
    Hit     = Table.SelectRows(Sh, each
                  List.Contains({"MW","MWCAPACITY","CAPACITY","MWCAP"}, Norm([Item]))),
    Data    = if Table.IsEmpty(Hit)
                  then error "No sheet called MW / MW Capacity in the Variables workbook."
                  else Hit{0}[Data],
    Rows    = Table.ToRows(Data),
    Codes   = {"1900","1902","1905"},
    AsTxt   = (v as any) as text => Text.Trim(Text.From(v ?? "")),
    IsCode  = (v as any) as logical => List.Contains(Codes, AsTxt(v)),

    // ---- decide which layout this sheet is -------------------------------------------------
    // long layout is identified by an Effective From header; wide layout by a row of plant codes
    DateHdr = {"EFFECTIVEFROM","EFFECTIVEDATE","FROMDATE"},
    LongIdx = List.PositionOf(
                  List.Transform(Rows, (r) =>
                      List.AnyTrue(List.Transform(r, (c) => List.Contains(DateHdr, Norm(c))))), true),
    WideIdx = List.PositionOf(
                  List.Transform(Rows, (r) => List.Count(List.Select(r, IsCode)) >= 2), true),

    // ---- long layout: one row per Tech per plant --------------------------------------------
    Long    = let
                  Hdr   = Rows{LongIdx},
                  Find  = (alts as list) as number =>
                              let Idxs = List.Select({0..List.Count(Hdr) - 1},
                                             (i) => List.Contains(alts, Norm(Hdr{i})))
                              in  if List.IsEmpty(Idxs) then -1 else List.First(Idxs),
                  iDate = Find({"EFFECTIVEFROM","EFFECTIVEDATE","FROMDATE","DATE"}),
                  iTech = Find({"TECH","TECHNOLOGY","NATURE"}),
                  iArea = Find({"VALUATIONAREA","VALAREA","PLANT","PLANTCODE"}),
                  iMW   = Find({"MW","CAPACITYMW","CAPACITY"}),
                  Chk   = if iTech < 0 or iArea < 0 or iMW < 0
                              then error "The MW sheet has an Effective From column but I could not "
                                       & "find Tech, Valuation Area and MW next to it. Read qcMWSheet."
                              else true,
                  Body  = if Chk then List.Skip(Rows, LongIdx + 1) else {},
                  Keep  = List.Select(Body, (r) =>
                              AsTxt(r{iTech}) <> "" and AsTxt(r{iArea}) <> ""),
                  Recs  = List.Transform(Keep, (r) =>
                              [ EffectiveFrom = (if iDate < 0 then #date(1900,1,1)
                                                 else try DateTime.Date(DateTime.From(r{iDate}))
                                                      otherwise #date(1900,1,1)),
                                Tech          = AsTxt(r{iTech}),
                                ValuationArea = AsTxt(r{iArea}),
                                MW            = (try Number.From(r{iMW}) otherwise 0) ])
              in  Recs,

    // ---- wide layout: plant codes across the top --------------------------------------------
    Wide    = let
                  Hdr   = Rows{WideIdx},
                  Map   = List.Select(
                              List.Transform({0..List.Count(Hdr) - 1},
                                  (i) => [Idx = i, Code = AsTxt(Hdr{i})]),
                              (m) => List.Contains(Codes, m[Code])),
                  Body  = List.Skip(Rows, WideIdx + 1),
                  Keep  = List.Select(Body, (r) =>
                              AsTxt(List.First(r)) <> "" and not IsCode(List.First(r))
                              and List.AnyTrue(List.Transform(Map,
                                  (m) => (try r{m[Idx]} otherwise null) <> null))),
                  Recs  = List.TransformMany(Keep, (r) => Map, (r, m) =>
                              [ EffectiveFrom = #date(1900,1,1),
                                Tech          = AsTxt(List.First(r)),
                                ValuationArea = m[Code],
                                MW            = (try Number.From(r{m[Idx]}) otherwise 0) ])
              in  Recs,

    Pairs   = if LongIdx >= 0 then Long
              else if WideIdx >= 0 then Wide
              else error "The MW sheet is neither layout I recognise: no Effective From/Tech header "
                       & "row, and no row containing two of 1900/1902/1905. Read qcMWSheet.",
    T       = Table.FromRecords(Pairs,
                  type table [EffectiveFrom = date, Tech = text, ValuationArea = text, MW = number]),
    Out     = Table.Buffer(T)
in
    Out
```


## dimCapacity

```
let
    Months   = List.Distinct(List.Sort(factInventory[Month])),
    Combos   = Table.Distinct(Table.SelectColumns(varMWCapacity, {"Tech","ValuationArea"})),
    Grid     = Table.AddColumn(Combos, "Month", each Months),
    Expanded = Table.ExpandListColumn(Grid, "Month"),
    AsOf     = Table.AddColumn(Expanded, "CapacityMW", (row) =>
                   let
                       Rows   = Table.SelectRows(varMWCapacity, each
                                    [Tech] = row[Tech]
                                    and [ValuationArea] = row[ValuationArea]
                                    and [EffectiveFrom] <= row[Month]),
                       Sorted = Table.Sort(Rows, {{"EffectiveFrom", Order.Descending}}),
                       Val    = try Sorted{0}[MW] otherwise null
                   in  Val, type number),
    Typed    = Table.TransformColumnTypes(AsOf, {{"Month", type date}})
in
    Typed
```

## dimNature

> Bridge table. Without it, slicing FG by Nature leaves Capacity MW unfiltered and Days is wrong everywhere except the grand total.

```
let
    FromRM  = List.RemoveNulls(dimMaterialAttr[Nature]),
    FromFG  = List.RemoveNulls(dimFGAttr[Nature]),
    FromCap = List.RemoveNulls(varMWCapacity[Tech]),
    All     = List.Distinct(List.Combine({FromRM, FromFG, FromCap})),
    T       = Table.FromList(All, Splitter.SplitByNothing(), {"Nature"}),
    Typed   = Table.TransformColumnTypes(T, {{"Nature", type text}})
in
    Typed
```

## dimTBMaster

```
let
    Raw      = fnVarSheet(
                   {"TB Master", "TBMaster", "TB"},
                   {
                     {{"GL Account Number","gl Account Number","GLAccountNumber",
                       "GL Account","G/L Account","GL No"},                    "GLAccount"},
                     {{"GL Account Description","GL Description","GLDescription",
                       "Account Description","Account Name"},                  "GLDescMaster"},
                     {{"Nature"},                                             "Nature"},
                     {{"Plant","Valuation Area"},                             "TBPlant"},
                     {{"Sort Order","SortOrder","Sort"},                       "TBSort"}
                   }),
    Keys     = Table.TransformColumns(Raw, {
                   {"GLAccount", each Text.TrimStart(Text.Trim(Text.From(_ ?? "")), "0"), type text}}),
    NoBlank  = Table.SelectRows(Keys, each [GLAccount] <> null and [GLAccount] <> ""),
    Wanted   = {"GLAccount","GLDescMaster","Nature","TBPlant","TBSort"},
    Present  = Table.ColumnNames(NoBlank),
    Padded   = List.Accumulate(List.Difference(Wanted, Present), NoBlank,
                   (t, c) => Table.AddColumn(t, c, each null)),
    Slim     = Table.SelectColumns(Padded, Wanted),
    Typed    = Table.TransformColumnTypes(Slim, {
                   {"Nature", type text}, {"TBPlant", type text}}),
    Dedup    = Table.Distinct(Typed, {"GLAccount"})
in
    Dedup
```

## factTB_Staged

> Header-tolerant: sheet names, header position, case, spaces and punctuation are all matched loosely, and the common SAP spellings (`gl Account Number`, `Profit Center`, `Amount in local currency`, …) are recognised. A column it genuinely cannot find comes through blank rather than failing the refresh. Month comes from the file name, so files must be `TB_YYYYMM.xlsx`.

```
let
    Norm     = (n as any) as text =>
                   Text.Upper(Text.Remove(Text.Trim(Text.From(n ?? "")), {" ",".","_","-","/","(",")"})),
    GLNames  = {"GLACCOUNTNUMBER","GLACCOUNT","GLACCOUNTNO","GLACCNO","ACCOUNTNUMBER","GLCODE"},
    Alias    = {
                   {GLNames, "GLAccount"},
                   {{"GLACCOUNTDESCRIPTION","GLACCOUNTDESC","ACCOUNTDESCRIPTION",
                     "GLDESCRIPTION","GLDESC","ACCOUNTNAME"}, "GLDesc"},
                   {{"PROFITCENTRE","PROFITCENTER","PROFITCTR","PRCTR"}, "ProfitCentre"},
                   {{"PROFITCENTREDESCRIPTION","PROFITCENTERDESCRIPTION",
                     "PROFITCENTREDESC","PROFITCENTERDESC"}, "ProfitCentreDesc"},
                   {{"AMOUNT","AMOUNTINLOCALCURRENCY","AMOUNTINLC","AMTINLOCCUR",
                     "BALANCE","CLOSINGBALANCE"}, "Amount"}
               },
    Wanted   = {"GLAccount","GLDesc","ProfitCentre","ProfitCentreDesc","Amount"},

    Clean    = (content as binary) as table =>
                   let
                       Wb       = Excel.Workbook(content, null, true),
                       Sheets   = Table.SelectRows(Wb, each [Kind] = "Sheet"),
                       Picked   = try Sheets{[Item = "Sheet1", Kind = "Sheet"]}[Data]
                                  otherwise Sheets{0}[Data],
                       // find the header row: the one holding a GL-account-ish cell
                       RowsL    = Table.ToRows(Picked),
                       HdrIdx   = List.PositionOf(
                                      List.Transform(RowsL, (r) =>
                                          List.AnyTrue(List.Transform(r,
                                              (c) => List.Contains(GLNames, Norm(c))))), true),
                       Skipped  = if HdrIdx <= 0 then Picked else Table.Skip(Picked, HdrIdx),
                       Promoted = Table.PromoteHeaders(Skipped, [PromoteAllScalars = true]),

                       Lookup   = (c as any) as nullable text =>
                                      let Hits = List.Select(Alias, (a) => List.Contains(a{0}, Norm(c)))
                                      in  if List.IsEmpty(Hits) then null else Hits{0}{1},
                       Pairs    = List.RemoveNulls(
                                      List.Transform(Table.ColumnNames(Promoted),
                                          (c) => let t = Lookup(c) in if t = null then null else {c, t})),
                       // if two source columns map to the same name, keep the first
                       Renames  = List.Accumulate(Pairs, {}, (acc, pr) =>
                                      if List.Contains(List.Transform(acc, (x) => x{1}), pr{1})
                                      then acc else acc & {pr}),
                       Renamed  = Table.RenameColumns(Promoted, Renames),
                       Padded   = List.Accumulate(
                                      List.Difference(Wanted, Table.ColumnNames(Renamed)), Renamed,
                                      (tbl, col) => Table.AddColumn(tbl, col, each null)),
                       Kept     = Table.SelectColumns(Padded, Wanted),
                       NoJunk   = Table.SelectRows(Kept, each
                                      [GLAccount] <> null
                                      and Text.Trim(Text.From([GLAccount])) <> ""
                                      and not Text.StartsWith(Text.From([GLAccount]), "Total",
                                              Comparer.OrdinalIgnoreCase))
                   in
                       NoJunk,

    Files    = Folder.Files(pRoot & "\TB"),
    OnlyXlsx = Table.SelectRows(Files, each
                   Text.StartsWith(Text.Lower([Extension]), ".xls")
                   and not Text.StartsWith([Name], "~$")
                   and not Text.StartsWith([Name], ".")),
    Loaded   = Table.AddColumn(OnlyXlsx, "Data", each Clean([Content])),

    // month from the file name: TB_YYYYMM.xlsx
    WithMonth = Table.AddColumn(Loaded, "Month", each
                   let
                       digits = Text.Select([Name], {"0".."9"}),
                       yyyymm = Text.Middle(digits, 0, 6)
                   in
                       try #date(Number.From(Text.Start(yyyymm, 4)),
                                 Number.From(Text.Middle(yyyymm, 4, 2)), 1)
                       otherwise null, type date),
    Slim     = Table.SelectColumns(WithMonth, {"Name","Month","Data"}),
    Expanded = Table.ExpandTableColumn(Slim, "Data", Wanted),
    Renamed  = Table.RenameColumns(Expanded, {{"Name","SourceFile"}}),
    Keys     = Table.TransformColumns(Renamed, {
                   {"GLAccount",    each Text.TrimStart(Text.Trim(Text.From(_ ?? "")), "0"), type text},
                   {"ProfitCentre", each Text.Trim(Text.From(_ ?? "")), type text}}),
    // plant = characters 3-6 of the profit centre  (0-based start = 2)
    PlantRaw = Table.AddColumn(Keys, "PlantCode",
                   each try Text.Middle([ProfitCentre], 2, 4) otherwise null, type text),
    Known    = List.Buffer(dimPlant[ValuationArea]),
    PlantCol = Table.AddColumn(PlantRaw, "ValuationArea",
                   each if List.Contains(Known, [PlantCode]) then [PlantCode] else "Unallocated",
                   type text),
    Typed    = Table.TransformColumnTypes(PlantCol, {{"Amount", type number}})
in
    Typed
```


## factTB

> The inner join to dimTBMaster IS the trial-balance cleaning - only whitelisted GL accounts survive. `Category` is worked out from the Nature text on TB Master, so the trial balance and MB5B can be compared on the same RM / FG / Consumables row.

```
let
    Mapped  = Table.NestedJoin(factTB_Staged, {"GLAccount"}, dimTBMaster, {"GLAccount"},
                  "tpl", JoinKind.Inner),
    Expand  = Table.ExpandTableColumn(Mapped, "tpl", {"Nature","TBPlant","TBSort"}),
    // RM / FG / Consumables from whatever the Nature (or GL description) says
    Bucket  = (n as any, d as any) as text =>
                  let T = Text.Upper(Text.From(n ?? "") & " " & Text.From(d ?? "")) in
                  if Text.Contains(T, "FINISH") or Text.Contains(T, "FG")
                      then "FG"
                  else if Text.Contains(T, "CONSUM") or Text.Contains(T, "STORE")
                      or Text.Contains(T, "SPARE") or Text.Contains(T, "PACK")
                      then "Consumables"
                  else if Text.Contains(T, "RAW") or Text.Contains(T, "RM")
                      or Text.Contains(T, "WIP") or Text.Contains(T, "SEMI")
                      then "RM"
                  else "RM",
    Cat     = Table.AddColumn(Expand, "Category",
                  each Bucket([Nature], [GLDesc]), type text)
in
    Cat
```

## factTB_Unmapped

> GL accounts present in the raw TB but absent from TB Master. Empty = good. This is what stops a new GL silently vanishing.

```
let
    Anti  = Table.NestedJoin(factTB_Staged, {"GLAccount"}, dimTBMaster, {"GLAccount"},
                "tpl", JoinKind.LeftAnti),
    Clean = Table.RemoveColumns(Anti, {"tpl"}),
    Group = Table.Group(Clean, {"GLAccount","GLDesc"},
                {{"Amount", each List.Sum([Amount]), type number},
                 {"Rows",   each Table.RowCount(_), Int64.Type}})
in
    Group
```

## dimDate

> One row per month, because every fact is monthly. A daily calendar would repeat each Month value ~30 times and Power BI would refuse to put it on the "one" side of the relationship.

```
let
    MinD   = Date.StartOfMonth(List.Min(factInventory[Month])),
    MaxD   = Date.StartOfMonth(List.Max(factInventory[Month])),
    Start  = #date(Date.Year(MinD) - (if Date.Month(MinD) < 4 then 1 else 0), 4, 1),
    Count  = (Date.Year(MaxD) * 12 + Date.Month(MaxD))
             - (Date.Year(Start) * 12 + Date.Month(Start)) + 1,
    Months = List.Transform({0..Count - 1}, (i) => Date.AddMonths(Start, i)),
    T      = Table.TransformColumnTypes(
                 Table.FromList(Months, Splitter.SplitByNothing(), {"Month"}),
                 {{"Month", type date}}),
    MN     = Table.AddColumn(T, "MonthName", each Date.ToText([Month], "MMM''yy"), type text),
    MS     = Table.AddColumn(MN, "MonthSort",
                 each Date.Year([Month]) * 100 + Date.Month([Month]), Int64.Type),
    MI     = Table.AddColumn(MS, "MonthIndex",
                 each Date.Year([Month]) * 12 + Date.Month([Month]), Int64.Type),
    FY     = Table.AddColumn(MI, "FY", each
                 let y = if Date.Month([Month]) >= 4 then Date.Year([Month]) else Date.Year([Month]) - 1
                 in  "FY " & Text.From(y) & "-" & Text.End(Text.From(y + 1), 2), type text)
in
    FY
```

## qcHeaders

> Your self-check: lists the real sheet names and headers of every file in all four folders. Leave Enable load ON.

```
let
    Folders  = {"RM Raw", "FG Raw", "Consble Raw", "TB"},
    AllFiles = Table.Combine(List.Transform(Folders, (f) =>
                   Table.AddColumn(
                       Table.SelectRows(Folder.Files(pRoot & "\" & f),
                           each Text.Lower([Extension]) = ".xlsx"
                           and not Text.StartsWith([Name], "~$")
                           and not Text.StartsWith([Name], ".")),
                       "Folder", each f, type text))),
    Slim     = Table.SelectColumns(AllFiles, {"Folder","Name","Content"}),
    Hdrs     = Table.AddColumn(Slim, "Headers", each
                   let
                       Wb = Excel.Workbook([Content], null, true),
                       Sh = Table.SelectRows(Wb, each [Kind] = "Sheet"),
                       D  = try Sh{[Item="Sheet1", Kind="Sheet"]}[Data] otherwise Sh{0}[Data],
                       P  = Table.PromoteHeaders(D, [PromoteAllScalars=true])
                   in
                       Text.Combine(List.Transform(Table.ColumnNames(P), Text.From), " | "),
                   type text),
    Sheets   = Table.AddColumn(Hdrs, "SheetNames", each
                   let Wb = Excel.Workbook([Content], null, true)
                   in  Text.Combine(Table.SelectRows(Wb, each [Kind] = "Sheet")[Item], " | "),
                   type text),
    Out      = Table.SelectColumns(Sheets, {"Folder","Name","SheetNames","Headers"})
in
    Out
```

## qcVarHeaders

> Your self-check for Variables and Calculations: every sheet, its exact headers, and its row count. Leave Enable load ON.

```
let
    Wb    = Excel.Workbook(File.Contents(pVarsFile), null, true),
    Sh    = Table.SelectRows(Wb, each [Kind] = "Sheet"),
    Slim  = Table.SelectColumns(Sh, {"Item","Data"}),
    Hdrs  = Table.AddColumn(Slim, "Headers", each
                Text.Combine(List.Transform(
                    Table.ColumnNames(Table.PromoteHeaders([Data], [PromoteAllScalars=true])),
                    Text.From), " | "), type text),
    Rows  = Table.AddColumn(Hdrs, "DataRows", each Table.RowCount([Data]) - 1, Int64.Type),
    Out   = Table.RenameColumns(Table.SelectColumns(Rows, {"Item","Headers","DataRows"}),
                {{"Item","SheetName"}})
in
    Out
```

## qcNatureNoCapacity

> Lists FG Natures with no matching Tech on the MW sheet. Those rows get blank Days. Empty table = good.

```
let
    FGNatures = List.Distinct(List.RemoveNulls(dimFGAttr[Nature])),
    CapTechs  = List.Distinct(List.RemoveNulls(varMWCapacity[Tech])),
    Orphans   = List.Difference(FGNatures, CapTechs),
    T         = Table.FromList(Orphans, Splitter.SplitByNothing(), {"Nature"})
in
    T
```

## qcMWSheet

> Diagnostic. Shows the MW sheet exactly as it sits in Excel, cell for cell, with no interpretation. If `varMWCapacity` complains, look here and read me the layout. Leave Enable load ON.

```
let
    Wb      = Excel.Workbook(File.Contents(pVarsFile), null, true),
    Sh      = Table.SelectRows(Wb, each [Kind] = "Sheet"),
    Norm    = (n as any) as text =>
                  Text.Upper(Text.Remove(Text.Trim(Text.From(n ?? "")), {" ",".","_","-"})),
    Hit     = Table.SelectRows(Sh, each
                  List.Contains({"MW","MWCAPACITY","CAPACITY","MWCAP"}, Norm([Item]))),
    Data    = Hit{0}[Data],
    AsText  = Table.TransformColumns(Data,
                  List.Transform(Table.ColumnNames(Data),
                      (c) => {c, each Text.From(_ ?? ""), type text}))
in
    AsText
```

## dimCategory

> The shared RM / FG / Consumables list. Both `factInventory` and `factTB` join to it, which is what puts the trial balance and MB5B on the same row of the Summary matrix.

```
let
    Src = #table(
        type table [Category = text, CategorySort = Int64.Type],
        {
            {"RM",          1},
            {"FG",          2},
            {"Consumables", 3}
        })
in
    Src
```

## dimMetric

> Deliberately disconnected — no relationship to anything. It exists so a matrix can have `Inventory (TB)`, `Inventory (MB5B)` and `Difference` as its three master columns, with months underneath them. The `Summary Value ₹ Cr` measure reads which one a cell is in.

```
let
    Src = #table(
        type table [Metric = text, MetricSort = Int64.Type],
        {
            {"Inventory (TB)",    1},
            {"Inventory (MB5B)",  2},
            {"Difference",        3}
        })
in
    Src
```

## dimMeasure

> Also disconnected. Gives the FG and RM matrices their `MW` / `In ₹ Cr` / `In Days` master columns.

```
let
    Src = #table(
        type table [Measure = text, MeasureSort = Int64.Type],
        {
            {"MW",       1},
            {"In ₹ Cr",  2},
            {"In Days",  3}
        })
in
    Src
```

---

# Appendix B — measures

Add these one at a time (**Home → New measure**), with `factInventory` selected. Copy the
whole block each time — several measures build on the ones above them, so keep the order.

Everything money is in **crore rupees** and named so a reader knows what it is without asking.
`SUM(...)/10000000` is the crore conversion.

*value, as at the end of the selected month*

```
Value ₹ Cr = DIVIDE(SUM(factInventory[CloseVal]), 10000000)
```

```
As On = "as on " & FORMAT(EOMONTH(MAX(dimDate[Month]), 0), "dd MMM yyyy")
```

```
Value ₹ Cr Title = "Value ₹ Cr " & [As On]
```

```
Opening Value ₹ Cr = DIVIDE(SUM(factInventory[OpenVal]), 10000000)
```

```
Receipts ₹ Cr = DIVIDE(SUM(factInventory[ReceiptVal]), 10000000)
```

```
Issues ₹ Cr = DIVIDE(SUM(factInventory[IssueVal]), 10000000)
```

```
Closing Qty = SUM(factInventory[CloseQty])
```

*by category*

```
RM ₹ Cr = CALCULATE([Value ₹ Cr], factInventory[Category] = "RM")
```

```
FG ₹ Cr = CALCULATE([Value ₹ Cr], factInventory[Category] = "FG")
```

```
Consumables ₹ Cr = CALCULATE([Value ₹ Cr], factInventory[Category] = "Consumables")
```

```
Share of Total % = DIVIDE([Value ₹ Cr], CALCULATE([Value ₹ Cr], ALL(factInventory[Category])))
```

*megawatts and days*

```
MW = SUM(factInventory[MW])
```

```
FG MW = CALCULATE([MW], factInventory[Category] = "FG")
```

```
Capacity MW = SUM(dimCapacity[CapacityMW])
```

```
Capacity MW (plant) = CALCULATE(SUM(dimCapacity[CapacityMW]), REMOVEFILTERS(dimNature))
```

The second one exists for a real problem: capacity is keyed by technology, and an RM nature
(`Glass`, `Wafer`) is not a technology, so plain `Capacity MW` goes blank the moment an RM
row filters it. Removing the nature filter falls back to the plant's capacity, which is the
right denominator for RM.

*Days works the same way for every category: the stock converted to megawatts, divided by*

*the MW capacity on the Variables workbook's MW sheet. RM converts through the 580 factor,*

*FG through its own MW, so one formula covers the whole report.*

```
Days of Inventory =
VAR Cap = IF(ISBLANK([Capacity MW]), [Capacity MW (plant)], [Capacity MW])
RETURN DIVIDE([MW], Cap)
```

So an FG technology row divides by that technology's capacity, and an RM row divides by the
plant's.

```
FG Days = DIVIDE([FG MW], [Capacity MW])
```

```
INR per Wp = SUM(factInventory[INR_WP])
```

*month-on-month and year-on-year comparison*

```
Value ₹ Cr LM =
VAR PrevIdx = MAX(dimDate[MonthIndex]) - 1
RETURN CALCULATE([Value ₹ Cr], ALL(dimDate), dimDate[MonthIndex] = PrevIdx)
```

```
Value ₹ Cr vs LM = [Value ₹ Cr] - [Value ₹ Cr LM]
```

```
Value ₹ Cr % vs LM = DIVIDE([Value ₹ Cr vs LM], [Value ₹ Cr LM])
```

```
Value ₹ Cr LY =
VAR PrevIdx = MAX(dimDate[MonthIndex]) - 12
RETURN CALCULATE([Value ₹ Cr], ALL(dimDate), dimDate[MonthIndex] = PrevIdx)
```

```
Value ₹ Cr % vs LY = DIVIDE([Value ₹ Cr] - [Value ₹ Cr LY], [Value ₹ Cr LY])
```

```
MW LM =
VAR PrevIdx = MAX(dimDate[MonthIndex]) - 1
RETURN CALCULATE([MW], ALL(dimDate), dimDate[MonthIndex] = PrevIdx)
```

```
MW vs LM = [MW] - [MW LM]
```

```
Days LM =
VAR PrevIdx = MAX(dimDate[MonthIndex]) - 1
RETURN CALCULATE([Days of Inventory], ALL(dimDate), dimDate[MonthIndex] = PrevIdx)
```

```
Days vs LM = [Days of Inventory] - [Days LM]
```

*peak, average and latest across whatever months are in view*

```
Avg Value ₹ Cr = AVERAGEX(VALUES(dimDate[MonthIndex]), [Value ₹ Cr])
```

```
Peak Value ₹ Cr = MAXX(VALUES(dimDate[MonthIndex]), [Value ₹ Cr])
```

```
Latest Month Value ₹ Cr =
VAR LastIdx = CALCULATE(MAX(dimDate[MonthIndex]), ALLSELECTED(dimDate))
RETURN CALCULATE([Value ₹ Cr], dimDate[MonthIndex] = LastIdx)
```

*trial balance reconciliation*

```
TB ₹ Cr = DIVIDE(SUM(factTB[Amount]), 10000000)
```

```
Difference ₹ Cr = [TB ₹ Cr] - [Value ₹ Cr]
```

```
Difference % = DIVIDE([Difference ₹ Cr], [TB ₹ Cr])
```

*data quality*

```
Stock Recon ₹ Cr = [Opening Value ₹ Cr] + [Receipts ₹ Cr] - [Issues ₹ Cr] - [Value ₹ Cr]
```

```
Rows Missing Attr = CALCULATE(COUNTROWS(factInventory), factInventory[AttrMissing] = TRUE())
```

```
Unmapped TB ₹ Cr = DIVIDE(SUM(factTB_Unmapped[Amount]), 10000000)
```

*days*

There is only one definition, so there is only one measure. `Days` is an alias of
`Days of Inventory` so that every visual reads the same word:

```
Days = [Days of Inventory]
```

One consequence worth knowing: 1905 has no module capacity, so its Days cells come out
blank rather than wrong. That is the correct behaviour — a blank is a question, a made-up
number is an error nobody catches.

*the switch measures — these are what give a matrix its master columns*

`dimMetric` and `dimMeasure` have no relationship to anything, so a measure has to read the
column a cell sits in with `SELECTEDVALUE` and return the right number. That is the whole
trick behind `Inventory (TB) | Inventory (MB5B) | Difference` sitting side by side with
months underneath.

```
Summary Value ₹ Cr =
SWITCH(SELECTEDVALUE(dimMetric[Metric]),
    "Inventory (TB)",   [TB ₹ Cr],
    "Inventory (MB5B)", [Value ₹ Cr],
    "Difference",       [Difference ₹ Cr],
    [Value ₹ Cr])
```

```
Unit Value =
SWITCH(SELECTEDVALUE(dimMeasure[Measure]),
    "MW",      [MW],
    "In ₹ Cr", [Value ₹ Cr],
    "In Days", [Days],
    [Value ₹ Cr])
```

*keeping a matrix to the last four months*

```
Last 4 Months =
VAR LastIdx = CALCULATE(MAX(dimDate[MonthIndex]), ALL(dimDate))
RETURN IF(MAX(dimDate[MonthIndex]) > LastIdx - 4, 1, 0)
```

Put `Last 4 Months` in a matrix's Filters pane and set it to **is 1**. The matrix then always
shows the four most recent months and never needs editing again — a new month of files
appears on its own and the oldest drops off.

*formatting, once all of the above exist*

Select each money measure → **Measure tools** → **Format: Decimal number**, 2 decimals.
For `Days of Inventory` and `MW` use 1 decimal. For the `%` measures use **Percentage**,
1 decimal. `Share of Total %` and `Difference %` both read better as percentages than as
raw ratios, and a reader can't tell the difference from the number alone.
