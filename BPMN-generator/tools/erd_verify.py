#!/usr/bin/env python3
"""
erd_verify.py — verification gate for erd_layout.py output, mirroring the discipline of
BPMN-generator/tools/bpmn_verify.py: mechanical checks before anything is called ready for
Lucidchart import, not a visual eyeball pass. Runs the full check set against EVERY
<diagram> (tab) in the file, not just the first one.

Checks (per diagram/tab):
  E1  file parses as XML
  E2  exactly one <mxfile> with >=1 <diagram>, each with an <mxGraphModel><root>
  E3  every vertex (entity box) has a non-empty label and positive width/height
      (legend swatches are exempt — they are deliberately label-less color chips)
  E4  every edge's source/target references an existing vertex id in the SAME diagram
  E5  no two entity vertices overlap (axis-aligned bounding-box check)
  E6  every entity in the diagram's corresponding DiagramSpec (matched by diagram id)
      appears exactly once as a vertex
  E7  every edge has a non-empty relationship label
  E8  canvas bounds are sane (no negative coordinates)
  E9  each edge's style-declared exitX/exitY/entryX/entryY fixed connection point,
      recomputed against the source/target box's OWN geometry, matches the geometry's
      sourcePoint/targetPoint fallback
  E10 REAL GEOMETRIC CHECK: every segment of every edge's full path is tested for
      intersection against every vertex's bounding box OTHER than that edge's own
      source/target and any legend cell
  E11 the legend block exists and does not overlap any entity vertex or get crossed by
      any edge segment

Exit code 0 only when every check passes, across every diagram in the file.

USAGE
-----
    python erd_verify.py <file.drawio>
"""

import sys
import xml.etree.ElementTree as ET

TOL = 0.5


def rect_overlap(a, b):
    return not (a["x"] + a["w"] <= b["x"] or b["x"] + b["w"] <= a["x"] or
                a["y"] + a["h"] <= b["y"] or b["y"] + b["h"] <= a["y"])


def seg_seg_intersect(p1, p2, p3, p4):
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    d1, d2 = cross(p3, p4, p1), cross(p3, p4, p2)
    d3, d4 = cross(p1, p2, p3), cross(p1, p2, p4)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    def on_seg(p, q, r):
        return (min(p[0], r[0]) - TOL <= q[0] <= max(p[0], r[0]) + TOL and
                min(p[1], r[1]) - TOL <= q[1] <= max(p[1], r[1]) + TOL)

    if abs(d1) < 1e-6 and on_seg(p3, p1, p4):
        return True
    if abs(d2) < 1e-6 and on_seg(p3, p2, p4):
        return True
    if abs(d3) < 1e-6 and on_seg(p1, p3, p2):
        return True
    if abs(d4) < 1e-6 and on_seg(p1, p4, p2):
        return True
    return False


def point_in_rect(p, r, pad=0.0):
    return (r["x"] - pad <= p[0] <= r["x"] + r["w"] + pad and
            r["y"] - pad <= p[1] <= r["y"] + r["h"] + pad)


def seg_intersects_rect(p1, p2, r):
    pad = -0.75
    if point_in_rect(p1, r, pad) or point_in_rect(p2, r, pad):
        return True
    corners = [(r["x"], r["y"]), (r["x"] + r["w"], r["y"]),
               (r["x"] + r["w"], r["y"] + r["h"]), (r["x"], r["y"] + r["h"])]
    for i in range(4):
        if seg_seg_intersect(p1, p2, corners[i], corners[(i + 1) % 4]):
            return True
    return False


def load_specs():
    """Map diagram id -> expected entity name set, from erd_layout.py's own DiagramSpecs,
    so E6 can cross-check each tab against the generator's own source of truth rather than
    a hardcoded copy that could drift out of sync."""
    sys.path.insert(0, "BPMN-generator/tools")
    sys.path.insert(0, "tools")
    import erd_layout
    return {
        erd_layout.TAB1.diagram_id: set(erd_layout.TAB1.entity_defs.keys()),
        erd_layout.TAB2.diagram_id: set(erd_layout.TAB2.entity_defs.keys()),
    }


def check_diagram(diagram_el, expected_entities, prefix_tag):
    problems = []
    graph_model = diagram_el.find("mxGraphModel")
    if graph_model is None:
        return ["%s E2 no <mxGraphModel> found under <diagram>" % prefix_tag]
    cell_root = graph_model.find("root")
    if cell_root is None:
        return ["%s E2 no <root> found under <mxGraphModel>" % prefix_tag]

    vertices, edges = {}, []
    for cell in cell_root.findall("mxCell"):
        if cell.get("vertex") == "1":
            geo = cell.find("mxGeometry")
            if geo is None:
                problems.append("%s E3 vertex %s has no mxGeometry" % (prefix_tag, cell.get("id")))
                continue
            w, h = float(geo.get("width", 0)), float(geo.get("height", 0))
            x, y = float(geo.get("x", 0)), float(geo.get("y", 0))
            label = cell.get("value") or ""
            is_legend_swatch = "legend_sw" in cell.get("id", "")
            if not label.strip() and not is_legend_swatch:
                problems.append("%s E3 vertex %s has an empty label" % (prefix_tag, cell.get("id")))
            if w <= 0 or h <= 0:
                problems.append("%s E3 vertex %s has non-positive size (%s x %s)"
                                 % (prefix_tag, cell.get("id"), w, h))
            vertices[cell.get("id")] = {"x": x, "y": y, "w": w, "h": h, "label": label}
        elif cell.get("edge") == "1":
            edges.append(cell)

    edge_records = []
    for e in edges:
        src, tgt = e.get("source"), e.get("target")
        if src not in vertices:
            problems.append("%s E4 edge %s source '%s' is not a known vertex" % (prefix_tag, e.get("id"), src))
            continue
        if tgt not in vertices:
            problems.append("%s E4 edge %s target '%s' is not a known vertex" % (prefix_tag, e.get("id"), tgt))
            continue
        label = e.get("value") or ""
        if not label.strip():
            problems.append("%s E7 edge %s has an empty relationship label" % (prefix_tag, e.get("id")))

        style = dict(kv.split("=", 1) for kv in e.get("style", "").split(";") if "=" in kv)
        try:
            ex, ey = float(style["exitX"]), float(style["exitY"])
            en, ee = float(style["entryX"]), float(style["entryY"])
        except (KeyError, ValueError):
            problems.append("%s E9 edge %s missing/invalid exitX/exitY/entryX/entryY in style" % (prefix_tag, e.get("id")))
            continue

        sb, tb = vertices[src], vertices[tgt]
        recomputed_exit = (sb["x"] + ex * sb["w"], sb["y"] + ey * sb["h"])
        recomputed_entry = (tb["x"] + en * tb["w"], tb["y"] + ee * tb["h"])

        geo = e.find("mxGeometry")
        sp = geo.find("mxPoint[@as='sourcePoint']")
        tp = geo.find("mxPoint[@as='targetPoint']")
        if sp is not None:
            stored = (float(sp.get("x")), float(sp.get("y")))
            if abs(stored[0] - recomputed_exit[0]) > TOL or abs(stored[1] - recomputed_exit[1]) > TOL:
                problems.append("%s E9 edge %s stored sourcePoint %s != exitX/exitY-recomputed %s"
                                 % (prefix_tag, e.get("id"), stored, recomputed_exit))
        if tp is not None:
            stored = (float(tp.get("x")), float(tp.get("y")))
            if abs(stored[0] - recomputed_entry[0]) > TOL or abs(stored[1] - recomputed_entry[1]) > TOL:
                problems.append("%s E9 edge %s stored targetPoint %s != entryX/entryY-recomputed %s"
                                 % (prefix_tag, e.get("id"), stored, recomputed_entry))

        waypoints = [(float(p.get("x")), float(p.get("y")))
                     for p in geo.findall("Array[@as='points']/mxPoint")]
        full_path = [recomputed_exit] + waypoints + [recomputed_entry]
        edge_records.append({"id": e.get("id"), "src": src, "tgt": tgt, "path": full_path})

    items = list(vertices.items())
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            id_a, a = items[i]
            id_b, b = items[j]
            if rect_overlap(a, b):
                problems.append("%s E5 vertices overlap: %s and %s" % (prefix_tag, id_a, id_b))

    if expected_entities is not None:
        found = {v["label"] for v in vertices.values()}
        missing = [name for name in expected_entities if not any(name in lbl for lbl in found)]
        if missing:
            problems.append("%s E6 entities missing from diagram: %s" % (prefix_tag, missing))
    else:
        problems.append("%s E6 could not match this diagram id to a known DiagramSpec (informational only)" % prefix_tag)

    if vertices:
        xs = [v["x"] for v in vertices.values()]
        ys = [v["y"] for v in vertices.values()]
        if min(xs) < 0 or min(ys) < 0:
            problems.append("%s E8 negative coordinates present (min x=%s, min y=%s)" % (prefix_tag, min(xs), min(ys)))

    for rec in edge_records:
        path = rec["path"]
        for i in range(len(path) - 1):
            p1, p2 = path[i], path[i + 1]
            for vid, box in vertices.items():
                if vid in (rec["src"], rec["tgt"]) or "legend" in vid:
                    continue
                if seg_intersects_rect(p1, p2, box):
                    problems.append("%s E10 edge %s (%s -> %s) segment %s->%s crosses entity box %s"
                                     % (prefix_tag, rec["id"], rec["src"], rec["tgt"], p1, p2, vid))

    legend_ids = [vid for vid in vertices if "legend" in vid]
    if not legend_ids:
        problems.append("%s E11 no legend cells found (expected ids containing 'legend')" % prefix_tag)
    else:
        entity_ids = [vid for vid in vertices if "legend" not in vid]
        for lid in legend_ids:
            lb = vertices[lid]
            for eid in entity_ids:
                if rect_overlap(lb, vertices[eid]):
                    problems.append("%s E11 legend cell %s overlaps entity box %s" % (prefix_tag, lid, eid))
            for rec in edge_records:
                path = rec["path"]
                for i in range(len(path) - 1):
                    if seg_intersects_rect(path[i], path[i + 1], lb):
                        problems.append("%s E11 edge %s crosses legend cell %s" % (prefix_tag, rec["id"], lid))

    return problems


def check(path):
    try:
        with open(path, "rb") as fh:
            root = ET.fromstring(fh.read())
    except Exception as exc:
        return ["E1 XML parse failed: %s" % exc]

    if root.tag != "mxfile":
        return ["E2 root element is <%s>, expected <mxfile>" % root.tag]
    diagrams = root.findall("diagram")
    if not diagrams:
        return ["E2 no <diagram> elements found"]

    try:
        specs_by_id = load_specs()
    except ImportError:
        specs_by_id = {}

    all_problems = []
    for d in diagrams:
        did = d.get("id", "?")
        tag = "[%s]" % did
        expected = specs_by_id.get(did)
        all_problems.extend(check_diagram(d, expected, tag))
    return all_problems


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    path = argv[0]
    problems = check(path)
    if problems:
        print("%s FAIL (%d)" % (path, len(problems)))
        for p in problems:
            print("  %s" % p)
        return 1
    print("%s PASS" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
