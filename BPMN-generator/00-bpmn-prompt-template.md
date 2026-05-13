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
   Set all `x`, `y` coordinates to 0 and `width`/`height` to standard values:
   - Tasks: width="100" height="80"
   - Gateways: width="50" height="50"
   - Events: width="36" height="36"
   - Sub-processes: width="150" height="100"
   - Lane: width="600" height="150"
   Lucidchart will auto-layout on import — placeholder coordinates are sufficient.

10. **Participant/Pool**: Wrap the process in a `<bpmn:collaboration>` with
    `<bpmn:participant id="{PoolID}" name="{PoolName}" processRef="{processID}"/>`

## Output Format

For each diagram in the inventory:

1. State: `## Generating: {DiagramID} — {Title}`
2. Output the complete, valid BPMN 2.0 XML in a fenced code block:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <bpmn:definitions ...>
     ...
   </bpmn:definitions>
   ```
3. After each diagram, state:
   `## Complete: {DiagramID} — Ready for Lucidchart import`
   `Diagrams remaining: {list remaining diagram IDs}`

## Verification Checklist (self-check before output)

Before outputting each XML block, verify:
- [ ] Every element ID from the spec element inventory appears exactly once
- [ ] Every sequence flow references IDs that exist in the element inventory
- [ ] Every lane's `flowNodeRef` list is complete (no elements orphaned outside a lane)
- [ ] All gateways have the correct number of incoming/outgoing sequence flows
- [ ] Parallel gateways have exactly one incoming and N outgoing (fork) or N incoming and one outgoing (join)
- [ ] Sub-process IDs match the referenced diagram IDs in the spec inventory
- [ ] No placeholder text remains in the XML (no {brackets}, no "TODO")

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

## Execution Checklist

Before running this prompt in a fresh chat, confirm:

- [ ] Target pillar MD file uploaded: `{NN}-{pillar-name}.md`
- [ ] BPMN spec file uploaded: `{NN}-{pillar-name}-bpmn-spec.md`
- [ ] Model selected: Claude Sonnet (sufficient for XML generation) or Claude Opus (for complex pillars)
- [ ] Note which diagrams to generate in this session (Lucidchart import limit is 1 file per import;
      consider generating L2 diagrams in one session and L3 diagrams in subsequent sessions grouped by L2)

## Diagram Count by Pillar

| Pillar | L2 Diagrams | L3 Diagrams | Total |
|--------|-------------|-------------|-------|
| 1 — Mine Planning | 4 | 16 | 20 |
| 2 — Mining Operations | 3 | 8 | 11 |
| 3 — Processing | 4 | 11 | 15 |
| 4 — Logistics | 4 | 9 | 13 |
| 5 — Maintenance | 4 | 9 | 13 |
| 6 — Health & Safety | 5 | 9 | 14 |
| **Total** | **24** | **62** | **86** |

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

1. Save the generated XML to a file: `{DiagramID}.bpmn`
2. In Lucidchart: File → Import → BPMN 2.0
3. Select the `.bpmn` file
4. Lucidchart will import and auto-layout the diagram
5. Apply the Teck brand colour scheme manually after import:
   - Tasks: Teck blue (#00538C) fill, white text
   - Gateways: amber (#F5A623) fill
   - Start events: green (#28A745) fill
   - End events: red (#DC3545) fill
   - Sub-processes: light grey (#F5F5F5) fill, Teck blue border
6. Export to SVG or PDF for documentation embed in Confluence
