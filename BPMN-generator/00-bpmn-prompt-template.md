# BPMN Generation Prompt Template
## Open-Pit Mining Value Chain — Lucidchart BPMN 2.0 XML

---

## How to Use This Template

1. Open a fresh Claude chat
2. Upload two files:
   - `{NN}-{pillar-name}.md` — the process model for the target pillar
   - `{NN}-{pillar-name}-bpmn-spec.md` — the BPMN element specification for the target pillar
3. Execute this prompt, substituting the bracketed values

---

## Prompt

```
You are a BPMN 2.0 expert producing Lucidchart-importable XML process diagrams for an
open-pit mining data programme at Teck Resources. You have been given two files:

1. **[PILLAR_NAME].md** — the full process model (business context, entities, narratives)
2. **[PILLAR_NAME]-bpmn-spec.md** — the BPMN element specification (IDs, types, flows)

Your task is to generate syntactically valid BPMN 2.0 XML for the diagrams specified in
the BPMN spec file. Generate one diagram at a time in the sequence listed in the
Diagram Inventory section of the spec file.

## Mandatory XML Requirements

1. **BPMN 2.0 namespace**: Use the following namespaces exactly:
   xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
   xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
   xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
   xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

2. **Root element**:
   <bpmn:definitions xmlns:bpmn="..." id="{DiagramID}_def" targetNamespace="http://teck.com/bpmn">

3. **Process element**: `isExecutable="false"` on all processes (documentation model)

4. **Lane sets**: Every task, gateway, and event must be referenced in a `<bpmn:laneSet>`
   with `<bpmn:lane>` elements containing `<bpmn:flowNodeRef>` for each element in that lane

5. **Sequence flows**: Every `<bpmn:sequenceFlow>` must have:
   - A unique `id` attribute (from the spec flow table)
   - `sourceRef` and `targetRef` matching valid element IDs
   - `name` attribute for conditional flows (the condition text from the spec)

6. **Gateway default flows**: Exclusive gateways should set `default` attribute to the
   most common/normal path flow ID

7. **Sub-processes**: Collapsed sub-processes use `<bpmn:subProcess triggeredByEvent="false">`
   with `flowElements` left empty (the sub-process content is in a separate diagram)

8. **Event types** — use these exact BPMN element types:
   - Start events: `<bpmn:startEvent>` with child `<bpmn:messageEventDefinition/>` (message)
     or `<bpmn:timerEventDefinition/>` (timer) or no child (none)
   - End events: `<bpmn:endEvent>` with child `<bpmn:errorEventDefinition/>` (error) or none
   - Intermediate catch: `<bpmn:intermediateCatchEvent>` with appropriate event definition child
   - Intermediate boundary: `<bpmn:boundaryEvent attachedToRef="{taskID}">` with event child

9. **DI block**: Include a `<bpmndi:BPMNDiagram>` block with `<bpmndi:BPMNPlane>`.

   **Lucidchart does NOT auto-layout a BPMN import. It honours DI coordinates literally.**
   Every shape given `x="0" y="0"` lands on the same point: the whole diagram imports as one
   stack of overlapping shapes in a corner with the lanes rendered empty. Real coordinates
   are mandatory.

   Standard sizes:
   - Tasks: width="140" height="80"
   - Sub-processes: width="160" height="100"
   - Gateways: width="50" height="50"
   - Events (start/end/intermediate/boundary): width="36" height="36"

   Required geometry rules:
   - **Pool**: one shape, `isHorizontal="true"`, its height equal to the sum of lane heights.
   - **Lanes**: stacked vertically and contiguous — each lane's `y` equals the previous lane's
     `y + height`. All lanes share the same `x` and `width`. Lanes are inset 30px from the
     pool's left edge to leave the pool label band: `lane.x = pool.x + 30`.
   - **Nodes**: `x` advances left-to-right with position in the flow; `y` places the node
     inside the vertical band of its own lane. No two node shapes may overlap. A node must
     sit entirely within its lane's bounds.
   - **Boundary events**: centred on the bottom edge of the host task.
   - **Edges**: at least two waypoints. The first must touch the source shape's boundary and
     the last must touch the target shape's boundary. Forward edges exit the source's right
     edge and enter the target's left edge; loop-back edges drop from the source's bottom,
     run through a horizontal channel below the nodes, and enter the target's bottom.

   Do not hand-compute this. Emit the model XML first, then run
   `tools/bpmn_layout.py` over the file — it derives the layout from the sequence-flow
   graph and rewrites only the `<bpmndi:BPMNDiagram>` block, leaving all model XML and
   comments byte-identical. Then run `tools/bpmn_verify.py` and resolve every finding.

10. **Participant/Pool**: Wrap the process in a `<bpmn:collaboration>` with
    `<bpmn:participant id="{PoolID}" name="{PoolName}" processRef="{processID}"/>`

## Output Format

For each diagram in the inventory:

1. State: `## Generating: {DiagramID} — {SequenceNumber} {Title}`
2. State the output file name, derived per the File Naming Standard below:
   `File: {FileName}.bpmn`
3. Output the complete, valid BPMN 2.0 XML in a fenced code block:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <bpmn:definitions ...>
     ...
   </bpmn:definitions>
   ```
4. After each diagram, state:
   `## Complete: {DiagramID} — {FileName}.bpmn — Ready for Lucidchart import`
   `Diagrams remaining: {list remaining diagram IDs}`

## File Naming Standard

Every generated diagram is saved to a file whose name carries the process decomposition
number from the pillar process model. This clusters every L2 diagram together with its own
L3 children in a directory listing and makes every file traceable to its section in the
pillar MD.

Format:

    P{pillar}_{sequence}_L{level}_{abbrev}.bpmn

Where:
- `P{pillar}`  — pillar number, e.g. `P2`
- `{sequence}` — the process decomposition number from the pillar MD, dots replaced by
                 hyphens: `2.1` becomes `2-1`; `2.1.1` becomes `2-1-1`
- `L{level}`   — diagram level, `L2` or `L3`
- `{abbrev}`   — the process abbreviation already used in the Diagram ID

Take the sequence number from the diagram's section heading in the BPMN spec file — e.g.
`## P2_L3_HUL — Hauling (L3, sub of 2.2.3)` yields `2-2-3`. If the spec section does not
state a number, take it from the Process Decomposition table of the pillar MD file.

Use hyphens, never dots: dots in a file name are ambiguous with the file extension and
some tools truncate at the first dot.

**The sequence number comes right after the pillar, ahead of the level.** This guarantees
that every file belonging to one process area — the L2 overview and all its L3 children —
sorts as one contiguous cluster in any directory listing, because `2-1` is a string prefix
of `2-1-1`, `2-1-2`, etc. That clustering is what `L{level}` ahead of `{sequence}` did not
give you: under the old scheme every L2 sorted into one block and every L3 into a separate
block below it, with no adjacency between a diagram and its own children.

The order *within* a cluster depends on which string comparison the tool uses:
- **Ordinal/byte comparison** — git, bash `ls`, Python's `sorted()`, most Unix tooling —
  sorts `2-1-1` before `2-1`, because `-` (0x2D) sorts before `_` (0x5F): children list
  first, parent last in each cluster.
- **Natural/culture-aware comparison** — PowerShell's `Sort-Object`, Windows Explorer —
  sorts `2-1` before `2-1-1`: parent first, children after.

Both give the same six files in one unbroken group; only the parent's position within it
changes. Rely on the grouping, not on which side of it the parent lands. (This also assumes
no level ever reaches a two-digit sibling count — `2-10` would not sort adjacent to
`2-1`–`2-9` under either scheme. None of the six pillars are close to that; revisit if one
ever is.)

**The Diagram ID itself does not change.** It remains the XML `id` prefix for every element
in the file (`P2_L3_HUL_def`, `P2_L3_HUL_T01`, …). Only the file name reorders around the
sequence infix, so the internal IDs stay stable and the BPMN spec files need no edits.

Examples (Pillar 2) — note how each L3 file shares its parent L2's sequence prefix:

| Diagram ID | Process Model Section | File Name |
|------------|----------------------|-----------|
| P2_L2_DB  | 2.1 Drill & Blast                   | `P2_2-1_L2_DB.bpmn`    |
| P2_L3_BDL | 2.1.1 Blast Design & Pattern Layout | `P2_2-1-1_L3_BDL.bpmn` |
| P2_L3_DRL | 2.1.2 Drilling Execution            | `P2_2-1-2_L3_DRL.bpmn` |
| P2_L2_LH  | 2.2 Load & Haul                     | `P2_2-2_L2_LH.bpmn`    |
| P2_L3_HUL | 2.2.3 Hauling                       | `P2_2-2-3_L3_HUL.bpmn` |
| P2_L2_MS  | 2.3 Mine Services                   | `P2_2-3_L2_MS.bpmn`    |

## Verification Checklist (self-check before output)

Before outputting each XML block, verify:
- [ ] Every element ID from the spec element inventory appears exactly once
- [ ] Every sequence flow references IDs that exist in the element inventory
- [ ] Every lane's `flowNodeRef` list is complete (no elements orphaned outside a lane)
- [ ] All gateways have the correct number of incoming/outgoing sequence flows
- [ ] Parallel gateways have exactly one incoming and N outgoing (fork) or N incoming and one outgoing (join)
- [ ] Sub-process IDs match the referenced diagram IDs in the spec inventory
- [ ] No placeholder text remains in the XML (no {brackets}, no "TODO")
- [ ] File name follows the File Naming Standard and carries the correct sequence number
      for that diagram's section in the pillar process model
- [ ] DI block carries real computed coordinates — no shape at x=0/y=0, no two shapes
      sharing a position, every node inside its own lane's bounds
- [ ] `tools/bpmn_verify.py` reports PASS for the file

## Sequence

Generate in the order listed in the Diagram Inventory table of the BPMN spec file.
Start with the L2 diagram, then generate each L3 sub-diagram for that L2 before
proceeding to the next L2. This ensures sub-process references resolve correctly.

## Error Handling

If you encounter an ambiguity in the spec (e.g., a flow references an ID not in the
element inventory), note the issue inline as an XML comment and resolve it using the
process narrative in the process model MD file before continuing. Do not halt generation.

Begin now with the first diagram in the Diagram Inventory.
```

---

## Verification Gate (mandatory before any Lucidchart import)

No generated diagram goes to Lucidchart until it passes this gate. The gate exists because
a BPMN file can be perfectly valid as a model and still import as an unreadable blob — the
model and the rendering are two separate correctness problems, and only the second one is
visible in Lucidchart.

```
python tools/bpmn_layout.py output/pillar-{NN}     # computes real DI geometry in place
python tools/bpmn_verify.py output/pillar-{NN}     # 15 checks per file; exit 0 = clear to import
```

`bpmn_layout.py` derives x/y from the sequence-flow graph (longest-path column ranking with
loop-back edges excluded, lane-based rows) and rewrites only the `<bpmndi:BPMNDiagram>`
block. All model XML and inline comments are left byte-identical, so it is safe to re-run.

`bpmn_verify.py` runs eight MODEL checks and seven RENDER checks per file:

| Group | Checks |
|-------|--------|
| MODEL | XML parses; flow endpoints resolve; every node in exactly one lane; declared incoming/outgoing match actual flows; start events have no incoming and end events no outgoing; gateway `default` names one of its own outgoing flows; parallel gateways are clean forks/joins; every node reachable from a start event |
| RENDER | every node has a shape and every flow an edge; no shape at the 0,0 placeholder and not all shapes co-located; no two shapes overlap; every node inside its own lane; lanes contiguous, aligned, summing to pool height; every edge has ≥2 waypoints; edge endpoints touch their source and target shapes |

A non-zero exit means do not import. Fix and re-run.

Spot-check by importing one L2 and one L3 diagram into Lucidchart and confirming that lanes
are populated, no shapes are stacked, and connectors attach to shape edges. The verifier
catches the mechanical failures; the human check catches taste (label overflow, crossings).

---

## Execution Checklist

Before running this prompt in a fresh chat, confirm:

- [ ] Target pillar MD file uploaded: `{NN}-{pillar-name}.md`
- [ ] BPMN spec file uploaded: `{NN}-{pillar-name}-bpmn-spec.md`
- [ ] Model selected: Claude Sonnet (sufficient for XML generation) or Claude Opus (for complex pillars)
- [ ] Note which diagrams to generate in this session (Lucidchart import limit is 1 file per import;
      consider generating L2 diagrams in one session and L3 diagrams in subsequent sessions grouped by L2)
- [ ] Python available to run the Verification Gate (`tools/bpmn_layout.py`, `tools/bpmn_verify.py`)

## Diagram Count by Pillar

| Pillar | L2 Diagrams | L3 Diagrams | Total |
|--------|-------------|-------------|-------|
| 1 — Mine Planning | 4 | 16 | 20 |
| 2 — Mining Operations | 3 | 12 | 15 |
| 3 — Processing | 4 | 11 | 15 |
| 4 — Logistics | 4 | 9 | 13 |
| 5 — Maintenance | 4 | 9 | 13 |
| 6 — Health & Safety | 5 | 9 | 14 |
| **Total** | **24** | **66** | **90** |

Pillar 2's row is verified against the actual generated and integrity-checked diagram set
(`output/pillar-02/`, 15 files, all passing `bpmn_verify.py`). The other five rows are as
originally documented and have not been independently re-checked against their own spec
files' Diagram Inventory tables — do so before treating them as final when that pillar's
turn comes.

## Recommended Session Breakdown

To avoid context limits in a single session, split generation as follows:

| Session | Content | Files to Upload |
|---------|---------|-----------------|
| Pillar N — L2 diagrams | All 4-5 L2 diagrams for the pillar | pillar MD + bpmn spec |
| Pillar N — L3 group A | L3 sub-diagrams for first 2 L2 process areas | pillar MD + bpmn spec |
| Pillar N — L3 group B | L3 sub-diagrams for remaining L2 process areas | pillar MD + bpmn spec |

For Pillar 2 (the most important — MFD anchor), generate all 11 diagrams in a single session;
it is the smallest pillar in diagram count and the most critical to validate first.

## Lucidchart Import Instructions

1. Save the generated XML per the File Naming Standard: `P{pillar}_{sequence}_L{level}_{abbrev}.bpmn`
   (e.g. `P2_2-2-3_L3_HUL.bpmn` for Hauling, process model section 2.2.3)
2. **Run the verification gate first — do not import a file that has not passed:**
   ```
   python tools/bpmn_layout.py output/pillar-{NN}      # compute real DI geometry
   python tools/bpmn_verify.py output/pillar-{NN}      # must report PASS on every file
   ```
3. In Lucidchart: File → Import → BPMN 2.0
4. Select the `.bpmn` file. Lucidchart renders the diagram at the coordinates in the file —
   it does not re-arrange anything, which is why step 2 is not optional.
5. Apply the Teck brand colour scheme manually after import:
   - Tasks: Teck blue (#00538C) fill, white text
   - Gateways: amber (#F5A623) fill
   - Start events: green (#28A745) fill
   - End events: red (#DC3545) fill
   - Sub-processes: light grey (#F5F5F5) fill, Teck blue border
6. Export to SVG or PDF for documentation embed in Confluence
