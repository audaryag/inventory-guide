#!/usr/bin/env python3
"""Generates a ready-to-open Power BI project (.pbip) from BUILD_GUIDE.md + spec.py.

Output: /home/ubuntu/pbip/  (Inventory Report.pbip + .SemanticModel + .Report)

The semantic model is TMSL (model.bim): every Power Query query, every relationship,
sort-by-column, hidden columns and all 40 measures. The report is PBIR (JSON per visual)
built from spec.py, so the pages match the guide exactly.
"""
import json, os, pathlib, re, shutil, sys, hashlib, uuid

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import build          # noqa: E402  (parse_queries / parse_measures; also rewrites index.html)
import spec           # noqa: E402

GUIDE = pathlib.Path("/home/ubuntu/BUILD_GUIDE.md")
EMPTY = bool(os.environ.get("PBIP_EMPTY"))
LEGACY = bool(os.environ.get("PBIP_LEGACY"))     # pre-PBIR layout: one report.json, no
                                                 # definition/ folder, no preview feature
OUT = pathlib.Path("/home/ubuntu/pbip-legacy" if LEGACY else
                   "/home/ubuntu/pbip-empty" if EMPTY else "/home/ubuntu/pbip")
NAME = "Inventory Report"

md = GUIDE.read_text()
queries = {q["name"]: q["code"] for q in build.parse_queries(
    md[md.index("# Appendix A"):md.index("# Appendix B")])}
measures = build.parse_measures(md[md.index("# Appendix B"):])

# ---------------------------------------------------------------- semantic model ----------
S, I, D, T, B = "string", "int64", "double", "dateTime", "boolean"

MB5B_COLS = [
    ("SourceFile", S), ("ValuationArea", S), ("Material", S), ("MatKey", S),
    ("MaterialDesc", S), ("FromDate", T), ("ToDate", T), ("OpenQty", D), ("OpenVal", D),
    ("ReceiptQty", D), ("ReceiptVal", D), ("IssueQty", D), ("IssueVal", D),
    ("CloseQty", D), ("CloseVal", D), ("BaseUOM", S), ("SpecialStock", S), ("Currency", S),
    ("Month", T), ("Category", S), ("Nature", S), ("GroupNature", S), ("BOMStdQty", D),
    ("Item", S), ("AttrMissing", B), ("MW Qty", D), ("Rate", D), ("RateParseFailed", B),
    ("Mid", S), ("Base", S), ("INR_WP", D), ("PlantType", S),
]

# tables that load into the model, with their exact column list
TABLES = {
    "factInventory": MB5B_COLS,
    "factTB": [("SourceFile", S), ("Month", T), ("GLAccount", S), ("GLDesc", S),
               ("ProfitCentre", S), ("ProfitCentreDesc", S), ("Amount", D),
               ("PlantCode", S), ("ValuationArea", S), ("Nature", S), ("TBPlant", S),
               ("TBSort", I), ("Category", S), ("Rule", S), ("PlantType", S)],
    "factTB_Unmapped": [("GLAccount", S), ("GLDesc", S), ("Amount", D), ("Rows", I)],
    "dimPlant": [("ValuationArea", S), ("Plant", S), ("PlantSort", I)],
    "dimDate": [("Month", T), ("MonthName", S), ("MonthSort", I), ("MonthIndex", I),
                ("FY", S), ("FYMonthNo", I), ("QuarterNo", I), ("Quarter", S),
                ("QuarterSort", I)],
    "dimNature": [("Nature", S)],
    "dimCapacity": [("Tech", S), ("ValuationArea", S), ("Month", T), ("CapacityMW", D)],
    "dimTBMaster": [("GLAccount", S), ("GLDescMaster", S), ("Nature", S), ("TBPlant", S),
                    ("TBSort", I)],
    "dimCategory": [("Category", S), ("CategorySort", I)],
    "dimPlantType": [("PlantType", S), ("Plant and Type", S), ("Plant", S),
                     ("Category", S), ("RowSort", I)],
    "dimMetric": [("Metric", S), ("MetricSort", I)],
    "dimMeasure": [("Measure", S), ("MeasureSort", I)],
    "qcHeaders": [("Folder", S), ("Name", S), ("SheetNames", S), ("Headers", S)],
    "qcVarHeaders": [("SheetName", S), ("Headers", S), ("DataRows", I)],
    "qcNatureNoCapacity": [("Nature", S)],
    "qcAttrMatch": [("Source", S), ("DistinctMaterials", I),
                    ("MatchedToStockFiles", I), ("FirstEight", S)],
    "qcTBByGL": [("GLAccount", S), ("GLDesc", S), ("Nature", S), ("Category", S),
                 ("ValuationArea", S), ("Rule", S), ("AmountRsCr", D), ("Rows", I)],
    "qcPlantCodes": [("Code", S), ("Rows", I), ("ValueRsCr", D), ("InReport", B)],
    "qcTBUnmatched": [("GLAccount", S), ("ProfitCentre", S), ("PCKey", S), ("GLDesc", S),
                      ("OnSheetAsGL", B), ("Reason", S), ("Rows", I), ("AmountRsCr", D)],
    "qcTBPlants": [("ProfitCentre", S), ("Description", S), ("PlantResolved", S),
                   ("Rows", I), ("InventoryRows", I), ("MatchedRows", I), ("AmountRsCr", D)],
    "qcMonthFiles": [("Category", S), ("Month", T), ("Files", I), ("FileNames", S),
                     ("Rows", I), ("ValueRsCr", D)],
    "qcMasterDupes": [("Sheet", S), ("MatKey", S), ("Natures", I), ("TheyAre", S),
                      ("Rows", I)],
}

# every other query stays a shared expression: helpers, staging, and the diagnostic whose
# shape depends on the sheet (qcMWSheet), which a fixed column list could not describe.
EXPRESSION_ORDER = ["pRoot", "pVarsFile", "fnCleanMB5B", "fnVarSheet", "fnVarSheetSafe", "stgRM", "stgFG",
                    "stgConble", "dimPlantMaster", "varPlantCodes", "dimMaterialAttr", "dimFGAttr", "varConstants",
                    "fnConstantAsOf", "factRM", "factFG", "factConble", "varMWCapacity",
                    "factTB_Staged", "qcMWSheet"]

RELATIONSHIPS = [
    ("dimDate", "Month", "factInventory", "Month"),
    ("dimDate", "Month", "factTB", "Month"),
    ("dimDate", "Month", "dimCapacity", "Month"),
    ("dimPlant", "ValuationArea", "factInventory", "ValuationArea"),
    ("dimPlant", "ValuationArea", "factTB", "ValuationArea"),
    ("dimPlant", "ValuationArea", "dimCapacity", "ValuationArea"),
    ("dimNature", "Nature", "factInventory", "Nature"),
    ("dimNature", "Nature", "dimCapacity", "Tech"),
    ("dimTBMaster", "GLAccount", "factTB", "GLAccount"),
    ("dimCategory", "Category", "factInventory", "Category"),
    ("dimCategory", "Category", "factTB", "Category"),
    ("dimPlantType", "PlantType", "factInventory", "PlantType"),
    ("dimPlantType", "PlantType", "factTB", "PlantType"),
]

SORT_BY = {("dimDate", "MonthName"): "MonthSort", ("dimPlant", "Plant"): "PlantSort",
           ("dimPlantType", "Plant and Type"): "RowSort",
           ("dimCategory", "Category"): "CategorySort", ("dimMetric", "Metric"): "MetricSort",
           ("dimMeasure", "Measure"): "MeasureSort", ("dimDate", "Quarter"): "QuarterSort"}

HIDDEN = {("factInventory", "MatKey"), ("factTB", "PlantCode"),
          ("factInventory", "PlantType"), ("factTB", "PlantType"),
          ("dimPlantType", "PlantType"), ("dimPlantType", "RowSort"), ("dimDate", "MonthSort"),
          ("dimDate", "MonthIndex"), ("dimDate", "FYMonthNo"), ("dimDate", "QuarterNo"),
          ("dimDate", "QuarterSort"), ("dimPlant", "PlantSort"),
          ("dimCategory", "CategorySort"), ("dimMetric", "MetricSort"),
          ("dimMeasure", "MeasureSort")}

# tables kept out of the report field list (helpers/diagnostics still refresh)
HIDDEN_TABLES = {"factTB_Unmapped", "qcHeaders", "qcVarHeaders", "qcNatureNoCapacity",
                 "qcAttrMatch", "qcTBByGL", "qcPlantCodes", "qcTBPlants",
                 "qcMonthFiles", "qcMasterDupes", "qcTBUnmatched"}


def measure_format(name):
    n = name.lower()
    if name in ("As On", "Value ₹ Cr Title"):
        return None                                  # text measures
    if "%" in name:
        return "0.0%"
    if "days" in n:
        return "#,##0.0"
    if "mw" in n.split() or n.endswith(" mw") or n.startswith("mw"):
        return "#,##0.00"
    if "cr" in n or "value" in n:
        return "#,##0.00"
    if "qty" in n or "rows" in n or "months" in n:
        return "#,##0"
    return "#,##0.00"


def model_bim():
    tables = []
    for tname, cols in TABLES.items():
        columns = []
        for cname, dtype in cols:
            col = {"name": cname, "dataType": dtype, "sourceColumn": cname,
                   "summarizeBy": "none",
                   "annotations": [{"name": "SummarizationSetBy", "value": "Automatic"}]}
            if dtype == T:
                col["formatString"] = "yyyy-mm-dd"
            if (tname, cname) in SORT_BY:
                col["sortByColumn"] = SORT_BY[(tname, cname)]
            if (tname, cname) in HIDDEN:
                col["isHidden"] = True
            columns.append(col)
        t = {"name": tname, "columns": columns,
             "partitions": [{"name": tname, "mode": "import",
                             "source": {"type": "m", "expression": queries[tname]}}],
             "annotations": [{"name": "PBI_ResultType", "value": "Table"}]}
        if tname in HIDDEN_TABLES:
            t["isHidden"] = True
        if tname == "factInventory":
            t["measures"] = [m for m in (
                {"name": mm["name"],
                 "expression": mm["code"].split("=", 1)[1].strip(),
                 **({"formatString": measure_format(mm["name"])}
                    if measure_format(mm["name"]) else {}),
                 "displayFolder": "Report measures"} for mm in measures)]
        tables.append(t)

    rels = []
    for i, (ft, fc, tt, tc) in enumerate(RELATIONSHIPS, 1):
        rels.append({"name": f"rel{i:02d}_{ft}_{tt}_{tc}",
                     "fromTable": tt, "fromColumn": tc,     # many side
                     "toTable": ft, "toColumn": fc,         # one side
                     "joinOnDateBehavior": "datePartOnly" if fc == "Month" else None})
    for r in rels:                                          # drop the None we may have set
        if r.get("joinOnDateBehavior") is None:
            r.pop("joinOnDateBehavior")

    # pRoot becomes a real Power Query parameter, so the folder is set from
    # Home > Transform data > Edit parameters instead of by editing code.
    queries["pRoot"] = ('"C:\\Data\\Inventory Report" meta [IsParameterQuery=true, '
                        'Type="Text", IsParameterQueryRequired=true]')

    exprs = [{"name": n, "kind": "m", "expression": queries[n],
              "annotations": [{"name": "PBI_NavigationStepName", "value": "Navigation"},
                              {"name": "PBI_ResultType",
                               "value": "Function" if n.startswith("fn") else (
                                   "Text" if n in ("pRoot", "pVarsFile") else "Table")}]}
             for n in EXPRESSION_ORDER]

    order = EXPRESSION_ORDER + list(TABLES)
    return {
        "name": NAME,
        "compatibilityLevel": 1567,
        "model": {
            "culture": "en-US",
            "dataAccessOptions": {"legacyRedirects": True, "returnErrorValuesAsNull": True},
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "sourceQueryCulture": "en-US",
            "tables": tables,
            "relationships": rels,
            "expressions": exprs,
            "annotations": [
                {"name": "PBI_QueryOrder", "value": json.dumps(order)},
                {"name": "__PBI_TimeIntelligenceEnabled", "value": "0"},
                {"name": "PBIDesktopVersion", "value": "generated"},
            ],
        },
    }


# ------------------------------------------------------------------------- report ----------
SCH = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
VC = f"{SCH}/visualContainer/2.9.0/schema.json"
PG = f"{SCH}/page/2.1.0/schema.json"
PGS = f"{SCH}/pagesMetadata/1.0.0/schema.json"
RPT = f"{SCH}/report/3.3.0/schema.json"
VER = f"{SCH}/versionMetadata/1.0.0/schema.json"

VISUAL_TYPE = {
    "Card": "card", "Slicer": "slicer", "Matrix": "pivotTable", "Table": "tableEx",
    "Stacked column chart": "columnChart", "Clustered column chart": "clusteredColumnChart",
    "Line and clustered column chart": "lineClusteredColumnComboChart",
    "Pie chart": "pieChart", "Donut chart": "donutChart", "Line chart": "lineChart",
    "Decomposition tree": "decompositionTreeVisual",
}

# spec well name -> PBIR role, per visual type family
ROLE = {
    "card": {"Fields": "Values", "Values": "Values"},
    "slicer": {"Field": "Values", "Values": "Values"},
    "pivotTable": {"Rows": "Rows", "Columns": "Columns", "Values": "Values"},
    "tableEx": {"Values": "Values", "Columns": "Values"},
    "columnChart": {"X-axis": "Category", "Y-axis": "Y", "Legend": "Series"},
    "clusteredColumnChart": {"X-axis": "Category", "Y-axis": "Y", "Legend": "Series"},
    "lineClusteredColumnComboChart": {"X-axis": "Category", "Column y-axis": "Y",
                                      "Line y-axis": "Y2", "Column legend": "Series"},
    "lineChart": {"X-axis": "Category", "Y-axis": "Y", "Legend": "Series"},
    "pieChart": {"Legend": "Category", "Values": "Y"},
    "donutChart": {"Legend": "Category", "Values": "Y"},
    "decompositionTreeVisual": {"Analyze": "Analyze", "Explain by": "Explain"},
}

MEASURE_NAMES = {m["name"] for m in measures}
FIELD_RE = re.compile(r"^(\w+)\[(.+)\]$")


def field_expr(token):
    """'dimPlant[Plant]' or 'Value ₹ Cr' -> (QueryExpressionContainer, queryRef, native)."""
    m = FIELD_RE.match(token)
    if m:
        entity, prop = m.group(1), m.group(2)
        if prop in MEASURE_NAMES:      # a measure written table[measure]
            return ({"Measure": {"Expression": {"SourceRef": {"Entity": entity}},
                                 "Property": prop}}, f"{entity}.{prop}", prop)
        return ({"Column": {"Expression": {"SourceRef": {"Entity": entity}},
                            "Property": prop}}, f"{entity}.{prop}", prop)
    if token in MEASURE_NAMES:
        return ({"Measure": {"Expression": {"SourceRef": {"Entity": "factInventory"}},
                             "Property": token}}, f"factInventory.{token}", token)
    raise SystemExit(f"unknown field in spec: {token!r}")


def vname(page, idx):
    h = hashlib.md5(f"{page}-{idx}".encode()).hexdigest()[:16]
    return f"v{h}"


def literal(v):
    return {"expr": {"Literal": {"Value": v}}}


def txt(v):
    return literal("'" + v.replace("'", "''") + "'")


GREEN, DARK, RED = "#4FA45F", "#1E6B3A", "#C0504D"


def title_objects(text):
    return {"title": [{"properties": {"show": literal("true"), "text": txt(text),
                                      "fontColor": {"solid": {"color": txt(DARK)}},
                                      "fontSize": literal("11D"),
                                      "bold": literal("true"),
                                      "fontFamily": txt("Arial")}}],
            "background": [{"properties": {"show": literal("true"),
                                           "color": {"solid": {"color": txt("#FFFFFF")}},
                                           "transparency": literal("0D")}}],
            "border": [{"properties": {"show": literal("true"),
                                       "color": {"solid": {"color": txt("#DCE5DC")}},
                                       "radius": literal("4D")}}]}


def table_objects():
    """tableEx takes none of a chart's objects: no legend, no axes, no data labels."""
    return {
        "columnHeaders": [{"properties": {
            "fontFamily": txt("Arial"), "fontSize": literal("9D"), "bold": literal("true"),
            "fontColor": {"solid": {"color": txt(DARK)}},
            "backColor": {"solid": {"color": txt("#EEF3EF")}}}}],
        "values": [{"properties": {
            "fontFamily": txt("Arial"), "fontSize": literal("9D"),
            "fontColor": {"solid": {"color": txt("#1F2A24")}},
            "backColor": {"solid": {"color": txt("#FFFFFF")}}}}],
        "grid": [{"properties": {"rowPadding": literal("2D"),
                                 "gridVertical": literal("true"),
                                 "gridVerticalColor": {"solid": {"color": txt("#E6EDE6")}},
                                 "gridHorizontalColor": {"solid": {"color": txt("#E6EDE6")}}}}],
    }


def matrix_objects(rows_levels, expand, subtotals=True, column_total=False,
                   col_expand=False):
    o = {
        "rowHeaders": [{"properties": {
            "stepped": literal("false"),
            "showExpandCollapseButtons": literal("true" if expand else "false"),
            "fontFamily": txt("Arial"), "bold": literal("true")}}],
        "columnHeaders": [{"properties": {
            "fontFamily": txt("Arial"), "bold": literal("true"),
            "autoSizeColumnWidth": literal("true"),
            "showExpandCollapseButtons": literal("true" if col_expand else "false"),
            "backColor": {"solid": {"color": txt("#EEF3EF")}},
            "fontColor": {"solid": {"color": txt(DARK)}}}}],
        "values": [{"properties": {"fontFamily": txt("Arial"),
                                   "backColorPrimary": {"solid": {"color": txt("#FFFFFF")}},
                                   "backColorSecondary": {"solid": {"color": txt("#F7FAF7")}},
                                   "bandedRowHeaders": literal("true")}}],
        # The bottom Total row is always on: it adds the plants inside one month, and plants
        # at the same date do add up. The right-hand Total column is always off, because the
        # columns are months and inventory is a level, not a flow - a total across March and
        # July counts the same steel twice. The figure for a window of months is the closing
        # month's level, which the measures themselves return.
        "subTotals": [{"properties": {
            "rowSubtotals": literal("true"),
            "columnSubtotals": literal("true" if column_total else "false"),
            "perRowLevel": literal("true" if subtotals else "false"),
            "perColumnLevel": literal("false")}}],
        "grid": [{"properties": {"gridVertical": literal("true"),
                                 "gridVerticalColor": {"solid": {"color": txt("#E6EDE6")}},
                                 "gridHorizontal": literal("true"),
                                 "gridHorizontalColor": {"solid": {"color": txt("#E6EDE6")}},
                                 "rowPadding": literal("2D"),
                                 "textSize": literal("9D")}}],
        "total": [{"properties": {"fontFamily": txt("Arial"), "bold": literal("true"),
                                  "backColor": {"solid": {"color": txt("#EEF3EF")}}}}],
    }
    return o


def chart_objects(kind, labels=False):
    o = {"legend": [{"properties": {"show": literal("true"), "position": txt("Top"),
                                    "fontFamily": txt("Arial")}}],
         "categoryAxis": [{"properties": {"fontFamily": txt("Arial"),
                                          "labelColor": {"solid": {"color": txt("#3A4A3F")}},
                                          "showAxisTitle": literal("false")}}],
         # the value axis is off on every chart: each one prints its own figures, and the
         # 0 / 500 / 1,000 / 2,000 scale down the side was only repeating them
         "valueAxis": [{"properties": {"show": literal("false"),
                                       "fontFamily": txt("Arial"),
                                       "labelColor": {"solid": {"color": txt("#3A4A3F")}},
                                       "showAxisTitle": literal("false"),
                                       "gridlineColor": {"solid": {"color": txt("#E6EDE6")}}}}],
         # so every bar, column and point carries its number instead
         "labels": [{"properties": {"show": literal("true"),
                                    "fontFamily": txt("Arial"),
                                    "fontSize": literal("8D"),
                                    "color": {"solid": {"color": txt("#1F2A24")}},
                                    "labelDisplayUnits": literal("1D"),
                                    "labelPrecision": literal("1D")}}]}
    if kind in ("clusteredColumnChart", "barChart", "clusteredBarChart",
                "lineClusteredColumnComboChart"):
        # above the bar, never on it. Inside end put a dark figure on a dark green column and
        # the number could not be read at all.
        o["labels"][0]["properties"]["labelPosition"] = txt("OutsideEnd")
        o["labels"][0]["properties"]["fontSize"] = literal("9D")
    if kind == "columnChart":
        # stacked: the consumables segment is too thin to hold a figure, so the segments are
        # left unlabelled and the month's total is printed above the column instead
        o["labels"] = [{"properties": {"show": literal("false")}}]
        o["totals"] = [{"properties": {"show": literal("true"),
                                       "fontFamily": txt("Arial"),
                                       "fontSize": literal("9D"),
                                       "bold": literal("true"),
                                       "labelDisplayUnits": literal("1D"),
                                       "labelPrecision": literal("1D"),
                                       "color": {"solid": {"color": txt(DARK)}}}}]
    if kind in ("pieChart", "donutChart"):
        for k in ("categoryAxis", "valueAxis", "totals"):
            o.pop(k, None)
        # the slice labels name the category and its share, so the legend would say it twice
        # and it was the legend that pushed the labels into each other
        o["legend"] = [{"properties": {"show": literal("false")}}]
        o["labels"] = [{"properties": {"show": literal("true"),
                                       "labelStyle": txt("Category, percent of total"),
                                       "position": txt("outside"),
                                       "overflow": literal("true"),
                                       "fontSize": literal("9D"),
                                       "percentageLabelPrecision": literal("1D"),
                                       "labelPrecision": literal("1D"),
                                       "color": {"solid": {"color": txt("#1F2A24")}},
                                       "fontFamily": txt("Arial")}}]
    o["legend"][0]["properties"].setdefault("fontSize", literal("8D"))
    return o


def shape_visual(page, idx, kind, text, pos):
    """The furniture: the green panel, the white boxes, the logo space and the panel wording.
    All of it is the built-in Shape visual, whose own Text section carries the wording, so
    there is no textbox paragraph structure to get wrong and nothing to bind to the model.
    Property names come from Power BI's published capabilities for visualType 'shape'."""
    x, y, w, h = pos
    filled = kind == "Rectangle"
    green = filled and h > 400                       # the panel itself, not a white box
    logo = kind == "Image"
    colour = spec.PANEL if green else spec.BOX
    # shape.fill, shape.outline and shape.shape are all declared with a 'default' selector in
    # Power BI's own capability catalogue; written without one, Desktop ignored the fill and
    # drew the panel and its boxes in the default light grey - which is why no green appeared.
    dflt = {"id": "default"}
    o = {"shape": [{"properties": {
             "tileShape": txt("rectangle"),
             "roundEdge": literal("0D" if green else "8D")},
             "selector": dflt}],
         "fill": [{"properties": {
             "show": literal("true" if filled else "false"),
             "fillColor": {"solid": {"color": txt(colour)}},
             "transparency": literal("0D")},
             "selector": dflt}],
         "outline": [{"properties": {
             "show": literal("true" if logo else "false"),
             "lineColor": {"solid": {"color": txt(spec.PANEL_SUB)}},
             "transparency": literal("60D"),
             "weight": literal("1D")},
             "selector": dflt}]}
    if text or logo:
        # the two heading lines are the larger type; the section labels above the white
        # boxes are the small bold ones, and the logo box carries only a reminder
        big = text in ("Inventory",) or text in spec.PAGES
        o["text"] = [{"properties": {
            "show": literal("true"),
            "text": txt(text or "Logo"),
            "fontFamily": txt("Arial"),
            "fontSize": literal("15D" if text == "Inventory"
                                else "13D" if big else "10D"),
            "bold": literal("true" if text == "Inventory" or not big else "false"),
            "fontColor": {"solid": {"color": txt(
                spec.PANEL_INK if text == "Inventory" else spec.PANEL_SUB)}},
            "horizontalAlignment": txt("left"),
            "verticalAlignment": txt("middle")}}]
    # the same colour is also painted as the container's own background. It is the generic
    # visual background every visual type supports, so the panel is green even if a future
    # Desktop reads the shape's fill differently again.
    vco = {"background": [{"properties": {
               "show": literal("true" if filled else "false"),
               "color": {"solid": {"color": txt(colour)}},
               "transparency": literal("0D")}}],
           "border": [{"properties": {"show": literal("false")}}],
           "visualHeader": [{"properties": {"show": literal("false")}}]}
    return {"$schema": VC, "name": vname(page, idx),
            "position": {"x": x, "y": y, "z": idx, "width": w, "height": h,
                         "tabOrder": idx * 100},
            "visual": {"visualType": "shape", "objects": o,
                       "visualContainerObjects": vco}}


def card_objects(width=200, height=60):
    # the figure is sized from the box it has to fit in, not chosen once for every card: a
    # 156-wide ticker card holding '1,234.5' plus a category label above it clips the number
    # at 16pt, so the narrow ticker cards get 11pt and the wide cards on Detail and Checks 14pt.
    size = 14 if width > 170 else (13 if height >= 60 else 11)
    if height < 52:
        size = min(size, 10)
    return {"labels": [{"properties": {"fontFamily": txt("Arial"),
                                       "fontSize": literal(f"{size}D"),
                                       "labelDisplayUnits": literal("1D"),
                                       "labelPrecision": literal("1D"),
                                       "color": {"solid": {"color": txt(DARK)}}}}],
            # the card's category label is the measure's name, which the card's own title
            # already says in plain English; printing both is what put a clipped third line
            # of type inside every ticker box
            "categoryLabels": [{"properties": {"show": literal("false")}}],
            "wordWrap": [{"properties": {"show": literal("true")}}]}


def slicer_objects():
    # the slicer's outline is the container's border, set with the title; a slicer has no
    # outline of its own, and writing one into general did nothing at all
    return {# the slicer header repeats the field's own name (MonthName, Category, Nature)
            # under a title that already names it in words, so it is off
            "header": [{"properties": {"show": literal("false")}}],
            "items": [{"properties": {"fontFamily": txt("Arial"),
                                      "textSize": literal("9D")}}],
            # singleSelect off means a plain click adds to the selection, so several
            # months can be ticked without holding CTRL
            "selection": [{"properties": {
                "singleSelect": literal("false"),
                "strictSingleSelect": literal("false"),
                "selectAllCheckboxEnabled": literal("true")}}],
            "data": [{"properties": {"mode": txt("Dropdown")}}]}


def not_blank_filter(fname, entity, prop):
    """Keeps the blank member out of a slicer list. It appears whenever a fact row has a
    code the dimension does not, and there is nothing to pick in it."""
    col = {"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": prop}}
    return {"name": fname, "type": "Advanced",
            "field": {"Column": {"Expression": {"SourceRef": {"Entity": entity}},
                                 "Property": prop}},
            "filter": {"Version": 2,
                       "From": [{"Name": "f", "Entity": entity, "Type": 0}],
                       "Where": [{"Condition": {"Not": {"Expression": {"Comparison": {
                           "ComparisonKind": 0, "Left": col,
                           "Right": {"Literal": {"Value": "null"}}}}}}}]},
            "howCreated": "User"}


def categorical_filter(fname, entity, prop, values, exclude=False):
    src = {"SourceRef": {"Source": "f"}}
    expr = {"Column": {"Expression": src, "Property": prop}}
    inexpr = {"In": {"Expressions": [expr],
                     "Values": [[{"Literal": {"Value": "'" + v + "'"}}] for v in values]}}
    cond = {"Not": {"Expression": inexpr}} if exclude else inexpr
    return {"name": fname, "type": "Categorical",
            "field": {"Column": {"Expression": {"SourceRef": {"Entity": entity}},
                                 "Property": prop}},
            "filter": {"Version": 2,
                       "From": [{"Name": "f", "Entity": entity, "Type": 0}],
                       "Where": [{"Condition": cond}]},
            "howCreated": "User"}


def measure_equals_filter(fname, entity, prop, value):
    return {"name": fname, "type": "Advanced",
            "field": {"Measure": {"Expression": {"SourceRef": {"Entity": entity}},
                                  "Property": prop}},
            "filter": {"Version": 2,
                       "From": [{"Name": "f", "Entity": entity, "Type": 0}],
                       "Where": [{"Condition": {"Comparison": {
                           "ComparisonKind": 0,
                           "Left": {"Measure": {"Expression": {"SourceRef": {"Source": "f"}},
                                                "Property": prop}},
                           "Right": {"Literal": {"Value": f"{value}L"}}}}}]},
            "howCreated": "User"}


def parse_spec_filter(text, seq):
    """'dimCategory[Category]  →  is FG' / 'Last 4 Months  →  is 1' / '... untick MW'."""
    left, _, right = [p.strip() for p in text.partition("→")]
    right = right.strip()
    m = FIELD_RE.match(left)
    if m and right.lower().startswith("untick"):
        return categorical_filter(f"flt{seq}", m.group(1), m.group(2),
                                  [right.split(None, 1)[1].strip()], exclude=True)
    if m:
        return categorical_filter(f"flt{seq}", m.group(1), m.group(2),
                                  [right.split(None, 1)[1].strip()])
    return measure_equals_filter(f"flt{seq}", "factInventory", left,
                                 int(right.split()[-1]))


def build_visual(page, idx, kind, title, wells, pos, extra_filters):
    vt = VISUAL_TYPE[kind]
    roles = ROLE[vt]
    qstate, rows_levels, sort_field = {}, 0, None
    for well, fields in wells:
        if well == "Filters":
            continue
        role = roles[well]
        projections = []
        for f in fields:
            fe, qref, native = field_expr(spec.base(f))
            proj = {"field": fe, "queryRef": qref, "nativeQueryRef": native}
            # a per-visual rename: the header reads TB, not TB Inventory Rs Cr
            if spec.label(f):
                proj["displayName"] = spec.label(f)
            projections.append(proj)
            if vt in ("columnChart", "clusteredColumnChart",
                      "lineClusteredColumnComboChart") and role == "Y" and not sort_field:
                sort_field = fe
        st = qstate.setdefault(role, {"projections": []})
        st["projections"].extend(projections)
        # 'Show items with no data' is deliberately OFF on a chart's axis. dimNature is a
        # bridge table carrying every nature in the model, RM and FG alike, so with it on the
        # FG-by-technology chart drew an axis of RM natures - Al Lam, Angle, Backsheet - each
        # with no bar and no line, which is the chart that kept coming up empty. Off, a
        # category with nothing to show removes itself. The matrices that must list a plant
        # even when its figure is blank turn it back on by name, below.
        if role in ("Category", "Series", "Rows", "Columns", "Explain"):
            st["showAll"] = st.get("showAll", False)
        if role == "Rows":
            rows_levels = len(projections)
    if "showAll" in qstate.get("Rows", {}):
        qstate["Rows"].pop("showAll")
    for r in ("Explain",):
        qstate.get(r, {}).pop("showAll", None)

    # 'Show items with no data' on the rows of the matrices that must list every plant: a
    # blank Days cell (1905 has no module capacity on the MW sheet) otherwise takes the whole
    # row away, and a missing plant reads as a data fault when it is a capacity gap.
    if vt == "pivotTable" and title in spec.SHOW_ALL_ROWS and "Rows" in qstate:
        qstate["Rows"]["showAll"] = True

    query = {"queryState": qstate}
    if vt == "pivotTable":
        cols = [spec.base(f) for w, fs in wells if w == "Columns" for f in fs]
        col_levels = len(qstate.get("Columns", {}).get("projections", []))
        objects = matrix_objects(rows_levels, expand=rows_levels > 1,
                                 subtotals=rows_levels > 1,
                                 column_total=False,
                                 col_expand=col_levels > 1)
    elif vt == "card":
        objects = card_objects(pos[2], pos[3])
    elif vt == "slicer":
        # every slicer multi-selects on a plain click: singleSelect off is what Power BI
        # calls 'Multi-select with CTRL', and leaving it on is why several months could
        # not be ticked
        objects = slicer_objects()
    elif vt == "tableEx":
        objects = table_objects()
    elif vt == "decompositionTreeVisual":
        objects = {}
    else:
        objects = chart_objects(vt, labels=vt in ("pieChart", "donutChart"))

    visual = {"visualType": vt, "query": query,
              "visualContainerObjects": title_objects(title)}
    if objects:
        visual["objects"] = objects
    if vt == "pivotTable":
        # One expansion state per role that has more than one level, and 'root': isToggled only
        # on Rows. Builds 12 and 17 wrote a Columns state carrying that root toggle and Desktop
        # answered with an empty card; the level list on its own is what opens the second column
        # level, and the expand/collapse buttons on the column headers are the way back if a
        # version of Desktop ignores it.
        states = []
        for role in ("Rows", "Columns"):
            projs = qstate.get(role, {}).get("projections", [])
            if len(projs) < 2:
                continue
            st = {"roles": [role],
                  "levels": [{"queryRefs": [p["queryRef"]], "isCollapsed": False}
                             for p in projs]}
            if role == "Rows":
                st["root"] = {"isToggled": True}
            states.append(st)
        if states:
            visual["expansionStates"] = states

    x, y, w, h = pos
    out = {"$schema": VC, "name": vname(page, idx),
           "position": {"x": x, "y": y, "z": idx, "width": w, "height": h,
                        "tabOrder": idx * 100},
           "visual": visual}
    filters = list(extra_filters)
    if vt == "slicer":
        for p in qstate.get("Values", {}).get("projections", []):
            col = p["field"].get("Column")
            if col:
                filters.append(not_blank_filter(
                    f"nb{vname(page, idx)}", col["Expression"]["SourceRef"]["Entity"],
                    col["Property"]))
    if filters:
        out["filterConfig"] = {"filters": filters}
    return out


def page_json(name, idx, drill=False):
    p = {"$schema": PG, "name": pname(name), "displayName": name,
         "displayOption": "FitToPage", "width": spec.CANVAS[0], "height": spec.CANVAS[1],
         "objects": {
             "background": [{"properties": {
                 "color": {"solid": {"color": txt("#F4F7F4")}},
                 "transparency": literal("0D")}}],
             "outspace": [{"properties": {
                 "color": {"solid": {"color": txt("#FFFFFF")}}}}]}}
    if drill:
        p["pageBinding"] = {"name": f"{pname(name)}_drill", "type": "Drillthrough"}
        p["filterConfig"] = {"filters": [
            dict(categorical_filter(f"drill{i}", *FIELD_RE.match(f).groups(), []),
                 howCreated="Drillthrough") for i, f in enumerate(spec.DRILL_FIELDS)]}
        for f in p["filterConfig"]["filters"]:
            f.pop("filter")                     # no values yet: the drill supplies them
    return p


def pname(page):
    return "pg" + hashlib.md5(page.encode()).hexdigest()[:16]


def write_report(root):
    d = root / "definition"
    (d / "pages").mkdir(parents=True, exist_ok=True)
    (d / "version.json").write_text(json.dumps({"$schema": VER, "version": "2.0.0"}, indent=2))
    theme = json.loads((HERE / "inventory-theme.json").read_text())
    res = root / "StaticResources" / "RegisteredResources"
    res.mkdir(parents=True, exist_ok=True)
    # the registered resource, the resourcePackages entry and customTheme.name must all be
    # the same string, extension included, or the service silently drops the theme
    tfile = theme["name"] + ".json"
    theme["name"] = tfile          # the theme's own name must equal the file it is loaded from
    (res / tfile).write_text(json.dumps(theme, indent=2, ensure_ascii=False))
    (d / "report.json").write_text(json.dumps({
        "$schema": RPT,
        "themeCollection": {"customTheme": {
            "name": tfile,
            "reportVersionAtImport": {"visual": "2.6.0", "report": "3.1.0", "page": "2.3.0"},
            "type": "RegisteredResources"}},
        "resourcePackages": [{"name": "RegisteredResources", "type": "RegisteredResources",
                              "items": [{"name": tfile, "path": tfile,
                                         "type": "CustomTheme"}]}],
        "settings": {"useStylableVisualContainerHeader": True,
                     "defaultFilterActionIsDataFilter": True,
                     "allowChangeFilterTypes": True},
        "objects": {"outspacePane": [{"properties": {"expanded": literal("false")}}]},
    }, indent=2, ensure_ascii=False))
    (d / "pages" / "pages.json").write_text(json.dumps({
        "$schema": PGS, "pageOrder": [pname(p) for p in spec.PAGES],
        "activePageName": pname(spec.PAGES[0])}, indent=2))

    for page in spec.PAGES:
        pdir = d / "pages" / pname(page)
        (pdir / "visuals").mkdir(parents=True, exist_ok=True)
        (pdir / "page.json").write_text(json.dumps(
            page_json(page, spec.PAGES.index(page), drill=page == spec.DRILL_PAGE),
            indent=2, ensure_ascii=False))

        idx = 0
        if EMPTY:                      # model-only variant: pages exist, visuals do not
            continue

        # the furniture first, so its z-order sits under every figure that lands on it
        for pg, kind, text, x, y, w, h, _note in spec.DECOR:
            if pg != page:
                continue
            idx += 1
            write_visual(pdir, shape_visual(page, idx, kind, text, (x, y, w, h)))

        if page in spec.BAND_PAGES:
            for mname, x, y, w, h, cap in spec.CARDS:
                idx += 1
                v = build_visual(page, idx, "Card", cap, [("Fields", [mname])],
                                 (x, y, w, h), [])
                write_visual(pdir, v)
            for field, x, y, w, h, cap in spec.SLICERS:
                idx += 1
                v = build_visual(page, idx, "Slicer", cap, [("Field", [field])],
                                 (x, y, w, h), [])
                write_visual(pdir, v)

        for vi, (pg, kind, title, wells, pos, why, extra) in enumerate(spec.VISUALS):
            if pg != page:
                continue
            idx += 1
            filters = [parse_spec_filter(t, f"{pname(page)}_{idx}_{i}")
                       for well, fields in wells if well == "Filters"
                       for i, t in enumerate(fields)]
            v = build_visual(page, idx, kind, title, wells, pos, filters)
            write_visual(pdir, v)


def write_report_legacy(root):
    """The pre-PBIR layout every .pbip-capable Desktop understands: a single report.json
    holding the sections, and no definition/ folder. Pages are made and named; the visuals
    are left to the guide, because the legacy visualContainer format cannot be generated
    reliably without Desktop to verify it."""
    theme = json.loads((HERE / "inventory-theme.json").read_text())
    res = root / "StaticResources" / "RegisteredResources"
    res.mkdir(parents=True, exist_ok=True)
    (res / "inventory-theme.json").write_text(json.dumps(theme, indent=2, ensure_ascii=False))
    sections = []
    for i, page in enumerate(spec.PAGES):
        sections.append({
            "id": i, "name": f"ReportSection{i:02d}", "displayName": page,
            "filters": "[]", "ordinal": i, "visualContainers": [],
            "config": json.dumps({"objects": {"background": [{"properties": {
                "color": {"solid": {"color": {"expr": {"Literal": {
                    "Value": "'#F4F7F4'"}}}}},
                "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}]}}),
            "displayOption": 1, "width": spec.CANVAS[0], "height": spec.CANVAS[1]})
    (root / "report.json").write_text(json.dumps({
        "id": 0, "layoutOptimization": 0, "publicCustomVisuals": [],
        "resourcePackages": [{"resourcePackage": {
            "disabled": False, "items": [{"name": "inventory-theme.json",
                                          "path": "inventory-theme.json",
                                          "type": 202}],
            "name": "RegisteredResources", "type": 2}}],
        "sections": sections,
        "config": json.dumps({
            "version": "5.55", "themeCollection": {"customTheme": {
                "name": theme["name"], "reportVersionAtImport": "5.55", "type": 2}},
            "activeSectionIndex": 0,
            "settings": {"useStylableVisualContainerHeader": True,
                         "defaultFilterActionIsDataFilter": True}}),
    }, indent=2, ensure_ascii=False))


def write_visual(pdir, v):
    vd = pdir / "visuals" / v["name"]
    vd.mkdir(parents=True, exist_ok=True)
    (vd / "visual.json").write_text(json.dumps(v, indent=2, ensure_ascii=False))


def platform(folder, kind):
    """Fabric item metadata; Desktop and Fabric both expect one per item."""
    (folder / ".platform").write_text(json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/"
                   "platformProperties/2.0.0/schema.json",
        "metadata": {"type": kind, "displayName": NAME},
        "config": {"version": "2.0",
                   "logicalId": str(uuid.uuid5(uuid.NAMESPACE_URL,
                                               f"inventory-{kind}"))}}, indent=2))


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    sm = OUT / f"{NAME}.SemanticModel"
    rp = OUT / f"{NAME}.Report"
    sm.mkdir(parents=True)
    rp.mkdir(parents=True)

    (OUT / f"{NAME}.pbip").write_text(json.dumps({
        **({} if LEGACY else {"$schema": "https://developer.microsoft.com/json-schemas/"
                              "fabric/pbip/pbipProperties/1.0.0/schema.json"}),
        "version": "1.0",
        "artifacts": [{"report": {"path": f"{NAME}.Report"}}],
        "settings": {"enableAutoRecovery": True}}, indent=2))

    (sm / "definition.pbism").write_text(json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/"
                   "definitionProperties/1.0.0/schema.json",
        "version": "1.0", "settings": {}}, indent=2))
    (sm / "model.bim").write_text(json.dumps(model_bim(), indent=2, ensure_ascii=False))
    platform(sm, "SemanticModel")

    if LEGACY:
        (rp / "definition.pbir").write_text(json.dumps({
            "version": "1.0",
            "datasetReference": {"byPath": {"path": f"../{NAME}.SemanticModel"}}}, indent=2))
        # older Desktop builds look for definition.pbidataset, newer for definition.pbism;
        # shipping both costs nothing and each build reads the one it knows
        shutil.copy(sm / "definition.pbism", sm / "definition.pbidataset")
        write_report_legacy(rp)
    else:
        (rp / "definition.pbir").write_text(json.dumps({
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/"
                       "definitionProperties/2.0.0/schema.json",
            "version": "4.0",
            "datasetReference": {"byPath": {"path": f"../{NAME}.SemanticModel"}}}, indent=2))
        platform(rp, "Report")
        write_report(rp)

    missing = set(queries) - set(TABLES) - set(EXPRESSION_ORDER)
    if missing:
        raise SystemExit(f"queries in the guide but not in the model: {sorted(missing)}")
    n_vis = len(list((rp / "definition" / "pages").rglob("visual.json"))) if not LEGACY else 0
    print(f"wrote {OUT}: {len(TABLES)} tables, {len(EXPRESSION_ORDER)} helper queries, "
          f"{len(measures)} measures, {len(RELATIONSHIPS)} relationships, "
          f"{len(spec.PAGES)} pages, {n_vis} visuals")


if __name__ == "__main__":
    main()
