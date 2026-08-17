"""Fixes for a report that is already built, newest first.

Each entry names one query and hands over its **whole** code, taken live out of
BUILD_GUIDE.md so the two can never drift apart: click the query, Advanced Editor,
Ctrl+A, paste, Done. No hunting for a line inside a query and no partial edits.
Everything here is already in the generated download, so a fresh copy needs none of it.
"""

import html

# query name -> why it changed. Order is the order to paste them in.
EDITS = [
    dict(n="000000000000000000", build="41", query="factInventory",
         title="One stock line per material per plant, so a split line cannot multiply a material\u2019s stock",
         why="An export holds one line per material per plant per month. A second line for the "
             "same four is the same balance arriving twice \u2014 a storage-location or "
             "special-stock split, or a month re-exported \u2014 and adding them multiplied "
             "the material\u2019s stock, which is what put Dholera Cell\u2019s FG in MW "
             "several times over while the 580 from Constants was being applied correctly. The "
             "line kept is the one with the largest closing quantity; the rest are listed on "
             "Checks Stock with what they held. Build 40\u2019s wider plant list is reverted: "
             "the trial balance names plants outside 1900, 1902 and 1905 and those are not part "
             "of this report.",
         steps=[
             "Repaste <code>factInventory</code>, <code>varPlantCodes</code> and "
             "<code>dimPlant</code> from the <strong>Queries</strong> tab, add "
             "<code>qcStockDupes</code> as a new Blank Query, then refresh.",
             "Checks Stock \u2192 <em>Materials an export gave more than one line for</em>: "
             "empty means no material was ever split. Rows there show what was set aside.",
             "FG page: Dholera Cell in MW should now agree with the export\u2019s own "
             "closing stock times 580 \u00f7 1,000,000.",
         ],
         find="", repl=""),
    dict(n="00000000000000000", build="40", query="factTB_Staged",
         title="The trial balance behaves like the VLOOKUP that produced the old figures, and every plant is reported",
         why="<code>TB Master</code> carries the same GL account and profit centre on more than "
             "one row with different Plants, for many pairs \u2014 so nothing on the sheet tells "
             "those rows apart. Holding them back emptied a plant\u2019s RM; breaking the tie by "
             "profit centre moved figures without fixing them. The old Excel used VLOOKUP, which "
             "takes the first matching row, and its figures are the ones being compared against "
             "\u2014 so the report now takes the first row too, in the sheet\u2019s own order. "
             "Separately, plant codes outside 1900, 1902 and 1905 are no longer discarded: the "
             "plant list is every code Plant Master names, every code TB Master\u2019s Plant "
             "column names, and every code the exports contain.",
         steps=[
             "Repaste <code>factTB_Staged</code>, <code>varPlantCodes</code>, "
             "<code>factInventory</code> and <code>dimPlant</code> from the "
             "<strong>Queries</strong> tab, then refresh.",
             "Checks TB \u2192 <em>Where every rupee went</em>: no row should say "
             "<em>dropped: two plants on TB Master</em> any more.",
             "A line placed by row order says <em>sheet gave two plants, first row used</em>. "
             "To stop depending on row order, correct those pairs on <code>TB Master</code> "
             "\u2014 they are listed with both plants on the unmatched table.",
         ],
         find="", repl=""),
    dict(n="0000000000000000", build="39", query="qcStockCheck",
         title="Three diagnostic pages, so a wrong figure shows its own ingredients",
         why="Nothing on the five report pages changed and no existing query was rewritten \u2014 "
             "this build only adds. Four read-only tables summarise what is already loaded, and "
             "three plain pages show them: <strong>Checks TB</strong> (where every rupee of the "
             "trial balance went, and by which rule), <strong>Checks Stock</strong> (every MB5B "
             "figure taken apart into quantity, MW, crores and the watts per piece those imply, "
             "plus the twelve largest FG and RM materials with the rate and BOM quantity behind "
             "each) and <strong>Checks Sources</strong> (files, sheets, headers, duplicate months, "
             "material-number matching, duplicate master rows and the capacity behind Days). "
             "Every one is the latest month only and sized to be read without scrolling.",
         steps=[
             "Add the four new queries from the <strong>Queries</strong> tab: "
             "<code>qcStockCheck</code>, <code>qcFGRate</code>, <code>qcRMRate</code>, "
             "<code>qcTBRules</code>. Leave Enable load ON for all four.",
             "Or, simpler: download the build 39 package, which already has the pages in it.",
             "Refresh, then read the three new page tabs at the bottom.",
         ],
         find="", repl=""),
    dict(n="000000000000000", build="38", query="factTB_Staged",
         title="A contradictory pair no longer empties a plant, and every line says how it was placed",
         why="Build 36 dropped every GL and profit centre pair that <code>TB Master</code> gives "
             "two different Plants — which took Dholera Module’s entire RM with it. "
             "There is now one tie-break that invents nothing: where the sheet argues between "
             "two plants and the line’s own profit centre names one of those two, that is "
             "the one. Where it still cannot decide, the row stays out and stays visible.",
         steps=[
             "Repaste <code>factTB_Staged</code>, then <code>factTB</code> and "
             "<code>qcTBByGL</code> from the <strong>Queries</strong> tab.",
             "Refresh. Checks → <em>Trial balance by GL account</em> now has a "
             "<strong>Rule</strong> column saying how each account was placed.",
             "A plant reading short: filter that table to it and read the Rule — it says "
             "whether the sheet has no row for those accounts or contradicts itself about them.",
         ],
         find="", repl=""),
    dict(n="00000000000000", build="37", query="factTB_Staged",
         title="Fixes build 36's refresh error (MasterGL matches no exports)",
         why="Build 36 rewrote this query and deleted a step it still referenced, so the "
             "refresh stopped with <em>The import MasterGL matches no exports</em> and sixteen "
             "queries were blocked. The step is restored. Nothing else about build 36 changed.",
         steps=["Repaste <code>factTB_Staged</code> below and refresh."],
         find="", repl=""),
    dict(n="0000000000000", build="36", query="factTB_Staged",
         title="A GL and profit centre pair only counts where TB Master agrees with itself",
         why="Where the same GL account and profit centre appear on <code>TB Master</code> twice "
             "with different Plants, the join took whichever row it met first — so some "
             "accounts landed on the wrong plant and others were right, scattered rather than "
             "swapped, and nothing said so. Such a pair now resolves to nothing and is named "
             "on Checks with both plants, so the duplicate row can be corrected.",
         steps=[
             "Repaste <code>factTB_Staged</code> and <code>qcTBUnmatched</code> below.",
             "Refresh, then read Checks → <em>GL and profit centre pairs TB Master has no "
             "row for</em>. The new <strong>Reason</strong> column says which rows are "
             "duplicates the sheet contradicts itself about.",
             "On <code>TB Master</code>, correct or delete the duplicate so each GL and profit "
             "centre pair appears once with one Plant, and refresh again.",
         ],
         find="", repl=""),
    dict(n="000000000000", build="35", query="factTB_Staged",
         title="The profit centre matches however either file writes it",
         why="The TB export writes the profit centre with two leading zeros that "
             "<code>TB Master</code> does not have, and Excel holds one side as a number and "
             "the other as text — so the same code failed to meet itself. The key is now "
             "the digits and letters only, upper-cased, with spaces, punctuation and leading "
             "zeros removed, on both sides.",
         steps=[
             "Repaste <code>factTB_Staged</code> and <code>qcTBUnmatched</code> below.",
             "Refresh, then look at the Checks table <em>GL and profit centre pairs TB Master "
             "has no row for</em>. It should be far shorter.",
             "Its <em>PCKey</em> column is the profit centre as the join sees it — if a "
             "pair is still listed, compare that key with what your sheet holds.",
         ],
         find="", repl=""),
    dict(n="00000000000", build="34", query="factTB_Staged",
         title="One rule for the trial balance, and a list of every pair still missing",
         why="Build 33 still read the plant out of the profit centre where <code>TB Master</code> "
             "had no row for a pair — so with the sheet half filled, two rules ran at once "
             "and the figures moved further off instead of closer. There is one rule now: the "
             "GL account and profit centre together find a row on <code>TB Master</code>, and "
             "that row’s Plant and Nature are used. A pair with no row is in no "
             "trial-balance figure anywhere, and <code>qcTBUnmatched</code> lists it with what "
             "it is worth, biggest first.",
         steps=[
             "Repaste <code>factTB_Staged</code> below.",
             "Add <code>qcTBUnmatched</code> as a new blank query from the "
             "<strong>Queries</strong> tab, and leave Enable load on.",
             "Refresh, then read the new Checks table <em>GL and profit centre pairs TB Master "
             "has no row for</em>. Every row on it is money the TB side is not counting.",
             "Type those pairs onto <code>TB Master</code> — GL account, profit centre, "
             "Plant, Nature — and refresh again. The list shrinks; when it is empty the "
             "trial balance is complete by construction.",
         ],
         find="", repl=""),
    dict(n="0000000000", build="33", query="factTB_Staged",
         title="The trial balance is matched on GL and profit centre together",
         why="<code>TB Master</code> lists the same GL account against all three plants, so a "
             "GL on its own says only that an account is inventory — it cannot say whose. "
             "The pair, GL account and profit centre, identifies one row of that sheet, and "
             "only then do its Plant, Nature and Sort belong to the line. That is what "
             "separates Dholera Cell from Dholera Module, and it is why 1905 had no trial "
             "balance at all. The nature is read from the sheet’s <strong>Nature</strong> "
             "column rather than guessed from the account description, which is what had "
             "consumables sitting on the FG row.",
         steps=[
             "In <code>Variables and Calculations.xlsx</code> → <code>TB Master</code>, add "
             "<strong>Profit Center</strong> as column F, written exactly as the TB export "
             "writes it, and fill <strong>Plant</strong> (D) beside it on every row.",
             "Repaste <code>factTB_Staged</code> below, then <code>factTB</code> and "
             "<code>qcTBPlants</code> from the <strong>Queries</strong> tab.",
             "Refresh. On Checks, <code>qcTBPlants</code> now has a <em>MatchedRows</em> "
             "column: a profit centre with rows but no matches is one still to be typed into "
             "TB Master.",
             "A pair the sheet does not carry falls back to the old profit-centre reading "
             "rather than vanishing, so nothing that worked before can be taken away by this.",
         ],
         find="", repl=""),
    dict(n="000000000", build="32", query="factTB_Staged",
         title="The trial balance reads its plant from the GL account, so Dholera Cell comes back",
         why="1905 had no trial balance at all because the plant was read out of the profit "
             "centre first, and 1905’s profit centre carries no code to read. The GL account "
             "is the one key the export and <code>TB Master</code> certainly share — column C "
             "against column D — so that is what is consulted first now, with the profit "
             "centre as the fallback. A GL that <code>TB Master</code> gives to two different "
             "plants is left to the profit centre instead: where the sheet is not unanimous, the "
             "GL cannot name a plant on its own, and picking one would move money to the wrong "
             "plant.",
         steps=[
             "In <code>Variables and Calculations.xlsx</code> → <code>TB Master</code>, make "
             "sure the <strong>Plant</strong> column reads 1905 against Dholera Cell’s GLs "
             "(1902 / 1900 against the others). This is the sheet the report now believes.",
             "Repaste <code>factTB_Staged</code> below, and <code>qcTBByGL</code> from the "
             "<strong>Queries</strong> tab — it now shows the plant each GL landed under.",
             "Refresh, then look at Summary: Inventory (TB) should carry a 1905 row. If it does "
             "not, Checks → <em>Trial balance by GL account</em> shows which plant those GLs "
             "went to instead.",
         ],
         find="", repl=""),
    dict(n="00000000", build="31", query="varMWCapacity",
         title="Capacity typed per plant, so 1905 finally has days of cover",
         why="Days of cover is megawatts over capacity, and capacity could only be typed per "
             "technology — so 1905, which has no technology rows on the MW sheet, had no "
             "denominator and dropped out of every Days table. A row labelled <code>Total</code> "
             "is now read as that plant’s whole capacity: the <em>March’26 | MW(S)</em> "
             "block on your working, 8.28 against 1902, 6.17 against 1900, 5.63 against 1905. "
             "Where a plant has a Total row that is its denominator; where it has none the "
             "technology rows are added up as before, so a plant with both cannot count its "
             "capacity twice. <code>Total</code>, <code>All</code>, <code>All Plants</code> and "
             "<code>MW(S)</code> all mean the same thing, and none of them is ever shown as a "
             "technology.",
         steps=[
             "On the <code>MW Capacity</code> sheet, keep your layout exactly as it is and add "
             "one row: <em>Total</em> in the technology column, and each plant’s whole "
             "capacity under its own plant column.",
             "Repaste <code>varMWCapacity</code> below, then <code>dimNature</code> from the "
             "<strong>Queries</strong> tab so the total row cannot appear as a nature.",
             "On the <strong>Measures</strong> tab repaste <code>Capacity MW</code> and "
             "<code>Capacity MW (plant)</code> — those two are what choose between the "
             "plant total and the technology rows.",
             "Refresh. 1905 now has a figure in every Days table; if it does not, "
             "<code>qcMWSheet</code> on Checks shows the sheet exactly as the query reads it.",
         ],
         find="", repl=""),
    dict(n="0000000", build="30", query="varMWCapacity",
         title="The MW sheet as a month per column, so a new month is a new column",
         why="The sheet is now read the way your FG working has it: a plant down the side, a "
             "month across the top, the column heading being the date those figures take "
             "effect from. Type a new month into a new column and nothing already there is "
             "touched \u2014 which matters, because a month with no column of its own keeps the "
             "last figure to its left, so overwriting one rewrites history. An empty cell is "
             "left empty rather than read as nought (nought capacity would wipe out the figure "
             "before it) and a dash is nought. The <strong>Techno</strong> column is optional: "
             "without it the row is that plant\u2019s whole capacity, and days of cover then "
             "reads per plant with the per-technology figure blank rather than invented. The "
             "old two layouts still load, so nothing breaks while you move the sheet over.",
         steps=[
             "Lay the <code>MW Capacity</code> sheet out as: <em>Techno</em> (optional), "
             "<em>Plant</em> holding 1902 / 1900 / 1905, then one column per month headed with "
             "that month\u2019s date as a real date, not text. A revised workbook is in "
             "the <strong>Auto</strong> download as <code>Variables and Calculations - sheet "
             "layout.xlsx</code> — all six sheets, a read-me tab, and your own rows to be "
             "pasted under the headings of the three master sheets.",
             "Repaste <code>varMWCapacity</code> below, and <code>dimNature</code> from the "
             "<strong>Queries</strong> tab \u2014 it now leaves the plant-level "
             "<code>(All)</code> row out of the nature list, so it cannot appear as a slice or "
             "a slicer tick.",
             "Refresh. <code>qcMWSheet</code> on Checks shows the sheet exactly as the query "
             "reads it, cell for cell, if a column is not being picked up.",
         ],
         find="", repl=""),
    dict(n="000000", build="29", query="",
         title="1902 is Jaipur Module and 1900 is Dholera Module, and the plant row expands again",
         why="Jaipur and Dholera were reading each other\u2019s figures because I fixed the codes "
             "in the code the way they were dictated to me, and your own Summary workbook has "
             "them the other way round: it labels its rows <em>1902 Jaipur Module</em>, "
             "<em>1900 Dholera Module</em>, <em>1905 Dholera Cell</em>, and the figures the "
             "report shows against 1902 are the figures that sheet prints on the Jaipur row. "
             "Both names are decided in <code>dimPlant</code> and read by every page, so this "
             "one query settles it everywhere. And Summary\u2019s rows go back to what you had: "
             "a plant, carrying that plant\u2019s whole inventory for the month, with a + that "
             "opens RM, FG and Consumables underneath.",
         steps=[
             "Repaste <code>dimPlant</code> from the <strong>Queries</strong> tab \u2014 that is "
             "where the three codes and names are decided \u2014 and <code>factTB_Staged</code>, "
             "which reads a profit centre that spells the plant out (JAIPUR \u2192 1902, "
             "CELL \u2192 1905, DHOLERA \u2192 1900).",
             "On Summary, on each of the three matrices \u2014 <em>Inventory (TB)</em>, "
             "<em>Inventory (MB5B)</em>, <em>Difference</em> \u2014 empty the Rows well and put "
             "in <code>dimPlant[Plant]</code> first, then <code>dimCategory[Category]</code> "
             "under it. Leave Columns as <code>dimDate[MonthName]</code> alone: the months must "
             "stay the only column field, because that is the hierarchy that was hiding the "
             "history.",
             "The table now opens on three plant rows. Click the + beside a plant to see RM, FG "
             "and Consumables, or the expand arrows at the top of the row header to open all "
             "three at once; whichever way you leave it is how it saves.",
             "Overview\u2019s two plant cards swap with them: the card fed by "
             "<code>Ticker 1902 Rs Cr</code> is titled <em>1902 Jaipur Module</em> and the one "
             "fed by <code>Ticker 1900 Rs Cr</code> is <em>1900 Dholera Module</em>.",
         ],
         find="", repl=""),
    dict(n="00000", build="28", query="",
         title="Summary with nothing to expand, and the plant names fixed in one place",
         why="Your Desktop opens every hierarchy collapsed however the file is saved \u2014 the "
             "three metric headings with no months under them, the plants with no RM / FG / "
             "Consumables under them. So Summary no longer has a hierarchy in it. Rows are one "
             "flat field that already reads <em>1900 Jaipur Module \u2014 RM</em>, and the three "
             "master columns are three matrices sitting flush across one box, each with the "
             "months as its only columns: the newest March plus the three most recent by default, "
             "your slicer ticks instead when you tick them. Same layout you asked for, nine rows "
             "that are simply there.",
         steps=[
             "This one needs a new query and two relationships, so the <strong>Auto</strong> tab "
             "download is much the quicker route \u2014 everything on this page is already in it.",
             "By hand, in Power Query: add the new query <code>dimPlantType</code> from the "
             "<strong>Queries</strong> tab, and repaste <code>factInventory</code>, "
             "<code>factTB</code> and <code>dimPlant</code> from there too \u2014 the two facts "
             "gain the key <code>PlantType</code> that it joins on, and dimPlant is where the "
             "three plant names are now decided.",
             "Model view: join <code>dimPlantType[PlantType]</code> to "
             "<code>factInventory[PlantType]</code> and to <code>factTB[PlantType]</code>, both "
             "One to many, Single. Then sort <code>dimPlantType[Plant and Type]</code> by "
             "<code>RowSort</code> (Column tools \u2192 Sort by column).",
             "On the page: three matrices side by side where the one table was, about 416 wide "
             "and 248 high each. Rows: <code>dimPlantType[Plant and Type]</code> only. Columns: "
             "<code>dimDate[MonthName]</code> only. Values: <code>TB Inventory Rs Cr</code> on "
             "the first, <code>Inventory Rs Cr</code> on the second, "
             "<code>Difference Inventory Rs Cr</code> on the third. Titles: "
             "<em>Inventory (TB)</em>, <em>Inventory (MB5B)</em>, <em>Difference</em> \u2014 those "
             "titles <em>are</em> your three master columns.",
             "On each: Filters pane \u2192 the measure <code>In Summary Window</code> \u2192 is 1; "
             "Format \u2192 Subtotals \u2192 Column subtotals <strong>Off</strong>, Row subtotals "
             "On; and in the Rows well click the field\u2019s arrow \u2192 "
             "<strong>Show items with no data</strong>, so a plant with a blank figure still "
             "shows as a row instead of disappearing.",
             "Also repaste <code>factTB_Staged</code> (1905 read from the plant name as well as "
             "the code) and, on the Detail matrix, replace <code>Share of Total %</code> with its "
             "new text from the <strong>Measures</strong> tab \u2014 it read 100% on every row "
             "because its denominator was the row itself.",
         ],
         find="", repl=""),
    dict(n="0000", build="27", query="",
         title="Ticking months adds them up \u2014 the seven measures that asked the visual what "
               "grain they were being read at",
         why="Those measures were written as <code>IF(ISINSCOPE(dimDate[MonthName]), the figure, "
             "the closing month)</code>, which trusts the visual to say whether a month is on "
             "show. A matrix whose column hierarchy is sitting collapsed does not always say so, "
             "and the figure then comes back as the plain sum over every month in the window "
             "\u2014 four month-ends added together, the one thing inventory must never be. "
             "They no longer ask: each one works out the last month that has data in the current "
             "filter and returns <em>that</em> month's level, full stop. In a month column that "
             "is the month itself, so nothing you already read changes; on a collapsed heading, "
             "a quarter, a Total row or a four-month window it is the newest of those months.",
         steps=[
             "The seven are <code>Inventory Rs Cr</code>, <code>Inventory MW</code>, "
             "<code>TB Inventory Rs Cr</code>, <code>Summary Value Rs Cr</code>, "
             "<code>Days by Period</code>, <code>Unit Value by Period</code> and "
             "<code>RM Days All Plants by Period</code>.",
             "Their new text is on the <strong>Measures</strong> tab of this site with a copy "
             "button on each. In Power BI: click the measure in the Data pane, select "
             "everything in the formula bar, paste, press Enter.",
             "Or just take the <strong>Auto</strong> tab download, which has all seven and "
             "every query fix on this page already in it.",
         ],
         find="", repl=""),
    dict(n="000", build="26", query="factTB",
         title="Trial balance reading high \u2014 SAP subtotal lines, and a doubled export",
         why="Two things that inflate a trial balance without any single figure being wrong. SAP "
             "writes <em>subtotal</em> and <em>Result</em> lines into the same column as the "
             "account numbers, and each carries the sum of the lines above it \u2014 leave one in "
             "and that money is counted twice. Those lines are dropped now. And a TB line "
             "arriving twice is counted once, on the same rule your stock files already use: the "
             "same month, account, profit centre and amount is the same line, whatever the file "
             "was called, so a month exported twice into the TB folder cannot double the books. "
             "Paste this with the factTB_Staged card below it \u2014 that one stops the TB Master's "
             "plant rescuing a line with no profit centre at all, which is usually a subtotal."),
    dict(n="00", build="26", query="",
         title="Summary as one table \u2014 TB / MB5B / Check as the master columns, months under "
               "them. Do this on the visual, not in a query",
         why="Six blocks side by side was my doing, not yours, and build 24 then put the months "
             "on top and the three metrics underneath, which is the wrong way round. It is now "
             "a <strong>single</strong> matrix across the full width with "
             "<strong>Inventory (TB)</strong>, <strong>Inventory (MB5B)</strong> and "
             "<strong>Difference</strong> as the three master columns and the months underneath "
             "each of them, exactly as the Excel sheet had it. Rows are the three plants, each "
             "opening into RM / FG / Consumables; the Grand Total row at the foot is every plant "
             "added together, so the Total Overall blocks are not needed.",
         steps=[
             "Easiest is the <strong>Auto</strong> tab download \u2014 it is drawn this way "
             "already, and every query fix on this page is inside it.",
             "By hand: keep one matrix, delete the other five, then drag it out to the full "
             "width of the white area and about 248 high \u2014 only as tall as its rows, so "
             "nothing sits blank under it \u2014 then pull the three charts below up into the "
             "space and make each of them about 168 high.",
             "Rows: <code>dimPlant[Plant]</code> then <code>dimCategory[Category]</code>. "
             "Columns: <code>dimMetric[Metric]</code> <strong>first</strong>, then "
             "<code>dimDate[MonthName]</code> \u2014 that order is what makes the metric the "
             "master column. Values: the single measure <code>Summary Value Rs Cr</code>, which "
             "reads which master column a cell is in and returns the books, the stock report or "
             "the gap accordingly.",
             "If it opens showing only the three metric headings and no months, click the "
             "matrix and use the expand arrows at the top right of its header, or right-click "
             "one of the headings \u2192 Expand \u2192 All. Save, and Power BI remembers it.",
             "Format pane \u2192 Subtotals \u2192 Row subtotals <strong>On</strong> with Per row "
             "level On (that is the plant total and the Grand Total), Column subtotals "
             "<strong>Off</strong> (a Total column would add March to July).",
             "Format pane \u2192 Values / Row headers / Column headers \u2192 Font size 8, and "
             "Word wrap On for the column headers: twelve figures across the width.",
             "Overview, FG, RM and Detail are untouched.",
         ],
         find="", repl=""),
    dict(n="0a", build="23", query="factTB_Staged",
         title="Inventory (TB) missing plant 1905, and missing its Raw Material row",
         why="Two faults, both on the TB side only \u2014 MB5B was never involved. <strong>The "
             "plant:</strong> a trial balance row carries a profit centre, not a plant, and the "
             "old code read the plant out of characters 3\u20136 of it and nowhere else. A "
             "profit centre written to any other pattern therefore resolved to no plant, and "
             "the row was dropped \u2014 which is how one plant disappears from Inventory (TB) "
             "while MB5B still shows it. Now: those four characters first, then the first of "
             "1900 / 1902 / 1905 appearing <em>anywhere</em> in the profit centre, then in its "
             "description, then the Plant or Nature written against that GL on your "
             "<strong>TB Master</strong> sheet. <strong>The RM row:</strong> the category test "
             "asked about consumables before raw material, and an account called \"Raw "
             "Material &amp; Packing\" contains the word PACK \u2014 so the whole of RM was "
             "filed as Consumables, the RM row vanished and Consumables read far too high. Raw "
             "material is now tested first. Nothing is dropped silently any more: "
             "<strong>qcTBPlants</strong> on Checks lists every profit centre, what it resolved "
             "to and what it is worth, so an unresolved one can be read off the screen instead "
             "of guessed at."),
    dict(n="0b", build="23", query="factTB",
         title="Same fix, second half \u2014 the RM / FG / Consumables split and the plant filter",
         why="Paste this straight after the one above; they are one change in two queries. Raw "
             "material is tested before consumables here, and the rows that resolve to none of "
             "the three plants are left out at this step rather than the one before it, so "
             "qcTBPlants can still account for them. There is still no Unallocated plant."),
    dict(n="0c", build="23", query="qcTBPlants",
         title="New self-check \u2014 every TB profit centre and the plant it resolved to",
         why="A brand new query, so create it rather than replace it: Power Query \u2192 Home "
             "\u2192 New Source \u2192 Blank Query \u2192 Advanced Editor \u2192 paste \u2192 "
             "Done \u2192 rename it exactly <code>qcTBPlants</code>, and leave Enable load "
             "<strong>on</strong>. It is the table that answers \"why is that plant not on the "
             "TB side\" without either of us guessing: a blank or (none) under PlantResolved is "
             "a row Inventory (TB) leaves out, and the amount beside it is exactly what is "
             "missing. Read me those profit centre codes and the rule becomes exact."),
    dict(n="0", build="22", query="",
         title="Empty tables, and no months under TB / MB5B / Difference \u2014 take the "
               "download for this one",
         why="One fault behind both: a matrix with <em>two</em> fields in Columns, a metric "
             "above the month. Power BI opens such a matrix on its outer level only \u2014 one "
             "figure per metric and no month history, which is why ticking months changed a "
             "single number instead of adding columns \u2014 and where the file tries to "
             "pre-open it, Desktop draws the visual as an empty card, which is what emptied "
             "Summary's lower block and the FG and RM tables. Build 22 stops nesting: each "
             "metric gets its own matrix with <code>dimDate[MonthName]</code> as the only "
             "field in Columns, laid out side by side \u2014 an <strong>In MW</strong> block, "
             "an <strong>In Rs Cr</strong> block and an <strong>In Days</strong> block on FG, "
             "In Rs Cr and In Days on RM, and TB / as per MB5B / Check on Summary, each over "
             "its own row of months. That is the layout of the Excel sheets these pages "
             "replace. Column subtotals are off everywhere too: inventory is a level, not a "
             "flow, so there is no Total column adding March to July \u2014 the Total row, "
             "which adds the plants inside one month, stays.",
         steps=[
             "This one is ten new visuals across three pages, so doing it by hand is not "
             "worth your evening: take the download on the <strong>Auto</strong> tab. Every "
             "query fix on this page is already inside it, so nothing you pasted is lost.",
             "If you do want to do it by hand: on each existing matrix, drag "
             "<code>dimMetric[Metric]</code> (or <code>dimMeasure[Measure]</code>) out of the "
             "Columns box so only <code>dimDate[MonthName]</code> is left, put a "
             "<strong>single</strong> measure in Values, then copy-paste the visual once per "
             "extra metric and swap that measure. Format pane \u2192 Subtotals \u2192 Column "
             "subtotals: Off on each.",
             "Leave <code>In Summary Window is 1</code> in the Filters pane exactly as it is: "
             "that is what holds the columns to the newest March plus the three months after "
             "it until you tick months yourself.",
             "Overview and Detail are untouched.",
         ],
         find="", repl=""),
    dict(n="1", build="20", query="dimTBMaster",
         title="Errors in dimTBMaster \u2014 the TB whitelist erroring on every one of its rows",
         why="A forced type cast. <code>Int64.Type</code> on the sort column, and "
             "<code>type text</code> on the rest, error the whole row when one cell holds a "
             "blank, a dash, a number stored as text, or 1.5 \u2014 and Power BI then reports "
             "<em>Errors in dimTBMaster</em>. What is lost is the whitelist of inventory GL "
             "accounts, so Inventory (TB) reads empty and Difference reads as minus MB5B. Every "
             "column is now converted cell by cell with a fallback, so an untidy cell becomes a "
             "blank instead of an error. A spreadsheet typed by hand is allowed to be untidy; "
             "the report has to cope with it."),
    dict(n="2", build="20", query="dimMaterialAttr",
         title="The RM master \u2014 same cure, so one loosely typed cell cannot cost every nature",
         why="This is the query that reads your <strong>RM Nature</strong> sheet (there is no "
             "query called RM Master). <code>BOM Std Qty</code> cast straight to a number errors "
             "the row when the cell holds text, a dash or a stray space, and an errored row "
             "carries no nature, no group nature and no MW with it."),
    dict(n="3", build="20", query="varConstants",
         title="The Constants sheet \u2014 it carries the RM megawatt factor",
         why="If the 580 is typed as text, or an Effective From cell is not a date, the row "
             "errors and RM MW comes out blank across the whole report."),
    dict(n="4", build="19", query="factTB_Staged",
         title="The trial balance now reads the folder and the TB Master whitelist in one query",
         why="This is the fix for <em>\u201creferences other queries or steps, so it may not "
             "directly access a data source\u201d</em> on factTB. A query may open as many "
             "sources as it likes; it may not lean on another query for data and reach a source "
             "as well. Doing the whitelist join here, where the TB folder is already being read, "
             "removes that pairing altogether. It also carries the safe conversion of the "
             "<code>Amount</code> column, so an amount typed with a comma or a dash for nil "
             "cannot error its row."),
    dict(n="5", build="19", query="factTB",
         title="\u2026 so factTB reads nothing but the staged table",
         why="It keeps the rows the whitelist matched, using the <code>Whitelisted</code> flag "
             "set in factTB_Staged, and works out RM / FG / Consumables from the Nature text. "
             "Paste this <strong>after</strong> #4, since it needs that flag to exist. It also "
             "no longer keeps every TB row when TB Master matches nothing \u2014 that fallback "
             "was reading Buildings and Plant &amp; Machinery as raw-material inventory."),
    dict(n="6", build="19", query="factTB_Unmapped",
         title="\u2026 and so does the list of GL accounts TB Master does not cover",
         why="Reads the same flag, so the two can never disagree about which account counted."),
    dict(n="7", build="19", query="",
         title="&ldquo;references other queries or steps, so it may not directly access a data "
               "source&rdquo; \u2014 a dozen queries blocked at once",
         why="Power Query's privacy firewall refusing to let a folder source and the "
             "<code>Variables and Calculations</code> workbook meet \u2014 which is the whole "
             "design, since the figures come from the folders and the names come from the "
             "workbook. It is not a fault in any query and cannot be coded around: two sources "
             "have to meet somewhere. Turn the firewall off for your own files, once: "
             "<strong>File &rarr; Options and settings &rarr; Options &rarr; GLOBAL &rarr; "
             "Privacy &rarr; tick &ldquo;Always ignore Privacy Level settings&rdquo; &rarr; "
             "OK</strong>, then the same under <strong>CURRENT FILE &rarr; Privacy</strong>, "
             "then Refresh. The Global one covers every file you open afterwards, so this is the "
             "last time it will bite."),
]

HOWTO = ("Newest first. Each one is a <strong>whole query</strong>: in Power Query click the "
         "query named on the card, <strong>Home &rarr; Advanced Editor</strong>, "
         "<strong>Ctrl+A</strong>, <strong>Delete</strong>, paste, <strong>Done</strong>. "
         "Nothing to hunt for and nothing to match up. Do them in the order shown \u2014 #5 and "
         "#6 read a column that #4 creates \u2014 and press <strong>Close &amp; Apply</strong> "
         "once at the end. Red error text between pastes is normal. Every one of these is "
         "already inside the download on the <strong>Auto</strong> tab, so a fresh copy needs "
         "none of them.")


def edit_cards(qcode):
    """The Edits tab's HTML. qcode maps query name -> its full M code from the guide."""
    out = []
    for e in EDITS:
        name, body = e["query"], ""
        if e.get("steps"):
            body = "<ul class='elist'>" + "".join("<li>%s</li>" % x for x in e["steps"]) + "</ul>"
        if name:
            code = qcode.get(name)
            if code is None:
                raise SystemExit("edits.py names a query the guide does not define: " + name)
            body = ("<p class='note'>Power Query &rarr; click <strong>%s</strong> in the list on "
                    "the left &rarr; <strong>Home &rarr; Advanced Editor</strong> &rarr; "
                    "<strong>Ctrl+A</strong> &rarr; <strong>Delete</strong> &rarr; paste this "
                    "&rarr; <strong>Done</strong>.</p>"
                    "<button class='copy' data-target='ecode%s'>Copy the whole query</button>"
                    "<pre id='ecode%s'>%s</pre>"
                    % (html.escape(name), e["n"], e["n"], html.escape(code)))
        out.append(
            '<section class="card" id="e-%s" data-name="%s">\n'
            '  <header><span class="num">%s</span><h3>%s</h3>'
            '<button class="done" data-key="e-%s">Done</button></header>\n'
            '  <p class="note"><strong>Why:</strong> %s</p>\n  %s\n</section>'
            % (e["n"], html.escape(name or "privacy setting").lower(), e["n"], e["title"],
               e["n"], e["why"], body))
    return "\n".join(out)
