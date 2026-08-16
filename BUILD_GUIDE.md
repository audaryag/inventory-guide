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

### How to add each query (you will repeat this 40 times)

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
| 8 | `fnVarSheetSafe` | helper — lets a missing master sheet load empty instead of failing |
| 9 | `dimPlant` | the plants come from Plant Master, kept to the ones with data |
| 10 | `dimMaterialAttr` |  |
| 11 | `dimFGAttr` |  |
| 12 | `varConstants` | needs a `RM_MW_FACTOR` = 580 row |
| 13 | `fnConstantAsOf` |  |
| 14 | `dimPlantMaster` | reads the Plant Master sheet — helper, load off |
| 15 | `varPlantCodes` | the plant codes on that sheet — helper, load off |
| 16 | `factRM` |  |
| 17 | `factFG` |  |
| 18 | `factConble` |  |
| 19 | `factInventory` |  |
| 20 | `varMWCapacity` | reads the two-block MW sheet |
| 21 | `dimCapacity` |  |
| 22 | `dimNature` |  |
| 23 | `dimTBMaster` |  |
| 24 | `factTB_Staged` |  |
| 25 | `factTB` |  |
| 26 | `factTB_Unmapped` |  |
| 27 | `dimDate` |  |
| 28 | `qcHeaders` | self-check |
| 29 | `qcVarHeaders` | self-check |
| 30 | `qcNatureNoCapacity` | self-check |
| 31 | `qcMWSheet` | self-check — shows the MW sheet raw |
| 32 | `dimCategory` | lets TB and MB5B share one RM/FG/Consumables row |
| 33 | `dimMetric` | makes Inventory (TB) / Inventory (MB5B) / Difference into columns |
| 34 | `dimMeasure` | makes MW / In ₹ Cr / In Days into columns |
| 35 | `qcAttrMatch` | self-check — do the material numbers match between sheets and files |
| 36 | `qcTBByGL` | self-check — the trial balance by GL account, signed |
| 37 | `qcPlantCodes` | self-check — every plant code the files contain, and what the ones outside the three cost |
| 38 | `qcMonthFiles` | self-check — did any month arrive from two files |
| 39 | `qcMasterDupes` | self-check — one material with two natures on a master sheet |
| 40 | `qcTBPlants` | self-check — every TB profit centre and the plant it resolved to |

**1.4 — Do this before the first refresh; it is not optional.** The report reads two kinds of
source - the four stock/TB folders and the `Variables and Calculations` workbook - and every nature,
plant name and TB category comes from putting the two together. Power Query's privacy firewall
blocks that pairing by default and reports it as *"Query 'x' references other queries or steps, so
it may not directly access a data source. Please rebuild this data combination"*, blocking a dozen
queries at once. It is not a fault in the queries and it cannot be coded around: two different
sources have to meet somewhere. Turn the firewall off once, for your own files:

**File → Options and settings → Options → GLOBAL → Privacy → "Always ignore Privacy Level
settings" → OK.** Then also, on the same dialog, **CURRENT FILE → Privacy → "Always ignore Privacy
Level settings" → OK**, and refresh again. The Global one covers every file you open afterwards, so
this is the last time you have to think about it.

If it asks about **credentials**, choose **Organizational** for OneDrive and click through.

**1.5 — Important.** Turn off loading for the helper queries. For **each** of these,
right-click the query in the left list and **untick "Enable load"**:

```
pRoot, pVarsFile, fnCleanMB5B, stgRM, stgFG, stgConble,
fnVarSheet, fnVarSheetSafe, dimPlantMaster, varPlantCodes,
factRM, factFG, factConble, varConstants,
fnConstantAsOf, varMWCapacity, factTB_Staged
```

Leave these ticked (they become your tables):
```
factInventory, factTB, factTB_Unmapped, dimPlant, dimDate,
dimNature, dimCapacity, dimTBMaster, dimMaterialAttr, dimFGAttr,
dimCategory, dimMetric, dimMeasure,
qcHeaders, qcVarHeaders, qcNatureNoCapacity, qcMWSheet,
qcAttrMatch, qcTBByGL, qcPlantCodes,
qcMonthFiles, qcMasterDupes, qcTBPlants
```

**1.6** Ribbon: **Home** → **Close & Apply**. Wait for it to load.

### Checkpoint — do not go to Part 2 until all five are true

1. The Queries list on the left of Power Query shows **40** names, and every name in the
   table above appears in it, spelled identically. Compare them one by one; a missing one
   is the single most common cause of an error later.
2. The 17 helper names in step 1.5 are shown in *italics* in that list (that is what
   "Enable load off" looks like); the other 23 are not italic.
3. Click `factInventory`: the preview shows rows, and the columns include `CloseVal`,
   `Category`, `Nature`, `Month`, `ValuationArea`, `MW`.
4. Click `factTB`: it shows rows, `Month` is filled in on every row, and `ValuationArea`
   is not the word `Unallocated` on every row.
5. Click `factTB_Unmapped`: ideally empty. Rows here mean a GL account in your TB is
   missing from `TB Master`, so its money is not counted anywhere — add it to `TB Master`
   and refresh.

After **Close & Apply**, the Data pane on the right must list exactly these 23 tables:
`factInventory`, `factTB`, `factTB_Unmapped`, `dimPlant`, `dimDate`, `dimNature`,
`dimCapacity`, `dimTBMaster`, `dimMaterialAttr`, `dimFGAttr`, `dimCategory`, `dimMetric`,
`dimMeasure`, `qcHeaders`, `qcVarHeaders`, `qcNatureNoCapacity`, `qcMWSheet`,
`qcAttrMatch`, `qcTBByGL`, `qcPlantCodes`, `qcMonthFiles`, `qcMasterDupes`, `qcTBPlants`.

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
| "Expression.Syntax Error" right after pasting | the whole appendix went into one query | one query per Blank Query, 40 times |

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
2. Count the measures (calculator icons) — there must be **78**. Fewer means Appendix B is
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
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On and Column subtotals: On. The bottom row is the month's whole inventory, and the right-hand Total column is the average of the month-ends shown, which is what a stock level averages to — it is never their sum.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 10, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 10, Colour: #14532D.

**4.19** **Clustered column chart** — The long view, under the table: one bar per month for the last twelve months that have data, or fewer if that is all there is. The figure above each bar is the megawatts held that month. It is in MW rather than rupees on purpose: this strip is about how much product is sitting there, which prices cannot flatter. Each bar is that month's closing stock on its own, so nothing here is ever added across months.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `MW` |
| Filters | `In Last 12  →  is 1` |

Title: `Total Inventory by Month, Last 12 Months (MW)`

Position: Horizontal 200, Vertical 576, Width 700, Height 130.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- This one must ignore the two controls at the top, or it would shrink back to five months. Click the 'Months' slicer once, then ribbon Format → Edit interactions; small icons appear on every other visual. On this chart click the circle-with-a-line (None). Leave Plant and Type set to filter, so those two still work on it.
- In the Visualizations pane click the paintbrush icon, then click 'Data labels' and set it to On, Font: Arial, Font size: 9, Bold: On, Colour: #1F2A24, Display units: None, Value decimal places: 1, Position: Outside end. Outside, not inside: a dark figure on a dark green bar cannot be read, which is exactly what was wrong before.
- In the Visualizations pane click the paintbrush icon, then click 'Y-axis' and set it to Off. The number is printed above every bar, so a scale up the side would only eat the height.
- In the Visualizations pane click the paintbrush icon, then click 'X-axis', then 'Values', then 'Font' and set it to Arial, Font size: 8, Colour: #1F2A24, Concatenate labels: Off, and Maximum height: 20%.
- In the Visualizations pane click the paintbrush icon, then click 'X-axis', then 'Inner padding: 30%, and Format pane', then 'General', then 'Properties', then 'Padding' and set it to Left 12, Right 12. The padding is what stops the first and last bar touching the sides of the card, and it pulls both edges in by the same amount.
- In the Visualizations pane click the paintbrush icon, then click 'Columns', then 'Colour: #2E7D46. Format pane', then 'Lines', then 'Colour' and set it to #9AA79F, Stroke width: 1, Show marker: On, Marker size: 3 — the line is only there to carry its labels, so it is deliberately quiet.
- In the Visualizations pane click the paintbrush icon, then click 'Legend' and set it to Off. Two series, both labelled on the chart, so a key would repeat what the labels already say.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 11, Colour: #14532D.

**4.20** **Donut chart** — What the finished goods are made of in the latest month that has data — the module technologies, largest slice first. It is pinned to the latest month by the In Latest Month filter, because adding one month-end of stock to another would be meaningless; the Plant and Type slicers still narrow it.

| Well | Field |
|---|---|
| Legend | `dimNature[Nature]` |
| Values | `Latest Month Value ₹ Cr` |
| Filters | `dimCategory[Category]  →  is FG` |

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
| Values | `Latest Month Value ₹ Cr` |
| Filters | `dimCategory[Category]  →  is RM` |

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

**4.26** **Matrix** — One table, the whole reconciliation: a row per plant opening into RM, FG and Consumables, a column per month — the newest March plus the three after it by default — and under each month the three figures side by side: TB, MB5B and the Check between them. The Total row under each plant is that plant across its three types, and the Grand Total row at the foot is every plant added together, which is the Total Overall block of the Excel sheet — so this single matrix replaces the six that stood here.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]`, `dimCategory[Category]` |
| Columns | `dimDate[MonthName]` |
| Values | `TB Inventory Rs Cr` → rename it to **TB**, `Inventory Rs Cr` → rename it to **MB5B**, `Difference Inventory Rs Cr` → rename it to **Check** |
| Filters | `In Summary Window  →  is 1` |

Title: `Inventory — TB, MB5B and the Check, by Plant and Type (Rs Cr.)`

Position: Horizontal 192, Vertical 88, Width 1072, Height 352.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Columns holds dimDate[MonthName] and nothing else. The three measures in Values are what put TB, MB5B and Check under each month: a Metric field above the month would be a two-level column hierarchy, and Desktop opens one of those collapsed onto a single figure per metric — or draws the visual as an empty card. Measures under a single column field cannot do either.
- Rename each measure in the Values box — double-click it and type TB, MB5B, Check — so the headings read the way the Excel sheet did rather than repeating "Rs Cr." three times across every month.
- Filters pane → drag the measure In Summary Window in → is 1. That is what gives you the newest March plus three months by default, and the months you tick in the slicer when you tick them.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On with 'Per row level' On. Those totals add plants inside one month, which is a real figure — one point in time, three stock locations — and they are what make the six separate tables unnecessary.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Stepped layout' and set it to Off, +/- icons: On, so Plant and Type sit in two columns with an expander on each plant.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font: Arial, Font size: 8, Colour: #1F2A24; Row headers', then 'Font size: 8; Column headers', then 'Font size' and set it to 8, Word wrap: On. Twelve figures across the width means every column has to earn its pixels.
- Values box → the down-arrow next to Check → Conditional formatting → Background color → Format style: Diverging, tick 'Add a middle colour', middle number 0, and make both Minimum and Maximum red. A gap either side of zero is equally wrong.
- Drag the line between two column headings if a figure shows three dots; column widths are remembered when you save.

**4.27** **Clustered column chart** — The books against the stock report, two bars per period: the same figures as the matrix above, but you can see a gap opening without reading a single number. Same periods as the matrices, because it carries the same filter.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `TB Inventory Rs Cr`, `Inventory Rs Cr` |
| Filters | `In Summary Window  →  is 1` |

Title: `Inventory (TB) vs Inventory (MB5B) by Month (Rs Cr.)`

Position: Horizontal 192, Vertical 464, Width 529, Height 120.

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

**4.28** **Line and clustered column chart** — The question the reconciliation is really asking: is the gap widening or closing. The bar is the difference in crore rupees, the line above it the same difference as a percentage of the trial balance, so a small gap on a big month reads as small.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Column y-axis | `Difference Inventory Rs Cr` |
| Line y-axis | `Difference Inventory %` |
| Filters | `In Summary Window  →  is 1` |

Title: `Difference by Month (Rs Cr. and % of TB)`

Position: Horizontal 735, Vertical 464, Width 529, Height 120.

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
- In the Visualizations pane click the paintbrush icon, then click 'Legend' and set it to Off — the title says which is which, and 120 pixels of height has none to spare.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 11, Colour: #14532D.

**4.29** **Line chart** — The long view under the reconciliation: three lines across the last twelve months that have data, or fewer if that is all there is — raw material days, finished goods days, and the two added together, which is what the Overview card calls Days of inventory (RM + FG). Every month is its own closing figure divided by capacity, so nothing is added across months. Read it for shape: RM climbing while FG is flat means material is arriving faster than it is being consumed.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `RM Days`, `FG Days`, `Total Days (RM + FG)` |
| Filters | `In Last 12  →  is 1` |

Title: `Days of Inventory by Month, Last 12 Months — RM, FG and Total`

Position: Horizontal 192, Vertical 592, Width 1072, Height 120.

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

**4.30** **Slicer** — Which months appear under each master column. Tick nothing and it shows the last four with data; tick your own and it shows those, up to twelve.

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

**4.31** **Slicer** — A coarser filter over the same months: tick Q1 and only April, May and June are left for the two matrices to show. Leave it empty to see every month.

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

**4.32** **Slicer** — One plant, or all of them. It filters the technology matrix and all three charts, so picking Dholera Cell turns the page into a Dholera Cell page.

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

**4.33** **Slicer** — One module technology, when you want the page to be about that technology only.

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

**4.34** **Matrix** — Finished goods per plant in megawatts, one column per month — the newest March plus the three after it by default. The Excel sheet had this as one wide table with an IN MW block, an IN CRS block and an IN DAYS block; these are those blocks.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]` |
| Columns | `dimDate[MonthName]` |
| Values | `Inventory MW` → rename it to **MW** |
| Filters | `dimCategory[Category]  →  is FG`, `In Summary Window  →  is 1` |

Title: `Inventory FG by Plant — In MW`

Position: Horizontal 192, Vertical 88, Width 350, Height 112.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Columns holds dimDate[MonthName] and nothing else, and Values holds one measure. That is what puts the months on show with nothing to expand: a Metric field above the month is a two-level column hierarchy, and Desktop opens one of those collapsed onto a single figure per metric — or draws the visual as an empty card, which is what emptied this page. One metric per matrix, side by side, is the same grid the Excel sheet had.
- Filters pane → dimCategory[Category] → tick FG only, then the measure In Summary Window → is 1.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice. Row subtotals: On — that one adds the plants inside a single month, which is a real figure, and it is the Grand Total row the Excel sheet had.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font: Arial, Font size: 8, Colour: #1F2A24; Row headers', then 'Font size: 8; Column headers', then 'Font size' and set it to 8. Three blocks across the width means every column has to earn its pixels.
- Clicking a plant row filters the technology blocks and the charts below to it.

**4.35** **Matrix** — Finished goods per plant in crore rupees, one column per month — the newest March plus the three after it by default. The Excel sheet had this as one wide table with an IN MW block, an IN CRS block and an IN DAYS block; these are those blocks.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]` |
| Columns | `dimDate[MonthName]` |
| Values | `Inventory Rs Cr` → rename it to **Rs Cr.** |
| Filters | `dimCategory[Category]  →  is FG`, `In Summary Window  →  is 1` |

Title: `Inventory FG by Plant — In Rs Cr`

Position: Horizontal 549, Vertical 88, Width 350, Height 112.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Fastest way to build the next block: click this matrix, Ctrl+C, Ctrl+V, then in Values swap the measure. Position, filters and formatting all come with the copy.
- Filters pane → dimCategory[Category] → tick FG only, then the measure In Summary Window → is 1.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice. Row subtotals: On — that one adds the plants inside a single month, which is a real figure, and it is the Grand Total row the Excel sheet had.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font: Arial, Font size: 8, Colour: #1F2A24; Row headers', then 'Font size: 8; Column headers', then 'Font size' and set it to 8. Three blocks across the width means every column has to earn its pixels.
- Clicking a plant row filters the technology blocks and the charts below to it.

**4.36** **Matrix** — Finished goods per plant in days of cover, one column per month — the newest March plus the three after it by default. The Excel sheet had this as one wide table with an IN MW block, an IN CRS block and an IN DAYS block; these are those blocks.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]` |
| Columns | `dimDate[MonthName]` |
| Values | `Days` → rename it to **Days** |
| Filters | `dimCategory[Category]  →  is FG`, `In Summary Window  →  is 1` |

Title: `Inventory FG by Plant — In Days`

Position: Horizontal 907, Vertical 88, Width 350, Height 112.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Fastest way to build the next block: click this matrix, Ctrl+C, Ctrl+V, then in Values swap the measure. Position, filters and formatting all come with the copy.
- Filters pane → dimCategory[Category] → tick FG only, then the measure In Summary Window → is 1.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice. Row subtotals: On — that one adds the plants inside a single month, which is a real figure, and it is the Grand Total row the Excel sheet had.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font: Arial, Font size: 8, Colour: #1F2A24; Row headers', then 'Font size: 8; Column headers', then 'Font size' and set it to 8. Three blocks across the width means every column has to earn its pixels.
- Days is MW ÷ capacity MW, so a plant with no row on the MW Capacity sheet is blank here on purpose — a missing denominator is not the same as no stock.

**4.37** **Matrix** — The same months and the same unit, by module technology rather than by plant — G12 Perc, G12R Topcon, M10 Perc, M10 Topcon and the rest — which is where a build-up in one technology shows itself.

| Well | Field |
|---|---|
| Rows | `dimNature[Nature]` |
| Columns | `dimDate[MonthName]` |
| Values | `Inventory MW` → rename it to **MW** |
| Filters | `dimCategory[Category]  →  is FG`, `In Summary Window  →  is 1` |

Title: `Inventory FG by Techno — In MW`

Position: Horizontal 192, Vertical 208, Width 350, Height 180.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Fastest way to build the next block: click this matrix, Ctrl+C, Ctrl+V, then in Values swap the measure. Position, filters and formatting all come with the copy. Then in Rows take dimPlant[Plant] out and drag dimNature[Nature] in.
- Check the filters came across: Category is FG, In Summary Window is 1.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice. Row subtotals: On — that one adds the plants inside a single month, which is a real figure, and it is the Grand Total row the Excel sheet had.
- With the Plant slicer on one plant this becomes that plant's technology split, which is the Module block the Excel sheet had.

**4.38** **Matrix** — The same months and the same unit, by module technology rather than by plant — G12 Perc, G12R Topcon, M10 Perc, M10 Topcon and the rest — which is where a build-up in one technology shows itself.

| Well | Field |
|---|---|
| Rows | `dimNature[Nature]` |
| Columns | `dimDate[MonthName]` |
| Values | `Inventory Rs Cr` → rename it to **Rs Cr.** |
| Filters | `dimCategory[Category]  →  is FG`, `In Summary Window  →  is 1` |

Title: `Inventory FG by Techno — In Rs Cr`

Position: Horizontal 549, Vertical 208, Width 350, Height 180.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Fastest way to build the next block: click this matrix, Ctrl+C, Ctrl+V, then in Values swap the measure. Position, filters and formatting all come with the copy. Then in Rows take dimPlant[Plant] out and drag dimNature[Nature] in.
- Check the filters came across: Category is FG, In Summary Window is 1.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice. Row subtotals: On — that one adds the plants inside a single month, which is a real figure, and it is the Grand Total row the Excel sheet had.
- With the Plant slicer on one plant this becomes that plant's technology split, which is the Module block the Excel sheet had.

**4.39** **Matrix** — The same months and the same unit, by module technology rather than by plant — G12 Perc, G12R Topcon, M10 Perc, M10 Topcon and the rest — which is where a build-up in one technology shows itself.

| Well | Field |
|---|---|
| Rows | `dimNature[Nature]` |
| Columns | `dimDate[MonthName]` |
| Values | `Days` → rename it to **Days** |
| Filters | `dimCategory[Category]  →  is FG`, `In Summary Window  →  is 1` |

Title: `Inventory FG by Techno — In Days`

Position: Horizontal 907, Vertical 208, Width 350, Height 180.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Fastest way to build the next block: click this matrix, Ctrl+C, Ctrl+V, then in Values swap the measure. Position, filters and formatting all come with the copy. Then in Rows take dimPlant[Plant] out and drag dimNature[Nature] in.
- Check the filters came across: Category is FG, In Summary Window is 1.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice. Row subtotals: On — that one adds the plants inside a single month, which is a real figure, and it is the Grand Total row the Excel sheet had.
- With the Plant slicer on one plant this becomes that plant's technology split, which is the Module block the Excel sheet had.

**4.40** **Line and clustered column chart** — Which technology is holding the finished goods right now, in money as bars and in megawatts as the line over them. Money is on the bars because every technology has a value, while a megawatt figure only exists for the ones your MW Capacity sheet covers — as bars, that left the chart looking empty. It is deliberately pinned to the latest month with data: there is no period on the axis here, so without that pin it would add four months of stock together and read four times too high.

| Well | Field |
|---|---|
| X-axis | `dimNature[Nature]` |
| Column y-axis | `Latest Month Value ₹ Cr` |
| Line y-axis | `Latest Month MW` |
| Filters | `dimCategory[Category]  →  is FG` |

Title: `FG by Technology, Latest Month — Rs Cr. as Bars, MW as the Line`

Position: Horizontal 192, Vertical 396, Width 354, Height 292.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- Nothing to add in the Filters pane: both measures set the month themselves. Do not put a period field on this chart.
- A technology with bars but no line has no row on the MW Capacity sheet — qcFGNoCapacity on Checks names them.
- In the Visualizations pane click the paintbrush icon, then click 'Data labels' and set it to On, Font: Arial, Font size: 9, Colour: #1F2A24, Display units: None, Value decimal places: 1.
- In the Visualizations pane click the paintbrush icon, then click 'Y-axis' and set it to Off — the label on each bar is the number.
- In the Visualizations pane click the paintbrush icon, then click 'X-axis', then 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Legend' and set it to On, at the top — two measures now, so the line needs naming.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 11, Colour: #14532D.
- Clicking a bar filters both matrices to that technology; right-click → Drill through → Detail for the materials behind it.

**4.41** **Line and clustered column chart** — How long the finished goods on hand would last, month by month, with the change on last month printed above each bar — so a slow build-up is visible before it becomes a number anyone argues about.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Column y-axis | `Days` |
| Line y-axis | `Days vs LM` |
| Filters | `dimCategory[Category]  →  is FG`, `In Last 12  →  is 1` |

Title: `FG Days by Month, Last 12 Months (Days and % vs LM)`

Position: Horizontal 560, Vertical 396, Width 368, Height 292.

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

**4.42** **Donut chart** — Where the finished goods are sitting, as a share of the whole. Pinned to the latest month for the same reason as the bar chart: a share of four added-up months would mean nothing.

| Well | Field |
|---|---|
| Legend | `dimPlant[Plant]` |
| Values | `Latest Month FG ₹ Cr` |

Title: `FG Share by Plant (%), Latest Month`

Position: Horizontal 941, Vertical 396, Width 323, Height 292.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Detail labels' and set Font size to 9. If a slice label is still cut off, set 'Position' to Outside, and switch on 'Overflow text' if your version offers it.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'. If the legend eats the chart, switch Legend off entirely — the labels already name the slices.
- Nothing to add in the Filters pane: Latest Month FG ₹ Cr pins the month itself.
- In the Visualizations pane click the paintbrush icon, then click 'Detail labels', then 'Label contents' and set it to Category, percent of total. Font: Arial, Font size: 9, Colour: #1F2A24, Percentage decimal places: 1 — so the percentage is printed on each slice and nobody has to hover.
- In the Visualizations pane click the paintbrush icon, then click 'Legend' and set it to Off. The slice labels already name the plants.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 11, Colour: #14532D.
- Clicking a slice filters the rest of the page to that plant; clicking it again releases it.

---

## Page — RM

**The panel first.** Go to `Overview`, click the green panel, then hold **Ctrl** and click the logo box, the two heading lines, the two section labels, the three white boxes and all 9 figures on the panel — or draw a selection box around the whole left strip. **Ctrl+C**, come back to `RM`, **Ctrl+V**. Everything arrives at the same coordinates, so the panel is identical on every page.

Then click the second heading line and change its text from `Overview` to `RM`, so the panel doubles as the page's name. Nothing else on the panel changes: the nine figures ignore every slicer on every page by design, because they are the latest month's position and they must read the same wherever you are.

The visuals below are what goes to the **right** of the panel, which is why every Horizontal starts at 192 rather than 16.

**4.43** **Slicer** — Which months appear under each master column, and on both charts along the bottom. Nothing ticked means the last four with data; tick your own for up to twelve.

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

**4.44** **Slicer** — The quarter-mode equivalent: empty means the last four fiscal quarters.

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

**4.45** **Slicer** — One plant, or all three.

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

**4.46** **Slicer** — Module or Cell, when you want the page to be about one of the two only — the same split the Excel sheet had as its Module and Cell blocks.

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

**4.47** **Matrix** — Raw material and packing per plant in crore rupees, one column per month — the top block of the old RM sheet, which had IN CRS and IN DAYS side by side over the same three plants. MW is left out because an RM megawatt figure is derived from a BOM rather than measured.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]` |
| Columns | `dimDate[MonthName]` |
| Values | `Inventory Rs Cr` → rename it to **Rs Cr.** |
| Filters | `dimCategory[Category]  →  is RM`, `In Summary Window  →  is 1` |

Title: `RM Inventory Plant Wise — In Rs Cr`

Position: Horizontal 192, Vertical 88, Width 529, Height 112.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Columns holds dimDate[MonthName] and nothing else, and Values holds one measure. That is what puts the months on show with nothing to expand: a Metric field above the month is a two-level column hierarchy, and Desktop opens one of those collapsed onto a single figure per metric — or draws the visual as an empty card, which is what emptied this page. One metric per matrix, side by side, is the same grid the Excel sheet had.
- Filters pane → dimCategory[Category] → tick RM only, then In Summary Window → is 1.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice. Row subtotals: On — that one adds the plants inside a single month, which is a real figure, and it is the Grand Total row the Excel sheet had.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- Clicking a plant row filters the nature blocks and both charts below it.

**4.48** **Matrix** — Raw material and packing per plant in days of cover, one column per month — the top block of the old RM sheet, which had IN CRS and IN DAYS side by side over the same three plants. MW is left out because an RM megawatt figure is derived from a BOM rather than measured.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]` |
| Columns | `dimDate[MonthName]` |
| Values | `Days` → rename it to **Days** |
| Filters | `dimCategory[Category]  →  is RM`, `In Summary Window  →  is 1` |

Title: `RM Inventory Plant Wise — In Days`

Position: Horizontal 735, Vertical 88, Width 529, Height 112.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Fastest way to build the next block: click this matrix, Ctrl+C, Ctrl+V, then in Values swap the measure. Position, filters and formatting all come with the copy.
- Filters pane → dimCategory[Category] → tick RM only, then In Summary Window → is 1.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice. Row subtotals: On — that one adds the plants inside a single month, which is a real figure, and it is the Grand Total row the Excel sheet had.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- Clicking a plant row filters the nature blocks and both charts below it.

**4.49** **Matrix** — The second block of the old sheet in crore rupees: Module and Cell, each opening into its natures — cell cost, frame, glass, POE, wafer, paste, screens, gases and the rest — with a subtotal on each group and a grand total under them.

| Well | Field |
|---|---|
| Rows | `factInventory[GroupNature]`, `dimNature[Nature]` |
| Columns | `dimDate[MonthName]` |
| Values | `Inventory Rs Cr` → rename it to **Rs Cr.** |
| Filters | `dimCategory[Category]  →  is RM`, `In Summary Window  →  is 1` |

Title: `RM Inventory by Group Nature and Nature — In Rs Cr`

Position: Horizontal 192, Vertical 208, Width 529, Height 220.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Fastest way to build the next block: click this matrix, Ctrl+C, Ctrl+V, then in Values swap the measure. Position, filters and formatting all come with the copy. Then in Rows drop factInventory[GroupNature] and dimNature[Nature] in and take dimPlant[Plant] out.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Stepped layout' and set it to Off, +/- icons: On, so Group Nature and Nature get a column each with an expander on each group.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On with 'Per row level' On, so Total Module and Total Cell both appear and not only the grand total.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice. Row subtotals: On — that one adds the plants inside a single month, which is a real figure, and it is the Grand Total row the Excel sheet had.
- A nature reading Unassigned is a material the RM master does not carry — it is money the report will not silently file under someone else's nature. qcAttrMatch on Checks names them.
- Right-click a nature row → Drill through → Detail for the material-by-material list behind it.

**4.50** **Matrix** — The second block of the old sheet in days of cover: Module and Cell, each opening into its natures — cell cost, frame, glass, POE, wafer, paste, screens, gases and the rest — with a subtotal on each group and a grand total under them.

| Well | Field |
|---|---|
| Rows | `factInventory[GroupNature]`, `dimNature[Nature]` |
| Columns | `dimDate[MonthName]` |
| Values | `Days` → rename it to **Days** |
| Filters | `dimCategory[Category]  →  is RM`, `In Summary Window  →  is 1` |

Title: `RM Inventory by Group Nature and Nature — In Days`

Position: Horizontal 735, Vertical 208, Width 529, Height 220.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Fastest way to build the next block: click this matrix, Ctrl+C, Ctrl+V, then in Values swap the measure. Position, filters and formatting all come with the copy. Then in Rows drop factInventory[GroupNature] and dimNature[Nature] in and take dimPlant[Plant] out.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Stepped layout' and set it to Off, +/- icons: On, so Group Nature and Nature get a column each with an expander on each group.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On with 'Per row level' On, so Total Module and Total Cell both appear and not only the grand total.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice. Row subtotals: On — that one adds the plants inside a single month, which is a real figure, and it is the Grand Total row the Excel sheet had.
- A nature reading Unassigned is a material the RM master does not carry — it is money the report will not silently file under someone else's nature. qcAttrMatch on Checks names them.
- Right-click a nature row → Drill through → Detail for the material-by-material list behind it.

**4.51** **Clustered column chart** — Raw material held in crore rupees: one group per period along the bottom and the three plants side by side inside each group, so you read the months left to right and compare the plants within a month. It follows the pickers above, so it is four periods by default and up to twelve if you tick them.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Legend | `dimPlant[Plant]` |
| Y-axis | `Inventory Rs Cr` |
| Filters | `dimCategory[Category]  →  is RM`, `In Summary Window  →  is 1` |

Title: `RM Inventory (Rs Cr.) by Plant`

Position: Horizontal 192, Vertical 436, Width 529, Height 200.

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

**4.52** **Line and clustered column chart** — The same chart in days rather than rupees — how long each plant's raw material would last at its own capacity, three plant bars per month, and over them a line for the whole business: every plant's RM megawatts added together over every plant's capacity added together. The line is not the average of the three bars, and it is not their sum: it is one big plant's worth of days, which is the figure to quote for the company. Read together with the chart beside it, this tells you whether a bigger rupee figure is actually more stock or just a dearer month.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Column legend | `dimPlant[Plant]` |
| Column y-axis | `Days by Period` |
| Line y-axis | `RM Days All Plants by Period` |
| Filters | `dimCategory[Category]  →  is RM`, `In Summary Window  →  is 1` |

Title: `RM Inventory (Days) by Plant, with Total Days Across All Plants`

Position: Horizontal 735, Vertical 436, Width 529, Height 200.

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

**4.53** **Card** — The drill-through page opens already filtered to the bar or row you came from, so this card is that one number.

| Well | Field |
|---|---|
| Fields | `Inventory Rs Cr` |

Title: `Value ₹ Cr of What You Clicked`

Position: Horizontal 192, Vertical 16, Width 254, Height 96.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.

**4.54** **Card** — Same slice in megawatts.

| Well | Field |
|---|---|
| Fields | `Inventory MW` |

Title: `MW Held`

Position: Horizontal 453, Vertical 16, Width 254, Height 96.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.

**4.55** **Card** — Stock in MW divided by the MW capacity on the Variables sheet. With no category picked that MW is RM plus FG over the same capacity, so the two add up — the title says so rather than leaving a reader to assume it means FG alone. Blank where the plant has no capacity row — 1905.

| Well | Field |
|---|---|
| Fields | `Days of Inventory` |

Title: `Days of Inventory (RM + FG)`

Position: Horizontal 714, Vertical 16, Width 254, Height 96.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.

**4.56** **Card** — How big this slice is against the whole.

| Well | Field |
|---|---|
| Fields | `Share of Total %` |

Title: `Share of the Total`

Position: Horizontal 975, Vertical 16, Width 289, Height 96.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.

**4.57** **Pie chart** — RM / FG / consumables for exactly what you clicked.

| Well | Field |
|---|---|
| Legend | `dimCategory[Category]` |
| Values | `Inventory Rs Cr` |

Title: `Split by Category`

Position: Horizontal 192, Vertical 120, Width 347, Height 232.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Detail labels' and set Font size to 9. If a slice label is still cut off, set 'Position' to Outside, and switch on 'Overflow text' if your version offers it.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'. If the legend eats the chart, switch Legend off entirely — the labels already name the slices.
- In the Visualizations pane click the paintbrush icon, then click 'Detail labels', then 'Label contents' and set it to Category, percent of total.

**4.58** **Donut chart** — Which technology or material nature the slice is made of.

| Well | Field |
|---|---|
| Legend | `dimNature[Nature]` |
| Values | `Inventory Rs Cr` |

Title: `Split by Technology / Nature`

Position: Horizontal 546, Vertical 120, Width 347, Height 232.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Detail labels' and set Font size to 9. If a slice label is still cut off, set 'Position' to Outside, and switch on 'Overflow text' if your version offers it.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'. If the legend eats the chart, switch Legend off entirely — the labels already name the slices.
- In the Visualizations pane click the paintbrush icon, then click 'Detail labels', then 'Label contents' and set it to Category, percent of total.

**4.59** **Pie chart** — Where the slice sits. A single-colour pie means it is one plant already.

| Well | Field |
|---|---|
| Legend | `dimPlant[Plant]` |
| Values | `Inventory Rs Cr` |

Title: `Split by Plant`

Position: Horizontal 900, Vertical 120, Width 364, Height 232.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Detail labels' and set Font size to 9. If a slice label is still cut off, set 'Position' to Outside, and switch on 'Overflow text' if your version offers it.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'. If the legend eats the chart, switch Legend off entirely — the labels already name the slices.
- In the Visualizations pane click the paintbrush icon, then click 'Detail labels', then 'Label contents' and set it to Category, percent of total.

**4.60** **Matrix** — The line-item detail. A Matrix rather than a Table, so it opens nature → material instead of being one long flat list — that is the difference between clicking and scrolling.

| Well | Field |
|---|---|
| Rows | `dimNature[Nature]`, `factInventory[Material]`, `factInventory[MaterialDesc]` |
| Values | `Inventory Rs Cr`, `Inventory MW`, `Days`, `INR per Wp`, `Share of Total %` |

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

**4.61** **Card** — How many rows came out of RM Raw, FG Raw and Consble Raw together. Zero means pRoot is wrong or the three folders are named differently.

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

**4.62** **Card** — Zero here is the reason Inventory (TB) reads as empty on Summary: either the TB folder has no TB_YYYYMM.xlsx files, or the GL numbers in them match nothing on TB Master.

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

**4.63** **Card** — How many month-ends the stock files cover. One month means only one file was read, and then every monthly chart has a single bar however it is built.

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

**4.64** **Card** — More than three means the stock files carry a valuation area beyond the three plants; those now appear as 'Plant xxxx' rather than as a blank row.

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

**4.65** **Card** — The share of stock rows the master sheets do not cover. Anything above zero is what shows up as an Unassigned slice on the donuts and an Unassigned row in the technology matrix — the material numbers differ between the master sheet and the raw files.

| Well | Field |
|---|---|
| Fields | `Check Unassigned %` |

Title: `Value with No Nature (%)`

Position: Horizontal 1044, Vertical 56, Width 220, Height 88.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Callout value' (that is the big number) and set Font size to 24.
- If the list has a 'Category label' — the small grey wording Power BI prints under the number — set its Font size to 10, or switch it off, because the title above already says the same thing. The newer Card visual has no category label at all, so skip this line if you cannot see it.
- In the Visualizations pane click the paintbrush icon, then click 'Callout value', then 'Font' and set it to Arial, Font size: 14, Colour: #B3261E.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Effects', then 'Background' and set it to #FFFFFF.

**4.66** **Table** — One row per file actually read. If a month is missing from the report, it is missing from this list first — check the file is in the folder and is a real .xlsx.

| Well | Field |
|---|---|
| Columns | `qcHeaders[Folder]`, `qcHeaders[Name]`, `qcHeaders[SheetNames]` |

Title: `Every File the Four Folders Gave, with Its Sheets`

Position: Horizontal 192, Vertical 160, Width 533, Height 100.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 9, Colour: #14532D.

**4.67** **Table** — The workbook that carries RM Nature, FG Master, TB Master, Constants and MW. A sheet missing from this list, or showing 0 rows, is why the natures or the trial balance are empty.

| Well | Field |
|---|---|
| Columns | `qcVarHeaders[SheetName]`, `qcVarHeaders[DataRows]` |

Title: `Sheets Found in Variables and Calculations`

Position: Horizontal 731, Vertical 160, Width 533, Height 100.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 9, Colour: #14532D.

**4.68** **Table** — Empty is good. A long list here with 0 trial-balance rows above means TB Master is not matching your GL numbers at all, and the report is showing the whole trial balance rather than the inventory accounts.

| Well | Field |
|---|---|
| Columns | `factTB_Unmapped[GLAccount]`, `factTB_Unmapped[GLDesc]`, `factTB_Unmapped[Amount]` |

Title: `GL Accounts in the TB Files That TB Master Does Not List`

Position: Horizontal 731, Vertical 268, Width 533, Height 100.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 9, Colour: #14532D.

**4.69** **Table** — Each of these gets blank Days, because days of inventory divides by capacity. Add the technology to the MW sheet and it fills in by itself.

| Well | Field |
|---|---|
| Columns | `qcNatureNoCapacity[Nature]` |

Title: `FG Technologies with No Capacity on the MW Sheet`

Position: Horizontal 731, Vertical 376, Width 533, Height 100.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 9, Colour: #14532D.

**4.70** **Table** — The one table that explains an Unassigned donut. If RM Nature and FG Master hold thousands of materials but Matched is near zero, the two sides are keyed differently — compare the first eight numbers on each row and the difference is usually visible at a glance (a prefix, a suffix, a plant code stuck to the front).

| Well | Field |
|---|---|
| Columns | `qcAttrMatch[Source]`, `qcAttrMatch[DistinctMaterials]`, `qcAttrMatch[MatchedToStockFiles]`, `qcAttrMatch[FirstEight]` |

Title: `Do the Material Numbers Match Between the Sheets and the Files`

Position: Horizontal 192, Vertical 268, Width 533, Height 100.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 9, Colour: #14532D.

**4.71** **Table** — Sorted with the most negative first. An inventory account sitting there as a credit is why a plant's Inventory (TB) nets to nearly zero on Summary while the by-type block shows a large minus figure — the sign, not the mapping, is what is wrong.

| Well | Field |
|---|---|
| Columns | `qcTBByGL[GLAccount]`, `qcTBByGL[GLDesc]`, `qcTBByGL[Category]`, `qcTBByGL[AmountRsCr]` |

Title: `Trial Balance by GL Account, Signed`

Position: Horizontal 192, Vertical 592, Width 533, Height 100.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 9, Colour: #14532D.

**4.72** **Table** — The TB files carry a profit centre, not a plant, so every plant on the TB side of Summary is resolved from it. A blank or (none) in PlantResolved is a row Inventory (TB) leaves out — so if a plant shows on the MB5B side and not on the TB side, its profit centres are the ones sitting here unresolved, and the amount beside them is what is missing. Read me those profit centre codes and the rule that reads them becomes exact.

| Well | Field |
|---|---|
| Columns | `qcTBPlants[ProfitCentre]`, `qcTBPlants[Description]`, `qcTBPlants[PlantResolved]`, `qcTBPlants[InventoryRows]`, `qcTBPlants[AmountRsCr]` |

Title: `Trial Balance Profit Centres, and the Plant Each Resolved to`

Position: Horizontal 731, Vertical 592, Width 533, Height 100.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 9, Colour: #14532D.

**4.73** **Table** — There are three plants. Any other code here — 1903, 1904, 1908, or a blank valuation area — is a row the report leaves out rather than parking it on an Unallocated plant that does not exist, and the value beside it is exactly what leaving it out costs. If that figure is large, the code belongs to one of the three and the export is writing it differently; tell me which and it joins its plant.

| Well | Field |
|---|---|
| Columns | `qcPlantCodes[Code]`, `qcPlantCodes[Rows]`, `qcPlantCodes[ValueRsCr]`, `qcPlantCodes[InReport]` |

Title: `Every Plant Code the Stock Files Contain, and What It Is Worth`

Position: Horizontal 192, Vertical 484, Width 533, Height 100.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 9, Colour: #14532D.

**4.74** **Table** — Files of 1 on every row is what you want. A 2 means the same month came in twice — one export saved under two names, or a folder holding a partial file and a full one. Identical lines are removed before anything is counted, so the figures are right either way, but the file that should not be there is still worth deleting.

| Well | Field |
|---|---|
| Columns | `qcMonthFiles[Category]`, `qcMonthFiles[Month]`, `qcMonthFiles[Files]`, `qcMonthFiles[ValueRsCr]` |

Title: `Did Any Month Arrive from Two Files`

Position: Horizontal 731, Vertical 484, Width 533, Height 100.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 9, Colour: #14532D.

**4.75** **Table** — Empty is what you want. A row here is a material written twice on RM Nature or FG Master with a different nature each time; only the first of them can be used, so which nature the material gets depends on the order of the sheet. Delete the wrong row and refresh.

| Well | Field |
|---|---|
| Columns | `qcMasterDupes[Sheet]`, `qcMasterDupes[MatKey]`, `qcMasterDupes[TheyAre]`, `qcMasterDupes[Rows]` |

Title: `One Material with Two Natures on a Master Sheet`

Position: Horizontal 192, Vertical 376, Width 533, Height 100.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- In the Visualizations pane click the paintbrush icon, then click 'Column headers', then 'Font' and set it to Arial, Font size: 9, Colour: #14532D.

---

## Making it clickable

**4.76 Drill through.** On the `Detail` page click the empty area around the visuals so
nothing is selected, then drag these into the **Drill through** well of the
Visualizations pane (leave *Keep all filters* on):

- `dimPlant[Plant]`
- `dimDate[MonthName]`
- `dimCategory[Category]`
- `dimNature[Nature]`

That is the whole trick. A **Back** arrow appears on `Detail` by itself, and every bar,
row and slice on the other pages now offers **right-click → Drill through → `Detail`**,
which opens the pies filtered to whatever was clicked.

**4.77 Interactions.** A *left*-click needs no setup — it already cross-filters the rest
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
| searching `Value` in the Data pane finds nothing | Part 3 was done from an older guide, so the measure is called `Closing Value` | add all 78 from Appendix B, then delete the six old names listed in 3.7 |
| RM and FG matrices show numbers under `In ₹ Cr` but nothing under `In Days` | the `Days` measure was deleted as an "old name" | paste `Days = [Days of Inventory]` back in; it is in Appendix B |
| on a card, the number is fine but the wording is cut in half | the card's default text is too big for the space | set **Callout value** → Font size **24**, **General → Title** → Font size **12**, and Height **96** (every card in Part 4 is 96 high). A **Category label**, if your version has one, goes to **10** or off — the title says the same thing |
| the paintbrush list has a **Callout value** but no **Category label** | you are on the newer Card visual, which has no category label | nothing to fix: the heading comes from **General → Title → Text**, which Part 4 gives you the wording for |
| a measure exists but is named `Value  Cr` | the ₹ character was lost while pasting | right-click → Rename, type the name again |
| `There is already a measure with the name …`, and it names a table such as `dimMetric` | you have already pasted that measure — Power BI filed it under whichever table happened to be selected at the time, which changes nothing about how it works | press Escape to cancel, tick that measure off your list and move to the next one. To be sure of the formula, click the existing measure and compare the formula bar with the guide, overwriting it only if it differs. Never let a second copy be made: `Receipts ₹ Cr 2` is not a name any visual looks for |
| `The file is being used by another process` | an Excel file in the folders is open | close all Excel, end any stray `EXCEL.EXE` in Task Manager, delete any `~$...xlsx` file |
| `We couldn't find folder` | `pRoot` is wrong | copy the path from the File Explorer address bar; keep the quote marks, no trailing backslash |
| `Token Literal expected` | `pRoot` lost its quote marks | it must read `"C:\…\Inventory Report"`, quotes included |
| `Expression.Syntax Error` right after pasting | the whole appendix went into one query | one Blank Query per heading, 33 times |
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

1. **Queries.** Walk the 33 names in 1.3 against your Queries list. For a name you have,
   open **Advanced Editor**, Ctrl+A, paste the appendix version over it, **Done** — harmless
   even when nothing changed. For a name you do not have, create it. The ones most likely
   missing or stale: `dimDate`, `factInventory`, `factTB`, `factTB_Staged`, `varMWCapacity`,
   `dimCategory`, `dimMetric`, `dimMeasure`. Then **Close & Apply**.
2. **Relationships.** Manage relationships must match 2.3 exactly — 11 rows, all Single,
   nothing on `dimMetric` or `dimMeasure`.
3. **Measures.** Add all 78 from Appendix B top to bottom (adding beside old ones is safe),
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

        // one material number written the same way everywhere: no spaces, dots or hyphens,
        // upper case, no SAP leading zeros. The master sheets normalise identically, and a
        // key that differs only in punctuation is the usual reason a nature never matches.
        NormMat   = (v as any) as text =>
                        let Bare = Text.Select(Text.Upper(Text.From(v ?? "")),
                                       {"A".."Z", "0".."9"}),
                            Cut  = Text.TrimStart(Bare, "0")
                        in  if Cut = "" and Bare <> "" then "0" else Cut,
        Keys      = Table.TransformColumns(Kept, {
                        {"ValuationArea", each Text.Trim(Text.From(_ ?? "")), type text},
                        {"Material",      each NormMat(_), type text},
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

## fnVarSheetSafe

> Shared helper. Same as `fnVarSheet`, but a sheet it cannot find comes back as an empty table instead of stopping the refresh, so a workbook missing one master sheet still loads and the Checks page reports the gap. Create it straight after `fnVarSheet`.

```
let
    fnVarSheetSafe = (sheetAliases as list, columnAliases as list) as table =>
        try fnVarSheet(sheetAliases, columnAliases)
        otherwise #table({}, {})
in
    fnVarSheetSafe
```

## dimMaterialAttr

```
let
    Raw      = fnVarSheetSafe(
                   {"RM Nature", "RM Master", "RMNature", "RM"},
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
    // same normalisation as fnCleanMB5B, so the two sides of the join cannot disagree
    // over punctuation, case or SAP's leading zeros
    NormMat  = (v as any) as text =>
                   let Bare = Text.Select(Text.Upper(Text.From(v ?? "")),
                                  {"A".."Z", "0".."9"}),
                       Cut  = Text.TrimStart(Bare, "0")
                   in  if Cut = "" and Bare <> "" then "0" else Cut,
    // a sheet that is missing, or missing a column, comes through empty rather than failing
    // the whole refresh; qcAttrMatch and qcVarSheets on Checks then say so out loud
    Cols     = {"ValuationArea","Material","MaterialDescVar","Nature","GroupNature",
                "BOMStdQty","Item"},
    Padded   = List.Accumulate(List.Difference(Cols, Table.ColumnNames(Raw)), Raw,
                   (t, c) => Table.AddColumn(t, c, each null)),
    Keys     = Table.TransformColumns(Padded, {
                   {"ValuationArea", each Text.Trim(Text.From(_ ?? "")), type text},
                   {"Material",      each NormMat(_), type text}}),
    NoBlank  = Table.SelectRows(Keys, each [Material] <> null and [Material] <> ""),
    MatKey   = Table.AddColumn(NoBlank, "MatKey",
                   each [ValuationArea] & "|" & [Material], type text),
    // cell-by-cell with a fallback, so one oddly typed cell on the sheet cannot error the row
    // and take the whole master table down with it
    Typed    = Table.TransformColumns(MatKey, {
                   {"Nature",      each Text.Trim(Text.From(_ ?? "")), type text},
                   {"GroupNature", each Text.Trim(Text.From(_ ?? "")), type text},
                   {"BOMStdQty",   each try Number.From(_) otherwise null, type number},
                   {"Item",        each Text.Trim(Text.From(_ ?? "")), type text}}),
    // a third key, on the description, for the case where the sheet keys its rows by
    // material description rather than by number: unmatched rows fall back to it last
    Present  = Table.ColumnNames(Typed),
    WithDesc = if List.Contains(Present, "MaterialDescVar") then Typed
               else Table.AddColumn(Typed, "MaterialDescVar", each null, type text),
    DescKey  = Table.AddColumn(WithDesc, "DescKey",
                   each Text.Upper(Text.Trim(Text.From([MaterialDescVar] ?? ""))), type text),
    Slim     = Table.SelectColumns(DescKey,
                   {"MatKey","Material","DescKey","Nature","GroupNature","BOMStdQty","Item"}),
    Dedup    = Table.Distinct(Slim, {"MatKey"}),
    Buffered = Table.Buffer(Dedup)
in
    Buffered
```

## dimFGAttr

```
let
    Raw      = fnVarSheetSafe(
                   {"FG Master", "FM Master", "FG Nature", "FGMaster", "FG"},
                   {
                     {{"Valuation Area","Val Area","Plant","Valuation area"}, "ValuationArea"},
                     {{"Material","Material No","Material Number"},           "Material"},
                     {{"Material Description","Merterial Description","Material Desc",
                       "Material description"},                              "MaterialDescVar"},
                     {{"Nature","Tech","Technology"},                         "Nature"}
                   }),
    NormMat  = (v as any) as text =>
                   let Bare = Text.Select(Text.Upper(Text.From(v ?? "")),
                                  {"A".."Z", "0".."9"}),
                       Cut  = Text.TrimStart(Bare, "0")
                   in  if Cut = "" and Bare <> "" then "0" else Cut,
    Cols     = {"ValuationArea","Material","MaterialDescVar","Nature"},
    Padded   = List.Accumulate(List.Difference(Cols, Table.ColumnNames(Raw)), Raw,
                   (t, c) => Table.AddColumn(t, c, each null)),
    Keys     = Table.TransformColumns(Padded, {
                   {"ValuationArea", each Text.Trim(Text.From(_ ?? "")), type text},
                   {"Material",      each NormMat(_), type text},
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
                   {"EffectiveFrom", each if _ = null then #date(1900,1,1)
                                     else try DateTime.Date(DateTime.From(_))
                                          otherwise #date(1900,1,1), type date}}),
    // cell-by-cell with a fallback: one constant typed as text cannot error the row and take
    // the RM megawatt factor down with it
    Typed    = Table.TransformColumns(Filled, {
                   {"ConstantName", each Text.Trim(Text.From(_ ?? "")), type text},
                   {"Value",        each try Number.From(_) otherwise null, type number}}),
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

## dimPlantMaster

> The plants come from the **Plant Master** sheet of `Variables and Calculations.xlsx`, the same workbook that holds every other master. Three rows on that sheet, three plants in the report; add a plant there and it appears here without anyone opening Power Query. Enable load OFF - `dimPlant` is the table the report reads.

> If the sheet is missing, or is there with no rows under its headers, this returns nothing and `dimPlant` falls back to the three codes written into it, so the report still opens. `qcVarHeaders` on Checks is where you see which of the two happened.

```
let
    Raw     = fnVarSheetSafe(
                  {"Plant Master", "PlantMaster", "Plants", "Plant"},
                  {
                    {{"Valuation Area","Val Area","Plant Code","Code","Plant"}, "ValuationArea"},
                    {{"Plant Name","Name","Description","Plant Description",
                      "Valuation Area Description"}, "PlantName"},
                    {{"Sort","Order","Sort Order"}, "PlantSort"}
                  }),
    Cols    = {"ValuationArea", "PlantName", "PlantSort"},
    Padded  = List.Accumulate(List.Difference(Cols, Table.ColumnNames(Raw)), Raw,
                  (t, c) => Table.AddColumn(t, c, each null)),
    Slim    = Table.SelectColumns(Padded, Cols),
    // the code is text and trimmed, because 1900 read as a number will not join to a text key
    Keyed   = Table.TransformColumns(Slim, {
                  {"ValuationArea", each Text.Trim(Text.From(_ ?? "")), type text},
                  {"PlantName",     each Text.Trim(Text.From(_ ?? "")), type text}}),
    Real    = Table.SelectRows(Keyed, each [ValuationArea] <> ""),
    // the label the whole report shows: the code and the name together, so the slicer, the
    // legends and the ticker cards can never disagree about what a plant is called
    Label   = Table.AddColumn(Real, "Plant",
                  each if [PlantName] = "" then [ValuationArea]
                       else [ValuationArea] & " " & [PlantName], type text),
    Sorted  = Table.AddColumn(Label, "SortNo",
                  each try Number.From([PlantSort]) otherwise null, type number),
    Indexed = Table.AddIndexColumn(Sorted, "Seq", 1, 1, Int64.Type),
    Order   = Table.AddColumn(Indexed, "PlantSortNo",
                  each Int64.From([SortNo] ?? [Seq]), Int64.Type),
    Out     = Table.SelectColumns(Order, {"ValuationArea", "Plant", "PlantSortNo"})
in
    Out
```

## varPlantCodes

> Just the list of plant codes on the Plant Master sheet, so the fact queries can keep to them without each one re-reading the workbook. Falls back to the three codes if the sheet gave nothing. Enable load OFF.

```
let
    FromMaster = try List.Distinct(List.RemoveNulls(dimPlantMaster[ValuationArea]))
                 otherwise {},
    Out        = if List.Count(FromMaster) = 0 then {"1900", "1902", "1905"} else FromMaster
in
    Out
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
    // Third pass on the material description, for a master sheet that lists its rows by
    // description rather than by number. It only ever fills a row the first two passes left
    // empty, so it cannot overwrite a proper match.
    DescK    = Table.AddColumn(Both, "DescKey",
                   each Text.Upper(Text.Trim(Text.From([MaterialDesc] ?? ""))), type text),
    ByDesc   = Table.Buffer(Table.Distinct(Table.SelectRows(Table.SelectColumns(dimMaterialAttr,
                   {"DescKey","Nature","GroupNature","BOMStdQty","Item"}),
                   each [DescKey] <> null and [DescKey] <> ""), {"DescKey"})),
    Third    = Table.NestedJoin(DescK, {"DescKey"}, ByDesc, {"DescKey"},
                   "attr3", JoinKind.LeftOuter),
    All3     = Table.ExpandTableColumn(Third, "attr3",
                   {"Nature","GroupNature","BOMStdQty","Item"},
                   {"Nature3","GroupNature3","BOMStdQty3","Item3"}),
    Coal     = Table.AddColumn(All3, "NatureX",
                   each [Nature] ?? [Nature2] ?? [Nature3], type text),
    Coal2    = Table.AddColumn(Coal, "GroupNatureX",
                   each [GroupNature] ?? [GroupNature2] ?? [GroupNature3], type text),
    Coal3    = Table.AddColumn(Coal2, "BOMStdQtyX",
                   each [BOMStdQty] ?? [BOMStdQty2] ?? [BOMStdQty3], type number),
    Coal4    = Table.AddColumn(Coal3, "ItemX",
                   each [Item] ?? [Item2] ?? [Item3], type text),
    Dropped  = Table.RemoveColumns(Coal4, {"Nature","Nature2","Nature3",
                   "GroupNature","GroupNature2","GroupNature3",
                   "BOMStdQty","BOMStdQty2","BOMStdQty3","Item","Item2","Item3","DescKey"}),
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

    // Inr Wp = Closing Value / (MW * 10^6). A zero or missing MW is left blank rather than
    // divided by: dividing by zero in M produces NaN, which then prints as NaN in the report.
    INRwp    = Table.AddColumn(MW, "INR_WP",
                   each if [MW] = null or [MW] = 0 then null
                        else try [CloseVal] / ([MW] * 1000000) otherwise null, type number),

    Cleaned  = Table.RemoveColumns(INRwp, {"RateText"})
in
    Cleaned
```

## factConble

> Consumables carry no nature in any master sheet, so they are named here. Without this they
> arrive as null and show up as a `(Blank)` row in the technology split and on Detail.

```
let
    Src      = stgConble,
    Nature   = Table.AddColumn(Src, "Nature", each "Consumables", type text),
    Group    = Table.AddColumn(Nature, "GroupNature", each "Consumables", type text),
    Missing  = Table.AddColumn(Group, "AttrMissing", each false, type logical)
in
    Missing
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
    // last line of defence against a blank category: whatever slipped through above is
    // named, so no visual anywhere can show a nameless (Blank) row
    NoNulls  = Table.TransformColumns(Typed, {
                   {"Nature",      each if _ = null or _ = "" then "Unassigned" else _, type text},
                   {"GroupNature", each if _ = null or _ = "" then "Unassigned" else _, type text}}),
    // the plants are the ones on the Plant Master sheet, through varPlantCodes. A row whose
    // valuation area is blank, or is a code that sheet does not list, is dropped rather than
    // parked on an Unallocated row - there is no such plant and no such provision.
    // qcPlantCodes on Checks lists every code the files contained and what it was worth, so a
    // dropped row is never a silent one.
    Plants   = varPlantCodes,
    OnePlant = Table.SelectRows(NoNulls,
                   each List.Contains(Plants, Text.Trim(Text.From([ValuationArea] ?? "")))),
    Trimmed  = Table.TransformColumns(OnePlant, {
                   {"ValuationArea", each Text.Trim(Text.From(_)), type text}}),
    // Duplicates. The same stock line can arrive twice - the same month exported twice into
    // the same folder, or a file copied under a second name - and two identical lines would
    // double that material's stock. A row is treated as the same line when its plant,
    // material, month, special stock, unit and every figure agree; the file it came from is
    // deliberately not part of that test, which is what catches the same month in two files.
    // Two genuinely different lines for one material in one month (different batch, different
    // special stock) differ in at least one figure and are both kept.
    DedupKey = {"ValuationArea","Material","Month","SpecialStock","BaseUOM",
                "OpenQty","OpenVal","ReceiptQty","ReceiptVal","IssueQty","IssueVal",
                "CloseQty","CloseVal","Category"},
    OneEach  = Table.Distinct(Trimmed, DedupKey),
    // the megawatt column is renamed because Power BI will not let a table hold a column
    // and a measure with the same name, and the report needs the measure to be called MW
    Renamed  = Table.RenameColumns(OneEach, {{"MW", "MW Qty"}})
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
    // 'Consumables' and 'Unassigned' are written by the fact queries rather than read from a
    // master sheet, so they have to be listed here as well. A nature that a fact row carries
    // and this table does not is what draws a slice labelled (Blank).
    All     = List.Distinct(List.Combine({FromRM, FromFG, FromCap,
                  {"Consumables", "Unassigned"}})),
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
                     {{"Nature","NaturePlant","Nature Plant"},                "Nature"},
                     {{"Plant","Valuation Area","NaturePlant2"},              "TBPlant"},
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
    // Master columns are converted one cell at a time with a fallback, never with a straight
    // type cast. A sort column holding 1.5, a blank, a dash or the word "last" is a typing
    // habit on a spreadsheet, not a mistake in the data - but Int64.Type on any of them raises
    // a row error, and Power BI then reports "Errors in dimTBMaster" and drops the whole
    // whitelist, which is how eight perfectly good GL accounts stopped being inventory.
    Sortable = Table.TransformColumns(Slim, {
                   {"TBSort", each try Int64.From(Number.Round(Number.From(_))) otherwise null,
                    Int64.Type}}),
    Texted   = Table.TransformColumns(Sortable, {
                   {"GLAccount",    each Text.From(_ ?? ""),  type text},
                   {"GLDescMaster", each Text.From(_ ?? ""),  type text},
                   {"Nature",       each Text.Trim(Text.From(_ ?? "")), type text},
                   {"TBPlant",      each Text.Trim(Text.From(_ ?? "")), type text}}),
    Dedup    = Table.Distinct(Texted, {"GLAccount"})
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
    // the three named plant codes, written out here rather than read from dimPlant: a query
    // that opens a folder itself may not also reference another query, or the refresh stops
    // with 'references other queries or steps, so it may not directly access a data source'
    Known    = {"1900", "1902", "1905"},
    // The plant sat at characters 3-6 of the profit centre and nowhere else, so a profit
    // centre written to any other pattern lost its plant and the row was dropped - which is
    // how a whole plant went missing from Inventory (TB) while MB5B had it. Now: those four
    // characters first, then the first known code appearing anywhere in the profit centre,
    // then anywhere in its description. qcTBPlants on Checks shows what each one resolved to.
    Anywhere = (t as any) as nullable text =>
                   let Txt  = Text.From(t ?? ""),
                       Hits = List.Select(Known, each Text.Contains(Txt, _))
                   in  if List.IsEmpty(Hits) then null else Hits{0},
    PlantRaw = Table.AddColumn(Keys, "PlantCode",
                   each try Text.Middle([ProfitCentre], 2, 4) otherwise null, type text),
    PlantCol = Table.AddColumn(PlantRaw, "ValuationArea",
                   each if List.Contains(Known, [PlantCode]) then [PlantCode]
                        else if Anywhere([ProfitCentre]) <> null then Anywhere([ProfitCentre])
                        else Anywhere([ProfitCentreDesc]),
                   type text),
    // cell-by-cell, so an amount typed with a comma, a dash for nil, or a trailing CR/DR
    // cannot error the row and take the trial balance with it
    Typed    = Table.TransformColumns(PlantCol, {
                   {"Amount", each try Number.From(_)
                              otherwise try Number.From(Text.Select(Text.From(_ ?? ""),
                                             {"0".."9", ".", "-"}))
                              otherwise null, type number}}),

    // ---- the TB Master whitelist, read HERE and not in a later query -----------------------
    // Power Query's firewall forbids a query that references another query from also reaching
    // a data source, and it applies that test to the whole chain: factTB referencing both
    // factTB_Staged (which opens the TB folder) and dimTBMaster (which opens the workbook) is
    // exactly the combination it blocks, with 'references other queries or steps, so it may
    // not directly access a data source'. Doing the join in this query keeps both sources in
    // one place - a query may open as many sources as it likes as long as it leans on no other
    // query for data - so factTB and factTB_Unmapped below read nothing but this table.
    // fnVarSheet is a function, not data, so calling it here does not count as leaning.
    MasterRaw = try
                    fnVarSheet(
                        {"TB Master", "TBMaster", "TB"},
                        {
                          {{"GL Account Number","gl Account Number","GLAccountNumber",
                            "GL Account","G/L Account","GL No"},                  "GLAccount"},
                          {{"GL Account Description","GL Description","GLDescription",
                            "Account Description","Account Name"},                "GLDescMaster"},
                          {{"Nature","NaturePlant","Nature Plant"},               "Nature"},
                          {{"Plant","Valuation Area","NaturePlant2"},             "TBPlant"},
                          {{"Sort Order","SortOrder","Sort"},                      "TBSort"}
                        })
                otherwise #table({}, {}),
    MCols    = {"GLAccount","Nature","TBPlant","TBSort"},
    MPad     = List.Accumulate(List.Difference(MCols, Table.ColumnNames(MasterRaw)), MasterRaw,
                   (t, c) => Table.AddColumn(t, c, each null)),
    MKey     = Table.TransformColumns(MPad, {
                   {"GLAccount", each Text.TrimStart(Text.Trim(Text.From(_ ?? "")), "0"),
                    type text}}),
    MSort    = Table.TransformColumns(MKey, {
                   {"TBSort", each try Int64.From(Number.Round(Number.From(_))) otherwise null,
                    Int64.Type},
                   {"Nature",  each Text.Trim(Text.From(_ ?? "")), type text},
                   {"TBPlant", each Text.Trim(Text.From(_ ?? "")), type text}}),
    MReal    = Table.SelectRows(MSort, each [GLAccount] <> ""),
    // a plant code written on the master sheet itself, in the Plant column or inside the
    // NaturePlant text - the last resort when the profit centre carries no code at all
    MPlanted = Table.AddColumn(MReal, "MasterPlant",
                   each if Anywhere([TBPlant]) <> null then Anywhere([TBPlant])
                        else Anywhere([Nature]), type text),
    MKeep    = MCols & {"MasterPlant"},
    Master   = Table.Buffer(Table.Distinct(Table.SelectColumns(MPlanted, MKeep), {"GLAccount"})),
    Joined   = Table.NestedJoin(Typed, {"GLAccount"}, Master, {"GLAccount"},
                   "tpl", JoinKind.LeftOuter),
    Flagged  = Table.AddColumn(Joined, "Whitelisted",
                   each not Table.IsEmpty([tpl]), type logical),
    Widened  = Table.ExpandTableColumn(Flagged, "tpl",
                   {"Nature","TBPlant","TBSort","MasterPlant"}),
    Resolved = Table.AddColumn(Widened, "PlantResolved",
                   each [ValuationArea] ?? [MasterPlant], type text),
    Dropped  = Table.RemoveColumns(Resolved, {"ValuationArea"}),
    Renamed2 = Table.RenameColumns(Dropped, {{"PlantResolved", "ValuationArea"}}),
    // Rows that resolve to none of the three plants are kept HERE and left out in factTB, so
    // qcTBPlants can still see them: a plant going missing from Inventory (TB) has to be
    // visible somewhere, and a row silently dropped at this step is a row nobody can find.
    Out      = Table.TransformColumnTypes(Renamed2, {
                   {"Nature", type text}, {"TBPlant", type text}, {"TBSort", Int64.Type},
                   {"ValuationArea", type text}})
in
    Out
```


## dimPlant

> One row per plant, taken from the **Plant Master** sheet through `dimPlantMaster`, and kept to the plants the files actually contain. No Unallocated row and no blank member: a fact row whose valuation area is not one of these was left out upstream, and `qcPlantCodes` on Checks says what that cost.

```
let
    // written out only as the fallback for a Plant Master sheet that is missing or empty
    Fallback = #table(
        type table [ValuationArea = text, Plant = text, PlantSortNo = Int64.Type],
        {
            {"1900", "1900 Jaipur Module",  1},
            {"1902", "1902 Dholera Module", 2},
            {"1905", "1905 Dholera Cell",   3}
        }),
    Master   = try dimPlantMaster otherwise Fallback,
    Named    = if Table.IsEmpty(Master) then Fallback else Master,
    // codes present in the stock files or the trial balance. Only other queries are read
    // here and no folder is opened, which is what keeps the firewall quiet.
    Seen     = List.Distinct(List.RemoveNulls(
                   List.Combine({factInventory[ValuationArea], factTB_Staged[ValuationArea]}))),
    // a named plant with nothing behind it is left out, so the Plant slicer lists what the
    // files actually contain and not a fixed list padded with rows that pick nothing
    Live     = Table.SelectRows(Named, each List.Contains(Seen, [ValuationArea])),
    Kept     = if Table.IsEmpty(Live) then Named else Live,
    Dedup    = Table.Distinct(Kept, {"ValuationArea"}),
    Ren      = Table.RenameColumns(Dedup, {{"PlantSortNo", "PlantSort"}}),
    Typed    = Table.TransformColumnTypes(Ren, {
                   {"ValuationArea", type text}, {"Plant", type text},
                   {"PlantSort", Int64.Type}})
in
    Typed
```

## factTB

> The whitelist against `TB Master` happens in `factTB_Staged`, which is where the trial balance is read - see the note there for why. This query keeps the accounts that matched and works out `Category` from the Nature text, so the trial balance and MB5B can be compared on the same RM / FG / Consumables row. A GL account that is not on `TB Master` is not inventory and is not counted here; `factTB_Unmapped` and `qcTBByGL` name every one of them.

```
let
    // whitelisted by TB Master, and resolving to one of the three plants. No Unallocated:
    // a row whose profit centre names no plant is left out rather than parked on a plant that
    // does not exist, and qcTBPlants on Checks is where those rows are accounted for.
    Kept    = Table.SelectRows(factTB_Staged,
                  each [Whitelisted] = true and [ValuationArea] <> null),
    // RM / FG / Consumables from whatever the Nature (or GL description) says
    // Raw material is tested BEFORE consumables, and that order matters: an account called
    // "Raw Material & Packing" holds the word PACK, so with consumables tested first the whole
    // of RM was filed under Consumables and the RM row vanished from Inventory (TB) while
    // Consumables read far too high. Packing on its own still lands in Consumables.
    Bucket  = (n as any, d as any) as text =>
                  let T = Text.Upper(Text.From(n ?? "") & " " & Text.From(d ?? "")) in
                  if Text.Contains(T, "FINISH") or Text.Contains(T, "FG")
                      then "FG"
                  else if Text.Contains(T, "RAW") or Text.Contains(T, "RM")
                      or Text.Contains(T, "WIP") or Text.Contains(T, "SEMI")
                      then "RM"
                  else if Text.Contains(T, "CONSUM") or Text.Contains(T, "STORE")
                      or Text.Contains(T, "SPARE") or Text.Contains(T, "PACK")
                      then "Consumables"
                  else "RM",
    Cat     = Table.AddColumn(Kept, "Category",
                  each Bucket([Nature], [GLDesc]), type text),
    // exact column list and types, so the table is the same shape every refresh
    Wanted  = {"SourceFile","Month","GLAccount","GLDesc","ProfitCentre","ProfitCentreDesc",
               "Amount","PlantCode","ValuationArea","Nature","TBPlant","TBSort","Category"},
    Padded  = List.Accumulate(List.Difference(Wanted, Table.ColumnNames(Cat)), Cat,
                  (t, c) => Table.AddColumn(t, c, each null)),
    Slim    = Table.SelectColumns(Padded, Wanted),
    Typed   = Table.TransformColumnTypes(Slim, {
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

> GL accounts present in the raw TB but absent from `TB Master`. Empty = good. This is what stops a new GL account silently vanishing - and, just as important, what stops a fixed-asset account being counted as inventory. It reads the same `Whitelisted` flag as `factTB`, so the two can never disagree.

```
let
    Out   = Table.SelectRows(factTB_Staged, each [Whitelisted] = false),
    Group = Table.Group(Out, {"GLAccount","GLDesc"},
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

## qcAttrMatch

> Answers one question: are the material numbers in the stock files the same numbers as in RM Nature and FG Master? `Matched` near zero with a healthy `Distinct` on both sides means the two sheets are keyed differently - read me the samples. Leave Enable load ON.

```
let
    MB5B    = List.Distinct(List.RemoveNulls(factInventory[Material])),
    RM      = List.Distinct(List.RemoveNulls(dimMaterialAttr[Material])),
    FG      = List.Distinct(List.RemoveNulls(dimFGAttr[Material])),
    Sample  = (l as list) as text =>
                  Text.Combine(List.Transform(List.FirstN(List.Sort(l), 8), Text.From), " | "),
    // the same question again on the description, because a master sheet keyed by description
    // rather than by material number would show Matched near zero above and healthy here
    MB5BD   = List.Distinct(List.RemoveNulls(List.Transform(factInventory[MaterialDesc],
                  each Text.Upper(Text.Trim(Text.From(_ ?? "")))))),
    RMD     = List.Distinct(List.RemoveNulls(List.Transform(dimMaterialAttr[DescKey],
                  each Text.Upper(Text.Trim(Text.From(_ ?? "")))))),
    Rows    = {
        {"Stock files (MB5B)", List.Count(MB5B), null, Sample(MB5B)},
        {"RM Nature sheet",    List.Count(RM),
         List.Count(List.Intersect({RM, MB5B})), Sample(RM)},
        {"FG Master sheet",    List.Count(FG),
         List.Count(List.Intersect({FG, MB5B})), Sample(FG)},
        {"Stock files - descriptions", List.Count(MB5BD), null, Sample(MB5BD)},
        {"RM Nature - descriptions",   List.Count(RMD),
         List.Count(List.Intersect({RMD, MB5BD})), Sample(RMD)}
    },
    T       = Table.FromRows(Rows,
                  type table [Source = text, DistinctMaterials = Int64.Type,
                              MatchedToStockFiles = Int64.Type, FirstEight = text])
in
    T
```

## qcPlantCodes

> Every valuation area the stock files actually contain, with its rows and its closing value, before the three-plant rule is applied. A code here that is not 1900 / 1902 / 1905 is a row the report leaves out, so this is where you see what leaving it out costs. Leave Enable load ON.

```
let
    Src     = Table.Combine({factRM, factFG, factConble}),
    Coded   = Table.AddColumn(Src, "Code",
                  each Text.Trim(Text.From([ValuationArea] ?? "")), type text),
    Named   = Table.TransformColumns(Coded, {
                  {"Code", each if _ = "" then "(blank)" else _, type text}}),
    Grouped = Table.Group(Named, {"Code"}, {
                  {"Rows",     each Table.RowCount(_), Int64.Type},
                  {"ValueRsCr", each List.Sum(List.Transform(_[CloseVal],
                                    each _ ?? 0)) / 10000000, type number}}),
    Flagged = Table.AddColumn(Grouped, "InReport",
                  each List.Contains({"1900","1902","1905"}, [Code]), type logical),
    Sorted  = Table.Sort(Flagged, {{"ValueRsCr", Order.Descending}})
in
    Sorted
```

## qcMonthFiles

> One row per category and month, with how many files it came from. `Files` of 1 everywhere is what you want. A 2 means the same month arrived twice - the same export saved under two names, or a folder holding both a partial and a full file - and the duplicate lines are removed before anything is counted, but the file that should not be there is still worth deleting. Leave Enable load ON.

```
let
    Src     = factInventory,
    Grouped = Table.Group(Src, {"Category", "Month"}, {
                  {"Files",     each List.Count(List.Distinct([SourceFile])), Int64.Type},
                  {"FileNames", each Text.Combine(
                                    List.Transform(List.Distinct([SourceFile]), Text.From),
                                    " | "), type text},
                  {"Rows",      each Table.RowCount(_), Int64.Type},
                  {"ValueRsCr", each List.Sum(List.Transform([CloseVal], each _ ?? 0))
                                    / 10000000, type number}}),
    Sorted  = Table.Sort(Grouped, {{"Files", Order.Descending}, {"Month", Order.Descending}})
in
    Sorted
```

## qcMasterDupes

> Master rows that contradict each other: one material carrying two different natures on the RM or FG sheet. Only one of them can be used - the first - so this is the list to clean up on the sheet itself, and until it is, the nature a material gets depends on which row Excel happens to hold first. Empty is what you want. Leave Enable load ON.

```
let
    NormMat = (v as any) as text =>
                  let Bare = Text.Select(Text.Upper(Text.From(v ?? "")), {"A".."Z", "0".."9"}),
                      Cut  = Text.TrimStart(Bare, "0")
                  in  if Cut = "" and Bare <> "" then "0" else Cut,
    Read    = (sheet as list, label as text) as table =>
        let
            Raw    = fnVarSheetSafe(sheet, {
                         {{"Valuation Area","Val Area","Plant","Valuation area"}, "ValuationArea"},
                         {{"Material","Material No","Material Number"},           "Material"},
                         {{"Nature","Tech","Technology"},                         "Nature"}
                     }),
            Cols   = {"ValuationArea","Material","Nature"},
            Padded = List.Accumulate(List.Difference(Cols, Table.ColumnNames(Raw)), Raw,
                         (t, c) => Table.AddColumn(t, c, each null)),
            Slim   = Table.SelectColumns(Padded, Cols),
            Keys   = Table.TransformColumns(Slim, {
                         {"ValuationArea", each Text.Trim(Text.From(_ ?? "")), type text},
                         {"Material",      each NormMat(_), type text},
                         {"Nature",        each Text.Trim(Text.From(_ ?? "")), type text}}),
            Real   = Table.SelectRows(Keys, each [Material] <> ""),
            Keyed  = Table.AddColumn(Real, "MatKey",
                         each [ValuationArea] & "|" & [Material], type text),
            Named  = Table.AddColumn(Keyed, "Sheet", each label, type text)
        in
            Table.SelectColumns(Named, {"Sheet","MatKey","Nature"}),
    RM      = Read({"RM Nature", "RM Master", "RMNature", "RM"}, "RM Nature"),
    FG      = Read({"FG Master", "FM Master", "FG Nature", "FGMaster", "FG"}, "FG Master"),
    Both    = Table.Combine({RM, FG}),
    Grouped = Table.Group(Both, {"Sheet","MatKey"}, {
                  {"Natures",  each List.Count(List.Distinct([Nature])), Int64.Type},
                  {"TheyAre",  each Text.Combine(List.Distinct([Nature]), " | "), type text},
                  {"Rows",     each Table.RowCount(_), Int64.Type}}),
    Clashes = Table.SelectRows(Grouped, each [Natures] > 1),
    Sorted  = Table.Sort(Clashes, {{"Sheet", Order.Ascending}, {"MatKey", Order.Ascending}})
in
    Sorted
```

## qcTBByGL

> Every GL account the trial balance brought in, with the nature TB Master gives it and its signed total. This is where a credit-balance GL shows itself: an inventory account with a negative total is the reason a plant's TB nets to zero. Leave Enable load ON.

```
let
    Grouped = Table.Group(factTB, {"GLAccount", "GLDesc", "Nature", "Category"}, {
                  {"AmountRsCr", each List.Sum([Amount]) / 10000000, type number},
                  {"Rows", each Table.RowCount(_), Int64.Type}}),
    Sorted  = Table.Sort(Grouped, {{"AmountRsCr", Order.Ascending}}),
    Typed   = Table.TransformColumnTypes(Sorted, {
                  {"GLAccount", type text}, {"GLDesc", type text},
                  {"Nature", type text}, {"Category", type text}})
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

## qcTBPlants

> Every profit centre the trial balance files contain, with the plant the report resolved it to and what it is worth. A blank `PlantResolved` is a row Inventory (TB) leaves out - so if a plant is missing from Summary while MB5B has it, this table names the profit centres that did not resolve, and the fix is a rule, not a guess. Leave Enable load ON.

```
let
    Src     = factTB_Staged,
    Named   = Table.TransformColumns(Src, {
                  {"ProfitCentre", each if Text.From(_ ?? "") = "" then "(blank)" else _,
                   type text}}),
    Grouped = Table.Group(Named, {"ProfitCentre"}, {
                  {"Description", each Text.From(List.First([ProfitCentreDesc]) ?? ""), type text},
                  {"PlantResolved", each Text.Combine(
                                        List.Transform(List.Distinct([ValuationArea]),
                                            each Text.From(_ ?? "(none)")), " | "), type text},
                  {"Rows", each Table.RowCount(_), Int64.Type},
                  {"InventoryRows", each List.Count(List.Select([Whitelisted], each _ = true)),
                   Int64.Type},
                  {"AmountRsCr", each List.Sum(List.Transform([Amount], each _ ?? 0)) / 10000000,
                   type number}}),
    Sorted  = Table.Sort(Grouped, {{"PlantResolved", Order.Ascending},
                                   {"AmountRsCr", Order.Descending}})
in
    Sorted
```

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
INR per Wp = DIVIDE(SUM(factInventory[CloseVal]), SUM(factInventory[MW Qty]) * 1000000)
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

These next two do the same for megawatts and for finished goods. They exist because a visual
with no month on it - the two Overview donuts, the FG technology bars, the FG plant donut -
cannot be pinned to the latest month by a filter on a measure: the filter is evaluated once for
the whole visual, so every month still lands in it and the figures read three or four times too
high. A measure that sets the month itself is the only thing that holds.

```
Latest Month MW =
VAR LastIdx = CALCULATE(MAX(dimDate[MonthIndex]), ALLSELECTED(dimDate))
RETURN CALCULATE([MW], FILTER(ALL(dimDate), dimDate[MonthIndex] = LastIdx))
```

```
Latest Month FG ₹ Cr =
VAR LastIdx = CALCULATE(MAX(dimDate[MonthIndex]), ALLSELECTED(dimDate))
RETURN CALCULATE([FG ₹ Cr], FILTER(ALL(dimDate), dimDate[MonthIndex] = LastIdx))
```

*trial balance reconciliation*

```
TB ₹ Cr = ROUND(DIVIDE(SUM(factTB[Amount]), 10000000), 2)
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
VAR LastM = MAX(dimDate[MonthIndex])
VAR Closing = CALCULATE([Value ₹ Cr], dimDate[MonthIndex] = LastM)
RETURN IF(ISINSCOPE(dimDate[MonthName]), [Value ₹ Cr], Closing)

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
    IF(Place <= 12, 1, 0),
    IF(Alive > 0 && (Me = MarchIdx || Place <= 3), 1, 0)
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
VAR LastM = MAX(dimDate[MonthIndex])
VAR Closing = CALCULATE([RM Days All Plants], dimDate[MonthIndex] = LastM)
RETURN IF(ISINSCOPE(dimDate[MonthName]), [RM Days All Plants], Closing)

Inventory MW =
VAR LastM = MAX(dimDate[MonthIndex])
VAR Closing = CALCULATE([MW], dimDate[MonthIndex] = LastM)
RETURN IF(ISINSCOPE(dimDate[MonthName]), [MW], Closing)

In Last 12 =
VAR LastM = [Latest Month Index]
VAR ThisM = MAX(dimDate[MonthIndex])
RETURN IF(ThisM > LastM - 12 && ThisM <= LastM, 1, 0)

Summary Value Rs Cr =
VAR LastM = MAX(dimDate[MonthIndex])
VAR Closing = CALCULATE([Summary Value ₹ Cr], dimDate[MonthIndex] = LastM)
RETURN IF(ISINSCOPE(dimDate[MonthName]), [Summary Value ₹ Cr], Closing)

TB Inventory Rs Cr =
VAR LastM = MAX(dimDate[MonthIndex])
VAR Closing = CALCULATE([TB ₹ Cr], dimDate[MonthIndex] = LastM)
RETURN IF(ISINSCOPE(dimDate[MonthName]), [TB ₹ Cr], Closing)

Difference Inventory Rs Cr = [TB Inventory Rs Cr] - [Inventory Rs Cr]

Difference Inventory % =
VAR Books = [TB Inventory Rs Cr]
RETURN IF(ABS(Books) < 0.05, BLANK(), DIVIDE([Difference Inventory Rs Cr], Books))

Unit Value by Period =
VAR LastM = MAX(dimDate[MonthIndex])
VAR Closing = CALCULATE([Unit Value], dimDate[MonthIndex] = LastM)
RETURN IF(ISINSCOPE(dimDate[MonthName]), [Unit Value], Closing)

In Latest Month =
IF(MAX(dimDate[MonthIndex]) = [Latest Month Index], 1, 0)

Days by Period =
VAR LastM = MAX(dimDate[MonthIndex])
VAR Closing = CALCULATE([Days], dimDate[MonthIndex] = LastM)
RETURN IF(ISINSCOPE(dimDate[MonthName]), [Days], Closing)

Check MB5B Rows = COUNTROWS(factInventory)

Check TB Rows = COUNTROWS(factTB)

Check Months of Data = DISTINCTCOUNT(factInventory[Month])

Check Plant Codes = DISTINCTCOUNT(factInventory[ValuationArea])

Check Unassigned % =
VAR Unnamed =
    CALCULATE(
        SUM(factInventory[CloseVal]),
        factInventory[Nature] IN {"Unassigned", "(blank)"}
    )
RETURN
DIVIDE(Unnamed, SUM(factInventory[CloseVal]))

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
the TB folder produced nothing or TB Master matched none of its GL accounts.

`Check Unassigned %` is deliberately weighted by **value, not by row count**. Counted by rows it
read 2.6% while every rupee of raw material and finished goods was unnamed - consumables are tens
of thousands of rows and a few crore, raw materials are a few hundred rows and hundreds of crore,
so the row-count version says the mapping is nearly fine when it is not. Weighted by value it says
what share of the money on the report has no nature, which is the number that matters.

`Latest Month Value ₹ Cr`, `Latest Month MW` and `Latest Month FG ₹ Cr` are for the visuals
whose axis is **not** a period — the two Overview donuts, the FG technology bars and the FG
plant donut. Each one sets the newest month with data itself. This is deliberate and it matters:
the older way, a filter reading the `In Latest Month` measure, is evaluated once for the whole
visual, so all four ticked months still landed in it and those visuals read three or four times
too high. Use the Latest Month measure and put no period field and no month filter on those
four visuals.

`Inventory Rs Cr` and `Inventory MW` are the level-aware pair the **Detail** page reads. Detail
is reached by drilling from a month, but it can also be opened on its own with four months in
context, and `Value ₹ Cr` would then add four month-ends together - which is where the 5,393 on a
1,433 report came from. Both hand back the month-end at month grain and the average of the
month-ends at any wider grain.

`Days by Period` is `Days` with the quarter rule, and the RM page's days chart uses it. Days is
a ratio of two stock figures, so at a quarter grain it has to be the average of the quarter's three
month-end ratios; adding them would give a nonsense number three times too big.

### Changed in build 22

**One matrix per metric, laid out like the sheets these pages replace.** Build 21 kept the month
as the only column field but hung three measures underneath it, so a period read
`Apr'26 | TB | MB5B | Difference` - the right numbers in the wrong order for anyone who knows the
Excel. The Excel puts the metric outside the month: an `IN MW` block, an `IN CRS` block and an
`IN DAYS` block, each with its own row of months. Getting that from one matrix needs a two-level
column hierarchy, which is exactly what Desktop drew as an empty card. So each metric is now its
own matrix with `dimDate[MonthName]` as its only column field, and they sit side by side: Summary
carries `Inventory (TB)`, `As per MB5B` and `Check`, each over four months, with the same three
across all plants beneath them; FG carries In MW, In Rs Cr and In Days by plant and again by
technology; RM carries In Rs Cr and In Days by plant and again by group nature and nature. Ten
visuals where there were four, no hierarchy anywhere, and nothing to expand.

**No Total column on any of them, and a total is never a sum across time.** Inventory is a level,
not a flow: a Total column across March and July counts the same steel twice, so column subtotals
are off on every matrix. The Total row stays - that one adds the plants inside a single month,
which is a real figure and is the Grand Total the Excel sheet had. `Inventory Rs Cr`,
`Inventory MW`, `TB Inventory Rs Cr`, `Summary Value Rs Cr`, `Days by Period`,
`Unit Value by Period` and `RM Days All Plants by Period` no longer average the month-ends at a
wider grain either: they hand back the **closing** month's level, because the total inventory of a
window of months is what was on hand at the end of it.

### Changed in build 21

**No matrix has a two-level column hierarchy any more.** A matrix with a metric field above a
month field opens on the metric level - one figure per metric, no months - and the file's attempt
to pre-open it made Desktop draw the visual as an empty card instead: that is what took Summary's
lower block and the FG and RM tables off the page. Every matrix now has the month as its only
column field, with the metrics as measures side by side underneath and a short per-visual name on
each (`TB`, `MB5B`, `Difference`; `MW`, `Rs Cr.`, `Days`). Same grid, read the other way, and
nothing to expand.

**FG by technology is money on the bars with megawatts as a line.** It was megawatts alone, and a
technology only has megawatts where the MW Capacity sheet covers it, so the chart looked empty.
Every technology has a value, so the bars are always there and the line appears where a capacity
figure exists.

### Changed in build 20

**No forced type casts on the master sheets.** *Errors in dimTBMaster* on all eight rows was a
`Int64.Type` cast on the sort column: a blank, a dash, `1.5` or a number stored as text errors the
whole row, and what is lost is the whitelist of inventory GL accounts - so Inventory (TB) reads
empty. Every master column in `dimTBMaster`, `dimMaterialAttr`, `varConstants` and the trial
balance's own amount is now converted cell by cell with a fallback, so an oddly typed cell becomes a
blank instead of an error. A spreadsheet typed by hand is allowed to be untidy; the report has to
cope with it.

**The site has an Edits tab.** Every one of these fixes is there as find-this / replace-with-this
inside one named query, with a copy button on each box, so a report that is already built can be
corrected in place - no new download, and nothing typed out of a message.

### Changed in build 19

**The refresh error you hit is the privacy firewall, and step 1.4 of this guide now turns it off.**
*"Query 'factTB' (step 'Typed') references other queries or steps, so it may not directly access a
data source"* is Power Query refusing to let a folder source and a workbook source meet - which is
the whole point of the report, because the figures come from the folders and the names come from
`Variables and Calculations`. It only appeared now because `TB Master` finally has rows in it, so
the join actually runs. **File → Options → GLOBAL → Privacy → "Always ignore Privacy Level
settings"**, then the same under **CURRENT FILE**, then Refresh.

**The trial balance no longer needs that pairing at all.** `factTB_Staged` now reads the folder and
the `TB Master` whitelist in the one query - a query may open as many sources as it likes, it just
may not lean on another query for data - and `factTB` and `factTB_Unmapped` read nothing but the
staged table and its `Whitelisted` flag. That removes the exact combination the error named. The
other pairings in the model (natures onto stock, plant names, the nature list) are legitimate and
still need the setting above.

### Changed in build 18

All of this is about repeated data, now that the master sheets are filled in.

**A stock line that arrives twice is counted once.** `factInventory` treats two rows as the same
line when the plant, material, month, special stock, unit and every figure agree - and deliberately
ignores which file they came from, which is what catches the same month exported twice into one
folder. Two genuinely different lines for one material in a month (a different batch, a different
special stock) differ in at least one figure and are both kept, so nothing real is lost.

**One master row per material, on FG as well as RM.** Both sheets are reduced to one row per
valuation area + material before anything joins to them, so a material written twice on the sheet
cannot multiply that material's stock.

**`qcMasterDupes` names the contradictions.** If a material appears twice with two *different*
natures, only the first can be used, and which one that is depends on the order of the sheet. That
table lists every such material and both natures, so the sheet can be cleaned rather than guessed
at. Empty is what you want.

**`qcMonthFiles` says whether a month came from two files.** One row per category and month with the
count of files behind it. The figures are right either way now that duplicates are removed, but a
month showing 2 means there is a file in the folder that should not be there.

### Changed in build 17

Read straight off your Checks page, so each line is a fact from your own refresh rather than a
preference.

**The month columns now open under TB, MB5B and Difference.** A matrix opens on the outer level of
its column hierarchy, so TB / MB5B / Difference showed one figure each and that figure was the
window, not a month - which is what looked like the months being added together. Both hierarchies
are written out expanded with `root.isToggled`, the part build 12 left out when the same change
drew four matrices as empty cards. Summary is exactly: three plants as rows, each opening into RM /
FG / Consumables; TB / MB5B / Difference as the three master columns; the newest March and the three
months after it under each of them; no Total column, because a total across unlike columns is not a
number.

**The plants come from the Plant Master sheet.** Your workbook has one with three rows, and
`dimPlantMaster` reads it - code, name and sort order - so the plant list is master data like
everything else rather than three lines written into a query. If that sheet is missing or empty the
three codes are still there as a fallback.

**The trial balance stops counting fixed assets as inventory.** `TB Master` matched none of your GL
accounts, and `factTB` had a fallback that kept every row when the whitelist matched nothing - so
GL 1000006 Buildings (₹1,977.80 Cr), 1000007 Plant & Machinery - Wind and 1000008 Plant & Machinery
- Solar were all being read as raw-material inventory. That fallback is gone. Inventory (TB) is
empty until `TB Master` lists your inventory GLs, and `factTB_Unmapped` and `qcTBByGL` name every
account that fell out. An empty column is a visible gap; a trial balance full of fixed assets is a
wrong number that looks right.

**`Check Unassigned %` is weighted by value, not by rows.** It read 2.6% while every rupee of raw
material and finished goods was unnamed: consumables are tens of thousands of rows and a few crore,
raw materials are a few hundred rows and hundreds of crore. Weighted by value the card says what
share of the money on the report has no nature.

### Changed in build 16

**There is no Unallocated plant.** Not in `dimPlant`, not in the facts, nowhere. A stock row whose
valuation area is blank, or is a code that is not 1900 / 1902 / 1905, is left out rather than parked
on a plant that does not exist, and a trial-balance row whose profit centre does not resolve to one
of the three is left out the same way.

**Nothing is dropped silently.** The new `qcPlantCodes` on Checks lists every valuation area the
stock files actually contained, its row count, its closing value in ₹ Cr, and whether the report
kept it. If a code outside the three is carrying real money, that is the line that says so.

**The by-plant tables open on March plus the last three months.** `In Summary Window` now pins the
newest March that has data and adds the three most recent months to it, the same rule Overview's
table already used, so Summary, FG and RM all open on four columns beginning with the year-end
close. Ticking months yourself still replaces that entirely.

### Changed in build 15

Built against the real workbook you sent, whose sheets are `RM Nature` and `TB Master` with the
headers `Valuation Area | Material | Material description | Nature | Group Nature | BOM Std Qty |
Item` and `Company Code | Co Code description | gl Account Number | GL Account Description |
Profit Centre | Profit Center Description | NaturePlant | at`.

**Every one of those headers is now recognised**, `NaturePlant` included - the TB master's nature
column was being read as missing because the guide looked for `Nature` and `Plant` as two columns.

**A missing master sheet loads empty instead of failing.** `fnVarSheetSafe` is the new helper: the
workbook you sent has no `FG Master` sheet at all, and the old code would have stopped the refresh
on it. The same goes for a master sheet that is missing a column - it comes through blank, and
`qcVarHeaders` on Checks names it.

**`qcVarHeaders` is the sheet that settles this question.** It prints every sheet in the workbook,
its exact headers, and its **DataRows**. If `RM Nature` shows `DataRows` of 0 - which is what the
copy you sent contains, a header row and nothing under it - then no report can name a material,
because there is nothing to name it from. That is a data question, not a report question, and it is
the first line to read after a refresh.

### Changed in build 14

All of this is about one thing: `Variables and Calculations.xlsx` is the master, and the MB5B
export has to meet it.

**The material key keeps only letters and digits.** It was stripping spaces, dots, hyphens,
slashes and underscores; it now keeps `A-Z` and `0-9` and throws away everything else, which
covers the non-breaking spaces, tab characters, commas and brackets that Excel and SAP put into a
cell without showing them. Leading zeros are still stripped, and a material that is genuinely `0`
stays `0` instead of becoming empty.

**A third match, on the material description.** If the master sheet keys its rows by description
rather than by number, the first two passes cannot match anything. The third pass joins on the
description, and only ever fills a row the first two left empty, so it can never overwrite a
proper match.

**`qcAttrMatch` asks the same question about descriptions.** Two more rows, so the Checks page now
says whether the two sides meet on the number, on the description, or on neither - which is the
one fact that decides where the mapping goes next.

### Changed in build 13

Five of these are build 12's own damage, and I would rather say so plainly.

**The four missing matrices are back.** Build 12 wrote an expansion state on the column
hierarchy of every matrix. On the four whose rows are a single level - `Total Across All Plants`
on Summary, both FG matrices and `RM Inventory by Plant` - Desktop answered by drawing an empty
white card. Only the row hierarchy is written out now, which is all that was ever needed.

**The Total column appears only where the columns are months.** On Summary it was adding
Inventory (TB) + Inventory (MB5B) + Difference together and printing the result as a total, which
is three unlike things in one number. Overview's Inventory by Month keeps its Total column,
because there a total across the columns is the inventory of the window.

**There are three plants.** 1903, 1904 and 1908 turn up in the exports and are not plants;
`factInventory` sends those rows to `Unallocated`, keeping their value, and `dimPlant` lists the
three plants plus `Unallocated` if anything landed there. The plant is labelled with its code -
`1900 Jaipur Module` - so the slicer, the legends and the ticker cards all read the same.

**`dimNature` carries `Consumables` and `Unassigned`.** Both are written by the fact queries
rather than read from a master sheet, so the bridge table did not have them and a fifth of the
Detail donut came out as `(Blank)`.

**The megawatt figures sit above their bars.** Inside the bar a dark figure on dark green cannot
be read, which is what the Overview MW strip looked like. The `% vs last month` line has been
taken off that chart - it was never asked for and it was the second thing crowding it.

**Detail is level-aware.** Its cards, its three pies and its matrix read `Inventory Rs Cr` and
`Inventory MW`, so opening the page with four months in context averages the month-ends instead
of adding them - the 5,393 against a 1,433 report.

**The trial balance stops printing 3.8E-13.** `TB ₹ Cr` is rounded to the paisa, and
`Difference Inventory %` is blank rather than a twenty-digit percentage when the books side is
zero, which it is while TB Master matches none of your GL accounts.

### Changed in build 12

Everything here came out of the Power BI screenshots, so each line is a thing that was visibly
wrong on screen rather than a preference.

**Material numbers are normalised the same way on both sides.** The RM Nature and FG Master
sheets read their material as text with the leading zeros gone; the MB5B files keep them. So
`000000001010203` never met `1010203`, every fact row fell through to `Unassigned`, and with no
nature there was no BOM quantity, hence no MW and no Days on RM. Both sides now strip spaces,
dots, dashes, slashes, underscores and leading zeros before the key is built, and the key is
still valuation area + material with a material-only second pass behind it.

**Consumables are labelled `Consumables`**, not left blank, which is where the unnamed slice on
Detail and the `(Blank)` bar on FG came from. Anything still unmatched reads `Unassigned` on both
Nature and Group Nature, so a figure is either named or openly unnamed - never invisible.

**Every matrix carries a Total row and a Total column**, and both hierarchies are written out
expanded, so the month columns are open the moment the page loads instead of collapsed to one
total. The missing Total on Overview's Inventory by Month was this switch written Off.

**The four latest-month visuals use a Latest Month measure** instead of a filter, per the note
above.

**INR per Wp is a measure**, `DIVIDE(SUM(CloseVal), SUM(MW Qty) * 1000000)`, so a row with no
megawatts leaves the cell empty rather than printing `NaN`.

**The Plant slicer lists each plant once.** A named plant with nothing behind it is dropped, an
unnamed code that is in the files appears as `Plant 1904`, and the list is de-duplicated on the
code, so nothing is listed twice.

**The green panel really is green.** Power BI's shape fill, outline and shape sections each take
a `default` selector; written without one Desktop ignored the colour and drew light grey boxes,
which is why the headings looked invisible. Both the shape fill and the container background now
carry `#14532D`.

**The ticker cards drop their category label**, which was the clipped third line of type; the
figure and the card's own title are enough.

**Slicers drop their header**, which was printing `MonthName`, `Category` and `Nature` under a
title that already says it in words.

**Chart axis scales are off and the figures are on the visuals.** Stacked columns print the
month's total above the column rather than one figure per segment, donuts show category and share
with the legend off so the labels stop colliding, and the palette starts at mid green instead of
near-black so the stack reads as separate bands.

**Two new self-checks on the Checks page.** `qcAttrMatch` counts the distinct materials in the
stock files, in RM Nature and in FG Master and how many of each meet the files, so a key mismatch
is one glance rather than a guess. `qcTBByGL` lists the trial balance by GL account with its sign,
which is what is needed to settle whether TB is being read the right way round and whether TB
Master is matching your GL numbers at all.

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
