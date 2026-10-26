# Pillar 3 — Processing & Beneficiation: BPMN Diagrams

Companion to [03-processing-and-beneficiation.md](../../03-processing-and-beneficiation.md). Source: the **Process Decomposition** section (L2 → L3 → L4) and the **Process Flow Narratives**.

Same method and naming standard as [Pillar 2](../02-mining-operations-extraction/README.md): `bpmn-style-guide` layout rules, L2 shows L3 as collapsed sub-processes, each L3 diagram carries its L4 steps as tasks with the row detail (ISA-95 level, actors, standards, DDVC layer, P754 annotation) in the task `documentation`.

PNG copies of every diagram are in [png/](png/), for document management. They are generated from the `.bpmn` files by [tools/bpmn_to_png.py](../tools/bpmn_to_png.py), so regenerate them after any diagram change: `python ../tools/bpmn_to_png.py . png` (needs Microsoft Edge).

## Process groups are generic (LL-005 to LL-015)

Process groups and L4 steps are site- and mineral-agnostic. A site's ore type, plant and facilities set which instances run and in what order; that is configuration, not a different diagram. See the pillar's *Circuit Configuration Variants* and the overlay's `process_configuration` section.

| Pattern | Reused for | Shown on |
|---|---|---|
| 3.2.1 Reagent Management & Pulp Conditioning | Every flotation circuit and every separation | 3.2 L2 loop; 3.2.3 calls it as a narrative step |
| 3.2.2 Flotation Circuit | Each target mineral or bulk concentrate, in sequence or parallel | 3.2 L2 loop *Another target mineral in tailings?* |
| 3.2.3 Concentrate Separation | Each bulk concentrate | 3.2 L2 *Concentrate destination?* (Saleable / Bulk / Waste) |
| 3.3.1 Thickening | Each saleable concentrate, bulk concentrate, and the tailings | 3.3 L2 *Tailings stream?*; 3.2.3.1 refers to it |
| 3.3.2 Concentrate Filtration, 3.3.3 Drying & Packaging | Each saleable concentrate train | 3.3 L2 |
| 3.5 Tailings Management, 3.6 Water Management | Each facility and water system | Optional groups as gateways (*Classification fitted?*, *Treatment required?*) |

## Building and checking

```
python -I ../tools/build_pillar3.py        # generated diagrams + doc sync + coverage
python -I "%USERPROFILE%\.claude\skills\bpmn-style-guide\scripts\check_bpmn_layout.py" *.bpmn
python -I ../../../BPMN-generator/tools/bpmn_verify.py .
python -I ../tools/bpmn_to_png.py . png
```

[tools/build_pillar3.py](../tools/build_pillar3.py) uses the shared engine [tools/bpmn_build.py](../tools/bpmn_build.py). It:
- **generates** the L1, 3.2, 3.3, 3.5 and 3.6 diagrams and all their L3 diagrams from a declared structure, taking names and documentation from the pillar file;
- **syncs** the hand-laid diagrams (3.1, 3.4 and their L3): names and documentation of numbered steps and the L2 / L3 pool documentation are refreshed from the pillar file, layout untouched;
- **checks coverage**: every L2, L3 and L4 row drawn exactly once, every L2 and L3 with its own diagram, no diagram step without a row.

Status 2026-10-26: 29 files; layout checker 0 errors; `bpmn_verify.py` 29 / 29 pass; coverage OK (6 L2, 22 L3, 71 L4 rows); every PNG rendered with every element drawn.

## Diagram index

| Level | Diagram | L4 handling |
|---|---|---|
| L1 | [3 Processing & Beneficiation](3_processing-and-beneficiation.bpmn) | L2 areas as collapsed sub-processes; 3.4 from its own shift start; 3.6 from site water demand; associations for data and water links |
| L2 | [3.1 Comminution](3.1_comminution.bpmn) | L3 as collapsed sub-processes |
| L2 | [3.2 Concentration (Flotation)](3.2_concentration-flotation.bpmn) | L3 collapsed; pattern reuse loop; three-way concentrate destination |
| L2 | [3.3 Dewatering & Product Handling](3.3_dewatering-and-product-handling.bpmn) | L3 collapsed; thickening for every stream; tailings to 3.5 |
| L2 | [3.4 Metallurgical Accounting & Quality](3.4_metallurgical-accounting-and-quality.bpmn) | L3 as collapsed sub-processes |
| L2 | [3.5 Tailings Management](3.5_tailings-management.bpmn) | L3 collapsed; classification optional; deposition and construction in parallel |
| L2 | [3.6 Water Management](3.6_water-management.bpmn) | L3 collapsed; supply, reclaim and seepage in parallel, then distribution and the balance |
| L3 | [3.1.1 Primary Crushing](3.1.1_primary-crushing.bpmn) | L4 as tasks |
| L3 | [3.1.2 Secondary/Tertiary Crushing & Screening](3.1.2_secondary-tertiary-crushing-and-screening.bpmn) | L4 as tasks; pebble crushing is a second flow |
| L3 | [3.1.3 Grinding & Classification](3.1.3_grinding-and-classification.bpmn) | L4 as tasks; media addition is a second flow |
| L3 | [3.2.1 Reagent Management & Pulp Conditioning](3.2.1_reagent-management-and-pulp-conditioning.bpmn) | L4 as tasks; activation / depression conditional |
| L3 | [3.2.2 Flotation Circuit](3.2.2_flotation-circuit.bpmn) | Pattern; three OSA-driven decisions |
| L3 | [3.2.3 Concentrate Separation](3.2.3_concentrate-separation.bpmn) | Pattern; conditioning via 3.2.1; sink and float products in parallel |
| L3 | [3.3.1 Thickening](3.3.1_thickening.bpmn) | Pattern; overflow recovery in parallel with underflow |
| L3 | [3.3.2 Concentrate Filtration](3.3.2_concentrate-filtration.bpmn) | Filtrate recovery in parallel; re-filter loop; ends CTP-2 |
| L3 | [3.3.3 Concentrate Drying & Packaging](3.3.3_concentrate-drying-and-packaging.bpmn) | Each step conditional on the product specification |
| L3 | [3.4.1 Sampling](3.4.1_sampling.bpmn) | L4 as tasks (parallel) |
| L3 | [3.4.2 Assay & Analysis](3.4.2_assay-and-analysis.bpmn) | L4 as tasks; OSA is a second flow |
| L3 | [3.4.3 Mass Balance & Reconciliation](3.4.3_mass-balance-and-reconciliation.bpmn) | L4 as tasks; ends with a message end event (Finance) |
| L3 | [3.5.1 Tailings Transport & Distribution](3.5.1_tailings-transport-and-distribution.bpmn) | Pipeline integrity decision |
| L3 | [3.5.2 Tailings Classification](3.5.2_tailings-classification.bpmn) | Conditional group; fines and sand split; sand quality decision |
| L3 | [3.5.3 Tailings Deposition](3.5.3_tailings-deposition.bpmn) | Beach width decision |
| L3 | [3.5.4 Embankment Construction](3.5.4_embankment-construction.bpmn) | Placement QA decision; survey as a second flow |
| L3 | [3.5.5 Facility Storage & Safety Monitoring](3.5.5_facility-storage-and-safety-monitoring.bpmn) | Ends with an operating constraint when criteria are breached |
| L3 | [3.6.1 Makeup Water Supply](3.6.1_makeup-water-supply.bpmn) | Treatment conditional; pumped vs received check |
| L3 | [3.6.2 Reclaim Water](3.6.2_reclaim-water.bpmn) | Low pond decision |
| L3 | [3.6.3 Seepage & Drainage Collection](3.6.3_seepage-and-drainage-collection.bpmn) | Pump-start decision |
| L3 | [3.6.4 Process Water Supply & Distribution](3.6.4_process-water-supply-and-distribution.bpmn) | Low storage decision |
| L3 | [3.6.5 Site Water Balance & Reconciliation](3.6.5_site-water-balance-and-reconciliation.bpmn) | Balance tolerance decision; ends with a message |

Retired 2026-10-26 (LL-012, LL-014): `3.3.1_concentrate-thickening` (now `3.3.1_thickening`), `3.3.3_tailings-management` (now 3.5 and 3.6), `3.3.4_concentrate-drying-and-packaging` (now 3.3.3).
Retired 2026-10-23 (LL-005): `3.2.1_reagent-management`, `3.2.2_copper-flotation-circuit`, `3.2.3_zinc-flotation-circuit`, `3.2.4_lead-flotation-circuit`. The ID mapping is in the pillar's *Revision Notes*.

## Decisions on how the processes are drawn

| Topic | Representation |
|---|---|
| Mineral-specific circuits | Not drawn as separate diagrams. One Flotation Circuit pattern (3.2.2) is reused per configured target mineral; the 3.2 L2 loop shows the reuse. |
| Optional process groups | Exclusive gateway with a bypass: *Concentrate destination?* (3.2.3), *Drying or packaging required?* (3.3.3), *Secondary crushing fitted?* (3.1.2), *Activation or depression required?* (3.2.1.3), *Classification fitted?* (3.5.2), *Treatment required?* (3.6.1.2). Which sites run which is configuration and belongs in the overlay. |
| Regrind (3.2.2.3) | A task on the main path before the cleaner. The documentation says it applies only where a regrind mill is installed. |
| Pebble crushing (3.1.2.3) | Its own flow in 3.1.2. In 3.1.3 a narrative task diverts pebbles to it. |
| Grinding media addition (3.1.3.4) | A separate scheduled flow in 3.1.3. |
| OSA analysis (3.4.2.2) | A continuous second flow in 3.4.2. |
| Concentrate and tailings streams (3.3) | One Thickening pattern for every stream; *Tailings stream?* hands thickened tailings to 3.5. The concentrate train repeats per saleable concentrate. |
| Hand-offs | 3.3.2 ends with a message end event, "Filter cake to shed (CTP-2)". 3.3.3 ends with a message end event to Logistics for packed product. 3.4.3 ends with a message end event to Finance and waits on a message catch event, "Shift composite assays returned". |
| Decisions | Every gateway question is from the Process Flow Narratives. `Yes` / `No` sit beside the exits. |
| Measurement points | Role-based (MP-01 to MP-10 metal accounting; TP-01 to TP-05 tailings; WP-01 to WP-11 water) and instantiated per circuit, stream, user or destination, in the task documentation. |
| Optional merges | An unnamed exclusive gateway merges a bypass back into the main path (3.3, 3.3.3). Where a sub-process or task is reached by two paths (3.5.3, 3.5.5, 3.6.1.4), it merges them itself. |

## Issues in the source model

These came up while drawing. Fixing pillar content needs explicit instruction and a learning entry.

### Resolved 2026-10-23

| Item | Resolution |
|---|---|
| Commodity-specific flotation process groups (3.2.2 Cu, 3.2.3 Zn, 3.2.4 Pb) repeating one pattern | Replaced by the Flotation Circuit and Concentrate Separation patterns (LL-005) |
| Regrind rows (3.2.2.4, 3.2.3.5, 3.2.4.3) listed after the cleaner although they run before it | Regrind is now 3.2.2.3, before the cleaner 3.2.2.4 (LL-005) |
| Eight rows missing the Primary Actor column (3.2.3.x, 3.2.4.x, 3.3.3.2) | Zn and Pb rows retired; actor added to 3.3.3.2 (LL-007) |
| Unescaped pipe characters inside `[P754: …]` annotations broke the markdown tables | Escaped as `\|` (LL-007) |
| Molybdenum by-product circuit not decomposed (gap G1) | Covered by Concentrate Separation (3.2.3) and Drying & Packaging (3.3.3) (LL-005) |
| Tailings management a single thin L3 (3.3.3); water management out of scope | Generic 3.5 Tailings Management and 3.6 Water Management (LL-014) |
| Thickening described three times (concentrate, bulk, tailings) | One Thickening pattern, 3.3.1 (LL-012) |
| L1: 3.4 unreachable from a start event (`bpmn_verify` M8) | 3.4 now starts from "Shift start" |

### Open

| Item | Conflict | How the diagram handles it |
|---|---|---|
| 3.4.3.3 vs 3.4.3.4 | 3.4.3.3 Produce Monthly Metal Accounting Report lists "stocktake completed" as a trigger. 3.4.3.4 Conduct Inventory Adjustment and Stocktake lists "Monthly close" as a trigger. The narrative also puts the stocktake after the close. | Drawn stocktake first (3.4.3.4 → 3.4.3.3), following the 3.4.3.3 trigger. |

### L4 gaps: narrative steps with no L4 row

| Diagram | Step drawn from the narrative only | Why it matters |
|---|---|---|
| 3.1.1 | Throttle SAG mill feed rate and alert control room | COS low-level response has no L4 row |
| 3.1.3 | Divert pebbles to pebble crusher | Link to 3.1.2.3 |
| 3.1.3 | Adjust cyclone apex, feed density or throughput | P80 off-target response |
| 3.2.2 | Raise collector dose or cut air rate; Investigate feed, reagent or OSA fault; Adjust froth depth or cleaning | OSA-driven process changes are logged but have no row |
| 3.2.3 | Adjust depressant dose or cleaning | Separation product quality response |
| 3.3.1 | Reduce feed rate or increase flocculant | Underflow density response |
| 3.5.x, 3.6.x | One response step per decision: stop transfer; divert sand; relocate discharge; rework fill; investigate transfer loss; stop reclaim; increase makeup draw; investigate balance | Responses to monitoring decisions; add rows if a product needs their data |
| 3.3.2 | Adjust filter cycle, wash water or air; Transfer filter cake to concentrate shed | The transfer creates the production record, the CTP-2 opening entry |
| 3.4.1 | Submit shift composite samples to LIMS | LIMS sample registration has no step (the same gap as Pillar 2 2.1.5) |
| 3.4.2 | Issue re-assay instruction; Release results in LIMS | QC accept/reject outcome |
| 3.4.3 | Investigate balance error; escalate | Mass balance closure failure path |

Each carries a documentation note saying it comes from the narrative.
