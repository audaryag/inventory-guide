"""Turns spec.py into (a) guided one-at-a-time steps and (b) the PART 4 markdown."""
from spec import (CANVAS, PAGES, CARDS, SLICERS, VISUALS, DRILL_PAGE, DRILL_FIELDS,
                  BAND_PAGES)

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
        return ("In the Data pane (far right), click the little arrow to the left of %s to "
                "open it, then drag %s and drop it into the box called %s."
                % (tbl, col, well))
    return ("In the Data pane (far right), find %s — it has a small calculator icon next to "
            "it — and drag it into the box called %s." % (field, well))


def _insert(vtype):
    return ["Click once on an empty white part of the page, so that no visual has a border "
            "round it.",
            "In the Visualizations pane on the right (the grid of small icons), click %s. "
            "An empty visual appears on the page." % ICON.get(vtype, "the %s icon" % vtype)]


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
    first = ("Still in the same pane, click the word General, then Properties, then "
             "Size and style."
             if in_format else
             "In the Visualizations pane click the paintbrush icon, then click General, "
             "then Properties, then Size and style.")
    return [first,
            "Type the four numbers below into Height, Width, Horizontal (X) and "
            "Vertical (Y), pressing Tab after each one."]


def _pos_rows(x, y, w, h):
    return [("X", str(x)), ("Y", str(y)), ("Width", str(w)), ("Height", str(h))]


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
                        "finished — go back to Part 1-3 rather than guessing."))

    S.append(dict(
        title="Set the canvas size",
        page="—",
        do=["Click once on the empty white area of the page (not on a visual).",
            "In the Visualizations pane on the right, click the paintbrush icon.",
            "Click the words 'Canvas settings'.",
            "Set Type to 16:9, then type the Height and Width below into their boxes."],
        fields=[("Height", "720"), ("Width", "1280")],
        note="Every position in these steps assumes this canvas, so do it before anything "
             "else — changing it later moves everything."))

    S.append(dict(
        title="Load the colour theme",
        page="—",
        do=["Click the download link just below these steps and save inventory-theme.json "
            "into your Inventory Report folder.",
            "At the top of the window click the View tab.",
            "Click the small arrow under the word Themes to open the list.",
            "Click 'Browse for themes' at the bottom of that list.",
            "Choose the inventory-theme.json file you just saved, and click Open."],
        fields=[], note="This sets all colours, fonts, borders and card styling, so no step "
                        "below asks you to colour anything.", link="inventory-theme.json"))

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
        note="Names must match, because later steps say which page to work on."))

    # header band
    for i, (measure, x, y, w, h, what) in enumerate(CARDS, 1):
        S.append(dict(
            title="Header card %d of %d — %s" % (i, len(CARDS), what),
            page=PAGES[0],
            do=_insert("Card") + [
                _drag(measure, "Fields"),
                "The card now shows one big number."] + _place(x, y, w, h),
            fields=[("Measure", measure)] + _pos_rows(x, y, w, h),
            note="If the number looks wrong, you probably ticked a column instead of the "
                 "measure — measures have a calculator icon."))

    for (field, x, y, w, h, what) in SLICERS:
        multi = field in ("dimDate[MonthName]", "dimDate[Quarter]")
        S.append(dict(
            title="Header slicer — %s" % what,
            page=PAGES[0],
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
            note=""))

    n_band = len(CARDS) + len(SLICERS)
    others = [p for p in BAND_PAGES if p != PAGES[0]]
    S.append(dict(
        title="Copy the header band to the other pages",
        page=PAGES[0],
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
             "slicer on it would fight the drill-through." % DRILL_PAGE))

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
                        "different totals for the same month."))

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
                        do.append("Drag %s into the Filters pane (the pane just left of "
                                  "Visualizations, under the words 'Filters on this visual'), "
                                  "then tick %s and untick everything else."
                                  % (fld, val or "the value shown below"))
                else:
                    for f in fl:
                        do.append(_drag(f, wl))
            do += ["In the Visualizations pane click the paintbrush icon, then click "
                   "General, then Title, and type the title shown below into the Text box "
                   "(delete whatever Power BI already put there)."]
            do += _place(*pos, in_format=True)
            do += [_plain(e) for e in extra]
            fields = [("Visual", vtype), ("Title", title)]
            for wl, fl in wells:
                fields += [(wl, f) for f in fl]
            fields += _pos_rows(*pos)
            S.append(dict(
                title="%s %d of %d — %s" % (page, i, len(vs), title),
                page=page, do=do, fields=fields, note=why))

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
        note="This is what makes the report clickable: a Back arrow appears on this page "
             "automatically, and every bar, row and slice on the other pages now offers "
             "Drill through → %s." % DRILL_PAGE))

    S.append(dict(
        title="Try it — click a bar, get the pies",
        page=PAGES[0],
        do=["At the bottom of the window click the tab named %s." % PAGES[0],
            "Right-click one bar of the 'Value ₹ Cr by plant' chart.",
            "Choose Drill through → %s." % DRILL_PAGE,
            "The %s page opens showing only that plant: cards, three pies and the material "
            "list." % DRILL_PAGE,
            "Click the circled Back arrow at the top-left of the %s page to return."
            % DRILL_PAGE],
        fields=[], note="A left-click filters the rest of the page instead (that is Power "
                        "BI's built-in cross-filtering, nothing to set up). Right-click is "
                        "the one that opens the pies."))

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
        fields=[], note="Default is highlight, which greys out the rest of a bar rather than "
                        "removing it. Set the matrices to filter instead, so a click makes "
                        "their totals match what you clicked. Set the header cards to none, "
                        "so the band always shows the company total."))

    S.append(dict(
        title="Save",
        page="—",
        do=["Press Ctrl+S. If it asks for a name, type Inventory Model and click Save."],
        fields=[], note="Power BI does not autosave. Save every few steps, not just at "
                        "the end."))

    S.append(dict(
        title="Check it actually works",
        page="—",
        do=["Pick a month in the header slicer and confirm every page changes with it.",
            "On Summary, the Difference column should be 0.00 (or very close) for every "
            "plant — that is the books agreeing with the stock report.",
            "On FG, 1905 should show blank Days, because it has no capacity row.",
            "Right-click a bar → Drill through → Detail, and check the cards match the bar.",
            "Then Ctrl+S."],
        fields=[], note="If Difference is large, a source file is missing, duplicated or "
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
         "**To place any visual:** select it → Format pane → General → Properties →",
         "**Size and style** → type X, Y, Width, Height.", "",
         "**4.0 Canvas and theme, before anything else.**", "",
         "1. Click empty canvas → Format pane → Canvas settings → Type 16:9, "
         "Height %d, Width %d." % (H, W),
         "2. Download [inventory-theme.json](inventory-theme.json) (right-click → Save link as).",
         "3. Ribbon **View** → **Themes** → **Browse for themes** → pick that file.", "",
         "Colours, fonts, borders and card styling all come from the theme, so nothing below",
         "asks you to colour anything.", "",
         "**Create the %d pages** with the **+** at the bottom, named: " % len(PAGES) +
         " · ".join("`%s`" % p for p in PAGES) + ".", "",
         "---", "", "## The header band — build once on %s, then copy" % PAGES[0], "",
         "**4.1** %d **Card** visuals (**Insert → Card**), one measure each:" % len(CARDS), "",
         "| Card | Measure | X | Y | Width | Height |", "|---|---|---|---|---|---|"]
    for i, (m, x, y, w, h, what) in enumerate(CARDS, 1):
        L.append("| %d — %s | `%s` | %d | %d | %d | %d |" % (i, what, m, x, y, w, h))
    L += ["", "**4.2** %d **Slicer** visuals (**Insert → Slicer**), each set to" % len(SLICERS),
          "**Format → Slicer settings → Style: Dropdown**:", "",
          "| Slicer | Field | X | Y | Width | Height |", "|---|---|---|---|---|---|"]
    for (f, x, y, w, h, what) in SLICERS:
        L.append("| %s | `%s` | %d | %d | %d | %d |" % (what, f, x, y, w, h))
    L += ["", "**4.3** Select all %d → **Ctrl+C** → **Ctrl+V** on %s. Positions come with "
          "them." % (len(CARDS) + len(SLICERS),
                     ", ".join("`%s`" % p for p in BAND_PAGES if p != PAGES[0])), "",
          "Not on `%s` — it is filtered by whatever you clicked to get there." % DRILL_PAGE, "",
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
                  "", "Position: X %d, Y %d, W %d, H %d." % pos, ""]
            for e in extra:
                L += ["- %s" % e]
            if extra:
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
