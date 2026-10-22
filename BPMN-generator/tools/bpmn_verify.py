#!/usr/bin/env python3
"""
bpmn_verify.py — verification gate for Teck BPMN files before Lucidchart import.

Runs 15 checks per file in two groups.

MODEL checks (is the BPMN valid and faithful to the spec?)
  M1  file parses as XML
  M2  every sequenceFlow sourceRef/targetRef resolves to a real flow node
  M3  every flow node is referenced by exactly one lane
  M4  declared <incoming>/<outgoing> match the actual sequence flows
  M5  no start event has an incoming flow; no end event has an outgoing flow
  M6  every gateway `default` attribute names one of that gateway's own outgoing flows
  M7  parallel gateways are 1->N forks or N->1 joins
  M8  every non-boundary node is reachable from a start event

RENDER checks (will it actually draw in Lucidchart?)
  R1  every flow node has a BPMNShape; every sequence flow has a BPMNEdge
  R2  no shape sits at the origin placeholder, and coordinates are not all identical
      (this is the exact failure mode that produced the stacked-blob import)
  R3  no two node shapes overlap (boundary events are exempt against their own host)
  R4  every node shape lies inside the bounds of its own lane
  R5  lanes are contiguous, non-overlapping, share one x/width, and sum to the pool height
  R6  every edge has >= 2 waypoints
  R7  each edge's first waypoint touches the source shape and last touches the target shape

Exit code is 0 only when every file passes every check.

USAGE
-----
    python bpmn_verify.py <file.bpmn | directory> [...]
"""

import os
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict, deque

BPMN = "http://www.omg.org/spec/BPMN/20100524/MODEL"
BPMNDI = "http://www.omg.org/spec/BPMN/20100524/DI"
DC = "http://www.omg.org/spec/DD/20100524/DC"
DI = "http://www.omg.org/spec/DD/20100524/DI"

TASK_TYPES = {"task", "serviceTask", "userTask", "manualTask", "sendTask",
              "receiveTask", "scriptTask", "businessRuleTask", "callActivity"}
SUBPROCESS_TYPES = {"subProcess", "transaction", "adHocSubProcess"}
GATEWAY_TYPES = {"exclusiveGateway", "parallelGateway", "inclusiveGateway",
                 "eventBasedGateway", "complexGateway"}
EVENT_TYPES = {"startEvent", "endEvent", "intermediateCatchEvent",
               "intermediateThrowEvent", "boundaryEvent"}
NODE_TYPES = TASK_TYPES | SUBPROCESS_TYPES | GATEWAY_TYPES | EVENT_TYPES

TOL = 2  # px tolerance for waypoint-touches-shape


def q(ns, tag):
    return "{%s}%s" % (ns, tag)


def local(el):
    return el.tag.split("}", 1)[-1]


def overlap(a, b):
    return not (a["x"] + a["w"] <= b["x"] or b["x"] + b["w"] <= a["x"] or
                a["y"] + a["h"] <= b["y"] or b["y"] + b["h"] <= a["y"])


def touches(pt, s):
    x, y = pt
    on_v = (abs(x - s["x"]) <= TOL or abs(x - (s["x"] + s["w"])) <= TOL) and \
           (s["y"] - TOL <= y <= s["y"] + s["h"] + TOL)
    on_h = (abs(y - s["y"]) <= TOL or abs(y - (s["y"] + s["h"])) <= TOL) and \
           (s["x"] - TOL <= x <= s["x"] + s["w"] + TOL)
    return on_v or on_h


def check(path):
    problems = []
    try:
        with open(path, "rb") as fh:
            root = ET.fromstring(fh.read())
    except Exception as exc:                                        # M1
        return ["M1 XML parse failed: %s" % exc]

    proc = root.find(q(BPMN, "process"))
    if proc is None:
        return ["M1 no <bpmn:process> element"]

    nodes, boundary_host, flows = OrderedDict(), {}, OrderedDict()
    for child in proc:
        tag = local(child)
        if tag in NODE_TYPES:
            nodes[child.get("id")] = {"tag": tag, "el": child}
            if tag == "boundaryEvent":
                boundary_host[child.get("id")] = child.get("attachedToRef")
        elif tag == "sequenceFlow":
            flows[child.get("id")] = (child.get("sourceRef"), child.get("targetRef"))

    lane_of, lane_ids, lane_hits = {}, [], {}
    lane_set = proc.find(q(BPMN, "laneSet"))
    if lane_set is not None:
        for idx, lane in enumerate(lane_set.findall(q(BPMN, "lane"))):
            lane_ids.append(lane.get("id"))
            for r in lane.findall(q(BPMN, "flowNodeRef")):
                nid = r.text.strip()
                lane_hits[nid] = lane_hits.get(nid, 0) + 1
                lane_of[nid] = idx

    # ---- M2 ----
    for fid, (s, t) in flows.items():
        if s not in nodes:
            problems.append("M2 flow %s sourceRef '%s' is not a flow node" % (fid, s))
        if t not in nodes:
            problems.append("M2 flow %s targetRef '%s' is not a flow node" % (fid, t))

    # ---- M3 ----
    for nid in nodes:
        c = lane_hits.get(nid, 0)
        if c == 0:
            problems.append("M3 node %s is not referenced by any lane" % nid)
        elif c > 1:
            problems.append("M3 node %s is referenced by %d lanes" % (nid, c))
    for nid in lane_hits:
        if nid not in nodes:
            problems.append("M3 lane references unknown node %s" % nid)

    # ---- M4, M5, M6, M7 ----
    for nid, meta in nodes.items():
        el = meta["el"]
        decl_in = sorted(e.text.strip() for e in el.findall(q(BPMN, "incoming")))
        decl_out = sorted(e.text.strip() for e in el.findall(q(BPMN, "outgoing")))
        act_in = sorted(f for f, (s, t) in flows.items() if t == nid)
        act_out = sorted(f for f, (s, t) in flows.items() if s == nid)
        if decl_in != act_in:
            problems.append("M4 %s incoming declared %s actual %s" % (nid, decl_in, act_in))
        if decl_out != act_out:
            problems.append("M4 %s outgoing declared %s actual %s" % (nid, decl_out, act_out))
        if meta["tag"] == "startEvent" and act_in:
            problems.append("M5 startEvent %s has incoming flow(s)" % nid)
        if meta["tag"] == "endEvent" and act_out:
            problems.append("M5 endEvent %s has outgoing flow(s)" % nid)
        if meta["tag"] in GATEWAY_TYPES:
            d = el.get("default")
            if d and d not in act_out:
                problems.append("M6 gateway %s default '%s' is not one of its outgoing flows" % (nid, d))
        if meta["tag"] == "parallelGateway":
            if not ((len(act_in) == 1 and len(act_out) >= 2) or
                    (len(act_in) >= 2 and len(act_out) == 1)):
                problems.append("M7 parallelGateway %s has in=%d out=%d (not a fork or join)"
                                % (nid, len(act_in), len(act_out)))

    # ---- M8 ----
    starts = [n for n, m in nodes.items() if m["tag"] == "startEvent"]
    succ = {}
    for s, t in flows.values():
        succ.setdefault(s, []).append(t)
    for b, host in boundary_host.items():
        succ.setdefault(host, []).append(b)
    seen, dq = set(starts), deque(starts)
    while dq:
        u = dq.popleft()
        for v in succ.get(u, []):
            if v not in seen:
                seen.add(v)
                dq.append(v)
    for nid in nodes:
        if nid not in seen:
            problems.append("M8 node %s is unreachable from any start event" % nid)

    # ---- geometry ----
    shapes, edges = OrderedDict(), OrderedDict()
    for sh in root.iter(q(BPMNDI, "BPMNShape")):
        b = sh.find(q(DC, "Bounds"))
        if b is None:
            problems.append("R1 shape %s has no dc:Bounds" % sh.get("id"))
            continue
        shapes[sh.get("bpmnElement")] = {"x": float(b.get("x")), "y": float(b.get("y")),
                                         "w": float(b.get("width")), "h": float(b.get("height"))}
    for ed in root.iter(q(BPMNDI, "BPMNEdge")):
        edges[ed.get("bpmnElement")] = [(float(w.get("x")), float(w.get("y")))
                                        for w in ed.findall(q(DI, "waypoint"))]

    # ---- R1 ----
    for nid in nodes:
        if nid not in shapes:
            problems.append("R1 no BPMNShape for node %s" % nid)
    for fid in flows:
        if fid not in edges:
            problems.append("R1 no BPMNEdge for flow %s" % fid)

    node_shapes = OrderedDict((n, shapes[n]) for n in nodes if n in shapes)

    # ---- R2 ----
    at_origin = [n for n, s in node_shapes.items() if s["x"] == 0 and s["y"] == 0]
    if at_origin:
        problems.append("R2 %d shape(s) sit at placeholder origin (0,0): %s"
                        % (len(at_origin), ", ".join(sorted(at_origin)[:4])))
    positions = set((s["x"], s["y"]) for s in node_shapes.values())
    if len(node_shapes) > 1 and len(positions) == 1:
        problems.append("R2 every shape shares one position — Lucidchart will stack them")

    # ---- R3 ----
    items = list(node_shapes.items())
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a_id, a = items[i]
            b_id, b = items[j]
            if boundary_host.get(a_id) == b_id or boundary_host.get(b_id) == a_id:
                continue
            if overlap(a, b):
                problems.append("R3 shapes overlap: %s and %s" % (a_id, b_id))

    # ---- R4 / R5 ----
    lane_shapes = [shapes[l] for l in lane_ids if l in shapes]
    if len(lane_shapes) == len(lane_ids) and lane_shapes:
        for i in range(1, len(lane_shapes)):
            prev, cur = lane_shapes[i - 1], lane_shapes[i]
            if abs((prev["y"] + prev["h"]) - cur["y"]) > TOL:
                problems.append("R5 lanes %s and %s are not contiguous" % (lane_ids[i - 1], lane_ids[i]))
            if abs(prev["x"] - cur["x"]) > TOL or abs(prev["w"] - cur["w"]) > TOL:
                problems.append("R5 lanes %s and %s differ in x/width" % (lane_ids[i - 1], lane_ids[i]))
        pools = [s for e, s in shapes.items() if e not in nodes and e not in lane_ids]
        if pools:
            pool = pools[0]
            total = sum(l["h"] for l in lane_shapes)
            if abs(total - pool["h"]) > TOL:
                problems.append("R5 lane heights total %d but pool height is %d" % (total, pool["h"]))
        for nid, s in node_shapes.items():
            li = lane_of.get(nid)
            if li is None or li >= len(lane_shapes):
                continue
            lane = lane_shapes[li]
            inside = (s["x"] >= lane["x"] - TOL and s["x"] + s["w"] <= lane["x"] + lane["w"] + TOL
                      and s["y"] >= lane["y"] - TOL and s["y"] + s["h"] <= lane["y"] + lane["h"] + TOL)
            if not inside and nid not in boundary_host:
                problems.append("R4 node %s falls outside its lane %s" % (nid, lane_ids[li]))

    # ---- R6 / R7 ----
    for fid, wps in edges.items():
        if len(wps) < 2:
            problems.append("R6 edge %s has %d waypoint(s)" % (fid, len(wps)))
            continue
        if fid not in flows:
            continue
        s_id, t_id = flows[fid]
        if s_id in shapes and not touches(wps[0], shapes[s_id]):
            problems.append("R7 edge %s first waypoint does not touch source %s" % (fid, s_id))
        if t_id in shapes and not touches(wps[-1], shapes[t_id]):
            problems.append("R7 edge %s last waypoint does not touch target %s" % (fid, t_id))

    return problems


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
        return 2

    failed = 0
    for path in targets:
        problems = check(path)
        name = os.path.basename(path)
        if problems:
            failed += 1
            print("%-24s FAIL (%d)" % (name, len(problems)))
            for p in problems:
                print("      %s" % p)
        else:
            print("%-24s PASS" % name)
    print("-" * 52)
    print("%d file(s) checked, %d failed" % (len(targets), failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
