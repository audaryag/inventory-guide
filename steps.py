"""Turns spec.py into (a) guided one-at-a-time steps and (b) the PART 4 markdown."""
from spec import (CANVAS, PAGES, CARDS, SLICERS, VISUALS, DRILL_PAGE, DRILL_FIELDS,
                  BAND_PAGES)

W, H = CANVAS


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
            "If a name below does not exist in the Fields pane on the right, that part is not "
            "finished — go back to the guide's Part 1-3 rather than guessing."],
        fields=[], note=""))

    S.append(dict(
        title="Set the canvas size",
        page="—",
        do=["Click on the empty white area of the report (not on a visual).",
            "Open the Format pane: the paintbrush icon on the right.",
            "Open Canvas settings.",
            "Set Type to 16:9, then type the height and width below."],
        fields=[("Height", "720"), ("Width", "1280")],
        note="Every position in these steps assumes this canvas, so do it before anything "
             "else — changing it later moves everything."))

    S.append(dict(
        title="Load the colour theme",
        page="—",
        do=["Click the download link just below these steps to save inventory-theme.json "
            "(put it in your Inventory Report folder).",
            "Ribbon: View → Themes (dropdown) → Browse for themes.",
            "Pick the file you just saved."],
        fields=[], note="This sets all colours, fonts, borders and card styling, so no step "
                        "below asks you to colour anything.", link="inventory-theme.json"))

    S.append(dict(
        title="Create the %d pages" % len(PAGES),
        page="—",
        do=["At the bottom of the window, click the + button %d times." % len(PAGES),
            "Double-click each tab and rename it, in this order."],
        fields=[("Page %d" % (i + 1), p) for i, p in enumerate(PAGES)],
        note="Names must match, because later steps say which page to work on."))

    # header band
    for i, (measure, x, y, w, h, what) in enumerate(CARDS, 1):
        S.append(dict(
            title="Header card %d of %d — %s" % (i, len(CARDS), what),
            page=PAGES[0],
            do=["Ribbon: Insert → Card. A blank card appears.",
                "In the Fields pane on the right, find the measure named below and tick it "
                "(or drag it onto the card).",
                "With the card still selected: Format pane → General → Properties → "
                "Size and style, and type the four numbers."],
            fields=[("Measure", measure)] + _pos_rows(x, y, w, h),
            note="If the number looks wrong, you probably ticked a column instead of the "
                 "measure — measures have a calculator icon."))

    for (field, x, y, w, h, what) in SLICERS:
        S.append(dict(
            title="Header slicer — %s" % what,
            page=PAGES[0],
            do=["Ribbon: Insert → Slicer.",
                "Drag the field below into it.",
                "Format pane → Slicer settings → Style: Dropdown.",
                "For the Month and Quarter slicers also turn on Format pane → Slicer "
                "settings → Selection → Multi-select with Ctrl: Off, so ticking several "
                "months needs no keyboard.",
                "Then set the position numbers."],
            fields=[("Field", field)] + _pos_rows(x, y, w, h),
            note=""))

    n_band = len(CARDS) + len(SLICERS)
    others = [p for p in BAND_PAGES if p != PAGES[0]]
    S.append(dict(
        title="Copy the header band to the other pages",
        page=PAGES[0],
        do=["Click the first card, then Ctrl+click the other %d cards and all %d slicers "
            "(%d things selected)." % (len(CARDS) - 1, len(SLICERS), n_band),
            "Ctrl+C.",
            "Go to each page listed below and press Ctrl+V."],
        fields=[("Paste on", p) for p in others],
        note="Not on %s or %s: %s is filtered by whatever you clicked to get there, and "
             "%s must never be filtered or it stops being a check."
             % (DRILL_PAGE, "Data Quality", DRILL_PAGE, "Data Quality")))

    S.append(dict(
        title="Sync the slicers across pages",
        page="—",
        do=["Ribbon: View → tick Sync slicers. A pane opens on the right.",
            "Click the Month slicer, then tick both Sync and Visible for these pages: "
            + ", ".join(BAND_PAGES) + ".",
            "Do the same for the Quarter, Plant and Category slicers."],
        fields=[], note="Skip this and each page filters on its own, so two pages will show "
                        "different totals for the same month."))

    # one step per visual
    by_page = {}
    for v in VISUALS:
        by_page.setdefault(v[0], []).append(v)

    for page in PAGES:
        vs = by_page.get(page, [])
        for i, (_, vtype, title, wells, pos, why, extra) in enumerate(vs, 1):
            do = ["Go to the %s page." % page,
                  "Ribbon: Insert → %s." % vtype,
                  "Drop each field below into the well named next to it. Fields come from the "
                  "Fields pane on the right; drag them into the wells in the Visualizations "
                  "pane."]
            if any(wl == "Filters" for wl, _ in wells):
                do.append("For the Filters row: drag that field into the Filters pane (right "
                          "edge), then tick the value shown.")
            do.append("Set the title: Format pane → General → Title → type the title below.")
            do.append("Set the position: Format pane → General → Properties → Size and style.")
            do += extra
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
        do=["Go to the %s page and click the empty grey area around the visuals, so that "
            "nothing is selected." % DRILL_PAGE,
            "In the Visualizations pane, find the well called Drill through (scroll down; "
            "it is below Filters on this page).",
            "Drag each field below from the Fields pane into that Drill through well, "
            "one at a time.",
            "Leave 'Keep all filters' ON — it is on by default."],
        fields=[("Drill through", f) for f in DRILL_FIELDS],
        note="This is what makes the report clickable: a Back arrow appears on this page "
             "automatically, and every bar, row and slice on the other pages now offers "
             "Drill through → %s." % DRILL_PAGE))

    S.append(dict(
        title="Try it — click a bar, get the pies",
        page=PAGES[0],
        do=["Go to the %s page." % PAGES[0],
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
        do=["Click any chart once to select it.",
            "Ribbon: Format → Edit interactions. Small icons appear on every other visual.",
            "Each other visual now offers filter (funnel), highlight (chart) or none "
            "(circle with a line). Click the one you want.",
            "Click Edit interactions again to turn the mode off."],
        fields=[], note="Default is highlight, which greys out the rest of a bar rather than "
                        "removing it. Set the matrices to filter instead, so a click makes "
                        "their totals match what you clicked. Set the header cards to none, "
                        "so the band always shows the company total."))

    S.append(dict(
        title="Save",
        page="—",
        do=["Ctrl+S. If it asks for a name, call it Inventory Model.pbix."],
        fields=[], note="Power BI does not autosave. Save every few steps, not just at "
                        "the end."))

    S.append(dict(
        title="Check it actually works",
        page="Data Quality",
        do=["Look at the Data Quality page.",
            "Stock reconciliation must read 0.",
            "Rows missing master attributes should read 0.",
            "Both tables (unmapped GLs, Natures with no capacity) should be empty.",
            "Then pick a month in the header slicer and confirm every page changes."],
        fields=[], note="If any of those four is wrong, the numbers on the other pages are "
                        "wrong too — fix it before showing anyone."))
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
          "Not on `%s` (it is filtered by whatever you clicked to get there) or "
          "`Data Quality` (a filtered check is not a check)." % DRILL_PAGE, "",
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
