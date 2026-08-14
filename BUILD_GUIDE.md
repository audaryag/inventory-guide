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
| 8 | `dimPlant` | the three plants are named in it; other codes come from the facts |
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

### Checkpoint — do not go to Part 2 until all five are true

1. The Queries list on the left of Power Query shows **31** names, and every name in the
   table above appears in it, spelled identically. Compare them one by one; a missing one
   is the single most common cause of an error later.
2. The 14 helper names in step 1.5 are shown in *italics* in that list (that is what
   "Enable load off" looks like); the other 17 are not italic.
3. Click `factInventory`: the preview shows rows, and the columns include `CloseVal`,
   `Category`, `Nature`, `Month`, `ValuationArea`, `MW`.
4. Click `factTB`: it shows rows, `Month` is filled in on every row, and `ValuationArea`
   is not the word `Unallocated` on every row.
5. Click `factTB_Unmapped`: ideally empty. Rows here mean a GL account in your TB is
   missing from `TB Master`, so its money is not counted anywhere — add it to `TB Master`
   and refresh.

After **Close & Apply**, the Data pane on the right must list exactly these 17 tables:
`factInventory`, `factTB`, `factTB_Unmapped`, `dimPlant`, `dimDate`, `dimNature`,
`dimCapacity`, `dimTBMaster`, `dimMaterialAttr`, `dimFGAttr`, `dimCategory`, `dimMetric`,
`dimMeasure`, `qcHeaders`, `qcVarHeaders`, `qcNatureNoCapacity`, `qcMWSheet`.

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

> Two ways to reach *Sort by column*, use whichever pane you can see:
> **Data view** — left sidebar, the middle icon (a grid) → click the table in the Data pane
> → click the column's heading in the grid → ribbon **Column tools** → **Sort by column**.
> **Model view** — left sidebar, the third icon → click the field's name inside the table
> box → the **Properties** pane opens on the right → expand **Advanced** → **Sort by
> column**. If you can only see one view icon you are still inside the Power Query window;
> close it with **Home → Close & Apply** and all three icons appear.

**2.6** Do the same for: `dimPlant[Plant]` → `PlantSort`, `dimCategory[Category]` →
`CategorySort`, `dimMetric[Metric]` → `MetricSort`, `dimMeasure[Measure]` → `MeasureSort`,
`dimDate[Quarter]` → `QuarterSort`. The middle two matter — without them your master columns
come out alphabetically (Difference first), which reads backwards. `Quarter` matters because
alphabetical order puts Q1 of every year together.

**2.7** Hide the plumbing so the Fields list stays usable. In Model view, right-click the
field's name inside its table box → **Hide in report view**. Do it on:
`factInventory[MatKey]`, `factTB[PlantCode]`, `dimDate[MonthSort]`, `dimPlant[PlantSort]`,
`dimDate[FYMonthNo]`, `dimDate[QuarterNo]`, `dimDate[QuarterSort]`.

### Checkpoint — do not go to Part 3 until all four are true

1. Ribbon **Modeling** → **Manage relationships** lists **11** relationships, all with the
   **Active** box ticked. Read it as a table and compare it line by line with 2.3 — far
   easier than reading the diagram.
2. Every one says **Many to one** or **One to many** (never **Many to many**) and
   **Single** (never **Both**).
3. `dimMetric` and `dimMeasure` appear in **no** relationship at all.
4. There is no relationship you did not create yourself; delete any Power BI guessed.

**2.8** Nothing else to set up for quarters — the `Quarter` column does it. The **Month**
slicer lets you tick exactly which months a page compares, and the **Quarter** slicer picks
`Q1 FY 2026-27` (April–June) and so on. Both are just slicers, built in Part 4.

---

# PART 3 — Add the measures (15 min)

**3.1** Left sidebar: click the **Report** icon (top one).

**3.2** In the Fields pane, click `factInventory` once to select it.

**3.3** Ribbon: **Home** → **New measure**. A formula bar appears at the top.

**3.4** Delete what's there, paste **one** measure from Appendix B, press **Enter**.

**3.5** Repeat 3.3–3.4 for every measure in Appendix B, **strictly top to bottom**. One at a
time — Power BI takes one measure per box. Order matters: later measures use earlier ones, so
pasting out of order gives "cannot be determined" on a measure that is perfectly fine.

> It does not matter which table a measure ends up under. Power BI files it beside whatever
> was selected, and that changes nothing about how it behaves. To find one later, type its
> name into the search box at the top of the **Data** pane rather than opening tables.
>
> If the ₹ sign does not survive pasting and a measure lands as `Value  Cr`, right-click it
> → **Rename** and type the name again from the guide. The formula is unaffected.

### Checkpoint — do not go to Part 4 until all three are true

1. Type `Value` into the Data pane search box: `Value ₹ Cr` is there, with a calculator icon.
2. Count the measures (calculator icons) — there must be **75**. Fewer means Appendix B is
   not finished; the pages will fail on whichever one is missing.
3. None of these six old names survive: `Closing Value`, `Inv RM`, `Inv FG`,
   `Inv Consumables`, `TB Value`, `Prev Month`. Delete any you find (right-click → **Delete
   from model**), otherwise a visual may quietly use the old one.
4. `Days` is the one name that stays. **Do not delete it** — the RM and FG matrices use it.
   Click it once and check the formula bar reads `Days = [Days of Inventory]`; if it says
   anything else, select the whole formula and paste the Appendix B version over it.

**3.6** Everything money is already in **crore rupees** and named to say so
(`Value ₹ Cr`, `TB ₹ Cr`, …), so no currency symbol is needed. Click each ₹ Cr measure →
ribbon **Measure tools** → **Format: Decimal number**, **Decimal places: 2**.
For `MW`, `FG MW`, `Capacity MW`, `Days of Inventory`, use **Decimal places: 1**.
For every `%` measure use **Format: Percentage**, 1 decimal.

**3.7** If you built an earlier version of this file, the old names are gone: `Closing Value`
became `Value ₹ Cr`, `Inv RM/FG/Consumables` became `RM/FG/Consumables ₹ Cr`, `TB Value`
became `TB ₹ Cr`, `Prev Month` became `Value ₹ Cr LM`. Delete those six (right-click →
**Delete from model**) after the new ones exist, or visuals will still point at the old ones.

`Days` is the exception: the name is unchanged but the formula is not. Do **not** delete it —
click it and paste the Appendix B version (`Days = [Days of Inventory]`) over whatever is in
the formula bar. Deleting it breaks the RM and FG matrices, which read it through
`Unit Value`.

---

# PART 4 — Build the pages

Each visual is spelled out the same way: what to insert, which field goes in which
well, and the four numbers that place it on a 1280 x 720 canvas.

> Prefer one instruction at a time? Use the **Build it** tab — same content, one step per screen, with a Next button.

**To place any visual:** select it → Format pane → General → Properties → open
**Size** and **Position** → type Width, Height, **Horizontal** (this is X) and
**Vertical** (this is Y). Older versions put all four under **Size and style**.

**What the Format pane calls things.** Every name below is a heading you click in
the paintbrush pane. If a heading is not in your list, your version does not have
it — skip that line, nothing else changes.

| Name in the Format pane | What it actually is |
|---|---|
| Callout value | the one big number on a card |
| Category label | the small grey words *under* the number on a card, which repeat the measure's name. The newer Card visual has none |
| Title | the heading strip along the top of any visual, which you type yourself |
| Column headers | the headings across the top of a matrix or table |
| Row headers | the names down the left of a matrix, where the +/− signs live |
| Values | the numbers in the body of a matrix or table |
| Detail labels | the numbers or words written on the slices of a pie or donut |
| Legend | the small colour key that names each colour |
| X-axis | the labels along the bottom of a chart |
| Y-axis | the number scale up the side of a chart |
| Data labels | numbers printed on top of the bars themselves |
| Grid | the lines between matrix rows, and the row height |

**4.0 Canvas and theme, before anything else.**

1. Click empty canvas → Format pane → Canvas settings → Type 16:9, Height 720, Width 1280.
2. Download [inventory-theme.json](inventory-theme.json) (right-click → Save link as).
3. Ribbon **View** → **Themes** → **Browse for themes** → pick that file.

Colours, fonts, borders and card styling all come from the theme, so nothing below
asks you to colour anything.

Only two colours are ever used for a printed number, and never grey: **#FFFFFF** bold when the number sits on top of a coloured bar or slice, and **#14532D** (or **#1F2A24** for plain figures) when it sits on the white card. If a number anywhere looks faint grey — inside a bar, above a line, on an axis — that visual predates this theme: re-import the theme file, then check the visual's **Data labels → Colour**. On a combo chart the two series are set separately, under **Data labels → Apply settings to → Series**: the column series #FFFFFF, the line series #14532D.

**Create the 6 pages** with the **+** at the bottom, named: `Overview` · `Summary` · `FG` · `RM` · `Detail` · `Checks`.

---

## The furniture: the green panel (no data in any of it)

Build it once on `Overview` and copy it to the other five pages — the panel is the one thing that never moves, so a reader always finds the same figures in the same corner. Every page's own visuals then start at Horizontal 192, clear of it.

| What | Insert it with | Text / fill | Horizontal (X) | Vertical (Y) | Width | Height |
|---|---|---|---|---|---|---|
| the green panel | Insert → Shapes → Rectangle | #14532D | 0 | 0 | 184 | 720 |
| the logo strip | Insert → Image | any picture for now | 12 | 10 | 160 | 34 |
| text 'Inventory' | Insert → Text box | Arial 15, #FFFFFF | 12 | 50 | 160 | 22 |
| text 'Overview' | Insert → Text box | Arial 13, #BFE3C6 | 12 | 72 | 160 | 20 |
| text 'By Type' | Insert → Text box | Arial 10, #BFE3C6 | 12 | 100 | 160 | 16 |
| white box 1, for RM, FG and Consumables | Insert → Shapes → Rectangle | #FFFFFF, rounded corners 8 | 8 | 118 | 168 | 186 |
| text 'By Plant' | Insert → Text box | Arial 10, #BFE3C6 | 12 | 310 | 160 | 16 |
| white box 2, for the three plants | Insert → Shapes → Rectangle | #FFFFFF, rounded corners 8 | 8 | 328 | 168 | 186 |
| white box 3, for Total, Change since Last Month and the As on line | Insert → Shapes → Rectangle | #FFFFFF, rounded corners 8 | 8 | 522 | 168 | 186 |

Build the green panel first and **right-click → Send to back**. Then the three
white boxes, each **right-click → Send backward** once, so they cover the green but
stay under the cards. Every card on the panel has **General → Effects →
Background: Off**, and its number in **#1F2A24** — the white box behind it is what supplies the white.

---

## Page — Overview

**4.5** **Card** — Panel figure, sitting inside the white box. It reads the latest month that has data and ignores every slicer on the page, because stock is a level, not something you add up across months.

| Well | Field |
|---|---|
| Fields | `Ticker RM Rs Cr` |

Title: `RM`

Position: Horizontal 14, Vertical 122, Width 156, Height 58.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Display units' and set it to None, Value decimal places: 1, Font: Arial, Font size: 11, Bold: On, Colour: #1F2A24 (near-black, because the box behind it is white now). Display units None is what stops Power BI writing 2.5K instead of 2,539.4.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 10, Colour: #14532D, Text: the title above.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to Off, and Border: Off. The white comes from the box shape underneath, so the card itself stays see-through.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Properties', then 'Position' and set it to set Horizontal (X) and Vertical (Y) to 14 and 122 exactly, or the card will not sit square inside its box.

**4.6** **Card** — Panel figure, sitting inside the white box. It reads the latest month that has data and ignores every slicer on the page, because stock is a level, not something you add up across months.

| Well | Field |
|---|---|
| Fields | `Ticker FG Rs Cr` |

Title: `FG`

Position: Horizontal 14, Vertical 182, Width 156, Height 58.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Display units' and set it to None, Value decimal places: 1, Font: Arial, Font size: 11, Bold: On, Colour: #1F2A24 (near-black, because the box behind it is white now). Display units None is what stops Power BI writing 2.5K instead of 2,539.4.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 10, Colour: #14532D, Text: the title above.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to Off, and Border: Off. The white comes from the box shape underneath, so the card itself stays see-through.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Properties', then 'Position' and set it to set Horizontal (X) and Vertical (Y) to 14 and 182 exactly, or the card will not sit square inside its box.

**4.7** **Card** — Panel figure, sitting inside the white box. It reads the latest month that has data and ignores every slicer on the page, because stock is a level, not something you add up across months.

| Well | Field |
|---|---|
| Fields | `Ticker Consumables Rs Cr` |

Title: `Consumables`

Position: Horizontal 14, Vertical 242, Width 156, Height 58.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Display units' and set it to None, Value decimal places: 1, Font: Arial, Font size: 11, Bold: On, Colour: #1F2A24 (near-black, because the box behind it is white now). Display units None is what stops Power BI writing 2.5K instead of 2,539.4.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 10, Colour: #14532D, Text: the title above.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to Off, and Border: Off. The white comes from the box shape underneath, so the card itself stays see-through.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Properties', then 'Position' and set it to set Horizontal (X) and Vertical (Y) to 14 and 242 exactly, or the card will not sit square inside its box.

**4.8** **Card** — Panel figure, sitting inside the white box. It reads the latest month that has data and ignores every slicer on the page, because stock is a level, not something you add up across months.

| Well | Field |
|---|---|
| Fields | `Ticker 1900 Rs Cr` |

Title: `1900 Jaipur Module`

Position: Horizontal 14, Vertical 332, Width 156, Height 58.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Display units' and set it to None, Value decimal places: 1, Font: Arial, Font size: 11, Bold: On, Colour: #1F2A24 (near-black, because the box behind it is white now). Display units None is what stops Power BI writing 2.5K instead of 2,539.4.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 10, Colour: #14532D, Text: the title above.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to Off, and Border: Off. The white comes from the box shape underneath, so the card itself stays see-through.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Properties', then 'Position' and set it to set Horizontal (X) and Vertical (Y) to 14 and 332 exactly, or the card will not sit square inside its box.

**4.9** **Card** — Panel figure, sitting inside the white box. It reads the latest month that has data and ignores every slicer on the page, because stock is a level, not something you add up across months.

| Well | Field |
|---|---|
| Fields | `Ticker 1902 Rs Cr` |

Title: `1902 Dholera Module`

Position: Horizontal 14, Vertical 392, Width 156, Height 58.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Display units' and set it to None, Value decimal places: 1, Font: Arial, Font size: 11, Bold: On, Colour: #1F2A24 (near-black, because the box behind it is white now). Display units None is what stops Power BI writing 2.5K instead of 2,539.4.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 10, Colour: #14532D, Text: the title above.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to Off, and Border: Off. The white comes from the box shape underneath, so the card itself stays see-through.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Properties', then 'Position' and set it to set Horizontal (X) and Vertical (Y) to 14 and 392 exactly, or the card will not sit square inside its box.

**4.10** **Card** — Panel figure, sitting inside the white box. It reads the latest month that has data and ignores every slicer on the page, because stock is a level, not something you add up across months.

| Well | Field |
|---|---|
| Fields | `Ticker 1905 Rs Cr` |

Title: `1905 Dholera Cell`

Position: Horizontal 14, Vertical 452, Width 156, Height 58.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Display units' and set it to None, Value decimal places: 1, Font: Arial, Font size: 11, Bold: On, Colour: #1F2A24 (near-black, because the box behind it is white now). Display units None is what stops Power BI writing 2.5K instead of 2,539.4.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 10, Colour: #14532D, Text: the title above.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to Off, and Border: Off. The white comes from the box shape underneath, so the card itself stays see-through.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Properties', then 'Position' and set it to set Horizontal (X) and Vertical (Y) to 14 and 452 exactly, or the card will not sit square inside its box.

**4.11** **Card** — Panel figure, sitting inside the white box. It reads the latest month that has data and ignores every slicer on the page, because stock is a level, not something you add up across months.

| Well | Field |
|---|---|
| Fields | `Ticker Rs Cr` |

Title: `Total`

Position: Horizontal 14, Vertical 528, Width 156, Height 62.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Display units' and set it to None, Value decimal places: 1, Font: Arial, Font size: 13, Bold: On, Colour: #1F2A24 (near-black, because the box behind it is white now). Display units None is what stops Power BI writing 2.5K instead of 2,539.4.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 10, Colour: #14532D, Text: the title above.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to Off, and Border: Off. The white comes from the box shape underneath, so the card itself stays see-through.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Properties', then 'Position' and set it to set Horizontal (X) and Vertical (Y) to 14 and 528 exactly, or the card will not sit square inside its box.

**4.12** **Card** — One line reading, for example, +12.4 Rs Cr. (+2.1%) — the amount and the percentage together, each labelled, so nobody has to ask which is which. Same white box as Total, directly under it.

| Well | Field |
|---|---|
| Fields | `Ticker Change Text` |

Title: `Change since Last Month`

Position: Horizontal 14, Vertical 592, Width 156, Height 58.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Font' and set it to Arial, Font size: 11, Bold: On, Colour: #1F2A24. Eleven, not sixteen: this line carries the amount and the percentage together in a 156-wide box, and anything larger is cut off mid-figure. Green and red would fight with the white box, so the sign carries the meaning instead.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 10, Colour: #14532D, Text: Change since Last Month.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to Off, Border: Off.
- The measure writes its own + or − sign and both units, so leave Display units alone.

**4.13** **Card** — Says which month the whole panel is showing, so a reader never has to guess. 44 tall, not 28: the sentence sits under the words 'As on' and 28 cuts the sentence in half.

| Well | Field |
|---|---|
| Fields | `As On Text` |

Title: `As on`

Position: Horizontal 14, Vertical 652, Width 156, Height 44.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Font' and set it to Arial, Font size: 10, Colour: #4B5563.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title' and set it to Off — the sentence says it all.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to Off, Border: Off.

**4.14** **Slicer** — Tick nothing and you get March — the year-end close — followed by the last four months that have data, five columns in all, or fewer early in the year: in April just March and April. Tick your own months and they replace that, up to the 5 most recent of your ticks. The list holds only the months you have actually loaded — add July'25's MB5B and July'25 appears here, and until then it is not an option at all, because the calendar is built from the files rather than from a fixed April-to-March range. Months are the only period on this page: the columns and the bars are dimDate[MonthName] itself, not a switchable parameter.

| Well | Field |
|---|---|
| Field | `dimDate[MonthName]` |

Title: `Months (Leave Empty for March Plus the Last 4)`

Position: Horizontal 192, Vertical 8, Width 268, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Selection' and set it to switch OFF 'Multi-select with CTRL' so ticking several needs no keyboard.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font size' and set it to 10, Colour: #14532D.

**4.15** **Slicer** — Filters the history and the donuts. The panel on the left ignores it on purpose.

| Well | Field |
|---|---|
| Field | `dimPlant[Plant]` |

Title: `Plant`

Position: Horizontal 468, Vertical 8, Width 262, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font size' and set it to 10, Colour: #14532D.

**4.16** **Slicer** — RM, FG or consumables.

| Well | Field |
|---|---|
| Field | `dimCategory[Category]` |

Title: `Type`

Position: Horizontal 738, Vertical 8, Width 294, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font size' and set it to 10, Colour: #14532D.

**4.17** **Stacked column chart** — Five months side by side. The In Window filter is what keeps it to five without you having to prune the slicer.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `Inventory Rs Cr` |
| Legend | `dimCategory[Category]` |
| Filters | `In Window  →  is 1` |

Title: `Inventory by Month (Rs Cr.)`

Position: Horizontal 200, Vertical 88, Width 700, Height 336.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- In the Visualizations pane click the paintbrush icon, then click 'Data labels' and set it to Off. The segment figures are deliberately not printed: the consumables slice is too thin to hold one, so some months showed a number and others did not. Hover a segment for RM, FG or consumables in that month, and click it to filter the rest of the page to it.
- In the Visualizations pane click the paintbrush icon, then click 'Total labels' and set it to On, Font: Arial, Font size: 9, Bold: On, Colour: #14532D, Display units: None, Value decimal places: 1 — the month total above each bar is the only printed number, dark green because it sits on the white card.
- Drag Share of Total % into the visual's Tooltips well, so hovering gives the share as well as the figure.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Text' and set it to type the heading above. It is typed words, not a measure — the axis is always months, so the heading never has to change.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 12, Colour: #14532D.

**4.18** **Matrix** — The same five columns as the chart directly above it, for readers who want the figures rather than the shape. Only as tall as its four rows, so no white gap is left under it. Left to itself the first column is always March — the year-end close — and the four columns after it are the last four months that have data, so in July you get Mar, Apr, May, Jun, Jul and in April just Mar and Apr. Tick five months in the picker and your ticks replace that entirely. That behaviour lives in the In Window filter, so the chart above obeys it too.

| Well | Field |
|---|---|
| Rows | `dimCategory[Category]` |
| Columns | `dimDate[MonthName]` |
| Values | `Inventory Rs Cr` |
| Filters | `In Window  →  is 1` |

Title: `Inventory by Month (Rs Cr.)`

Position: Horizontal 200, Vertical 432, Width 700, Height 136.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Stepped layout' and set it to Off.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On, Column subtotals: Off. Here the total row earns its place, because the three types add up to the month.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 10, Colour: #14532D.

**4.19** **Line and clustered column chart** — The long view, under the table: one bar per month for the last twelve months that have data, or fewer if that is all there is. Two numbers on every month — the bar prints the megawatts held, the line above it prints the change on the month before as a percentage. It is in MW rather than rupees on purpose: this strip is about how much product is sitting there, which prices cannot flatter. Each bar is that month's closing stock on its own, so nothing here is ever added across months.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Column y-axis | `MW` |
| Line y-axis | `MW % vs LM` |
| Filters | `In Last 12  →  is 1` |

Title: `Total Inventory by Month, Last 12 Months (MW and % vs Last Month)`

Position: Horizontal 200, Vertical 576, Width 700, Height 130.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- This one must ignore the two controls at the top, or it would shrink back to five months. Click the 'Months' slicer once, then ribbon Format → Edit interactions; small icons appear on every other visual. On this chart click the circle-with-a-line (None). Leave Plant and Type set to filter, so those two still work on it.
- In the Visualizations pane click the paintbrush icon, then click 'Data labels: On. Then open 'Apply settings to'', then 'Series and pick MW' and set it to Font: Arial, Font size: 8, Bold: On, Colour: #FFFFFF, Display units: None, Value decimal places: 1, Position: Inside end — white, because this number is printed on the green bar.
- Still under Data labels, switch 'Apply settings to' → Series to 'MW % vs LM': Font: Arial, Font size: 8, Colour: #14532D, Value decimal places: 0, Position: Above. That is the second number you asked for — the percentage sits over the bar, the crore figure sits inside it, so the two never collide.
- In the Visualizations pane click the paintbrush icon, then click 'Y-axis' and set it to Off, and Secondary y-axis: Off. Both numbers are printed on the chart, so two scales up the sides would only eat the height.
- In the Visualizations pane click the paintbrush icon, then click 'X-axis', then 'Values', then 'Font' and set it to Arial, Font size: 8, Colour: #1F2A24, Concatenate labels: Off, and Maximum height: 20%.
- In the Visualizations pane click the paintbrush icon, then click 'X-axis', then 'Inner padding: 30%, and Format pane', then 'General', then 'Properties', then 'Padding' and set it to Left 12, Right 12. The padding is what stops the first and last bar touching the sides of the card, and it pulls both edges in by the same amount.
- In the Visualizations pane click the paintbrush icon, then click 'Columns', then 'Colour: #2E7D46. Format pane', then 'Lines', then 'Colour' and set it to #9AA79F, Stroke width: 1, Show marker: On, Marker size: 3 — the line is only there to carry its labels, so it is deliberately quiet.
- In the Visualizations pane click the paintbrush icon, then click 'Legend' and set it to Off. Two series, both labelled on the chart, so a key would repeat what the labels already say.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 11, Colour: #14532D.

**4.20** **Donut chart** — What the finished goods are made of in the latest month that has data — the module technologies, largest slice first. It is pinned to the latest month by the In Latest Month filter, because adding one month-end of stock to another would be meaningless; the Plant and Type slicers still narrow it.

| Well | Field |
|---|---|
| Legend | `dimNature[Nature]` |
| Values | `Value ₹ Cr` |
| Filters | `dimCategory[Category]  →  is FG`, `In Latest Month  →  is 1` |

Title: `FG Components, Latest Month (Rs Cr. and % Share)`

Position: Horizontal 916, Vertical 88, Width 348, Height 306.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Detail labels' and set Font size to 9. If a slice label is still cut off, set 'Position' to Outside, and switch on 'Overflow text' if your version offers it.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'. If the legend eats the chart, switch Legend off entirely — the labels already name the slices.
- In the Visualizations pane click the paintbrush icon, then click 'Detail labels', then 'Label contents' and set it to Category, percent of total, Font: Arial, Font size: 9, Colour: #1F2A24, Value decimal places: 1.
- In the Visualizations pane click the paintbrush icon, then click 'Detail labels', then 'Position' and set it to Outside, so a thin technology still shows its percentage.
- In the Visualizations pane click the paintbrush icon, then click 'Legend', then 'Position' and set it to Bottom center, Font size: 9.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 12, Colour: #14532D.
- Right-click a slice → Drill through → Detail to see the materials inside that technology.

**4.21** **Donut chart** — The same for raw materials in the latest month — cell, glass, frame, POE, packing and the rest — so the two donuts read as a pair: what the finished stock is, and what the raw stock is.

| Well | Field |
|---|---|
| Legend | `dimNature[Nature]` |
| Values | `Value ₹ Cr` |
| Filters | `dimCategory[Category]  →  is RM`, `In Latest Month  →  is 1` |

Title: `RM Components, Latest Month (Rs Cr. and % Share)`

Position: Horizontal 916, Vertical 402, Width 348, Height 304.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Detail labels' and set Font size to 9. If a slice label is still cut off, set 'Position' to Outside, and switch on 'Overflow text' if your version offers it.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'. If the legend eats the chart, switch Legend off entirely — the labels already name the slices.
- In the Visualizations pane click the paintbrush icon, then click 'Detail labels', then 'Label contents' and set it to Category, percent of total, Font: Arial, Font size: 9, Colour: #1F2A24, Value decimal places: 1.
- In the Visualizations pane click the paintbrush icon, then click 'Detail labels', then 'Position' and set it to Outside.
- In the Visualizations pane click the paintbrush icon, then click 'Legend', then 'Position' and set it to Bottom center, Font size: 9.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 12, Colour: #14532D.
- If the legend runs to more than about eight natures, Format pane → Legend → Font size: 8 and it still fits; the smallest natures are grouped under Others by the query, so it should not.

---

## Page — Summary

**The panel first.** Go to `Overview`, click the green panel, then hold **Ctrl** and click the logo box, the two heading lines, the two section labels, the three white boxes and all 9 figures on the panel — or draw a selection box around the whole left strip. **Ctrl+C**, come back to `Summary`, **Ctrl+V**. Everything arrives at the same coordinates, so the panel is identical on every page.

Then click the second heading line and change its text from `Overview` to `Summary`, so the panel doubles as the page's name. Nothing else on the panel changes: the nine figures ignore every slicer on every page by design, because they are the latest month's position and they must read the same wherever you are.

The visuals below are what goes to the **right** of the panel, which is why every Horizontal starts at 192 rather than 16.

**4.22** **Slicer** — Tick nothing and the matrix shows the last 4 months under each master column. Tick the months you want and it shows those, up to twelve — tick more than twelve and it keeps the twelve most recent of your ticks, because 3 master columns × 12 months is already 36 columns of figures.

| Well | Field |
|---|---|
| Field | `dimDate[MonthName]` |

Title: `Months (Leave Empty for the Last 4)`

Position: Horizontal 192, Vertical 8, Width 258, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Selection' and set it to switch OFF 'Multi-select with CTRL' so ticking several needs no keyboard.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font size' and set it to 10, Colour: #14532D.

**4.23** **Slicer** — A second, coarser filter: tick Q1 and only that quarter's months are left for the matrices and the charts to show. Leave it empty to see every month.

| Well | Field |
|---|---|
| Field | `dimDate[Quarter]` |

Title: `Quarters (Leave Empty for the Last 4)`

Position: Horizontal 463, Vertical 8, Width 206, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Selection' and set it to switch OFF 'Multi-select with CTRL'.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font size' and set it to 10, Colour: #14532D.

**4.24** **Slicer** — Narrows both matrices to one plant when you want to read it on its own.

| Well | Field |
|---|---|
| Field | `dimPlant[Plant]` |

Title: `Plant`

Position: Horizontal 683, Vertical 8, Width 189, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font size' and set it to 10, Colour: #14532D.

**4.25** **Slicer** — RM, FG or consumables, when you want the reconciliation for one of them only.

| Well | Field |
|---|---|
| Field | `dimCategory[Category]` |

Title: `Type`

Position: Horizontal 886, Vertical 8, Width 179, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font size' and set it to 10, Colour: #14532D.

**4.26** **Matrix** — The whole reconciliation in one grid: three master columns — Inventory (TB), Inventory (MB5B), Difference — with the periods under each, one row per plant (Jaipur Module, Dholera Module, Dholera Cell) opening into RM, FG and Consumables, and a total for each plant. Everything in crore rupees.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]`, `dimCategory[Category]` |
| Columns | `dimMetric[Metric]`, `dimDate[MonthName]` |
| Values | `Summary Value Rs Cr` |
| Filters | `In Summary Window  →  is 1` |

Title: `Inventory (TB) · Inventory (MB5B) · Difference by Plant (Rs Cr.)`

Position: Horizontal 192, Vertical 88, Width 1072, Height 212.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Order of the two Columns fields matters: dimMetric[Metric] FIRST, then dimDate[MonthName]. That is what makes TB / MB5B / Difference the master columns with the months nested inside; the other way round gives you months with three metrics inside each.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Stepped layout' and set it to Off, so Plant and Type get a column each instead of being indented into one.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then '+/- icons' and set it to On — that is the click-to-expand control on each plant.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On, and switch ON 'Per row level' so each plant shows its own total. Column subtotals: Off.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Grand total' and set it to Off on this matrix. The total of the totals, split by RM / FG / Consumables, is the second matrix underneath — a matrix can only give one flat grand total row, so the split has to be its own visual.
- Colour the differences: in the Values box click the small down-arrow next to Summary Value Rs Cr, click 'Conditional formatting', then 'Background color'. Set Format style to Diverging, tick 'Add a middle colour', set the middle number to 0, and make both the Minimum and Maximum colours red. A difference either direction is equally wrong, so both ends are red.
- Right-click any plant row, click 'Expand', then 'All', so RM, FG and Consumables show under every plant. Then press Ctrl+S — Power BI remembers it.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Text' and set it to type the heading above, and leave the fx button alone. The columns are always months, so the heading is always right.
- With twelve periods ticked this is 36 columns of figures, so a scrollbar appears along the bottom of the matrix. That is normal: scroll it sideways, or untick periods until it fits.

**4.27** **Matrix** — The bottom block: the same three master columns, but every plant added together — one row for RM, one for FG, one for Consumables, so you can read total RM across all plants at a glance, and a Total row under them which is the total inventory.

| Well | Field |
|---|---|
| Rows | `dimCategory[Category]` |
| Columns | `dimMetric[Metric]`, `dimDate[MonthName]` |
| Values | `Summary Value Rs Cr` |
| Filters | `In Summary Window  →  is 1` |

Title: `Total Across All Plants by Type (Rs Cr.)`

Position: Horizontal 192, Vertical 308, Width 1072, Height 112.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Same column order as the matrix above: dimMetric[Metric] first, then dimDate[MonthName]. Keep the same months ticked, so the two matrices line up column for column.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Stepped layout' and set it to Off.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On — that bottom row is the total of the totals, the whole inventory. Column subtotals: Off.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Font' and set it to Arial, Font size: 9, Bold: On, so this block reads as the summary of the one above rather than as more detail.
- This matrix has no Plant field on purpose. Leave the Plant slicer on 'All' when you want the across-all-plants figure — picking one plant filters this block too.

**4.28** **Clustered column chart** — The books against the stock report, two bars per period: the same figures as the matrix above, but you can see a gap opening without reading a single number. Same periods as the matrices, because it carries the same filter.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `TB Inventory Rs Cr`, `Inventory Rs Cr` |
| Filters | `In Summary Window  →  is 1` |

Title: `Inventory (TB) vs Inventory (MB5B) by Month (Rs Cr.)`

Position: Horizontal 192, Vertical 428, Width 529, Height 112.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Both measures go in the Y-axis, TB Inventory Rs Cr first — that fixes the order of the two bars, so the books are always the left-hand one.
- In the Visualizations pane click the paintbrush icon, then click 'Data labels' and set it to On, Font: Arial, Font size: 8, Colour: #1F2A24, Display units: None, Value decimal places: 0, Position: Inside end.
- In the Visualizations pane click the paintbrush icon, then click 'Y-axis' and set it to Off. The label on each bar is the number, so a scale up the side only eats the height.
- In the Visualizations pane click the paintbrush icon, then click 'X-axis', then 'Values', then 'Font' and set it to Arial, Font size: 8, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Legend', then 'Position' and set it to Top center, Font: Arial, Font size: 8. Two measures here, so the legend is the only thing naming them — leave it on.
- In the Visualizations pane click the paintbrush icon, then click 'X-axis', then 'Inner padding: 30%, and General', then 'Properties', then 'Padding' and set it to Left 12, Right 12, so the first and last bar keep off the card edges.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 11, Colour: #14532D.

**4.29** **Line and clustered column chart** — The question the reconciliation is really asking: is the gap widening or closing. The bar is the difference in crore rupees, the line above it the same difference as a percentage of the trial balance, so a small gap on a big month reads as small.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Column y-axis | `Difference Inventory Rs Cr` |
| Line y-axis | `Difference Inventory %` |
| Filters | `In Summary Window  →  is 1` |

Title: `Difference by Month (Rs Cr. and % of TB)`

Position: Horizontal 735, Vertical 428, Width 529, Height 112.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- In the Visualizations pane click the paintbrush icon, then click 'Columns', then 'Colour', then 'fx', then 'Format style' and set it to Rules, and colour any value below 0 red. A difference either direction is equally wrong, so red both ways.
- In the Visualizations pane click the paintbrush icon, then click 'Data labels: On. Then 'Apply settings to'', then 'Series' and set it to Difference Inventory Rs Cr — Font: Arial, Font size: 8, Colour: #1F2A24, Display units: None, Value decimal places: 2, Position: Inside end.
- Still under Data labels, switch 'Apply settings to' → Series to Difference Inventory %: Font: Arial, Font size: 8, Colour: #14532D, Value decimal places: 1, Position: Above. Two numbers per period, and they cannot collide.
- In the Visualizations pane click the paintbrush icon, then click 'Y-axis' and set it to Off, Secondary y-axis: Off. Both numbers are printed on the chart already.
- In the Visualizations pane click the paintbrush icon, then click 'X-axis', then 'Values', then 'Font' and set it to Arial, Font size: 8, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Lines', then 'Colour' and set it to #9AA79F, Stroke width: 1, Markers: On, Marker size: 3.
- In the Visualizations pane click the paintbrush icon, then click 'Legend' and set it to Off — the title says which is which, and 144 pixels of height has none to spare.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 11, Colour: #14532D.

**4.30** **Line chart** — The long view under the reconciliation: three lines across the last twelve months that have data, or fewer if that is all there is — raw material days, finished goods days, and the two added together, which is what the Overview card calls Days of inventory (RM + FG). Every month is its own closing figure divided by capacity, so nothing is added across months. Read it for shape: RM climbing while FG is flat means material is arriving faster than it is being consumed.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `RM Days`, `FG Days`, `Total Days (RM + FG)` |
| Filters | `In Last 12  →  is 1` |

Title: `Days of Inventory by Month, Last 12 Months — RM, FG and Total`

Position: Horizontal 192, Vertical 548, Width 1072, Height 156.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- This chart must ignore the period pickers at the top of Summary, or it would drop back to four months. Click the 'Months' slicer, then ribbon Format → Edit interactions, and on this chart click the circle-with-a-line (None). Repeat for the Quarters slicer. Leave Plant and Type filtering, so those two still work on it — picking a plant re-bases all three lines on that plant's capacity.
- In the Visualizations pane click the paintbrush icon, then click 'Data labels: On, Font: Arial, Font size: 8, Bold: On, Colour: #14532D, Display units: None, Value decimal places: 0, Position: Above. Twelve months × three lines is a lot of numbers: if they collide, set Data labels', then 'Apply settings to', then 'Series and switch the Total line's labels off, since it is the sum of the other two'.
- In the Visualizations pane click the paintbrush icon, then click 'Lines', then 'Stroke width: 2, Show marker: On, Marker size: 4. Then Lines', then 'Apply settings to', then 'Series' and set it to RM Days #2E7D46, FG Days #7FBB84, Total Days (RM + FG) #14532D — the total is the darkest, so it reads as the envelope.
- In the Visualizations pane click the paintbrush icon, then click 'Legend', then 'Position' and set it to Top center, Font: Arial, Font size: 9, Colour: #1F2A24. Three series need a key, unlike the single-series charts elsewhere.
- In the Visualizations pane click the paintbrush icon, then click 'Y-axis', then 'Title' and set it to On, Text: 'Days', Font: Arial, Font size: 9, Colour: #1F2A24, Display units: None. A days axis earns its title because the number is a ratio, not rupees.
- In the Visualizations pane click the paintbrush icon, then click 'X-axis', then 'Values', then 'Font' and set it to Arial, Font size: 8, Colour: #1F2A24, Concatenate labels: Off.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 12, Colour: #14532D.
- If a plant has no capacity row in the Variables workbook its days go blank rather than zero, so a gap in a line means missing capacity, not zero stock.
- Right-click a point → Drill through → Detail for the materials behind that month.

---

## Page — FG

**The panel first.** Go to `Overview`, click the green panel, then hold **Ctrl** and click the logo box, the two heading lines, the two section labels, the three white boxes and all 9 figures on the panel — or draw a selection box around the whole left strip. **Ctrl+C**, come back to `FG`, **Ctrl+V**. Everything arrives at the same coordinates, so the panel is identical on every page.

Then click the second heading line and change its text from `Overview` to `FG`, so the panel doubles as the page's name. Nothing else on the panel changes: the nine figures ignore every slicer on every page by design, because they are the latest month's position and they must read the same wherever you are.

The visuals below are what goes to the **right** of the panel, which is why every Horizontal starts at 192 rather than 16.

**4.31** **Slicer** — Which months appear under each master column. Tick nothing and it shows the last four with data; tick your own and it shows those, up to twelve.

| Well | Field |
|---|---|
| Field | `dimDate[MonthName]` |

Title: `Months (Leave Empty for the Last 4)`

Position: Horizontal 192, Vertical 8, Width 258, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Selection', then 'switch OFF 'Multi-select with CTRL', so months can be ticked by clicking'.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.
- Do not sync this one either. Both FG matrices read it, and nothing else should.

**4.32** **Slicer** — A coarser filter over the same months: tick Q1 and only April, May and June are left for the two matrices to show. Leave it empty to see every month.

| Well | Field |
|---|---|
| Field | `dimDate[Quarter]` |

Title: `Quarters (Leave Empty for the Last 4)`

Position: Horizontal 463, Vertical 8, Width 206, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Selection', then ''Multi-select with CTRL'' and set it to Off.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.
- It filters the months rather than replacing them, so the columns stay months.

**4.33** **Slicer** — One plant, or all of them. It filters the technology matrix and all three charts, so picking Dholera Cell turns the page into a Dholera Cell page.

| Well | Field |
|---|---|
| Field | `dimPlant[Plant]` |

Title: `Plant`

Position: Horizontal 683, Vertical 8, Width 189, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.

**4.34** **Slicer** — One module technology, when you want the page to be about that technology only.

| Well | Field |
|---|---|
| Field | `dimNature[Nature]` |

Title: `Technology`

Position: Horizontal 886, Vertical 8, Width 179, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.

**4.35** **Matrix** — Finished goods per plant in all three units at once — megawatts, crore rupees and days — with four periods under each of the three master columns by default. Days is MW ÷ capacity MW, so a plant with no capacity figure is blank on purpose.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]` |
| Columns | `dimMeasure[Measure]`, `dimDate[MonthName]` |
| Values | `Unit Value by Period` |
| Filters | `dimCategory[Category]  →  is FG`, `In Summary Window  →  is 1` |

Title: `FG by Plant — MW · Rs Cr. · Days`

Position: Horizontal 192, Vertical 88, Width 1072, Height 140.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- dimMeasure[Measure] goes in Columns FIRST, then dimDate[MonthName]. That order is what makes MW, Rs Cr. and Days the master columns with the periods nested inside them; the other way round gives you periods with three units inside each, which is not what you want.
- Values takes Unit Value by Period, not Unit Value. They are the same figure in a month column; the difference is the Total column, where the by-Period one averages the month-ends instead of adding them, because stock is a level.
- Filters pane → drag dimCategory[Category] in → tick FG only. Then drag the measure In Summary Window in and set 'is 1' — that is what limits it to four periods, or to the ones you tick, up to twelve.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Stepped layout' and set it to Off, +/- icons: On.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On, Column subtotals: Off.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24. Everything else comes from the theme.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 12, Colour: #14532D.
- Click a plant row and the technology matrix and the charts below follow it.
- With twelve periods ticked this is 36 number columns, so the matrix scrolls sideways. That is normal — scroll inside it, do not widen it.

**4.36** **Matrix** — Exactly the same three master columns and the same periods, but by module technology rather than by plant — which is where a build-up in one technology shows up.

| Well | Field |
|---|---|
| Rows | `dimNature[Nature]` |
| Columns | `dimMeasure[Measure]`, `dimDate[MonthName]` |
| Values | `Unit Value by Period` |
| Filters | `dimCategory[Category]  →  is FG`, `In Summary Window  →  is 1` |

Title: `FG by Technology — MW · Rs Cr. · Days`

Position: Horizontal 192, Vertical 236, Width 1072, Height 252.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Build it the fastest way: click the matrix above, Ctrl+C, Ctrl+V, then in the Rows box remove dimPlant[Plant] and drag dimNature[Nature] in. Everything else, filters included, comes with the copy.
- Then set its position and size from the numbers below, and retype the title.
- Check the filters came across: the Filters pane should still show Category is FG and In Summary Window is 1.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Stepped layout' and set it to Off.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On, Column subtotals: Off.
- With the Plant slicer on one plant, this becomes that plant's technology split.

**4.37** **Clustered column chart** — Which technology is holding the megawatts right now. It is deliberately pinned to the latest month with data: there is no period on the axis here, so without that pin it would add four months of stock together and read four times too high.

| Well | Field |
|---|---|
| X-axis | `dimNature[Nature]` |
| Y-axis | `MW` |
| Filters | `dimCategory[Category]  →  is FG`, `In Latest Month  →  is 1` |

Title: `FG MW by Technology, Latest Month — Click a Bar`

Position: Horizontal 192, Vertical 496, Width 354, Height 208.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag In Latest Month in → is 1. Do not skip it, and do not put a period field on this chart.
- In the Visualizations pane click the paintbrush icon, then click 'Data labels' and set it to On, Font: Arial, Font size: 9, Colour: #1F2A24, Display units: None, Value decimal places: 1.
- In the Visualizations pane click the paintbrush icon, then click 'Y-axis' and set it to Off — the label on each bar is the number.
- In the Visualizations pane click the paintbrush icon, then click 'X-axis', then 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Legend' and set it to Off. One measure, one colour.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 11, Colour: #14532D.
- Clicking a bar filters both matrices to that technology; right-click → Drill through → Detail for the materials behind it.

**4.38** **Line and clustered column chart** — How long the finished goods on hand would last, month by month, with the change on last month printed above each bar — so a slow build-up is visible before it becomes a number anyone argues about.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Column y-axis | `Days` |
| Line y-axis | `Days vs LM` |
| Filters | `dimCategory[Category]  →  is FG`, `In Last 12  →  is 1` |

Title: `FG Days of Inventory by Month, Last 12 Months (Days and % vs Last Month)`

Position: Horizontal 560, Vertical 496, Width 368, Height 208.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag In Last 12 in → is 1, so this always shows the last twelve months whatever the pickers above say.
- This chart must ignore the two period pickers, or it drops back to four months: click the Months slicer → Format tab → Edit interactions → set this chart to None (the circle-with-a-line icon). Do the same after clicking the Quarters slicer.
- In the Visualizations pane click the paintbrush icon, then click 'Data labels: On. 'Apply settings to'', then 'Series' and set it to Days — Font: Arial, Font size: 8, Colour: #1F2A24, Value decimal places: 0, Position: Inside end.
- Switch 'Apply settings to' → Series to Days vs LM: Font: Arial, Font size: 8, Colour: #14532D, Value decimal places: 0, Position: Above.
- In the Visualizations pane click the paintbrush icon, then click 'Y-axis' and set it to Off, Secondary y-axis: Off.
- In the Visualizations pane click the paintbrush icon, then click 'X-axis', then 'Values', then 'Font' and set it to Arial, Font size: 8, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Legend' and set it to Off — the title says which is which.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 11, Colour: #14532D.
- Right-click any bar → Drill through → Detail for the split behind that month.

**4.39** **Donut chart** — Where the finished goods are sitting, as a share of the whole. Pinned to the latest month for the same reason as the bar chart: a share of four added-up months would mean nothing.

| Well | Field |
|---|---|
| Legend | `dimPlant[Plant]` |
| Values | `FG ₹ Cr` |
| Filters | `In Latest Month  →  is 1` |

Title: `FG Share by Plant (%), Latest Month`

Position: Horizontal 941, Vertical 496, Width 323, Height 208.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Detail labels' and set Font size to 9. If a slice label is still cut off, set 'Position' to Outside, and switch on 'Overflow text' if your version offers it.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'. If the legend eats the chart, switch Legend off entirely — the labels already name the slices.
- Filters pane → drag In Latest Month in → is 1.
- In the Visualizations pane click the paintbrush icon, then click 'Detail labels', then 'Label contents' and set it to Category, percent of total. Font: Arial, Font size: 9, Colour: #1F2A24, Percentage decimal places: 1 — so the percentage is printed on each slice and nobody has to hover.
- In the Visualizations pane click the paintbrush icon, then click 'Legend' and set it to Off. The slice labels already name the plants.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 11, Colour: #14532D.
- Clicking a slice filters the rest of the page to that plant; clicking it again releases it.

---

## Page — RM

**The panel first.** Go to `Overview`, click the green panel, then hold **Ctrl** and click the logo box, the two heading lines, the two section labels, the three white boxes and all 9 figures on the panel — or draw a selection box around the whole left strip. **Ctrl+C**, come back to `RM`, **Ctrl+V**. Everything arrives at the same coordinates, so the panel is identical on every page.

Then click the second heading line and change its text from `Overview` to `RM`, so the panel doubles as the page's name. Nothing else on the panel changes: the nine figures ignore every slicer on every page by design, because they are the latest month's position and they must read the same wherever you are.

The visuals below are what goes to the **right** of the panel, which is why every Horizontal starts at 192 rather than 16.

**4.40** **Slicer** — Which months appear under each master column, and on both charts along the bottom. Nothing ticked means the last four with data; tick your own for up to twelve.

| Well | Field |
|---|---|
| Field | `dimDate[MonthName]` |

Title: `Months (Leave Empty for the Last 4)`

Position: Horizontal 192, Vertical 8, Width 258, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Selection', then ''Multi-select with CTRL'' and set it to Off.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.

**4.41** **Slicer** — The quarter-mode equivalent: empty means the last four fiscal quarters.

| Well | Field |
|---|---|
| Field | `dimDate[Quarter]` |

Title: `Quarters (Leave Empty for the Last 4)`

Position: Horizontal 463, Vertical 8, Width 206, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Selection', then ''Multi-select with CTRL'' and set it to Off.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.

**4.42** **Slicer** — One plant, or all three.

| Well | Field |
|---|---|
| Field | `dimPlant[Plant]` |

Title: `Plant`

Position: Horizontal 683, Vertical 8, Width 189, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.

**4.43** **Slicer** — Module or Cell, when you want the page to be about one of the two only — the same split the Excel sheet had as its Module and Cell blocks.

| Well | Field |
|---|---|
| Field | `factInventory[GroupNature]` |

Title: `Group Nature`

Position: Horizontal 886, Vertical 8, Width 179, Height 76.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Filters pane → drag the same field into this visual's own Filters box → Filter type: Advanced filtering → 'is not blank' → Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.
- In the Visualizations pane click the paintbrush icon, then click 'Slicer settings', then 'Options', then 'Style' and set it to Dropdown.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.

**4.44** **Matrix** — The top block of the old RM sheet, rebuilt: one row per plant, with Rs Cr. and Days as master columns and the periods under each. MW is unticked because an RM megawatt figure is derived from a BOM, not measured, so it does not belong beside the other two.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]` |
| Columns | `dimMeasure[Measure]`, `dimDate[MonthName]` |
| Values | `Unit Value by Period` |
| Filters | `dimCategory[Category]  →  is RM`, `dimMeasure[Measure]  →  untick MW`, `In Summary Window  →  is 1` |

Title: `RM Inventory by Plant — Rs Cr. · Days`

Position: Horizontal 192, Vertical 88, Width 1072, Height 140.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- dimMeasure[Measure] goes in Columns FIRST, then dimDate[MonthName] — that order is what makes Rs Cr. and Days the master columns.
- Filters pane → dimCategory[Category] → tick RM only; then drag dimMeasure[Measure] in and untick MW so only Rs Cr. and Days remain; then drag In Summary Window in and set 'is 1' for the four-periods-by-default behaviour.
- Values takes Unit Value by Period — in the Total column the plain Unit Value would add the month-ends together instead of averaging them.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Stepped layout' and set it to Off.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On (that is the Grand Total row the Excel sheet had), Column subtotals: Off.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 12, Colour: #14532D.
- Clicking a plant row filters the material matrix and both charts below it.

**4.45** **Matrix** — The second block of the old sheet: Module and Cell, each opening into its materials — cell cost, frame, glass, POE, wafer, paste, screens, gases and the rest — in the same two units and the same periods, with a subtotal on each group and a grand total under them.

| Well | Field |
|---|---|
| Rows | `factInventory[GroupNature]`, `dimNature[Nature]` |
| Columns | `dimMeasure[Measure]`, `dimDate[MonthName]` |
| Values | `Unit Value by Period` |
| Filters | `dimCategory[Category]  →  is RM`, `dimMeasure[Measure]  →  untick MW`, `In Summary Window  →  is 1` |

Title: `RM Inventory by Group Nature and Nature — Rs Cr. · Days`

Position: Horizontal 192, Vertical 236, Width 1072, Height 252.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Fastest way: click the matrix above, Ctrl+C, Ctrl+V, then drop factInventory[GroupNature] and dimNature[Nature] into Rows and remove dimPlant[Plant]. The three filters come with the copy.
- Then set its position and size from the numbers below, and retype the title.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Stepped layout' and set it to Off, +/- icons: On. Group Nature and Nature then sit in two columns with an expander on each group row.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On, and switch 'Per row level' On so both the Total Module and Total Cell lines appear, not only the grand total.
- Right-click a material row → Drill through → Detail for the material-by-material list behind it.

**4.46** **Clustered column chart** — Raw material held in crore rupees: one group per period along the bottom and the three plants side by side inside each group, so you read the months left to right and compare the plants within a month. It follows the pickers above, so it is four periods by default and up to twelve if you tick them.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Legend | `dimPlant[Plant]` |
| Y-axis | `Inventory Rs Cr` |
| Filters | `dimCategory[Category]  →  is RM`, `In Summary Window  →  is 1` |

Title: `RM Inventory (Rs Cr.) by Plant`

Position: Horizontal 192, Vertical 496, Width 529, Height 208.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- dimDate[MonthName] goes in the X-axis and dimPlant[Plant] in Legend — that order is what gives three bars per month rather than four bars per plant.
- In the Visualizations pane click the paintbrush icon, then click 'Data labels' and set it to On, Font: Arial, Font size: 8, Bold: On, Colour: #FFFFFF, Display units: None, Value decimal places: 0, Position: Inside end.
- In the Visualizations pane click the paintbrush icon, then click 'Legend', then 'Position' and set it to Top center, Font: Arial, Font size: 8. Keep it on: it is the only thing naming the plants.
- In the Visualizations pane click the paintbrush icon, then click 'Y-axis' and set it to Off — every bar is labelled, so the scale would only eat width.
- In the Visualizations pane click the paintbrush icon, then click 'X-axis', then 'Values', then 'Font' and set it to Arial, Font size: 8, Colour: #1F2A24, Concatenate labels: Off.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 12, Colour: #14532D.
- Clicking one plant's bar filters both matrices to that plant and that period.

**4.47** **Line and clustered column chart** — The same chart in days rather than rupees — how long each plant's raw material would last at its own capacity, three plant bars per month, and over them a line for the whole business: every plant's RM megawatts added together over every plant's capacity added together. The line is not the average of the three bars, and it is not their sum: it is one big plant's worth of days, which is the figure to quote for the company. Read together with the chart beside it, this tells you whether a bigger rupee figure is actually more stock or just a dearer month.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Column legend | `dimPlant[Plant]` |
| Column y-axis | `Days by Period` |
| Line y-axis | `RM Days All Plants by Period` |
| Filters | `dimCategory[Category]  →  is RM`, `In Summary Window  →  is 1` |

Title: `RM Inventory (Days) by Plant, with Total Days Across All Plants`

Position: Horizontal 735, Vertical 496, Width 529, Height 208.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- The line comes from RM Days All Plants by Period, which strips the plant filter off both the megawatts and the capacity, so a bar can be tall while the line is calm.
- Use Days by Period for the bars, not Days. Days is a ratio, so a total column has to average the three month-ends rather than add them, and that is the only difference between the two measures.
- In the Visualizations pane click the paintbrush icon, then click 'Data labels' and set it to On, Font: Arial, Font size: 8, Bold: On, Colour: #FFFFFF, Display units: None, Value decimal places: 0, Position: Inside end.
- Data labels → Apply settings to → Series → RM Days All Plants by Period: Font: Arial, Font size: 8, Bold: On, Colour: #14532D, Value decimal places: 0, Position: Above — dark green on the white card, because this label is not printed on a bar.
- In the Visualizations pane click the paintbrush icon, then click 'Lines', then 'Colour: #14532D, Stroke width: 2, Show marker: On, Marker size: 4. Format pane', then 'Lines', then 'Smooth line' and set it to Off, so the shape is honest.
- In the Visualizations pane click the paintbrush icon, then click 'Legend', then 'Position' and set it to Top center, Font: Arial, Font size: 8. The line appears in the legend as 'RM Days All Plants by Period' — rename it if you like by double-clicking the field in the well and typing 'Total (All Plants)'.
- In the Visualizations pane click the paintbrush icon, then click 'Y-axis' and set it to Off, and Secondary y-axis: Off. Bars and line are both in days on the same scale, so leave 'Align zeros' On if you switch either axis back on, or the line will sit at a misleading height.
- In the Visualizations pane click the paintbrush icon, then click 'X-axis', then 'Values', then 'Font' and set it to Arial, Font size: 8, Colour: #1F2A24, Concatenate labels: Off.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 12, Colour: #14532D.
- A plant with no capacity row in the Variables workbook shows blank here, not zero — that is deliberate, a missing denominator is not the same as no stock.

---

## Page — Detail

**The panel first.** Go to `Overview`, click the green panel, then hold **Ctrl** and click the logo box, the two heading lines, the two section labels, the three white boxes and all 9 figures on the panel — or draw a selection box around the whole left strip. **Ctrl+C**, come back to `Detail`, **Ctrl+V**. Everything arrives at the same coordinates, so the panel is identical on every page.

Then click the second heading line and change its text from `Overview` to `Detail`, so the panel doubles as the page's name. Nothing else on the panel changes: the nine figures ignore every slicer on every page by design, because they are the latest month's position and they must read the same wherever you are.

The visuals below are what goes to the **right** of the panel, which is why every Horizontal starts at 192 rather than 16.

**4.48** **Card** — The drill-through page opens already filtered to the bar or row you came from, so this card is that one number.

| Well | Field |
|---|---|
| Fields | `Value ₹ Cr` |

Title: `Value ₹ Cr of What You Clicked`

Position: Horizontal 192, Vertical 16, Width 254, Height 96.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.

**4.49** **Card** — Same slice in megawatts.

| Well | Field |
|---|---|
| Fields | `MW` |

Title: `MW`

Position: Horizontal 453, Vertical 16, Width 254, Height 96.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.

**4.50** **Card** — Stock in MW divided by the MW capacity on the Variables sheet. With no category picked that MW is RM plus FG over the same capacity, so the two add up — the title says so rather than leaving a reader to assume it means FG alone. Blank where the plant has no capacity row — 1905.

| Well | Field |
|---|---|
| Fields | `Days of Inventory` |

Title: `Days of Inventory (RM + FG)`

Position: Horizontal 714, Vertical 16, Width 254, Height 96.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.

**4.51** **Card** — How big this slice is against the whole.

| Well | Field |
|---|---|
| Fields | `Share of Total %` |

Title: `Share of the Total`

Position: Horizontal 975, Vertical 16, Width 289, Height 96.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.

**4.52** **Pie chart** — RM / FG / consumables for exactly what you clicked.

| Well | Field |
|---|---|
| Legend | `dimCategory[Category]` |
| Values | `Value ₹ Cr` |

Title: `Split by Category`

Position: Horizontal 192, Vertical 120, Width 347, Height 232.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Detail labels' and set Font size to 9. If a slice label is still cut off, set 'Position' to Outside, and switch on 'Overflow text' if your version offers it.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'. If the legend eats the chart, switch Legend off entirely — the labels already name the slices.
- In the Visualizations pane click the paintbrush icon, then click 'Detail labels', then 'Label contents' and set it to Category, percent of total.

**4.53** **Donut chart** — Which technology or material nature the slice is made of.

| Well | Field |
|---|---|
| Legend | `dimNature[Nature]` |
| Values | `Value ₹ Cr` |

Title: `Split by Technology / Nature`

Position: Horizontal 546, Vertical 120, Width 347, Height 232.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Detail labels' and set Font size to 9. If a slice label is still cut off, set 'Position' to Outside, and switch on 'Overflow text' if your version offers it.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'. If the legend eats the chart, switch Legend off entirely — the labels already name the slices.
- In the Visualizations pane click the paintbrush icon, then click 'Detail labels', then 'Label contents' and set it to Category, percent of total.

**4.54** **Pie chart** — Where the slice sits. A single-colour pie means it is one plant already.

| Well | Field |
|---|---|
| Legend | `dimPlant[Plant]` |
| Values | `Value ₹ Cr` |

Title: `Split by Plant`

Position: Horizontal 900, Vertical 120, Width 364, Height 232.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Detail labels' and set Font size to 9. If a slice label is still cut off, set 'Position' to Outside, and switch on 'Overflow text' if your version offers it.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'. If the legend eats the chart, switch Legend off entirely — the labels already name the slices.
- In the Visualizations pane click the paintbrush icon, then click 'Detail labels', then 'Label contents' and set it to Category, percent of total.

**4.55** **Matrix** — The line-item detail. A Matrix rather than a Table, so it opens nature → material instead of being one long flat list — that is the difference between clicking and scrolling.

| Well | Field |
|---|---|
| Rows | `dimNature[Nature]`, `factInventory[Material]`, `factInventory[MaterialDesc]` |
| Values | `Value ₹ Cr`, `MW`, `Days`, `INR per Wp`, `Share of Total %` |

Title: `Materials Behind This Number — Click + to Open a Nature`

Position: Horizontal 192, Vertical 364, Width 1072, Height 348.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then '+/- icons' and set it to On, Stepped layout: Off. That is the click-to-open control.
- In the Visualizations pane click the paintbrush icon, then click 'Grid', then 'Options', then 'Keep column headers visible' and set it to On. The headings then stay put while the rows scroll inside the visual, so a long list never makes the visual (or the page) grow.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On, so a closed nature row still shows its total.
- Click the Value ₹ Cr column header once so it sorts largest first.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Text size' and set it to 9 and Row padding: 1. At 348 high that is about eighteen rows on screen at once, roughly twice what the default padding allows.
- How to scroll it: put the mouse pointer inside the matrix, not on the page around it, and use the wheel — the scrollbar is hidden until the pointer is over the visual. Two-finger drag on a trackpad does the same.
- If the wheel still does nothing, the page itself is being scrolled instead: ribbon View → Page view → Fit to page, so the whole canvas is on screen and the wheel belongs to the visual under the pointer.
- For a really long list use Focus mode — hover the visual, click the diagonal-arrows icon in its top-right, and it fills the page with far more rows visible; the back arrow returns you. Or collapse a nature with its − icon to jump past it.

---

## Page — Checks

**The panel first.** Go to `Overview`, click the green panel, then hold **Ctrl** and click the logo box, the two heading lines, the two section labels, the three white boxes and all 9 figures on the panel — or draw a selection box around the whole left strip. **Ctrl+C**, come back to `Checks`, **Ctrl+V**. Everything arrives at the same coordinates, so the panel is identical on every page.

Then click the second heading line and change its text from `Overview` to `Checks`, so the panel doubles as the page's name. Nothing else on the panel changes: the nine figures ignore every slicer on every page by design, because they are the latest month's position and they must read the same wherever you are.

The visuals below are what goes to the **right** of the panel, which is why every Horizontal starts at 192 rather than 16.

**4.56** **Card** — How many rows came out of RM Raw, FG Raw and Consble Raw together. Zero means pRoot is wrong or the three folders are named differently.

| Well | Field |
|---|---|
| Fields | `Check MB5B Rows` |

Title: `Stock Rows Loaded`

Position: Horizontal 192, Vertical 56, Width 206, Height 88.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Font' and set it to Arial, Font size: 14, Colour: #14532D.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to #FFFFFF.

**4.57** **Card** — Zero here is the reason Inventory (TB) reads as empty on Summary: either the TB folder has no TB_YYYYMM.xlsx files, or the GL numbers in them match nothing on TB Master.

| Well | Field |
|---|---|
| Fields | `Check TB Rows` |

Title: `Trial Balance Rows Loaded`

Position: Horizontal 405, Vertical 56, Width 206, Height 88.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Font' and set it to Arial, Font size: 14, Colour: #14532D.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to #FFFFFF.

**4.58** **Card** — How many month-ends the stock files cover. One month means only one file was read, and then every monthly chart has a single bar however it is built.

| Well | Field |
|---|---|
| Fields | `Check Months of Data` |

Title: `Months of Data`

Position: Horizontal 618, Vertical 56, Width 206, Height 88.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Font' and set it to Arial, Font size: 14, Colour: #14532D.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to #FFFFFF.

**4.59** **Card** — More than three means the stock files carry a valuation area beyond the three plants; those now appear as 'Plant xxxx' rather than as a blank row.

| Well | Field |
|---|---|
| Fields | `Check Plant Codes` |

Title: `Plant Codes in the Data`

Position: Horizontal 831, Vertical 56, Width 206, Height 88.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Font' and set it to Arial, Font size: 14, Colour: #14532D.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to #FFFFFF.

**4.60** **Card** — The share of stock rows the master sheets do not cover. Anything above zero is what shows up as an Unassigned slice on the donuts and an Unassigned row in the technology matrix — the material numbers differ between the master sheet and the raw files.

| Well | Field |
|---|---|
| Fields | `Check Unassigned %` |

Title: `Rows with No Nature (%)`

Position: Horizontal 1044, Vertical 56, Width 220, Height 88.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Font' and set it to Arial, Font size: 14, Colour: #B3261E.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to #FFFFFF.

**4.61** **Table** — One row per file actually read. If a month is missing from the report, it is missing from this list first — check the file is in the folder and is a real .xlsx.

| Well | Field |
|---|---|
| Columns | `qcHeaders[Folder]`, `qcHeaders[Name]`, `qcHeaders[SheetNames]` |

Title: `Every File the Four Folders Gave, with Its Sheets`

Position: Horizontal 192, Vertical 160, Width 533, Height 264.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 9, Colour: #14532D.

**4.62** **Table** — The workbook that carries RM Nature, FG Master, TB Master, Constants and MW. A sheet missing from this list, or showing 0 rows, is why the natures or the trial balance are empty.

| Well | Field |
|---|---|
| Columns | `qcVarHeaders[SheetName]`, `qcVarHeaders[DataRows]` |

Title: `Sheets Found in Variables and Calculations`

Position: Horizontal 731, Vertical 160, Width 533, Height 264.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 9, Colour: #14532D.

**4.63** **Table** — Empty is good. A long list here with 0 trial-balance rows above means TB Master is not matching your GL numbers at all, and the report is showing the whole trial balance rather than the inventory accounts.

| Well | Field |
|---|---|
| Columns | `factTB_Unmapped[GLAccount]`, `factTB_Unmapped[GLDesc]`, `factTB_Unmapped[Amount]` |

Title: `GL Accounts in the TB Files That TB Master Does Not List`

Position: Horizontal 192, Vertical 432, Width 533, Height 264.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 9, Colour: #14532D.

**4.64** **Table** — Each of these gets blank Days, because days of inventory divides by capacity. Add the technology to the MW sheet and it fills in by itself.

| Well | Field |
|---|---|
| Columns | `qcNatureNoCapacity[Nature]` |

Title: `FG Technologies with No Capacity on the MW Sheet`

Position: Horizontal 731, Vertical 432, Width 533, Height 264.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 9, Colour: #14532D.

---

## Making it clickable

**4.65 Drill through.** On the `Detail` page click the empty area around the visuals so
nothing is selected, then drag these into the **Drill through** well of the
Visualizations pane (leave *Keep all filters* on):

- `dimPlant[Plant]`
- `dimDate[MonthName]`
- `dimCategory[Category]`
- `dimNature[Nature]`

That is the whole trick. A **Back** arrow appears on `Detail` by itself, and every bar,
row and slice on the other pages now offers **right-click → Drill through → `Detail`**,
which opens the pies filtered to whatever was clicked.

**4.66 Interactions.** A *left*-click needs no setup — it already cross-filters the rest
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

# PART 6 — Every error we have hit, and its one-line fix

Find the words Power BI showed you in the left column.

| What Power BI says | What is actually wrong | Fix |
|---|---|---|
| `Not enough elements in the enumeration to complete the operation` | a query expected more columns than the sheet has | you are on an old copy of that query — refresh the guide page and re-copy it |
| `could not find a row in the MW sheet containing at least two of 1900, 1902, 1905` | the MW sheet is in the effective-dated layout, not the wide one | re-copy `varMWCapacity`; the current one reads both layouts. Paste `qcMWSheet` to see the sheet raw |
| `Column 'GL Account Number' of the table wasn't found` | your TB export spells the header differently | re-copy `factTB_Staged`; it matches headers loosely and leaves a column blank rather than failing |
| `The Column Month in the table dimDate contains duplicate value` | you are on the old daily `dimDate` | re-copy `dimDate` (it is monthly now), Close & Apply, then make the relationship |
| `Mark as date table` will not accept any column | nothing is wrong | skip 2.4 entirely; a monthly table is deliberate and no measure needs it |
| `dimMetric cannot find table` | `dimCategory` / `dimMetric` / `dimMeasure` were never created | paste those three queries, Close & Apply, then paste the measure again |
| `Value ₹ Cr cannot be determined. Either the column does not exist, or there is no current row` | either `factInventory` has no `CloseVal` column, or you pasted measures out of order | check `CloseVal` exists in `factInventory`; if it does, paste Appendix B again strictly top to bottom |
| searching `Value` in the Data pane finds nothing | Part 3 was done from an older guide, so the measure is called `Closing Value` | add all 75 from Appendix B, then delete the six old names listed in 3.7 |
| RM and FG matrices show numbers under `In ₹ Cr` but nothing under `In Days` | the `Days` measure was deleted as an "old name" | paste `Days = [Days of Inventory]` back in; it is in Appendix B |
| on a card, the number is fine but the wording is cut in half | the card's default text is too big for the space | set **Callout value** → Font size **24**, **General → Title** → Font size **12**, and Height **96** (every card in Part 4 is 96 high). A **Category label**, if your version has one, goes to **10** or off — the title says the same thing |
| the paintbrush list has a **Callout value** but no **Category label** | you are on the newer Card visual, which has no category label | nothing to fix: the heading comes from **General → Title → Text**, which Part 4 gives you the wording for |
| a measure exists but is named `Value  Cr` | the ₹ character was lost while pasting | right-click → Rename, type the name again |
| `There is already a measure with the name …`, and it names a table such as `dimMetric` | you have already pasted that measure — Power BI filed it under whichever table happened to be selected at the time, which changes nothing about how it works | press Escape to cancel, tick that measure off your list and move to the next one. To be sure of the formula, click the existing measure and compare the formula bar with the guide, overwriting it only if it differs. Never let a second copy be made: `Receipts ₹ Cr 2` is not a name any visual looks for |
| `The file is being used by another process` | an Excel file in the folders is open | close all Excel, end any stray `EXCEL.EXE` in Task Manager, delete any `~$...xlsx` file |
| `We couldn't find folder` | `pRoot` is wrong | copy the path from the File Explorer address bar; keep the quote marks, no trailing backslash |
| `Token Literal expected` | `pRoot` lost its quote marks | it must read `"C:\…\Inventory Report"`, quotes included |
| `Expression.Syntax Error` right after pasting | the whole appendix went into one query | one Blank Query per heading, 31 times |
| the report has no **Data** or **Fields** pane | the pane is collapsed, or you are in the Power Query window | ribbon **View** → **Show panes**, or click the `>` at the right edge. Power Query has no such pane — Close & Apply first |
| there is no **Card** button on the Insert ribbon | cards are not on the ribbon | they live in the **Visualizations** pane on the right; Card is the icon showing `123`. Ignore "New visual" and "More visuals" |
| there is no **Format page** | it is a pane, not a page | select a visual, then click the **paintbrush** icon in the Visualizations pane |
| the materials list will not open up | it is a Table visual, which cannot expand | it must be a **Matrix** with `Nature`, `Material`, `MaterialDesc` in **Rows** — see the Detail page steps |
| every row of Summary shows the same number | the two `dimCategory` relationships are missing | add `dimCategory[Category]` → `factInventory[Category]` and → `factTB[Category]` |
| the Summary matrix is completely blank | `dimMetric` has been connected to something | delete every relationship on `dimMetric` and `dimMeasure`; they must stay disconnected |
| months read Apr, Aug, Dec… | `MonthName` is not sorted by `MonthSort` | do 2.5 |
| Difference is a big number, not 0.00 | a source file for that month is missing, duplicated, or was hand-edited | check the four folders have exactly one file each for that month |
| `1905` shows blank Days | correct behaviour | it has no capacity row on the MW sheet; `qcNatureNoCapacity` lists any others |
| `Drill through` is greyed out | the four fields are not in the Drill through box | do the drill-through step on the Detail page |

If a message is not in this table, send me the exact wording — including the name in
quotes, which is the part that says what Power BI could not find.

---

# Already part-built? Bring an older model up to date

If you built some of this before, do these four things once and you are level with the guide.
Nothing here is destructive.

1. **Queries.** Walk the 31 names in 1.3 against your Queries list. For a name you have,
   open **Advanced Editor**, Ctrl+A, paste the appendix version over it, **Done** — harmless
   even when nothing changed. For a name you do not have, create it. The ones most likely
   missing or stale: `dimDate`, `factInventory`, `factTB`, `factTB_Staged`, `varMWCapacity`,
   `dimCategory`, `dimMetric`, `dimMeasure`. Then **Close & Apply**.
2. **Relationships.** Manage relationships must match 2.3 exactly — 11 rows, all Single,
   nothing on `dimMetric` or `dimMeasure`.
3. **Measures.** Add all 75 from Appendix B top to bottom (adding beside old ones is safe),
   then delete the six old names in 3.7 — keeping `Days`, whose formula you overwrite instead.
4. **Sorting.** Set the five sort-by columns in 2.5 and 2.6.

Then run the Part 3 checkpoint above. If it passes, Part 4 will not surprise you.

---

# Monthly routine, once it's live

1. Drop the new MB5B exports into the three Raw folders.
2. Drop the new TB in as `TB_YYYYMM.xlsx`.
3. Add any new materials to `RM Nature` / `FG Master`.
4. If capacity or a constant changed, add a **new row** with the effective date.
5. Open the .pbix → **Refresh**. Check Summary: the Difference column should stay at 0.00.

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
    Slim     = Table.SelectColumns(Typed, {"MatKey","Material","Nature","GroupNature","BOMStdQty","Item"}),
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
    Slim     = Table.SelectColumns(MatKey, {"MatKey","Material","Nature"}),
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

    // Second pass on the material alone. Plant and material together is the safer key, but
    // it misses every row when the master sheet has no valuation area column, or records the
    // plant differently from the MB5B export -- and then nothing has a nature at all.
    ByMat    = Table.Buffer(Table.Distinct(Table.SelectColumns(dimMaterialAttr,
                   {"Material","Nature","GroupNature","BOMStdQty","Item"}), {"Material"})),
    Second   = Table.NestedJoin(Expanded, {"Material"}, ByMat, {"Material"},
                   "attr2", JoinKind.LeftOuter),
    Both     = Table.ExpandTableColumn(Second, "attr2",
                   {"Nature","GroupNature","BOMStdQty","Item"},
                   {"Nature2","GroupNature2","BOMStdQty2","Item2"}),
    Coal     = Table.AddColumn(Both, "NatureX", each [Nature] ?? [Nature2], type text),
    Coal2    = Table.AddColumn(Coal, "GroupNatureX",
                   each [GroupNature] ?? [GroupNature2], type text),
    Coal3    = Table.AddColumn(Coal2, "BOMStdQtyX",
                   each [BOMStdQty] ?? [BOMStdQty2], type number),
    Coal4    = Table.AddColumn(Coal3, "ItemX", each [Item] ?? [Item2], type text),
    Dropped  = Table.RemoveColumns(Coal4, {"Nature","Nature2","GroupNature","GroupNature2",
                   "BOMStdQty","BOMStdQty2","Item","Item2"}),
    Attr     = Table.RenameColumns(Dropped, {{"NatureX","Nature"},
                   {"GroupNatureX","GroupNature"}, {"BOMStdQtyX","BOMStdQty"},
                   {"ItemX","Item"}}),

    Flag     = Table.AddColumn(Attr, "AttrMissing",
                   each [Nature] = null, type logical),
    // a row the master sheet does not cover is named rather than left null: a donut slice
    // reading Unassigned tells you there is work to do, one reading (Blank) tells you nothing
    Named    = Table.TransformColumns(Flag, {
                   {"Nature",      each if _ = null or _ = "" then "Unassigned" else _, type text},
                   {"GroupNature", each if _ = null or _ = "" then "Unassigned" else _, type text}}),
    // RM MW = Closing Stock / BOM Std Qty * RM_MW_FACTOR / 10^6
    // (the 580 you had hardcoded, now read from the Constants sheet)
    MW       = Table.AddColumn(Named, "MW", each
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

    // Same second pass as factRM: the material on its own, for rows the plant-qualified
    // key missed because the FG Master sheet has no valuation area or writes it differently.
    ByMat    = Table.Buffer(Table.Distinct(Table.SelectColumns(dimFGAttr,
                   {"Material","Nature"}), {"Material"})),
    Second   = Table.NestedJoin(Expanded, {"Material"}, ByMat, {"Material"},
                   "attr2", JoinKind.LeftOuter),
    Both     = Table.ExpandTableColumn(Second, "attr2", {"Nature"}, {"Nature2"}),
    Coal     = Table.AddColumn(Both, "NatureX", each [Nature] ?? [Nature2], type text),
    Dropped  = Table.RemoveColumns(Coal, {"Nature","Nature2"}),
    Attr     = Table.RenameColumns(Dropped, {{"NatureX","Nature"}}),

    Flag     = Table.AddColumn(Attr, "AttrMissing", each [Nature] = null, type logical),
    // same as factRM: an FG whose technology the FG Master does not carry is called
    // Unassigned, so the technology matrix and the donut show it instead of a blank row
    Named    = Table.TransformColumns(Flag, {
                   {"Nature", each if _ = null or _ = "" then "Unassigned" else _, type text}}),

    // Rate = RIGHT(desc,3)
    RateTxt  = Table.AddColumn(Named, "RateText",
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

> The single table every report visual uses. The last three steps force an exact column list
> and exact types, so the table looks identical whatever the source files happen to contain -
> RM files have no Rate, consumables have no Nature, and this is what stops that mattering.

```
let
    Combined = Table.Combine({factRM, factFG, factConble}),
    Wanted   = {"SourceFile","ValuationArea","Material","MatKey","MaterialDesc",
                "FromDate","ToDate","OpenQty","OpenVal","ReceiptQty","ReceiptVal",
                "IssueQty","IssueVal","CloseQty","CloseVal","BaseUOM","SpecialStock",
                "Currency","Month","Category","Nature","GroupNature","BOMStdQty","Item",
                "AttrMissing","MW","Rate","RateParseFailed","Mid","Base","INR_WP"},
    Padded   = List.Accumulate(List.Difference(Wanted, Table.ColumnNames(Combined)),
                   Combined, (t, c) => Table.AddColumn(t, c, each null)),
    Kept     = Table.SelectColumns(Padded, Wanted),
    Typed    = Table.TransformColumnTypes(Kept, {
                   {"SourceFile", type text}, {"ValuationArea", type text},
                   {"Material", type text}, {"MatKey", type text},
                   {"MaterialDesc", type text}, {"FromDate", type date},
                   {"ToDate", type date}, {"OpenQty", type number},
                   {"OpenVal", type number}, {"ReceiptQty", type number},
                   {"ReceiptVal", type number}, {"IssueQty", type number},
                   {"IssueVal", type number}, {"CloseQty", type number},
                   {"CloseVal", type number}, {"BaseUOM", type text},
                   {"SpecialStock", type text}, {"Currency", type text},
                   {"Month", type date}, {"Category", type text},
                   {"Nature", type text}, {"GroupNature", type text},
                   {"BOMStdQty", type number}, {"Item", type text},
                   {"AttrMissing", type logical}, {"MW", type number},
                   {"Rate", type number}, {"RateParseFailed", type logical},
                   {"Mid", type text}, {"Base", type text}, {"INR_WP", type number}}),
    // the megawatt column is renamed because Power BI will not let a table hold a column
    // and a measure with the same name, and the report needs the measure to be called MW
    Renamed  = Table.RenameColumns(Typed, {{"MW", "MW Qty"}})
in
    Renamed
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
    All     = List.Distinct(List.Combine({FromRM, FromFG, FromCap, {"Unassigned"}})),
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
                   {"GLAccount", type text}, {"GLDescMaster", type text},
                   {"Nature", type text}, {"TBPlant", type text},
                   {"TBSort", Int64.Type}}),
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
    // the three named plant codes, written out here rather than read from dimPlant: a query
    // that opens a folder itself may not also reference another query, or the refresh stops
    // with 'references other queries or steps, so it may not directly access a data source'
    Known    = {"1900", "1902", "1905"},
    PlantCol = Table.AddColumn(PlantRaw, "ValuationArea",
                   each if List.Contains(Known, [PlantCode]) then [PlantCode] else "Unallocated",
                   type text),
    Typed    = Table.TransformColumnTypes(PlantCol, {{"Amount", type number}})
in
    Typed
```


## dimPlant

> The three plants are named here - no sheet, no header to mismatch, add a plant by adding a line. Every other code the stock files carry is then added automatically, so no fact row can fall into an unnamed blank member of a slicer.

```
let
    Named    = #table(
        type table [ValuationArea = text, Plant = text, PlantSort = Int64.Type],
        {
            {"1900", "Jaipur Module",  1},
            {"1902", "Dholera Module", 2},
            {"1905", "Dholera Cell",   3},
            // factTB_Staged parks a profit centre it cannot place here
            {"Unallocated", "Unallocated", 98}
        }),
    // codes present in the stock files or the trial balance but not named above. Only other
    // queries are read here and no folder is opened, which is what keeps the firewall quiet.
    Seen     = List.Distinct(List.RemoveNulls(
                   List.Combine({factInventory[ValuationArea], factTB_Staged[PlantCode]}))),
    Extra    = List.Difference(Seen, Named[ValuationArea]),
    ExtraT   = Table.FromRows(
                   List.Transform(Extra, (c) => {c, "Plant " & Text.From(c), 99}),
                   type table [ValuationArea = text, Plant = text, PlantSort = Int64.Type]),
    All      = Table.Combine({Named, ExtraT}),
    Dedup    = Table.Distinct(All, {"ValuationArea"})
in
    Dedup
```

## factTB

> The inner join to dimTBMaster IS the trial-balance cleaning - only whitelisted GL accounts survive. `Category` is worked out from the Nature text on TB Master, so the trial balance and MB5B can be compared on the same RM / FG / Consumables row.

```
let
    Mapped  = Table.NestedJoin(factTB_Staged, {"GLAccount"}, dimTBMaster, {"GLAccount"},
                  "tpl", JoinKind.Inner),
    Joined  = Table.ExpandTableColumn(Mapped, "tpl", {"Nature","TBPlant","TBSort"}),
    // If the whitelist matched nothing - no TB Master sheet, a sheet under another name, or
    // GL numbers written differently there than in the TB export - the inner join returns
    // nothing and Inventory (TB) reads as empty while Difference reads as minus MB5B. Keep
    // every staged row in that case: an unfiltered trial balance is wrong by whatever
    // non-inventory GLs it carries, but it is visible, and factTB_Unmapped names them.
    Raw     = List.Accumulate({"Nature","TBPlant","TBSort"}, factTB_Staged,
                  (t, c) => Table.AddColumn(t, c, each null)),
    Expand  = if Table.IsEmpty(Joined) then Raw else Joined,
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
                  each Bucket([Nature], [GLDesc]), type text),
    // exact column list and types, so the table is the same shape every refresh
    Wanted  = {"SourceFile","Month","GLAccount","GLDesc","ProfitCentre","ProfitCentreDesc",
               "Amount","PlantCode","ValuationArea","Nature","TBPlant","TBSort","Category"},
    Padded  = List.Accumulate(List.Difference(Wanted, Table.ColumnNames(Cat)), Cat,
                  (t, c) => Table.AddColumn(t, c, each null)),
    Kept    = Table.SelectColumns(Padded, Wanted),
    Typed   = Table.TransformColumnTypes(Kept, {
                  {"SourceFile", type text}, {"Month", type date},
                  {"GLAccount", type text}, {"GLDesc", type text},
                  {"ProfitCentre", type text}, {"ProfitCentreDesc", type text},
                  {"Amount", type number}, {"PlantCode", type text},
                  {"ValuationArea", type text}, {"Nature", type text},
                  {"TBPlant", type text}, {"TBSort", Int64.Type},
                  {"Category", type text}})
in
    Typed
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

> One row **only for a month that has data**. It is built from the months actually present in the stock files and the trial balance, not from a continuous April-to-March range, so a month you have not added yet cannot appear as an option in any slicer. Add July 2025's MB5B and July'25 appears in the pickers; until then it does not exist in the model at all. Nothing else has to change when a new month arrives.

```
let
    // the months that actually exist in the data: stock files and trial balance. Building the
    // calendar from these, rather than filling in every month between the first and the last,
    // is what keeps months you have not loaded yet out of the slicers.
    // the trial balance is read inside a try, so a missing or empty TB folder leaves the
    // calendar to the stock files instead of taking the whole calendar down with it
    TBM    = try factTB_Staged[Month] otherwise {},
    Seen   = List.RemoveNulls(List.Combine({factInventory[Month], TBM})),
    Months = List.Sort(List.Distinct(List.Transform(Seen, Date.StartOfMonth))),
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
                 in  "FY " & Text.From(y) & "-" & Text.End(Text.From(y + 1), 2), type text),
    // the year starts on 1 April, so Apr-Jun is Q1 and Jan-Mar is Q4
    FYMonth = Table.AddColumn(FY, "FYMonthNo",
                 each Number.Mod(Date.Month([Month]) - 4, 12) + 1, Int64.Type),
    Qtr    = Table.AddColumn(FYMonth, "QuarterNo",
                 each Number.RoundUp([FYMonthNo] / 3), Int64.Type),
    QName  = Table.AddColumn(Qtr, "Quarter",
                 each "Q" & Text.From([QuarterNo]) & " " & [FY], type text),
    QSort  = Table.AddColumn(QName, "QuarterSort", each
                 let y = if Date.Month([Month]) >= 4 then Date.Year([Month]) else Date.Year([Month]) - 1
                 in  y * 10 + [QuarterNo], Int64.Type),
    Out    = Table.SelectColumns(QSort,
                 {"Month","MonthName","MonthSort","MonthIndex","FY",
                  "FYMonthNo","QuarterNo","Quarter","QuarterSort"})
in
    Out
```

`Quarter` reads `Q1 FY 2026-27` for April–June, `Q4 FY 2026-27` for January–March. Sort it by
`QuarterSort` in step 2.5 or the slicer lists the quarters alphabetically, which puts Q1 of
every year together.

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
    Slim2 = Table.SelectColumns(Rows, {"Item","Headers","DataRows"}),
    Out   = Table.RenameColumns(Slim2, {{"Item","SheetName"}})
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
    T         = Table.FromList(Orphans, Splitter.SplitByNothing(), {"Nature"}),
    Typed     = Table.TransformColumnTypes(T, {{"Nature", type text}})
in
    Typed
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
MW = SUM(factInventory[MW Qty])
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

With no category picked — the header card on `Overview`, and the card on `Detail` — the
numerator is every category's MW over the one capacity, so the figure is RM days and FG days
added together, not FG on its own. That is why both cards are titled
`Days of inventory (RM + FG)`. If you ever want FG alone on the band, use the `FG Days`
measure below instead, which divides FG MW only.

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
RETURN CALCULATE([Value ₹ Cr], FILTER(ALL(dimDate), dimDate[MonthIndex] = LastIdx))
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

## New in this update

Everything below is new. If you built the pages before this update, paste these in order at
the end of your existing measures — nothing above changes.

```
Latest Month Index = CALCULATE(MAX(dimDate[MonthIndex]), REMOVEFILTERS())

As On Text =
VAR LastIdx = [Latest Month Index]
RETURN "As on " & CALCULATE(MAX(dimDate[MonthName]), REMOVEFILTERS(),
    FILTER(ALL(dimDate), dimDate[MonthIndex] = LastIdx))

Ticker Rs Cr =
VAR LastIdx = [Latest Month Index]
RETURN CALCULATE([Value ₹ Cr], REMOVEFILTERS(),
    FILTER(ALL(dimDate), dimDate[MonthIndex] = LastIdx))

Ticker RM Rs Cr =
VAR LastIdx = [Latest Month Index]
RETURN CALCULATE([Value ₹ Cr], REMOVEFILTERS(),
    FILTER(ALL(dimDate), dimDate[MonthIndex] = LastIdx),
    FILTER(ALL(dimCategory), dimCategory[Category] = "RM"))

Ticker FG Rs Cr =
VAR LastIdx = [Latest Month Index]
RETURN CALCULATE([Value ₹ Cr], REMOVEFILTERS(),
    FILTER(ALL(dimDate), dimDate[MonthIndex] = LastIdx),
    FILTER(ALL(dimCategory), dimCategory[Category] = "FG"))

Ticker Consumables Rs Cr =
VAR LastIdx = [Latest Month Index]
RETURN CALCULATE([Value ₹ Cr], REMOVEFILTERS(),
    FILTER(ALL(dimDate), dimDate[MonthIndex] = LastIdx),
    FILTER(ALL(dimCategory), dimCategory[Category] = "Consumables"))

Ticker 1900 Rs Cr =
VAR LastIdx = [Latest Month Index]
RETURN CALCULATE([Value ₹ Cr], REMOVEFILTERS(),
    FILTER(ALL(dimDate), dimDate[MonthIndex] = LastIdx),
    FILTER(ALL(dimPlant), dimPlant[ValuationArea] = "1900"))

Ticker 1902 Rs Cr =
VAR LastIdx = [Latest Month Index]
RETURN CALCULATE([Value ₹ Cr], REMOVEFILTERS(),
    FILTER(ALL(dimDate), dimDate[MonthIndex] = LastIdx),
    FILTER(ALL(dimPlant), dimPlant[ValuationArea] = "1902"))

Ticker 1905 Rs Cr =
VAR LastIdx = [Latest Month Index]
RETURN CALCULATE([Value ₹ Cr], REMOVEFILTERS(),
    FILTER(ALL(dimDate), dimDate[MonthIndex] = LastIdx),
    FILTER(ALL(dimPlant), dimPlant[ValuationArea] = "1905"))

Ticker Prev Rs Cr =
VAR LastIdx = [Latest Month Index]
RETURN CALCULATE([Value ₹ Cr], REMOVEFILTERS(),
    FILTER(ALL(dimDate), dimDate[MonthIndex] = LastIdx - 1))

Ticker Change Rs Cr = [Ticker Rs Cr] - [Ticker Prev Rs Cr]

Ticker Change % = DIVIDE([Ticker Change Rs Cr], [Ticker Prev Rs Cr])

Ticker Change Text =
IF(
    ISBLANK([Ticker Prev Rs Cr]),
    "No earlier month to compare",
    FORMAT([Ticker Change Rs Cr], "+#,##0.0;-#,##0.0") & " Rs Cr.   ("
        & FORMAT([Ticker Change %], "+0.0%;-0.0%") & ")"
)

Inventory Rs Cr =
IF(
    ISINSCOPE(dimDate[MonthName]),
    [Value ₹ Cr],
    AVERAGEX(VALUES(dimDate[MonthIndex]), [Value ₹ Cr])
)

In Window =
VAR Picked = ISFILTERED(dimDate[MonthName])
VAR Me = MAX(dimDate[MonthIndex])
VAR Live =
    CALCULATETABLE(VALUES(dimDate[MonthIndex]), REMOVEFILTERS(), factInventory)
VAR LastIdx = MAXX(Live, dimDate[MonthIndex])
VAR MarchIdx =
    MAXX(
        FILTER(
            ALL(dimDate),
            dimDate[FYMonthNo] = 12
                && dimDate[MonthIndex] <= LastIdx
                && CALCULATE(COUNTROWS(factInventory)) > 0),
        dimDate[MonthIndex])
VAR Alive = COUNTROWS(FILTER(Live, dimDate[MonthIndex] = Me))
VAR Place = COUNTROWS(FILTER(Live, dimDate[MonthIndex] > Me)) + 1
RETURN
IF(
    Picked,
    1,
    IF(
        Alive > 0
            && Me >= MarchIdx
            && (Place <= 4 || Me = MarchIdx),
        1,
        0)
)

In Summary Window =
VAR Picked = ISFILTERED(dimDate[MonthName])
VAR Me = MAX(dimDate[MonthIndex])
VAR Live =
    CALCULATETABLE(VALUES(dimDate[MonthIndex]), REMOVEFILTERS(), factInventory)
VAR Alive = COUNTROWS(FILTER(Live, dimDate[MonthIndex] = Me))
VAR Place = COUNTROWS(FILTER(Live, dimDate[MonthIndex] > Me)) + 1
RETURN
IF(
    Picked,
    IF(Place <= 12, 1, 0),
    IF(Alive > 0 && Place <= 4, 1, 0)
)

MW % vs LM = DIVIDE([MW] - [MW LM], [MW LM])

RM MW = CALCULATE([MW], factInventory[Category] = "RM")

RM Days = DIVIDE([RM MW], [Capacity MW (plant)])

Total Days (RM + FG) = DIVIDE([RM MW] + [FG MW], [Capacity MW (plant)])

RM Days All Plants =
VAR M = CALCULATE([RM MW], REMOVEFILTERS(dimPlant))
VAR Cap = CALCULATE([Capacity MW (plant)], REMOVEFILTERS(dimPlant))
RETURN DIVIDE(M, Cap)

RM Days All Plants by Period =
IF(
    ISINSCOPE(dimDate[MonthName]),
    [RM Days All Plants],
    AVERAGEX(VALUES(dimDate[MonthIndex]), [RM Days All Plants])
)

In Last 12 =
VAR LastM = [Latest Month Index]
VAR ThisM = MAX(dimDate[MonthIndex])
RETURN IF(ThisM > LastM - 12 && ThisM <= LastM, 1, 0)

Summary Value Rs Cr =
IF(
    ISINSCOPE(dimDate[MonthName]),
    [Summary Value ₹ Cr],
    AVERAGEX(VALUES(dimDate[MonthIndex]), [Summary Value ₹ Cr])
)

TB Inventory Rs Cr =
IF(
    ISINSCOPE(dimDate[MonthName]),
    [TB ₹ Cr],
    AVERAGEX(VALUES(dimDate[MonthIndex]), [TB ₹ Cr])
)

Difference Inventory Rs Cr = [TB Inventory Rs Cr] - [Inventory Rs Cr]

Difference Inventory % = DIVIDE([Difference Inventory Rs Cr], [TB Inventory Rs Cr])

Unit Value by Period =
IF(
    ISINSCOPE(dimDate[MonthName]),
    [Unit Value],
    AVERAGEX(VALUES(dimDate[MonthIndex]), [Unit Value])
)

In Latest Month =
IF(MAX(dimDate[MonthIndex]) = [Latest Month Index], 1, 0)

Days by Period =
IF(
    ISINSCOPE(dimDate[MonthName]),
    [Days],
    AVERAGEX(VALUES(dimDate[MonthIndex]), [Days])
)

Check MB5B Rows = COUNTROWS(factInventory)

Check TB Rows = COUNTROWS(factTB)

Check Months of Data = DISTINCTCOUNT(factInventory[Month])

Check Plant Codes = DISTINCTCOUNT(factInventory[ValuationArea])

Check Unassigned % =
DIVIDE(
    COUNTROWS(FILTER(factInventory, factInventory[Nature] = "Unassigned")),
    COUNTROWS(factInventory)
)

```

`Summary Value Rs Cr` is the Summary page's only figure. It is `Summary Value ₹ Cr` with the
quarter rule added: at month grain it hands back the month-end, at any total or quarter grain it averages
that quarter's three month-ends, so switching the toggle never turns a stock level into a sum.

`In Summary Window` is the Summary twin of `In Window`, and the only difference is the count:
nothing ticked means the **last 4** periods, and ticking your own means up to **twelve** of
them, the twelve most recent if you tick more. Put it in the Filters pane of both Summary
matrices and set it to **is 1**. The two FG matrices use the same measure, so FG picks up the
same four-by-default, twelve-at-most behaviour without a second copy of the logic.

`TB Inventory Rs Cr` is the trial-balance side with the same quarter rule, and
`Difference Inventory Rs Cr` / `Difference Inventory %` are the gap between the books and the
stock report in crore rupees and as a share of the books. The two charts along the bottom of
Summary read these three, so the chart and the matrix above it can never disagree.

`Unit Value by Period` is `Unit Value` with the quarter rule, and it is what the FG matrices
put in Values. `Unit Value` on its own is still correct for MW and Rs Cr. in a single month,
but at a quarter or total grain it would add three month-ends together; the by-Period version averages
them instead.

The five `Check ...` measures are what the **Checks** page reads. `Check TB Rows` at 0 means
the TB folder produced nothing; `Check Unassigned %` above zero is the share of stock rows the
master sheets do not cover, which is exactly what turns a donut slice into Unassigned.

`In Latest Month` pins a visual to the newest month that has data. Use it on any chart whose
axis is **not** a period — the FG technology bar chart and the FG donut are the two — because
without it four ticked months of stock would be added together and the chart would read four
times too high. Set it to **is 1** in those two visuals' Filters pane and it never needs
editing again.

`Days by Period` is `Days` with the quarter rule, and the RM page's days chart uses it. Days is
a ratio of two stock figures, so at a quarter grain it has to be the average of the quarter's three
month-end ratios; adding them would give a nonsense number three times too big.

### Changed in build 10

The green panel is furniture, and furniture belongs on every page.

**The panel is repeated on all six pages** at the same coordinates: the green rectangle at
Horizontal 0, Vertical 0, 184 × 720, the logo strip, the two heading lines, the two section
labels, the three white boxes and the nine figures, unchanged. Build it once on `Overview`,
select the whole strip, **Ctrl+C**, then **Ctrl+V** on `Summary`, `FG`, `RM`, `Detail` and
`Checks` — pasted visuals keep their positions, so the panel cannot drift page to page. On each
page change the second heading line from `Overview` to that page's name; nothing else changes.

**Every other visual moves right of the panel.** The five pages that were drawn across the full
width now start at Horizontal **192** instead of 16 and are narrower in the same proportion, so
nothing sits underneath the green. The positions in Part 4 are already the new ones.

**The As-on card is 44 tall, not 28**, because the sentence sits under the words 'As on' and 28
cut it in half.

### Changed in build 9

Three edits if you have already built this by hand.

**`dimDate`** no longer generates a continuous April-to-March range. Replace its first steps with
the ones in the `dimDate` section above: the calendar is now the list of months actually present in
`factInventory` and `factTB_Staged`, so a month with no file cannot appear in any slicer. Paste
`dimDate` after `factTB_Staged`, or Power Query will not find the reference.

**`In Window`** gains one condition, `Me >= MarchIdx`, so months that fall before the newest March
are excluded from the default five columns. Without it January and February of the same year could
appear ahead of March, and March was no longer the first column.

**The ticker cards** drop from 16pt to **11pt** (13pt on Total, 10pt on the As-on line). At 16pt a
four-figure crore value in a 156-wide card is cut off. The wide cards on Detail and Checks stay
readable at 14pt.
