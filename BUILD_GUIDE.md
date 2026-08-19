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

### How to add each query (you will repeat this 37 times)

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
| 3 | `varWorkbook` | opens and buffers Variables and Calculations once |
| 4 | `fnCleanMB5B` |  |
| 4 | `varMonths` | the months in the data, read cheaply — helper, load off |
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
| 24 | `factTB_Staged` |  |
| 25 | `factTB` |  |
| 26 | `dimDate` |  |
| 27 | `dimCategory` | lets TB and MB5B share one RM/FG/Consumables row |
| 28 | `dimMetric` | makes Inventory (TB) / Inventory (MB5B) / Difference into columns |
| 29 | `dimMeasure` | makes MW / In ₹ Cr / In Days into columns |
| 30 | `dimPlantType` | one row per plant and type, so Summary needs no expanding |
| 31 | `varRMTechnologyCosts` | dated RM-by-technology Cost INR/Wp inputs — helper, load off |
| 32 | `varRMPlantCosts` | separate dated 1900/1902 Cost INR/Wp inputs — helper, load off |
| 33 | `varRMConstants` | dated Module/Cell and plant variables — helper, load off |
| 33 | `varMonthGrid` | the months the dated sheets are spread over — helper, load off |
| 34 | `dimRMTechnologyDaily` | calculated component cost per day by month |
| 35 | `dimRMPlantDaily` | calculated 1900/1902 item cost per day by month |

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
pRoot, pVarsFile, varWorkbook, fnCleanMB5B, varMonths, stgRM, stgFG, stgConble,
fnVarSheet, fnVarSheetSafe, dimPlantMaster, varPlantCodes,
factRM, factFG, factConble, varConstants, dimMaterialAttr, dimFGAttr,
fnConstantAsOf, varMWCapacity, factTB_Staged,
varRMTechnologyCosts, varRMPlantCosts, varRMConstants, varMonthGrid
```

Leave these ticked (they become your tables):
```
factInventory, factTB, dimPlant, dimDate, dimNature, dimCapacity,
dimCategory, dimMetric, dimMeasure, dimPlantType,
dimRMTechnologyDaily, dimRMPlantDaily
```

**1.6** Ribbon: **Home** → **Close & Apply**. Wait for it to load.

### Checkpoint — do not go to Part 2 until all six are true

1. The Queries list on the left of Power Query shows **37** names, and every name in the
   table above appears in it, spelled identically. Compare them one by one; a missing one
   is the single most common cause of an error later.
2. The 25 helper names in step 1.5 are shown in *italics* in that list (that is what
   "Enable load off" looks like); the other 12 are not italic.
3. Click `factInventory`: the preview shows rows, and the columns include `CloseVal`,
   `Category`, `Nature`, `Month`, `ValuationArea`, `MW`.
4. Click `factTB`: it shows rows, `Month` is filled in on every row, and `ValuationArea`
   is not the word `Unallocated` on every row.
5. Click `factTB`: `Rule` says how each line was placed. `dropped: no row for this GL
   and profit centre` means that account is missing from `TB Master`, so its money is not
   counted anywhere — add the pair to `TB Master` and refresh.
6. Click `dimRMTechnologyDaily` and `dimRMPlantDaily`: both show one row per configured
   item and loaded month, with Cost INR/Wp, the matching constant and PerDayCostCr.

After **Close & Apply**, the Data pane on the right must list exactly these 12 tables:
`factInventory`, `factTB`, `dimPlant`, `dimDate`, `dimNature`, `dimCapacity`, `dimCategory`, `dimMetric`, `dimMeasure`, `dimPlantType`, `dimRMTechnologyDaily`, `dimRMPlantDaily`.

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
| "Expression.Syntax Error" right after pasting | the whole appendix went into one query | one query per Blank Query, 30 times |

Send me the exact error text and I'll tell you the one-line fix.

---

# PART 2 — Build the model (10 min)

**2.1** Left sidebar: click the **Model** icon (third one down, looks like a table diagram).

**2.2** Power BI will have guessed some relationships. **Delete all of them**: click each
connecting line and press Delete. Cleaner to start blank.

**2.3** Create these 14 relationships. To create one: click and drag the **from** field onto
the **to** field. Then double-click the line and confirm the settings.

| From (the "one" side) | To (the "many" side) | Cardinality | Direction |
|---|---|---|---|
| `dimDate[Month]` | `factInventory[Month]` | One to many | Single |
| `dimDate[Month]` | `factTB[Month]` | One to many | Single |
| `dimDate[Month]` | `dimCapacity[Month]` | One to many | Single |
| `dimDate[Month]` | `dimRMTechnologyDaily[Month]` | One to many | Single |
| `dimDate[Month]` | `dimRMPlantDaily[Month]` | One to many | Single |
| `dimPlant[ValuationArea]` | `factInventory[ValuationArea]` | One to many | Single |
| `dimPlant[ValuationArea]` | `factTB[ValuationArea]` | One to many | Single |
| `dimPlant[ValuationArea]` | `dimCapacity[ValuationArea]` | One to many | Single |
| `dimNature[Nature]` | `factInventory[Nature]` | One to many | Single |
| `dimNature[Nature]` | `dimCapacity[Tech]` | One to many | Single |
| `dimCategory[Category]` | `factInventory[Category]` | One to many | Single |
| `dimCategory[Category]` | `factTB[Category]` | One to many | Single |
| `dimPlantType[PlantType]` | `factInventory[PlantType]` | One to many | Single |
| `dimPlantType[PlantType]` | `factTB[PlantType]` | One to many | Single |

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

**2.6** Do the same for: `dimPlant[Plant]` → `PlantSort`, `dimPlantType[Plant and Type]` → `RowSort`, `dimCategory[Category]` →
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

**Create the 4 pages** with the **+** at the bottom, named: `Overview` · `Summary` · `FG` · `RM`.

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
| Fields | `Ticker 1902 Rs Cr` |

Title: `1902 Jaipur Module`

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
| Fields | `Ticker 1900 Rs Cr` |

Title: `1900 Dholera Module`

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

**4.26** **Matrix** — The first of the three master columns: what the books say, month by month. A row per plant, opening into RM, FG and Consumables, and the months under this heading are the newest March plus the three most recent unless the slicer above says otherwise.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]`, `dimCategory[Category]` |
| Columns | `dimDate[MonthName]` |
| Values | `TB Inventory Rs Cr` → rename it to **Rs Cr.** |
| Filters | `In Summary Window  →  is 1` |

Title: `Inventory (TB)`

Position: Horizontal 192, Vertical 88, Width 357, Height 300.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Rows takes two fields, in this order: dimPlant[Plant], then dimCategory[Category]. The table opens on the plant, showing that plant’s whole inventory for the month, and the + beside it opens RM, FG and Consumables underneath.
- Columns takes one field only: dimDate[MonthName]. The months are the columns of this block and the heading above them is its master column.
- Filters pane → drag the measure In Summary Window in → is 1. That is what gives the newest March plus the three most recent months by default, and your ticks instead when you tick months in the slicer.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March to July, the same steel counted twice.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On. The Grand Total row adds the plants and types inside one month, which is a real figure: one point in time.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Values', then 'Font size: 8; Column headers', then 'Font size: 8, Word wrap: On; Values', then 'Font' and set it to Arial, Font size: 8, Colour: #1F2A24.
- Row headers are shown on this first block only, so the three blocks read as one table across the page.

**4.27** **Matrix** — The second master column: the same rows and the same months as the MB5B stock report has them. Read straight across from the block on its left and you are comparing the books with the stock for one plant, one type, one month.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]`, `dimCategory[Category]` |
| Columns | `dimDate[MonthName]` |
| Values | `Inventory Rs Cr` → rename it to **Rs Cr.** |
| Filters | `In Summary Window  →  is 1` |

Title: `Inventory (MB5B)`

Position: Horizontal 556, Vertical 88, Width 357, Height 300.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Rows takes two fields, in this order: dimPlant[Plant], then dimCategory[Category]. The table opens on the plant, showing that plant’s whole inventory for the month, and the + beside it opens RM, FG and Consumables underneath.
- Columns takes one field only: dimDate[MonthName]. The months are the columns of this block and the heading above them is its master column.
- Filters pane → drag the measure In Summary Window in → is 1. That is what gives the newest March plus the three most recent months by default, and your ticks instead when you tick months in the slicer.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March to July, the same steel counted twice.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On. The Grand Total row adds the plants and types inside one month, which is a real figure: one point in time.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Values', then 'Font size: 8; Column headers', then 'Font size: 8, Word wrap: On; Values', then 'Font' and set it to Arial, Font size: 8, Colour: #1F2A24.
- The plant labels are repeated on this block, so it can be read on its own and no row can ever be misread against the wrong plant. Expand a plant here and expand it on the other two blocks so the three read across.

**4.28** **Matrix** — The third master column: the books less the stock report, on the same plant rows and the same months. Anything other than a small figure here is the reconciliation asking a question, and the Detail page is where it is answered.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]`, `dimCategory[Category]` |
| Columns | `dimDate[MonthName]` |
| Values | `Difference Inventory Rs Cr` → rename it to **Rs Cr.** |
| Filters | `In Summary Window  →  is 1` |

Title: `Difference`

Position: Horizontal 920, Vertical 88, Width 357, Height 300.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Rows takes two fields, in this order: dimPlant[Plant], then dimCategory[Category]. The table opens on the plant, showing that plant’s whole inventory for the month, and the + beside it opens RM, FG and Consumables underneath.
- Columns takes one field only: dimDate[MonthName]. The months are the columns of this block and the heading above them is its master column.
- Filters pane → drag the measure In Summary Window in → is 1. That is what gives the newest March plus the three most recent months by default, and your ticks instead when you tick months in the slicer.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March to July, the same steel counted twice.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On. The Grand Total row adds the plants and types inside one month, which is a real figure: one point in time.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Values', then 'Font size: 8; Column headers', then 'Font size: 8, Word wrap: On; Values', then 'Font' and set it to Arial, Font size: 8, Colour: #1F2A24.
- The plant labels are repeated on this block, so it can be read on its own and no row can ever be misread against the wrong plant. Expand a plant here and expand it on the other two blocks so the three read across.

**4.29** **Clustered column chart** — The books against the stock report, two bars per period: the same figures as the matrix above, but you can see a gap opening without reading a single number. Same periods as the matrices, because it carries the same filter.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `TB Inventory Rs Cr`, `Inventory Rs Cr` |
| Filters | `In Summary Window  →  is 1` |

Title: `Inventory (TB) vs Inventory (MB5B) by Month (Rs Cr.)`

Position: Horizontal 192, Vertical 396, Width 529, Height 152.

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

**4.30** **Line and clustered column chart** — The question the reconciliation is really asking: is the gap widening or closing. The bar is the difference in crore rupees, the line above it the same difference as a percentage of the trial balance, so a small gap on a big month reads as small.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Column y-axis | `Difference Inventory Rs Cr` |
| Line y-axis | `Difference Inventory %` |
| Filters | `In Summary Window  →  is 1` |

Title: `Difference by Month (Rs Cr. and % of TB)`

Position: Horizontal 735, Vertical 396, Width 529, Height 152.

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

**4.31** **Line chart** — The long view under the reconciliation: three lines across the last twelve months that have data, or fewer if that is all there is — raw material days, finished goods days, and the two added together, which is what the Overview card calls Days of inventory (RM + FG). Every month is its own closing figure divided by capacity, so nothing is added across months. Read it for shape: RM climbing while FG is flat means material is arriving faster than it is being consumed.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `RM Days`, `FG Days`, `Total Days (RM + FG)` |
| Filters | `In Last 12  →  is 1` |

Title: `Days of Inventory by Month, Last 12 Months — RM, FG and Total`

Position: Horizontal 192, Vertical 556, Width 1072, Height 148.

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

**4.32** **Slicer** — Which months appear under each master column. Tick nothing and it shows the last four with data; tick your own and it shows those, up to twelve.

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

**4.33** **Slicer** — A coarser filter over the same months: tick Q1 and only April, May and June are left for the two matrices to show. Leave it empty to see every month.

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

**4.34** **Slicer** — One plant, or all of them. It filters the technology matrix and all three charts, so picking Dholera Cell turns the page into a Dholera Cell page.

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

**4.35** **Slicer** — One module technology, when you want the page to be about that technology only.

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

**4.36** **Matrix** — Finished goods per plant in megawatts, one column per month — the newest March plus the three after it by default. The Excel sheet had this as one wide table with an IN MW block, an IN CRS block and an IN DAYS block; these are those blocks.

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

**4.37** **Matrix** — Finished goods per plant in crore rupees, one column per month — the newest March plus the three after it by default. The Excel sheet had this as one wide table with an IN MW block, an IN CRS block and an IN DAYS block; these are those blocks.

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

**4.38** **Matrix** — Finished goods per plant in days of cover, one column per month — the newest March plus the three after it by default. The Excel sheet had this as one wide table with an IN MW block, an IN CRS block and an IN DAYS block; these are those blocks.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]` |
| Columns | `dimDate[MonthName]` |
| Values | `Plant Days` → rename it to **Days** |
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
- Values takes Plant Days, not Days. Plant Days is MW ÷ the MWD column of Plant Master and has no other denominator — the MW Capacity sheet belongs to the technology table below. A blank cell means MWD is empty for that plant on the sheet.

**4.39** **Matrix** — The same months and the same unit, by module technology rather than by plant — G12 Perc, G12R Topcon, M10 Perc, M10 Topcon and the rest — which is where a build-up in one technology shows itself.

| Well | Field |
|---|---|
| Rows | `dimNature[Nature]` |
| Columns | `dimDate[MonthName]` |
| Values | `Inventory MW` → rename it to **MW** |
| Filters | `dimCategory[Category]  →  is FG`, `In Summary Window  →  is 1` |

Title: `Inventory FG by Techno — In MW`

Position: Horizontal 192, Vertical 208, Width 350, Height 200.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Fastest way to build the next block: click this matrix, Ctrl+C, Ctrl+V, then in Values swap the measure. Position, filters and formatting all come with the copy. Then in Rows take dimPlant[Plant] out and drag dimNature[Nature] in.
- Check the filters came across: Category is FG, In Summary Window is 1.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice. Row subtotals: On — that one adds the plants inside a single month, which is a real figure, and it is the Grand Total row the Excel sheet had.
- With the Plant slicer on one plant this becomes that plant's technology split, which is the Module block the Excel sheet had.

**4.40** **Matrix** — The same months and the same unit, by module technology rather than by plant — G12 Perc, G12R Topcon, M10 Perc, M10 Topcon and the rest — which is where a build-up in one technology shows itself.

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

**4.41** **Matrix** — The same months and the same unit, by module technology rather than by plant — G12 Perc, G12R Topcon, M10 Perc, M10 Topcon and the rest — which is where a build-up in one technology shows itself.

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

**4.42** **Line and clustered column chart** — Which technology is holding the finished goods right now, in money as bars and in megawatts as the line over them. Money is on the bars because every technology has a value, while a megawatt figure only exists for the ones your MW Capacity sheet covers — as bars, that left the chart looking empty. It is deliberately pinned to the latest month with data: there is no period on the axis here, so without that pin it would add four months of stock together and read four times too high.

| Well | Field |
|---|---|
| X-axis | `dimNature[Nature]` |
| Column y-axis | `Latest Month FG ₹ Cr` |
| Line y-axis | `Latest Month FG MW` |
| Filters | `dimCategory[Category]  →  is FG` |

Title: `FG by Technology, Latest Month — Rs Cr. as Bars, MW as the Line`

Position: Horizontal 192, Vertical 416, Width 354, Height 272.

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

**4.43** **Line and clustered column chart** — How long the finished goods on hand would last, month by month, with the change on last month printed above each bar — so a slow build-up is visible before it becomes a number anyone argues about.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Column y-axis | `Days` |
| Line y-axis | `Days vs LM` |
| Filters | `dimCategory[Category]  →  is FG`, `In Last 12  →  is 1` |

Title: `FG Days by Month, Last 12 Months (Days and % vs LM)`

Position: Horizontal 560, Vertical 416, Width 368, Height 272.

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

**4.44** **Donut chart** — Where the finished goods are sitting, as a share of the whole. Pinned to the latest month for the same reason as the bar chart: a share of four added-up months would mean nothing.

| Well | Field |
|---|---|
| Legend | `dimPlant[Plant]` |
| Values | `Latest Month FG ₹ Cr` |

Title: `FG Share by Plant (%), Latest Month`

Position: Horizontal 941, Vertical 416, Width 323, Height 272.

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

**4.45** **Slicer** — Which months appear under each master column, and on both charts along the bottom. Nothing ticked means the last four with data; tick your own for up to twelve.

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

**4.46** **Slicer** — The quarter-mode equivalent: empty means the last four fiscal quarters.

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

**4.47** **Slicer** — One plant, or all three.

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

**4.48** **Slicer** — Module or Cell, when you want the page to be about one of the two only — the same split the Excel sheet had as its Module and Cell blocks.

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

**4.49** **Matrix** — Raw material and packing per plant in crore rupees, one column per month — the top block of the old RM sheet, which had IN CRS and IN DAYS side by side over the same three plants. MW is left out because an RM megawatt figure is derived from a BOM rather than measured.

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

**4.50** **Matrix** — Raw material and packing per plant in days of cover, one column per month — the top block of the old RM sheet, which had IN CRS and IN DAYS side by side over the same three plants. MW is left out because an RM megawatt figure is derived from a BOM rather than measured.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]` |
| Columns | `dimDate[MonthName]` |
| Values | `RM Plant Days` → rename it to **Days** |
| Filters | `dimCategory[Category]  →  is RM`, `In Summary Window  →  is 1` |

Title: `RM Inventory Plant Wise — In Days`

Position: Horizontal 735, Vertical 88, Width 529, Height 112.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Fastest way to build the next block: click this matrix, Ctrl+C, Ctrl+V, then in Values swap the measure. Position, filters and formatting all come with the copy.
- Values takes RM Plant Days. 1900 and 1902 sum item-level Days calculated from their own dated Cost INR/Wp and plant variable; 1905 returns Total Cell Days; the Total row returns the technology Grand Total Days. No FG MWD or MW Capacity value enters this measure.
- Filters pane → dimCategory[Category] → tick RM only, then In Summary Window → is 1.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice. Row subtotals: On — that one adds the plants inside a single month, which is a real figure, and it is the Grand Total row the Excel sheet had.
- In the Visualizations pane click the paintbrush icon, then click 'Values', then 'Font' and set it to Arial, Font size: 9, Colour: #1F2A24.
- Clicking a plant row filters the nature blocks and both charts below it.

**4.51** **Matrix** — The second block of the old sheet in crore rupees: Module and Cell, each opening into its natures — cell cost, frame, glass, POE, wafer, paste, screens, gases and the rest — with a subtotal on each group and a grand total under them.

| Well | Field |
|---|---|
| Rows | `dimRMTechnologyDaily[PlantGroup]`, `dimRMTechnologyDaily[Item]` |
| Columns | `dimDate[MonthName]` |
| Values | `RM Technology Value ₹ Cr` → rename it to **Rs Cr.** |
| Filters | `dimCategory[Category]  →  is RM`, `In Summary Window  →  is 1` |

Title: `RM Inventory by Techno — In Rs Cr`

Position: Horizontal 192, Vertical 208, Width 529, Height 268.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Fastest way to build the next block: click this matrix, Ctrl+C, Ctrl+V, then in Values swap the measure. Position, filters and formatting all come with the copy. Then in Rows drop dimRMTechnologyDaily[PlantGroup] and dimRMTechnologyDaily[Item] in and take dimPlant[Plant] out.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Stepped layout' and set it to Off, +/- icons: On, so Module/Cell and the nature get a column each with an expander on each group.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On with 'Per row level' On, so Total Module and Total Cell both appear and not only the grand total — the two subtotals the old sheet had.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice. Row subtotals: On — that one adds the plants inside a single month, which is a real figure, and it is the Grand Total row the Excel sheet had.
- A nature reading Unassigned is a material the RM master does not carry — it is money the report will not silently file under someone else's nature. qcAttrMatch on Checks names them.
- Right-click a nature row → Drill through → Detail for the material-by-material list behind it.

**4.52** **Matrix** — The second block of the old sheet in days of cover: Module and Cell, each opening into its natures — cell cost, frame, glass, POE, wafer, paste, screens, gases and the rest — with a subtotal on each group and a grand total under them.

| Well | Field |
|---|---|
| Rows | `dimRMTechnologyDaily[PlantGroup]`, `dimRMTechnologyDaily[Item]` |
| Columns | `dimDate[MonthName]` |
| Values | `RM Technology Days` → rename it to **Days** |
| Filters | `dimCategory[Category]  →  is RM`, `In Summary Window  →  is 1` |

Title: `RM Inventory by Techno — In Days`

Position: Horizontal 735, Vertical 208, Width 529, Height 220.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' toggle under it, switch it On so a long heading goes onto two lines instead of being cut.
- Click 'Row headers' and do the same: Font size 10, Word wrap On if it is offered.
- Click 'Values' and set Font size to 10.
- Double-click the line between two column headings to widen a column that is still showing three dots — or drag that line. Column widths are remembered when you save.
- Fastest way to build the next block: click this matrix, Ctrl+C, Ctrl+V, then in Values swap the measure. Position, filters and formatting all come with the copy. Then in Rows drop dimRMTechnologyDaily[PlantGroup] and dimRMTechnologyDaily[Item] in and take dimPlant[Plant] out.
- In the Visualizations pane click the paintbrush icon, then click 'Row headers', then 'Stepped layout' and set it to Off, +/- icons: On, so Module/Cell and the nature get a column each with an expander on each group.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Row subtotals' and set it to On with 'Per row level' On, so Total Module and Total Cell both appear and not only the grand total — the two subtotals the old sheet had.
- In the Visualizations pane click the paintbrush icon, then click 'Subtotals', then 'Column subtotals' and set it to Off. Stock is a level, not a flow: a Total column would add March's steel to July's steel, which is the same steel counted twice. Row subtotals: On — that one adds the plants inside a single month, which is a real figure, and it is the Grand Total row the Excel sheet had.
- A nature reading Unassigned is a material the RM master does not carry — it is money the report will not silently file under someone else's nature. qcAttrMatch on Checks names them.
- Right-click a nature row → Drill through → Detail for the material-by-material list behind it.

**4.53** **Clustered column chart** — Raw material held in crore rupees: one group per period along the bottom and the three plants side by side inside each group, so you read the months left to right and compare the plants within a month. It follows the pickers above, so it is four periods by default and up to twelve if you tick them.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Legend | `dimPlant[Plant]` |
| Y-axis | `Inventory Rs Cr` |
| Filters | `dimCategory[Category]  →  is RM`, `In Summary Window  →  is 1` |

Title: `RM Inventory (Rs Cr.) by Plant`

Position: Horizontal 192, Vertical 484, Width 529, Height 200.

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

**4.54** **Line and clustered column chart** — The same chart in days rather than rupees — how long each plant's raw material would last at its own capacity, three plant bars per month, and over them a line for the whole business: every plant's RM megawatts added together over every plant's capacity added together. The line is not the average of the three bars, and it is not their sum: it is one big plant's worth of days, which is the figure to quote for the company. Read together with the chart beside it, this tells you whether a bigger rupee figure is actually more stock or just a dearer month.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Column legend | `dimPlant[Plant]` |
| Column y-axis | `RM Plant Days by Period` |
| Line y-axis | `RM Technology Days by Period` |
| Filters | `dimCategory[Category]  →  is RM`, `In Summary Window  →  is 1` |

Title: `RM Inventory (Days) by Plant, with Total Days Across All Plants`

Position: Horizontal 735, Vertical 436, Width 529, Height 200.

- Still in the paintbrush pane, click General, then Title, and set Font size to 12. If the title still ends in three dots, shorten the text you typed — a clipped title is the visual telling you it has run out of width.
- Click 'X-axis' and set Font size to 9. If the labels are turned on their side or cut off, that is the visual being too narrow — leave it, Power BI rotates them on purpose.
- Click 'Y-axis' and set Font size to 9.
- Click 'Legend' and set Font size to 9 and Position to 'Top center'.
- Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon as there are more than about six bars.
- The line comes from RM Technology Days by Period, the same calculated Grand Total Days as the lower technology table; the bars use RM Plant Days by Period.
- Use RM Plant Days by Period for the bars and RM Technology Days by Period for the line. Both average only when more than one month is deliberately put in one point; neither adds month-end Days.
- In the Visualizations pane click the paintbrush icon, then click 'Data labels' and set it to On, Font: Arial, Font size: 8, Bold: On, Colour: #FFFFFF, Display units: None, Value decimal places: 0, Position: Inside end.
- Data labels → Apply settings to → Series → RM Technology Days by Period: Font: Arial, Font size: 8, Bold: On, Colour: #14532D, Value decimal places: 0, Position: Above — dark green on the white card, because this label is not printed on a bar.
- In the Visualizations pane click the paintbrush icon, then click 'Lines', then 'Colour: #14532D, Stroke width: 2, Show marker: On, Marker size: 4. Format pane', then 'Lines', then 'Smooth line' and set it to Off, so the shape is honest.
- In the Visualizations pane click the paintbrush icon, then click 'Legend', then 'Position' and set it to Top center, Font: Arial, Font size: 8. The line appears in the legend as 'RM Technology Days by Period' — rename it if you like by double-clicking the field in the well and typing 'Total (All Plants)'.
- In the Visualizations pane click the paintbrush icon, then click 'Y-axis' and set it to Off, and Secondary y-axis: Off. Bars and line are both in days on the same scale, so leave 'Align zeros' On if you switch either axis back on, or the line will sit at a misleading height.
- In the Visualizations pane click the paintbrush icon, then click 'X-axis', then 'Values', then 'Font' and set it to Arial, Font size: 8, Colour: #1F2A24, Concatenate labels: Off.
- In the Visualizations pane click the paintbrush icon, then click 'General', then 'Title', then 'Font' and set it to Arial, Font size: 12, Colour: #14532D.
- A missing effective cost or constant shows blank here, not zero. An intentional zero remains zero input and also produces blank Days because a zero per-day cost cannot be divided into inventory.

---

## Making it clickable

**4.56 Interactions.** A *left*-click needs no setup — it already cross-filters the rest
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
2. On `MW Capacity` and `Constants`, never overwrite a number — add a new **column**
   headed with the date it takes effect (`MW Capacity`), or a new row with that date
   (`Constants`). Overwriting silently rewrites past months.

---

# PART 6 — Every error we have hit, and its one-line fix

Find the words Power BI showed you in the left column.

| What Power BI says | What is actually wrong | Fix |
|---|---|---|
| `Not enough elements in the enumeration to complete the operation` | a query expected more columns than the sheet has | you are on an old copy of that query — refresh the guide page and re-copy it |
| `The MW sheet is none of the three layouts I recognise` / `has month columns but no column of plant codes` | the MW sheet is not laid out as dates across the top over a column of 1900/1902/1905 | put the plant codes in their own column, the month dates in the header row, and re-copy `varMWCapacity`. Paste `qcMWSheet` to see the sheet exactly as the query reads it |
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
| `1905` shows blank Days | it has no capacity to divide by | add a `Total` row for it on the MW sheet with the plant's whole capacity (8.28 / 6.17 / 5.63 style). Where a plant has no `Total` row its technology rows are added up instead; `qcNatureNoCapacity` lists the technologies with neither |
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

## varMonths

> The months that exist in the data, read the cheap way. `dimDate` used to work its months out from `factInventory` and `factTB_Staged`, which meant every stock file and the whole trial balance were parsed a second time for a list of a dozen dates - and because three other tables reference `dimDate`, that second parse happened four times over. This reads only the From Date column of each stock file, and takes the trial balance's months from the file names, so nothing is cleaned, joined or typed twice. The month set is the same one the facts produce: `Date.StartOfMonth` of the same column, on rows that carry a material.

```
let
    Norm     = (n as any) as text =>
                   Text.Upper(Text.Remove(Text.Trim(Text.From(n ?? "")), {" ",".","_","-","/","(",")"})),
    // the header row is found in the first few dozen rows, so only those are materialised.
    // the rest of the sheet is read one column wide instead of twenty-nine.
    MonthsOf = (content as binary) as list =>
                   let
                       Wb       = Excel.Workbook(content, null, true),
                       Sheets   = Table.SelectRows(Wb, each [Kind] = "Sheet"),
                       Picked   = try Sheets{[Item = "Sheet1", Kind = "Sheet"]}[Data]
                                  otherwise Sheets{0}[Data],
                       Head     = Table.ToRows(Table.FirstN(Picked, 60)),
                       HdrIdx   = List.PositionOf(
                                      List.Transform(Head, (r) =>
                                          List.Contains(List.Transform(r, Norm), "MATERIAL")), true),
                       Skipped  = if HdrIdx > 0 then Table.Skip(Picked, HdrIdx) else Picked,
                       Promoted = Table.PromoteHeaders(Skipped, [PromoteAllScalars = true]),
                       Cols     = Table.ColumnNames(Promoted),
                       Pick     = (alts as list) as nullable text =>
                                      let Hits = List.Select(Cols, (c) => List.Contains(alts, Norm(c)))
                                      in  if List.IsEmpty(Hits) then null else List.First(Hits),
                       cFrom    = Pick({"FROMDATE"}),
                       cMat     = Pick({"MATERIAL","MATERIALNO"}),
                       Two      = if cFrom = null then null
                                  else Table.SelectColumns(Promoted,
                                           if cMat = null then {cFrom} else {cFrom, cMat}),
                       // a Total or subtotal line carries no material, and its stray date must
                       // not invent a month the facts do not have
                       Real     = if Two = null then null
                                  else if cMat = null then Two
                                  else Table.SelectRows(Two, each
                                           Text.Trim(Text.From(Record.Field(_, cMat) ?? "")) <> ""),
                       Dates    = if Real = null then {} else Table.Column(Real, cFrom),
                       Months   = List.RemoveNulls(List.Transform(Dates,
                                      (v) => try Date.StartOfMonth(Date.From(v)) otherwise null))
                   in
                       List.Distinct(Months),
    Stock    = (folder as text) as list =>
                   let
                       Files = try Folder.Files(pRoot & folder) otherwise #table({}, {}),
                       Only  = if Table.IsEmpty(Files) then Files
                               else Table.SelectRows(Files, each
                                        Text.StartsWith(Text.Lower([Extension]), ".xls")
                                        and not Text.StartsWith([Name], "~$")
                                        and not Text.StartsWith([Name], ".")),
                       Lists = if Table.IsEmpty(Only) then {}
                               else List.Transform(Only[Content], (c) => try MonthsOf(c) otherwise {})
                   in
                       List.Combine(Lists),
    // the trial balance's month is in its file name - TB_YYYYMM.xlsx - exactly as
    // factTB_Staged reads it, so those files are not opened here at all
    TBMonths = let
                   Files = try Folder.Files(pRoot & "\TB") otherwise #table({}, {}),
                   Only  = if Table.IsEmpty(Files) then Files
                           else Table.SelectRows(Files, each
                                    Text.StartsWith(Text.Lower([Extension]), ".xls")
                                    and not Text.StartsWith([Name], "~$")
                                    and not Text.StartsWith([Name], ".")),
                   Names = if Table.IsEmpty(Only) then {} else Only[Name],
                   Dates = List.Transform(Names, (n) =>
                               let digits = Text.Select(n, {"0".."9"}),
                                   yyyymm = Text.Middle(digits, 0, 6)
                               in  try #date(Number.From(Text.Start(yyyymm, 4)),
                                             Number.From(Text.Middle(yyyymm, 4, 2)), 1)
                                   otherwise null)
               in
                   List.RemoveNulls(Dates),
    All      = List.Combine({Stock("\RM Raw"), Stock("\FG Raw"), Stock("\Consble Raw"), TBMonths}),
    Out      = List.Buffer(List.Sort(List.Distinct(All)))
in
    Out
```

## varWorkbook

> The Variables workbook opened once for the whole refresh. Every master query takes its sheet from this buffered workbook rather than opening and unzipping the same `.xlsx` again.

```
let
    Bytes = Binary.Buffer(File.Contents(pVarsFile)),
    Book  = Excel.Workbook(Bytes, null, true),
    Out   = Table.Buffer(Book)
in
    Out
```

## fnVarSheet

> Shared helper. Create this BEFORE dimMaterialAttr, dimFGAttr and varConstants, which all call it.

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
        Wb       = varWorkbook,
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
    // This sheet is read directly rather than through fnVarSheet, because its headings collide:
    // "Plant" is both a code and a name, and an alias list that maps two of the sheet's columns
    // onto one name makes the rename fail - which returned an empty table, and an empty table
    // is why every plant's days of cover went blank while its name still looked right. Here each
    // heading is claimed by one target only, in order, and a column already claimed is not
    // offered again.
    Norm     = (n as any) as text =>
                   Text.Upper(Text.Remove(Text.Trim(Text.From(n ?? "")),
                       {" ", ".", "_", "-", "/", "(", ")", ",", "'", "%"})),
    Wb       = try varWorkbook otherwise #table({}, {}),
    Sheets   = try Table.SelectRows(Wb, each [Kind] = "Sheet") otherwise #table({}, {}),
    Want     = List.Transform({"Plant Master","PlantMaster","Plants","Plant"}, Norm),
    Hit      = try Table.SelectRows(Sheets, each List.Contains(Want, Norm([Item])))
               otherwise #table({}, {}),
    Data     = if Table.RowCount(Hit) = 0 then #table({}, {}) else Hit{0}[Data],
    Raw      = if Table.RowCount(Hit) = 0 then #table({}, {})
               else Table.PromoteHeaders(Data, [PromoteAllScalars=true]),
    Names    = Table.ColumnNames(Raw),
    // Each target names the headings it will accept, best first. Pick walks that list and takes
    // the first heading not already claimed, so "Plant" falls to the name only when a plainer
    // code column exists.
    Pick     = (want as list, used as list) as nullable text =>
                   List.First(List.RemoveNulls(List.Transform(want, (w) =>
                       List.First(List.Select(Names, (n) =>
                           Norm(n) = Norm(w) and not List.Contains(used, n)), null))), null),
    // "MWD" is matched loosely as well, so MWD (in MW) or MW/Day counts
    Loose    = (frag as text, used as list) as nullable text =>
                   List.First(List.Select(Names, (n) =>
                       Text.Contains(Norm(n), frag) and not List.Contains(used, n)), null),
    cArea    = Pick({"Valuation Area","Val Area","Plant Code","Code","Plant"}, {}),
    cMWD     = let p = Pick({"MWD","MW D","MWD (MW per day)","MW per Day","MW Day","MWPD",
                             "MW/Day","Plant MWD","MWD Capacity","Capacity MWD","Daily MW"},
                            {cArea})
               in  if p <> null then p else Loose("MWD", List.RemoveNulls({cArea})),
    cSort    = let u = List.RemoveNulls({cArea, cMWD}),
                   p = Pick({"Sort Order","Sort","Order","Sort No","Sequence"}, u)
               in  if p <> null then p else Loose("SORT", u),
    cName    = let u = List.RemoveNulls({cArea, cMWD, cSort})
               in  Pick({"Plant Name","Name","at","Description","Plant Description",
                         "Valuation Area Description","Plant"}, u),
    Renames  = List.RemoveNulls({
                   if cArea <> null then {cArea, "ValuationArea"} else null,
                   if cName <> null then {cName, "PlantName"}     else null,
                   if cSort <> null then {cSort, "PlantSort"}     else null,
                   if cMWD  <> null then {cMWD,  "PlantMWD"}      else null}),
    Renamed  = if List.IsEmpty(Renames) then Raw else Table.RenameColumns(Raw, Renames),
    Cols     = {"ValuationArea", "PlantName", "PlantSort", "PlantMWD"},
    Padded   = List.Accumulate(List.Difference(Cols, Table.ColumnNames(Renamed)), Renamed,
                   (t, c) => Table.AddColumn(t, c, each null)),
    Slim     = Table.SelectColumns(Padded, Cols),
    // the code is text and trimmed, because 1900 read as a number will not join to a text key
    Keyed    = Table.TransformColumns(Slim, {
                   {"ValuationArea", each Text.Trim(Text.From(_ ?? "")), type text},
                   {"PlantName",     each Text.Trim(Text.From(_ ?? "")), type text}}),
    Real     = Table.SelectRows(Keyed, each [ValuationArea] <> ""),
    // the label the whole report shows: the code and the name together, so the slicer, the
    // legends and the ticker cards can never disagree about what a plant is called
    Label    = Table.AddColumn(Real, "Plant",
                   each if [PlantName] = "" then [ValuationArea]
                        else [ValuationArea] & " " & [PlantName], type text),
    Sorted   = Table.AddColumn(Label, "SortNo",
                   each try Number.From([PlantSort]) otherwise null, type number),
    Indexed  = Table.AddIndexColumn(Sorted, "Seq", 1, 1, Int64.Type),
    Order    = Table.AddColumn(Indexed, "PlantSortNo",
                   each Int64.From([SortNo] ?? [Seq]), Int64.Type),
    // MWD - the plant's megawatts a day, typed on Plant Master. It is the denominator for days
    // of cover on the plant rows: days = inventory MW / MWD, nothing else divided in. A figure
    // typed as "3.6 MW", or with a comma in it, is still a figure.
    Rate     = Table.AddColumn(Order, "MWD",
                   each let t = Text.Trim(Text.From([PlantMWD] ?? "")),
                            v = try Number.From(t)
                                otherwise (try Number.From(
                                    Text.Select(t, {"0".."9","."})) otherwise null)
                        in  if v = null or v = 0 then null else v, type number),
    Out      = Table.SelectColumns(Rate, {"ValuationArea", "Plant", "PlantSortNo", "MWD"}),
    // three rows, and read by dimPlant, varPlantCodes and the fact queries: held in memory so
    // the workbook is opened for them once rather than once per reader
    Buffered = Table.Buffer(Out)
in
    Buffered
```

## varPlantCodes

> Just the list of plant codes on the Plant Master sheet, so the fact queries can keep to them without each one re-reading the workbook. The trial balance names other plants too and they are deliberately not in this report; `qcPlantCodes` on Checks says what they hold. Falls back to the three codes if the sheet gave nothing. Enable load OFF.

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
    // The master sheet, read once and held. This query leans on it three times - on the
    // plant-and-material key, on the material alone, then on the description - and without
    // this line Power Query re-opens and re-parses the workbook for each of the three, because
    // a merge re-evaluates its right-hand side every time it is asked for.
    AttrSrc  = Table.Buffer(dimMaterialAttr),
    Merged   = Table.NestedJoin(Src, {"MatKey"}, AttrSrc, {"MatKey"},
                   "attr", JoinKind.LeftOuter),
    Expanded = Table.ExpandTableColumn(Merged, "attr",
                   {"Nature","GroupNature","BOMStdQty","Item"}),

    // Second pass on the material alone. Plant and material together is the safer key, but
    // it misses every row when the master sheet has no valuation area column, or records the
    // plant differently from the MB5B export -- and then nothing has a nature at all.
    ByMat    = Table.Buffer(Table.Distinct(Table.SelectColumns(AttrSrc,
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
    ByDesc   = Table.Buffer(Table.Distinct(Table.SelectRows(Table.SelectColumns(AttrSrc,
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
    // The factor is looked up once per month rather than once per row - it can only change on a
    // dated Constants row, so every row of a month gets the same number either way - and joined
    // on. Asking for it per row scanned and sorted the Constants table tens of thousands of
    // times for an answer that was the same each time.
    Facs     = Table.Buffer(Table.AddColumn(
                   Table.Distinct(Table.SelectColumns(Named, {"Month"})), "MWFactor",
                   each fnConstantAsOf("RM_MW_FACTOR", [Month]), type number)),
    WithFac  = Table.ExpandTableColumn(
                   Table.NestedJoin(Named, {"Month"}, Facs, {"Month"}, "fac", JoinKind.LeftOuter),
                   "fac", {"MWFactor"}),
    MW       = Table.RemoveColumns(
                   Table.AddColumn(WithFac, "MW", each
                       try [CloseQty] / [BOMStdQty] * [MWFactor] / 1000000 otherwise null,
                       type number),
                   {"MWFactor"})
in
    MW
```

## factFG

```
let
    Src      = stgFG,
    // read once and held, for the same reason as factRM: two merges against it, and each one
    // would otherwise re-open the workbook
    AttrSrc  = Table.Buffer(dimFGAttr),
    Merged   = Table.NestedJoin(Src, {"MatKey"}, AttrSrc, {"MatKey"},
                   "attr", JoinKind.LeftOuter),
    Expanded = Table.ExpandTableColumn(Merged, "attr", {"Nature"}),

    // Same second pass as factRM: the material on its own, for rows the plant-qualified
    // key missed because the FG Master sheet has no valuation area or writes it differently.
    ByMat    = Table.Buffer(Table.Distinct(Table.SelectColumns(AttrSrc,
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

    // The last three digits of the material description: a module's wattage, 580 or 595.
    RateTxt  = Table.AddColumn(Named, "RateText",
                   each Text.End(Text.Trim([MaterialDesc] ?? ""), 3), type text),
    RateNum  = Table.AddColumn(RateTxt, "RateRaw",
                   each try Number.From(Text.Select([RateText], {"0".."9","."})) otherwise null,
                   type number),

    // A cell's efficiency is the percentage the description ends with, and it is a percentage
    // written out: "C-PERC-P-FC-182.20x183.75-10BB-23.50%" ends 23.50%, so the efficiency is
    // 0.235. Reading the last three characters instead gives "50%" -> 50 -> 0.05, a rate of
    // 1.7 W where the cell is 7.8, which is what left Dholera Cell's megawatts short. The last
    // hyphen-separated piece is taken, so a longer or shorter description makes no difference,
    // and a figure already typed as a fraction (0.235) is left as it is.
    EffCol   = Table.AddColumn(RateNum, "EffFrac",
                   each let Txt  = Text.Trim(Text.From([MaterialDesc] ?? "")),
                            Last = List.Last(Text.Split(Txt, "-")),
                            Num  = try Number.From(Text.Select(Last, {"0".."9","."}))
                                   otherwise null
                        in  if Num = null then null
                            else if Num > 1 then Num / 100
                            else Num,
                   type number),

    // Mid = MID(desc,13,13)  -- M counts from 0, so the start is 12. On a cell this is the
    // wafer size, written "182.20x183.75".
    MidCol   = Table.AddColumn(EffCol, "Mid",
                   each try Text.Middle(Text.Trim([MaterialDesc] ?? ""), 12, 13) otherwise null,
                   type text),
    // Base = LEFT(Mid,6) - the first of the two dimensions, as a number
    BaseCol  = Table.AddColumn(MidCol, "Base",
                   each try Number.From(Text.Select(Text.Start([Mid], 6), {"0".."9","."}))
                        otherwise null, type number),

    // A module and a cell are rated differently, and the plant is what says which:
    //   1900, 1902 (modules):  Rate = RIGHT(description,3)                     -> about 580 W
    //   1905 (cells):          Rate = Base x Base x efficiency / 1000          -> about 7.8 W
    // For the cell that is 182.20 x 182.20 x 0.235 / 1000, the same arithmetic as the FG
    // Console sheet, and a cell whose description carries no size or no percentage is left
    // without a rate rather than given a module's.
    Rate     = Table.AddColumn(BaseCol, "Rate",
                   each if Text.Trim(Text.From([ValuationArea] ?? "")) = "1905"
                        then (if [Base] = null or [EffFrac] = null then null
                              else try [Base] * [Base] * [EffFrac] / 1000 otherwise null)
                        else [RateRaw],
                   type number),
    RateBad  = Table.AddColumn(Rate, "RateParseFailed",
                   each [Rate] = null, type logical),

    // MW = Closing Stock * Rate / 10^6
    MW       = Table.AddColumn(RateBad, "MW",
                   each try [CloseQty] * [Rate] / 1000000 otherwise null, type number),

    // Inr Wp = Closing Value / (MW * 10^6). A zero or missing MW is left blank rather than
    // divided by: dividing by zero in M produces NaN, which then prints as NaN in the report.
    INRwp    = Table.AddColumn(MW, "INR_WP",
                   each if [MW] = null or [MW] = 0 then null
                        else try [CloseVal] / ([MW] * 1000000) otherwise null, type number),

    Cleaned  = Table.RemoveColumns(INRwp, {"RateText", "RateRaw", "EffFrac"})
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
                   {"Mid", type text}, {"Base", type number}, {"INR_WP", type number}}),
    // last line of defence against a blank category: whatever slipped through above is
    // named, so no visual anywhere can show a nameless (Blank) row
    NoNulls  = Table.TransformColumns(Typed, {
                   {"Nature",      each if _ = null or _ = "" then "Unassigned" else _, type text},
                   {"GroupNature", each if _ = null or _ = "" then "Unassigned" else _, type text}}),
    // The report covers the plants Plant Master names, and the trial balance's other plants
    // are deliberately ignored: they are real codes in SAP but no part of this report. A row
    // whose valuation area is blank, or is a code that sheet does not list, is dropped rather
    // than parked on an Unallocated row. qcPlantCodes on Checks lists every code the files
    // contained and what it was worth, so a dropped row is never a silent one.
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
    // One row per plant, material, month and type - because that is what an export holds. The
    // same material appears for several plants, but never twice for one plant in one month, so
    // a second line for the same four is the same balance arriving twice (a storage-location or
    // special-stock split, or a month re-exported) and adding them multiplies that material's
    // stock. The line kept is the one with the largest closing quantity, which is the whole
    // balance rather than a part of it.
    // One grouping pass does it. It used to be a full sort of the table, then a distinct, then
    // a second grouping for the counts, then a merge back onto the first - four passes over
    // fifty thousand rows, of which the sort alone holds the whole table in memory and cannot
    // fold. Table.Max picks the row inside each group as the group is formed, so the table is
    // walked once.
    Picked   = Table.Group(OneEach, {"ValuationArea", "Material", "Month", "Category"},
                   {{"Row", each Table.Max(_, "CloseQty"), type record}}),
    Expanded = Table.ExpandRecordColumn(Table.SelectColumns(Picked, {"Row"}), "Row",
                   Table.ColumnNames(OneEach)),
    // Expanding a record hands every column back as "any", and a whole-number column arriving
    // as any is read by the model as text - which is what made SUM refuse to add Closing Value
    // and emptied every visual on the page. The types are put back from the table the rows came
    // out of, so the column list and the types are the ones stated above and nothing is guessed.
    Unused   = Table.TransformColumnTypes(Expanded,
                   List.Transform(Table.ColumnNames(OneEach),
                       each {_, Type.TableColumn(Value.Type(OneEach), _)})),
    // the column list written out, so what this query hands on is stated rather than inferred
    KeepCols = {"SourceFile","ValuationArea","Material","MatKey","MaterialDesc","FromDate",
                "ToDate","OpenQty","OpenVal","ReceiptQty","ReceiptVal","IssueQty","IssueVal",
                "CloseQty","CloseVal","BaseUOM","SpecialStock","Currency","Month","Category",
                "Nature","GroupNature","BOMStdQty","Item","AttrMissing","MW","Rate",
                "RateParseFailed","Mid","Base","INR_WP"},
    Collapsed = Table.SelectColumns(Unused, KeepCols),
    // the megawatt column is renamed because Power BI will not let a table hold a column
    // and a measure with the same name, and the report needs the measure to be called MW
    Renamed  = Table.RenameColumns(Collapsed, {{"MW", "MW Qty"}}),
    // the flat plant-and-type key. dimPlantType joins on it, which is what lets a matrix show
    // one row per plant AND type without a two-level row hierarchy - and a hierarchy is the
    // one thing some versions of Desktop insist on opening collapsed, hiding the rows.
    Keyed    = Table.AddColumn(Renamed, "PlantType",
                   each Text.From([ValuationArea] ?? "") & "|" & Text.From([Category] ?? ""),
                   type text)
in
    Keyed
```

## varRMTechnologyCosts

> Reads only the externally supplied, effective-dated Cost INR/Wp inputs for the Module and Cell component rows. Dates run across the columns; a blank means unchanged and an intentional zero stays zero. Enable load OFF.

```
let
    Norm     = (v as any) as text => Text.Upper(Text.Remove(Text.Trim(Text.From(v ?? "")), {" ",".","_","-","/","(",")"})),
    Sheets   = Table.SelectRows(varWorkbook, each [Kind] = "Sheet"),
    Hit      = Table.SelectRows(Sheets, each List.Contains({"RMTECHNOLOGYCOSTS","RMTECHCOSTS","RMTECHNOLOGY"}, Norm([Item]))),
    Data     = if Table.IsEmpty(Hit) then #table({}, {}) else Hit{0}[Data],
    Raw      = if Table.IsEmpty(Hit) then #table({}, {}) else Table.PromoteHeaders(Data, [PromoteAllScalars=true]),
    Names    = Table.ColumnNames(Raw),
    GroupCol = List.First(List.Select(Names, each List.Contains({"PLANTGROUP","GROUP","TYPE"}, Norm(_))), null),
    ItemCol  = List.First(List.Select(Names, each List.Contains({"ITEM","COMPONENT","NATURE"}, Norm(_))), null),
    Fixed    = List.RemoveNulls({GroupCol, ItemCol}),
    DateCols = List.Select(List.Difference(Names, Fixed), each
                   (try Date.From(DateTime.FromText(Text.From(_))) otherwise
                    try Date.FromText(Text.BeforeDelimiter(Text.From(_), " ")) otherwise null) <> null),
    Kept     = if GroupCol = null or ItemCol = null then #table({}, {})
               else Table.SelectColumns(Raw, Fixed & DateCols),
    Named    = if Table.IsEmpty(Kept) then Kept else Table.RenameColumns(Kept, {{GroupCol,"PlantGroup"},{ItemCol,"Item"}}),
    Long     = if Table.IsEmpty(Named) then #table({}, {})
               else Table.UnpivotOtherColumns(Named, {"PlantGroup","Item"}, "EffectiveText", "Input"),
    Dated    = Table.AddColumn(Long, "EffectiveFrom", each
                   try Date.From(DateTime.FromText(Text.From([EffectiveText])))
                   otherwise try Date.FromText(Text.BeforeDelimiter(Text.From([EffectiveText]), " "))
                   otherwise null, type date),
    Costed   = Table.AddColumn(Dated, "CostINRWp", each
                   let t = Text.Trim(Text.From([Input] ?? ""))
                   in  if t = "" then null else if t = "-" then 0
                       else try Number.From([Input]) otherwise try Number.From(t) otherwise null,
                   type number),
    Clean    = Table.SelectRows(Costed, each [EffectiveFrom] <> null and [CostINRWp] <> null
                   and Text.Trim(Text.From([PlantGroup] ?? "")) <> ""
                   and Text.Trim(Text.From([Item] ?? "")) <> ""),
    Out      = Table.TransformColumns(Table.SelectColumns(Clean, {"EffectiveFrom","PlantGroup","Item","CostINRWp"}), {
                   {"PlantGroup", each Text.Proper(Text.Trim(Text.From(_))), type text},
                   {"Item", each Text.Trim(Text.From(_)), type text}}),
    Buffered = Table.Buffer(Out)
in
    Buffered
```

## varRMPlantCosts

> Reads the separate effective-dated Cost INR/Wp inputs for 1900 and 1902. The same item may have a different cost at each plant. Enable load OFF.

```
let
    Norm     = (v as any) as text => Text.Upper(Text.Remove(Text.Trim(Text.From(v ?? "")), {" ",".","_","-","/","(",")"})),
    Sheets   = Table.SelectRows(varWorkbook, each [Kind] = "Sheet"),
    Hit      = Table.SelectRows(Sheets, each List.Contains({"RMPLANTCOSTS","RMPLANTCOST"}, Norm([Item]))),
    Data     = if Table.IsEmpty(Hit) then #table({}, {}) else Hit{0}[Data],
    Raw      = if Table.IsEmpty(Hit) then #table({}, {}) else Table.PromoteHeaders(Data, [PromoteAllScalars=true]),
    Names    = Table.ColumnNames(Raw),
    PlantCol = List.First(List.Select(Names, each List.Contains({"PLANT","VALUATIONAREA","PLANTCODE"}, Norm(_))), null),
    ItemCol  = List.First(List.Select(Names, each List.Contains({"ITEM","COMPONENT","NATURE"}, Norm(_))), null),
    Fixed    = List.RemoveNulls({PlantCol, ItemCol}),
    DateCols = List.Select(List.Difference(Names, Fixed), each
                   (try Date.From(DateTime.FromText(Text.From(_))) otherwise
                    try Date.FromText(Text.BeforeDelimiter(Text.From(_), " ")) otherwise null) <> null),
    Kept     = if PlantCol = null or ItemCol = null then #table({}, {})
               else Table.SelectColumns(Raw, Fixed & DateCols),
    Named    = if Table.IsEmpty(Kept) then Kept else Table.RenameColumns(Kept, {{PlantCol,"ValuationArea"},{ItemCol,"Item"}}),
    Long     = if Table.IsEmpty(Named) then #table({}, {})
               else Table.UnpivotOtherColumns(Named, {"ValuationArea","Item"}, "EffectiveText", "Input"),
    Dated    = Table.AddColumn(Long, "EffectiveFrom", each
                   try Date.From(DateTime.FromText(Text.From([EffectiveText])))
                   otherwise try Date.FromText(Text.BeforeDelimiter(Text.From([EffectiveText]), " "))
                   otherwise null, type date),
    Costed   = Table.AddColumn(Dated, "CostINRWp", each
                   let t = Text.Trim(Text.From([Input] ?? ""))
                   in  if t = "" then null else if t = "-" then 0
                       else try Number.From([Input]) otherwise try Number.From(t) otherwise null,
                   type number),
    Clean    = Table.SelectRows(Costed, each [EffectiveFrom] <> null and [CostINRWp] <> null
                   and Text.Trim(Text.From([ValuationArea] ?? "")) <> ""
                   and Text.Trim(Text.From([Item] ?? "")) <> ""),
    Out      = Table.TransformColumns(Table.SelectColumns(Clean, {"EffectiveFrom","ValuationArea","Item","CostINRWp"}), {
                   {"ValuationArea", each Text.Trim(Text.From(_)), type text},
                   {"Item", each Text.Trim(Text.From(_)), type text}}),
    Buffered = Table.Buffer(Out)
in
    Buffered
```

## varRMConstants

> Reads the four externally supplied values: Module Production Constant, Cell Production Constant, 1900 Plant Variable and 1902 Plant Variable. Dates run across the columns and the latest value at or before a month applies. Enable load OFF.

```
let
    Norm     = (v as any) as text => Text.Upper(Text.Remove(Text.Trim(Text.From(v ?? "")), {" ",".","_","-","/","(",")"})),
    Sheets   = Table.SelectRows(varWorkbook, each [Kind] = "Sheet"),
    Hit      = Table.SelectRows(Sheets, each List.Contains({"RMCONSTANTS","RMDAYSCONSTANTS"}, Norm([Item]))),
    Data     = if Table.IsEmpty(Hit) then #table({}, {}) else Hit{0}[Data],
    Raw      = if Table.IsEmpty(Hit) then #table({}, {}) else Table.PromoteHeaders(Data, [PromoteAllScalars=true]),
    Names    = Table.ColumnNames(Raw),
    NameCol  = List.First(List.Select(Names, each List.Contains({"CONSTANTNAME","CONSTANT","NAME"}, Norm(_))), null),
    DateCols = if NameCol = null then {} else List.Select(List.RemoveItems(Names, {NameCol}), each
                   (try Date.From(DateTime.FromText(Text.From(_))) otherwise
                    try Date.FromText(Text.BeforeDelimiter(Text.From(_), " ")) otherwise null) <> null),
    Kept     = if NameCol = null then #table({}, {}) else Table.SelectColumns(Raw, {NameCol} & DateCols),
    Named    = if Table.IsEmpty(Kept) then Kept else Table.RenameColumns(Kept, {{NameCol,"ConstantName"}}),
    Long     = if Table.IsEmpty(Named) then #table({}, {})
               else Table.UnpivotOtherColumns(Named, {"ConstantName"}, "EffectiveText", "Input"),
    Dated    = Table.AddColumn(Long, "EffectiveFrom", each
                   try Date.From(DateTime.FromText(Text.From([EffectiveText])))
                   otherwise try Date.FromText(Text.BeforeDelimiter(Text.From([EffectiveText]), " "))
                   otherwise null, type date),
    Valued   = Table.AddColumn(Dated, "Value", each
                   let t = Text.Trim(Text.From([Input] ?? ""))
                   in  if t = "" then null else if t = "-" then 0
                       else try Number.From([Input]) otherwise try Number.From(t) otherwise null,
                   type number),
    Clean    = Table.SelectRows(Valued, each [EffectiveFrom] <> null and [Value] <> null
                   and Text.Trim(Text.From([ConstantName] ?? "")) <> ""),
    Out      = Table.TransformColumns(Table.SelectColumns(Clean, {"EffectiveFrom","ConstantName","Value"}), {
                   {"ConstantName", each Text.Trim(Text.From(_)), type text}}),
    Buffered = Table.Buffer(Out)
in
    Buffered
```

## varMWCapacity

> Reads the MW sheet in whichever of three layouts it is written, and picks by itself. **The one to keep it in** is a date across the top and a plant down the side: an optional first column naming the technology, a column of plant codes, then one column per month, headed with that month's date - a new month is a new column and nothing already typed is touched. It also still reads the long layout (`Effective From | Tech | Valuation Area | MW`) and the original wide one (`Tech` down the side, 1900/1902/1905 across the top). Headers are matched ignoring case, spaces and punctuation. One dated column is enough - the sheet is meant to start with a single month and grow a column each time a figure changes. A date column is an *effective from*, so a month with no column keeps the last figure typed before it; an empty cell is left empty rather than read as nought; `-` is nought. Plant codes are forced to text so they join to `dimPlant`. With no technology column the row is the plant's whole capacity, written against `(All)`.

```
let
    Wb      = varWorkbook,
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
    // a row that is the plant's whole capacity rather than one technology's. Written as
    // Total on the MW sheet - the March'26 | MW(S) block - and carried through as (All),
    // which is the name the days-of-cover measure looks for. It is not a nature and never
    // appears as one: dimNature drops it, so it cannot be sliced or drawn as a slice.
    TechName = (v as any) as text =>
                  let T = AsTxt(v) in
                  if List.Contains({"TOTAL","ALL","ALLPLANTS","PLANTTOTAL","TOTALPLANT",
                                    "GRANDTOTAL","MWS","CAPACITY","ALL"}, Norm(T))
                      then "(All)" else T,
    // a header cell that is a real date. A number is never taken for one: 1900 is a plant,
    // and Date.From would happily read it as a day in 1904.
    AsDate  = (v as any) as nullable date =>
                  if v = null then null
                  else if Value.Is(v, type date) then v
                  else if Value.Is(v, type datetime) then DateTime.Date(v)
                  else if Value.Is(v, type text) and (Text.Contains(v, "/") or Text.Contains(v, "-"))
                       then (try Date.From(v) otherwise null)
                  else null,

    // ---- decide which layout this sheet is -------------------------------------------------
    // long layout is identified by an Effective From header; wide layout by a row of plant codes
    DateHdr = {"EFFECTIVEFROM","EFFECTIVEDATE","FROMDATE"},
    LongIdx = List.PositionOf(
                  List.Transform(Rows, (r) =>
                      List.AnyTrue(List.Transform(r, (c) => List.Contains(DateHdr, Norm(c))))), true),
    WideIdx = List.PositionOf(
                  List.Transform(Rows, (r) => List.Count(List.Select(r, IsCode)) >= 2), true),
    // matrix layout: a header row carrying at least one real date, plants down the side.
    // One dated column is the normal starting point - the sheet grows a column per change -
    // so the layout is claimed on a single date, and only when plant codes sit underneath it.
    MtxCand = List.PositionOf(
                  List.Transform(Rows, (r) =>
                      List.Count(List.RemoveNulls(List.Transform(r, AsDate))) >= 1), true),
    MtxCodes = MtxCand >= 0 and List.AnyTrue(List.Transform(List.Skip(Rows, MtxCand + 1),
                  (r) => List.AnyTrue(List.Transform(r, IsCode)))),
    MtxIdx  = if MtxCodes then MtxCand else -1,

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
                                Tech          = TechName(r{iTech}),
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
                                Tech          = TechName(List.First(r)),
                                ValuationArea = m[Code],
                                MW            = (try Number.From(r{m[Idx]}) otherwise 0) ])
              in  Recs,

    // ---- matrix layout: a month per column, a plant per row ---------------------------------
    // the layout to keep the sheet in. Each date column is an effective-from, so the figure
    // stands until a later column changes it and a month with no column of its own is not a
    // hole. A blank cell is not nought: nought capacity would wipe out the figure before it.
    Matrix  = let
                  Hdr    = Rows{MtxIdx},
                  Cols   = List.Select(
                               List.Transform({0..List.Count(Hdr) - 1},
                                   (i) => [Idx = i, D = AsDate(Hdr{i})]),
                               (m) => m[D] <> null),
                  DIdx   = List.Transform(Cols, each _[Idx]),
                  Body   = List.Skip(Rows, MtxIdx + 1),
                  Other  = List.Select({0..List.Count(Hdr) - 1}, (i) => not List.Contains(DIdx, i)),
                  // the plant column is whichever of the remaining columns holds the codes
                  Score  = List.Transform(Other, (i) =>
                               [ Idx = i,
                                 N   = List.Count(List.Select(Body,
                                           (r) => IsCode(try r{i} otherwise null))) ]),
                  Best   = List.Last(List.Sort(Score, (a, b) => Value.Compare(a[N], b[N])), null),
                  iArea  = if Best = null or Best[N] = 0 then -1 else Best[Idx],
                  Chk    = if iArea < 0
                               then error "The MW sheet has month columns but no column of plant "
                                        & "codes (1900 / 1902 / 1905) beside them. Read qcMWSheet."
                               else true,
                  // a technology column is optional: the first other column that carries text
                  Named  = List.Select(Other, (i) =>
                               i <> iArea and List.AnyTrue(List.Transform(Body,
                                   (r) => AsTxt(try r{i} otherwise null) <> ""
                                          and not IsCode(try r{i} otherwise null)))),
                  iTech  = if not Chk or List.IsEmpty(Named) then -1 else List.First(Named),
                  Keep   = if Chk then List.Select(Body, (r) => IsCode(try r{iArea} otherwise null))
                           else {},
                  Cells  = List.TransformMany(Keep, (r) => Cols, (r, c) =>
                               [ EffectiveFrom = c[D],
                                 Tech          = if iTech < 0 or AsTxt(try r{iTech} otherwise null) = ""
                                                 then "(All)" else TechName(r{iTech}),
                                 ValuationArea = AsTxt(r{iArea}),
                                 Raw           = (try r{c[Idx]} otherwise null) ]),
                  Filled = List.Select(Cells, (x) => AsTxt(x[Raw]) <> ""),
                  Recs   = List.Transform(Filled, (x) =>
                               [ EffectiveFrom = x[EffectiveFrom],
                                 Tech          = x[Tech],
                                 ValuationArea = x[ValuationArea],
                                 MW            = (if AsTxt(x[Raw]) = "-" then 0
                                                  else try Number.From(x[Raw]) otherwise 0) ])
              in  Recs,

    Pairs   = if LongIdx >= 0 then Long
              else if MtxIdx >= 0 then Matrix
              else if WideIdx >= 0 then Wide
              else error "The MW sheet is none of the three layouts I recognise: no Effective "
                       & "From/Tech header row, no row of month dates over a column of plant "
                       & "codes, and no row containing two of 1900/1902/1905. Read qcMWSheet.",
    T       = Table.FromRecords(Pairs,
                  type table [EffectiveFrom = date, Tech = text, ValuationArea = text, MW = number]),
    Out     = Table.Buffer(T)
in
    Out
```


## varMonthGrid

> The months the effective-dated sheets are spread over: MW capacity and the RM costs each hold a value against a date, and one row per month is what lets a matrix show a figure for a month with no column of its own. It runs from the earliest date typed on those sheets to eighteen months past today, and reads no stock file at all - which is the point, because `dimCapacity` and the two RM tables used to take this list from `dimDate` and drag the whole data folder through with it. A month in this grid that the data has no rows for simply goes unused.

```
let
    Dates  = List.RemoveNulls(List.Combine({
                 try varMWCapacity[EffectiveFrom] otherwise {},
                 try varRMTechnologyCosts[EffectiveFrom] otherwise {},
                 try varRMPlantCosts[EffectiveFrom] otherwise {},
                 try varRMConstants[EffectiveFrom] otherwise {}})),
    First  = if List.IsEmpty(Dates) then Date.StartOfMonth(Date.From(DateTime.LocalNow()))
             else Date.StartOfMonth(List.Min(Dates)),
    Last   = Date.StartOfMonth(Date.AddMonths(Date.From(DateTime.LocalNow()), 18)),
    Span   = (Date.Year(Last) * 12 + Date.Month(Last))
             - (Date.Year(First) * 12 + Date.Month(First)),
    Months = if Span < 0 then {First}
             else List.Transform({0..Span}, (i) => Date.AddMonths(First, i)),
    Out    = List.Buffer(Months)
in
    Out
```

## dimNature

> Bridge table. Without it, slicing FG by Nature leaves Capacity MW unfiltered and Days is wrong everywhere except the grand total.

```
let
    FromRM  = List.RemoveNulls(dimMaterialAttr[Nature]),
    FromFG  = List.RemoveNulls(dimFGAttr[Nature]),
    // (All) is the MW sheet saying 'this is the whole plant, not one technology'. It is a
    // capacity row, never a nature, and listing it here would draw it as a slice and a slicer tick.
    FromCap = List.Select(List.RemoveNulls(varMWCapacity[Tech]), each _ <> "(All)"),
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
    // One normalisation for both keys and both sides, and it has to survive everything Excel
    // and SAP do to a code that is really just a number. The export writes a profit centre
    // with two leading zeros that the sheet does not have; one file holds it as text and the
    // other as a number, so 1902001 arrives as "1902001", "001902001", "1902001.0" or with a
    // space or a hyphen inside it. So: take the digits and letters, drop everything else,
    // upper-case it, and drop leading zeros. All of those then come out as 1902001, and a
    // code that is genuinely different still is.
    KeyOf    = (v as any) as text =>
                   let T = Text.Trim(Text.From(v ?? "")),
                       // a code has no fraction: 1902001.0 is Excel's doing, not SAP's
                       D = if Text.Contains(T, ".") then Text.Start(T, Text.PositionOf(T, ".")) else T,
                       K = Text.Upper(Text.Select(D, {"0".."9", "a".."z", "A".."Z"})),
                       Z = Text.TrimStart(K, "0")
                   in  if Z = "" then K else Z,
    Keys     = Table.AddColumn(
                   Table.TransformColumns(Renamed, {
                       {"GLAccount",    each KeyOf(_), type text},
                       {"ProfitCentre", each Text.Trim(Text.From(_ ?? "")), type text}}),
                   "PCKey", each KeyOf([ProfitCentre]), type text),
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
    // 1902 Jaipur Module, 1900 Dholera Module, 1905 Dholera Cell - the same three names the
    // whole report uses, and the codes as the Summary workbook has them. A profit centre that
    // spells the plant out instead of numbering it is still a plant, and 1905 was being lost
    // for exactly that reason: "Dholera Cell" carries no 1905 anywhere in it. Cell is tested
    // before Dholera, because Dholera Cell contains both words.
    ByName   = (t as any) as nullable text =>
                   let T = Text.Upper(Text.From(t ?? "")) in
                   if Text.Contains(T, "JAIPUR") then "1902"
                   else if Text.Contains(T, "CELL") then "1905"
                   else if Text.Contains(T, "DHOLERA") then "1900"
                   else null,
    PlantRaw = Table.AddColumn(Keys, "PlantCode",
                   each try Text.Middle([ProfitCentre], 2, 4) otherwise null, type text),
    PlantCol = Table.AddColumn(PlantRaw, "ValuationArea",
                   each if List.Contains(Known, [PlantCode]) then [PlantCode]
                        else if Anywhere([ProfitCentre]) <> null then Anywhere([ProfitCentre])
                        else if Anywhere([ProfitCentreDesc]) <> null then Anywhere([ProfitCentreDesc])
                        else if ByName([ProfitCentreDesc]) <> null then ByName([ProfitCentreDesc])
                        else ByName([ProfitCentre]),
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
    // factTB_Staged (which opens the TB folder) and a query that opens the workbook is
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
                          {{"Plant","Plant Number","Plant No","Plant Code",
                            "Valuation Area","NaturePlant2"},                     "TBPlant"},
                          {{"Sort Order","SortOrder","Sort"},                      "TBSort"},
                          {{"Profit Center","Profit Centre","ProfitCenter","ProfitCentre",
                            "Profit Ctr","PRCTR"},                                  "MPC"}
                        })
                otherwise #table({}, {}),
    MCols    = {"GLAccount","PCKey","Nature","TBPlant","TBSort"},
    MPad     = List.Accumulate(
                   List.Difference({"GLAccount","MPC","Nature","TBPlant","TBSort"},
                       Table.ColumnNames(MasterRaw)),
                   MasterRaw, (t, c) => Table.AddColumn(t, c, each null)),
    // Both keys normalised the same way on both sides, so a code typed as a number in one
    // file and as text in the other still matches: 0000123400 and 123400 and 123400.0 all
    // come out as 123400.
    MKey     = Table.AddColumn(
                   Table.TransformColumns(MPad, {
                       {"GLAccount", each KeyOf(_), type text}}),
                   "PCKey", each KeyOf([MPC]), type text),
    MSort    = Table.TransformColumns(MKey, {
                   {"TBSort", each try Int64.From(Number.Round(Number.From(_))) otherwise null,
                    Int64.Type},
                   {"Nature",  each Text.Trim(Text.From(_ ?? "")), type text},
                   {"TBPlant", each Text.Trim(Text.From(_ ?? "")), type text}}),
    MReal    = Table.SelectRows(MSort, each [GLAccount] <> ""),
    // a plant code written on the master sheet itself, in the Plant column or inside the
    // NaturePlant text - the last resort when the profit centre carries no code at all
    // the GL account is the one key the trial balance and TB Master certainly share, so the
    // plant written against a GL on that sheet is read as a code (1905) or as a name
    // (Dholera Cell), in that order, on both of its columns
    MPlanted = Table.Buffer(Table.AddColumn(MReal, "MasterPlant",
                   each if Anywhere([TBPlant]) <> null then Anywhere([TBPlant])
                        else if Anywhere([Nature]) <> null then Anywhere([Nature])
                        else if ByName([TBPlant]) <> null then ByName([TBPlant])
                        else ByName([Nature]), type text)),
    // The GL account alone cannot name a plant: TB Master lists the same GL against all three
    // plants, so on its own it is a whitelist and nothing more. The pair - GL account AND
    // profit centre - is what identifies one row of that sheet, and only then do its Plant,
    // Nature and Sort belong to the trial-balance line. That pair is the report's answer for
    // every trial-balance figure on every page.
    // A pair is only an answer if the sheet is unanimous about it. Where the same GL account
    // and profit centre appear on TB Master twice with different Plants, the join used to
    // take whichever row it met first - which put some accounts on the wrong plant and left
    // others right, scattered rather than swapped, and no way to see it had happened. Those
    // pairs are held back here: they resolve to nothing, they are counted nowhere, and
    // qcTBUnmatched names them with 'two plants on TB Master for this pair'.
    // and the same sheet read by GL alone, for the two jobs the pair cannot do: saying whether
    // an account is an inventory account at all, and giving its nature where the pair has no
    // row. Its plant is deliberately not used - that is the ambiguity the pair exists to
    // remove.
    MasterGL = Table.Buffer(
                   Table.RenameColumns(
                       Table.Distinct(
                           Table.SelectColumns(MPlanted, {"GLAccount","Nature","TBSort"}),
                           {"GLAccount"}),
                       {{"Nature","GLNature"},{"TBSort","GLTBSort"}})),
    MGroup   = Table.Group(MPlanted, {"GLAccount", "PCKey"}, {
                   {"Plants",  each List.Distinct(List.Select(List.Transform([TBPlant],
                                   each Text.Trim(Text.From(_ ?? ""))), each _ <> "")), type list},
                   {"Natures", each List.Distinct(List.Select(List.Transform([Nature],
                                   each Text.Trim(Text.From(_ ?? ""))), each _ <> "")), type list},
                   {"Rows",    each Table.RowCount(_), Int64.Type}}),
    MAmbig   = Table.SelectRows(MGroup, each List.Count([Plants]) > 1),
    // One row per GL account and profit centre, and where TB Master carries that pair more
    // than once it is the FIRST of them, in the sheet's own row order. That is not a choice
    // about which plant is correct - it is what VLOOKUP does, and the figures the old report
    // was checked against were produced by VLOOKUP on this same sheet. Holding those pairs
    // back instead emptied a plant's RM; taking the first row reproduces the old numbers.
    // qcTBUnmatched still names every such pair with both plants, so the sheet can be
    // corrected and the answer then stops depending on row order at all.
    MasterPair = Table.Buffer(
                     Table.Distinct(Table.SelectColumns(MPlanted, MCols),
                         {"GLAccount", "PCKey"})),
    // the pairs the sheet contradicts itself about, carried through only so each line can say
    // that its plant came from the first of two rows rather than from an unambiguous one
    AmbigKeys = Table.Buffer(Table.AddColumn(
                    Table.SelectColumns(MAmbig, {"GLAccount","PCKey","Plants"}),
                    "AmbigPlants", each Text.Combine([Plants], " / "), type text)),
    Joined   = Table.NestedJoin(Typed, {"GLAccount","PCKey"}, MasterPair, {"GLAccount","PCKey"},
                   "tpl", JoinKind.LeftOuter),
    Joined2  = Table.NestedJoin(Joined, {"GLAccount"}, MasterGL, {"GLAccount"},
                   "tgl", JoinKind.LeftOuter),
    Joined3  = Table.NestedJoin(Joined2, {"GLAccount","PCKey"},
                   Table.SelectColumns(AmbigKeys, {"GLAccount","PCKey","AmbigPlants"}),
                   {"GLAccount","PCKey"}, "tam", JoinKind.LeftOuter),
    // an inventory account is one the sheet lists at all; whether its plant is known is a
    // separate question, answered by PairMatched below
    Flagged  = Table.AddColumn(Joined3, "Whitelisted",
                   each not Table.IsEmpty([tgl]), type logical),
    Paired   = Table.AddColumn(Flagged, "PairMatched",
                   each not Table.IsEmpty([tpl]), type logical),
    Widened  = Table.ExpandTableColumn(
                   Table.ExpandTableColumn(
                       Table.ExpandTableColumn(Paired, "tpl", {"Nature","TBPlant","TBSort"}),
                       "tgl", {"GLNature","GLTBSort"}),
                   "tam", {"AmbigPlants"}),
    // the nature is the matched row's, and where the pair has no row yet the GL's own nature
    // stands in - so Consumables & Spares is never guessed at from the account name
    Natured  = Table.AddColumn(Widened, "NatureUse",
                   each if Text.Trim(Text.From([Nature] ?? "")) <> "" then [Nature]
                        else [GLNature], type text),
    // The plant is the matched row's Plant column, read as a code (1905) or as a plant name
    // (Dholera Cell). There is no second rule: reading it from the profit centre as well made
    // two rules run at once and moved the figures further off. Where TB Master gives the pair
    // two plants, the row used is the first one on the sheet - VLOOKUP's own behaviour, and
    // the behaviour the old report's figures came from. A pair with no row at all resolves to
    // nothing, is left out of every trial-balance figure, and is listed by qcTBUnmatched with
    // what it is worth.
    FromPair = Table.AddColumn(Natured, "PairPlant",
                   each if Anywhere([TBPlant]) <> null then Anywhere([TBPlant])
                        else ByName([TBPlant]), type text),
    Resolved = Table.AddColumn(FromPair, "PlantResolved", each [PairPlant], type text),
    // how each line was placed, in words - so Checks can say whether a plant is short
    // because the sheet has no row for it, and which lines depended on the sheet's row order
    Ruled    = Table.AddColumn(Resolved, "Rule",
                   each if [PairPlant] <> null and [AmbigPlants] <> null
                        then "sheet gave two plants, first row used"
                        else if [PairPlant] <> null then "matched on GL and profit centre"
                        else if [Whitelisted] then "dropped: no row for this GL and profit centre"
                        else "not an inventory account", type text),
    Dropped  = Table.RemoveColumns(Ruled, {"ValuationArea", "PairPlant"}),
    Renamed2 = Table.RenameColumns(Dropped, {{"PlantResolved", "ValuationArea"}}),
    // Rows that resolve to none of the three plants are kept HERE and left out in factTB, so
    // qcTBPlants can still see them: a plant going missing from Inventory (TB) has to be
    // visible somewhere, and a row silently dropped at this step is a row nobody can find.
    Natured2 = Table.RemoveColumns(
                   Table.RenameColumns(
                       Table.RemoveColumns(Renamed2, {"Nature"}),
                       {{"NatureUse", "Nature"}}),
                   {"GLNature", "GLTBSort"}),
    Out      = Table.TransformColumnTypes(Natured2, {
                   {"Nature", type text}, {"TBPlant", type text}, {"TBSort", Int64.Type},
                   {"ValuationArea", type text}, {"Rule", type text}})
in
    Out
```


## dimPlant

> One row per plant the report knows about: every code the **Plant Master** sheet names, every code the Plant column of **TB Master** names, and every code the stock files and the trial balance actually contain. A code no sheet names is still listed, under itself, so no plant can be missing from a figure without appearing on the page. The three known plants keep their names whatever a sheet says, because a swapped pair of spreadsheet rows once renamed Jaipur and Dholera on every page at once.

```
let
    // The three plants and their names are decided here and nowhere else, so no sheet and no
    // The names come from the Plant Master sheet; the pairs below are only what the report
    // falls back to when that sheet names no plant at all, so a swapped pair on the sheet
    // is corrected on the sheet and nowhere else.
    Fixed    = #table(
        type table [ValuationArea = text, Plant = text, PlantSortNo = Int64.Type],
        {
            {"1902", "1902 Jaipur Module",  1},
            {"1900", "1900 Dholera Module", 2},
            {"1905", "1905 Dholera Cell",   3}
        }),
    Master   = Table.Buffer(try dimPlantMaster otherwise #table(
                   type table [ValuationArea = text, Plant = text, PlantSortNo = Int64.Type,
                               MWD = nullable number], {})),
    // codes the masters name, and codes the files themselves hold - the union of the two, so a
    // plant is reported whether it was declared or merely arrived
    Named    = if Table.IsEmpty(Master) then {"1900","1902","1905"}
               else Master[ValuationArea],
    Seen     = List.Distinct(List.RemoveNulls(
                   List.Transform(Named, each Text.Trim(Text.From(_ ?? ""))))),
    // The plants are the ones Plant Master and TB Master name, and that is the end of it. This
    // step used to read factInventory and factTB_Staged as well, to drop a plant that no file
    // had any stock for - and it cost a fortune: every query that touches dimPlant made both
    // fact tables run again, and each of those re-parses the workbook, which is why a refresh
    // that took five minutes came to take thirty. A declared plant with no stock now shows as
    // an empty row instead, which is the cheaper mistake and a visible one.
    Codes    = List.Select(Seen, each _ <> ""),
    // the label: the fixed name for the three, the Plant Master name for anything else it
    // names, and the bare code for a plant nobody has named yet
    MWDOf    = (c as text) as nullable number =>
                   let m = Table.SelectRows(Master, (r) => r[ValuationArea] = c)
                   in  if Table.IsEmpty(m) then null
                       else try Number.From(Table.First(m)[MWD]) otherwise null,
    // Plant Master decides the name. The built-in pairs are used only for a code that sheet
    // does not name, because a name written in two places is a name that can disagree with
    // itself - which is how Jaipur and Dholera came to be reading each other's figures.
    NameOf   = (c as text) as text =>
                   let m = Table.SelectRows(Master, (r) => r[ValuationArea] = c),
                       f = Table.SelectRows(Fixed,  (r) => r[ValuationArea] = c)
                   in  if not Table.IsEmpty(m)
                          and Text.Trim(Text.From(Table.First(m)[Plant] ?? "")) <> ""
                          then Table.First(m)[Plant]
                       else if not Table.IsEmpty(f) then Table.First(f)[Plant]
                       else c,
    // the three come first, in their own order; everything else after them, by code, so the
    // report reads the way it always has and a new plant is added at the end
    SortOf   = (c as text) as number =>
                   let f = Table.SelectRows(Fixed,  (r) => r[ValuationArea] = c),
                       m = Table.SelectRows(Master, (r) => r[ValuationArea] = c)
                   in  if not Table.IsEmpty(f) then Number.From(Table.First(f)[PlantSortNo])
                       else if not Table.IsEmpty(m)
                            then 100 + (try Number.From(Table.First(m)[PlantSortNo]) otherwise 0)
                       else 900 + (try Number.From(Text.Select(c, {"0".."9"})) otherwise 0),
    // Module or Cell - the two groups the RM sheet's lower block is built on: the cell plant
    // on one side, the module plants on the other. It is read off the plant's own name, so a
    // plant added to Plant Master falls on the right side without anyone editing this.
    GroupOf  = (label as text) as text =>
                   if Text.Contains(Text.Upper(label), "CELL") then "Cell" else "Module",
    Built    = Table.FromRecords(List.Transform(Codes, (c) =>
                   let label = NameOf(c) in
                   [ValuationArea = c, Plant = label, PlantSort = SortOf(c),
                    MWD = MWDOf(c), PlantGroup = GroupOf(label)]),
                   type table [ValuationArea = text, Plant = text, PlantSort = number,
                               MWD = nullable number, PlantGroup = text]),
    // if nothing has loaded yet, the three known plants still make a table, so the report opens
    Rows     = if List.IsEmpty(Codes)
               then Table.AddColumn(
                        Table.AddColumn(
                            Table.RenameColumns(Fixed, {{"PlantSortNo", "PlantSort"}}),
                            "MWD", each null, type number),
                        "PlantGroup",
                        each if Text.Contains(Text.Upper([Plant]), "CELL") then "Cell"
                             else "Module", type text)
               else Built,
    Dedup    = Table.Distinct(Rows, {"ValuationArea"}),
    Typed    = Table.TransformColumnTypes(Dedup, {
                   {"ValuationArea", type text}, {"Plant", type text},
                   {"PlantSort", Int64.Type}, {"MWD", type number},
                   {"PlantGroup", type text}})
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
    Whole   = Table.SelectRows(factTB_Staged,
                  each [Whitelisted] = true and [ValuationArea] <> null),
    // SAP writes subtotal and result lines into the same column as the accounts. They carry
    // the sum of the lines above them, so leaving one in counts that money twice - which is
    // the classic reason a trial balance figure reads high without any single row being wrong.
    NoSums  = Table.SelectRows(Whole, each
                  let G = Text.Upper(Text.Trim(Text.From([GLAccount] ?? ""))),
                      D = Text.Upper(Text.From([GLDesc] ?? "")) in
                  G <> "" and not Text.Contains(G, "*")
                  and not Text.StartsWith(G, "TOTAL") and not Text.StartsWith(G, "RESULT")
                  and not Text.Contains(D, "RESULT")
                  and not Text.StartsWith(D, "TOTAL")),
    // the same line arriving twice is counted once, on the same rule the stock files use: two
    // rows are the same line when the month, the account, the profit centre and the amount all
    // agree. SourceFile is deliberately left out of that test, so one month exported twice into
    // the TB folder under two names cannot double the trial balance.
    Kept    = Table.Distinct(NoSums, {"Month", "GLAccount", "ProfitCentre", "Amount"}),
    // RM / FG / Consumables from whatever the Nature (or GL description) says
    // Raw material is tested BEFORE consumables, and that order matters: an account called
    // "Raw Material & Packing" holds the word PACK, so with consumables tested first the whole
    // of RM was filed under Consumables and the RM row vanished from Inventory (TB) while
    // Consumables read far too high. Packing on its own still lands in Consumables.
    // The Nature column on TB Master is the answer where it is filled - Consumables & Spares,
    // Raw Materials & Packing, Finished Goods - and the account description is read only when
    // that column is empty. Guessing from the description is what put Consumables on the FG
    // row: an account named for what it feeds is not an account named for what it holds.
    Bucket  = (n as any, d as any) as text =>
                  let N = Text.Trim(Text.From(n ?? "")),
                      T = Text.Upper(if N <> "" then N else Text.From(d ?? "")) in
                  // the short codes first, because they are exact: a Nature column holding
                  // RM / FG / CONS says which bucket it is and nothing needs reading into it.
                  // CONS on its own would otherwise fall past the CONSUM test and land in RM.
                  if T = "CONS" or T = "CONSUMABLE" or T = "CONSUMABLES"
                      then "Consumables"
                  else if T = "FG" then "FG"
                  else if T = "RM" then "RM"
                  else if Text.Contains(T, "FINISH") or Text.Contains(T, "FG")
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
               "Amount","PlantCode","ValuationArea","Nature","TBPlant","TBSort","Category",
               "Rule"},
    Padded  = List.Accumulate(List.Difference(Wanted, Table.ColumnNames(Cat)), Cat,
                  (t, c) => Table.AddColumn(t, c, each null)),
    Slim    = Table.SelectColumns(Padded, Wanted),
    Typed   = Table.TransformColumnTypes(Slim, {
                  {"SourceFile", type text}, {"Month", type date},
                  {"GLAccount", type text}, {"GLDesc", type text},
                  {"ProfitCentre", type text}, {"ProfitCentreDesc", type text},
                  {"Amount", type number}, {"PlantCode", type text}, {"Rule", type text},
                  {"ValuationArea", type text}, {"Nature", type text},
                  {"TBPlant", type text}, {"TBSort", Int64.Type},
                  {"Category", type text}}),
    // the same flat plant-and-type key as factInventory, so one row of the Summary table can
    // hold the trial balance, the MB5B figure and the gap between them
    Keyed   = Table.AddColumn(Typed, "PlantType",
                  each Text.From([ValuationArea] ?? "") & "|" & Text.From([Category] ?? ""),
                  type text)
in
    Keyed
```

## dimDate

> One row per month, because every fact is monthly. A daily calendar would repeat each Month value ~30 times and Power BI would refuse to put it on the "one" side of the relationship.

> One row **only for a month that has data**. It is built from the months actually present in the stock files and the trial balance, not from a continuous April-to-March range, so a month you have not added yet cannot appear as an option in any slicer. Add July 2025's MB5B and July'25 appears in the pickers; until then it does not exist in the model at all. Nothing else has to change when a new month arrives.

```
let
    // the months that actually exist in the data: stock files and trial balance. Building the
    // calendar from these, rather than filling in every month between the first and the last,
    // is what keeps months you have not loaded yet out of the slicers.
    // varMonths is where that list is worked out, and it is read there rather than off
    // factInventory and factTB_Staged: referencing the facts here parsed every stock file and
    // the whole trial balance a second time, and three other tables reference this calendar,
    // so that second parse ran four times over. That was most of a long refresh.
    Months = varMonths,
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

## dimRMTechnologyDaily

> One row per month, Module/Cell group and configured component. It carries the latest effective Cost INR/Wp, the matching production constant and the calculated crore-rupees per day. This table powers only the two lower RM matrices.

```
let
    // the month grid comes from the dated sheets, not from dimDate: referencing the calendar
    // here pulled the whole stock folder through this table too
    Months   = varMonthGrid,
    Combos   = Table.Distinct(Table.SelectColumns(varRMTechnologyCosts, {"PlantGroup","Item"})),
    Grid     = Table.AddColumn(Combos, "Month", each Months),
    Expanded = Table.ExpandListColumn(Grid, "Month"),
    AsOfCost = (g as text, i as text, m as date) as nullable number =>
                   let rows = Table.SelectRows(varRMTechnologyCosts, each
                                   [PlantGroup] = g and [Item] = i and [EffectiveFrom] <= m),
                       sorted = Table.Sort(rows, {{"EffectiveFrom", Order.Descending}})
                   in if Table.IsEmpty(sorted) then null else sorted{0}[CostINRWp],
    AsOfConst = (n as text, m as date) as nullable number =>
                   let rows = Table.SelectRows(varRMConstants, each
                                   [ConstantName] = n and [EffectiveFrom] <= m),
                       sorted = Table.Sort(rows, {{"EffectiveFrom", Order.Descending}})
                   in if Table.IsEmpty(sorted) then null else sorted{0}[Value],
    Cost     = Table.AddColumn(Expanded, "CostINRWp", each
                   AsOfCost([PlantGroup], [Item], Date.From([Month])), type number),
    Named    = Table.AddColumn(Cost, "ConstantName", each
                   if Text.Upper([PlantGroup]) = "CELL" then "Cell Production Constant"
                   else "Module Production Constant", type text),
    Constant = Table.AddColumn(Named, "ProductionConstant", each
                   AsOfConst([ConstantName], Date.From([Month])), type number),
    Daily    = Table.AddColumn(Constant, "PerDayCostCr", each
                   if [CostINRWp] = null or [ProductionConstant] = null then null
                   else [CostINRWp] * [ProductionConstant] / 10, type number),
    Out      = Table.TransformColumnTypes(Table.SelectColumns(Daily,
                   {"Month","PlantGroup","Item","CostINRWp","ProductionConstant","PerDayCostCr"}),
                   {{"Month", type date}, {"PlantGroup", type text}, {"Item", type text},
                    {"CostINRWp", type number}, {"ProductionConstant", type number},
                    {"PerDayCostCr", type number}})
in
    Out
```

## dimRMPlantDaily

> One row per month, plant and configured component for 1900 and 1902. Plant costs and variables are independent and effective-dated. 1905 is deliberately absent: its plant Days is copied from Total Cell Days, exactly as the old sheet did.

```
let
    // as in dimRMTechnologyDaily: the grid is the dated sheets' own months, so no stock file
    // is opened to build this table
    Months   = varMonthGrid,
    Combos   = Table.Distinct(Table.SelectColumns(varRMPlantCosts, {"ValuationArea","Item"})),
    Grid     = Table.AddColumn(Combos, "Month", each Months),
    Expanded = Table.ExpandListColumn(Grid, "Month"),
    AsOfCost = (p as text, i as text, m as date) as nullable number =>
                   let rows = Table.SelectRows(varRMPlantCosts, each
                                   [ValuationArea] = p and [Item] = i and [EffectiveFrom] <= m),
                       sorted = Table.Sort(rows, {{"EffectiveFrom", Order.Descending}})
                   in if Table.IsEmpty(sorted) then null else sorted{0}[CostINRWp],
    AsOfConst = (n as text, m as date) as nullable number =>
                   let rows = Table.SelectRows(varRMConstants, each
                                   [ConstantName] = n and [EffectiveFrom] <= m),
                       sorted = Table.Sort(rows, {{"EffectiveFrom", Order.Descending}})
                   in if Table.IsEmpty(sorted) then null else sorted{0}[Value],
    Cost     = Table.AddColumn(Expanded, "CostINRWp", each
                   AsOfCost([ValuationArea], [Item], Date.From([Month])), type number),
    Named    = Table.AddColumn(Cost, "ConstantName", each
                   [ValuationArea] & " Plant Variable", type text),
    Variable = Table.AddColumn(Named, "PlantVariable", each
                   AsOfConst([ConstantName], Date.From([Month])), type number),
    Daily    = Table.AddColumn(Variable, "PerDayCostCr", each
                   if [CostINRWp] = null or [PlantVariable] = null then null
                   else [CostINRWp] * [PlantVariable] / 10, type number),
    Out      = Table.TransformColumnTypes(Table.SelectColumns(Daily,
                   {"Month","ValuationArea","Item","CostINRWp","PlantVariable","PerDayCostCr"}),
                   {{"Month", type date}, {"ValuationArea", type text}, {"Item", type text},
                    {"CostINRWp", type number}, {"PlantVariable", type number},
                    {"PerDayCostCr", type number}})
in
    Out
```

## dimCapacity

```
let
    // the months are the grid the dated sheets are spread over. Reading factInventory here
    // parsed the whole stock folder a second time; reading dimDate did the same thing one step
    // removed, because the calendar was itself built from the facts.
    Months   = varMonthGrid,
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

## dimPlantType

> One row per plant **and** type - `1902 Jaipur Module  —  RM`, `1902 Jaipur Module  —  FG` and so on, nine rows for three plants. It exists so the Summary table can list plant and type without a two-level row hierarchy: a hierarchy has to be expanded, and some versions of Desktop open one collapsed however the file was saved, which hid every row. Built from `dimPlant` and `dimCategory`, so the three plant names come from the one place that decides them and can never disagree with the rest of the report. Leave Enable load ON.

```
let
    Plants = dimPlant,
    Cats   = dimCategory,
    Cross  = Table.AddColumn(Plants, "cat", each Cats),
    Opened = Table.ExpandTableColumn(Cross, "cat", {"Category", "CategorySort"}),
    Keyed  = Table.AddColumn(Opened, "PlantType",
                 each Text.From([ValuationArea] ?? "") & "|" & Text.From([Category] ?? ""),
                 type text),
    // the label the Summary rows show: the plant exactly as the rest of the report names it,
    // then the type
    Label  = Table.AddColumn(Keyed, "Plant and Type",
                 each Text.From([Plant]) & "  —  " & Text.From([Category]), type text),
    Order  = Table.AddColumn(Label, "RowSort",
                 each Int64.From([PlantSort]) * 10 + Int64.From([CategorySort]), Int64.Type),
    Out    = Table.SelectColumns(Order,
                 {"PlantType", "Plant and Type", "Plant", "Category", "RowSort"}),
    Typed  = Table.TransformColumnTypes(Out, {
                 {"PlantType", type text}, {"Plant and Type", type text},
                 {"Plant", type text}, {"Category", type text}, {"RowSort", Int64.Type}})
in
    Typed
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

*megawatts and days*

```
MW = SUM(factInventory[MW Qty])
```

```
FG MW = CALCULATE([MW], factInventory[Category] = "FG")
```

```
Capacity MW = CALCULATE(SUM(dimCapacity[CapacityMW]), dimCapacity[Tech] <> "(All)")
```

```
Plant MWD = SUM(dimPlant[MWD])
```

*RM days from effective-dated cost inputs — used on the RM page only*

```
RM Technology Value ₹ Cr =
VAR Groups = VALUES(dimRMTechnologyDaily[PlantGroup])
VAR Items = VALUES(dimRMTechnologyDaily[Item])
RETURN
    CALCULATE(
        [RM ₹ Cr],
        TREATAS(Groups, dimPlant[PlantGroup]),
        TREATAS(Items, factInventory[Item])
    )
```

```
RM Technology Per Day Cost =
VAR ExpectedRows = COUNTROWS(dimRMTechnologyDaily)
VAR ConfiguredRows =
    COUNTROWS(
        FILTER(
            dimRMTechnologyDaily,
            NOT ISBLANK(dimRMTechnologyDaily[CostINRWp])
                && NOT ISBLANK(dimRMTechnologyDaily[ProductionConstant])
        )
    )
RETURN
    IF(
        ExpectedRows = 0 || ConfiguredRows <> ExpectedRows,
        BLANK(),
        SUM(dimRMTechnologyDaily[PerDayCostCr])
    )
```

```
RM Technology Days =
DIVIDE([RM Technology Value ₹ Cr], [RM Technology Per Day Cost])
```

`RM Technology Days` is a ratio at every level. A component divides its own inventory crore
value by its own per-day cost. Total Module and Total Cell divide their total inventory by the
sum of their component per-day costs. The grand total divides all configured RM inventory by
Module plus Cell per-day cost, which is why the old sheet's March grand total is 16 rather than
13 + 48. A missing input blanks the affected result; an intentional zero is retained, and
`DIVIDE` correctly returns blank for a zero denominator.

```
RM Plant Days =
VAR PlantCode = SELECTEDVALUE(dimPlant[ValuationArea])
VAR IsOnePlant = HASONEVALUE(dimPlant[ValuationArea])
VAR PlantRows =
    CALCULATETABLE(
        dimRMPlantDaily,
        TREATAS({PlantCode}, dimRMPlantDaily[ValuationArea])
    )
VAR ExpectedRows = COUNTROWS(PlantRows)
VAR ConfiguredRows =
    COUNTROWS(
        FILTER(
            PlantRows,
            NOT ISBLANK(dimRMPlantDaily[CostINRWp])
                && NOT ISBLANK(dimRMPlantDaily[PlantVariable])
        )
    )
VAR ConfiguredItems =
    SELECTCOLUMNS(PlantRows, "ConfiguredItem", dimRMPlantDaily[Item])
VAR ModulePlantValue =
    CALCULATE(
        [RM ₹ Cr],
        REMOVEFILTERS(factInventory[Item]),
        TREATAS(ConfiguredItems, factInventory[Item])
    )
VAR ModulePlantPerDayCost = SUMX(PlantRows, dimRMPlantDaily[PerDayCostCr])
VAR ModulePlantDays =
    IF(
        ExpectedRows = 0 || ConfiguredRows <> ExpectedRows,
        BLANK(),
        DIVIDE(ModulePlantValue, ModulePlantPerDayCost)
    )
VAR CellPlantDays =
    CALCULATE(
        [RM Technology Days],
        REMOVEFILTERS(dimRMTechnologyDaily[PlantGroup]),
        REMOVEFILTERS(dimRMTechnologyDaily[Item]),
        TREATAS({"Cell"}, dimRMTechnologyDaily[PlantGroup])
    )
VAR AllPlantsDays =
    CALCULATE(
        [RM Technology Days],
        REMOVEFILTERS(dimPlant),
        REMOVEFILTERS(dimRMTechnologyDaily[PlantGroup]),
        REMOVEFILTERS(dimRMTechnologyDaily[Item])
    )
RETURN
    IF(
        NOT IsOnePlant,
        AllPlantsDays,
        IF(PlantCode = "1905", CellPlantDays, ModulePlantDays)
    )
```

For 1900 and 1902 this is the old sheet's own arithmetic: add the configured items' inventory
crore values, add their per-day costs, and divide the one by the other. 1900 has six configured
items and a plant variable of 5; 1902 has seven and a variable of 8. Adding the individual item
Days instead would give every component equal weight regardless of its rupees per day, which is
why March 1900 reads about 15 rather than a far larger figure. 1905 returns Total Cell Days
exactly, and the Total row returns the same calculated result as the technology Grand Total
Days rather than the sum of the three plant rows.

```
RM Plant Days by Period =
AVERAGEX(VALUES(dimDate[Month]), [RM Plant Days])
```

```
RM Technology Days by Period =
AVERAGEX(VALUES(dimDate[Month]), [RM Technology Days])
```

*days of cover for a plant row*

```
Plant Days = DIVIDE([MW], CALCULATE(SUM(dimPlant[MWD]), REMOVEFILTERS(dimNature)))
```

`Plant Days` is the only measure the two **In Days by plant** tables use, and it divides by the
`MWD` column of **Plant Master** — nothing else. There is deliberately no fallback to the
`MW Capacity` sheet: that sheet is for technologies, and a plant row that borrowed from it read
as a figure when it was the wrong denominator. A blank cell here means `MWD` is empty for that
plant on the sheet, which is a thing you can see and fix; the technology tables and every card
keep using `Days of Inventory` exactly as before.

```
Capacity MW (plant) =
VAR Whole =
    CALCULATE(SUM(dimCapacity[CapacityMW]),
        REMOVEFILTERS(dimNature),
        dimCapacity[Tech] = "(All)")
VAR ByTech =
    CALCULATE(SUM(dimCapacity[CapacityMW]),
        REMOVEFILTERS(dimNature),
        dimCapacity[Tech] <> "(All)")
RETURN
    IF(Whole <> 0 && NOT ISBLANK(Whole), Whole, ByTech)
```

`MWD` comes first because that is the figure you type per plant on **Plant Master**, and it is
what days of cover on a plant row divides by: `days = inventory MW / MWD`. The `MW Capacity`
sheet is left to the technology rows, which have their own denominator, and its `Total` rows
are only used for a plant that has no `MWD` typed against it.

The second one exists for a real problem: capacity is keyed by technology, and an RM nature
(`Glass`, `Wafer`) is not a technology, so plain `Capacity MW` goes blank the moment an RM
row filters it. Removing the nature filter falls back to the plant's capacity, which is the
right denominator for RM.

And a plant's capacity can be given two ways, which is what `(All)` is doing in both of them.
A `Total` row on the MW sheet is the plant's whole capacity, typed directly - the figures on
your `March'26 | MW(S)` block, 8.28 against 1902 and so on. Where you have typed one, it *is*
the plant's denominator; where you have not, the technology rows are added up instead. So a
plant with no technologies on that sheet - 1905 - still gets days of cover the moment its
total is typed, and a plant with both does not count its capacity twice. `Capacity MW` leaves
those total rows out entirely, because a technology's own denominator is its own row.

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

The megawatt twin of it. Both of these name finished goods inside the measure instead of
leaning on a filter on the visual, which is why the FG technology chart can no longer come
up empty: an RM nature returns a blank against them and drops off the axis by itself.

```
Latest Month FG MW =
VAR LastIdx = CALCULATE(MAX(dimDate[MonthIndex]), ALLSELECTED(dimDate))
RETURN CALCULATE([FG MW], FILTER(ALL(dimDate), dimDate[MonthIndex] = LastIdx))
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
VAR LastM =
    MAXX(FILTER(VALUES(dimDate[MonthIndex]), CALCULATE(COUNTROWS(factInventory)) > 0),
         dimDate[MonthIndex])
RETURN CALCULATE([Value ₹ Cr], dimDate[MonthIndex] = LastM)

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
VAR LastM =
    MAXX(FILTER(VALUES(dimDate[MonthIndex]), CALCULATE(COUNTROWS(factInventory)) > 0),
         dimDate[MonthIndex])
RETURN CALCULATE([RM Days All Plants], dimDate[MonthIndex] = LastM)

Inventory MW =
VAR LastM =
    MAXX(FILTER(VALUES(dimDate[MonthIndex]), CALCULATE(COUNTROWS(factInventory)) > 0),
         dimDate[MonthIndex])
RETURN CALCULATE([MW], dimDate[MonthIndex] = LastM)

In Last 12 =
VAR LastM = [Latest Month Index]
VAR ThisM = MAX(dimDate[MonthIndex])
RETURN IF(ThisM > LastM - 12 && ThisM <= LastM, 1, 0)

Summary Value Rs Cr =
VAR LastM =
    MAXX(FILTER(VALUES(dimDate[MonthIndex]), CALCULATE(COUNTROWS(factInventory)) > 0),
         dimDate[MonthIndex])
RETURN CALCULATE([Summary Value ₹ Cr], dimDate[MonthIndex] = LastM)

TB Inventory Rs Cr =
VAR LastM =
    MAXX(FILTER(VALUES(dimDate[MonthIndex]), CALCULATE(COUNTROWS(factTB)) > 0),
         dimDate[MonthIndex])
RETURN CALCULATE([TB ₹ Cr], dimDate[MonthIndex] = LastM)

Difference Inventory Rs Cr = [TB Inventory Rs Cr] - [Inventory Rs Cr]

Difference Inventory % =
VAR Books = [TB Inventory Rs Cr]
RETURN IF(ABS(Books) < 0.05, BLANK(), DIVIDE([Difference Inventory Rs Cr], Books))

Unit Value by Period =
VAR LastM =
    MAXX(FILTER(VALUES(dimDate[MonthIndex]), CALCULATE(COUNTROWS(factInventory)) > 0),
         dimDate[MonthIndex])
RETURN CALCULATE([Unit Value], dimDate[MonthIndex] = LastM)

In Latest Month =
IF(MAX(dimDate[MonthIndex]) = [Latest Month Index], 1, 0)

Days by Period =
VAR LastM =
    MAXX(FILTER(VALUES(dimDate[MonthIndex]), CALCULATE(COUNTROWS(factInventory)) > 0),
         dimDate[MonthIndex])
RETURN CALCULATE([Days], dimDate[MonthIndex] = LastM)
```

`Summary Value Rs Cr` is the Summary page's only figure. It is `Summary Value ₹ Cr` with the
closing rule added, and it no longer asks what grain it is being read at: it always returns the level at
the **last month that has data in the current filter**. In a month column that is that month; on a collapsed
heading, a quarter or a four-month window it is the newest of those months. There is no path through it that
can add two month-ends together, whatever the visual reports about its own scope.

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
but at a quarter or total grain it would add three month-ends together; the by-Period version returns the
closing month's figure instead.

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
1,433 report came from. Both return the closing month's level: the month itself in a month column, the
newest month in view at any wider grain.

`Days by Period` is `Days` with the quarter rule, and the RM page's days chart uses it. Days is
a ratio of two stock figures, so at a quarter grain it has to be the closing month's ratio; adding three of
them would give a nonsense number three times too big.

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

**No forced type casts on the master sheets.** *Errors in the trial-balance whitelist* on all eight rows was a
`Int64.Type` cast on the sort column: a blank, a dash, `1.5` or a number stored as text errors the
whole row, and what is lost is the whitelist of inventory GL accounts - so Inventory (TB) reads
empty. Every master column in `dimMaterialAttr`, `varConstants` and the trial
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
`1902 Jaipur Module` - so the slicer, the legends and the ticker cards all read the same.

**`dimNature` carries `Consumables` and `Unassigned`.** Both are written by the fact queries
rather than read from a master sheet, so the bridge table did not have them and a fifth of the
Detail donut came out as `(Blank)`.

**The megawatt figures sit above their bars.** Inside the bar a dark figure on dark green cannot
be read, which is what the Overview MW strip looked like. The `% vs last month` line has been
taken off that chart - it was never asked for and it was the second thing crowding it.

**Detail is level-aware.** Its cards, its three pies and its matrix read `Inventory Rs Cr` and
`Inventory MW`, so opening the page with four months in context shows the closing month's level instead
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

### Changed in build 27

**No measure asks about scope any more.** Seven measures used to read
`IF(ISINSCOPE(dimDate[MonthName]), <the figure>, <the closing month>)`, which trusts the visual to say
whether a month is on show. A matrix whose column hierarchy is sitting collapsed does not always say so,
and the figure then came back as `<the figure>` over every month in the window — which is a sum of
month-ends, the one thing inventory must never be. `Inventory Rs Cr`, `Inventory MW`, `TB Inventory Rs Cr`,
`Summary Value Rs Cr`, `Days by Period`, `Unit Value by Period` and `RM Days All Plants by Period` now
compute the last month that has data in the current filter and return that month's level unconditionally:

each of them now takes `LastM` as the largest `dimDate[MonthIndex]` in the current filter that has rows in
the fact table, and returns `CALCULATE(<the base figure>, dimDate[MonthIndex] = LastM)`. The full text of
each is in Appendix B.

In a month column `LastM` is that month, so the month's own figure is unchanged. On a collapsed heading,
a quarter, a Total row or a four-month window it is the newest of those months. There is no branch left
that can add two month-ends together. The `MonthIndex` filter is also clamped to months that actually
carry rows, so a calendar running ahead of the data cannot blank the figure.

**Summary is one matrix with the metrics as its master columns.** Columns holds `dimMetric[Metric]` first
and `dimDate[MonthName]` second, so the three master columns are Inventory (TB), Inventory (MB5B) and
Difference, and the months sit underneath each of them — the newest March plus the last three by default,
and whatever the slicer says when it is used. Both column levels are written into the file open, and the
expand/collapse buttons are switched on for the column headers so the second level can be opened by hand
if a version of Desktop opens it collapsed.
