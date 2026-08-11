"""Single source of truth for the report pages.

steps.py turns this into (a) the guided click-by-click steps on the web page and
(b) the PART 4 section of BUILD_GUIDE.md, so the two can never disagree.
"""

CANVAS = (1280, 720)

PAGES = ["Overview", "Summary", "FG", "RM", "Data Quality"]

# ---- header band, built once on Overview then copied ------------------------------------
CARDS = [
    ("Value ₹ Cr",         16, 12, 200, 88, "Total value ₹ Cr"),
    ("RM ₹ Cr",           224, 12, 200, 88, "Raw materials ₹ Cr"),
    ("FG ₹ Cr",           432, 12, 200, 88, "Finished goods ₹ Cr"),
    ("Consumables ₹ Cr",  640, 12, 200, 88, "Consumables ₹ Cr"),
    ("Days of Inventory", 848, 12, 200, 88, "FG days of inventory"),
    ("Value ₹ Cr % vs LM", 1056, 12, 208, 88, "Change vs last month"),
]

SLICERS = [
    ("dimDate[MonthName]", 16, 108, 300, 44, "Month"),
    ("dimPlant[Plant]",   324, 108, 300, 44, "Plant"),
    ("factInventory[Category]", 632, 108, 300, 44, "Category"),
]

# ---- one entry per visual ----------------------------------------------------------------
# wells: list of (well name, [fields])  |  pos: (x, y, w, h)  |  extra: list of extra clicks
VISUALS = [
    ("Overview", "Stacked column chart", "Value ₹ Cr by month and category",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Y-axis", ["Value ₹ Cr"]),
      ("Legend", ["factInventory[Category]"])],
     (16, 168, 764, 264),
     "Every month side by side, split RM / FG / consumables.", []),

    ("Overview", "Clustered column chart", "Value ₹ Cr by plant",
     [("X-axis", ["dimPlant[Plant]"]),
      ("Y-axis", ["Value ₹ Cr"]),
      ("Legend", ["factInventory[Category]"])],
     (788, 168, 476, 264),
     "Which plant is holding the stock, and of what kind.", []),

    ("Overview", "Line and clustered column chart",
     "Value ₹ Cr — this month vs last month",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Column y-axis", ["Value ₹ Cr", "Value ₹ Cr LM"]),
      ("Line y-axis", ["Value ₹ Cr % vs LM"])],
     (16, 444, 764, 268),
     "Bars compare the two months directly; the line is the percentage swing, which is "
     "what people argue about.", []),

    ("Overview", "Matrix", "Months side by side",
     [("Rows", ["factInventory[Category]"]),
      ("Columns", ["dimDate[MonthName]"]),
      ("Values", ["Value ₹ Cr"])],
     (788, 444, 476, 268),
     "The same numbers as a table, because some readers only trust a table.",
     ["Format pane → Row headers → Stepped layout: Off.",
      "Turn Format pane → Subtotals → Row subtotals: On, so each column has a total."]),

    ("Summary", "Matrix", "Value ₹ Cr by month, category and plant",
     [("Rows", ["factInventory[Category]", "dimPlant[Plant]"]),
      ("Columns", ["dimDate[MonthName]"]),
      ("Values", ["Value ₹ Cr"])],
     (16, 168, 1248, 264),
     "The whole model in one grid: months across, category and plant down. Click a row's "
     "arrow to expand plants under a category.",
     ["Format pane → Row headers → Stepped layout: Off.",
      "Format pane → Subtotals → turn on both Row subtotals and Column subtotals."]),

    ("Summary", "Matrix", "MW and days by month",
     [("Rows", ["dimDate[MonthName]"]),
      ("Values", ["MW", "FG MW", "Capacity MW", "Days of Inventory", "Days vs LM"])],
     (16, 444, 620, 268),
     "The MW view of the same months, with days of inventory and how it moved.", []),

    ("Summary", "Matrix", "Trial balance vs MB5B",
     [("Rows", ["dimPlant[Plant]"]),
      ("Values", ["TB ₹ Cr", "Value ₹ Cr", "Difference ₹ Cr", "Difference %"])],
     (644, 444, 620, 268),
     "The reconciliation: what the books say against what the stock report says.",
     ["In the Values well click the arrow next to Difference ₹ Cr → Conditional formatting "
      "→ Background color.",
      "Format style: Diverging. Minimum red, Centre white with Centre = 0, Maximum red.",
      "Both ends red on purpose: a difference either direction is equally wrong."]),

    ("FG", "Matrix", "FG by technology",
     [("Rows", ["dimNature[Nature]"]),
      ("Values", ["Value ₹ Cr", "FG MW", "Capacity MW", "Days of Inventory", "INR per Wp",
                  "Value ₹ Cr % vs LM"]),
      ("Filters", ["factInventory[Category]  →  is FG"])],
     (16, 168, 764, 264),
     "Technology by technology: value, MW, capacity, days, rupees per watt and the "
     "month's movement.",
     ["Format pane → Row headers → Stepped layout: Off."]),

    ("FG", "Matrix", "FG technology by month",
     [("Rows", ["dimNature[Nature]"]),
      ("Columns", ["dimDate[MonthName]"]),
      ("Values", ["FG MW"]),
      ("Filters", ["factInventory[Category]  →  is FG"])],
     (788, 168, 476, 264),
     "MW per technology with the months side by side, so a build-up in one tech is obvious.",
     []),

    ("FG", "Area chart", "FG value ₹ Cr by technology over time",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Y-axis", ["Value ₹ Cr"]),
      ("Legend", ["dimNature[Nature]"]),
      ("Filters", ["factInventory[Category]  →  is FG"])],
     (16, 444, 764, 268),
     "History of FG stock, split by technology.", []),

    ("FG", "Line and clustered column chart", "FG days of inventory vs last month",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Column y-axis", ["Days of Inventory"]),
      ("Line y-axis", ["Days vs LM"]),
      ("Filters", ["factInventory[Category]  →  is FG"])],
     (788, 444, 476, 268),
     "Days of inventory month by month, with the change on a line — the number your "
     "superior asks for first.", []),

    ("RM", "Matrix", "RM by plant and nature",
     [("Rows", ["dimPlant[Plant]", "dimNature[Nature]", "factInventory[GroupNature]"]),
      ("Values", ["Value ₹ Cr", "MW", "Value ₹ Cr % vs LM"]),
      ("Filters", ["factInventory[Category]  →  is RM"])],
     (16, 168, 620, 544),
     "The RM equivalent of the FG grid.",
     ["Format pane → Row headers → Stepped layout: Off."]),

    ("RM", "Matrix", "RM by month",
     [("Rows", ["dimNature[Nature]"]),
      ("Columns", ["dimDate[MonthName]"]),
      ("Values", ["Value ₹ Cr"]),
      ("Filters", ["factInventory[Category]  →  is RM"])],
     (644, 168, 620, 264),
     "RM months side by side.", []),

    ("RM", "Decomposition tree", "RM breakdown",
     [("Analyze", ["Value ₹ Cr"]),
      ("Explain by", ["dimPlant[Plant]", "dimNature[Nature]", "factInventory[GroupNature]"]),
      ("Filters", ["factInventory[Category]  →  is RM"])],
     (644, 444, 620, 268),
     "Replaces most of what the RM sheet does by hand, and drills in any order you click.",
     []),

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
