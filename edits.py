"""Fixes for a report that is already built, newest first.

Each entry names one query and hands over its **whole** code, taken live out of
BUILD_GUIDE.md so the two can never drift apart: click the query, Advanced Editor,
Ctrl+A, paste, Done. No hunting for a line inside a query and no partial edits.
Everything here is already in the generated download, so a fresh copy needs none of it.
"""

import html

# query name -> why it changed. Order is the order to paste them in.
EDITS = [
    dict(n="0", build="21", query="",
         title="Blank matrices, and no months under TB / MB5B / Difference \u2014 six visuals to "
               "correct by hand",
         why="Two faults with one cause: a matrix with <em>two</em> fields in Columns. Power BI "
             "opens such a matrix on the outer level only \u2014 one figure per metric, no months "
             "\u2014 and where the file tries to pre-open it, Desktop draws the visual as an empty "
             "card instead, which is why Summary's lower block and the FG and RM tables were "
             "missing altogether. The cure is to stop nesting: <strong>one</strong> field in "
             "Columns (the month) and the metrics as measures side by side underneath, which is "
             "the same grid read the other way and needs no expanding. On each of the six "
             "matrices below: click it, and in the Visualizations pane drag "
             "<code>dimMetric[Metric]</code> (or <code>dimMeasure[Measure]</code>) out of the "
             "Columns box, leaving <code>dimDate[MonthName]</code> alone in there. Then remove "
             "the single measure from Values and drag these in instead, in order \u2014 and "
             "double-click each one in the Values box to type the short name over it, because "
             "that is what the column heading reads.",
         steps=[
             "<strong>Summary</strong>, both matrices \u2014 Values: <code>TB Inventory Rs Cr</code> "
             "renamed <strong>TB</strong>, <code>Inventory Rs Cr</code> renamed "
             "<strong>MB5B</strong>, <code>Difference Inventory Rs Cr</code> renamed "
             "<strong>Difference</strong>. Drop <code>Summary Value Rs Cr</code>.",
             "<strong>FG</strong>, both matrices \u2014 Values: <code>Inventory MW</code> renamed "
             "<strong>MW</strong>, <code>Inventory Rs Cr</code> renamed <strong>Rs Cr.</strong>, "
             "<code>Days</code> renamed <strong>Days</strong>. Drop "
             "<code>Unit Value by Period</code>.",
             "<strong>RM</strong>, both matrices \u2014 Values: <code>Inventory Rs Cr</code> renamed "
             "<strong>Rs Cr.</strong>, <code>Days</code> renamed <strong>Days</strong>. Drop "
             "<code>Unit Value by Period</code>, and remove the <code>dimMeasure[Measure]</code> "
             "entry from the Filters pane as well \u2014 it has nothing left to filter.",
             "Then click each of the six, and in the Filters pane leave "
             "<code>In Summary Window is 1</code> exactly as it is: that is what holds the "
             "columns to the newest March plus the three months after it until you tick months "
             "yourself.",
             "Everything else on those pages stays put. If you would rather not do it by hand, "
             "the download on the <strong>Auto</strong> tab is already built this way.",
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
