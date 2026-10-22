# Pillar 2 — Mining Operations (Extraction): BPMN Diagrams

Companion to [02-mining-operations-extraction.md](../../02-mining-operations-extraction.md). Source: the **Process Decomposition** section (L2 → L3 → L4). The pillar model itself is unchanged.

Layout follows the `bpmn-style-guide` rules (one screen at 1,920 px, 8 steps a row, 5 lanes at most, loop-backs outside the pool). All files are BPMN 2.0 XML with diagram information and open in bpmn.io, Camunda Modeler or any BPMN 2.0 tool.

## Diagram index

| Level | Diagram | L4 handling |
|---|---|---|
| L1 | [2 Mining Operations (Extraction)](2_mining-operations-extraction.bpmn) | L2 areas as collapsed sub-processes; 2.3 runs alongside 2.1 and 2.2 and is linked to 2.2 by an association |
| L2 | [2.1 Drill & Blast](2.1_drill-and-blast.bpmn) | L3 as collapsed sub-processes |
| L2 | [2.2 Load & Haul](2.2_load-and-haul.bpmn) | L3 as collapsed sub-processes |
| L2 | [2.3 Mine Services](2.3_mine-services.bpmn) | L3 as **expanded groups with L4 shown inside** |
| L3 | [2.1.1 Blast Design & Pattern Layout](2.1.1_blast-design-and-pattern-layout.bpmn) | L4 as tasks |
| L3 | [2.1.2 Drilling Execution](2.1.2_drilling-execution.bpmn) | L4 as tasks |
| L3 | [2.1.3 Charging & Stemming](2.1.3_charging-and-stemming.bpmn) | L4 as tasks |
| L3 | [2.1.4 Detonation & Assessment](2.1.4_detonation-and-assessment.bpmn) | L4 as tasks |
| L3 | [2.1.5 Muck Pile Preparation](2.1.5_muck-pile-preparation.bpmn) | L4 as tasks |
| L3 | [2.2.1 Face Preparation](2.2.1_face-preparation.bpmn) | L4 as tasks |
| L3 | [2.2.2 Loading](2.2.2_loading.bpmn) | L4 as tasks |
| L3 | [2.2.3 Hauling](2.2.3_hauling.bpmn) | L4 as tasks, plus destination override and 2.2.4.1 |
| L3 | [2.2.4 Stockpile Management](2.2.4_stockpile-management.bpmn) | 2.2.4.2 and 2.2.4.3 as tasks; 2.2.4.1 sits in 2.2.3 |
| L3 | [2.3.1 Haul Road Maintenance](2.3.1_haul-road-maintenance.bpmn) | L4 as tasks |
| L3 | [2.3.2 Pit Dewatering](2.3.2_pit-dewatering.bpmn) | L4 as tasks (parallel) |
| L3 | [2.3.3 Slope Stability Monitoring](2.3.3_slope-stability-monitoring.bpmn) | L4 as tasks (parallel) |

## Decision: where do the L4 steps go?

Tested the "roll L4 up into the L3 box" idea against the style-guide limits (16 steps per diagram, 8 per row).

| Area | L3 | L4 | Steps if all L4 shown on the L2 diagram | Verdict |
|---|---|---|---|---|
| 2.1 Drill & Blast | 5 | 19 | 24 + gateways + events | Over limit. Keep L3 collapsed. |
| 2.2 Load & Haul | 4 | 14 | 18 + gateways + events | Over limit. Keep L3 collapsed. |
| 2.3 Mine Services | 3 | 6 | 9 + events | Fits. Shown expanded as the test case. |

Result:

- **L2 diagrams show L3 as collapsed sub-processes** (2.1 and 2.2). Nothing else keeps them readable.
- **L2 2.3 shows L3 as expanded groups with L4 inside**, including 2.3.2 with its two L4 steps stacked. It fits at 742 × 888 and reads well, but it carries no decisions. The L3 diagrams for 2.3 still add the fork/join, the loop and the alert logic.
- **Each L3 diagram carries its L4 steps as plain tasks**, not as nested groups. The largest L3 has 5 L4 steps (2.2.3), so every L3 diagram stays on a single row of 8 columns or fewer. Nesting L4 groups inside L3 would add a level of boxes without freeing any space.
- The L4 rows are fine as single tasks. Their detail (inputs, outputs, TUM state, ISA-95 level, DDVC layer, actors) is stored in each task's BPMN `documentation`, so it is available in the modeler's properties panel without crowding the diagram.

## Naming standard

| Element | Pattern | Example |
|---|---|---|
| Folder | Same name as the pillar model file, without `.md` | `02-mining-operations-extraction` |
| File | `[decomposition ID]_[kebab-case title].bpmn`; `&` becomes `and` | `2.1.1_blast-design-and-pattern-layout.bpmn` |
| Pool name | `[ID] [Title]` as in the decomposition; L2 pools add ` (L2)` | `2.2.3 Hauling`, `2.2 Load & Haul (L2)` |
| Task / sub-process name | `[L4 or L3 ID] [Title]` exactly as in the decomposition table | `2.1.2.1 Navigate Drill Rig to Hole` |
| Narrative-only task | No ID; documentation note says it comes from the Process Flow Narratives | `Classify breakdown as TUM: DT` |
| Lane name | Actor role from the decomposition `Actor` column | `Drill & Blast Engineer` |
| Gateway name | A question | `Override needed?` |
| Event name | The state reached or awaited | `Haul cycle closed at face` |
| XML IDs | `[Type]_L[level]_[ID with underscores]`, plus a suffix for child elements | `Defs_L3_2_2_3`, `Pool_L3_2_2_3`, `Lane_L3_2_2_3_tr` |

Titles are copied from the decomposition table, not shortened or reworded.

## Conventions

- Task names carry the decomposition ID (e.g. `2.1.2.1 Navigate Drill Rig to Hole`) for traceability.
- Tasks without an ID are steps taken from the **Process Flow Narratives** section and not from a decomposition row (e.g. *Remediate or redesign rejected holes*, *Classify breakdown as TUM: DT*). Each carries a documentation note saying so.
- Gateways, events and loop-backs also come from the Process Flow Narratives section.
- Service task (gear marker): automated by SCADA or the monitoring system.
- Intermediate message catch event: waits on an external input (lab assays, blend plan).
- Message end event: hand-off out of the pillar (2.2.4 → Processing).
- Lane order is chosen to avoid flow crossings, not always initiator-first (e.g. 2.1.4).

## How the diagrams resolve the source-model issues

1. **2.1.1 step order: design before survey.** The diagram runs 2.1.1.2 Design Hole Layout Parameters → 2.1.1.3 Select Explosive Product → 2.1.1.1 Survey & Stake Pattern, because surveyors stake the *designed* collar coordinates. The decomposition lists survey first and gives 2.1.1.2 a "survey completion" trigger, which contradicts the 2.1.1.1 trigger ("approved blast pattern file"). The pillar model is unchanged; the trigger text on 2.1.1.1–2.1.1.3 would need a `CORRECTION:` to fix. 2.1.1.3 also lists "hole water measurement" as a trigger, which only exists after drilling (2.1.2.3). The diagram treats the design-time selection as initial and the per-hole selection as confirmed at charging.
2. **Stockpile management is a routing branch of the haul cycle, not a parallel stream.** See the next section.
3. **L4 gaps.** Steps that appear in the Process Flow Narratives but have no L4 row are drawn as tasks without an ID, each with a documentation note. See the table at the end.

## Decision: how stockpile management is represented

**Conclusion.** Stockpile management is not a stream parallel to Load & Haul. Its decision part sits inside the haul cycle; its inventory and reclaim part is a downstream hand-off.

| 2.2.4 element | Representation | Where |
|---|---|---|
| Choosing crusher vs stockpile vs waste | Planned destination assigned at 2.2.2.4; **runtime override** (Pillar 1 1.4.3.2) changes it | 2.2.3 gateway *Override needed?* → *Override destination (reason code)* → rejoin at *2.2.3.2 Queue at Destination* |
| 2.2.4.1 Build ROM Stockpile | Stockpile branch after the dump | 2.2.3 gateway *Stockpile dump?* → task 2.2.4.1 → rejoin the cycle |
| 2.2.4.2 Track Stockpile Grade | Inventory accounting, started by the recorded build | 2.2.4 L3 diagram |
| 2.2.4.3 Reclaim and Blend to Mill Feed | Separate cycle driven by the blend plan; the hand-off to Processing | 2.2.4 L3 diagram, ends with a message end event |

On the 2.2 L2 diagram, 2.2.4 stays a collapsed sub-process *after* the haul-cycle loop, as a sequential hand-off. 2.2.4.1 is drawn once, in 2.2.3, and not repeated in the 2.2.4 diagram.

**What the standards say.** The standards this model cites do not define stockpile management as its own process. ISA-95 treats a stockpile as material storage, and AMIRA P754 treats it as a custody-transfer and inventory measurement point (the model cites Principles 1 and 5). Stockpile-vs-crusher choice is a dispatch decision in FMS products and in Pillar 1 (1.4.3.1 and 1.4.3.2). The "parallel stream" reading came from the 2.2.4 row grouping, not from a standard. I did not check external sources beyond this repo.

## L4 gaps: narrative steps with no L4 row

The decomposition table (L3 → L4 rows) and the Process Flow Narratives section describe the same processes, but the narrative has more steps. A step with no L4 row has no ID, inputs/outputs, TUM state or DDVC layer, so it cannot be traced into the entity catalog. The diagrams still draw the ones that change the flow.

| Diagram | Step drawn from the narrative only | Why it matters |
|---|---|---|
| 2.1.2 | Remediate or redesign rejected holes | Rejected holes loop back to re-drilling |
| 2.1.5 | *Submit to Laboratory* is not drawn; only the wait *Lab assays returned* | LIMS sample registration has no step |
| 2.2.2 | Flag payload exception for review | Payload exceptions need a review step |
| 2.2.3 | Classify breakdown as TUM: DT | Creates a downtime delay event |
| 2.3.3 | Assess stability event; Issue operational constraint | The constraint creates OD/SBO delay events |
| 2.3.1 (not drawn) | Assess road condition; Assign grader and water truck | Supervisor steps |
| 2.2 (not drawn) | Assign equipment to shift | Covered by Pillar 1 1.4.2, so not a Pillar 2 gap |

Fixing them means adding L4 rows to the pillar model, which needs explicit instruction.
