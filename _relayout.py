"""One-off: rebuilds the Summary / FG / RM matrix blocks in spec.py.

Each metric becomes its own matrix with dimDate[MonthName] as the only Columns field, which
is the layout of the Excel sheets these pages replace (IN CRS block, IN DAYS block, IN MW
block, each with its own row of months) and the only one Desktop draws without expanding.
"""
import io
import pathlib

P = pathlib.Path("/home/ubuntu/inv-guide/spec.py")
src = P.read_text().split("\n")            # 0-indexed lines

WHY_COLS = (
    "Columns holds dimDate[MonthName] and nothing else, and Values holds one measure. That "
    "is what puts the months on show with nothing to expand: a Metric field above the month "
    "is a two-level column hierarchy, and Desktop opens one of those collapsed onto a single "
    "figure per metric \u2014 or draws the visual as an empty card, which is what emptied this "
    "page. One metric per matrix, side by side, is the same grid the Excel sheet had.")
NO_TOTAL = (
    "Format pane \u2192 Subtotals \u2192 Column subtotals: Off. Stock is a level, not a flow: a "
    "Total column would add March's steel to July's steel, which is the same steel counted "
    "twice. Row subtotals: On \u2014 that one adds the plants inside a single month, which is a "
    "real figure, and it is the Grand Total row the Excel sheet had.")
FONTS = ("Format pane \u2192 Values \u2192 Font: Arial, Font size: 8, Colour: #1F2A24; Row headers "
         "\u2192 Font size: 8; Column headers \u2192 Font size: 8. Three blocks across the width "
         "means every column has to earn its pixels.")
LINEUP = ("Fastest way to build the next block: click this matrix, Ctrl+C, Ctrl+V, then in "
          "Values swap the measure. Position, filters and formatting all come with the copy.")


def matrix(page, title, rows, measure, mlabel, filters, pos, why, extra):
    wells = ['[("Rows", %s),' % rows,
             '      ("Columns", ["dimDate[MonthName]"]),',
             '      ("Values", ["%s" + AS + "%s"]),' % (measure, mlabel)]
    if filters:
        wells.append('      ("Filters", %s)],' % filters)
    else:
        wells[-1] = wells[-1].rstrip(",") + "],"
    out = io.StringIO()
    out.write('    ("%s", "Matrix",\n     %r,\n     %s\n' % (page, title, "\n".join(wells)))
    out.write("     %r,\n" % (pos,))
    out.write("     %r,\n" % why)
    out.write("     [%s]),\n\n" % ",\n      ".join(repr(e) for e in extra))
    return out.getvalue()


# ---- Summary: TB block, MB5B block, Check block - then the same three across all plants ----
SUM_ROWS = '["dimPlant[Plant]", "dimCategory[Category]"]'
SUM_FILT = '["In Summary Window  \u2192  is 1"]'
sum_blocks = ""
for i, (t, m, why) in enumerate([
    ("Inventory (TB) \u2014 by Plant and Type (Rs Cr.)", "TB Inventory Rs Cr",
     "The books: what the trial balance says is on hand, one row per plant opening into RM, "
     "FG and Consumables, and one column per month \u2014 the newest March plus the three months "
     "after it by default. This is the left-hand block of the Excel sheet, unchanged in "
     "meaning."),
    ("As per MB5B \u2014 by Plant and Type (Rs Cr.)", "Inventory Rs Cr",
     "The stock report against it: the same rows and the same months, valued from MB5B. Read "
     "it beside the block on its left, month for month."),
    ("Check \u2014 TB Minus MB5B (Rs Cr.)", "Difference Inventory Rs Cr",
     "The reconciliation itself, month by month: books minus stock report. A figure either "
     "side of zero is equally wrong, which is why both ends are coloured red."),
]):
    extra = [WHY_COLS if i == 0 else LINEUP,
             "Filters pane \u2192 drag the measure In Summary Window in \u2192 is 1. That is what "
             "gives you the newest March plus three months by default, and the months you "
             "tick in the slicer when you tick them.",
             NO_TOTAL,
             "Format pane \u2192 Row headers \u2192 Stepped layout: Off, +/- icons: On, so Plant and "
             "Type sit in two columns with an expander on each plant.",
             "Format pane \u2192 Subtotals \u2192 Row subtotals: On with 'Per row level' On, so each "
             "plant totals its own three types.",
             FONTS,
             "All three blocks carry the same filter and the same slicers, so they always "
             "show the same months in the same order \u2014 read straight across."]
    if m == "Difference Inventory Rs Cr":
        extra.append(
            "Values box \u2192 the down-arrow next to the measure \u2192 Conditional formatting \u2192 "
            "Background color \u2192 Format style: Diverging, tick 'Add a middle colour', middle "
            "number 0, and make both Minimum and Maximum red.")
    sum_blocks += matrix("Summary", t, SUM_ROWS, m, "Rs Cr.", SUM_FILT,
                         (16 + i * 416, 88, 408, 232), why, extra)

for i, (t, m, why) in enumerate([
    ("Total Overall \u2014 Inventory (TB) (Rs Cr.)", "TB Inventory Rs Cr",
     "Every plant added together, by type: one row for RM, one for FG, one for Consumables "
     "and a Total under them \u2014 the bottom block of the Excel sheet. Plants inside one month "
     "add up legitimately, which is why this block exists at all."),
    ("Total Overall \u2014 as per MB5B (Rs Cr.)", "Inventory Rs Cr",
     "The same three types across all plants, from the stock report."),
    ("Total Overall \u2014 Check (Rs Cr.)", "Difference Inventory Rs Cr",
     "And the gap on the whole business, by type and by month. This is the number to take "
     "to a review: if it is small on every type in every month, the report reconciles."),
]):
    sum_blocks += matrix(
        "Summary", t, '["dimCategory[Category]"]', m, "Rs Cr.", SUM_FILT,
        (16 + i * 416, 328, 408, 112), why,
        [LINEUP if i else
         "Same as the block directly above it with dimPlant[Plant] taken out of Rows \u2014 copy "
         "that matrix, paste, remove the Plant field, and set the size below.",
         "Filters pane \u2192 In Summary Window \u2192 is 1, so it shows the same months as the "
         "block above and lines up column for column.",
         NO_TOTAL,
         "Format pane \u2192 Row headers \u2192 Font: Arial, Font size: 8, Bold: On.",
         "This matrix has no Plant field on purpose. Leave the Plant slicer on All when you "
         "want the across-all-plants figure \u2014 picking one plant filters this block too."])

# ---- FG: IN MW | IN CRS | IN DAYS, by plant and then by technology ----------------------
FG_FILT = '["dimCategory[Category]  \u2192  is FG",\n                   "In Summary Window  \u2192  is 1"]'
METRICS = [("Inventory MW", "MW", "megawatts"),
           ("Inventory Rs Cr", "Rs Cr.", "crore rupees"),
           ("Days", "Days", "days of cover")]
fg_blocks = ""
for i, (m, lab, unit) in enumerate(METRICS):
    fg_blocks += matrix(
        "FG", "Inventory FG by Plant \u2014 In %s" % lab.rstrip("."), '["dimPlant[Plant]"]',
        m, lab, FG_FILT, (16 + i * 416, 88, 408, 112),
        "Finished goods per plant in %s, one column per month \u2014 the newest March plus the "
        "three after it by default. The Excel sheet had this as one wide table with an IN MW "
        "block, an IN CRS block and an IN DAYS block; these are those blocks." % unit,
        [WHY_COLS if i == 0 else LINEUP,
         "Filters pane \u2192 dimCategory[Category] \u2192 tick FG only, then the measure In Summary "
         "Window \u2192 is 1.",
         NO_TOTAL,
         FONTS,
         "Days is MW \u00f7 capacity MW, so a plant with no row on the MW Capacity sheet is "
         "blank here on purpose \u2014 a missing denominator is not the same as no stock."
         if lab == "Days" else
         "Clicking a plant row filters the technology blocks and the charts below to it."])

for i, (m, lab, unit) in enumerate(METRICS):
    fg_blocks += matrix(
        "FG", "Inventory FG by Techno \u2014 In %s" % lab.rstrip("."), '["dimNature[Nature]"]',
        m, lab, FG_FILT, (16 + i * 416, 208, 408, 180),
        "The same months and the same unit, by module technology rather than by plant \u2014 G12 "
        "Perc, G12R Topcon, M10 Perc, M10 Topcon and the rest \u2014 which is where a build-up "
        "in one technology shows itself.",
        [LINEUP + " Then in Rows take dimPlant[Plant] out and drag dimNature[Nature] in.",
         "Check the filters came across: Category is FG, In Summary Window is 1.",
         NO_TOTAL,
         "With the Plant slicer on one plant this becomes that plant's technology split, "
         "which is the Module block the Excel sheet had."])

# ---- RM: IN CRS | IN DAYS, by plant and then by group nature and nature ------------------
RM_FILT = '["dimCategory[Category]  \u2192  is RM",\n                   "In Summary Window  \u2192  is 1"]'
RM_METRICS = [("Inventory Rs Cr", "Rs Cr.", "crore rupees"), ("Days", "Days", "days of cover")]
rm_blocks = ""
for i, (m, lab, unit) in enumerate(RM_METRICS):
    rm_blocks += matrix(
        "RM", "RM Inventory Plant Wise \u2014 In %s" % lab.rstrip("."), '["dimPlant[Plant]"]',
        m, lab, RM_FILT, (16 + i * 632, 88, 616, 112),
        "Raw material and packing per plant in %s, one column per month \u2014 the top block of "
        "the old RM sheet, which had IN CRS and IN DAYS side by side over the same three "
        "plants. MW is left out because an RM megawatt figure is derived from a BOM rather "
        "than measured." % unit,
        [WHY_COLS if i == 0 else LINEUP,
         "Filters pane \u2192 dimCategory[Category] \u2192 tick RM only, then In Summary Window \u2192 is 1.",
         NO_TOTAL,
         "Format pane \u2192 Values \u2192 Font: Arial, Font size: 9, Colour: #1F2A24.",
         "Clicking a plant row filters the nature blocks and both charts below it."])

for i, (m, lab, unit) in enumerate(RM_METRICS):
    rm_blocks += matrix(
        "RM", "RM Inventory by Group Nature and Nature \u2014 In %s" % lab.rstrip("."),
        '["factInventory[GroupNature]", "dimNature[Nature]"]', m, lab, RM_FILT,
        (16 + i * 632, 208, 616, 220),
        "The second block of the old sheet in %s: Module and Cell, each opening into its "
        "natures \u2014 cell cost, frame, glass, POE, wafer, paste, screens, gases and the rest "
        "\u2014 with a subtotal on each group and a grand total under them." % unit,
        [LINEUP + " Then in Rows drop factInventory[GroupNature] and dimNature[Nature] in "
         "and take dimPlant[Plant] out.",
         "Format pane \u2192 Row headers \u2192 Stepped layout: Off, +/- icons: On, so Group Nature "
         "and Nature get a column each with an expander on each group.",
         "Format pane \u2192 Subtotals \u2192 Row subtotals: On with 'Per row level' On, so Total "
         "Module and Total Cell both appear and not only the grand total.",
         NO_TOTAL,
         "A nature reading Unassigned is a material the RM master does not carry \u2014 it is "
         "money the report will not silently file under someone else's nature. qcAttrMatch "
         "on Checks names them.",
         "Right-click a nature row \u2192 Drill through \u2192 Detail for the material-by-material "
         "list behind it."])


def splice(lines, start1, end1, text):
    """Replaces the 1-indexed inclusive line range with text (which ends in a newline)."""
    return lines[:start1 - 1] + text.rstrip("\n").split("\n") + lines[end1:]


# bottom up, so earlier line numbers stay valid
src = splice(src, 782, 824, rm_blocks)
src = splice(src, 623, 672, fg_blocks)
src = splice(src, 464, 529, sum_blocks)
out = "\n".join(src)

# the charts move up under the taller matrix stacks
for a, b in [("(16, 412, 412, 292)", "(16, 396, 412, 292)"),
             ("(444, 412, 428, 292)", "(444, 396, 428, 292)"),
             ("(888, 412, 376, 292)", "(888, 396, 376, 292)"),
             ("(16, 504, 616, 200)", "(16, 436, 616, 200)"),
             ("(648, 504, 616, 200)", "(648, 436, 616, 200)")]:
    assert out.count(a) == 1, a
    out = out.replace(a, b)

P.write_text(out)
print("spec.py rewritten")
