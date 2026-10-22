# Pillar 3 — Processing & Beneficiation: BPMN Diagrams

Companion to [03-processing-and-beneficiation.md](../../03-processing-and-beneficiation.md). Source: the **Process Decomposition** section (L2 → L3 → L4) and the **Process Flow Narratives**. The pillar model itself is unchanged.

Same method and naming standard as [Pillar 2](../02-mining-operations-extraction/README.md): `bpmn-style-guide` layout rules, L2 shows L3 as collapsed sub-processes, each L3 diagram carries its L4 steps as tasks with the row detail (ISA-95 level, actors, standards, DDVC layer, P754 annotation) in the task `documentation`. All 17 files pass `check_bpmn_layout.py`.

## Diagram index

| Level | Diagram | L4 handling |
|---|---|---|
| L1 | [3 Processing & Beneficiation](3_processing-and-beneficiation.bpmn) | L2 areas as collapsed sub-processes; 3.4 runs alongside 3.1 to 3.3 and is linked to each by an association |
| L2 | [3.1 Comminution](3.1_comminution.bpmn) | L3 as collapsed sub-processes |
| L2 | [3.2 Concentration (Flotation)](3.2_concentration-flotation.bpmn) | L3 as collapsed sub-processes |
| L2 | [3.3 Dewatering & Product Handling](3.3_dewatering-and-product-handling.bpmn) | L3 as collapsed sub-processes |
| L2 | [3.4 Metallurgical Accounting & Quality](3.4_metallurgical-accounting-and-quality.bpmn) | L3 as collapsed sub-processes |
| L3 | [3.1.1 Primary Crushing](3.1.1_primary-crushing.bpmn) | L4 as tasks |
| L3 | [3.1.2 Secondary/Tertiary Crushing & Screening](3.1.2_secondary-tertiary-crushing-and-screening.bpmn) | L4 as tasks; pebble crushing is a second flow |
| L3 | [3.1.3 Grinding & Classification](3.1.3_grinding-and-classification.bpmn) | L4 as tasks; media addition is a second flow |
| L3 | [3.2.1 Reagent Management](3.2.1_reagent-management.bpmn) | L4 as tasks |
| L3 | [3.2.2 Copper Flotation Circuit](3.2.2_copper-flotation-circuit.bpmn) | L4 as tasks, three OSA-driven decisions |
| L3 | [3.2.3 Zinc Flotation Circuit](3.2.3_zinc-flotation-circuit.bpmn) | L4 as tasks |
| L3 | [3.2.4 Lead Flotation Circuit](3.2.4_lead-flotation-circuit.bpmn) | L4 as tasks |
| L3 | [3.3.1 Concentrate Thickening](3.3.1_concentrate-thickening.bpmn) | L4 as tasks |
| L3 | [3.3.2 Concentrate Filtration](3.3.2_concentrate-filtration.bpmn) | L4 as tasks; ends with a message end event (CTP-2) |
| L3 | [3.3.3 Tailings Management](3.3.3_tailings-management.bpmn) | L4 as tasks |
| L3 | [3.4.1 Sampling](3.4.1_sampling.bpmn) | L4 as tasks (parallel) |
| L3 | [3.4.2 Assay & Analysis](3.4.2_assay-and-analysis.bpmn) | L4 as tasks; OSA is a second flow |
| L3 | [3.4.3 Mass Balance & Reconciliation](3.4.3_mass-balance-and-reconciliation.bpmn) | L4 as tasks; ends with a message end event (Finance) |

The L1 diagram shows the four L2 areas. Pillar 3 has 4 L2, 13 L3 and 46 L4 rows. Every L3 and L4 row is drawn once.

## Decision: where do the L4 steps go?

Applied the Pillar 2 rule (16 steps per diagram, 8 per row). L4 counts per L2: 3.1 has 11, 3.2 has 15, 3.3 has 10, 3.4 has 10. None fits on its L2 diagram once the decisions and events are added, so all four L2 diagrams keep L3 collapsed. No L2 diagram uses the expanded-group form. The largest L3 has 5 L4 steps (3.2.3), so each L3 diagram fits in one row of 10 columns or fewer.

## Decisions on how the processes are drawn

| Topic | Representation |
|---|---|
| Optional circuits (secondary/tertiary crushing, Zn, Pb) | Exclusive gateway on the L2 diagram with a bypass (`Secondary crushing fitted?`, `Zn circuit fitted?`, `Pb circuit active?`). Which sites run which circuit is a Teck variant and belongs in the overlay, not the diagram. |
| Optional regrind mills (3.2.2.4, 3.2.3.5, 3.2.4.3) | Drawn as a task on the main path, before the cleaner. The documentation says they apply only where a regrind mill is installed. A gateway per commodity would add three diamonds with no information the sites do not already hold. |
| Pebble crushing (3.1.2.3) | Its own flow in 3.1.2. In 3.1.3 a narrative task diverts pebbles to it and returns them to the SAG mill. |
| Grinding media addition (3.1.3.4) | A separate scheduled flow in 3.1.3 (its own start event, "Ball addition interval reached"), not a step in the SAG → ball → cyclone chain. |
| OSA analysis (3.4.2.2) | A continuous second flow in 3.4.2, independent of the laboratory assay path. |
| Concentrate and tailings streams (3.3) | Parallel fork/join on the L2 diagram, as in the narrative. |
| Commodity-specific filter trains | One concentrate stream is drawn. The narrative says it repeats per commodity. |
| Hand-offs | 3.3.2 ends with a message end event, "Filter cake to shed (CTP-2)". 3.4.3 ends with a message end event to Finance. 3.4.3 waits on a message catch event, "Shift composite assays returned". |
| Decisions | Every gateway question is from the Process Flow Narratives. `Yes`/`No` labels sit beside the exits. |
| Shift-composite sampling in the flotation circuits | Not drawn in 3.2.2 to 3.2.4. The P754 measurement points (MP-05, MP-11, MP-15) are in the cleaner task documentation. The sampling steps are 3.4.1.1. |
| Daily, weekly and monthly cadence in 3.4.3 | Drawn as one sequence. The cadence is in the task documentation, not in separate start events. |

## Issues in the source model

These came up while drawing. None is fixed here; fixing them needs explicit instruction and a `CORRECTION:` entry.

### Order conflicts

| Item | Conflict | How the diagram handles it |
|---|---|---|
| 3.4.3.3 vs 3.4.3.4 | 3.4.3.3 Produce Monthly Metal Accounting Report lists "stocktake completed" as a trigger. 3.4.3.4 Conduct Inventory Adjustment and Stocktake lists "Monthly close" as a trigger. The narrative also puts the stocktake after the close. | Drawn stocktake first (3.4.3.4 → 3.4.3.3), following the 3.4.3.3 trigger. |
| 3.2.2.4, 3.2.3.5, 3.2.4.3 regrind | The table lists the regrind row after the cleaner, but the description and narrative put regrind before cleaning. | Drawn before the cleaner. |

### Missing Primary Actor column

Eight rows have 10 columns instead of 11. The Primary Actor(s) cell is absent, so every later cell is shifted left by one. The Actors line in their documentation reads "(not stated in decomposition)".

`3.2.3.2`, `3.2.3.3`, `3.2.3.4`, `3.2.3.5`, `3.2.4.1`, `3.2.4.2`, `3.2.4.3`, `3.3.3.2`

### L4 gaps: narrative steps with no L4 row

| Diagram | Step drawn from the narrative only | Why it matters |
|---|---|---|
| 3.1.1 | Throttle SAG mill feed rate and alert control room | COS low-level response has no L4 row |
| 3.1.3 | Divert pebbles to pebble crusher | Link to 3.1.2.3 |
| 3.1.3 | Adjust cyclone apex, feed density or throughput | P80 off-target response |
| 3.2.2 | Raise collector dose or cut air rate; Investigate feed shift and escalate; Add cleaning stages or adjust froth depth | OSA-driven process changes are logged but have no row |
| 3.3.1 | Reduce feed rate or increase flocculant | Underflow density response |
| 3.3.2 | Adjust filter cycle, wash water or air; Transfer filter cake to concentrate shed | The transfer creates the production record, the CTP-2 opening entry |
| 3.3.3 | Reduce tailings input; start water management | Freeboard response; "Monitor TSF" also has no row |
| 3.4.1 | Submit shift composite samples to LIMS | LIMS sample registration has no step (the same gap as Pillar 2 2.1.5) |
| 3.4.2 | Issue re-assay instruction; Release results in LIMS | QC accept/reject outcome |
| 3.4.3 | Investigate balance error; escalate | Mass balance closure failure path |

Each carries a documentation note saying it comes from the narrative.

### Not drawn

- The narrative's "Auto-sample rougher concentrate and tailings" step (3.2.2): covered by 3.4.1.1.
- The Cu, Zn and Pb differences between sites (Antamina, Red Dog, QB, HVC, CdA): site variants go in the overlay.
