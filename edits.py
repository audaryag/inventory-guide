"""Fixes to paste into a report that is already built, newest first.

Each entry is a find-and-replace inside one query's Advanced Editor, so a report that
already exists can be corrected without rebuilding anything and without anyone having to
type M code out of a chat message. Everything here is already in the generated download,
so a fresh copy needs none of it.
"""

import html

EDITS = [
    dict(
        n="1", build="20", query="dimTBMaster",
        title="Errors in dimTBMaster \u2014 the TB whitelist erroring on every one of its rows",
        why="A forced type cast. <code>Int64.Type</code> on the sort column, and "
            "<code>type text</code> on the rest, error the whole row when one cell holds a "
            "blank, a dash, a number stored as text, or 1.5 \u2014 and Power BI then reports "
            "<em>Errors in dimTBMaster</em>. The whitelist of inventory GL accounts is what is "
            "lost, so Inventory (TB) reads empty and Difference reads as minus MB5B. Converting "
            "cell by cell with a fallback turns an oddly typed cell into a blank instead of an "
            "error.",
        find='''    Typed    = Table.TransformColumnTypes(Slim, {
                   {"GLAccount", type text}, {"GLDescMaster", type text},
                   {"Nature", type text}, {"TBPlant", type text},
                   {"TBSort", Int64.Type}}),
    Dedup    = Table.Distinct(Typed, {"GLAccount"})
in
    Dedup''',
        repl='''    Sortable = Table.TransformColumns(Slim, {
                   {"TBSort", each try Int64.From(Number.Round(Number.From(_))) otherwise null,
                    Int64.Type}}),
    Texted   = Table.TransformColumns(Sortable, {
                   {"GLAccount",    each Text.From(_ ?? ""), type text},
                   {"GLDescMaster", each Text.From(_ ?? ""), type text},
                   {"Nature",       each Text.Trim(Text.From(_ ?? "")), type text},
                   {"TBPlant",      each Text.Trim(Text.From(_ ?? "")), type text}}),
    Dedup    = Table.Distinct(Texted, {"GLAccount"})
in
    Dedup'''),

    dict(
        n="2", build="20", query="dimMaterialAttr",
        title="The same cure on the RM master \u2014 so one loosely typed cell cannot cost every nature",
        why="<code>BOMStdQty</code> cast straight to a number errors the row when the cell holds "
            "text, a dash or a stray space, and an errored row carries no nature, no group "
            "nature and no MW with it. Same edit as #1, on the RM master.",
        find='''    Typed    = Table.TransformColumnTypes(MatKey, {
                   {"Nature", type text}, {"GroupNature", type text},
                   {"BOMStdQty", type number}, {"Item", type text}}),''',
        repl='''    Typed    = Table.TransformColumns(MatKey, {
                   {"Nature",      each Text.Trim(Text.From(_ ?? "")), type text},
                   {"GroupNature", each Text.Trim(Text.From(_ ?? "")), type text},
                   {"BOMStdQty",   each try Number.From(_) otherwise null, type number},
                   {"Item",        each Text.Trim(Text.From(_ ?? "")), type text}}),'''),

    dict(
        n="3", build="20", query="factTB_Staged",
        title="The same cure on the trial balance amount",
        why="An amount typed with a thousands comma, a dash for nil, or a trailing CR / DR errors "
            "the row, and that row's money then counts nowhere at all. Keep whatever punctuation follows "
            "the line in your own file \u2014 a comma if more steps come after it, nothing if "
            "<code>in Typed</code> comes next.",
        find='''    Typed    = Table.TransformColumnTypes(OnPlant, {{"Amount", type number}})''',
        repl='''    Typed    = Table.TransformColumns(OnPlant, {
                   {"Amount", each try Number.From(_)
                              otherwise try Number.From(Text.Select(Text.From(_ ?? ""),
                                             {"0".."9", ".", "-"}))
                              otherwise null, type number}})'''),

    dict(
        n="4", build="20", query="varConstants",
        title="The same cure on the Constants sheet \u2014 it carries the RM megawatt factor",
        why="If the 580 is typed as text, or an Effective From cell is not a date, the row errors "
            "and RM MW comes out blank across the whole report.",
        find='''    Typed    = Table.TransformColumnTypes(Filled, {
                   {"ConstantName", type text}, {"Value", type number}}),''',
        repl='''    Typed    = Table.TransformColumns(Filled, {
                   {"ConstantName", each Text.Trim(Text.From(_ ?? "")), type text},
                   {"Value",        each try Number.From(_) otherwise null, type number}}),'''),

    dict(
        n="5", build="19", query="",
        title="&ldquo;references other queries or steps, so it may not directly access a data "
              "source&rdquo; \u2014 a dozen queries blocked at once",
        why="Power Query's privacy firewall refusing to let a folder source and the "
            "<code>Variables and Calculations</code> workbook meet \u2014 which is the whole "
            "design, since the figures come from the folders and the names come from the "
            "workbook. It is not a fault in any query and cannot be coded around: two sources "
            "have to meet somewhere. Turn the firewall off for your own files, once: "
            "<strong>File &rarr; Options and settings &rarr; Options &rarr; GLOBAL &rarr; "
            "Privacy &rarr; tick &ldquo;Always ignore Privacy Level settings&rdquo; &rarr; "
            "OK</strong>, then the same under <strong>CURRENT FILE &rarr; Privacy</strong>, then "
            "Refresh. The Global one covers every file you open afterwards, so it is the last "
            "time it will bite.",
        find="", repl=""),
]


def edit_cards():
    """The Edits tab's HTML: one card per fix, with a copy button on each code box."""
    out = []
    for e in EDITS:
        find = repl = where = ""
        if e["find"]:
            where = ("<p class='note'>Power Query &rarr; click <strong>%s</strong> in the list on "
                     "the left &rarr; <strong>Home &rarr; Advanced Editor</strong> &rarr; find "
                     "the lines below and paste over them &rarr; <strong>Done</strong>. When all "
                     "the edits are in, <strong>Close &amp; Apply</strong>.</p>"
                     % html.escape(e["query"]))
            find = ("<h4>Find this</h4><button class='copy' data-target='efind%s'>Copy</button>"
                    "<pre id='efind%s'>%s</pre>"
                    % (e["n"], e["n"], html.escape(e["find"])))
            repl = ("<h4>Replace it with exactly this</h4>"
                    "<button class='copy' data-target='erepl%s'>Copy</button>"
                    "<pre id='erepl%s'>%s</pre>"
                    % (e["n"], e["n"], html.escape(e["repl"])))
        out.append(
            '<section class="card" id="e-%s" data-name="%s">\n'
            '  <header><span class="num">%s</span><h3>%s</h3>'
            '<button class="done" data-key="e-%s">Done</button></header>\n'
            '  <p class="note"><strong>Why:</strong> %s</p>\n  %s%s%s\n</section>'
            % (e["n"], html.escape(e["query"] or "setting").lower(), e["n"], e["title"],
               e["n"], e["why"], where, find, repl))
    return "\n".join(out)
