"""Fixes for a report that is already built, newest first.

Each entry names one query and hands over its **whole** code, taken live out of
BUILD_GUIDE.md so the two can never drift apart: click the query, Advanced Editor,
Ctrl+A, paste, Done. No hunting for a line inside a query and no partial edits.
Everything here is already in the generated download, so a fresh copy needs none of it.
"""

import html

# query name -> why it changed. Order is the order to paste them in.
EDITS = [
    dict(n="0a", build="23", query="factTB_Staged",
         title="Inventory (TB) missing plant 1905, and missing its Raw Material row",
         why="Two faults, both on the TB side only \u2014 MB5B was never involved. <strong>The "
             "plant:</strong> a trial balance row carries a profit centre, not a plant, and the "
             "old code read the plant out of characters 3\u20136 of it and nowhere else. A "
             "profit centre written to any other pattern therefore resolved to no plant, and "
             "the row was dropped \u2014 which is how one plant disappears from Inventory (TB) "
             "while MB5B still shows it. Now: those four characters first, then the first of "
             "1900 / 1902 / 1905 appearing <em>anywhere</em> in the profit centre, then in its "
             "description, then the Plant or Nature written against that GL on your "
             "<strong>TB Master</strong> sheet. <strong>The RM row:</strong> the category test "
             "asked about consumables before raw material, and an account called \"Raw "
             "Material &amp; Packing\" contains the word PACK \u2014 so the whole of RM was "
             "filed as Consumables, the RM row vanished and Consumables read far too high. Raw "
             "material is now tested first. Nothing is dropped silently any more: "
             "<strong>qcTBPlants</strong> on Checks lists every profit centre, what it resolved "
             "to and what it is worth, so an unresolved one can be read off the screen instead "
             "of guessed at."),
    dict(n="0b", build="23", query="factTB",
         title="Same fix, second half \u2014 the RM / FG / Consumables split and the plant filter",
         why="Paste this straight after the one above; they are one change in two queries. Raw "
             "material is tested before consumables here, and the rows that resolve to none of "
             "the three plants are left out at this step rather than the one before it, so "
             "qcTBPlants can still account for them. There is still no Unallocated plant."),
    dict(n="0c", build="23", query="qcTBPlants",
         title="New self-check \u2014 every TB profit centre and the plant it resolved to",
         why="A brand new query, so create it rather than replace it: Power Query \u2192 Home "
             "\u2192 New Source \u2192 Blank Query \u2192 Advanced Editor \u2192 paste \u2192 "
             "Done \u2192 rename it exactly <code>qcTBPlants</code>, and leave Enable load "
             "<strong>on</strong>. It is the table that answers \"why is that plant not on the "
             "TB side\" without either of us guessing: a blank or (none) under PlantResolved is "
             "a row Inventory (TB) leaves out, and the amount beside it is exactly what is "
             "missing. Read me those profit centre codes and the rule becomes exact."),
    dict(n="0", build="22", query="",
         title="Empty tables, and no months under TB / MB5B / Difference \u2014 take the "
               "download for this one",
         why="One fault behind both: a matrix with <em>two</em> fields in Columns, a metric "
             "above the month. Power BI opens such a matrix on its outer level only \u2014 one "
             "figure per metric and no month history, which is why ticking months changed a "
             "single number instead of adding columns \u2014 and where the file tries to "
             "pre-open it, Desktop draws the visual as an empty card, which is what emptied "
             "Summary's lower block and the FG and RM tables. Build 22 stops nesting: each "
             "metric gets its own matrix with <code>dimDate[MonthName]</code> as the only "
             "field in Columns, laid out side by side \u2014 an <strong>In MW</strong> block, "
             "an <strong>In Rs Cr</strong> block and an <strong>In Days</strong> block on FG, "
             "In Rs Cr and In Days on RM, and TB / as per MB5B / Check on Summary, each over "
             "its own row of months. That is the layout of the Excel sheets these pages "
             "replace. Column subtotals are off everywhere too: inventory is a level, not a "
             "flow, so there is no Total column adding March to July \u2014 the Total row, "
             "which adds the plants inside one month, stays.",
         steps=[
             "This one is ten new visuals across three pages, so doing it by hand is not "
             "worth your evening: take the download on the <strong>Auto</strong> tab. Every "
             "query fix on this page is already inside it, so nothing you pasted is lost.",
             "If you do want to do it by hand: on each existing matrix, drag "
             "<code>dimMetric[Metric]</code> (or <code>dimMeasure[Measure]</code>) out of the "
             "Columns box so only <code>dimDate[MonthName]</code> is left, put a "
             "<strong>single</strong> measure in Values, then copy-paste the visual once per "
             "extra metric and swap that measure. Format pane \u2192 Subtotals \u2192 Column "
             "subtotals: Off on each.",
             "Leave <code>In Summary Window is 1</code> in the Filters pane exactly as it is: "
             "that is what holds the columns to the newest March plus the three months after "
             "it until you tick months yourself.",
             "Overview and Detail are untouched.",
         ],
         find="", repl=""),
    dict(n="1", build="20", query="dimTBMaster",
         title="Errors in dimTBMaster \u2014 the TB whitelist erroring on every one of its rows",
         why="A forced type cast. <code>Int64.Type</code> on the sort column, and "
             "<code>type text</code> on the rest, error the whole row when one cell holds a "
             "blank, a dash, a number stored as text, or 1.5 \u2014 and Power BI then reports "
             "<em>Errors in dimTBMaster</em>. What is lost is the whitelist of inventory GL "
             "accounts, so Inventory (TB) reads empty and Difference reads as minus MB5B. Every "
             "column is now converted cell by cell with a fallback, so an untidy cell becomes a "
             "blank instead of an error. A spreadsheet typed by hand is allowed to be untidy; "
             "the report has to cope with it."),
    dict(n="2", build="20", query="dimMaterialAttr",
         title="The RM master \u2014 same cure, so one loosely typed cell cannot cost every nature",
         why="This is the query that reads your <strong>RM Nature</strong> sheet (there is no "
             "query called RM Master). <code>BOM Std Qty</code> cast straight to a number errors "
             "the row when the cell holds text, a dash or a stray space, and an errored row "
             "carries no nature, no group nature and no MW with it."),
    dict(n="3", build="20", query="varConstants",
         title="The Constants sheet \u2014 it carries the RM megawatt factor",
         why="If the 580 is typed as text, or an Effective From cell is not a date, the row "
             "errors and RM MW comes out blank across the whole report."),
    dict(n="4", build="19", query="factTB_Staged",
         title="The trial balance now reads the folder and the TB Master whitelist in one query",
         why="This is the fix for <em>\u201creferences other queries or steps, so it may not "
             "directly access a data source\u201d</em> on factTB. A query may open as many "
             "sources as it likes; it may not lean on another query for data and reach a source "
             "as well. Doing the whitelist join here, where the TB folder is already being read, "
             "removes that pairing altogether. It also carries the safe conversion of the "
             "<code>Amount</code> column, so an amount typed with a comma or a dash for nil "
             "cannot error its row."),
    dict(n="5", build="19", query="factTB",
         title="\u2026 so factTB reads nothing but the staged table",
         why="It keeps the rows the whitelist matched, using the <code>Whitelisted</code> flag "
             "set in factTB_Staged, and works out RM / FG / Consumables from the Nature text. "
             "Paste this <strong>after</strong> #4, since it needs that flag to exist. It also "
             "no longer keeps every TB row when TB Master matches nothing \u2014 that fallback "
             "was reading Buildings and Plant &amp; Machinery as raw-material inventory."),
    dict(n="6", build="19", query="factTB_Unmapped",
         title="\u2026 and so does the list of GL accounts TB Master does not cover",
         why="Reads the same flag, so the two can never disagree about which account counted."),
    dict(n="7", build="19", query="",
         title="&ldquo;references other queries or steps, so it may not directly access a data "
               "source&rdquo; \u2014 a dozen queries blocked at once",
         why="Power Query's privacy firewall refusing to let a folder source and the "
             "<code>Variables and Calculations</code> workbook meet \u2014 which is the whole "
             "design, since the figures come from the folders and the names come from the "
             "workbook. It is not a fault in any query and cannot be coded around: two sources "
             "have to meet somewhere. Turn the firewall off for your own files, once: "
             "<strong>File &rarr; Options and settings &rarr; Options &rarr; GLOBAL &rarr; "
             "Privacy &rarr; tick &ldquo;Always ignore Privacy Level settings&rdquo; &rarr; "
             "OK</strong>, then the same under <strong>CURRENT FILE &rarr; Privacy</strong>, "
             "then Refresh. The Global one covers every file you open afterwards, so this is the "
             "last time it will bite."),
]

HOWTO = ("Newest first. Each one is a <strong>whole query</strong>: in Power Query click the "
         "query named on the card, <strong>Home &rarr; Advanced Editor</strong>, "
         "<strong>Ctrl+A</strong>, <strong>Delete</strong>, paste, <strong>Done</strong>. "
         "Nothing to hunt for and nothing to match up. Do them in the order shown \u2014 #5 and "
         "#6 read a column that #4 creates \u2014 and press <strong>Close &amp; Apply</strong> "
         "once at the end. Red error text between pastes is normal. Every one of these is "
         "already inside the download on the <strong>Auto</strong> tab, so a fresh copy needs "
         "none of them.")


def edit_cards(qcode):
    """The Edits tab's HTML. qcode maps query name -> its full M code from the guide."""
    out = []
    for e in EDITS:
        name, body = e["query"], ""
        if e.get("steps"):
            body = "<ul class='elist'>" + "".join("<li>%s</li>" % x for x in e["steps"]) + "</ul>"
        if name:
            code = qcode.get(name)
            if code is None:
                raise SystemExit("edits.py names a query the guide does not define: " + name)
            body = ("<p class='note'>Power Query &rarr; click <strong>%s</strong> in the list on "
                    "the left &rarr; <strong>Home &rarr; Advanced Editor</strong> &rarr; "
                    "<strong>Ctrl+A</strong> &rarr; <strong>Delete</strong> &rarr; paste this "
                    "&rarr; <strong>Done</strong>.</p>"
                    "<button class='copy' data-target='ecode%s'>Copy the whole query</button>"
                    "<pre id='ecode%s'>%s</pre>"
                    % (html.escape(name), e["n"], e["n"], html.escape(code)))
        out.append(
            '<section class="card" id="e-%s" data-name="%s">\n'
            '  <header><span class="num">%s</span><h3>%s</h3>'
            '<button class="done" data-key="e-%s">Done</button></header>\n'
            '  <p class="note"><strong>Why:</strong> %s</p>\n  %s\n</section>'
            % (e["n"], html.escape(name or "privacy setting").lower(), e["n"], e["title"],
               e["n"], e["why"], body))
    return "\n".join(out)
