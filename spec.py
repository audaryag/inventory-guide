"""Single source of truth for the report pages.

steps.py turns this into (a) the guided click-by-click steps on the web page and
(b) the PART 4 section of BUILD_GUIDE.md, so the two can never disagree.
"""

CANVAS = (1280, 720)

PAGES = ["Overview", "Summary", "FG", "RM", "Detail"]

# The drill-through page: right-click any bar, row or slice on the other pages and choose
# Drill through → Detail, and these fields carry the clicked context across.
DRILL_PAGE = "Detail"
DRILL_FIELDS = ["dimPlant[Plant]", "dimDate[MonthName]", "dimCategory[Category]",
                "dimNature[Nature]"]

# Pages that get a copy of the header band. Detail is driven by what you clicked rather
# than by slicers, so it gets no slicers of its own.
BAND_PAGES = ["Overview", "Summary", "FG", "RM"]

# ---- header band, built once on Overview then copied ------------------------------------
# 96 high, not 88: a card has to hold a 12pt title strip above a 24pt number, and 88
# clips the lower one of the two.
CARDS = [
    ("Value ₹ Cr",         16, 10, 200, 96, "Total value ₹ Cr"),
    ("RM ₹ Cr",           224, 10, 200, 96, "Raw materials ₹ Cr"),
    ("FG ₹ Cr",           432, 10, 200, 96, "Finished goods ₹ Cr"),
    ("Consumables ₹ Cr",  640, 10, 200, 96, "Consumables ₹ Cr"),
    ("Days of Inventory", 848, 10, 200, 96, "Days of inventory (RM + FG)"),
    ("Value ₹ Cr % vs LM", 1056, 10, 208, 96, "Change vs last month"),
]

SLICERS = [
    ("dimDate[MonthName]", 16, 114, 300, 40, "Month — tick the ones to compare"),
    ("dimDate[Quarter]",  324, 114, 300, 40, "Quarter (FY starts 1 April)"),
    ("dimPlant[Plant]",   632, 114, 300, 40, "Plant"),
    ("dimCategory[Category]", 940, 114, 324, 40, "Category"),
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
     "behind it.",
     ["Stacked, not Clustered: one bar per month whose height is the month's total, cut "
      "into the three categories. Clustered would stand RM, FG and consumables apart and "
      "the month total would no longer be a bar you can read. Not 'line and clustered' "
      "either — that one is the third visual on this page."]),

    ("Overview", "Clustered column chart", "Value ₹ Cr by plant — click to go deeper",
     [("X-axis", ["dimPlant[Plant]", "dimCategory[Category]", "dimNature[Nature]"]),
      ("Y-axis", ["Value ₹ Cr"])],
     (16, 444, 764, 268),
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
     (788, 168, 476, 216),
     "Bars compare the two months directly; the line is the percentage swing, which is "
     "what people argue about.", []),

    ("Overview", "Donut chart", "Share of value — click a slice",
     [("Legend", ["dimCategory[Category]"]),
      ("Values", ["Value ₹ Cr"])],
     (788, 396, 476, 172),
     "Where the money actually sits. Clicking a slice filters the page to that category, "
     "which is quicker than the Category slicer.",
     ["Format pane → Detail labels → Label contents: Percent of total."]),

    ("Overview", "Matrix", "Months side by side",
     [("Rows", ["dimCategory[Category]"]),
      ("Columns", ["dimDate[MonthName]"]),
      ("Values", ["Value ₹ Cr"])],
     (788, 580, 476, 132),
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
      "Format pane → Subtotals → Row subtotals: On. Then switch Column subtotals to Off, "
      "and turn on 'Per row level' so each plant shows its own total. The grand total row "
      "at the bottom is the Total row you asked for.",
      "Colour the differences: in the Values box, click the small down-arrow next to "
      "Summary Value ₹ Cr, click 'Conditional formatting', then 'Background color'. Set "
      "Format style to Diverging, tick 'Add a middle colour', set the middle number to 0, "
      "and make both the Minimum and Maximum colours red. A difference either direction is "
      "equally wrong, so both ends are red.",
      "Right-click any plant row in the matrix, click 'Expand', then 'All', so RM, FG and "
      "consumables show under every plant. Then press Ctrl+S — Power BI remembers it."]),

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
      ("Filters", ["dimCategory[Category]  →  is FG"])],
     (16, 168, 1248, 176),
     "FG per plant in all three units at once — megawatts, crore rupees and days — with the "
     "months you tick under each. Days is MW ÷ capacity MW, so 1905 is blank on purpose.",
     ["dimMeasure[Measure] goes in Columns FIRST, then dimDate[MonthName].",
      "Format pane → Row headers → Stepped layout: Off.",
      "No month filter on this one — the Month slicer decides which months are columns. "
      "Tick any four to compare, or pick a Quarter and it shows that quarter's three.",
      "Click a plant row to filter the technology table below it."]),

    ("FG", "Matrix", "FG by technology — MW · In ₹ Cr · In Days",
     [("Rows", ["dimNature[Nature]"]),
      ("Columns", ["dimMeasure[Measure]", "dimDate[MonthName]"]),
      ("Values", ["Unit Value"]),
      ("Filters", ["dimCategory[Category]  →  is FG"])],
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
      ("Filters", ["dimCategory[Category]  →  is RM",
                   "dimMeasure[Measure]  →  untick MW"])],
     (16, 168, 1248, 176),
     "RM by plant in crore rupees and days, the months you tick under each. MW is "
     "unticked here because an RM megawatt figure is a derived number, not a measured one.",
     ["dimMeasure[Measure] in Columns first, then dimDate[MonthName].",
      "In the Filters pane, drag dimMeasure[Measure] in and untick MW.",
      "Format pane → Row headers → Stepped layout: Off."]),

    ("RM", "Matrix", "RM by group nature and nature",
     [("Rows", ["factInventory[GroupNature]", "dimNature[Nature]"]),
      ("Columns", ["dimMeasure[Measure]", "dimDate[MonthName]"]),
      ("Values", ["Unit Value"]),
      ("Filters", ["dimCategory[Category]  →  is RM",
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
     (16, 16, 296, 96),
     "The drill-through page opens already filtered to the bar or row you came from, so "
     "this card is that one number.", []),

    ("Detail", "Card", "MW",
     [("Fields", ["MW"])],
     (320, 16, 296, 96),
     "Same slice in megawatts.", []),

    ("Detail", "Card", "Days of inventory (RM + FG)",
     [("Fields", ["Days of Inventory"])],
     (624, 16, 296, 96),
     "Stock in MW divided by the MW capacity on the Variables sheet. With no category "
     "picked that MW is RM plus FG over the same capacity, so the two add up — the title "
     "says so rather than leaving a reader to assume it means FG alone. Blank where the "
     "plant has no capacity row — 1905.", []),

    ("Detail", "Card", "Share of the total",
     [("Fields", ["Share of Total %"])],
     (928, 16, 336, 96),
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

    ("Detail", "Matrix", "Materials behind this number — click + to open a nature",
     [("Rows", ["dimNature[Nature]", "factInventory[Material]",
                "factInventory[MaterialDesc]"]),
      ("Values", ["Value ₹ Cr", "MW", "Days", "INR per Wp", "Share of Total %"])],
     (16, 428, 1248, 284),
     "The line-item detail. A Matrix rather than a Table, so it opens nature → material "
     "instead of being one long flat list — that is the difference between clicking and "
     "scrolling.",
     ["Format pane → Row headers → +/- icons: On, Stepped layout: Off. That is the click-to-"
      "open control.",
      "Format pane → Grid → Options → Keep column headers visible: On. The headings then "
      "stay put while the rows scroll inside the visual, so a long list never makes the "
      "visual (or the page) grow.",
      "Format pane → Subtotals → Row subtotals: On, so a closed nature row still shows its "
      "total.",
      "Click the Value ₹ Cr column header once so it sorts largest first."]),

]
