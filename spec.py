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

# ---- colours and type, quoted by every step so nothing is left to taste -----------------
FONT = "Arial"
INK = "#1F2A24"          # body text, and the figures inside the white ticker boxes
HEAD = "#14532D"         # headings
PANEL = "#14532D"        # the ticker panel down the left
PANEL_INK = "#FFFFFF"    # text sitting straight on the green panel
PANEL_SUB = "#BFE3C6"    # the small wording on the green panel
BOX = "#FFFFFF"          # the three white boxes inside the panel
UP, DOWN = "#2E7D32", "#B3261E"

# Overview carries the ticker panel and its own controls, so it is built visual by visual.
# The other pages still share the older card-and-slicer band.
BAND_PAGES = ["Summary", "FG", "RM"]

# ---- header band for Summary / FG / RM ---------------------------------------------------
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

# ---- Overview furniture: a shape, a logo box and three pieces of wording ------------------
# (page, kind, text, x, y, w, h, note)
DECOR = [
    ("Overview", "Rectangle", "", 0, 0, 184, 720,
     "The ticker panel, 184 wide rather than 236 \u2014 narrow enough that the history and the "
     "donuts get the room, wide enough for a four-figure number. Fill %s, no border, no "
     "rounded corners. Right-click it and choose Send to back so everything else sits on "
     "top of it." % PANEL),
    ("Overview", "Image", "", 12, 10, 160, 34,
     "Empty box for the company logo, a wide strip across the top of the panel rather than "
     "a square, because a wordmark logo is wider than it is tall. Insert \u2192 Image, pick any "
     "small file for now, then swap it later by clicking the image and choosing Browse. "
     "Format pane \u2192 Image \u2192 Image fit: Fit, so a wider or narrower logo still sits inside "
     "the strip without being stretched."),
    ("Overview", "Text box", "Inventory", 12, 50, 160, 22,
     "First line of the heading, directly under the logo strip. Arial 15, bold, colour %s, "
     "left aligned." % PANEL_INK),
    ("Overview", "Text box", "Overview", 12, 72, 160, 20,
     "Second line of the heading, on its own line under 'Inventory' so neither word has to "
     "shrink to fit the narrower panel. Arial 13, colour %s, left aligned." % PANEL_SUB),
    ("Overview", "Text box", "By Type", 12, 100, 160, 16,
     "Arial 10, bold, colour %s. Section heading above the first white box." % PANEL_SUB),
    ("Overview", "Rectangle", "", 8, 118, 168, 186,
     "White box number 1, the one the RM, FG and Consumables cards sit inside. Fill %s, "
     "rounded corners 8, no border. Right-click it and choose Send backward once so it "
     "covers the green panel but stays under the cards." % BOX),
    ("Overview", "Text box", "By Plant", 12, 310, 160, 16,
     "Arial 10, bold, colour %s. Section heading above the second white box." % PANEL_SUB),
    ("Overview", "Rectangle", "", 8, 328, 168, 186,
     "White box number 2, for the three plant cards. Fill %s, rounded corners 8, no border, "
     "then Send backward once." % BOX),
    ("Overview", "Rectangle", "", 8, 522, 168, 186,
     "White box number 3, for Total, Change since Last Month and the As on line. Fill %s, "
     "rounded corners 8, no border, then Send backward once." % BOX),
]

# ---- one entry per visual ----------------------------------------------------------------
# wells: list of (well name, [fields])  |  pos: (x, y, w, h)  |  extra: list of extra clicks
VISUALS = [
    # ---- Overview: the ticker panel, three white boxes, fixed to the latest month -------
    ("Overview", "Card", "RM",
     [("Fields", ["Ticker RM Rs Cr"])],
     (14, 122, 156, 58),
     "Panel figure, sitting inside the white box. It reads the latest month that has data "
     "and ignores every slicer on the page, because stock is a level, not something you "
     "add up across months.",
     ["Format pane \u2192 Callout value \u2192 Display units: None, Value decimal places: 1, "
      "Font: Arial, Font size: 20, Bold: On, Colour: #1F2A24 (near-black, because the box "
      "behind it is white now). Display units None is what stops Power BI writing 2.5K "
      "instead of 2,539.4.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 10, Colour: #14532D, "
      "Text: the title above.",
      "Format pane \u2192 General \u2192 Effects \u2192 Background: Off, and Border: Off. The white "
      "comes from the box shape underneath, so the card itself stays see-through.",
      "Format pane \u2192 General \u2192 Properties \u2192 Position: set Horizontal (X) and "
      "Vertical (Y) to 14 and 122 exactly, or the card will not sit square inside its box."],
     ),

    ("Overview", "Card", "FG",
     [("Fields", ["Ticker FG Rs Cr"])],
     (14, 182, 156, 58),
     "Panel figure, sitting inside the white box. It reads the latest month that has data "
     "and ignores every slicer on the page, because stock is a level, not something you "
     "add up across months.",
     ["Format pane \u2192 Callout value \u2192 Display units: None, Value decimal places: 1, "
      "Font: Arial, Font size: 20, Bold: On, Colour: #1F2A24 (near-black, because the box "
      "behind it is white now). Display units None is what stops Power BI writing 2.5K "
      "instead of 2,539.4.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 10, Colour: #14532D, "
      "Text: the title above.",
      "Format pane \u2192 General \u2192 Effects \u2192 Background: Off, and Border: Off. The white "
      "comes from the box shape underneath, so the card itself stays see-through.",
      "Format pane \u2192 General \u2192 Properties \u2192 Position: set Horizontal (X) and "
      "Vertical (Y) to 14 and 182 exactly, or the card will not sit square inside its box."],
     ),

    ("Overview", "Card", "Consumables",
     [("Fields", ["Ticker Consumables Rs Cr"])],
     (14, 242, 156, 58),
     "Panel figure, sitting inside the white box. It reads the latest month that has data "
     "and ignores every slicer on the page, because stock is a level, not something you "
     "add up across months.",
     ["Format pane \u2192 Callout value \u2192 Display units: None, Value decimal places: 1, "
      "Font: Arial, Font size: 20, Bold: On, Colour: #1F2A24 (near-black, because the box "
      "behind it is white now). Display units None is what stops Power BI writing 2.5K "
      "instead of 2,539.4.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 10, Colour: #14532D, "
      "Text: the title above.",
      "Format pane \u2192 General \u2192 Effects \u2192 Background: Off, and Border: Off. The white "
      "comes from the box shape underneath, so the card itself stays see-through.",
      "Format pane \u2192 General \u2192 Properties \u2192 Position: set Horizontal (X) and "
      "Vertical (Y) to 14 and 242 exactly, or the card will not sit square inside its box."],
     ),

    ("Overview", "Card", "1900 Jaipur Module",
     [("Fields", ["Ticker 1900 Rs Cr"])],
     (14, 332, 156, 58),
     "Panel figure, sitting inside the white box. It reads the latest month that has data "
     "and ignores every slicer on the page, because stock is a level, not something you "
     "add up across months.",
     ["Format pane \u2192 Callout value \u2192 Display units: None, Value decimal places: 1, "
      "Font: Arial, Font size: 20, Bold: On, Colour: #1F2A24 (near-black, because the box "
      "behind it is white now). Display units None is what stops Power BI writing 2.5K "
      "instead of 2,539.4.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 10, Colour: #14532D, "
      "Text: the title above.",
      "Format pane \u2192 General \u2192 Effects \u2192 Background: Off, and Border: Off. The white "
      "comes from the box shape underneath, so the card itself stays see-through.",
      "Format pane \u2192 General \u2192 Properties \u2192 Position: set Horizontal (X) and "
      "Vertical (Y) to 14 and 332 exactly, or the card will not sit square inside its box."],
     ),

    ("Overview", "Card", "1902 Dholera Module",
     [("Fields", ["Ticker 1902 Rs Cr"])],
     (14, 392, 156, 58),
     "Panel figure, sitting inside the white box. It reads the latest month that has data "
     "and ignores every slicer on the page, because stock is a level, not something you "
     "add up across months.",
     ["Format pane \u2192 Callout value \u2192 Display units: None, Value decimal places: 1, "
      "Font: Arial, Font size: 20, Bold: On, Colour: #1F2A24 (near-black, because the box "
      "behind it is white now). Display units None is what stops Power BI writing 2.5K "
      "instead of 2,539.4.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 10, Colour: #14532D, "
      "Text: the title above.",
      "Format pane \u2192 General \u2192 Effects \u2192 Background: Off, and Border: Off. The white "
      "comes from the box shape underneath, so the card itself stays see-through.",
      "Format pane \u2192 General \u2192 Properties \u2192 Position: set Horizontal (X) and "
      "Vertical (Y) to 14 and 392 exactly, or the card will not sit square inside its box."],
     ),

    ("Overview", "Card", "1905 Dholera Cell",
     [("Fields", ["Ticker 1905 Rs Cr"])],
     (14, 452, 156, 58),
     "Panel figure, sitting inside the white box. It reads the latest month that has data "
     "and ignores every slicer on the page, because stock is a level, not something you "
     "add up across months.",
     ["Format pane \u2192 Callout value \u2192 Display units: None, Value decimal places: 1, "
      "Font: Arial, Font size: 20, Bold: On, Colour: #1F2A24 (near-black, because the box "
      "behind it is white now). Display units None is what stops Power BI writing 2.5K "
      "instead of 2,539.4.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 10, Colour: #14532D, "
      "Text: the title above.",
      "Format pane \u2192 General \u2192 Effects \u2192 Background: Off, and Border: Off. The white "
      "comes from the box shape underneath, so the card itself stays see-through.",
      "Format pane \u2192 General \u2192 Properties \u2192 Position: set Horizontal (X) and "
      "Vertical (Y) to 14 and 452 exactly, or the card will not sit square inside its box."],
     ),

    ("Overview", "Card", "Total",
     [("Fields", ["Ticker Rs Cr"])],
     (14, 528, 156, 62),
     "Panel figure, sitting inside the white box. It reads the latest month that has data "
     "and ignores every slicer on the page, because stock is a level, not something you "
     "add up across months.",
     ["Format pane \u2192 Callout value \u2192 Display units: None, Value decimal places: 1, "
      "Font: Arial, Font size: 22, Bold: On, Colour: #1F2A24 (near-black, because the box "
      "behind it is white now). Display units None is what stops Power BI writing 2.5K "
      "instead of 2,539.4.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 10, Colour: #14532D, "
      "Text: the title above.",
      "Format pane \u2192 General \u2192 Effects \u2192 Background: Off, and Border: Off. The white "
      "comes from the box shape underneath, so the card itself stays see-through.",
      "Format pane \u2192 General \u2192 Properties \u2192 Position: set Horizontal (X) and "
      "Vertical (Y) to 14 and 528 exactly, or the card will not sit square inside its box."],
     ),

    ("Overview", "Card", "Change since Last Month",
     [("Fields", ["Ticker Change Text"])],
     (14, 592, 156, 58),
     "One line reading, for example, +12.4 Rs Cr. (+2.1%) \u2014 the amount and the percentage "
     "together, each labelled, so nobody has to ask which is which. Same white box as Total, "
     "directly under it.",
     ["Format pane \u2192 Callout value \u2192 Font: Arial, Font size: 12, Bold: On, "
      "Colour: #1F2A24. Twelve rather than fifteen, because this line carries the amount and "
      "the percentage together and the panel is narrower now. Green and red would fight with "
      "the white box, so the sign carries the meaning instead.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 10, Colour: #14532D, "
      "Text: Change since Last Month.",
      "Format pane \u2192 General \u2192 Effects \u2192 Background: Off, Border: Off.",
      "The measure writes its own + or \u2212 sign and both units, so leave Display units alone."],
     ),

    ("Overview", "Card", "As on",
     [("Fields", ["As On Text"])],
     (14, 652, 156, 28),
     "Says which month the whole panel is showing, so a reader never has to guess.",
     ["Format pane \u2192 Callout value \u2192 Font: Arial, Font size: 10, Colour: #4B5563.",
      "Format pane \u2192 General \u2192 Title: Off \u2014 the sentence says it all.",
      "Format pane \u2192 General \u2192 Effects \u2192 Background: Off, Border: Off."],
     ),

    # ---- Overview controls ---------------------------------------------------------------
    ("Overview", "Slicer", "By month / By quarter",
     [("Field", ["Period[Period]"])],
     (200, 20, 216, 52),
     "The toggle. Period is the field parameter you made in the New tab; picking By quarter "
     "swaps the chart and the table from months to quarters and averages the month-ends.",
     ["Format pane \u2192 Slicer settings \u2192 Options \u2192 Style: Tile, so it reads as two buttons "
      "rather than a list.",
      "Format pane \u2192 Slicer settings \u2192 Selection: switch ON 'Single select' so exactly one "
      "of the two is always chosen.",
      "Format pane \u2192 Values \u2192 Font: Arial, Font size: 10, Colour: #14532D.",
      "Format pane \u2192 General \u2192 Title: Off."]),

    ("Overview", "Slicer", "Months (leave empty for the last 5)",
     [("Field", ["dimDate[MonthName]"])],
     (424, 20, 268, 52),
     "Tick nothing and the chart shows the last 5 months by itself. Tick more than 5 and it "
     "shows the 5 most recent of your ticks. In quarter mode this is the quarter picker.",
     ["Format pane \u2192 Slicer settings \u2192 Options \u2192 Style: Dropdown.",
      "Format pane \u2192 Slicer settings \u2192 Selection: switch OFF 'Multi-select with CTRL' so "
      "ticking several needs no keyboard.",
      "Format pane \u2192 Values \u2192 Font: Arial, Font size: 10, Colour: #1F2A24.",
      "Format pane \u2192 General \u2192 Title \u2192 Font size: 10, Colour: #14532D."]),

    ("Overview", "Slicer", "Plant",
     [("Field", ["dimPlant[Plant]"])],
     (700, 20, 262, 52),
     "Filters the history and the donuts. The panel on the left ignores it on purpose.",
     ["Format pane \u2192 Slicer settings \u2192 Options \u2192 Style: Dropdown.",
      "Format pane \u2192 Values \u2192 Font: Arial, Font size: 10, Colour: #1F2A24.",
      "Format pane \u2192 General \u2192 Title \u2192 Font size: 10, Colour: #14532D."]),

    ("Overview", "Slicer", "Type",
     [("Field", ["dimCategory[Category]"])],
     (970, 20, 294, 52),
     "RM, FG or consumables.",
     ["Format pane \u2192 Slicer settings \u2192 Options \u2192 Style: Dropdown.",
      "Format pane \u2192 Values \u2192 Font: Arial, Font size: 10, Colour: #1F2A24.",
      "Format pane \u2192 General \u2192 Title \u2192 Font size: 10, Colour: #14532D."]),

    # ---- Overview history: chart above, the same numbers as a table below ----------------
    ("Overview", "Stacked column chart", "Inventory by Month (Rs Cr.)",
     [("X-axis", ["Period[Period]"]),
      ("Y-axis", ["Inventory Rs Cr"]),
      ("Legend", ["dimCategory[Category]"]),
      ("Filters", ["In Window  \u2192  is 1"])],
     (200, 88, 700, 336),
     "Five months side by side, or four quarters if the toggle is set to By quarter, in "
     "which case each bar is the average of that quarter's month-ends. The In Window filter "
     "is what keeps it to five (or four) without you having to prune the slicer.",
     ["Format pane \u2192 Data labels: On, Font: Arial, Font size: 9, Bold: On, Colour: "
      "#FFFFFF, Display units: None, Value decimal places: 1. Every bar segment then prints "
      "its own number, in white because it is printed on top of the colour.",
      "Format pane \u2192 Data labels \u2192 Options \u2192 Position: Inside center, Orientation: "
      "Horizontal.",
      "Format pane \u2192 Total labels: On, Font: Arial, Font size: 9, Bold: On, Colour: "
      "#14532D \u2014 that prints the whole month's figure above each bar, on the white card, so "
      "this one is dark green rather than white.",
      "Format pane \u2192 General \u2192 Title \u2192 use the measure instead of typed words: click the "
      "fx button beside Text, choose 'Field value', and pick the measure Period Title. The "
      "heading then reads 'Inventory by Month (Rs Cr.)' or 'Inventory by Quarter (Rs Cr., "
      "Average of Month-Ends)' to match the toggle.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 12, Colour: #14532D."]),

    ("Overview", "Matrix", "Inventory by Month (Rs Cr.)",
     [("Rows", ["dimCategory[Category]"]),
      ("Columns", ["Period[Period]"]),
      ("Values", ["Inventory Rs Cr"]),
      ("Filters", ["In Window  \u2192  is 1"])],
     (200, 432, 700, 136),
     "The same five columns as the chart directly above it, for readers who want the "
     "figures rather than the shape. Only as tall as its four rows, so no white gap is left "
     "under it.",
     ["Format pane \u2192 Row headers \u2192 Stepped layout: Off.",
      "Format pane \u2192 Subtotals \u2192 Row subtotals: On, Column subtotals: Off. Here the total "
      "row earns its place, because the three types add up to the month.",
      "Format pane \u2192 Values \u2192 Font: Arial, Font size: 10, Colour: #1F2A24.",
      "Format pane \u2192 Column headers \u2192 Font: Arial, Font size: 10, Colour: #14532D."]),

    ("Overview", "Line and clustered column chart",
     "Total Inventory by Month, Last 12 Months (Rs Cr. and % vs Last Month)",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Column y-axis", ["Value \u20b9 Cr"]),
      ("Line y-axis", ["Value \u20b9 Cr % vs LM"]),
      ("Filters", ["In Last 12  \u2192  is 1"])],
     (200, 576, 700, 130),
     "The long view, under the table: one bar per month for the last twelve months that have "
     "data, or fewer if that is all there is. Two numbers on every month \u2014 the bar prints the "
     "crore figure, the line above it prints the change on the month before as a percentage. "
     "Each bar is that month's closing stock on its own, so nothing here is ever added across "
     "months.",
     ["This one must ignore the two controls at the top, or it would shrink back to five "
      "months. Click the 'By Month / By Quarter' slicer once, then ribbon Format \u2192 Edit "
      "interactions; small icons appear on every other visual. On this chart click the "
      "circle-with-a-line (None). Do the same after selecting the 'Months' slicer. Leave "
      "Plant and Type set to filter, so those two still work on it.",
      "Format pane \u2192 Data labels: On. Then open 'Apply settings to' \u2192 Series and pick "
      "'Value \u20b9 Cr': Font: Arial, Font size: 8, Bold: On, Colour: #14532D, Display units: "
      "None, Value decimal places: 0, Position: Inside end.",
      "Still under Data labels, switch 'Apply settings to' \u2192 Series to "
      "'Value \u20b9 Cr % vs LM': Font: Arial, Font size: 8, Colour: #6B7280, Value decimal "
      "places: 0, Position: Above. That is the second number you asked for \u2014 the percentage "
      "sits over the bar, the crore figure sits inside it, so the two never collide.",
      "Format pane \u2192 Y-axis: Off, and Secondary y-axis: Off. Both numbers are printed on "
      "the chart, so two scales up the sides would only eat the height.",
      "Format pane \u2192 X-axis \u2192 Values \u2192 Font: Arial, Font size: 8, Colour: #1F2A24, "
      "Concatenate labels: Off, and Maximum height: 20%.",
      "Format pane \u2192 X-axis \u2192 Inner padding: 30%, and Format pane \u2192 General \u2192 "
      "Properties \u2192 Padding: Left 12, Right 12. The padding is what stops the first and last "
      "bar touching the sides of the card, and it pulls both edges in by the same amount.",
      "Format pane \u2192 Columns \u2192 Colour: #2E7D46. Format pane \u2192 Lines \u2192 Colour: "
      "#9AA79F, Stroke width: 1, Show marker: On, Marker size: 3 \u2014 the line is only there to "
      "carry its labels, so it is deliberately quiet.",
      "Format pane \u2192 Legend: Off. Two series, both labelled on the chart, so a key would "
      "repeat what the labels already say.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 11, Colour: #14532D."]),

    # ---- Overview donuts -----------------------------------------------------------------
    ("Overview", "Donut chart", "Share by Type (%)",
     [("Legend", ["dimCategory[Category]"]),
      ("Values", ["Inventory Rs Cr"])],
     (916, 88, 348, 306),
     "RM against FG against consumables, as a percentage of the selected months.",
     ["Format pane \u2192 Detail labels \u2192 Label contents: Percent of total, Font: Arial, Font "
      "size: 10, Colour: #1F2A24, Value decimal places: 1.",
      "Format pane \u2192 Detail labels \u2192 Position: Outside, so a thin slice still shows its "
      "percentage.",
      "Format pane \u2192 Legend \u2192 Position: Bottom center, Font size: 9.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 12, Colour: #14532D."]),

    ("Overview", "Donut chart", "Share by Plant (%)",
     [("Legend", ["dimPlant[Plant]"]),
      ("Values", ["Inventory Rs Cr"])],
     (916, 402, 348, 304),
     "The same money split by plant instead of by type.",
     ["Format pane \u2192 Detail labels \u2192 Label contents: Percent of total, Font: Arial, Font "
      "size: 10, Colour: #1F2A24, Value decimal places: 1.",
      "Format pane \u2192 Detail labels \u2192 Position: Outside.",
      "Format pane \u2192 Legend \u2192 Position: Bottom center, Font size: 9.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 12, Colour: #14532D."]),

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


# ---- headings: Title Case everywhere ------------------------------------------------------
# Every word gets a capital except the short joining words, and even those get one when they
# open a heading or follow a dash, a colon or a middle dot. Done here, once, so a title can
# never disagree between the guide, the steps and the generated project.
SMALL = {"a", "an", "and", "as", "at", "but", "by", "for", "from", "in", "into", "nor",
         "of", "on", "or", "per", "since", "the", "to", "vs", "via", "with"}
_BREAK = {"\u2014", "\u2013", "-", "\u00b7", ":", "|", "/"}


def title_case(text):
    if not text:
        return text
    words = text.split(" ")
    out, opening = [], True
    for w in words:
        if w in _BREAK or w.endswith(("\u2014", ":")):
            out.append(w)
            opening = True
            continue
        core = w.lstrip("(\u201c'\u2018")
        lead = w[:len(w) - len(core)]
        bare = core.rstrip(")\u201d'\u2019.,%")
        tail = core[len(bare):]
        low = bare.lower()
        if bare[:1].isupper():                            # already capital: never undo it
            fixed = bare
        elif low in SMALL and not opening:
            fixed = low
        elif bare[:1].isalpha():
            fixed = bare[0].upper() + bare[1:]
        else:
            fixed = bare
        out.append(lead + fixed + tail)
        opening = False
    return " ".join(out)


CARDS = [(m, x, y, w, h, title_case(t)) for m, x, y, w, h, t in CARDS]
SLICERS = [(f, x, y, w, h, title_case(t)) for f, x, y, w, h, t in SLICERS]
DECOR = [(p, k, title_case(t), x, y, w, h, n) for p, k, t, x, y, w, h, n in DECOR]
VISUALS = [(p, k, title_case(t), wells, pos, why, extra)
           for p, k, t, wells, pos, why, extra in VISUALS]
