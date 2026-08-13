"""Turns spec.py into (a) guided one-at-a-time steps and (b) the PART 4 markdown."""
from spec import (CANVAS, PAGES, CARDS, SLICERS, VISUALS, DRILL_PAGE, DRILL_FIELDS,
                  BAND_PAGES, DECOR, FONT, PANEL, PANEL_INK, PANEL_SUB, HEAD, INK)

W, H = CANVAS



# Which icon to click in the Visualizations pane, described the way it looks on screen.
ICON = {
    "Card":                          "the icon showing 123 (called Card)",
    "Slicer":                        "the icon of a funnel with a bar under it (called Slicer)",
    "Matrix":                        "the icon of a small grid of boxes (called Matrix)",
    "Stacked column chart":          "the icon of three bars stacked in two colours "
                                     "(called Stacked column chart)",
    "Clustered column chart":        "the icon of three plain bars side by side "
                                     "(called Clustered column chart)",
    "Line and clustered column chart":"the icon of bars with a line drawn over them "
                                     "(called Line and clustered column chart)",
    "Pie chart":                     "the icon of a filled circle (called Pie chart)",
    "Donut chart":                   "the icon of a ring (called Donut chart)",
    "Table":                         "the icon of a plain grid with a heading row (called Table)",
    "Decomposition tree":            "the icon of boxes joined by branches "
                                     "(called Decomposition tree)",
}


def _hover_note():
    return ("Hover the mouse over an icon and Power BI shows its name, so you can be sure "
            "you have the right one.")


def _drag(field, well):
    """One literal sentence for putting one field into one well."""
    if "[" in field:                                    # a table column
        tbl, col = field.split("[")[0], field.split("[")[1].rstrip("]")
        return ("In the Data pane (far right), scroll to the table called %s and click the "
                "little arrow to its left to open it, then drag the field called %s out of "
                "it and drop it into the box called %s. (If the list is long, type %s into "
                "the search box at the top of the pane first.)"
                % (tbl, col, well, col))
    return ("In the Data pane (far right) click the search box at the very top of the pane "
            "and type: %s — the whole list shrinks to just that one item (it has a small "
            "calculator icon, because it is a measure). Drag it into the box called %s, then "
            "clear the search box." % (field, well))


def _insert(vtype):
    return ["Click once on an empty white part of the page, so that no visual has a border "
            "round it.",
            "In the Visualizations pane on the right (the grid of small icons), click %s. "
            "An empty visual appears on the page." % ICON.get(vtype, "the %s icon" % vtype),
            "Check you took the right one: hover the mouse over the icon that is now "
            "highlighted and the name that appears must read exactly '%s'. Several icons "
            "look alike, so if it says anything else, click the correct one now — with the "
            "visual still empty, changing type costs nothing." % vtype]


def _plain(line):
    """Turn 'Format pane -> A -> B: C' shorthand into a literal instruction."""
    if not line.startswith("Format pane \u2192"):
        return line
    body = line[len("Format pane \u2192"):].strip().rstrip(".")
    parts = [b.strip() for b in body.split("\u2192")]
    last = parts[-1]
    setting, _, value = last.partition(":")
    if value:
        path = ", then ".join("'%s'" % s for s in parts[:-1] + [setting.strip()])
        tail = " and set it to %s" % value.strip()
    else:
        path = ", then ".join("'%s'" % s for s in parts)
        tail = ""
    return ("In the Visualizations pane click the paintbrush icon, then click %s%s."
            % (path, tail))


def _place(x, y, w, h, in_format=False):
    first = ("Still in the same pane, click the word General, then Properties."
             if in_format else
             "In the Visualizations pane click the paintbrush icon, then click General, "
             "then Properties.")
    return [first,
            "Inside Properties there are two groups, Size and Position. Click the small "
            "arrow beside each to open it. (Older versions call the whole thing 'Size and "
            "style' and list all four boxes together.)",
            "Type the four numbers below into their boxes, pressing Tab after each one. "
            "Horizontal is the same thing as X, and Vertical is the same thing as Y."]


def _pos_rows(x, y, w, h):
    return [("Horizontal (X)", str(x)), ("Vertical (Y)", str(y)),
            ("Width", str(w)), ("Height", str(h))]


SHAPE = {
    "Matrix": "a grid with the row names down the left and the column headings across the "
              "top, and a Total row at the bottom",
    "Stacked column chart": "bars, each one split into coloured blocks, with a small colour "
                            "key above it",
    "Clustered column chart": "groups of plain bars standing side by side",
    "Line and clustered column chart": "bars with a line drawn across the top of them",
    "Pie chart": "a filled circle cut into coloured slices",
    "Donut chart": "a ring cut into coloured slices, hollow in the middle",
    "Table": "plain rows with a heading row above them",
    "Decomposition tree": "one box on the left with a + on it",
    "Card": "one number",
    "Slicer": "a dropdown",
}


def _fit(vtype, title):
    """Settings that stop text clipping or overflowing, per visual type.

    Power BI's defaults are sized for a full-screen visual; these pages fit 5-8 visuals
    on one canvas, so titles, headers and labels have to come down a size or two.
    """
    common = ["Still in the paintbrush pane, click General, then Title, and set Font size "
              "to 12. If the title still ends in three dots, shorten the text you typed — "
              "a clipped title is the visual telling you it has run out of width."]
    if vtype in ("Matrix", "Table"):
        return common + [
            "Click 'Column headers' and set Font size to 10; if there is a 'Word wrap' "
            "toggle under it, switch it On so a long heading goes onto two lines instead "
            "of being cut.",
            "Click 'Row headers' and do the same: Font size 10, Word wrap On if it is "
            "offered.",
            "Click 'Values' and set Font size to 10.",
            "Double-click the line between two column headings to widen a column that is "
            "still showing three dots — or drag that line. Column widths are remembered "
            "when you save."]
    if vtype in ("Pie chart", "Donut chart"):
        return common + [
            "Click 'Detail labels' and set Font size to 9. If a slice label is still cut "
            "off, set 'Position' to Outside, and switch on 'Overflow text' if your version "
            "offers it.",
            "Click 'Legend' and set Font size to 9 and Position to 'Top center'. If the "
            "legend eats the chart, switch Legend off entirely — the labels already name "
            "the slices."]
    if vtype == "Card":
        return common + [
            "Click 'Callout value' (that is the big number) and set Font size to 24.",
            "If the list has a 'Category label' — the small grey wording Power BI prints "
            "under the number — set its Font size to 10, or switch it off, because the "
            "title above already says the same thing. The newer Card visual has no category "
            "label at all, so skip this line if you cannot see it."]
    if vtype == "Decomposition tree":
        return common
    return common + [
        "Click 'X-axis' and set Font size to 9. If the labels are turned on their side or "
        "cut off, that is the visual being too narrow — leave it, Power BI rotates them "
        "on purpose.",
        "Click 'Y-axis' and set Font size to 9.",
        "Click 'Legend' and set Font size to 9 and Position to 'Top center'.",
        "Leave 'Data labels' off on this one: numbers printed on every bar overlap as soon "
        "as there are more than about six bars."]


def _check(vtype, wells):
    """What the finished visual must look like, in plain words."""
    named = [f for wl, fl in wells if wl != "Filters" for f in fl]
    return ("The visual shows %s, it is not empty and not showing an error triangle, the "
            "title and every heading are readable in full rather than ending in three dots, "
            "and the Visualizations pane still lists every field you dropped in: %s."
            % (SHAPE.get(vtype, "what the title describes"), ", ".join(named)))


def _stuck(vtype, wells=()):
    common = ("Empty visual: a slicer above is filtering everything out — clear the header "
              "dropdowns and look again. 'Can't display this visual': a field is in the wrong "
              "box, so drag it out and put it back where the list below says. Wrong size: "
              "retype the four numbers rather than dragging the corners. Text ending in three "
              "dots: drop that font size by 1 and, on a heading, switch its Word wrap on.")
    if vtype == "Matrix":
        rows = [f for wl, fl in wells if wl == "Rows" for f in fl]
        extra = (" No + signs on the row names: one of the two Rows fields is missing, or "
                 "stepped layout is still on — both are set in the lines above."
                 if len(rows) > 1 else "")
        return (common + extra + " Every row showing the same number: a relationship from "
                "Part 2 is missing.")
    if vtype == "Decomposition tree":
        return common + " Nothing to expand means the Explain by box is empty."
    return common



def _decor_steps():
    """The green panel, the logo box and the wording on Overview: no data, pure furniture."""
    out = []
    for kind, text, x, y, w, h, note in [(d[1], d[2], d[3], d[4], d[5], d[6], d[7])
                                         for d in DECOR if d[0] == "Overview"]:
        if kind == "Rectangle":
            do = ["At the bottom of the window click the tab named Overview.",
                  "Click once on an empty part of the page so nothing is selected.",
                  "At the top of the window click the Insert tab, then click Shapes, then "
                  "click Rectangle. A grey rectangle appears.",
                  "In the Format pane on the right click Shape, then Style, then Fill, and "
                  "click the colour box. Choose 'Custom colour' at the bottom of the list "
                  "and type %s into the Hex box, then press Enter." % PANEL,
                  "Still under Style, click Border and switch it Off.",
                  "Under Shape, set Rounded corners to 0 if that box exists."]
            do += _place(x, y, w, h, in_format=True)
            do += ["Right-click the rectangle and choose Send to back. Everything you add "
                   "next will sit on top of it."]
            out.append(dict(
                title="Overview — the green panel down the left",
                page="Overview", do=do,
                fields=[("Shape", "Rectangle"), ("Fill colour (Hex)", PANEL),
                        ("Border", "Off")] + _pos_rows(x, y, w, h),
                note="This is only paint. The panel is what makes the left-hand figures read "
                     "as one block instead of nine loose cards.",
                check="A dark green stripe runs down the whole left edge of the page, from "
                      "the very top to the very bottom.",
                stuck="If it hides something you built earlier, right-click it and choose "
                      "Send to back again. If the green is the wrong shade, reopen Fill → "
                      "Custom colour and retype %s." % PANEL))
        elif kind == "Image":
            do = ["At the bottom of the window click the tab named Overview.",
                  "At the top of the window click the Insert tab, then click Image.",
                  "Pick any picture file for now — a placeholder is fine; you can swap in "
                  "the company logo later by clicking the image and choosing Browse.",
                  "In the Format pane click Image, then Style, and set Fit to 'Fit', so the "
                  "picture shrinks inside the box instead of being cropped.",
                  "Click General, then Effects, and switch Background Off and Border Off."]
            do += _place(x, y, w, h, in_format=True)
            out.append(dict(
                title="Overview — the logo box, top left",
                page="Overview", do=do,
                fields=[("Insert", "Image"), ("Fit", "Fit")] + _pos_rows(x, y, w, h),
                note="Left empty for now on purpose. When you have the real logo, click this "
                     "box, choose Browse and pick the file — nothing else moves.",
                check="A small square sits in the top-left corner of the green panel, with "
                      "the words 'Inventory Overview' to its right once the next step is "
                      "done.",
                stuck="If the picture is stretched, set Fit to 'Fit' rather than 'Fill'. If "
                      "the box has a white surround, its Background is still on."))
        else:
            size, colour = (15, PANEL_INK) if h >= 28 else (10, PANEL_SUB)
            do = ["At the bottom of the window click the tab named Overview.",
                  "Click once on an empty part of the page so nothing is selected.",
                  "At the top of the window click the Insert tab, then click Text box. A "
                  "small empty box appears with the cursor inside it.",
                  "Type exactly: %s" % text,
                  "Select the words you just typed by dragging across them with the mouse.",
                  "A small toolbar sits above the text box. In it: set the font to %s, set "
                  "the size to %d, click the B button to make it bold, then click the "
                  "letter-A colour button, choose 'Custom colour' and type %s into the Hex "
                  "box." % (FONT, size, colour),
                  "Click once outside the text box to finish typing, then click the box "
                  "itself once so it has a border round it.",
                  "In the Format pane click General, then Effects, and switch Background "
                  "Off and Border Off, so only the words show on the green."]
            do += _place(x, y, w, h, in_format=True)
            out.append(dict(
                title="Overview — the wording '%s'" % text,
                page="Overview", do=do,
                fields=[("Text", text), ("Font", FONT), ("Font size", str(size)),
                        ("Bold", "Yes"), ("Colour (Hex)", colour)] + _pos_rows(x, y, w, h),
                note=note,
                check="The words '%s' show in %s on the green panel, at the position "
                      "below." % (text, "white" if colour == PANEL_INK else "pale green"),
                stuck="If the words are invisible, the colour is still black on dark green — "
                      "reselect the text and set the Hex to %s. If a white box surrounds "
                      "them, Background is still on under General → Effects." % colour))
    return out


def steps():
    """Each step: dict(title, page, do=[lines], fields=[(label, value)], note, link?)."""
    S = []

    S.append(dict(
        title="Before you start",
        page="—",
        do=["You should already have: the queries loaded (Part 1), the relationships made "
            "(Part 2) and the measures added (Part 3).",
            "Click the very first icon on the left edge of the Power BI window — it looks "
            "like a bar chart. That is Report view, where all of these steps happen.",
            "Three panes should now be down the right-hand side: Filters, then "
            "Visualizations (a grid of small chart icons), then Data (a list of your tables "
            "such as factInventory and dimDate).",
            "If a pane is missing, click the View tab at the top and then 'Show panes' "
            "(or click the small > arrow at the right edge of the window to open it).",
            "Hover the mouse over any icon in the Visualizations pane and Power BI tells "
            "you its name — use that whenever a step names an icon."],
        fields=[], note="If a name a step asks for is not in the Data pane, that part is not "
                        "finished — go back to Part 1-3 rather than guessing.",
        check="The Data pane on the right lists factInventory, factTB, dimPlant, dimDate, "
              "dimNature, dimCapacity, dimTBMaster, dimCategory, dimMetric and dimMeasure, "
              "and typing Value into the search box at the top of that pane finds "
              "'Value \u20b9 Cr' with a calculator icon beside it.",
        stuck="A missing table means that query was never pasted (Part 1). A missing measure "
              "means Part 3 is unfinished. Neither can be fixed from here, so go back and "
              "finish it — nothing below will work otherwise."))

    S.append(dict(
        title="Set the canvas size",
        page="—",
        do=["Click once on the empty white area of the page (not on a visual).",
            "In the Visualizations pane on the right, click the paintbrush icon.",
            "Click the words 'Canvas settings'.",
            "Set Type to 16:9, then type the Height and Width below into their boxes."],
        fields=[("Height", "720"), ("Width", "1280")],
        note="Every position in these steps assumes this canvas, so do it before anything "
             "else — changing it later moves everything.",
        check="The white page is a wide rectangle and the Canvas settings boxes read "
              "Height 720, Width 1280.",
        stuck="No paintbrush icon means a visual is still selected — press Escape, click the "
              "grey area outside the page, then click the empty white page once."))

    S.append(dict(
        title="Load the colour theme",
        page="—",
        do=["Click the download link just below these steps and save inventory-theme.json "
            "into your Inventory Report folder.",
            "At the top of the window click the View tab.",
            "Click the small arrow under the word Themes to open the list.",
            "Click 'Browse for themes' at the bottom of that list.",
            "Choose the inventory-theme.json file you just saved, and click Open."],
        fields=[], note="This sets all colours, fonts, borders and text sizes, so no step "
                        "below asks you to choose any of them. If you imported an earlier "
                        "copy of this file, download and import it again — the sizes in it "
                        "were lowered so titles and card labels stop being cut off.",
        link="inventory-theme.json",
        check="A message says the theme imported successfully, and the page background turns "
              "a very light grey rather than pure white.",
        stuck="'Invalid theme file' means the download saved as .txt — rename it so it ends "
              ".json and import again. If there is no 'Browse for themes' entry, your Power "
              "BI is an old build: everything still works, it just stays in default colours."))

    S.append(dict(
        title="Create the %d pages" % len(PAGES),
        page="—",
        do=["Look at the very bottom-left of the window: there is a yellow tab called "
            "'Page 1' and a + button next to it.",
            "Click the + button %d times, so there are %d tabs in total."
            % (len(PAGES) - 1, len(PAGES)),
            "Double-click the first tab, type the first name below, and press Enter.",
            "Do the same for the other tabs, in this exact order."],
        fields=[("Page %d" % (i + 1), p) for i, p in enumerate(PAGES)],
        note="Names must match, because later steps say which page to work on.",
        check="%d tabs along the bottom, reading left to right: %s."
              % (len(PAGES), ", ".join(PAGES)),
        stuck="A tab still called 'Page 1' just needs double-clicking and retyping. If a tab "
              "is in the wrong place, drag it sideways."))

    # ---- the furniture on Overview: panel, logo box, wording ---------------------------
    S.extend(_decor_steps())

    # header band, on the pages that still use it
    BAND = BAND_PAGES[0]
    for i, (measure, x, y, w, h, what) in enumerate(CARDS, 1):
        S.append(dict(
            title="Header card %d of %d — %s (on %s)" % (i, len(CARDS), what, BAND),
            page=BAND,
            do=_insert("Card") + [
                _drag(measure, "Fields"),
                "The card now shows one big number.",
                "In the Visualizations pane click the paintbrush icon, then click 'Callout "
                "value' and set Font size to 24. The callout value is the big number "
                "itself.",
                "Now give it a heading. Click General, then Title, switch Title On, and "
                "type the words shown as Title below into the Text box, then set Font size "
                "to 12. The title is drawn in its own strip above the number, so it can "
                "never be cut in half.",
                "Look down the paintbrush list for 'Category label'. If it is there, that "
                "is the small grey wording Power BI prints under the number (it repeats the "
                "measure's name): set its Font size to 10, or switch it off since the title "
                "already says the same thing. If there is no 'Category label' in your list, "
                "you have the newer Card visual, which does not have one — the title you "
                "just typed is the heading, and there is nothing else to set."]
            + _place(x, y, w, h, in_format=True),
            fields=[("Measure", measure), ("Title", what),
                    ("Callout value font size", "24"), ("Title font size", "12"),
                    ("Category label font size (if you have one)", "10")]
                   + _pos_rows(x, y, w, h),
            note="If the number looks wrong, you probably ticked a column instead of the "
                 "measure — measures have a calculator icon.",
            check="The card shows one number with the heading '%s' above it, both readable "
                  "in full, sitting in the top band of the page." % what,
            stuck="'(Blank)' means no data reached it — check that factInventory has rows and "
                  "that no slicer is filtering everything out. A word instead of a number "
                  "means a text column was dropped in: remove it from the Fields box and drag "
                  "the measure instead (calculator icon, not a table icon)."))

    for (field, x, y, w, h, what) in SLICERS:
        multi = field in ("dimDate[MonthName]", "dimDate[Quarter]")
        S.append(dict(
            title="Header slicer — %s (on %s)" % (what, BAND),
            page=BAND,
            do=_insert("Slicer") + [
                _drag(field, "Field"),
                "In the Visualizations pane click the paintbrush icon, then click "
                "'Slicer settings', then 'Options', and set Style to Dropdown."]
               + (["Still under 'Slicer settings', click 'Selection' and switch OFF "
                   "'Multi-select with CTRL'. After that you can tick as many %s as you "
                   "like just by clicking them — no keyboard needed."
                   % ("months" if "Month" in field else "quarters")] if multi else [])
               + _place(x, y, w, h, in_format=True),
            fields=[("Field", field)] + _pos_rows(x, y, w, h),
            note="",
            check="A closed dropdown sits in the header band; clicking it lists the values of "
                  "%s, and clicking one changes the numbers on the cards above." % field,
            stuck="An empty dropdown means the field came from the wrong table — remove it and "
                  "drag %s exactly. A slider instead of a list means a number column was "
                  "used; check the field name again." % field))

    n_band = len(CARDS) + len(SLICERS)
    others = [p for p in BAND_PAGES if p != BAND]
    S.append(dict(
        title="Copy the header band to the other pages",
        page=BAND,
        do=["Click once on the first card. Then hold Ctrl and click each of the other %d "
            "cards and all %d slicers, so %d things are selected at once."
            % (len(CARDS) - 1, len(SLICERS), n_band),
            "Press Ctrl+C.",
            "Click the tab at the bottom for the next page in the list below, then press "
            "Ctrl+V. If Power BI asks about the data, click 'Keep'.",
            "Repeat for every page in the list. The cards land in the same place on each "
            "page, so nothing needs moving."],
        fields=[("Paste on", p) for p in others],
        note="Not on %s — that page is filtered by whatever you clicked to get there, so a "
             "slicer on it would fight the drill-through." % DRILL_PAGE,
        check="These pages now each have the same row of cards and dropdowns across the top, "
              "in the same place: " + ", ".join(others) + ".",
        stuck="If the band lands crooked, do not nudge it by hand — press Ctrl+Z, reselect all "
              "%d items and paste again. If only one card pasted, the Ctrl+click selection was "
              "lost partway; select them all again." % n_band))

    S.append(dict(
        title="Sync the slicers across pages",
        page="—",
        do=["At the top of the window click the View tab, then tick the box called "
            "'Sync slicers'. A new pane opens on the right.",
            "Click once on the Month slicer on the page.",
            "In the 'Sync slicers' pane, tick BOTH boxes (Sync and Visible) on the rows for "
            "these pages: " + ", ".join(BAND_PAGES) + ".",
            "Then click the Quarter slicer and do the same, then the Plant slicer, then the "
            "Category slicer."],
        fields=[], note="Skip this and each page filters on its own, so two pages will show "
                        "different totals for the same month.",
        check="Pick one month on %s, then click through %s — the same month is still picked on "
              "each of them." % (BAND, ", ".join(BAND_PAGES[1:])),
        stuck="If a page ignores the choice, its row in the Sync slicers pane is unticked — "
              "tick both boxes on that row. Leave the %s row unticked everywhere."
              % DRILL_PAGE))

    # one step per visual
    by_page = {}
    for v in VISUALS:
        by_page.setdefault(v[0], []).append(v)

    for page in PAGES:
        vs = by_page.get(page, [])
        for i, (_, vtype, title, wells, pos, why, extra) in enumerate(vs, 1):
            do = ["At the bottom of the window click the tab named %s." % page]
            do += _insert(vtype)
            for wl, fl in wells:
                if wl == "Filters":
                    for f in fl:
                        fld = f.split("  →")[0].strip()
                        val = f.split("→")[-1].strip() if "→" in f else ""
                        if "[" in fld:
                            tbl2, col2 = fld.split("[")[0], fld.split("[")[1].rstrip("]")
                            src = ("open the table called %s in the Data pane and drag the "
                                   "field called %s" % (tbl2, col2))
                        else:
                            src = ("type %s into the search box at the top of the Data pane, "
                                   "then drag it" % fld)
                        v = (val or "").strip()
                        if v.lower().startswith("untick "):
                            act = ("Then untick %s in the list and leave everything else "
                                   "ticked." % v[7:])
                        elif v.lower().startswith("is "):
                            act = ("Then tick %s in the list and untick everything else."
                                   % v[3:])
                        else:
                            act = "Then tick the value shown below and untick everything else."
                        do.append("Now the filter: %s into the Filters pane (that is the pane "
                                  "just to the LEFT of Visualizations), dropping it under the "
                                  "words 'Filters on this visual'. %s" % (src, act))
                else:
                    for f in fl:
                        do.append(_drag(f, wl))
            do += ["In the Visualizations pane click the paintbrush icon, then click "
                   "General, then Title, and type the title shown below into the Text box "
                   "(delete whatever Power BI already put there)."]
            do += _fit(vtype, title)
            do += _place(*pos, in_format=True)
            do += [_plain(e) for e in extra]
            fields = [("Visual", vtype), ("Title", title)]
            for wl, fl in wells:
                fields += [(wl, f) for f in fl]
            fields += _pos_rows(*pos)
            S.append(dict(
                title="%s %d of %d — %s" % (page, i, len(vs), title),
                page=page, do=do, fields=fields, note=why,
                check=_check(vtype, wells), stuck=_stuck(vtype, wells)))

    S.append(dict(
        title="Make clicking a bar open the pie charts",
        page=DRILL_PAGE,
        do=["At the bottom of the window click the tab named %s." % DRILL_PAGE,
            "Click once on the empty grey space around the visuals, so no visual has a "
            "border round it.",
            "Look at the Visualizations pane on the right and scroll it down to the bottom: "
            "there is a box called 'Drill through'.",
            "Drag each of the four fields below out of the Data pane and drop it into that "
            "'Drill through' box, one at a time. (Open the table first by clicking the arrow "
            "next to its name.)",
            "Leave the switch called 'Keep all filters' as it is — it is already on."],
        fields=[("Drill through", f) for f in DRILL_FIELDS],
        check="A round Back arrow has appeared by itself in the top-left corner of the %s "
              "page, and the Drill through box lists all four fields." % DRILL_PAGE,
        stuck="No Drill through box means a visual is still selected — press Escape and click "
              "the grey space outside the page. If a field will not drop in, it came from the "
              "wrong table; the table name is the part before the square bracket.",
        note="This is what makes the report clickable: a Back arrow appears on this page "
             "automatically, and every bar, row and slice on the other pages now offers "
             "Drill through → %s." % DRILL_PAGE))

    S.append(dict(
        title="Try it — click a bar, get the pies",
        page=PAGES[0],
        do=["At the bottom of the window click the tab named %s." % PAGES[0],
            "Right-click one coloured block of the 'Inventory by Month (Rs Cr.)' chart.",
            "Choose Drill through → %s." % DRILL_PAGE,
            "The %s page opens showing only that plant: cards, three pies and the material "
            "list." % DRILL_PAGE,
            "Click the circled Back arrow at the top-left of the %s page to return."
            % DRILL_PAGE],
        fields=[],
        check="The %s page opens and its first card shows a smaller number than the company "
              "total, because it is showing only the plant you clicked." % DRILL_PAGE,
        stuck="'Drill through' greyed out means the four fields are not in the Drill through "
              "box yet — go back one step. If the page opens but shows the full total, you "
              "right-clicked something that is not one of the four drill-through fields; "
              "right-click a coloured block of the month chart instead, or a slice of "
              "'Share by Plant (%)'.",
        note="A left-click filters the rest of the page instead (that is Power BI's built-in "
             "cross-filtering, nothing to set up). Right-click is the one that opens the "
             "pies."))

    S.append(dict(
        title="Choose what a click filters",
        page=PAGES[0],
        do=["Click once on a chart so it has a border round it.",
            "At the top of the window click the Format tab (it only appears when a visual is "
            "selected), then click 'Edit interactions'.",
            "Small icons now sit at the top-right corner of every OTHER visual: a funnel "
            "(filter), a bar chart (highlight) and a circle with a line through it (do "
            "nothing).",
            "For each matrix on the page click the funnel. For each header card click the "
            "circle.",
            "Click 'Edit interactions' again to switch the mode off, then press Ctrl+S."],
        fields=[],
        check="With the mode switched off again, clicking a bar changes the matrix totals but "
              "leaves the header cards unchanged.",
        stuck="If the cards still change, their icon is set to funnel or chart — turn Edit "
              "interactions back on and click the circle-with-a-line icon on each card.",
        note="Default is highlight, which greys out the rest of a bar rather than "
                        "removing it. Set the matrices to filter instead, so a click makes "
                        "their totals match what you clicked. Set the header cards to none, "
                        "so the band always shows the company total."))

    S.append(dict(
        title="Save",
        page="—",
        do=["Press Ctrl+S. If it asks for a name, type Inventory Model and click Save."],
        fields=[],
        check="The window title no longer says 'unsaved'.",
        stuck="If saving fails, the file is open somewhere else or sitting in a folder "
              "OneDrive is mid-sync on — save to the Desktop first, then move it.",
        note="Power BI does not autosave. Save every few steps, not just at the end."))

    S.append(dict(
        title="Check it actually works",
        page="—",
        do=["Pick a month in the header slicer and confirm every page changes with it.",
            "On Summary, the Difference column should be 0.00 (or very close) for every "
            "plant — that is the books agreeing with the stock report.",
            "On FG, 1905 should show blank Days, because it has no capacity row.",
            "Right-click a bar → Drill through → Detail, and check the cards match the bar.",
            "Then Ctrl+S."],
        fields=[],
        check="All five pages react to the month dropdown, Summary's Difference column reads "
              "about 0.00, and right-click → Drill through → %s opens filtered." % DRILL_PAGE,
        stuck="Difference far from zero: a TB file or a Raw file is missing for that month, or "
              "one has been hand-edited. Blank pages: no month is picked in the header "
              "dropdown. The same number on every row of Summary: the two dimCategory "
              "relationships from Part 2 are missing.",
        note="If Difference is large, a source file is missing, duplicated or "
                        "hand-edited — the numbers on every page are wrong until that is "
                        "fixed. The qc* queries are still in the model if you want to put "
                        "them on a page of their own to see why."))
    return S


def part4_markdown():
    L = ["# PART 4 — Build the pages", "",
         "Each visual is spelled out the same way: what to insert, which field goes in which",
         "well, and the four numbers that place it on a %d x %d canvas." % (W, H),
         "",
         "> Prefer one instruction at a time? Use the **Build it** tab — same content, "
         "one step per screen, with a Next button.",
         "",
         "**To place any visual:** select it → Format pane → General → Properties → open",
         "**Size** and **Position** → type Width, Height, **Horizontal** (this is X) and",
         "**Vertical** (this is Y). Older versions put all four under **Size and style**.", "",
         "**What the Format pane calls things.** Every name below is a heading you click in",
         "the paintbrush pane. If a heading is not in your list, your version does not have",
         "it — skip that line, nothing else changes.", "",
         "| Name in the Format pane | What it actually is |",
         "|---|---|",
         "| Callout value | the one big number on a card |",
         "| Category label | the small grey words *under* the number on a card, which repeat "
         "the measure's name. The newer Card visual has none |",
         "| Title | the heading strip along the top of any visual, which you type yourself |",
         "| Column headers | the headings across the top of a matrix or table |",
         "| Row headers | the names down the left of a matrix, where the +/− signs live |",
         "| Values | the numbers in the body of a matrix or table |",
         "| Detail labels | the numbers or words written on the slices of a pie or donut |",
         "| Legend | the small colour key that names each colour |",
         "| X-axis | the labels along the bottom of a chart |",
         "| Y-axis | the number scale up the side of a chart |",
         "| Data labels | numbers printed on top of the bars themselves |",
         "| Grid | the lines between matrix rows, and the row height |", "",
         "**4.0 Canvas and theme, before anything else.**", "",
         "1. Click empty canvas → Format pane → Canvas settings → Type 16:9, "
         "Height %d, Width %d." % (H, W),
         "2. Download [inventory-theme.json](inventory-theme.json) (right-click → Save link as).",
         "3. Ribbon **View** → **Themes** → **Browse for themes** → pick that file.", "",
         "Colours, fonts, borders and card styling all come from the theme, so nothing below",
         "asks you to colour anything.", "",
         "**Create the %d pages** with the **+** at the bottom, named: " % len(PAGES) +
         " · ".join("`%s`" % p for p in PAGES) + ".", "",
         "---", "", "## The furniture on `Overview` (no data in any of it)", "",
         "| What | Insert it with | Text / fill | Horizontal (X) | Vertical (Y) | Width | "
         "Height |", "|---|---|---|---|---|---|---|"] + \
        ["| %s | Insert → %s | %s | %d | %d | %d | %d |"
         % ("the green panel" if k == "Rectangle" else
            ("the logo box" if k == "Image" else "text '%s'" % t),
            "Shapes → Rectangle" if k == "Rectangle" else k,
            PANEL if k == "Rectangle" else ("any picture for now" if k == "Image"
                                            else "%s, %s" % (FONT, PANEL_INK if h >= 28
                                                             else PANEL_SUB)),
            x, y, w, h)
         for (pg, k, t, x, y, w, h, note) in DECOR if pg == "Overview"] + \
        ["",
         "Build the rectangle first and **right-click → Send to back**; everything else on",
         "the panel sits on top of it. Each card on the panel then has **General → Effects →",
         "Background: Off**, so the green shows through and the nine figures read as one",
         "block.", "",
         "---", "", "## The header band — build once on %s, then copy" % BAND_PAGES[0], "",
         "**4.1** %d **Card** visuals (**Insert → Card**), one measure each:" % len(CARDS), "",
         "| Card | Measure | Horizontal (X) | Vertical (Y) | Width | Height |", "|---|---|---|---|---|---|"]
    for i, (m, x, y, w, h, what) in enumerate(CARDS, 1):
        L.append("| %d — %s | `%s` | %d | %d | %d | %d |" % (i, what, m, x, y, w, h))
    L += ["",
          "For each card: **Callout value** → Font size **24**; **General → Title** → On,",
          "Text = the wording in the Card column above, Font size **12**; and if your version",
          "has a **Category label**, Font size **10** or switch it off (the newer Card visual",
          "has none).", "",
          "**4.2** %d **Slicer** visuals (**Insert → Slicer**), each set to" % len(SLICERS),
          "**Format → Slicer settings → Style: Dropdown**:", "",
          "| Slicer | Field | Horizontal (X) | Vertical (Y) | Width | Height |", "|---|---|---|---|---|---|"]
    for (f, x, y, w, h, what) in SLICERS:
        L.append("| %s | `%s` | %d | %d | %d | %d |" % (what, f, x, y, w, h))
    L += ["", "**4.3** Select all %d → **Ctrl+C** → **Ctrl+V** on %s. Positions come with "
          "them." % (len(CARDS) + len(SLICERS),
                     ", ".join("`%s`" % p for p in BAND_PAGES if p != BAND_PAGES[0])), "",
          "Not on `%s` — it is filtered by whatever you clicked to get there. Not on "
          "`Overview` either: that page has its own controls, and its left-hand panel is "
          "meant to ignore them." % DRILL_PAGE, "",
          "**4.4** Ribbon **View** → tick **Sync slicers**; for each slicer tick **Sync** and",
          "**Visible** on " + ", ".join("`%s`" % p for p in BAND_PAGES) + ". Without it, two",
          "pages can disagree about the same month.", ""]

    by_page = {}
    for v in VISUALS:
        by_page.setdefault(v[0], []).append(v)
    n = 4
    for page in PAGES:
        L += ["---", "", "## Page — %s" % page, ""]
        for (_, vtype, title, wells, pos, why, extra) in by_page.get(page, []):
            n += 1
            L += ["**4.%d** **%s** — %s" % (n, vtype, why), "",
                  "| Well | Field |", "|---|---|"]
            for wl, fl in wells:
                L.append("| %s | %s |" % (wl, ", ".join("`%s`" % f for f in fl)))
            L += ["", "Title: `%s`" % title,
                  "", "Position: Horizontal %d, Vertical %d, Width %d, Height %d." % pos,
                  ""]
            for e in _fit(vtype, title) + [_plain(x) for x in extra]:
                L += ["- %s" % e]
            L.append("")

    L += ["---", "", "## Making it clickable", "",
          "**4.%d Drill through.** On the `%s` page click the empty area around the visuals "
          "so" % (n + 1, DRILL_PAGE),
          "nothing is selected, then drag these into the **Drill through** well of the",
          "Visualizations pane (leave *Keep all filters* on):", ""]
    for f in DRILL_FIELDS:
        L.append("- `%s`" % f)
    L += ["",
          "That is the whole trick. A **Back** arrow appears on `%s` by itself, and every bar,"
          % DRILL_PAGE,
          "row and slice on the other pages now offers **right-click → Drill through → `%s`**,"
          % DRILL_PAGE,
          "which opens the pies filtered to whatever was clicked.", "",
          "**4.%d Interactions.** A *left*-click needs no setup — it already cross-filters "
          "the rest" % (n + 2),
          "of the page. To change what it does: select a visual → ribbon **Format** →",
          "**Edit interactions**, then on each other visual pick **filter** (funnel),",
          "**highlight** (chart) or **none**.", "",
          "Worth setting deliberately: matrices to **filter** (so their totals match the "
          "click),",
          "and the header cards to **none** (so the band always shows the company total).", "",
          "---", ""]
    return "\n".join(L)
