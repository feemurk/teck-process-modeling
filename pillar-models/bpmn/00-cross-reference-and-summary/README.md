# Value Chain (L0): BPMN Diagram

Companion to [00-cross-reference-and-summary.md](../../00-cross-reference-and-summary.md). Source: the **Value Chain Overview Diagram**, **Custody Transfer Point Summary** and Key Interfaces. The pillar models are unchanged.

| Level | Diagram | Child handling |
|---|---|---|
| L0 | [L0 Open-Pit Mining Value Chain](L0_open-pit-value-chain.bpmn) | Six pillars as collapsed sub-processes; L2 areas listed in each sub-process documentation. Each pillar's own L1 diagram is in its folder. |

## Levels

| Level | Scope | ID pattern | Where |
|---|---|---|---|
| L0 | The whole value chain; each box is a pillar | 1 to 6 | this folder |
| L1 | One pillar; each box is an L2 area | 2, 3 | the pillar folder, file `[pillar number]_[title].bpmn` |
| L2 | One area; each box is an L3 sub-process | 2.1 | the pillar folder |
| L3 | One sub-process; each box is an L4 step | 2.1.1 | the pillar folder |

The decomposition tables already number it this way: the pillar is "2", its areas "2.x" are labelled L2. The first version of this diagram was named L1 and was renamed L0 to match.

## What is drawn

- **Chain (sequence flows):** Start → 1 Planning → 2 Operations → 3 Processing → 4 Logistics → End. The flows between pillars carry the custody transfer points they cross (CTP-1, CTP-2). CTP-3, CTP-4 and CTP-5 sit inside Pillar 4, so CTP-5 is the end event.
- **Loop-backs (outside the pool):** 2 → 1 shift production report (actuals vs plan); 4 → 3 CoA commercial grade (mine-to-vessel reconciliation).
- **Cross-cutting pillars (associations, bottom lane):** 6 Health & Safety → 5 Maintenance & Reliability (permit to work gates work orders); 5 → 2 (work_order_id ↔ delay_event TUM:DT).
- Pillars 5 and 6 are in a lane of their own because they are not steps in the material flow.

## Not drawn

Kept off the diagram to stay within the style-guide limits (5 lanes, 3 loops). They are in the Key Interfaces list of the cross-reference file:

| Interface | Why left off |
|---|---|
| 4 → 1 concentrate production forecast | Fourth loop-back |
| 5 → 1 planned downtime windows | Fourth loop-back |
| 5 → 3, 4 calibration certificates (P754 Principle 8) | Association would cross the 3 and 4 lanes |
| 6 → 2, 3, 4 risk controls | Gate on every pillar; stated in the 6 documentation instead |

## Naming

Follows the Pillar 2 [naming standard](../02-mining-operations-extraction/README.md#naming-standard): XML IDs use `[Type]_L0_[id]`, sub-process names are `[ID] [Title]`.
