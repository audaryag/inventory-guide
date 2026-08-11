"""Single source of truth for the report pages.

build.py turns this into (a) the guided click-by-click steps on the web page and
(b) the PART 4 section of BUILD_GUIDE.md, so the two can never disagree.
"""

CANVAS = (1280, 720)

PAGES = ["Overview", "Summary", "FG", "RM", "Data Quality"]

# ---- header band, built once on Overview then copied ------------------------------------
CARDS = [
    ("Inventory Total",  16, 12, 240, 88, "Total inventory"),
    ("Inv RM",          264, 12, 240, 88, "Raw materials"),
    ("Inv FG",          512, 12, 240, 88, "Finished goods"),
    ("Inv Consumables", 760, 12, 240, 88, "Consumables"),
    ("Difference",     1008, 12, 240, 88, "TB vs MB5B difference"),
]

SLICERS = [
    ("dimDate[MonthName]", 16, 108, 300, 44, "Month"),
    ("dimPlant[Plant]",   324, 108, 300, 44, "Plant"),
]

# ---- one entry per visual ----------------------------------------------------------------
# wells: list of (well name, [fields])  |  pos: (x, y, w, h)  |  extra: list of extra clicks
VISUALS = [
    # page, visual type, title, wells, pos, why, extra
    ("Overview", "Stacked column chart", "Inventory by month and category",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Y-axis", ["Closing Value"]),
      ("Legend", ["factInventory[Category]"])],
     (16, 168, 764, 272),
     "Shows the whole inventory month by month, split RM / FG / consumables.", []),

    ("Overview", "Clustered column chart", "Inventory by plant",
     [("X-axis", ["dimPlant[Plant]"]),
      ("Y-axis", ["Closing Value"]),
      ("Legend", ["factInventory[Category]"])],
     (788, 168, 476, 272),
     "Shows which plant is holding the stock.", []),

    ("Overview", "Line chart", "Closing value vs previous month",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Y-axis", ["Closing Value", "Prev Month"])],
     (16, 452, 1248, 260),
     "Two lines: this month and last month, so a jump is obvious.", []),

    ("Summary", "Matrix", "Trial balance vs MB5B",
     [("Rows", ["dimPlant[Plant]"]),
      ("Values", ["TB Value", "Closing Value", "Difference", "Difference %"])],
     (16, 168, 764, 300),
     "The reconciliation itself: what the books say vs what the stock report says.",
     ["In the Values well click the little arrow next to Difference → Conditional formatting "
      "→ Background color.",
      "Set Format style to Diverging. Minimum red, Centre white with Centre = 0, Maximum red.",
      "Both ends red on purpose: a difference either direction is equally wrong."]),

    ("Summary", "Waterfall chart", "Difference by plant",
     [("Category", ["dimPlant[Plant]"]),
      ("Y-axis", ["Difference"])],
     (788, 168, 476, 300),
     "Shows which plant creates the gap, rather than just that a gap exists.", []),

    ("Summary", "Line chart", "Difference trend",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Y-axis", ["Difference"])],
     (16, 480, 1248, 232),
     "Tells you whether the gap is being cleaned up or getting worse.", []),

    ("FG", "Matrix", "FG by tech and material",
     [("Rows", ["dimNature[Nature]", "factInventory[Material]"]),
      ("Values", ["Closing Value", "FG MW", "Capacity MW", "Days", "INR per Wp"]),
      ("Filters", ["factInventory[Category]  →  is FG"])],
     (16, 168, 1248, 288),
     "The main FG table: value, MW, capacity, days and rupees per watt in one grid.",
     ["Format pane → Row headers → turn Stepped layout OFF, so Nature and Material get "
      "their own columns."]),

    ("FG", "Area chart", "FG value by tech over time",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Y-axis", ["Closing Value"]),
      ("Legend", ["dimNature[Nature]"]),
      ("Filters", ["factInventory[Category]  →  is FG"])],
     (16, 468, 828, 244),
     "History of FG stock, split by technology.", []),

    ("FG", "Line chart", "FG inventory days",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Y-axis", ["Days"]),
      ("Filters", ["factInventory[Category]  →  is FG"])],
     (852, 468, 412, 244),
     "Days of inventory — the number your superior will ask for first.", []),

    ("RM", "Matrix", "RM by plant and nature",
     [("Rows", ["dimPlant[Plant]", "dimNature[Nature]", "factInventory[GroupNature]"]),
      ("Values", ["Closing Value", "MW"]),
      ("Filters", ["factInventory[Category]  →  is RM"])],
     (16, 168, 620, 544),
     "The RM equivalent of the FG grid.", []),

    ("RM", "Decomposition tree", "RM breakdown",
     [("Analyze", ["Closing Value"]),
      ("Explain by", ["dimPlant[Plant]", "dimNature[Nature]", "factInventory[GroupNature]"]),
      ("Filters", ["factInventory[Category]  →  is RM"])],
     (644, 168, 620, 544),
     "Replaces most of what the RM sheet does by hand, and drills in any order you click.",
     []),

    ("Data Quality", "Card", "Rows missing master attributes (want 0)",
     [("Fields", ["Rows Missing Attr"])],
     (16, 168, 300, 100),
     "Materials with no row in the master sheets. Should read 0.", []),

    ("Data Quality", "Card", "Stock reconciliation (must be 0)",
     [("Fields", ["Stock Recon"])],
     (324, 168, 300, 100),
     "Opening + receipts - issues - closing. Anything but 0 means a file is duplicated, "
     "truncated or hand-edited.", []),

    ("Data Quality", "Table", "GLs in TB but not in TB Master (want empty)",
     [("Columns", ["factTB_Unmapped[GLAccount]", "factTB_Unmapped[GLDesc]",
                   "factTB_Unmapped[Amount]"])],
     (632, 168, 632, 100),
     "Catches a new GL account nobody added to TB Master — otherwise it vanishes silently.",
     []),

    ("Data Quality", "Table", "FG Natures with no capacity row (want empty)",
     [("Columns", ["qcNatureNoCapacity[Nature]"])],
     (16, 276, 608, 210),
     "Anything listed here gets blank Days. This is the check that catches a Nature/Tech typo.",
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
                   "factInventory[Category]", "Closing Value"])],
     (632, 494, 632, 218),
     "Check after every refresh: a missing month looks like a real fall in inventory, "
     "not like an error.", []),
]
