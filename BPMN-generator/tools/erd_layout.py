#!/usr/bin/env python3
"""
erd_layout.py — generate a draw.io/mxGraph XML file with multiple diagram TABS,
importable into Lucidchart via File > Import Diagram > Draw.io. Tab 1 is the
entity-relationship diagram of the Curated entities in process-model-ref.md. Tab 2 is the
dimensional (star-schema) model for the Contextualized facts/dimensions/KPIs defined in
beam-overlay.yaml Section 7.

WHY THIS SHAPE, NOT DRAW.IO'S NATIVE "TABLE" WIDGET OR CROW'S-FOOT ARROW STYLES
--------------------------------------------------------------------------------
draw.io has a purpose-built nested table/row/cell shape for ER diagrams and a library of
crow's-foot-notation arrow ends (ERone, ERmany, etc.). Neither is used here: the exact
geometry rules for the nested table shape and the exact arrow-style keyword strings could
not be confirmed from documentation without a live draw.io session to export and inspect,
and Lucid's own community forum documents that Lucid's import of draw.io files does not
reliably preserve edge labels. Rather than gamble on unverified specifics the way the first
BPMN pass gambled on "Lucidchart auto-layouts" (it doesn't), this generator uses the
smallest, highest-confidence subset of mxGraph XML: plain rectangular vertices with an
HTML-formatted multi-line label (bold header + field list) and plain edges with fully
explicit waypoints (no auto-routing) and a text label.

LAYOUT — TWO ROWS + DEDICATED ROUTING LANES, NO AUTO-ROUTING, PER TAB
-----------------------------------------------------------------------
Each tab is its own DiagramSpec (entities, a two-row assignment, relationships, a legend)
run through the shared Layout engine. Every relationship is one of three kinds, each with
its own deterministic, collision-free route:

  same-row, adjacent    — straight horizontal segment, left-right exit/entry points.
                           Safe because nothing sits between two literally-adjacent boxes.
  same-row, non-adjacent — "dip" route: exits/enters the row's OUTER edge (bottom for the
                           top row, top for the bottom row) into a dedicated horizontal lane
                           that sits entirely below/above every box in that row.
  cross-row              — exits the top row's bottom, enters the bottom row's top, via a
                           third dedicated horizontal lane in the gap between the two rows.

Tab 2 (the star schema) reuses this exact engine: dimensions in row A, facts + KPI-summary
boxes in row B — every dimension-to-fact edge is a cross-row edge through the highway lane,
which is precisely what a star schema's fan-out from a central fact table needs, so no new
layout algorithm was written for it.

erd_verify.py independently re-derives every edge's absolute path from the emitted XML and
checks every segment against every non-endpoint box, in EVERY <diagram> in the file, for a
real geometric intersection — not a visual/eyeball check.

USAGE
-----
    python erd_layout.py <output.drawio>
"""

import sys

# --- box sizing -----------------------------------------------------------------
BOX_W = 280
HEADER_H = 34
FIELD_H = 22
BOX_PAD_BOTTOM = 10

# --- row/lane geometry (px) ------------------------------------------------------
COL_GAP = 60
CANVAS_X0 = 40
ROW_A_Y = 40
LANE_GAP = 40
LANE_STAGGER = 12
SIDE_STAGGER_MIN, SIDE_STAGGER_MAX = 0.22, 0.78
LEGEND_GAP = 90


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def entity_size(fields):
    return BOX_W, HEADER_H + len(fields) * FIELD_H + BOX_PAD_BOTTOM


class DiagramSpec:
    """Everything needed to lay out and render one tab: its entities (name -> (type,
    fields)), the two-row assignment, the relationships, the type-color palette, and the
    legend entries. Kept as one object (rather than module globals) specifically so a
    second tab can exist without shadowing or resetting the first."""

    def __init__(self, name, diagram_id, entity_defs, row_a, row_b, relationships,
                 type_colors, legend_entries, external_color=("#F5F5F5", "#666666")):
        self.name = name
        self.diagram_id = diagram_id
        self.entity_defs = entity_defs
        self.row_a = row_a
        self.row_b = row_b
        self.relationships = relationships
        self.type_colors = type_colors
        self.legend_entries = legend_entries
        self.external_color = external_color


class Layout:
    """Computes every box position and every edge's explicit waypoint path for one
    DiagramSpec."""

    def __init__(self, spec):
        self.spec = spec
        self.box = {}

        # Lane clearance must be sized from how many edges will actually share each lane
        # — a fixed gap sized for tab 1's 7 cross-row edges silently let tab 2's 12 spill
        # past it into row B's own boxes (caught by erd_verify.py's E10, not by eye). This
        # static pass classifies every edge by row membership + row order alone (no pixel
        # geometry needed yet), so lane heights can be computed correctly before anything
        # is actually placed.
        lane_counts = {"A": 0, "B": 0, "hwy": 0}
        for rel in spec.relationships:
            kind = self._static_kind(rel[0], rel[1])
            if kind == "dip":
                row = "A" if rel[0] in spec.row_a else "B"
                lane_counts[row] += 1
            elif kind == "cross":
                lane_counts["hwy"] += 1

        def lane_height(n):
            return LANE_STAGGER * max(0, n - 1) + LANE_GAP

        self._place_row("A", spec.row_a, ROW_A_Y)
        row_a_bottom = max(b["y"] + b["h"] for b in self.box.values())
        self.row_a_lane_y = row_a_bottom + LANE_GAP
        self.highway_y = self.row_a_lane_y + lane_height(lane_counts["A"])
        self.row_b_lane_y = self.highway_y + lane_height(lane_counts["hwy"])
        row_b_y = self.row_b_lane_y + lane_height(lane_counts["B"])
        self._place_row("B", spec.row_b, row_b_y)

        row_b_bottom = max(self.box[n]["y"] + self.box[n]["h"] for n in spec.row_b)
        self.legend_y = row_b_bottom + LEGEND_GAP

        self._side_usage = {}
        self._side_total = self._count_side_usage()
        self._lane_usage = {"A": 0, "B": 0, "hwy": 0}

    def _place_row(self, row_label, order, y):
        x = CANVAS_X0
        for name in order:
            etype, fields = self.spec.entity_defs[name]
            w, h = entity_size(fields)
            self.box[name] = {"x": x, "y": y, "w": w, "h": h, "type": etype,
                               "fields": fields, "row": row_label}
            x += w + COL_GAP

    def _static_kind(self, src, tgt):
        """Same classification as _edge_kind, but using only which row a name was
        assigned to and its index in that row's order — no pixel geometry required, so
        this can run before any box is placed (see the lane-sizing pass in __init__)."""
        ra = "A" if src in self.spec.row_a else "B"
        rb = "A" if tgt in self.spec.row_a else "B"
        if ra != rb:
            return "cross"
        order = self.spec.row_a if ra == "A" else self.spec.row_b
        ia, ib = order.index(src), order.index(tgt)
        return "adjacent" if abs(ia - ib) == 1 else "dip"

    def _edge_kind(self, src, tgt):
        ra, rb = self.box[src]["row"], self.box[tgt]["row"]
        if ra != rb:
            return "cross"
        order = self.spec.row_a if ra == "A" else self.spec.row_b
        ia, ib = order.index(src), order.index(tgt)
        return "adjacent" if abs(ia - ib) == 1 else "dip"

    def _count_side_usage(self):
        counts = {}
        for rel in self.spec.relationships:
            src, tgt = rel[0], rel[1]
            kind = self._edge_kind(src, tgt)
            if kind == "adjacent":
                sside = "right" if self.box[tgt]["x"] > self.box[src]["x"] else "left"
                tside = "left" if sside == "right" else "right"
            elif kind == "dip":
                sside = "bottom" if self.box[src]["row"] == "A" else "top"
                tside = sside
            else:
                sside = "bottom" if self.box[src]["row"] == "A" else "top"
                tside = "top" if self.box[tgt]["row"] == "B" else "bottom"
            counts[(src, sside)] = counts.get((src, sside), 0) + 1
            counts[(tgt, tside)] = counts.get((tgt, tside), 0) + 1
        return counts

    def _fraction(self, name, side):
        total = self._side_total.get((name, side), 1)
        i = self._side_usage.get((name, side), 0)
        self._side_usage[(name, side)] = i + 1
        if total <= 1:
            return 0.5
        return SIDE_STAGGER_MIN + (SIDE_STAGGER_MAX - SIDE_STAGGER_MIN) * i / (total - 1)

    def _point(self, name, side, frac):
        b = self.box[name]
        if side == "left":
            return (b["x"], b["y"] + frac * b["h"])
        if side == "right":
            return (b["x"] + b["w"], b["y"] + frac * b["h"])
        if side == "top":
            return (b["x"] + frac * b["w"], b["y"])
        return (b["x"] + frac * b["w"], b["y"] + b["h"])

    @staticmethod
    def _xy_fraction(side, frac):
        return {"left": (0.0, frac), "right": (1.0, frac),
                "top": (frac, 0.0), "bottom": (frac, 1.0)}[side]

    def route(self, src, tgt):
        kind = self._edge_kind(src, tgt)
        if kind == "adjacent":
            sside = "right" if self.box[tgt]["x"] > self.box[src]["x"] else "left"
            tside = "left" if sside == "right" else "right"
            sfrac = self._fraction(src, sside)
            tfrac = self._fraction(tgt, tside)
            path = [self._point(src, sside, sfrac), self._point(tgt, tside, tfrac)]
        elif kind == "dip":
            row = self.box[src]["row"]
            sside = tside = "bottom" if row == "A" else "top"
            lane_base = self.row_a_lane_y if row == "A" else self.row_b_lane_y
            lane_key = "A" if row == "A" else "B"
            lane_y = lane_base + LANE_STAGGER * self._lane_usage[lane_key]
            self._lane_usage[lane_key] += 1
            sfrac = self._fraction(src, sside)
            tfrac = self._fraction(tgt, tside)
            p0 = self._point(src, sside, sfrac)
            p3 = self._point(tgt, tside, tfrac)
            path = [p0, (p0[0], lane_y), (p3[0], lane_y), p3]
        else:
            sside = "bottom" if self.box[src]["row"] == "A" else "top"
            tside = "top" if self.box[tgt]["row"] == "B" else "bottom"
            lane_y = self.highway_y + LANE_STAGGER * self._lane_usage["hwy"]
            self._lane_usage["hwy"] += 1
            sfrac = self._fraction(src, sside)
            tfrac = self._fraction(tgt, tside)
            p0 = self._point(src, sside, sfrac)
            p3 = self._point(tgt, tside, tfrac)
            path = [p0, (p0[0], lane_y), (p3[0], lane_y), p3]

        return {"exit_xy": self._xy_fraction(sside, sfrac),
                "entry_xy": self._xy_fraction(tside, tfrac),
                "path": path, "waypoints": path[1:-1]}


def render_entity(cell_id, name, info, type_colors, external_color):
    etype = info["type"]
    fill, stroke = external_color if etype.startswith("External") else type_colors.get(etype, ("#FFFFFF", "#000000"))
    dashed = "1" if etype.startswith("External") else "0"
    field_lines = "".join(
        "<div style='padding:1px 6px;font-family:Consolas,monospace;font-size:11px;text-align:left;'>%s</div>" % f
        for f in info["fields"]
    )
    raw_label = (
        "<div style='font-weight:bold;font-size:13px;border-bottom:1px solid %s;"
        "padding:4px 6px;text-align:center;'>%s<br/>"
        "<span style='font-weight:normal;font-size:10px;font-style:italic;'>%s</span></div>"
        "%s" % (stroke, name, etype, field_lines)
    )
    style = (
        "rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;"
        "fillColor=%s;strokeColor=%s;dashed=%s;spacing=0;fontSize=11;" % (fill, stroke, dashed)
    )
    return (
        '      <mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">\n'
        '        <mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry"/>\n'
        "      </mxCell>\n"
    ) % (cell_id, esc(raw_label), style, info["x"], info["y"], info["w"], info["h"])


def render_edge(cell_id, src_id, tgt_id, route_info, label, dashed=False):
    ex, ey = route_info["exit_xy"]
    en, ee = route_info["entry_xy"]
    style = (
        "edgeStyle=none;rounded=0;html=1;fontSize=10;endArrow=block;endFill=0;startArrow=none;"
        "dashed=%s;"
        "exitX=%g;exitY=%g;exitDx=0;exitDy=0;entryX=%g;entryY=%g;entryDx=0;entryDy=0;"
        % ("1" if dashed else "0", ex, ey, en, ee)
    )
    (sx, sy), (tx, ty) = route_info["path"][0], route_info["path"][-1]
    wp_xml = "".join('<mxPoint x="%g" y="%g"/>' % (x, y) for x, y in route_info["waypoints"])
    return (
        '      <mxCell id="%s" value="%s" style="%s" edge="1" parent="1" source="%s" target="%s">\n'
        '        <mxGeometry relative="1" as="geometry">\n'
        '          <mxPoint x="%g" y="%g" as="sourcePoint"/>\n'
        '          <mxPoint x="%g" y="%g" as="targetPoint"/>\n'
        "          %s\n"
        "        </mxGeometry>\n"
        "      </mxCell>\n"
    ) % (cell_id, esc(label), style, src_id, tgt_id, sx, sy, tx, ty,
         ('<Array as="points">%s</Array>' % wp_xml) if wp_xml else "")


def render_legend(start_id, y, legend_entries, type_colors, external_color):
    out = []
    title_style = "text;html=1;fontSize=14;fontStyle=1;align=left;verticalAlign=middle;"
    out.append(
        '      <mxCell id="%s" value="Legend" style="%s" vertex="1" parent="1">\n'
        '        <mxGeometry x="%d" y="%d" width="200" height="26" as="geometry"/>\n'
        "      </mxCell>\n" % (start_id, title_style, CANVAS_X0, y)
    )
    row_y = y + 34
    for i, (label, desc) in enumerate(legend_entries):
        etype_key = label.split(" (")[0]
        fill, stroke = external_color if "External" in label else type_colors.get(etype_key, ("#FFFFFF", "#000000"))
        dashed = "1" if "External" in label else "0"
        swatch_id = "%s_sw%d" % (start_id, i)
        text_id = "%s_tx%d" % (start_id, i)
        swatch_style = "rounded=0;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;dashed=%s;" % (fill, stroke, dashed)
        text_style = "text;html=1;fontSize=11;align=left;verticalAlign=middle;whiteSpace=wrap;"
        ry = row_y + i * 30
        out.append(
            '      <mxCell id="%s" value="" style="%s" vertex="1" parent="1">\n'
            '        <mxGeometry x="%d" y="%d" width="28" height="20" as="geometry"/>\n'
            "      </mxCell>\n" % (swatch_id, swatch_style, CANVAS_X0, ry)
        )
        out.append(
            '      <mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">\n'
            '        <mxGeometry x="%d" y="%d" width="900" height="20" as="geometry"/>\n'
            "      </mxCell>\n" % (text_id, esc("<b>%s</b> — %s" % (label, desc)), text_style,
                                    CANVAS_X0 + 38, ry)
        )
    return "".join(out)


def render_diagram(spec, id_prefix):
    layout = Layout(spec)
    node_id = {name: "%sn%d" % (id_prefix, i) for i, name in enumerate(spec.entity_defs.keys())}

    out = []
    out.append('  <diagram name="%s" id="%s">\n' % (esc(spec.name), spec.diagram_id))
    out.append('    <mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" '
                'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
                'pageWidth="3600" pageHeight="1800" math="0" shadow="0">\n')
    out.append("      <root>\n")
    out.append('        <mxCell id="0"/>\n')
    out.append('        <mxCell id="1" parent="0"/>\n')

    for name in spec.entity_defs:
        out.append(render_entity(node_id[name], name, layout.box[name],
                                  spec.type_colors, spec.external_color))

    for i, rel in enumerate(spec.relationships):
        src, tgt, label = rel[0], rel[1], rel[2]
        dashed = rel[3] if len(rel) > 3 else False
        route_info = layout.route(src, tgt)
        out.append(render_edge("%se%d" % (id_prefix, i), node_id[src], node_id[tgt],
                                route_info, label, dashed))

    out.append(render_legend("%slegend" % id_prefix, layout.legend_y,
                              spec.legend_entries, spec.type_colors, spec.external_color))

    out.append("      </root>\n")
    out.append("    </mxGraphModel>\n")
    out.append("  </diagram>\n")
    return "".join(out)


# ============================================================================
# TAB 1 — Curated entity-relationship diagram (process-model-ref.md)
# ============================================================================

TAB1_ENTITY_DEFS = {
    "mobile_equipment_source_minestar": ("Source", [
        "PK  minestar_unit_id",
        "    minestar_status (system's own flag)",
        "    make, model, nominal_payload_t ...",
        "    [duplicates possible — see notes]",
    ]),
    "mobile_equipment_source_wenco": ("Source", [
        "PK  wenco_unit_id",
        "    wenco_status (system's own flag)",
        "    make, model, nominal_payload_t ...",
        "    [duplicates possible — see notes]",
    ]),
    "mobile_equipment_source_xref": ("Map", [
        "PK  xref_id",
        "FK  equipment_master_id -> mobile_equipment",
        "FK  source_system_equipment_id",
        "    source_system_name (Minestar | Wenco)",
        "    valid_from_utc, valid_to_utc",
        "    is_authoritative, decided_by",
    ]),
    "mobile_equipment": ("Master", [
        "PK  equipment_master_id (governed, not yet real)",
        "    fleet_number, make, model",
        "FK  equipment_class",
        "    nominal_payload_t, equipment_status",
    ]),
    "equipment_class": ("Reference", [
        "PK  class_id",
        "    functional_type, nominal_capacity",
        "    capacity_unit, typical_make_model",
    ]),
    "operator_shift_assignment": ("Transactional", [
        "PK  assignment_id",
        "FK  operator_id -> operator",
        "FK  equipment_id -> mobile_equipment",
        "FK  shift_id -> shift",
        "    assignment_start_utc, assignment_end_utc",
    ]),
    "operator": ("Master", [
        "PK  operator_id",
        "    operator_name, authorization_classes",
        "    employment_type, active_flag",
    ]),
    "shift": ("Reference", [
        "PK  shift_id",
        "    shift_date, shift_type, site_id",
        "    shift_start_utc, shift_end_utc",
    ]),
    "dig_polygon": ("External (Pillar 1)", [
        "PK  polygon_id",
        "    (owned by Mine Planning & Scheduling)",
        "    referenced by haul_cycle.origin_polygon_id",
    ]),
    "haul_cycle": ("Transactional", [
        "PK  cycle_id",
        "FK  truck_id, shovel_id -> mobile_equipment",
        "FK  shift_id -> shift",
        "FK  destination_location_id -> location",
        "FK  origin_polygon_id -> dig_polygon (Pillar 1)",
        "    material_type, payload_est_t",
        "    queue_shovel_start_utc ... return_end_utc",
    ]),
    "haul_cycle_stage_event": ("Transactional", [
        "PK  stage_event_id",
        "FK  haul_cycle_id -> haul_cycle",
        "FK  equipment_id -> mobile_equipment",
        "    stage_type, start_ts, end_ts, duration_s",
        "    tum_category",
    ]),
    "location": ("Reference", [
        "PK  location_id",
        "    location_name, location_type",
        "    coordinates_wgs84, active_flag",
    ]),
    "stockpile_inventory_movement": ("Transactional", [
        "PK  movement_id",
        "FK  stockpile_zone_id -> location",
        "FK  equipment_id -> mobile_equipment",
        "FK  shift_id -> shift",
        "    movement_type, mass_t, grade_cu_pct/zn_pct",
    ]),
    "delay_event": ("Transactional", [
        "PK  delay_id",
        "FK  equipment_id -> mobile_equipment",
        "FK  shift_id -> shift",
        "FK  work_order_id -> work_order (Pillar 5, gap)",
        "    delay_start_utc, delay_end_utc, tum_category",
    ]),
    "work_order": ("External (Pillar 5)", [
        "PK  work_order_id",
        "    (owned by Maintenance & Reliability)",
        "    referenced by delay_event.work_order_id — gap XP-01",
    ]),
}

TAB1_ROW_A = [
    "mobile_equipment_source_minestar", "mobile_equipment_source_wenco",
    "mobile_equipment_source_xref", "mobile_equipment", "equipment_class",
    "operator_shift_assignment", "operator", "shift",
]
TAB1_ROW_B = [
    "dig_polygon", "haul_cycle", "haul_cycle_stage_event", "location",
    "stockpile_inventory_movement", "delay_event", "work_order",
]

TAB1_RELATIONSHIPS = [
    ("mobile_equipment_source_minestar", "mobile_equipment_source_xref", "mapped via"),
    ("mobile_equipment_source_wenco", "mobile_equipment_source_xref", "mapped via"),
    ("mobile_equipment_source_xref", "mobile_equipment", "resolves to (1 master : N source rows)"),
    ("mobile_equipment", "equipment_class", "classified as (N:1)"),
    ("mobile_equipment", "operator_shift_assignment", "assigned via (1:N)"),
    ("operator", "operator_shift_assignment", "assigned via (1:N)"),
    ("shift", "operator_shift_assignment", "contains (1:N)"),
    ("mobile_equipment", "haul_cycle", "performs / loads (1:N, as truck or shovel)"),
    ("mobile_equipment", "delay_event", "subject of (1:N)"),
    ("mobile_equipment", "haul_cycle_stage_event", "subject of (1:N)"),
    ("operator", "delay_event", "records (1:N, recorded_by)"),
    ("shift", "haul_cycle", "contains (1:N)"),
    ("shift", "delay_event", "contains (1:N)"),
    ("shift", "stockpile_inventory_movement", "contains (1:N)"),
    ("haul_cycle", "dig_polygon", "originates from — cross-pillar, Pillar 1"),
    ("haul_cycle", "haul_cycle_stage_event", "parent of (1:N)"),
    ("haul_cycle", "location", "delivers to (N:1)"),
    ("stockpile_inventory_movement", "location", "at (N:1, stockpile zone)"),
    ("haul_cycle", "stockpile_inventory_movement", "feeds (1:0..1, additions)"),
    ("haul_cycle", "delay_event", "may link to (1:0..1)"),
    ("delay_event", "work_order", "should link to — cross-pillar, Pillar 5, gap XP-01 unenforced"),
]

TAB1_TYPE_COLOR = {
    "Master": ("#DAE8FC", "#6C8EBF"),
    "Reference": ("#D5E8D4", "#82B366"),
    "Transactional": ("#FFE6CC", "#D79B00"),
    "Source": ("#F8CECC", "#B85450"),
    "Map": ("#E1D5E7", "#9673A6"),
}
TAB1_LEGEND = [
    ("Master", "Governed, deduplicated representation of a business entity"),
    ("Reference", "Bounded, low-cardinality lookup/classification list"),
    ("Transactional", "A discrete business event with its own natural key"),
    ("Source (Teck-specific)", "Raw per-source-system record — duplicates intact"),
    ("Map (Teck-specific)", "Crosswalk from a Master ID to Source ID(s), with a validity window"),
    ("External / cross-pillar (dashed)", "Owned by another pillar's product; referenced, not modeled here"),
]

TAB1 = DiagramSpec("Curated ER Model", "mfd-training-mock-erd", TAB1_ENTITY_DEFS,
                    TAB1_ROW_A, TAB1_ROW_B, TAB1_RELATIONSHIPS, TAB1_TYPE_COLOR, TAB1_LEGEND)


# ============================================================================
# TAB 2 — Contextualized dimensional model (beam-overlay.yaml Section 7)
# ============================================================================

TAB2_ENTITY_DEFS = {
    "dim_site": ("Dimension", [
        "PK  site_code",
        "    site_name, region",
    ]),
    "dim_shift": ("Dimension", [
        "PK  shift_id",
        "FK  site_code -> dim_site",
        "    shift_date, shift_type",
        "    shift_start_utc, shift_end_utc",
    ]),
    "dim_equipment": ("Dimension", [
        "PK  equipment_master_id",
        "    fleet_number, equipment_class",
        "    make, model, nominal_payload_t",
        "    [depends on OI-009 mastering gap]",
    ]),
    "dim_operator": ("Dimension", [
        "PK  operator_id",
        "    operator_name, authorization_classes",
        "    employment_type",
    ]),
    "dim_tum_category": ("Dimension", [
        "PK  tum_category_code",
        "    category_label",
        "FK  parent_category_code -> self",
        "    is_productive, standard_alignment",
        "    [GMG hierarchy unverified, see notes]",
    ]),
    "dim_material_type": ("Dimension", [
        "PK  material_type_code (ore|waste|marginal)",
        "    material_type_label",
    ]),
    "dim_location": ("Dimension", [
        "PK  location_id",
        "    location_name, location_type",
        "    [required on movement, optional on TUM]",
    ]),
    "fct_equipment_time_usage": ("Fact", [
        "FK  site_code, shift_id",
        "FK  equipment_master_id, operator_id",
        "FK  tum_category_code",
        "FK  location_id (optional, degenerate)",
        "    duration_s, episode_count",
        "grain: site+shift+equipment+operator+category",
    ]),
    "fct_material_movement": ("Fact", [
        "FK  site_code, shift_id",
        "FK  equipment_master_id (truck), operator_id",
        "FK  material_type_code",
        "FK  location_id (destination, required)",
        "    payload_t, cycle_count",
        "grain: site+shift+equipment+operator+material+dest",
    ]),
    "kpi_tum_availability": ("KPI Group", [
        "Physical Availability = AT / CT",
        "Use of Availability = OT / AT",
        "Effective Utilization = (WT+PT) / CT",
        "grain: site, shift, equipment, operator",
    ]),
    "kpi_reliability": ("KPI Group", [
        "MTBF = AT / DT episodes (unscheduled)",
        "  [cross-pillar, needs Pillar 5 work_order]",
        "MTBS = AT / all DT episodes",
        "MTTR = DT duration / DT episodes",
    ]),
    "kpi_material_movement": ("KPI Group", [
        "Total Material Moved = SUM(payload_t)",
        "Ore Moved / Waste Moved (by material_type)",
        "Strip Ratio = Waste Moved / Ore Moved",
    ]),
}

TAB2_ROW_A = [
    "dim_tum_category", "dim_site", "dim_shift", "dim_equipment", "dim_operator",
    "dim_material_type", "dim_location",
]
TAB2_ROW_B = [
    "fct_equipment_time_usage", "kpi_tum_availability", "kpi_reliability",
    "fct_material_movement", "kpi_material_movement",
]

# (source, target, label, dashed)
TAB2_RELATIONSHIPS = [
    ("dim_tum_category", "fct_equipment_time_usage", "classifies (1:N)", False),
    ("dim_site", "fct_equipment_time_usage", "1:N", False),
    ("dim_site", "fct_material_movement", "1:N", False),
    ("dim_shift", "fct_equipment_time_usage", "1:N", False),
    ("dim_shift", "fct_material_movement", "1:N", False),
    ("dim_equipment", "fct_equipment_time_usage", "1:N", False),
    ("dim_equipment", "fct_material_movement", "1:N (truck)", False),
    ("dim_operator", "fct_equipment_time_usage", "1:N", False),
    ("dim_operator", "fct_material_movement", "1:N", False),
    ("dim_material_type", "fct_material_movement", "1:N", False),
    ("dim_location", "fct_material_movement", "1:N (required)", False),
    ("dim_location", "fct_equipment_time_usage", "optional, degenerate", True),
    ("fct_equipment_time_usage", "kpi_tum_availability", "derives", True),
    ("fct_equipment_time_usage", "kpi_reliability", "derives", True),
    ("fct_material_movement", "kpi_material_movement", "derives", True),
]

TAB2_TYPE_COLOR = {
    "Dimension": ("#D5E8D4", "#82B366"),
    "Fact": ("#FFE6CC", "#D79B00"),
    "KPI Group": ("#E1D5E7", "#9673A6"),
}
TAB2_LEGEND = [
    ("Dimension", "Conformed or new reference dimension — site, shift, equipment, operator, tum_category, material_type, location"),
    ("Fact", "Base metric grain — the intermediate layer the first version of Section 7 skipped"),
    ("KPI Group", "Named industry KPIs, grouped; dashed 'derives' edges show which fact each is built from"),
]

TAB2 = DiagramSpec("Contextualized Dimensional Model", "mfd-training-mock-dimensional",
                    TAB2_ENTITY_DEFS, TAB2_ROW_A, TAB2_ROW_B, TAB2_RELATIONSHIPS,
                    TAB2_TYPE_COLOR, TAB2_LEGEND)


def generate():
    out = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    out.append('<mxfile host="app.diagrams.net" agent="erd_layout.py" version="3.0">\n')
    out.append(render_diagram(TAB1, "t1_"))
    out.append(render_diagram(TAB2, "t2_"))
    out.append("</mxfile>\n")
    return "".join(out)


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    xml = generate()
    with open(argv[0], "w", encoding="utf-8", newline="\n") as fh:
        fh.write(xml)
    print("Wrote %s — tab 1: %d entities/%d relationships; tab 2: %d entities/%d relationships"
          % (argv[0], len(TAB1.entity_defs), len(TAB1.relationships),
             len(TAB2.entity_defs), len(TAB2.relationships)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
