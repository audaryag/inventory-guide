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

### How to add each query (you will repeat this 28 times)

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
| "Expression.Syntax Error" right after pasting | the whole appendix went into one query | one query per Blank Query, 28 times |

Send me the exact error text and I'll tell you the one-line fix.

---

# PART 2 — Build the model (10 min)

**2.1** Left sidebar: click the **Model** icon (third one down, looks like a table diagram).

**2.2** Power BI will have guessed some relationships. **Delete all of them**: click each
connecting line and press Delete. Cleaner to start blank.

**2.3** Create these 8 relationships. To create one: click and drag the **from** field onto
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

Every one is **Single** direction. If Power BI offers "Both", don't take it — bidirectional
relationships cause wrong totals in ways that are very hard to spot later.

**2.4** Skip "Mark as date table" — it needs one row per *day*, and `dimDate` is monthly on
purpose. None of the measures need it; `Prev Month` uses `MonthIndex` instead.

**2.5** Fix month sorting: click the `MonthName` column in `dimDate` → ribbon
**Column tools** → **Sort by column** → pick `MonthSort`. Without this, months sort
alphabetically (Apr, Aug, Dec…) and every chart reads as nonsense.

**2.6** Do the same for `dimPlant`: click `Plant` → **Sort by column** → `PlantSort`.

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

**3.6** Format the money ones. Click each of `Closing Value`, `Opening Value`,
`Receipts Value`, `Issues Value`, `TB Value`, `Difference` → ribbon **Measure tools** →
**Format: Currency**, **Decimal places: 0**.
For `Difference %`, set **Format: Percentage**, 1 decimal.
For `Days`, `MW`, `Capacity MW`, set **Decimal places: 1**.

---

# PART 4 — Build the pages

Every visual below is spelled out the same way: what to insert, exactly which field goes in
which well, and the four numbers that place it. Nothing is left to taste.

**How to place a visual precisely** (do this for every one): select it, open the **Format**
pane (paintbrush icon) → **General** → **Properties** → **Size and style**, and type the
four numbers. X and Y are the top-left corner, in pixels, on a 1280 × 720 canvas.

**4.0 — Set the canvas and the theme first.** Doing this after building means re-doing it.

1. Click empty canvas → **Format** pane → **Canvas settings** → **Type: 16:9**,
   Height 720, Width 1280.
2. Download the theme: [inventory-theme.json](inventory-theme.json)
   (right-click → Save link as, into your `Inventory Report` folder).
3. Ribbon **View** → **Themes** dropdown → **Browse for themes** → pick that file.

Colours, fonts, card styling, matrix gridlines and rounded borders all come from the theme,
so no visual below needs manual colouring — only the conditional formatting in 4.10, which
is data-driven and can't live in a theme.

**Make the five pages now**, so you can copy the header band into them: click the **+** at
the bottom five times, then double-click each tab and name them
`Overview` · `Summary` · `FG` · `RM` · `Data Quality`.

---

## The header band — build once on Overview, then copy to all five

**4.1** Insert five **Card** visuals. For each: **Insert** → **Card**, drop the measure into
the **Fields** well, then set the position.

| Card | Measure in Fields | X | Y | Width | Height |
|---|---|---|---|---|---|
| 1 | `Inventory Total` | 16 | 12 | 240 | 88 |
| 2 | `Inv RM` | 264 | 12 | 240 | 88 |
| 3 | `Inv FG` | 512 | 12 | 240 | 88 |
| 4 | `Inv Consumables` | 760 | 12 | 240 | 88 |
| 5 | `Difference` | 1008 | 12 | 240 | 88 |

**4.2** Insert two **Slicer** visuals. For each: **Insert** → **Slicer**, drag the field in,
then **Format** → **Slicer settings** → **Style: Dropdown**.

| Slicer | Field | X | Y | Width | Height |
|---|---|---|---|---|---|
| Month | `dimDate[MonthName]` | 16 | 108 | 300 | 44 |
| Plant | `dimPlant[Plant]` | 324 | 108 | 300 | 44 |

**4.3** Select all seven (click the first, Ctrl+click the rest) → **Ctrl+C** → go to each of
the other four pages → **Ctrl+V**. Positions come with them, so the band lands identically.

**4.4** Ribbon **View** → tick **Sync slicers**. In the pane that opens, click the Month
slicer and tick **Sync** and **Visible** for all five pages; repeat for the Plant slicer.
Without this, each page filters independently and two pages will disagree.

> Everything below sits between Y=168 and Y=712, which is the space under the band.

---

## Page 1 — Overview

**4.5** **Stacked column chart** — inventory mix by month.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `Closing Value` |
| Legend | `factInventory[Category]` |

Position: X 16, Y 168, W 764, H 272. Title: `Inventory by month and category`.

**4.6** **Clustered column chart** — where the stock sits.

| Well | Field |
|---|---|
| X-axis | `dimPlant[Plant]` |
| Y-axis | `Closing Value` |
| Legend | `factInventory[Category]` |

Position: X 788, Y 168, W 476, H 272. Title: `Inventory by plant`.

**4.7** **Line chart** — this month against last.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `Closing Value`, then `Prev Month` |

Position: X 16, Y 452, W 1248, H 260. Title: `Closing value vs previous month`.

---

## Page 2 — Summary (TB vs MB5B)

**4.8** **Matrix** — the reconciliation itself.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]` |
| Values | `TB Value`, `Closing Value`, `Difference`, `Difference %` |

Position: X 16, Y 168, W 764, H 300. Title: `Trial balance vs MB5B`.

**4.9** **Waterfall chart** — which plant causes the gap.

| Well | Field |
|---|---|
| Category | `dimPlant[Plant]` |
| Y-axis | `Difference` |

Position: X 788, Y 168, W 476, H 300. Title: `Difference by plant`.

**4.10** Conditional formatting on the matrix (the one thing the theme can't do): click the
matrix → in the **Values** well click the dropdown on `Difference` →
**Conditional formatting** → **Background color** → **Format style: Diverging** →
Minimum red, Centre white with **Centre = 0**, Maximum red. Both directions red because a
difference either way is equally wrong.

**4.11** **Line chart** — is the gap closing or widening?

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `Difference` |

Position: X 16, Y 480, W 1248, H 232. Title: `Difference trend`.

---

## Page 3 — FG

**4.12** **Matrix** — FG down to material, with MW and Days.

| Well | Field |
|---|---|
| Rows | `dimNature[Nature]`, then `factInventory[Material]` below it |
| Values | `Closing Value`, `FG MW`, `Capacity MW`, `Days`, `INR per Wp` |
| Filters pane | `factInventory[Category]` → **is FG** |

Position: X 16, Y 168, W 1248, H 288. Title: `FG by tech and material`.
Turn **Format** → **Row headers** → **Stepped layout: Off** so Nature and Material sit in
their own columns.

**4.13** **Area chart** — FG history by tech.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `Closing Value` |
| Legend | `dimNature[Nature]` |
| Filters pane | `factInventory[Category]` → **is FG** |

Position: X 16, Y 468, W 828, H 244. Title: `FG value by tech over time`.

**4.14** **Line chart** — days of inventory, the number your superior will ask for.

| Well | Field |
|---|---|
| X-axis | `dimDate[MonthName]` |
| Y-axis | `Days` |
| Filters pane | `factInventory[Category]` → **is FG** |

Position: X 852, Y 468, W 412, H 244. Title: `FG inventory days`.

---

## Page 4 — RM

**4.15** **Matrix** — RM by plant and nature.

| Well | Field |
|---|---|
| Rows | `dimPlant[Plant]`, `dimNature[Nature]`, `factInventory[GroupNature]` |
| Values | `Closing Value`, `MW` |
| Filters pane | `factInventory[Category]` → **is RM** |

Position: X 16, Y 168, W 620, H 544. Title: `RM by plant and nature`.

**4.16** **Decomposition tree** — replaces most of what the RM sheet does by hand, and
drills in whatever order you click.

| Well | Field |
|---|---|
| Analyze | `Closing Value` |
| Explain by | `dimPlant[Plant]`, `dimNature[Nature]`, `factInventory[GroupNature]` |
| Filters pane | `factInventory[Category]` → **is RM** |

Position: X 644, Y 168, W 620, H 544. Title: `RM breakdown`.

---

## Page 5 — Data Quality

Not decoration. This page is how you find out something is wrong before your superior does.
Glance at it after every refresh: the two cards should read 0, the two tables should be empty.

**4.17** **Card**: `Rows Missing Attr` — materials with no row in the master sheets.
X 16, Y 168, W 300, H 100. Title: `Rows missing master attributes (want 0)`.

**4.18** **Card**: `Stock Recon` — Opening + Receipts − Issues − Closing.
X 324, Y 168, W 300, H 100. Title: `Stock reconciliation (must be 0)`.

Anything other than 0 means a file is duplicated, truncated, or hand-edited.

**4.19** **Table**: `factTB_Unmapped` → `GLAccount`, `GLDesc`, `Amount`.
X 632, Y 168, W 632, H 100. Title: `GLs in TB but not in TB Master (want empty)`.

**4.20** **Table**: `qcNatureNoCapacity` → `Nature`.
X 16, Y 276, W 608, H 210. Title: `FG Natures with no capacity row (want empty)`.

Anything here silently gets blank Days — this is the check that catches a Nature/Tech typo.

**4.21** **Table**: `qcHeaders` → `Folder`, `Name`, `SheetNames`, `Headers`.
X 632, Y 276, W 632, H 210. Title: `Actual headers of every source file`.

**4.22** **Table**: `qcVarHeaders` → `SheetName`, `Headers`, `DataRows`.
X 16, Y 494, W 608, H 218. Title: `Variables workbook sheets`. `DataRows = 0` = empty sheet.

**4.23** **Table**: `factInventory` → `SourceFile`, `Month`, `Category`, `Closing Value`.
X 632, Y 494, W 632, H 218. Title: `Files loaded this refresh`.

Read this one after each monthly refresh to confirm every file actually came in — a missing
month looks like a real fall in inventory, not like an error.

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

> The inner join to dimTBMaster IS the trial-balance cleaning - only whitelisted GL accounts survive.

```
let
    Mapped  = Table.NestedJoin(factTB_Staged, {"GLAccount"}, dimTBMaster, {"GLAccount"},
                  "tpl", JoinKind.Inner),
    Expand  = Table.ExpandTableColumn(Mapped, "tpl", {"Nature","TBPlant","TBSort"})
in
    Expand
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

---

# Appendix B — measures

Add these one at a time (**Home → New measure**), with `factInventory` selected.

```
Closing Value   = SUM(factInventory[CloseVal])
```

```
Inventory Total = [Closing Value]
```

```
Closing Qty     = SUM(factInventory[CloseQty])
```

```
Opening Value   = SUM(factInventory[OpenVal])
```

```
Receipts Value  = SUM(factInventory[ReceiptVal])
```

```
Issues Value    = SUM(factInventory[IssueVal])
```

```
MW              = SUM(factInventory[MW])
```

```
INR per Wp      = SUM(factInventory[INR_WP])
```

```
Inv RM          = CALCULATE([Closing Value], factInventory[Category] = "RM")
```

```
Inv FG          = CALCULATE([Closing Value], factInventory[Category] = "FG")
```

```
Inv Consumables = CALCULATE([Closing Value], factInventory[Category] = "Consumables")
```

```
Capacity MW     = SUM(dimCapacity[CapacityMW])
```

*Days applies to FG only: capacity is module capacity, so RM and consumables*

*have no meaningful denominator. Scoping it here stops a plausible-looking but*

*meaningless number appearing if someone drops Days onto the RM page.*

```
FG MW           = CALCULATE([MW], factInventory[Category] = "FG")
```

```
Days            = DIVIDE([FG MW], [Capacity MW])
```

```
TB Value        = SUM(factTB[Amount])
```

```
Difference      = [TB Value] - [Closing Value]
```

```
Difference %    = DIVIDE([Difference], [TB Value])
```

```
Prev Month      =
VAR PrevIdx = MAX(dimDate[MonthIndex]) - 1
RETURN CALCULATE([Closing Value], ALL(dimDate), dimDate[MonthIndex] = PrevIdx)
```

```
MoM Delta       = [Closing Value] - [Prev Month]
```

*data quality*

```
Stock Recon     = [Opening Value] + [Receipts Value] - [Issues Value] - [Closing Value]
```

```
Rows Missing Attr = CALCULATE(COUNTROWS(factInventory), factInventory[AttrMissing] = TRUE())
```

```
Unmapped TB     = SUM(factTB_Unmapped[Amount])
```
