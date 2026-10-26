# Pillar 3: Processing & Beneficiation — BPMN Generation Specification

## Purpose
Use alongside `03-processing-and-beneficiation.md` to generate Lucidchart BPMN 2.0 XML.
Same ID convention — prefix P3. AMIRA P754 measurement points are annotated on relevant tasks.

## Lucidchart BPMN 2.0 XML Notes
- Use `isExecutable="false"` on all processes (documentation model, not executable)
- Lane `flowNodeRef` elements must list every task/gateway/event ID that sits in that lane
- All `sequenceFlow` elements must reference valid `sourceRef` and `targetRef` IDs

### DI geometry — Lucidchart does NOT auto-layout
**Lucidchart honours the `<bpmndi:BPMNDiagram>` coordinates literally.** It does not
re-arrange anything on import. Placeholder coordinates (`x="0" y="0"` on every shape)
produce an import in which every shape is stacked on a single point in the corner and the
lanes render empty. Real computed coordinates are mandatory.

Do not hand-compute the geometry. Emit the model XML first, then run the repo tooling:

```
python tools/bpmn_layout.py output/pillar-03     # computes DI geometry in place
python tools/bpmn_verify.py output/pillar-03     # must PASS before any import
```

`bpmn_layout.py` derives the layout from the sequence-flow graph and rewrites only the
DI block — all model XML and inline comments stay byte-identical, so it is safe to re-run.
See the Verification Gate section of `00-bpmn-prompt-template.md` for the full protocol.

## Diagram Inventory
| Diagram ID | Level | Title | L3 Sub-diagrams |
|------------|-------|-------|-----------------|
| P3_L2_COM | L2 | Comminution | P3_L3_PRC, P3_L3_SCR, P3_L3_GRD |
| P3_L2_FLT | L2 | Concentration (Flotation) | P3_L3_RGT, P3_L3_FLC (pattern), P3_L3_SEP (pattern) |
| P3_L2_DWT | L2 | Dewatering & Product Handling | P3_L3_THK (pattern), P3_L3_FIL, P3_L3_DRY |
| P3_L2_MET | L2 | Metallurgical Accounting & Quality | P3_L3_SMP, P3_L3_ASY, P3_L3_MBA |
| P3_L2_TSF | L2 | Tailings Management | P3_L3_TTD, P3_L3_TCL, P3_L3_TDP, P3_L3_EMB, P3_L3_FSM |
| P3_L2_WAT | L2 | Water Management | P3_L3_MWS, P3_L3_RCW, P3_L3_SPG, P3_L3_PWD, P3_L3_WBL |

---

## P3_L2_COM — Comminution (L2)

### Pool & Lanes
| ID | Name |
|----|------|
| P3_L2_COM_PL | Comminution |
| P3_L2_COM_LN_DCS | DCS / Auto-control |
| P3_L2_COM_LN_OPR | Control Room Operator |
| P3_L2_COM_LN_MET | Metallurgist |
| P3_L2_COM_LN_FMS | FMS (ROM interface) |

### Element Inventory
| ID | Type | Name | Lane | Notes |
|----|------|------|------|-------|
| P3_L2_COM_SE | startEvent (message) | ROM ore available at crusher pocket; plant running | P3_L2_COM_LN_FMS | |
| P3_L2_COM_SP01 | subProcess (collapsed) | Primary Crushing (3.1.1) | P3_L2_COM_LN_OPR | Ref P3_L3_PRC; P754 MP-01 |
| P3_L2_COM_XGW01 | exclusiveGateway | Secondary crushing fitted? | P3_L2_COM_LN_MET | Configuration (crushing circuit) |
| P3_L2_COM_SP02 | subProcess (collapsed) | Secondary/Tertiary Crushing & Screening (3.1.2) [three-stage crushing circuits] | P3_L2_COM_LN_DCS | Ref P3_L3_SCR |
| P3_L2_COM_SP03 | subProcess (collapsed) | Grinding & Classification (3.1.3) | P3_L2_COM_LN_DCS | Ref P3_L3_GRD |
| P3_L2_COM_XGW02 | exclusiveGateway | Cyclone overflow P80 on target? | P3_L2_COM_LN_MET | |
| P3_L2_COM_T01 | task | Adjust mill throughput / cyclone apex / feed density | P3_L2_COM_LN_MET | |
| P3_L2_COM_EE01 | endEvent | Cyclone overflow at target P80 feeding flotation | P3_L2_COM_LN_DCS | |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P3_L2_COM_F01 | P3_L2_COM_SE | P3_L2_COM_SP01 | |
| P3_L2_COM_F02 | P3_L2_COM_SP01 | P3_L2_COM_XGW01 | |
| P3_L2_COM_F03 | P3_L2_COM_XGW01 | P3_L2_COM_SP02 | Yes — three-stage crushing circuit |
| P3_L2_COM_F04 | P3_L2_COM_XGW01 | P3_L2_COM_SP03 | Cu SABC — direct to grinding |
| P3_L2_COM_F05 | P3_L2_COM_SP02 | P3_L2_COM_SP03 | |
| P3_L2_COM_F06 | P3_L2_COM_SP03 | P3_L2_COM_XGW02 | |
| P3_L2_COM_F07 | P3_L2_COM_XGW02 | P3_L2_COM_EE01 | P80 on target |
| P3_L2_COM_F08 | P3_L2_COM_XGW02 | P3_L2_COM_T01 | P80 off target |
| P3_L2_COM_F09 | P3_L2_COM_T01 | P3_L2_COM_SP03 | Adjusted — retry |

---

## P3_L3_PRC — Primary Crushing (L3) | P3_L3_SCR — Secondary/Tertiary Crushing (L3) | P3_L3_GRD — Grinding (L3)

### P3_L3_PRC (Lanes: FMS/ROM LN_FMS | DCS LN_DCS | Operator LN_OPR)
| ID | Type | Name | Lane | P754 |
|----|------|------|------|------|
| P3_L3_PRC_SE | startEvent | Haul truck tip event; apron feeder active | LN_FMS | |
| P3_L3_PRC_T01 | serviceTask | Receive ROM Feed at Crusher; Record MP-01 Mass (3.1.1.1) | LN_DCS | P754 MP-01 CTP |
| P3_L3_PRC_T02 | task | Execute Primary Crushing; Monitor CSS and Power (3.1.1.2) | LN_DCS | |
| P3_L3_PRC_T03 | serviceTask | Transport via Discharge Conveyor; Record Belt Weigher (3.1.1.3) | LN_DCS | P754 cross-check |
| P3_L3_PRC_T04 | task | Manage Coarse Ore Stockpile Level (3.1.1.4) | LN_OPR | |
| P3_L3_PRC_XGW01 | exclusiveGateway | COS level below minimum? | LN_DCS | |
| P3_L3_PRC_T05 | task | Throttle SAG mill feed rate (DCS auto) | LN_DCS | |
| P3_L3_PRC_EE01 | endEvent | COS level stable; ore feeding to SAG/secondary crusher | LN_OPR | |

Flows: SE→T01→T02→T03→T04→XGW01 | XGW01→EE01[OK] | XGW01→T05[Low] | T05→T04[Loop]

### P3_L3_SCR — Secondary/Tertiary Crushing (three-stage crushing circuits; pebble crushing in SABC circuits)
Lanes: DCS LN_DCS | Operator LN_OPR
T01: Classify Ore by Screen (3.1.2.1) | T02: Execute Secondary/Tertiary Crushing (3.1.2.2)
XGW01: Oversize returned to crusher? [Yes→T02 loop] [No→T03]
T03: Execute Pebble Crushing [Cu SABC only] (3.1.2.3) — parallel if pebble crusher installed

### P3_L3_GRD — Grinding & Classification (Lanes: DCS LN_DCS | Operator LN_OPR | Metallurgist LN_MET)
| ID | Type | Name | Lane |
|----|------|------|------|
| P3_L3_GRD_SE | startEvent | COS reclaim feeding SAG / ball mill feed | LN_DCS |
| P3_L3_GRD_T01 | task | Operate SAG Mill — speed, bearing pressure, water (3.1.3.1) | LN_DCS |
| P3_L3_GRD_T02 | task | Operate Ball Mill — sump level, cyclone feed (3.1.3.2) | LN_DCS |
| P3_L3_GRD_T03 | task | Classify Slurry by Hydrocyclone (3.1.3.3) | LN_DCS |
| P3_L3_GRD_T04 | task | Add Grinding Media per Schedule (3.1.3.4) | LN_OPR |
| P3_L3_GRD_PGW01 | parallelGateway | [FORK] Media addition parallel to cyclone operation | LN_OPR |
| P3_L3_GRD_PGW02 | parallelGateway | [JOIN] | LN_DCS |
| P3_L3_GRD_EE01 | endEvent | Cyclone overflow at target P80 to flotation feed | LN_DCS |

Flows: SE→T01→T02→PGW01 | PGW01→T03[P1] | PGW01→T04[P2] | T03→PGW02 | T04→PGW02 | PGW02→EE01

---

## P3_L2_FLT — Concentration / Flotation (L2)

> **Revised 2026-10-23 (LL-005).** Flotation is two reusable patterns, not one diagram per commodity. The Flotation Circuit (3.2.2) runs once per configured target mineral or bulk concentrate; circuits chain through their tailings. Concentrate Separation (3.2.3) splits a bulk concentrate. Which instances a site runs is configuration (`flotation_circuit`), not a branch per site. The generated diagrams are in `pillar-models/bpmn/03-processing-and-beneficiation/` (built by `pillar-models/bpmn/tools/build_pillar3.py`).

### Pool & Lanes
| ID | Name |
|----|------|
| P3_L2_FLT_PL | Concentration (Flotation) |
| P3_L2_FLT_LN_OPS | Control Room Operator / DCS Auto-control / Metallurgist |

### Element Inventory
| ID | Type | Name | Lane | Notes |
|----|------|------|------|-------|
| P3_L2_FLT_SE | startEvent | Cyclone overflow at flotation feed | LN_OPS | |
| P3_L2_FLT_SP01 | subProcess (collapsed) | Reagent Management & Pulp Conditioning (3.2.1) | LN_OPS | Ref P3_L3_RGT; re-entered for each circuit |
| P3_L2_FLT_SP02 | subProcess (collapsed) | Flotation Circuit (3.2.2) | LN_OPS | Ref P3_L3_FLC; one instance per configured circuit |
| P3_L2_FLT_PGW01 | parallelGateway | [FORK] Concentrate and tailings leave the circuit | LN_OPS | |
| P3_L2_FLT_XGW01 | exclusiveGateway | Bulk concentrate to separate? | LN_OPS | Configuration |
| P3_L2_FLT_SP03 | subProcess (collapsed) | Concentrate Separation (3.2.3) | LN_OPS | Ref P3_L3_SEP |
| P3_L2_FLT_EE01 | endEvent | Saleable concentrates to dewatering | LN_OPS | |
| P3_L2_FLT_XGW02 | exclusiveGateway | Another target mineral in tailings? | LN_OPS | Configuration |
| P3_L2_FLT_EE02 | endEvent | Final tailings to tailings management | LN_OPS | |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P3_L2_FLT_F01 | SE | SP01 | |
| P3_L2_FLT_F02 | SP01 | SP02 | |
| P3_L2_FLT_F03 | SP02 | PGW01 | |
| P3_L2_FLT_F04 | PGW01 | XGW01 | Concentrate |
| P3_L2_FLT_F05 | PGW01 | XGW02 | Tailings |
| P3_L2_FLT_F06 | XGW01 | SP03 | Yes |
| P3_L2_FLT_F07 | XGW01 | EE01 | No (default) |
| P3_L2_FLT_F08 | SP03 | EE01 | |
| P3_L2_FLT_F09 | XGW02 | SP01 | Yes — loop: condition tailings for the next circuit |
| P3_L2_FLT_F10 | XGW02 | EE02 | No (default) |

---

## P3_L3_RGT — Reagent Management & Pulp Conditioning | P3_L3_FLC — Flotation Circuit | P3_L3_SEP — Concentrate Separation

### P3_L3_RGT (Lanes: Plant Chemist / Metallurgist LN_CHM | DCS LN_DCS)
T01: Manage Reagent Inventory and Preparation (3.2.1.1) | T02: Adjust Pulp pH (3.2.1.2)
XGW01: Activation or depression required? [Yes → T03: Activate or Depress Minerals for Target Circuit (3.2.1.3)]
T04: Dose Collector and Frother (3.2.1.4)

### P3_L3_FLC — Flotation Circuit [pattern] (Lanes: DCS, Metallurgist)
| ID | Type | Name | Lane | P754 |
|----|------|------|------|------|
| P3_L3_FLC_SE | startEvent | Conditioned circuit feed | LN_DCS | MP-01 (first circuit) or MP-07 (later circuits) |
| P3_L3_FLC_T01 | task | Operate Rougher Flotation (3.2.2.1) | LN_DCS | MP-02, MP-03 |
| P3_L3_FLC_XGW01 | exclusiveGateway | Rougher tail grade above threshold? | LN_DCS | Yes → raise collector dose or cut air rate (LN_MET) |
| P3_L3_FLC_T02 | task | Operate Scavenger Flotation (3.2.2.2) | LN_DCS | MP-04 circuit loss |
| P3_L3_FLC_XGW02 | exclusiveGateway | Scavenger tail grade above limit? | LN_DCS | Yes → investigate and escalate (LN_MET) |
| P3_L3_FLC_T03 | task | Operate Regrind Mill (3.2.2.3) [if installed] | LN_DCS | |
| P3_L3_FLC_T04 | task | Operate Cleaner Flotation (3.2.2.4) | LN_DCS | MP-05 (CTP when saleable) |
| P3_L3_FLC_XGW03 | exclusiveGateway | Concentrate grade below specification? | LN_DCS | Yes → adjust froth depth or cleaning (LN_MET) |
| P3_L3_FLC_EE01 | endEvent | Concentrate and tailings leave circuit | LN_DCS | |

### P3_L3_SEP — Concentrate Separation [pattern] (Lanes: DCS, Metallurgist)
T01: Condition Bulk Concentrate for Separation (3.2.3.1) MP-08 | T02: Operate Separation Rougher Flotation (3.2.3.2) → sink concentrate MP-10 (CTP)
T03: Operate Separation Cleaner Flotation (3.2.3.3) → float concentrate MP-09 (CTP) | XGW01: Float product below spec? [Yes → adjust depressant dose or cleaning]

---

## P3_L2_DWT — Dewatering & Product Handling (L2)

> **Revised 2026-10-26 (LL-012, LL-014).** Thickening is one pattern (3.3.1) used for every saleable concentrate, any bulk concentrate and the tailings; tailings handling moved to P3_L2_TSF; drying and packaging is 3.3.3. The generated diagrams in `pillar-models/bpmn/03-processing-and-beneficiation/` (built by `pillar-models/bpmn/tools/build_pillar3.py`) are the reference; the inventory below summarises them.

### Pool & Lanes: DCS / Control Room Operator LN_OPS

Flows: SE (Concentrate or tailings stream available) → SP01 Thickening (3.3.1) → XGW01 Tailings stream? [Yes → message end "Thickened tailings to 3.5"] [No → SP02 Concentrate Filtration (3.3.2) → XGW02 Drying or packaging required? [Yes → SP03 Concentrate Drying & Packaging (3.3.3)] → merge → EE01]

### P3_L3_THK — Thickening [pattern] (Lanes: Control Room Operator / Metallurgist, DCS)
T01 Feed Slurry to Thickener (3.3.1.1) → T02 Dose Flocculant (3.3.1.2) → PGW fork → [T04 Recover Thickener Overflow Water (3.3.1.4) WP-05] ‖ [XGW01 Underflow density below minimum? → T03 Pump Thickener Underflow (3.3.1.3)]

### P3_L3_FIL — Concentrate Filtration (Lanes: DCS, Plant Operator, Process Technician / Metallurgist)
T01 Operate Filter (3.3.2.1) → fork → [T04 Recover Filtrate Water (3.3.2.4) WP-06] ‖ [T02 Discharge Filter Cake (3.3.2.2) → T03 Verify Moisture Content (3.3.2.3) → XGW01 Moisture within specification? → transfer to shed → message end CTP-2; No → adjust and re-filter (loop to T01)]

### P3_L3_DRY — Concentrate Drying & Packaging (Lanes: DCS, Plant Operator)
XGW01 Drying specified? [Yes → T01 Dry Concentrate (3.3.3.1)] → merge → XGW02 Packed dispatch specified? [Yes → T02 Package and Weigh Concentrate (3.3.3.2) → message end to Logistics]

---

## P3_L2_MET — Metallurgical Accounting & Quality (L2)

### Pool & Lanes: Auto-samplers/Instruments LN_AUT | Laboratory LN_LAB | Metallurgist LN_MET | Chief Metallurgist LN_CHF | ERP/Systems LN_SYS

| ID | Type | Name | Lane |
|----|------|------|------|
| P3_L2_MET_SE | startEvent (timer) | Shift start; all auto-samplers active | P3_L2_MET_LN_AUT |
| P3_L2_MET_SP01 | subProcess (collapsed) | Sampling (3.4.1) | P3_L2_MET_LN_AUT | Ref P3_L3_SMP; continuous during shift |
| P3_L2_MET_SP02 | subProcess (collapsed) | Assay & Analysis (3.4.2) | P3_L2_MET_LN_LAB | Ref P3_L3_ASY |
| P3_L2_MET_SP03 | subProcess (collapsed) | Mass Balance & Reconciliation (3.4.3) | P3_L2_MET_LN_CHF | Ref P3_L3_MBA |
| P3_L2_MET_XGW01 | exclusiveGateway | QC batch accepted? | P3_L2_MET_LN_LAB | |
| P3_L2_MET_T01 | task | Issue Re-assay Instruction; Hold Batch | P3_L2_MET_LN_LAB | |
| P3_L2_MET_XGW02 | exclusiveGateway | Shift balance error within tolerance? | P3_L2_MET_LN_CHF | |
| P3_L2_MET_T02 | task | Investigate Discrepancy; Escalate to Chief Metallurgist | P3_L2_MET_LN_MET | |
| P3_L2_MET_EE01 | endEvent | Shift mass balance accepted; daily/monthly reconciliation feeds upstream | P3_L2_MET_LN_CHF | |

Flows: SE→SP01 [continuous] | SP01→SP02 [at shift end, composites submitted] | SP02→XGW01
XGW01→SP03[Pass] | XGW01→T01[Fail] | T01→SP02[Loop — re-assay] | SP03→XGW02
XGW02→EE01[Within tolerance] | XGW02→T02[Outside] | T02→EE01[Resolved or escalated]

### P3_L3_SMP through P3_L3_MBA (L3 elements)
**P3_L3_SMP** — Sampling: T01: Collect Auto-Sampler Increments (3.4.1.1) [continuous loop per interval]
T02: Collect Grab/Composite Samples (3.4.1.2) | T03: Prepare Samples in Lab (3.4.1.3) | Insert QC at preparation

**P3_L3_ASY** — Assay & Analysis: T01: Perform Lab Assay (3.4.2.1) [ICP/XRF/fire assay]
T02: Monitor OSA in real-time (3.4.2.2) [parallel continuous stream]
T03: Perform QA/QC — CRM, duplicate, blank (3.4.2.3) | XGW01: QC pass? [loop back if fail]

**P3_L3_MBA** — Mass Balance: T01: Close Shift Mass Balance (3.4.3.1) [shift end trigger]
T02: Daily/Weekly Reconciliation (3.4.3.2) | T03: Monthly Metal Accounting Report (3.4.3.3) [monthly trigger]
T04: Conduct Inventory Adjustment and Stocktake (3.4.3.4) [monthly/quarterly]
ICE01: Monthly period end intermediate timer event

---

## P3_L2_TSF — Tailings Management (L2) and P3_L2_WAT — Water Management (L2)

> **Added 2026-10-26 (LL-014).** Generic process areas; facility and water-system differences are configuration (`tailings_facility`, `water_system`). The generated diagrams in `pillar-models/bpmn/03-processing-and-beneficiation/` are the reference: `3.5_*` and `3.6_*`.

| Diagram ID | Pillar ID | Title | Key decisions |
|---|---|---|---|
| P3_L2_TSF | 3.5 | Tailings Management | Classification fitted? |
| P3_L3_TTD | 3.5.1 | Tailings Transport & Distribution | Line pressure or flow abnormal? |
| P3_L3_TCL | 3.5.2 | Tailings Classification [conditional] | Sand fit for construction? |
| P3_L3_TDP | 3.5.3 | Tailings Deposition | Beach width below minimum? |
| P3_L3_EMB | 3.5.4 | Embankment Construction | Placement meets specification? |
| P3_L3_FSM | 3.5.5 | Facility Storage & Safety Monitoring | Within operating criteria? |
| P3_L2_WAT | 3.6 | Water Management | — (supply, reclaim, seepage in parallel) |
| P3_L3_MWS | 3.6.1 | Makeup Water Supply | Treatment required?; Transfer volumes reconcile? |
| P3_L3_RCW | 3.6.2 | Reclaim Water | Pond above minimum intake level? |
| P3_L3_SPG | 3.6.3 | Seepage & Drainage Collection | Pond above pump-start level? |
| P3_L3_PWD | 3.6.4 | Process Water Supply & Distribution | Process water storage below minimum? |
| P3_L3_WBL | 3.6.5 | Site Water Balance & Reconciliation | Balance within tolerance? |
