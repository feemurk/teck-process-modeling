#!/usr/bin/env python3
"""
bpmn_layout.py — compute real BPMN DI geometry for Teck BPMN files.

WHY THIS EXISTS
---------------
Lucidchart does NOT auto-layout a BPMN 2.0 import. It honours the <bpmndi:BPMNShape>
coordinates literally. A file emitted with placeholder x="0" y="0" on every shape imports
as a single stack of overlapping shapes jammed into one corner, with the lanes rendered
empty. Real coordinates are mandatory, not cosmetic.

WHAT IT DOES
------------
Reads a .bpmn file, computes a lane-aware left-to-right layout from the sequence flow graph,
and rewrites ONLY the <bpmndi:BPMNDiagram> block. All model XML — elements, IDs, attributes,
comments, formatting — is left byte-identical.

LAYOUT ALGORITHM
----------------
  shape size: tasks and sub-processes are sized from their own label text, not a fixed
               constant. A label is word-wrapped at the shape's baseline width using an
               estimated character width; if the resulting text still overflows the
               baseline height, the shape widens (up to a cap) and height is recomputed
               from the new, shorter wrap. This is what keeps a long task name — e.g.
               "Load Truck with Shovel (2.2.2.3) — TUM: PT (shovel) / WT (truck)" — from
               being clipped inside a box sized for a short one. Gateways and events keep
               fixed icon sizes; Lucid places their labels outside the icon.
  x (column) : longest-path rank over the sequence-flow DAG. Back edges (loops) are detected
               by DFS and excluded from ranking, so a loop-back does not push its target right.
               Boundary events are pinned to their host's rank via a zero-weight edge.
  y (row)    : the node's lane. Multiple nodes in the same (lane, column) cell stack into
               sub-rows; the vertical pitch between sub-rows expands to the tallest shape
               actually present in the file, so a widened/heightened box never overlaps its
               neighbour in the same lane. The lane grows to fit.
  edges      : orthogonal routing. Forward edges exit the source's right edge and enter the
               target's left edge. Back edges drop out of the source's bottom, run through a
               dedicated horizontal channel below the nodes, and enter the target's bottom.
               Boundary events exit downward.

USAGE
-----
    python bpmn_layout.py <file.bpmn | directory> [...]
"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict, deque

BPMN = "http://www.omg.org/spec/BPMN/20100524/MODEL"

TASK_TYPES = {"task", "serviceTask", "userTask", "manualTask", "sendTask",
              "receiveTask", "scriptTask", "businessRuleTask", "callActivity"}
SUBPROCESS_TYPES = {"subProcess", "transaction", "adHocSubProcess"}
GATEWAY_TYPES = {"exclusiveGateway", "parallelGateway", "inclusiveGateway",
                 "eventBasedGateway", "complexGateway"}
EVENT_TYPES = {"startEvent", "endEvent", "intermediateCatchEvent",
               "intermediateThrowEvent", "boundaryEvent"}
NODE_TYPES = TASK_TYPES | SUBPROCESS_TYPES | GATEWAY_TYPES | EVENT_TYPES

# --- layout constants (px) ---------------------------------------------------
POOL_X, POOL_Y = 160, 80
POOL_LABEL_W = 30        # vertical label band on the left of the pool
LANE_LABEL_W = 30        # vertical label band on the left of each lane
LEFT_PAD, RIGHT_PAD = 50, 60
H_GAP = 70               # horizontal gap between columns
V_PITCH_MIN = 130        # floor on vertical pitch between stacked nodes in one lane
V_MARGIN = 40            # clearance added above the tallest shape when setting pitch
LANE_PAD = 25            # padding at top and bottom inside a lane
LANE_MIN_H = 160
BACK_GAP = 35            # first back-edge channel offset below the nodes
BACK_STEP = 22           # additional offset per extra back edge

# --- label-driven shape sizing -------------------------------------------------
# Lucidchart wraps a task/sub-process label inside its box and does not grow the box
# to fit — text that doesn't fit is clipped or crowds the border. These constants drive
# a word-wrap estimate so the box is sized to the label instead of a one-size guess.
AVG_CHAR_PX = 5.6         # deliberately generous width per character at 8pt, so the
                          # estimate over- rather than under-shoots wrapped line count
LINE_HEIGHT_PX = 14
SHAPE_H_PAD = 16          # left+right inset subtracted from width before wrapping
SHAPE_V_PAD = 20          # top+bottom inset before the first/last text line

# (baseline_w, baseline_h, max_w, max_h)
TASK_BOX = (140, 80, 220, 160)
SUBPROCESS_BOX = (160, 100, 220, 160)


def wrap_line_count(label, width):
    """Approximate word-wrapped line count of `label` inside a box of `width` px."""
    if not label:
        return 1
    usable = max(24, width - SHAPE_H_PAD)
    chars_per_line = max(6, int(usable / AVG_CHAR_PX))
    lines = 1
    cur = 0
    for word in label.split():
        add = len(word) if cur == 0 else len(word) + 1
        if cur + add > chars_per_line and cur > 0:
            lines += 1
            cur = len(word)
        else:
            cur += add
    return lines


def size_of(tag, label=""):
    if tag in GATEWAY_TYPES:
        return (50, 50)
    if tag not in TASK_TYPES and tag not in SUBPROCESS_TYPES:
        return (36, 36)

    base_w, base_h, max_w, max_h = TASK_BOX if tag in TASK_TYPES else SUBPROCESS_BOX

    def needed_h(w):
        return max(base_h, SHAPE_V_PAD + wrap_line_count(label, w) * LINE_HEIGHT_PX)

    h = needed_h(base_w)
    if h <= base_h:
        return (base_w, base_h)
    # baseline width can't hold the label without clipping — widen, then re-wrap
    return (max_w, min(max_h, needed_h(max_w)))


def q(tag):
    return "{%s}%s" % (BPMN, tag)


def local(el):
    return el.tag.split("}", 1)[-1]


# --- model extraction --------------------------------------------------------

def read_model(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    root = ET.fromstring(raw)

    collab = root.find(q("collaboration"))
    participant = collab.find(q("participant")) if collab is not None else None
    proc = root.find(q("process"))
    if proc is None:
        raise ValueError("no <bpmn:process> element")

    lane_set = proc.find(q("laneSet"))
    lanes = []
    lane_of = {}
    if lane_set is not None:
        for idx, lane in enumerate(lane_set.findall(q("lane"))):
            refs = [r.text.strip() for r in lane.findall(q("flowNodeRef"))]
            lanes.append({"id": lane.get("id"), "name": lane.get("name") or "", "refs": refs})
            for r in refs:
                lane_of[r] = idx

    nodes = OrderedDict()
    boundary_host = OrderedDict()
    flows = []
    for child in proc:
        tag = local(child)
        if tag in NODE_TYPES:
            nid = child.get("id")
            label = child.get("name") or ""
            w, h = size_of(tag, label)
            nodes[nid] = {"id": nid, "tag": tag, "w": w, "h": h,
                          "lane": lane_of.get(nid, 0)}
            if tag == "boundaryEvent":
                boundary_host[nid] = child.get("attachedToRef")
        elif tag == "sequenceFlow":
            flows.append({"id": child.get("id"),
                          "src": child.get("sourceRef"),
                          "tgt": child.get("targetRef")})

    return {
        "diagram_id": (proc.get("id") or "").replace("_proc", ""),
        "plane_ref": (collab.get("id") if collab is not None else proc.get("id")),
        "pool_id": participant.get("id") if participant is not None else None,
        "lanes": lanes,
        "nodes": nodes,
        "boundary_host": boundary_host,
        "flows": flows,
    }


# --- ranking -----------------------------------------------------------------

def compute_ranks(nodes, flows, boundary_host):
    """Longest-path rank with back edges removed. Boundary events share their host's rank."""
    edges = [(f["src"], f["tgt"], 1) for f in flows
             if f["src"] in nodes and f["tgt"] in nodes]
    for b, host in boundary_host.items():
        if host in nodes:
            edges.append((host, b, 0))

    succ = OrderedDict((n, []) for n in nodes)
    indeg = dict((n, 0) for n in nodes)
    for u, v, w in edges:
        succ[u].append((v, w))
        indeg[v] += 1

    # DFS back-edge detection (0 = unvisited, 1 = on stack, 2 = done)
    color = dict((n, 0) for n in nodes)
    back = set()
    roots = [n for n in nodes if indeg[n] == 0] + list(nodes)
    for root in roots:
        if color[root] != 0:
            continue
        color[root] = 1
        stack = [(root, iter(succ[root]))]
        while stack:
            u, it = stack[-1]
            descended = False
            for v, w in it:
                if color[v] == 1:
                    back.add((u, v))
                elif color[v] == 0:
                    color[v] = 1
                    stack.append((v, iter(succ[v])))
                    descended = True
                    break
            if not descended:
                color[u] = 2
                stack.pop()

    # longest path over forward edges only
    fsucc = OrderedDict((n, []) for n in nodes)
    findeg = dict((n, 0) for n in nodes)
    for u, v, w in edges:
        if (u, v) in back:
            continue
        fsucc[u].append((v, w))
        findeg[v] += 1

    rank = dict((n, 0) for n in nodes)
    queue = deque(n for n in nodes if findeg[n] == 0)
    while queue:
        u = queue.popleft()
        for v, w in fsucc[u]:
            if rank[v] < rank[u] + w:
                rank[v] = rank[u] + w
            findeg[v] -= 1
            if findeg[v] == 0:
                queue.append(v)

    lo = min(rank.values()) if rank else 0
    return dict((n, r - lo) for n, r in rank.items()), back


# --- geometry ----------------------------------------------------------------

def layout(model):
    nodes = model["nodes"]
    lanes = model["lanes"] or [{"id": None, "name": "", "refs": list(nodes)}]
    boundary_host = model["boundary_host"]
    rank, back = compute_ranks(nodes, model["flows"], boundary_host)

    placed = [n for n in nodes if n not in boundary_host]

    # column widths
    ncols = max([rank[n] for n in placed] or [0]) + 1
    col_w = [50] * ncols
    for n in placed:
        col_w[rank[n]] = max(col_w[rank[n]], nodes[n]["w"])

    lane_x = POOL_X + POOL_LABEL_W
    col_x = []
    x = lane_x + LANE_LABEL_W + LEFT_PAD
    for c in range(ncols):
        col_x.append(x)
        x += col_w[c] + H_GAP
    lane_w = (x - H_GAP + RIGHT_PAD) - lane_x

    # Vertical pitch must clear the tallest shape actually present, or two shapes
    # stacked in the same lane/column cell would overlap once labels grow a box
    # past the baseline height (see size_of).
    tallest = max([nodes[n]["h"] for n in placed], default=0)
    v_pitch = max(V_PITCH_MIN, tallest + V_MARGIN)

    # sub-row slots within each (lane, column) cell
    cells = OrderedDict()
    slot = {}
    for n in placed:
        key = (nodes[n]["lane"], rank[n])
        cells.setdefault(key, [])
        slot[n] = len(cells[key])
        cells[key].append(n)

    lane_slots = [0] * len(lanes)
    for (li, _c), members in cells.items():
        if li < len(lane_slots):
            lane_slots[li] = max(lane_slots[li], len(members))

    lane_geom = []
    y = POOL_Y
    for li, lane in enumerate(lanes):
        h = max(LANE_MIN_H, 2 * LANE_PAD + lane_slots[li] * v_pitch)
        lane_geom.append({"id": lane["id"], "x": lane_x, "y": y, "w": lane_w, "h": h})
        y += h
    pool_h = y - POOL_Y
    pool_w = POOL_LABEL_W + lane_w

    shapes = OrderedDict()
    for n in placed:
        nd = nodes[n]
        c = rank[n]
        cx = col_x[c] + col_w[c] / 2.0
        lg = lane_geom[min(nd["lane"], len(lane_geom) - 1)]
        cy = lg["y"] + LANE_PAD + slot[n] * v_pitch + v_pitch / 2.0
        shapes[n] = {"x": int(round(cx - nd["w"] / 2.0)), "y": int(round(cy - nd["h"] / 2.0)),
                     "w": nd["w"], "h": nd["h"]}

    # boundary events sit on the host's bottom edge
    for b, host in boundary_host.items():
        nd = nodes[b]
        hs = shapes.get(host)
        if hs is None:
            continue
        shapes[b] = {"x": int(round(hs["x"] + hs["w"] * 0.72 - nd["w"] / 2.0)),
                     "y": int(round(hs["y"] + hs["h"] - nd["h"] / 2.0)),
                     "w": nd["w"], "h": nd["h"]}

    pool = {"x": POOL_X, "y": POOL_Y, "w": pool_w, "h": pool_h}
    return {"pool": pool, "lanes": lane_geom, "shapes": shapes,
            "back": back, "boundary_host": boundary_host}


def route(model, geom):
    """Orthogonal waypoints per sequence flow."""
    shapes = geom["shapes"]
    boundary_host = geom["boundary_host"]
    pool = geom["pool"]
    edges = OrderedDict()
    back_n = 0

    for f in model["flows"]:
        s, t = shapes.get(f["src"]), shapes.get(f["tgt"])
        if s is None or t is None:
            continue
        s_cx, s_cy = s["x"] + s["w"] / 2.0, s["y"] + s["h"] / 2.0
        t_cx, t_cy = t["x"] + t["w"] / 2.0, t["y"] + t["h"] / 2.0

        if f["src"] in boundary_host:
            # drop out of the boundary event, then run in to the target's left edge
            wps = [(s_cx, s["y"] + s["h"]), (s_cx, t_cy), (t["x"], t_cy)]
        elif t["x"] >= s["x"] + s["w"] + 20:
            if abs(s_cy - t_cy) < 2:
                wps = [(s["x"] + s["w"], s_cy), (t["x"], t_cy)]
            else:
                mx = (s["x"] + s["w"] + t["x"]) / 2.0
                wps = [(s["x"] + s["w"], s_cy), (mx, s_cy), (mx, t_cy), (t["x"], t_cy)]
        else:
            ch = max(s["y"] + s["h"], t["y"] + t["h"]) + BACK_GAP + back_n * BACK_STEP
            ch = min(ch, pool["y"] + pool["h"] - 8)
            back_n += 1
            wps = [(s_cx, s["y"] + s["h"]), (s_cx, ch), (t_cx, ch), (t_cx, t["y"] + t["h"])]

        edges[f["id"]] = [(int(round(a)), int(round(b))) for a, b in wps]
    return edges


# --- emit --------------------------------------------------------------------

def render_di(model, geom, edges):
    did = model["diagram_id"]
    out = []
    a = out.append
    a('  <bpmndi:BPMNDiagram id="%s_diagram">' % did)
    a('    <bpmndi:BPMNPlane id="%s_plane" bpmnElement="%s">' % (did, model["plane_ref"]))

    if model["pool_id"]:
        p = geom["pool"]
        a('      <bpmndi:BPMNShape id="%s_di" bpmnElement="%s" isHorizontal="true">'
          % (model["pool_id"], model["pool_id"]))
        a('        <dc:Bounds x="%d" y="%d" width="%d" height="%d"/>' % (p["x"], p["y"], p["w"], p["h"]))
        a('      </bpmndi:BPMNShape>')

    for lg in geom["lanes"]:
        if not lg["id"]:
            continue
        a('      <bpmndi:BPMNShape id="%s_di" bpmnElement="%s" isHorizontal="true">' % (lg["id"], lg["id"]))
        a('        <dc:Bounds x="%d" y="%d" width="%d" height="%d"/>' % (lg["x"], lg["y"], lg["w"], lg["h"]))
        a('      </bpmndi:BPMNShape>')

    a('')
    for nid in model["nodes"]:
        s = geom["shapes"].get(nid)
        if s is None:
            continue
        extra = ' isExpanded="false"' if model["nodes"][nid]["tag"] in SUBPROCESS_TYPES else ''
        a('      <bpmndi:BPMNShape id="%s_di" bpmnElement="%s"%s>' % (nid, nid, extra))
        a('        <dc:Bounds x="%d" y="%d" width="%d" height="%d"/>' % (s["x"], s["y"], s["w"], s["h"]))
        a('      </bpmndi:BPMNShape>')

    a('')
    for f in model["flows"]:
        wps = edges.get(f["id"])
        if not wps:
            continue
        a('      <bpmndi:BPMNEdge id="%s_di" bpmnElement="%s">' % (f["id"], f["id"]))
        for wx, wy in wps:
            a('        <di:waypoint x="%d" y="%d"/>' % (wx, wy))
        a('      </bpmndi:BPMNEdge>')

    a('    </bpmndi:BPMNPlane>')
    a('  </bpmndi:BPMNDiagram>')
    return "\n".join(out)


DI_BLOCK = re.compile(r"[ \t]*<bpmndi:BPMNDiagram\b.*?</bpmndi:BPMNDiagram>", re.S)


def process_file(path):
    model = read_model(path)
    geom = layout(model)
    edges = route(model, geom)
    di = render_di(model, geom, edges)

    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if not DI_BLOCK.search(text):
        raise ValueError("no <bpmndi:BPMNDiagram> block found")
    new_text = DI_BLOCK.sub(lambda m: di, text, count=1)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(new_text)

    p = geom["pool"]
    return "%-24s %2d nodes  %2d flows  %d lanes  pool %dx%d" % (
        os.path.basename(path), len(geom["shapes"]), len(edges), len(geom["lanes"]),
        p["w"], p["h"])


def main(argv):
    targets = []
    for arg in argv:
        if os.path.isdir(arg):
            targets += [os.path.join(arg, f) for f in sorted(os.listdir(arg))
                        if f.endswith(".bpmn")]
        else:
            targets.append(arg)
    if not targets:
        print(__doc__)
        return 1
    for path in targets:
        print(process_file(path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
