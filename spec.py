"""Single source of truth for the report pages.

steps.py turns this into (a) the guided click-by-click steps on the web page and
(b) the PART 4 section of BUILD_GUIDE.md, so the two can never disagree.
"""

CANVAS = (1280, 720)

PAGES = ["Overview", "Summary", "FG", "RM", "Detail", "Data Quality"]

# The drill-through page: right-click any bar, row or slice on the other pages and choose
# Drill through → Detail, and these fields carry the clicked context across.
DRILL_PAGE = "Detail"
DRILL_FIELDS = ["dimPlant[Plant]", "dimDate[MonthName]", "dimCategory[Category]",
                "dimNature[Nature]"]

# Pages that get a copy of the header band. Detail is driven by what you clicked rather
# than by slicers, and Data Quality should never be filtered.
BAND_PAGES = ["Overview", "Summary", "FG", "RM"]

# ---- header band, built once on Overview then copied ------------------------------------
CARDS = [
    ("Value ₹ Cr",         16, 12, 200, 88, "Total value ₹ Cr"),
    ("RM ₹ Cr",           224, 12, 200, 88, "Raw materials ₹ Cr"),
    ("FG ₹ Cr",           432, 12, 200, 88, "Finished goods ₹ Cr"),
    ("Consumables ₹ Cr",  640, 12, 200, 88, "Consumables ₹ Cr"),
    ("Days of Inventory", 848, 12, 200, 88, "Days of inventory"),
    ("Value ₹ Cr % vs LM", 1056, 12, 208, 88, "Change vs last month"),
]

SLICERS = [
    ("dimDate[MonthName]", 16, 108, 300, 44, "Month"),
    ("dimPlant[Plant]",   324, 108, 300, 44, "Plant"),
    ("dimCategory[Category]", 632, 108, 300, 44, "Category"),
]

# ---- one entry per visual ----------------------------------------------------------------
# wells: list of (well name, [fields])  |  pos: (x, y, w, h)  |  extra: list of extra clicks
VISUALS = [
    ("Overview", "Stacked column chart", "Value ₹ Cr by month and category",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Y-axis", ["Value ₹ Cr"]),
      ("Legend", ["dimCategory[Category]"])],
     (16, 168, 764, 264),
     "Every month side by side, split RM / FG / consumables. Click one segment and the "
     "rest of the page follows it; right-click → Drill through → Detail for the pies "
     "behind it.", []),

    ("Overview", "Clustered column chart", "Value ₹ Cr by plant — click to go deeper",
     [("X-axis", ["dimPlant[Plant]", "dimCategory[Category]", "dimNature[Nature]"]),
      ("Y-axis", ["Value ₹ Cr"])],
     (788, 168, 476, 264),
     "Three fields in the X-axis makes it a hierarchy, so the little arrows appear in the "
     "visual's top-right corner: plant, then category inside a plant, then nature inside "
     "that. Clicking is the whole point — nobody has to build three charts.",
     ["The double-down-arrow in the header turns on drill mode; after that a single click "
      "on a bar opens the next level, and the up-arrow goes back.",
      "Right-click a bar → Drill through → Detail for the pie-chart page instead."]),

    ("Overview", "Line and clustered column chart",
     "Value ₹ Cr — this month vs last month",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Column y-axis", ["Value ₹ Cr", "Value ₹ Cr LM"]),
      ("Line y-axis", ["Value ₹ Cr % vs LM"])],
     (16, 444, 764, 268),
     "Bars compare the two months directly; the line is the percentage swing, which is "
     "what people argue about.", []),

    ("Overview", "Matrix", "Months side by side",
     [("Rows", ["dimCategory[Category]"]),
      ("Columns", ["dimDate[MonthName]"]),
      ("Values", ["Value ₹ Cr"])],
     (788, 444, 476, 268),
     "The same numbers as a table, because some readers only trust a table.",
     ["Format pane → Row headers → Stepped layout: Off.",
      "Turn Format pane → Subtotals → Row subtotals: On, so each column has a total."]),

    # ---- Summary: TB | MB5B | Difference as master columns, plants as master rows -------
    ("Summary", "Matrix", "Inventory (TB) · Inventory (MB5B) · Difference — ₹ Cr",
     [("Rows", ["dimPlant[Plant]", "dimCategory[Category]"]),
      ("Columns", ["dimMetric[Metric]", "dimDate[MonthName]"]),
      ("Values", ["Summary Value ₹ Cr"]),
      ("Filters", ["Last 4 Months  →  is 1"])],
     (16, 168, 1248, 300),
     "The whole reconciliation in one grid, exactly as it is read out: three master columns "
     "(TB, MB5B, Difference), the last four months under each, one row per plant with RM, "
     "FG and consumables beneath it, and a Total row. Everything in crore rupees.",
     ["Order of the two Columns fields matters: dimMetric[Metric] FIRST, then "
      "dimDate[MonthName]. That is what makes TB / MB5B / Difference the master columns "
      "with months nested inside.",
      "Format pane → Row headers → Stepped layout: Off (so Plant and Category get their "
      "own columns).",
      "Format pane → Row headers → +/- icons: On (that is the click-to-expand control).",
      "Format pane → Subtotals → Row subtotals On, Column subtotals Off, and set "
      "'Per row level' so each plant shows its own total. Grand total row = the Total row.",
      "In the Values well, arrow next to Summary Value ₹ Cr → Conditional formatting → "
      "Background color → Format style Diverging, centre 0, both ends red: a difference "
      "either direction is equally wrong.",
      "Expand all plants once with the arrow at the top-left of the matrix, then save — "
      "the expansion state is remembered."]),

    ("Summary", "Clustered column chart", "Difference ₹ Cr by plant — click a bar",
     [("X-axis", ["dimPlant[Plant]"]),
      ("Y-axis", ["Difference ₹ Cr"])],
     (16, 480, 620, 232),
     "The reconciliation as a picture. Click a bar and the matrix above filters to that "
     "plant; right-click → Drill through → Detail for the materials behind it.",
     ["Format pane → Columns → Colour → fx → Format style: Rules, and colour any negative "
      "value red. A difference either direction is equally wrong."]),

    ("Summary", "Clustered column chart", "Inventory (TB) vs Inventory (MB5B) by month",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Y-axis", ["TB ₹ Cr", "Value ₹ Cr"])],
     (644, 480, 620, 232),
     "Two bars per month, books against stock report — a gap that is opening up shows here "
     "before anyone notices it in the numbers.", []),

    # ---- FG: MW | In ₹ Cr | In Days as master columns ----------------------------------
    ("FG", "Matrix", "FG by plant — MW · In ₹ Cr · In Days",
     [("Rows", ["dimPlant[Plant]"]),
      ("Columns", ["dimMeasure[Measure]", "dimDate[MonthName]"]),
      ("Values", ["Unit Value"]),
      ("Filters", ["dimCategory[Category]  →  is FG", "Last 4 Months  →  is 1"])],
     (16, 168, 1248, 176),
     "FG per plant in all three units at once — megawatts, crore rupees and days — with the "
     "last four months under each. Days is MW ÷ capacity MW, so 1905 is blank on purpose.",
     ["dimMeasure[Measure] goes in Columns FIRST, then dimDate[MonthName].",
      "Format pane → Row headers → Stepped layout: Off.",
      "Click a plant row to filter the technology table below it."]),

    ("FG", "Matrix", "FG by technology — MW · In ₹ Cr · In Days",
     [("Rows", ["dimNature[Nature]"]),
      ("Columns", ["dimMeasure[Measure]", "dimDate[MonthName]"]),
      ("Values", ["Unit Value"]),
      ("Filters", ["dimCategory[Category]  →  is FG", "Last 4 Months  →  is 1"])],
     (16, 356, 620, 356),
     "The same three units by technology rather than by plant, which is where a build-up in "
     "one technology shows up.",
     ["Same column order: dimMeasure[Measure] then dimDate[MonthName].",
      "Format pane → Row headers → Stepped layout: Off."]),

    ("FG", "Clustered column chart", "FG MW by technology — click a bar",
     [("X-axis", ["dimNature[Nature]"]),
      ("Y-axis", ["MW"]),
      ("Filters", ["dimCategory[Category]  →  is FG"])],
     (644, 356, 620, 176),
     "Clicking one technology filters both matrices to it; right-click drills through.", []),

    ("FG", "Line and clustered column chart", "Days of inventory by month — click a bar",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Column y-axis", ["Days"]),
      ("Line y-axis", ["Days vs LM"]),
      ("Filters", ["dimCategory[Category]  →  is FG"])],
     (644, 544, 620, 168),
     "Days month by month with the change on a line. Right-click any bar → Drill through → "
     "Detail for the technology and material split behind it.",
     []),

    # ---- RM: plant first, then group nature / nature, in ₹ Cr and days -----------------
    ("RM", "Matrix", "RM by plant — In ₹ Cr · In Days",
     [("Rows", ["dimPlant[Plant]"]),
      ("Columns", ["dimMeasure[Measure]", "dimDate[MonthName]"]),
      ("Values", ["Unit Value"]),
      ("Filters", ["dimCategory[Category]  →  is RM", "Last 4 Months  →  is 1",
                   "dimMeasure[Measure]  →  untick MW"])],
     (16, 168, 1248, 176),
     "RM by plant in crore rupees and days of cover, last four months under each. MW is "
     "unticked here because an RM megawatt figure is a derived number, not a measured one.",
     ["dimMeasure[Measure] in Columns first, then dimDate[MonthName].",
      "In the Filters pane, drag dimMeasure[Measure] in and untick MW.",
      "Format pane → Row headers → Stepped layout: Off."]),

    ("RM", "Matrix", "RM by group nature and nature",
     [("Rows", ["factInventory[GroupNature]", "dimNature[Nature]"]),
      ("Columns", ["dimMeasure[Measure]", "dimDate[MonthName]"]),
      ("Values", ["Unit Value"]),
      ("Filters", ["dimCategory[Category]  →  is RM", "Last 4 Months  →  is 1",
                   "dimMeasure[Measure]  →  untick MW"])],
     (16, 356, 620, 356),
     "Then the same numbers down the material hierarchy: group nature, and nature inside it. "
     "The +/- arrow on each group row is the drill-in.",
     ["Format pane → Row headers → Stepped layout: Off, +/- icons: On."]),

    ("RM", "Clustered column chart", "RM ₹ Cr by group nature — click a bar",
     [("X-axis", ["factInventory[GroupNature]"]),
      ("Y-axis", ["Value ₹ Cr"]),
      ("Filters", ["dimCategory[Category]  →  is RM"])],
     (644, 356, 620, 176),
     "One click sets the whole page to a group nature; right-click drills through to the "
     "materials.", []),

    ("RM", "Decomposition tree", "RM — click through any way you like",
     [("Analyze", ["Value ₹ Cr"]),
      ("Explain by", ["dimPlant[Plant]", "factInventory[GroupNature]", "dimNature[Nature]",
                      "factInventory[Material]"]),
      ("Filters", ["dimCategory[Category]  →  is RM"])],
     (644, 544, 620, 168),
     "The interactive one: click a box and it opens the next level, in whatever order you "
     "click. This is what replaces filtering the RM sheet by hand.",
     ["Click the + on a node to choose which field to split by next."]),

    ("Detail", "Card", "Value ₹ Cr of what you clicked",
     [("Fields", ["Value ₹ Cr"])],
     (16, 16, 296, 92),
     "The drill-through page opens already filtered to the bar or row you came from, so "
     "this card is that one number.", []),

    ("Detail", "Card", "MW",
     [("Fields", ["MW"])],
     (320, 16, 296, 92),
     "Same slice in megawatts.", []),

    ("Detail", "Card", "Days of inventory",
     [("Fields", ["Days of Inventory"])],
     (624, 16, 296, 92),
     "Stock in MW divided by the MW capacity on the Variables sheet. Blank where the "
 "plant has no capacity row — 1905.", []),

    ("Detail", "Card", "Share of the total",
     [("Fields", ["Share of Total %"])],
     (928, 16, 336, 92),
     "How big this slice is against the whole.", []),

    ("Detail", "Pie chart", "Split by category",
     [("Legend", ["dimCategory[Category]"]),
      ("Values", ["Value ₹ Cr"])],
     (16, 120, 404, 296),
     "RM / FG / consumables for exactly what you clicked.",
     ["Format pane → Detail labels → Label contents: Category, percent of total."]),

    ("Detail", "Donut chart", "Split by technology / nature",
     [("Legend", ["dimNature[Nature]"]),
      ("Values", ["Value ₹ Cr"])],
     (428, 120, 404, 296),
     "Which technology or material nature the slice is made of.",
     ["Format pane → Detail labels → Label contents: Category, percent of total."]),

    ("Detail", "Pie chart", "Split by plant",
     [("Legend", ["dimPlant[Plant]"]),
      ("Values", ["Value ₹ Cr"])],
     (840, 120, 424, 296),
     "Where the slice sits. A single-colour pie means it is one plant already.",
     ["Format pane → Detail labels → Label contents: Category, percent of total."]),

    ("Detail", "Table", "Materials behind this number",
     [("Columns", ["factInventory[Material]", "factInventory[MaterialDesc]", "Value ₹ Cr", "MW",
                   "INR per Wp", "Share of Total %"])],
     (16, 428, 1248, 284),
     "The line-item detail: the question 'which materials is that made of?' answered by "
     "clicking, instead of by another Excel sheet.",
     ["Click the Value ₹ Cr column header twice so it sorts largest first."]),

    ("Data Quality", "Card", "Rows missing master attributes (want 0)",
     [("Fields", ["Rows Missing Attr"])],
     (16, 168, 300, 100),
     "Materials with no row in the master sheets.", []),

    ("Data Quality", "Card", "Stock reconciliation ₹ Cr (must be 0)",
     [("Fields", ["Stock Recon ₹ Cr"])],
     (324, 168, 300, 100),
     "Opening + receipts - issues - closing. Anything but 0 means a file is duplicated, "
     "truncated or hand-edited.", []),

    ("Data Quality", "Table", "GLs in TB but not in TB Master (want empty)",
     [("Columns", ["factTB_Unmapped[GLAccount]", "factTB_Unmapped[GLDesc]",
                   "Unmapped TB ₹ Cr"])],
     (632, 168, 632, 100),
     "Catches a new GL account nobody added to TB Master — otherwise it vanishes silently.",
     []),

    ("Data Quality", "Table", "FG technologies with no capacity row (want empty)",
     [("Columns", ["qcNatureNoCapacity[Nature]"])],
     (16, 276, 608, 210),
     "Anything listed here gets blank days. This is the check that catches a Nature/Tech typo.",
     []),

    ("Data Quality", "Table", "Actual headers of every source file",
     [("Columns", ["qcHeaders[Folder]", "qcHeaders[Name]", "qcHeaders[SheetNames]",
                   "qcHeaders[Headers]"])],
     (632, 276, 632, 210),
     "Read this when a column comes through blank — it shows what the file really says.", []),

    ("Data Quality", "Table", "Variables workbook sheets",
     [("Columns", ["qcVarHeaders[SheetName]", "qcVarHeaders[Headers]",
                   "qcVarHeaders[DataRows]"])],
     (16, 494, 608, 218),
     "DataRows = 0 means a sheet is empty.", []),

    ("Data Quality", "Table", "Files loaded this refresh",
     [("Columns", ["factInventory[SourceFile]", "factInventory[Month]",
                   "factInventory[Category]", "Value ₹ Cr"])],
     (632, 494, 632, 218),
     "Check after every refresh: a missing month looks like a real fall in inventory, "
     "not like an error.", []),
]
