"""Single source of truth for the report pages.

steps.py turns this into (a) the guided click-by-click steps on the web page and
(b) the PART 4 section of BUILD_GUIDE.md, so the two can never disagree.
"""

CANVAS = (1280, 720)

# Checks is last on purpose: the five report pages come first, and it is the page you
# open when a figure looks wrong, so a refresh problem names itself.
PAGES = ["Overview", "Summary", "FG", "RM", "Detail", "Checks"]

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

# Overview and Summary carry their own controls, so they are built visual by visual.
# No page uses the old card-and-slicer band any more: all five carry their own controls.
BAND_PAGES = []

# ---- header band for RM -------------------------------------------------------------
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
      "Font: Arial, Font size: 16, Bold: On, Colour: #1F2A24 (near-black, because the box "
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
      "Font: Arial, Font size: 16, Bold: On, Colour: #1F2A24 (near-black, because the box "
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
      "Font: Arial, Font size: 16, Bold: On, Colour: #1F2A24 (near-black, because the box "
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
      "Font: Arial, Font size: 16, Bold: On, Colour: #1F2A24 (near-black, because the box "
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
      "Font: Arial, Font size: 16, Bold: On, Colour: #1F2A24 (near-black, because the box "
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
      "Font: Arial, Font size: 16, Bold: On, Colour: #1F2A24 (near-black, because the box "
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
    ("Overview", "Slicer", "Months (leave empty for March plus the last 4)",
     [("Field", ["dimDate[MonthName]"])],
     (192, 8, 268, 76),
     "Tick nothing and you get March — the year-end close — followed by the last four "
     "months that have data, five columns in all, or fewer early in the year: in April just "
     "March and April. Tick your own months and they replace that, up to the 5 most recent of "
     "your ticks. Months are the only period on this page: the columns and the bars are "
     "dimDate[MonthName] itself, not a switchable parameter.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane \u2192 Slicer settings \u2192 Options \u2192 Style: Dropdown.",
      "Format pane \u2192 Slicer settings \u2192 Selection: switch OFF 'Multi-select with CTRL' so "
      "ticking several needs no keyboard.",
      "Format pane \u2192 Values \u2192 Font: Arial, Font size: 10, Colour: #1F2A24.",
      "Format pane \u2192 General \u2192 Title \u2192 Font size: 10, Colour: #14532D."]),

    ("Overview", "Slicer", "Plant",
     [("Field", ["dimPlant[Plant]"])],
     (468, 8, 262, 76),
     "Filters the history and the donuts. The panel on the left ignores it on purpose.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane \u2192 Slicer settings \u2192 Options \u2192 Style: Dropdown.",
      "Format pane \u2192 Values \u2192 Font: Arial, Font size: 10, Colour: #1F2A24.",
      "Format pane \u2192 General \u2192 Title \u2192 Font size: 10, Colour: #14532D."]),

    ("Overview", "Slicer", "Type",
     [("Field", ["dimCategory[Category]"])],
     (738, 8, 294, 76),
     "RM, FG or consumables.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane \u2192 Slicer settings \u2192 Options \u2192 Style: Dropdown.",
      "Format pane \u2192 Values \u2192 Font: Arial, Font size: 10, Colour: #1F2A24.",
      "Format pane \u2192 General \u2192 Title \u2192 Font size: 10, Colour: #14532D."]),

    # ---- Overview history: chart above, the same numbers as a table below ----------------
    ("Overview", "Stacked column chart", "Inventory by Month (Rs Cr.)",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Y-axis", ["Inventory Rs Cr"]),
      ("Legend", ["dimCategory[Category]"]),
      ("Filters", ["In Window  \u2192  is 1"])],
     (200, 88, 700, 336),
     "Five months side by side. The In Window filter is what keeps it to five without you "
     "having to prune the slicer.",
     ["Format pane \u2192 Data labels: Off. The segment figures are deliberately not printed: "
      "the consumables slice is too thin to hold one, so some months showed a number and "
      "others did not. Hover a segment for RM, FG or consumables in that month, and click it "
      "to filter the rest of the page to it.",
      "Format pane \u2192 Total labels: On, Font: Arial, Font size: 9, Bold: On, Colour: "
      "#14532D, Display units: None, Value decimal places: 1 \u2014 the month total above each "
      "bar is the only printed number, dark green because it sits on the white card.",
      "Drag Share of Total % into the visual's Tooltips well, so hovering gives the share as "
      "well as the figure.",
      "Format pane \u2192 General \u2192 Title \u2192 Text: type the heading above. It is typed "
      "words, not a measure \u2014 the axis is always months, so the heading never has to change.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 12, Colour: #14532D."]),

    ("Overview", "Matrix", "Inventory by Month (Rs Cr.)",
     [("Rows", ["dimCategory[Category]"]),
      ("Columns", ["dimDate[MonthName]"]),
      ("Values", ["Inventory Rs Cr"]),
      ("Filters", ["In Window  \u2192  is 1"])],
     (200, 432, 700, 136),
     "The same five columns as the chart directly above it, for readers who want the "
     "figures rather than the shape. Only as tall as its four rows, so no white gap is left "
     "under it. Left to itself the first column is always March \u2014 the year-end close \u2014 and "
     "the four columns after it are the last four months that have data, so in July you get "
     "Mar, Apr, May, Jun, Jul and in April just Mar and Apr. Tick five months in the picker "
     "and your ticks replace that entirely. That behaviour lives in the In Window filter, so "
     "the chart above obeys it too.",
     ["Format pane \u2192 Row headers \u2192 Stepped layout: Off.",
      "Format pane \u2192 Subtotals \u2192 Row subtotals: On, Column subtotals: Off. Here the total "
      "row earns its place, because the three types add up to the month.",
      "Format pane \u2192 Values \u2192 Font: Arial, Font size: 10, Colour: #1F2A24.",
      "Format pane \u2192 Column headers \u2192 Font: Arial, Font size: 10, Colour: #14532D."]),

    ("Overview", "Line and clustered column chart",
     "Total Inventory by Month, Last 12 Months (MW and % vs Last Month)",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Column y-axis", ["MW"]),
      ("Line y-axis", ["MW % vs LM"]),
      ("Filters", ["In Last 12  \u2192  is 1"])],
     (200, 576, 700, 130),
     "The long view, under the table: one bar per month for the last twelve months that have "
     "data, or fewer if that is all there is. Two numbers on every month \u2014 the bar prints the "
     "megawatts held, the line above it prints the change on the month before as a percentage. "
     "It is in MW rather than rupees on purpose: this strip is about how much product is "
     "sitting there, which prices cannot flatter. "
     "Each bar is that month's closing stock on its own, so nothing here is ever added across "
     "months.",
     ["This one must ignore the two controls at the top, or it would shrink back to five "
      "months. Click the 'Months' slicer once, then ribbon Format \u2192 Edit interactions; "
      "small icons appear on every other visual. On this chart click the circle-with-a-line "
      "(None). Leave Plant and Type set to filter, so those two still work on it.",
      "Format pane \u2192 Data labels: On. Then open 'Apply settings to' \u2192 Series and pick "
      "MW: Font: Arial, Font size: 8, Bold: On, Colour: #FFFFFF, Display units: "
      "None, Value decimal places: 1, Position: Inside end \u2014 white, because this number is "
      "printed on the green bar.",
      "Still under Data labels, switch 'Apply settings to' \u2192 Series to "
      "'MW % vs LM': Font: Arial, Font size: 8, Colour: #14532D, Value decimal "
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

    # ---- Overview donuts: what the latest month is actually made of --------------------
    ("Overview", "Donut chart", "FG Components, Latest Month (Rs Cr. and % Share)",
     [("Legend", ["dimNature[Nature]"]),
      ("Values", ["Value \u20b9 Cr"]),
      ("Filters", ["dimCategory[Category]  \u2192  is FG",
                   "In Latest Month  \u2192  is 1"])],
     (916, 88, 348, 306),
     "What the finished goods are made of in the latest month that has data \u2014 the module "
     "technologies, largest slice first. It is pinned to the latest month by the In Latest "
     "Month filter, because adding one month-end of stock to another would be meaningless; "
     "the Plant and Type slicers still narrow it.",
     ["Format pane \u2192 Detail labels \u2192 Label contents: Category, percent of total, Font: "
      "Arial, Font size: 9, Colour: #1F2A24, Value decimal places: 1.",
      "Format pane \u2192 Detail labels \u2192 Position: Outside, so a thin technology still shows "
      "its percentage.",
      "Format pane \u2192 Legend \u2192 Position: Bottom center, Font size: 9.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 12, Colour: #14532D.",
      "Right-click a slice \u2192 Drill through \u2192 Detail to see the materials inside that "
      "technology."]),

    ("Overview", "Donut chart", "RM Components, Latest Month (Rs Cr. and % Share)",
     [("Legend", ["dimNature[Nature]"]),
      ("Values", ["Value \u20b9 Cr"]),
      ("Filters", ["dimCategory[Category]  \u2192  is RM",
                   "In Latest Month  \u2192  is 1"])],
     (916, 402, 348, 304),
     "The same for raw materials in the latest month \u2014 cell, glass, frame, POE, packing and "
     "the rest \u2014 so the two donuts read as a pair: what the finished stock is, and what the "
     "raw stock is.",
     ["Format pane \u2192 Detail labels \u2192 Label contents: Category, percent of total, Font: "
      "Arial, Font size: 9, Colour: #1F2A24, Value decimal places: 1.",
      "Format pane \u2192 Detail labels \u2192 Position: Outside.",
      "Format pane \u2192 Legend \u2192 Position: Bottom center, Font size: 9.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 12, Colour: #14532D.",
      "If the legend runs to more than about eight natures, Format pane \u2192 Legend \u2192 Font "
      "size: 8 and it still fits; the smallest natures are grouped under Others by the query, "
      "so it should not."]),

    # ---- Summary: TB | MB5B | Difference as master columns, plants as master rows -------
    # Its own controls, exactly like Overview. The periods under each master column are
    # months: dimDate[MonthName] itself, so nothing has to swap a field for them to appear.
    ("Summary", "Slicer", "Months (leave empty for the last 4)",
     [("Field", ["dimDate[MonthName]"])],
     (16, 8, 300, 76),
     "Tick nothing and the matrix shows the last 4 months under each master column. Tick "
     "the months you want and it shows those, up to twelve \u2014 tick more than twelve and it "
     "keeps the twelve most recent of your ticks, because 3 master columns \u00d7 12 months is "
     "already 36 columns of figures.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane \u2192 Slicer settings \u2192 Options \u2192 Style: Dropdown.",
      "Format pane \u2192 Slicer settings \u2192 Selection: switch OFF 'Multi-select with CTRL' so "
      "ticking several needs no keyboard.",
      "Format pane \u2192 Values \u2192 Font: Arial, Font size: 10, Colour: #1F2A24.",
      "Format pane \u2192 General \u2192 Title \u2192 Font size: 10, Colour: #14532D."]),

    ("Summary", "Slicer", "Quarters (leave empty for the last 4)",
     [("Field", ["dimDate[Quarter]"])],
     (332, 8, 240, 76),
     "A second, coarser filter: tick Q1 and only that quarter's months are left for the "
     "matrices and the charts to show. Leave it empty to see every month.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane \u2192 Slicer settings \u2192 Options \u2192 Style: Dropdown.",
      "Format pane \u2192 Slicer settings \u2192 Selection: switch OFF 'Multi-select with CTRL'.",
      "Format pane \u2192 Values \u2192 Font: Arial, Font size: 10, Colour: #1F2A24.",
      "Format pane \u2192 General \u2192 Title \u2192 Font size: 10, Colour: #14532D."]),

    ("Summary", "Slicer", "Plant",
     [("Field", ["dimPlant[Plant]"])],
     (588, 8, 220, 76),
     "Narrows both matrices to one plant when you want to read it on its own.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane \u2192 Slicer settings \u2192 Options \u2192 Style: Dropdown.",
      "Format pane \u2192 Values \u2192 Font: Arial, Font size: 10, Colour: #1F2A24.",
      "Format pane \u2192 General \u2192 Title \u2192 Font size: 10, Colour: #14532D."]),

    ("Summary", "Slicer", "Type",
     [("Field", ["dimCategory[Category]"])],
     (824, 8, 208, 76),
     "RM, FG or consumables, when you want the reconciliation for one of them only.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane \u2192 Slicer settings \u2192 Options \u2192 Style: Dropdown.",
      "Format pane \u2192 Values \u2192 Font: Arial, Font size: 10, Colour: #1F2A24.",
      "Format pane \u2192 General \u2192 Title \u2192 Font size: 10, Colour: #14532D."]),

    ("Summary", "Matrix",
     "Inventory (TB) · Inventory (MB5B) · Difference by Plant (Rs Cr.)",
     [("Rows", ["dimPlant[Plant]", "dimCategory[Category]"]),
      ("Columns", ["dimMetric[Metric]", "dimDate[MonthName]"]),
      ("Values", ["Summary Value Rs Cr"]),
      ("Filters", ["In Summary Window  →  is 1"])],
     (16, 88, 1248, 212),
     "The whole reconciliation in one grid: three master columns \u2014 Inventory (TB), "
     "Inventory (MB5B), Difference \u2014 with the periods under each, one row per plant "
     "(Jaipur Module, Dholera Module, Dholera Cell) opening into RM, FG and Consumables, "
     "and a total for each plant. Everything in crore rupees.",
     ["Order of the two Columns fields matters: dimMetric[Metric] FIRST, then "
      "dimDate[MonthName]. That is what makes TB / MB5B / Difference the master columns "
      "with the months nested inside; the other way round gives you months with three "
      "metrics inside each.",
      "Format pane \u2192 Row headers \u2192 Stepped layout: Off, so Plant and Type get a column "
      "each instead of being indented into one.",
      "Format pane \u2192 Row headers \u2192 +/- icons: On \u2014 that is the click-to-expand control on "
      "each plant.",
      "Format pane \u2192 Subtotals \u2192 Row subtotals: On, and switch ON 'Per row level' so each "
      "plant shows its own total. Column subtotals: Off.",
      "Format pane \u2192 Subtotals \u2192 Grand total: Off on this matrix. The total of the totals, "
      "split by RM / FG / Consumables, is the second matrix underneath \u2014 a matrix can only "
      "give one flat grand total row, so the split has to be its own visual.",
      "Colour the differences: in the Values box click the small down-arrow next to "
      "Summary Value Rs Cr, click 'Conditional formatting', then 'Background color'. Set "
      "Format style to Diverging, tick 'Add a middle colour', set the middle number to 0, "
      "and make both the Minimum and Maximum colours red. A difference either direction is "
      "equally wrong, so both ends are red.",
      "Right-click any plant row, click 'Expand', then 'All', so RM, FG and Consumables "
      "show under every plant. Then press Ctrl+S \u2014 Power BI remembers it.",
      "Format pane \u2192 General \u2192 Title \u2192 Text: type the heading above, and leave the fx "
      "button alone. The columns are always months, so the heading is always right.",
      "With twelve periods ticked this is 36 columns of figures, so a scrollbar appears "
      "along the bottom of the matrix. That is normal: scroll it sideways, or untick "
      "periods until it fits."]),

    ("Summary", "Matrix", "Total across All Plants by Type (Rs Cr.)",
     [("Rows", ["dimCategory[Category]"]),
      ("Columns", ["dimMetric[Metric]", "dimDate[MonthName]"]),
      ("Values", ["Summary Value Rs Cr"]),
      ("Filters", ["In Summary Window  →  is 1"])],
     (16, 308, 1248, 112),
     "The bottom block: the same three master columns, but every plant added together \u2014 one "
     "row for RM, one for FG, one for Consumables, so you can read total RM across all "
     "plants at a glance, and a Total row under them which is the total inventory.",
     ["Same column order as the matrix above: dimMetric[Metric] first, then "
      "dimDate[MonthName]. Keep the same months ticked, so the two matrices line up column "
      "for column.",
      "Format pane \u2192 Row headers \u2192 Stepped layout: Off.",
      "Format pane \u2192 Subtotals \u2192 Row subtotals: On \u2014 that bottom row is the total of the "
      "totals, the whole inventory. Column subtotals: Off.",
      "Format pane \u2192 Row headers \u2192 Font: Arial, Font size: 9, Bold: On, so this block reads "
      "as the summary of the one above rather than as more detail.",
      "This matrix has no Plant field on purpose. Leave the Plant slicer on 'All' when you "
      "want the across-all-plants figure \u2014 picking one plant filters this block too."]),

    ("Summary", "Clustered column chart",
     "Inventory (TB) vs Inventory (MB5B) by Month (Rs Cr.)",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Y-axis", ["TB Inventory Rs Cr", "Inventory Rs Cr"]),
      ("Filters", ["In Summary Window  \u2192  is 1"])],
     (16, 428, 616, 112),
     "The books against the stock report, two bars per period: the same figures as the "
     "matrix above, but you can see a gap opening without reading a single number. Same "
     "periods as the matrices, because it carries the same filter.",
     ["Both measures go in the Y-axis, TB Inventory Rs Cr first \u2014 that fixes the order of "
      "the two bars, so the books are always the left-hand one.",
      "Format pane \u2192 Data labels: On, Font: Arial, Font size: 8, Colour: #1F2A24, Display "
      "units: None, Value decimal places: 0, Position: Inside end.",
      "Format pane \u2192 Y-axis: Off. The label on each bar is the number, so a scale up the "
      "side only eats the height.",
      "Format pane \u2192 X-axis \u2192 Values \u2192 Font: Arial, Font size: 8, Colour: #1F2A24.",
      "Format pane \u2192 Legend \u2192 Position: Top center, Font: Arial, Font size: 8. Two "
      "measures here, so the legend is the only thing naming them \u2014 leave it on.",
      "Format pane \u2192 X-axis \u2192 Inner padding: 30%, and General \u2192 Properties \u2192 Padding: "
      "Left 12, Right 12, so the first and last bar keep off the card edges.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 11, Colour: #14532D."]),

    ("Summary", "Line and clustered column chart",
     "Difference by Month (Rs Cr. and % of TB)",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Column y-axis", ["Difference Inventory Rs Cr"]),
      ("Line y-axis", ["Difference Inventory %"]),
      ("Filters", ["In Summary Window  \u2192  is 1"])],
     (648, 428, 616, 112),
     "The question the reconciliation is really asking: is the gap widening or closing. The "
     "bar is the difference in crore rupees, the line above it the same difference as a "
     "percentage of the trial balance, so a small gap on a big month reads as small.",
     ["Format pane \u2192 Columns \u2192 Colour \u2192 fx \u2192 Format style: Rules, and colour any value "
      "below 0 red. A difference either direction is equally wrong, so red both ways.",
      "Format pane \u2192 Data labels: On. Then 'Apply settings to' \u2192 Series: Difference "
      "Inventory Rs Cr \u2014 Font: Arial, Font size: 8, Colour: #1F2A24, Display units: None, "
      "Value decimal places: 2, Position: Inside end.",
      "Still under Data labels, switch 'Apply settings to' \u2192 Series to Difference "
      "Inventory %: Font: Arial, Font size: 8, Colour: #14532D, Value decimal places: 1, "
      "Position: Above. Two numbers per period, and they cannot collide.",
      "Format pane \u2192 Y-axis: Off, Secondary y-axis: Off. Both numbers are printed on the "
      "chart already.",
      "Format pane \u2192 X-axis \u2192 Values \u2192 Font: Arial, Font size: 8, Colour: #1F2A24.",
      "Format pane \u2192 Lines \u2192 Colour: #9AA79F, Stroke width: 1, Markers: On, Marker size: 3.",
      "Format pane \u2192 Legend: Off \u2014 the title says which is which, and 144 pixels of height "
      "has none to spare.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 11, Colour: #14532D."]),

    # ---- FG: its own controls, then MW | Rs Cr. | Days as master columns ---------------
    ("FG", "Slicer", "Months (leave empty for the last 4)",
     [("Field", ["dimDate[MonthName]"])],
     (16, 8, 300, 76),
     "Which months appear under each master column. Tick nothing and it shows the last four "
     "with data; tick your own and it shows those, up to twelve.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane → Slicer settings → Options → Style: Dropdown.",
      "Format pane → Slicer settings → Selection → switch OFF 'Multi-select with CTRL', so "
      "months can be ticked by clicking.",
      "Format pane → Values → Font: Arial, Font size: 10, Colour: #1F2A24.",
      "Do not sync this one either. Both FG matrices read it, and nothing else should."]),

    ("FG", "Slicer", "Quarters (leave empty for the last 4)",
     [("Field", ["dimDate[Quarter]"])],
     (332, 8, 240, 76),
     "A coarser filter over the same months: tick Q1 and only April, May and June are left "
     "for the two matrices to show. Leave it empty to see every month.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane → Slicer settings → Options → Style: Dropdown.",
      "Format pane → Slicer settings → Selection → 'Multi-select with CTRL': Off.",
      "Format pane → Values → Font: Arial, Font size: 10, Colour: #1F2A24.",
      "It filters the months rather than replacing them, so the columns stay months."]),

    ("FG", "Slicer", "Plant",
     [("Field", ["dimPlant[Plant]"])],
     (588, 8, 220, 76),
     "One plant, or all of them. It filters the technology matrix and all three charts, so "
     "picking Dholera Cell turns the page into a Dholera Cell page.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane → Slicer settings → Options → Style: Dropdown.",
      "Format pane → Values → Font: Arial, Font size: 10, Colour: #1F2A24."]),

    ("FG", "Slicer", "Technology",
     [("Field", ["dimNature[Nature]"])],
     (824, 8, 208, 76),
     "One module technology, when you want the page to be about that technology only.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane → Slicer settings → Options → Style: Dropdown.",
      "Format pane → Values → Font: Arial, Font size: 10, Colour: #1F2A24."]),

    ("FG", "Matrix", "FG by Plant — MW · Rs Cr. · Days",
     [("Rows", ["dimPlant[Plant]"]),
      ("Columns", ["dimMeasure[Measure]", "dimDate[MonthName]"]),
      ("Values", ["Unit Value by Period"]),
      ("Filters", ["dimCategory[Category]  →  is FG",
                   "In Summary Window  →  is 1"])],
     (16, 88, 1248, 140),
     "Finished goods per plant in all three units at once — megawatts, crore rupees and "
     "days — with four periods under each of the three master columns by default. Days is "
     "MW ÷ capacity MW, so a plant with no capacity figure is blank on purpose.",
     ["dimMeasure[Measure] goes in Columns FIRST, then dimDate[MonthName]. That order is what "
      "makes MW, Rs Cr. and Days the master columns with the periods nested inside them; "
      "the other way round gives you periods with three units inside each, which is not "
      "what you want.",
      "Values takes Unit Value by Period, not Unit Value. They are the same figure in a "
      "month column; the difference is the Total column, where the by-Period one averages "
      "the month-ends instead of adding them, because stock is a level.",
      "Filters pane → drag dimCategory[Category] in → tick FG only. Then drag the measure "
      "In Summary Window in and set 'is 1' — that is what limits it to four periods, or to "
      "the ones you tick, up to twelve.",
      "Format pane → Row headers → Stepped layout: Off, +/- icons: On.",
      "Format pane → Subtotals → Row subtotals: On, Column subtotals: Off.",
      "Format pane → Values → Font: Arial, Font size: 9, Colour: #1F2A24. Everything else "
      "comes from the theme.",
      "Format pane → General → Title → Font: Arial, Font size: 12, Colour: #14532D.",
      "Click a plant row and the technology matrix and the charts below follow it.",
      "With twelve periods ticked this is 36 number columns, so the matrix scrolls "
      "sideways. That is normal — scroll inside it, do not widen it."]),

    ("FG", "Matrix", "FG by Technology — MW · Rs Cr. · Days",
     [("Rows", ["dimNature[Nature]"]),
      ("Columns", ["dimMeasure[Measure]", "dimDate[MonthName]"]),
      ("Values", ["Unit Value by Period"]),
      ("Filters", ["dimCategory[Category]  →  is FG",
                   "In Summary Window  →  is 1"])],
     (16, 236, 1248, 252),
     "Exactly the same three master columns and the same periods, but by module technology "
     "rather than by plant — which is where a build-up in one technology shows up.",
     ["Build it the fastest way: click the matrix above, Ctrl+C, Ctrl+V, then in the Rows "
      "box remove dimPlant[Plant] and drag dimNature[Nature] in. Everything else, filters "
      "included, comes with the copy.",
      "Then set its position and size from the numbers below, and retype the title.",
      "Check the filters came across: the Filters pane should still show Category is FG and "
      "In Summary Window is 1.",
      "Format pane → Row headers → Stepped layout: Off.",
      "Format pane → Subtotals → Row subtotals: On, Column subtotals: Off.",
      "With the Plant slicer on one plant, this becomes that plant's technology split."]),

    ("FG", "Clustered column chart", "FG MW by Technology, Latest Month — Click a Bar",
     [("X-axis", ["dimNature[Nature]"]),
      ("Y-axis", ["MW"]),
      ("Filters", ["dimCategory[Category]  →  is FG",
                   "In Latest Month  →  is 1"])],
     (16, 496, 412, 208),
     "Which technology is holding the megawatts right now. It is deliberately pinned to the "
     "latest month with data: there is no period on the axis here, so without that pin it "
     "would add four months of stock together and read four times too high.",
     ["Filters pane → drag In Latest Month in → is 1. Do not skip it, and do not put a "
      "period field on this chart.",
      "Format pane → Data labels: On, Font: Arial, Font size: 9, Colour: #1F2A24, Display "
      "units: None, Value decimal places: 1.",
      "Format pane → Y-axis: Off — the label on each bar is the number.",
      "Format pane → X-axis → Values → Font: Arial, Font size: 9, Colour: #1F2A24.",
      "Format pane → Legend: Off. One measure, one colour.",
      "Format pane → General → Title → Font: Arial, Font size: 11, Colour: #14532D.",
      "Clicking a bar filters both matrices to that technology; right-click → Drill "
      "through → Detail for the materials behind it."]),

    ("FG", "Line and clustered column chart",
     "FG Days of Inventory by Month, Last 12 Months (Days and % vs Last Month)",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Column y-axis", ["Days"]),
      ("Line y-axis", ["Days vs LM"]),
      ("Filters", ["dimCategory[Category]  →  is FG",
                   "In Last 12  →  is 1"])],
     (444, 496, 428, 208),
     "How long the finished goods on hand would last, month by month, with the change on "
     "last month printed above each bar — so a slow build-up is visible before it becomes a "
     "number anyone argues about.",
     ["Filters pane → drag In Last 12 in → is 1, so this always shows the last twelve "
      "months whatever the pickers above say.",
      "This chart must ignore the two period pickers, or it drops back to four months: "
      "click the Months slicer → Format tab → Edit interactions → set this chart to None "
      "(the circle-with-a-line icon). Do the same after clicking the Quarters slicer.",
      "Format pane → Data labels: On. 'Apply settings to' → Series: Days — Font: Arial, "
      "Font size: 8, Colour: #1F2A24, Value decimal places: 0, Position: Inside end.",
      "Switch 'Apply settings to' → Series to Days vs LM: Font: Arial, Font size: 8, "
      "Colour: #14532D, Value decimal places: 0, Position: Above.",
      "Format pane → Y-axis: Off, Secondary y-axis: Off.",
      "Format pane → X-axis → Values → Font: Arial, Font size: 8, Colour: #1F2A24.",
      "Format pane → Legend: Off — the title says which is which.",
      "Format pane → General → Title → Font: Arial, Font size: 11, Colour: #14532D.",
      "Right-click any bar → Drill through → Detail for the split behind that month."]),

    ("FG", "Donut chart", "FG Share by Plant (%), Latest Month",
     [("Legend", ["dimPlant[Plant]"]),
      ("Values", ["FG ₹ Cr"]),
      ("Filters", ["In Latest Month  →  is 1"])],
     (888, 496, 376, 208),
     "Where the finished goods are sitting, as a share of the whole. Pinned to the latest "
     "month for the same reason as the bar chart: a share of four added-up months would "
     "mean nothing.",
     ["Filters pane → drag In Latest Month in → is 1.",
      "Format pane → Detail labels → Label contents: Category, percent of total. Font: "
      "Arial, Font size: 9, Colour: #1F2A24, Percentage decimal places: 1 — so the "
      "percentage is printed on each slice and nobody has to hover.",
      "Format pane → Legend: Off. The slice labels already name the plants.",
      "Format pane → General → Title → Font: Arial, Font size: 11, Colour: #14532D.",
      "Clicking a slice filters the rest of the page to that plant; clicking it again "
      "releases it."]),

    # ---- RM: its own controls, Rs Cr. | Days master columns, then two plant charts -----
    ("RM", "Slicer", "Months (leave empty for the last 4)",
     [("Field", ["dimDate[MonthName]"])],
     (16, 8, 300, 76),
     "Which months appear under each master column, and on both charts along the bottom. "
     "Nothing ticked means the last four with data; tick your own for up to twelve.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane → Slicer settings → Options → Style: Dropdown.",
      "Format pane → Slicer settings → Selection → 'Multi-select with CTRL': Off.",
      "Format pane → Values → Font: Arial, Font size: 10, Colour: #1F2A24."]),

    ("RM", "Slicer", "Quarters (leave empty for the last 4)",
     [("Field", ["dimDate[Quarter]"])],
     (332, 8, 240, 76),
     "The quarter-mode equivalent: empty means the last four fiscal quarters.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane → Slicer settings → Options → Style: Dropdown.",
      "Format pane → Slicer settings → Selection → 'Multi-select with CTRL': Off.",
      "Format pane → Values → Font: Arial, Font size: 10, Colour: #1F2A24."]),

    ("RM", "Slicer", "Plant",
     [("Field", ["dimPlant[Plant]"])],
     (588, 8, 220, 76),
     "One plant, or all three.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane → Slicer settings → Options → Style: Dropdown.",
      "Format pane → Values → Font: Arial, Font size: 10, Colour: #1F2A24."]),

    ("RM", "Slicer", "Group Nature",
     [("Field", ["factInventory[GroupNature]"])],
     (824, 8, 208, 76),
     "Module or Cell, when you want the page to be about one of the two only — the same "
     "split the Excel sheet had as its Module and Cell blocks.",
     [
      "Filters pane \u2192 drag the same field into this visual's own Filters box \u2192 Filter type: Advanced filtering \u2192 'is not blank' \u2192 Apply. That takes the empty row out of the list; it only appears because some rows carry a code the master sheet does not have.",
     "Format pane → Slicer settings → Options → Style: Dropdown.",
      "Format pane → Values → Font: Arial, Font size: 10, Colour: #1F2A24."]),

    ("RM", "Matrix", "RM Inventory by Plant — Rs Cr. · Days",
     [("Rows", ["dimPlant[Plant]"]),
      ("Columns", ["dimMeasure[Measure]", "dimDate[MonthName]"]),
      ("Values", ["Unit Value by Period"]),
      ("Filters", ["dimCategory[Category]  →  is RM",
                   "dimMeasure[Measure]  →  untick MW",
                   "In Summary Window  →  is 1"])],
     (16, 88, 1248, 140),
     "The top block of the old RM sheet, rebuilt: one row per plant, with Rs Cr. and Days as "
     "master columns and the periods under each. MW is unticked because an RM megawatt "
     "figure is derived from a BOM, not measured, so it does not belong beside the other two.",
     ["dimMeasure[Measure] goes in Columns FIRST, then dimDate[MonthName] — that order is what "
      "makes Rs Cr. and Days the master columns.",
      "Filters pane → dimCategory[Category] → tick RM only; then drag dimMeasure[Measure] in "
      "and untick MW so only Rs Cr. and Days remain; then drag In Summary Window in and set "
      "'is 1' for the four-periods-by-default behaviour.",
      "Values takes Unit Value by Period — in the Total column the plain Unit Value would "
      "add the month-ends together instead of averaging them.",
      "Format pane → Row headers → Stepped layout: Off.",
      "Format pane → Subtotals → Row subtotals: On (that is the Grand Total row the Excel "
      "sheet had), Column subtotals: Off.",
      "Format pane → General → Title → Font: Arial, Font size: 12, Colour: #14532D.",
      "Clicking a plant row filters the material matrix and both charts below it."]),

    ("RM", "Matrix", "RM Inventory by Group Nature and Nature — Rs Cr. · Days",
     [("Rows", ["factInventory[GroupNature]", "dimNature[Nature]"]),
      ("Columns", ["dimMeasure[Measure]", "dimDate[MonthName]"]),
      ("Values", ["Unit Value by Period"]),
      ("Filters", ["dimCategory[Category]  →  is RM",
                   "dimMeasure[Measure]  →  untick MW",
                   "In Summary Window  →  is 1"])],
     (16, 236, 1248, 252),
     "The second block of the old sheet: Module and Cell, each opening into its materials — "
     "cell cost, frame, glass, POE, wafer, paste, screens, gases and the rest — in the same "
     "two units and the same periods, with a subtotal on each group and a grand total under "
     "them.",
     ["Fastest way: click the matrix above, Ctrl+C, Ctrl+V, then drop "
      "factInventory[GroupNature] and dimNature[Nature] into Rows and remove "
      "dimPlant[Plant]. The three filters come with the copy.",
      "Then set its position and size from the numbers below, and retype the title.",
      "Format pane → Row headers → Stepped layout: Off, +/- icons: On. Group Nature and "
      "Nature then sit in two columns with an expander on each group row.",
      "Format pane → Subtotals → Row subtotals: On, and switch 'Per row level' On so both "
      "the Total Module and Total Cell lines appear, not only the grand total.",
      "Right-click a material row → Drill through → Detail for the material-by-material "
      "list behind it."]),

    ("RM", "Clustered column chart", "RM Inventory (Rs Cr.) by Plant",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Legend", ["dimPlant[Plant]"]),
      ("Y-axis", ["Inventory Rs Cr"]),
      ("Filters", ["dimCategory[Category]  \u2192  is RM",
                   "In Summary Window  \u2192  is 1"])],
     (16, 496, 616, 208),
     "Raw material held in crore rupees: one group per period along the bottom and the three "
     "plants side by side inside each group, so you read the months left to right and compare "
     "the plants within a month. It follows the pickers above, so it is four periods by "
     "default and up to twelve if you tick them.",
     ["dimDate[MonthName] goes in the X-axis and dimPlant[Plant] in Legend \u2014 that order is what "
      "gives three bars per month rather than four bars per plant.",
      "Format pane \u2192 Data labels: On, Font: Arial, Font size: 8, Bold: On, Colour: #FFFFFF, "
      "Display units: None, Value decimal places: 0, Position: Inside end.",
      "Format pane \u2192 Legend \u2192 Position: Top center, Font: Arial, Font size: 8. Keep it on: "
      "it is the only thing naming the plants.",
      "Format pane \u2192 Y-axis: Off \u2014 every bar is labelled, so the scale would only eat "
      "width.",
      "Format pane \u2192 X-axis \u2192 Values \u2192 Font: Arial, Font size: 8, Colour: #1F2A24, "
      "Concatenate labels: Off.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 12, Colour: #14532D.",
      "Clicking one plant's bar filters both matrices to that plant and that period."]),

    ("RM", "Line and clustered column chart",
     "RM Inventory (Days) by Plant, with Total Days across All Plants",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Column legend", ["dimPlant[Plant]"]),
      ("Column y-axis", ["Days by Period"]),
      ("Line y-axis", ["RM Days All Plants by Period"]),
      ("Filters", ["dimCategory[Category]  \u2192  is RM",
                   "In Summary Window  \u2192  is 1"])],
     (648, 496, 616, 208),
     "The same chart in days rather than rupees \u2014 how long each plant's raw material would "
     "last at its own capacity, three plant bars per month, and over them a line for the "
     "whole business: every plant's RM megawatts added together over every plant's capacity "
     "added together. The line is not the average of the three bars, and it is not their sum: "
     "it is one big plant's worth of days, which is the figure to quote for the company. Read "
     "together with the chart beside it, this tells you whether a bigger rupee figure is "
     "actually more stock or just a dearer month.",
     ["The line comes from RM Days All Plants by Period, which strips the plant filter off "
      "both the megawatts and the capacity, so a bar can be tall while the line is calm.",
      "Use Days by Period for the bars, not Days. Days is a ratio, so a total column has to average the three "
      "month-ends rather than add them, and that is the only difference between the two "
      "measures.",
      "Format pane \u2192 Data labels: On, Font: Arial, Font size: 8, Bold: On, Colour: #FFFFFF, "
      "Display units: None, Value decimal places: 0, Position: Inside end.",
      "Data labels \u2192 Apply settings to \u2192 Series \u2192 RM Days All Plants by Period: Font: "
      "Arial, Font size: 8, Bold: On, Colour: #14532D, Value decimal places: 0, Position: "
      "Above \u2014 dark green on the white card, because this label is not printed on a bar.",
      "Format pane \u2192 Lines \u2192 Colour: #14532D, Stroke width: 2, Show marker: On, Marker "
      "size: 4. Format pane \u2192 Lines \u2192 Smooth line: Off, so the shape is honest.",
      "Format pane \u2192 Legend \u2192 Position: Top center, Font: Arial, Font size: 8. The line "
      "appears in the legend as 'RM Days All Plants by Period' \u2014 rename it if you like by "
      "double-clicking the field in the well and typing 'Total (All Plants)'.",
      "Format pane \u2192 Y-axis: Off, and Secondary y-axis: Off. Bars and line are both in days "
      "on the same scale, so leave 'Align zeros' On if you switch either axis back on, or the "
      "line will sit at a misleading height.",
      "Format pane \u2192 X-axis \u2192 Values \u2192 Font: Arial, Font "
      "size: 8, Colour: #1F2A24, Concatenate labels: Off.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 12, Colour: #14532D.",
      "A plant with no capacity row in the Variables workbook shows blank here, not zero \u2014 "
      "that is deliberate, a missing denominator is not the same as no stock."]),

    ("Summary", "Line chart", "Days of Inventory by Month, Last 12 Months \u2014 RM, FG and Total",
     [("X-axis", ["dimDate[MonthName]"]),
      ("Y-axis", ["RM Days", "FG Days", "Total Days (RM + FG)"]),
      ("Filters", ["In Last 12  \u2192  is 1"])],
     (16, 548, 1248, 156),
     "The long view under the reconciliation: three lines across the last twelve months "
     "that have data, or fewer if that is all there is \u2014 raw material days, finished goods "
     "days, and the two added together, which is what the Overview card calls Days of "
     "inventory (RM + FG). Every month is its own closing figure divided by capacity, so "
     "nothing is added across months. Read it for shape: RM climbing while FG is flat means "
     "material is arriving faster than it is being consumed.",
     ["This chart must ignore the period pickers at the top of Summary, or it would drop "
      "back to four months. Click the 'Months' slicer, then ribbon Format \u2192 Edit "
      "interactions, and on this chart click the circle-with-a-line (None). Repeat for the "
      "Quarters slicer. Leave Plant and Type filtering, so those two still work on it \u2014 "
      "picking a plant re-bases all three lines on that plant's capacity.",
      "Format pane \u2192 Data labels: On, Font: Arial, Font size: 8, Bold: On, Colour: #14532D, "
      "Display units: None, Value decimal places: 0, Position: Above. Twelve months \u00d7 three "
      "lines is a lot of numbers: if they collide, set Data labels \u2192 Apply settings to \u2192 "
      "Series and switch the Total line's labels off, since it is the sum of the other two.",
      "Format pane \u2192 Lines \u2192 Stroke width: 2, Show marker: On, Marker size: 4. Then Lines "
      "\u2192 Apply settings to \u2192 Series: RM Days #2E7D46, FG Days #7FBB84, "
      "Total Days (RM + FG) #14532D \u2014 the total is the darkest, so it reads as the envelope.",
      "Format pane \u2192 Legend \u2192 Position: Top center, Font: Arial, Font size: 9, Colour: "
      "#1F2A24. Three series need a key, unlike the single-series charts elsewhere.",
      "Format pane \u2192 Y-axis \u2192 Title: On, Text: 'Days', Font: Arial, Font size: 9, Colour: "
      "#1F2A24, Display units: None. A days axis earns its title because the number is a "
      "ratio, not rupees.",
      "Format pane \u2192 X-axis \u2192 Values \u2192 Font: Arial, Font size: 8, Colour: #1F2A24, "
      "Concatenate labels: Off.",
      "Format pane \u2192 General \u2192 Title \u2192 Font: Arial, Font size: 12, Colour: #14532D.",
      "If a plant has no capacity row in the Variables workbook its days go blank rather than "
      "zero, so a gap in a line means missing capacity, not zero stock.",
      "Right-click a point \u2192 Drill through \u2192 Detail for the materials behind that month."]),

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
     (16, 120, 404, 232),
     "RM / FG / consumables for exactly what you clicked.",
     ["Format pane → Detail labels → Label contents: Category, percent of total."]),

    ("Detail", "Donut chart", "Split by technology / nature",
     [("Legend", ["dimNature[Nature]"]),
      ("Values", ["Value ₹ Cr"])],
     (428, 120, 404, 232),
     "Which technology or material nature the slice is made of.",
     ["Format pane → Detail labels → Label contents: Category, percent of total."]),

    ("Detail", "Pie chart", "Split by plant",
     [("Legend", ["dimPlant[Plant]"]),
      ("Values", ["Value ₹ Cr"])],
     (840, 120, 424, 232),
     "Where the slice sits. A single-colour pie means it is one plant already.",
     ["Format pane → Detail labels → Label contents: Category, percent of total."]),

    ("Detail", "Matrix", "Materials behind this number — click + to open a nature",
     [("Rows", ["dimNature[Nature]", "factInventory[Material]",
                "factInventory[MaterialDesc]"]),
      ("Values", ["Value ₹ Cr", "MW", "Days", "INR per Wp", "Share of Total %"])],
     (16, 364, 1248, 348),
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
      "Click the Value ₹ Cr column header once so it sorts largest first.",
      "Format pane → Values → Text size: 9 and Row padding: 1. At 348 high that is about "
      "eighteen rows on screen at once, roughly twice what the default padding allows.",
      "How to scroll it: put the mouse pointer inside the matrix, not on the page around it, "
      "and use the wheel — the scrollbar is hidden until the pointer is over the visual. "
      "Two-finger drag on a trackpad does the same.",
      "If the wheel still does nothing, the page itself is being scrolled instead: ribbon "
      "View → Page view → Fit to page, so the whole canvas is on screen and the wheel "
      "belongs to the visual under the pointer.",
      "For a really long list use Focus mode — hover the visual, click the diagonal-arrows "
      "icon in its top-right, and it fills the page with far more rows visible; the back "
      "arrow returns you. Or collapse a nature with its − icon to jump past it."]),

    # ---- Checks: the page that tells you what the source files did not give -------------
    ("Checks", "Card", "Stock rows loaded",
     [("Fields", ["Check MB5B Rows"])],
     (16, 56, 240, 88),
     "How many rows came out of RM Raw, FG Raw and Consble Raw together. Zero means pRoot is "
     "wrong or the three folders are named differently.",
     ["Format pane \u2192 Callout value \u2192 Font: Arial, Font size: 16, Colour: #14532D.",
      "Format pane \u2192 General \u2192 Effects \u2192 Background: #FFFFFF."]),

    ("Checks", "Card", "Trial balance rows loaded",
     [("Fields", ["Check TB Rows"])],
     (264, 56, 240, 88),
     "Zero here is the reason Inventory (TB) reads as empty on Summary: either the TB folder "
     "has no TB_YYYYMM.xlsx files, or the GL numbers in them match nothing on TB Master.",
     ["Format pane \u2192 Callout value \u2192 Font: Arial, Font size: 16, Colour: #14532D.",
      "Format pane \u2192 General \u2192 Effects \u2192 Background: #FFFFFF."]),

    ("Checks", "Card", "Months of data",
     [("Fields", ["Check Months of Data"])],
     (512, 56, 240, 88),
     "How many month-ends the stock files cover. One month means only one file was read, and "
     "then every monthly chart has a single bar however it is built.",
     ["Format pane \u2192 Callout value \u2192 Font: Arial, Font size: 16, Colour: #14532D.",
      "Format pane \u2192 General \u2192 Effects \u2192 Background: #FFFFFF."]),

    ("Checks", "Card", "Plant codes in the data",
     [("Fields", ["Check Plant Codes"])],
     (760, 56, 240, 88),
     "More than three means the stock files carry a valuation area beyond the three plants; "
     "those now appear as 'Plant xxxx' rather than as a blank row.",
     ["Format pane \u2192 Callout value \u2192 Font: Arial, Font size: 16, Colour: #14532D.",
      "Format pane \u2192 General \u2192 Effects \u2192 Background: #FFFFFF."]),

    ("Checks", "Card", "Rows with no nature (%)",
     [("Fields", ["Check Unassigned %"])],
     (1008, 56, 256, 88),
     "The share of stock rows the master sheets do not cover. Anything above zero is what "
     "shows up as an Unassigned slice on the donuts and an Unassigned row in the technology "
     "matrix \u2014 the material numbers differ between the master sheet and the raw files.",
     ["Format pane \u2192 Callout value \u2192 Font: Arial, Font size: 16, Colour: #B3261E.",
      "Format pane \u2192 General \u2192 Effects \u2192 Background: #FFFFFF."]),

    ("Checks", "Table", "Every file the four folders gave, with its sheets",
     [("Columns", ["qcHeaders[Folder]", "qcHeaders[Name]", "qcHeaders[SheetNames]"])],
     (16, 160, 620, 264),
     "One row per file actually read. If a month is missing from the report, it is missing "
     "from this list first \u2014 check the file is in the folder and is a real .xlsx.",
     ["Format pane \u2192 Values \u2192 Font: Arial, Font size: 9, Colour: #1F2A24.",
      "Format pane \u2192 Column headers \u2192 Font: Arial, Font size: 9, Colour: #14532D."]),

    ("Checks", "Table", "Sheets found in Variables and Calculations",
     [("Columns", ["qcVarHeaders[SheetName]", "qcVarHeaders[DataRows]"])],
     (644, 160, 620, 264),
     "The workbook that carries RM Nature, FG Master, TB Master, Constants and MW. A sheet "
     "missing from this list, or showing 0 rows, is why the natures or the trial balance are "
     "empty.",
     ["Format pane \u2192 Values \u2192 Font: Arial, Font size: 9, Colour: #1F2A24.",
      "Format pane \u2192 Column headers \u2192 Font: Arial, Font size: 9, Colour: #14532D."]),

    ("Checks", "Table", "GL accounts in the TB files that TB Master does not list",
     [("Columns", ["factTB_Unmapped[GLAccount]", "factTB_Unmapped[GLDesc]",
                   "factTB_Unmapped[Amount]"])],
     (16, 432, 620, 264),
     "Empty is good. A long list here with 0 trial-balance rows above means TB Master is not "
     "matching your GL numbers at all, and the report is showing the whole trial balance "
     "rather than the inventory accounts.",
     ["Format pane \u2192 Values \u2192 Font: Arial, Font size: 9, Colour: #1F2A24.",
      "Format pane \u2192 Column headers \u2192 Font: Arial, Font size: 9, Colour: #14532D."]),

    ("Checks", "Table", "FG technologies with no capacity on the MW sheet",
     [("Columns", ["qcNatureNoCapacity[Nature]"])],
     (644, 432, 620, 264),
     "Each of these gets blank Days, because days of inventory divides by capacity. Add the "
     "technology to the MW sheet and it fills in by itself.",
     ["Format pane \u2192 Values \u2192 Font: Arial, Font size: 9, Colour: #1F2A24.",
      "Format pane \u2192 Column headers \u2192 Font: Arial, Font size: 9, Colour: #14532D."]),

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
