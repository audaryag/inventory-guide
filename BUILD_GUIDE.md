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

### How to add each query (you will repeat this 27 times)

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
qcHeaders, qcVarHeaders, qcNatureNoCapacity
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
| "Expression.Syntax Error" right after pasting | the whole appendix went into one query | one query per Blank Query, 27 times |

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

**2.4** Mark the date table: click `dimDate` in the Fields list → ribbon **Table tools** →
**Mark as date table** → choose the `Date` column.

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

Five pages. Add a page with the **+** at the bottom of the window; rename by
double-clicking the tab.

## The header band (do this once, then copy to every page)

**4.1** On page 1, add five **Card** visuals across the top. To add one: **Insert** →
**Card** (or click Card in the Visualizations pane), then drag it into place.
Drop one measure into each card's **Fields** well:
`Inventory Total` · `Inv RM` · `Inv FG` · `Inv Consumables` · `Difference`

**4.2** Add two slicers below them: **Insert** → **Slicer**.
- Slicer 1: drag `dimDate[MonthName]` into it. In **Format** → **Slicer settings** →
  **Style: Dropdown**.
- Slicer 2: drag `dimPlant[Plant]` into it. Same dropdown style.

**4.3** Select all seven visuals (click one, Ctrl+click the rest) → **Ctrl+C**.
On each other page, **Ctrl+V**. Now the band is identical everywhere.

**4.4** Sync the slicers so picking a month on one page applies everywhere:
ribbon **View** → tick **Sync slicers**. A pane opens on the right. Click the Month
slicer, then tick both **Sync** and **Visible** for all five pages. Repeat for the
Plant slicer.

## Page 1 — Overview

**4.5** **Stacked column chart**:
- X-axis: `dimDate[MonthName]`
- Y-axis: `Closing Value`
- Legend: `factInventory[Category]`

**4.6** **Line chart**:
- X-axis: `dimDate[MonthName]`
- Y-axis: `Closing Value` and `Prev Month` (drag both in)

**4.7** **Clustered column chart**:
- X-axis: `dimPlant[Plant]`
- Y-axis: `Closing Value`
- Legend: `factInventory[Category]`

## Page 2 — Summary (TB vs MB5B)

**4.8** **Matrix**:
- Rows: `dimPlant[Plant]`
- Values: `TB Value`, `Closing Value`, `Difference`, `Difference %`

**4.9** Colour the Difference column: click the matrix, in the **Values** well click the
dropdown on `Difference` → **Conditional formatting** → **Background color** →
choose diverging, centred on 0. Now a bad reconciliation is visible at a glance instead of
something you have to read.

**4.10** **Waterfall chart**:
- Category: `dimPlant[Plant]`
- Y-axis: `Difference`

## Page 3 — FG

**4.11** **Matrix**:
- Rows: `dimNature[Nature]`, then `factInventory[Material]` underneath it
- Values: `Closing Value`, `FG MW`, `Capacity MW`, `Days`, `INR per Wp`
- **Filters** pane: drag `factInventory[Category]` → set to **is FG**

**4.12** **Area chart**:
- X-axis: `dimDate[MonthName]`
- Y-axis: `Closing Value`
- Legend: `dimNature[Nature]`
- Same Category = FG filter

## Page 4 — RM

**4.13** **Matrix**:
- Rows: `dimPlant[Plant]`, `dimNature[Nature]`, `factInventory[GroupNature]`
- Values: `Closing Value`, `MW`
- Filter: `factInventory[Category]` is **RM**

**4.14** **Decomposition tree**:
- Analyze: `Closing Value`
- Explain by: `dimPlant[Plant]`, `dimNature[Nature]`, `factInventory[GroupNature]`
- Same RM filter

This one visual replaces most of what your RM sheet does by hand, and it drills in any
order you click.

## Page 5 — Data Quality

Not decoration. This page is how you find out something's wrong before your superior does.

**4.15** **Card**: `Rows Missing Attr` — materials with no row in the master sheets.

**4.16** **Card**: `Stock Recon` — should always read **0**. Anything else means a bad or
duplicated file.

**4.17** **Table**: `factTB_Unmapped` → fields `GLAccount`, `GLDesc`, `Amount`, `Rows` —
GL accounts in the raw TB that `TB Master` doesn't list. Empty is good.

**4.18** **Table**: `qcNatureNoCapacity` → field `Nature` — FG Natures with no matching Tech
on `MW Capacity`. Empty is good; anything listed here has blank Days.

**4.19** **Table**: `qcHeaders` → fields `Folder`, `Name`, `SheetNames`, `Headers` — the real
headers of every source file. This is what you read when a column comes through blank.

**4.20** **Table**: `qcVarHeaders` → fields `SheetName`, `Headers`, `DataRows` — same for the
Variables workbook. `DataRows = 0` means a sheet is empty.

**4.21** **Table**: `factInventory` → `SourceFile`, `Month`, `Category`, with
`Closing Value`. Scan it after each refresh to confirm every month's file actually loaded.

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

> This version reads the ORIGINAL two-block MW sheet and unpivots the three plant columns. Expect 18 rows (6 Techs x 3 plants), MW = 0 for every 1905.

```
let
    Wb      = Excel.Workbook(File.Contents(pVarsFile), null, true),
    Sh      = Table.SelectRows(Wb, each [Kind] = "Sheet"),
    Norm    = (n as any) as text => Text.Upper(Text.Remove(Text.Trim(Text.From(n ?? "")), {" ","."})),
    Hit     = Table.SelectRows(Sh, each List.Contains({"MW","MWCAPACITY","CAPACITY"}, Norm([Item]))),
    Data    = Hit{0}[Data],
    C       = Table.ColumnNames(Data),
    // keep only rows whose first cell is text: that is the Tech block, not the Plant block
    TechRow = Table.SelectRows(Data, each
                  [Column1] <> null and [Column1] <> "" and Value.Is([Column1], type text)
                  and not Text.StartsWith(Text.From([Column1]), "Plant", Comparer.OrdinalIgnoreCase)),
    Pick    = Table.SelectColumns(TechRow, {C{0}, C{2}, C{3}, C{4}}),
    Named   = Table.RenameColumns(Pick, {
                  {C{0}, "Tech"}, {C{2}, "1900"}, {C{3}, "1902"}, {C{4}, "1905"}}),
    Unpiv   = Table.UnpivotOtherColumns(Named, {"Tech"}, "ValuationArea", "MWRaw"),
    MWNum   = Table.AddColumn(Unpiv, "MW", each try Number.From([MWRaw]) otherwise 0, type number),
    Dated   = Table.AddColumn(MWNum, "EffectiveFrom", each #date(1900,1,1), type date),
    Keys    = Table.TransformColumns(Dated, {
                  {"Tech",          each Text.Trim(Text.From(_ ?? "")), type text},
                  {"ValuationArea", each Text.Trim(Text.From(_ ?? "")), type text}}),
    Out     = Table.Buffer(Table.SelectColumns(Keys,
                  {"EffectiveFrom","Tech","ValuationArea","MW"}))
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

```
let
    Files    = Folder.Files(pRoot & "\TB"),
    OnlyXlsx = Table.SelectRows(Files, each Text.Lower([Extension]) = ".xlsx"
                   and not Text.StartsWith([Name], "~$")
                   and not Text.StartsWith([Name], ".")),
    Loaded   = Table.AddColumn(OnlyXlsx, "Data", each
                   let
                       Wb = Excel.Workbook([Content], true, true),
                       Sh = Wb{[Item="Sheet1", Kind="Sheet"]}[Data],
                       Pr = Table.PromoteHeaders(Sh, [PromoteAllScalars=true])
                   in
                       Table.SelectColumns(Pr, {
                           "GL Account Number","GL Account Description",
                           "Profit Centre","Profit Centre Description","Amount"},
                           MissingField.Error)),
    // month from the file name: TB_YYYYMM.xlsx
    WithMonth = Table.AddColumn(Loaded, "Month", each
                   let
                       digits = Text.Select([Name], {"0".."9"}),
                       yyyymm = Text.Middle(digits, 0, 6)
                   in
                       try #date(Number.From(Text.Start(yyyymm,4)),
                                 Number.From(Text.Middle(yyyymm,4,2)), 1)
                       otherwise null, type date),
    Slim     = Table.SelectColumns(WithMonth, {"Name","Month","Data"}),
    Expanded = Table.ExpandTableColumn(Slim, "Data",
                   {"GL Account Number","GL Account Description",
                    "Profit Centre","Profit Centre Description","Amount"}),
    Renamed  = Table.RenameColumns(Expanded, {
                   {"Name","SourceFile"},
                   {"GL Account Number","GLAccount"},
                   {"GL Account Description","GLDesc"},
                   {"Profit Centre","ProfitCentre"},
                   {"Profit Centre Description","ProfitCentreDesc"}}),
    Keys     = Table.TransformColumns(Renamed, {
                   {"GLAccount",    each Text.TrimStart(Text.Trim(Text.From(_)), "0"), type text},
                   {"ProfitCentre", each Text.Trim(Text.From(_)), type text}}),
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

```
let
    MinD  = List.Min(factInventory[FromDate]),
    MaxD  = List.Max(factInventory[ToDate]),
    Start = #date(Date.Year(MinD) - (if Date.Month(MinD) < 4 then 1 else 0), 4, 1),
    End   = #date(Date.Year(MaxD) + (if Date.Month(MaxD) >= 4 then 1 else 0), 3, 31),
    Days  = List.Dates(Start, Duration.Days(End - Start) + 1, #duration(1,0,0,0)),
    T     = Table.TransformColumnTypes(
                Table.FromList(Days, Splitter.SplitByNothing(), {"Date"}),
                {{"Date", type date}}),
    M     = Table.AddColumn(T, "Month", each Date.StartOfMonth([Date]), type date),
    MN    = Table.AddColumn(M, "MonthName", each Date.ToText([Date], "MMM''yy"), type text),
    MS    = Table.AddColumn(MN, "MonthSort",
                each Date.Year([Date]) * 100 + Date.Month([Date]), Int64.Type),
    FY    = Table.AddColumn(MS, "FY", each
                let y = if Date.Month([Date]) >= 4 then Date.Year([Date]) else Date.Year([Date]) - 1
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
Prev Month      = CALCULATE([Closing Value], DATEADD(dimDate[Date], -1, MONTH))
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
