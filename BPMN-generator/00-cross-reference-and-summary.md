# 00: Cross-Reference and Summary — Open-Pit Mining Value Chain

---

## Overview

This document synthesises the six process model pillars into a unified value chain view. It provides the artefacts required for programme-level navigation: the value chain diagram, master entity cross-reference (entities spanning multiple pillars), the five custody transfer points with AMIRA P754 relevance, the standard alignment matrix, ISA-95 level distribution, and the consolidated programme-wide gap register. It is the entry point for BEAM facilitators, data product designers, and the Collibra metamodel team working across pillar boundaries.

All six pillars are in scope:

| # | Pillar | Domain | Primary ISA-95 Levels |
|---|--------|--------|-----------------------|
| 1 | Mine Planning & Scheduling | Strategic and operational planning | 3-4 |
| 2 | Mining Operations (Extraction) | Physical extraction — drill, blast, load, haul | 0-3 |
| 3 | Processing & Beneficiation | Comminution, flotation, dewatering, metallurgical accounting | 0-3 |
| 4 | Logistics & Outbound Supply Chain | Concentrate handling, transport, port, commercial documentation | 0-4 |
| 5 | Maintenance & Reliability | Asset availability, PM/CM execution, reliability engineering | 0-4 |
| 6 | Health & Safety | Hazard control, permit to work, incident management, occupational health | 0-4 |

---

## Value Chain Overview Diagram

```
╔═══════════════════════════════════════════════════════════════════════════════════════════╗
║                    TECK RESOURCES — OPEN-PIT MINING VALUE CHAIN                          ║
║                    Data-Driven Value Chain (DDVC): Capture → Curate → Contextualize      ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  PILLAR 6: HEALTH & SAFETY  (cross-cutting governance layer — gates all five pillars)   │
│  Hazard ID & Risk Control | Permit to Work | Incident Management | OH Monitoring        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
           │ PTW gates P5 work orders    │ Risk controls gate all activities
           │ Incident data consumes      │ all pillars' operational records
           ▼                             ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│  PILLAR 5: MAINTENANCE   │   │  PILLAR 1: MINE PLANNING  │
│  & RELIABILITY           │◄──│  & SCHEDULING             │
│                          │   │                          │
│  PM / CM Execution       │   │  LOM → Medium-Term →     │
│  Reliability Engineering │   │  Short-Term → Dispatch   │
│  Asset Life Management   │   │                          │
│                          │   │  Block Model ★            │
│  work_order ★            │   │  dig_polygon ★           │
│  equipment_failure_rec.  │   │  period_plan ★           │
│  fmeca_record            │   │  shift_production_report ★│
└─────────────┬────────────┘   └────────────┬─────────────┘
              │ TUM:DT links                │ Planned downtime
              │ work_order_id               │ windows constrain
              │ ← delay_event              │ fleet allocation
              ▼                             ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  PILLAR 2: MINING OPERATIONS (EXTRACTION)                                               │
│                                                                                         │
│  2.1 Drill & Blast ──────────────────► 2.2 Load & Haul ──────────────► 2.3 Mine Svcs  │
│      blast_pattern                         haul_cycle ★                    slope_mon.   │
│      drill_hole                            delay_event ★ (TUM)             dewatering   │
│      blast_event                           stockpile_inventory_movement     pump_tel.    │
│      grade_control_sample                                                               │
│      material_classification                                                             │
│                            ▼ Internal CTP: Mine-to-ROM Stockpile                       │
│                    mobile_equipment ★  |  operator_shift_assignment ★  |  shift ★      │
└──────────────────────────────────────────┬──────────────────────────────────────────────┘
                                           │ ROM ore tonnes + grade
                                           │ CTP-1: Mine to Concentrator
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  PILLAR 3: PROCESSING & BENEFICIATION                                                   │
│                                                                                         │
│  3.1 Comminution → 3.2 Flotation (Cu/Zn/Pb circuits) → 3.3 Dewatering → 3.4 Met Acctg│
│      process_node ★         concentrate_production_rec.     filter cake        shift_   │
│      mill_telemetry         osa_grade_telemetry              concentrate_type ★  mass_  │
│      amira_meas.point ★     commercial_sample_record ★       tsf_inventory       balance│
│                             assay_result                     port receipt ►             │
│                                           │                                             │
│           ◄── P754: MP-01 through MP-06 (Cu) / MP-07 through MP-11 (Zn) / MP-12–15 Pb│
└──────────────────────────────────────────┬──────────────────────────────────────────────┘
                                           │ Filter cake + LIMS batch record
                                           │ CTP-2: Concentrator to Logistics
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  PILLAR 4: LOGISTICS & OUTBOUND SUPPLY CHAIN                                            │
│                                                                                         │
│  4.1 Conc. Handling → 4.2 Inland Transport → 4.3 Port Operations → 4.4 Commercial Docs │
│      conc_shed_zone          weighbridge_tx ★     vessel_loading_rec.   certificate_of_ │
│      conc_inventory_rec.     bill_of_lading ★     draft_survey_rec. ★   analysis ★      │
│      dispatch_lot_rec. ★     transport_dispatch   commercial_sample     commercial_     │
│                              transit_loss_rec.    port_inventory_rec.   invoice ★       │
│                                                                                         │
│  CTP-3: Site-to-Transport    CTP-4: Transport-     CTP-5: Port-to-Vessel               │
│  (site weighbridge)          to-Port (port         (final draft survey)                │
│                              weighbridge)          ← REVENUE RECOGNITION                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

★ = Cross-pillar entity (appears in entity cross-reference below)

KEY INTERFACES:
  Pillar 1 ─────► Pillar 2: dig_polygon, destination_assignment, daily_targets (FMS upload)
  Pillar 2 ─────► Pillar 1: shift_production_report (actuals vs. plan reconciliation)
  Pillar 2 ─────► Pillar 3: ROM ore tonnes + estimated grade to crusher/stockpile
  Pillar 3 ─────► Pillar 4: filter cake + LIMS batch record (shed receipt belt weigher)
  Pillar 4 ─────► Pillar 3: CoA (commercial grade) for mine-to-vessel grade reconciliation
  Pillar 4 ─────► Pillar 1: concentrate production forecast for smelter contracting
  Pillar 5 ◄────► Pillar 2: work_order_id ↔ delay_event (TUM:DT) bidirectional link
  Pillar 5 ─────► Pillar 1: planned_downtime_windows constrain fleet allocation
  Pillar 5 ─────► Pillars 3,4: instrument calibration certificates → P754 Principle 8
  Pillar 6 ─────► Pillar 5: PTW is a gate condition for maintenance work order execution
  Pillar 6 ◄────► All: incident investigations consume operational data from all pillars
```

---

## Master Entity Cross-Reference

Entities appearing in more than one pillar. For each shared entity: which pillar owns the definition (primary steward), which pillars consume or extend it, and what the cross-pillar dependency is.

| Entity Name | Primary Steward | Consuming Pillars | Cross-Pillar Dependency | Collibra Design Note |
|-------------|----------------|-------------------|------------------------|----------------------|
| `mobile_equipment` | Pillar 2 (FMS is source of truth for operational state) | Pillars 1 (fleet allocation), 5 (maintenance work orders, equipment_failure_record), 6 (incident_record — equipment involved) | Single curated master entity. EAM (Pillar 5 SAP PM) and FMS (Pillar 2) both hold equipment records — reconciliation required. `equipment_id` must be a canonical key shared across FMS, EAM, and any other system referencing the asset. | Single Collibra Business Asset for each physical equipment unit. Attribute ownership split: operational state (Pillar 2/FMS), maintenance attributes (Pillar 5/EAM), criticality class (Pillar 5 Reliability Engineering). |
| `equipment_class` | Pillar 2 (FMS/GMG Mobile Equipment Open Data taxonomy) | Pillars 1 (fleet sizing — productivity parameters per class), 5 (FMECA, PM task library, criticality assessment per class) | Equipment class is the denominator for fleet sizing (Pillar 1), the grouping for reliability analysis (Pillar 5 MTBF/MTTR), and the normalisation unit for TUM analytics (Pillar 2). Must be consistent across all three pillars. | Single Reference Data asset in Collibra. Changes to equipment class definitions require review across Pillars 1, 2, and 5. |
| `dig_polygon` | Pillar 1 (Mine Planning — design authority) | Pillar 2 (FMS destination assignment, haul cycle origin tracking, grade control sampling) | Designed in Pillar 1, uploaded to FMS for Pillar 2 execution. Grade control results (Pillar 2, 2.1.5.2) may trigger a destination revision that updates the Pillar 1-owned record. Version history of the polygon (original design vs. grade-control-revised destination) must be preserved. | Own as a master data asset in Pillar 1. Pillar 2 consumes a read-only version. Destination revisions are recorded as events against the parent polygon, not as replacement records. |
| `shift` | Pillar 1 (Mine Planning — shift schedule authority) | Pillars 2 (haul_cycle, delay_event), 3 (shift_mass_balance, concentrate_production_record), 5 (work_order — shift during which maintenance occurred) | The shift is the primary temporal reporting grain across three pillars. The `shift_id` must be consistent across FMS (Pillar 2), the metallurgical accounting system (Pillar 3), and the EAM (Pillar 5). Shift boundary timestamps (shift_start_utc, shift_end_utc) are the canonical time boundaries for all shift-level aggregations. | Single Reference Data asset. Shift calendar published by Pillar 1 (Mine Planning) and consumed by all downstream pillars. Time zone handling for UTC conversion is a hard rule (DR-06 alignment). |
| `operator` | Pillar 1 (HR/Roster — employment authority) | Pillar 2 (operator_shift_assignment — party of record for haul cycles and delay events), Pillar 6 (incident_record — persons involved; exposure_monitoring_record — worker identity) | Operator identity is the party-of-record for TUM time classification in Pillar 2 and for safety event attribution in Pillar 6. The canonical operator identifier must be consistent across: roster system (HR), FMS login (Pillar 2), safety management system (Pillar 6), and EAM (Pillar 5 — tradesperson on work order). | Human Resource master data. `operator_id` is the canonical key. Privacy considerations apply for Pillar 6 health monitoring records — health data requires appropriate access controls. |
| `location` | Pillar 2 (FMS destination reference — operational authority) | Pillars 1 (material destination assignment), 4 (port_facility, weighbridge location), 5 (maintenance bay location) | Location/destination reference data spans from in-pit locations (crusher, stockpile zones, waste dumps) to port facilities. The `location` entity in Pillar 2 and the `port_facility` entity in Pillar 4 are related but distinct — both must be part of the same spatial hierarchy in Collibra (site → area → process cell → unit). | Location hierarchy must accommodate: in-pit (Pillar 2 FMS), plant (Pillar 3 process nodes), logistics (Pillar 4 shed zones, port facilities), and maintenance (Pillar 5 functional locations). ISA-95 equipment hierarchy provides the standard structure. |
| `block_model` | Pillar 1 (Resource Geology / Mine Planning — design and release authority) | Pillar 2 (grade prediction for material classification; dig polygon design reference), Pillar 3 (mill feed grade forecast for blend planning) | The block model is the single most consequential shared data asset. Its version governance is a programme-level decision: which version is current for (a) FMS operational use, (b) mine planning, and (c) regulatory reserve reporting. These three use cases may require different versions simultaneously. | Two release types required: operational release (for FMS and grade control) and reserve-quality release (QP-signed, immutable after regulatory filing). Both must be managed in Collibra as versioned assets with different access controls and release workflow requirements. |
| `geological_drill_hole` (resource) vs. `drill_hole` (grade control) | Pillar 1 (Resource Geology) / Pillar 2 (Grade Control Geologist) | Cross-referenced in block model interpolation (Pillar 1) and material classification (Pillar 2) | Resource drill holes and grade control drill holes are structurally the same entity type but governed by different processes, quality standards, and uses. They must be related entities (both are drill holes) but cannot be conflated — different sampling standards, different QA/QC requirements, different spatial density. | Define a `drill_hole` parent entity type in Collibra with two specialisations: `resource_drill_hole` (Pillar 1 — QP-governed, JORC/NI 43-101 compliant) and `grade_control_drill_hole` (Pillar 2 — operational, internal grade control standard). The relationship between the two (spatial proximity, grade correlation) is a Contextualized product concern. |
| `delay_event` | Pillar 2 (FMS — source of truth for equipment state transitions) | Pillar 5 (linked via work_order_id to explain cause of TUM:DT events), Pillar 6 (incidents may cause or result from delay events — slope alert, blast exclusion zone) | The `delay_event` entity is the intersection of three pillars. Its GMG TUM category is a Pillar 2 data governance responsibility. Its work_order_id linkage is a Pillar 5 integration requirement. Its safety-related subset (geotechnical exclusion, blast exclusion) carries a Pillar 6 risk_register_record reference. | The `delay_event` entity definition in Collibra must carry three optional foreign keys: TUM category (mandatory), work_order_id (mandatory for DT events — not optional), and hazard_category_id from Pillar 6 (optional — for safety-driven stoppages). All three must be populated before the MFD Contextualized product can decompose downtime by cause. |
| `process_node` | Pillar 3 (Plant Engineering / Process Control — design authority) | Pillar 5 (physical equipment registered in EAM as functional location, maintenance work orders generated against process nodes) | The Pillar 3 `process_node` (SAG mill, flotation cell bank, thickener) and the Pillar 5 EAM functional location (the same physical equipment in SAP PM) must be reconciled to a single canonical identity. Currently the PI Historian tag name, the SAP PM functional location code, and the plant engineering drawing number are three separate identifiers for the same equipment — none of which is the Collibra canonical ID. | Collibra must define the canonical equipment ID for fixed plant assets. The mapping table (PI Historian tag → SAP PM functional location → plant engineering drawing) is a Collibra glossary responsibility, not a source system responsibility. |
| `concentrate_type` | Pillar 3 (Metallurgist / Commercial — product specification authority) | Pillar 4 (classify concentrate_inventory_record, dispatch_lot_record, certificate_of_analysis, commercial_invoice) | The `concentrate_type` reference entity defines the commercial specification (grade, moisture, penalty elements) that governs both the Pillar 3 production record and the Pillar 4 commercial document. A change to the smelter contract (new payability factors, revised penalty thresholds) updates the `smelter_contract` (Pillar 4) and should trigger a review of the `concentrate_type` specification. | Versioned reference entity. Smelter contract annual renewal is the primary trigger for `concentrate_type` specification revision. Version history must be preserved for historical invoice recalculation. |
| `amira_measurement_point` | Pillar 3 (Metallurgical Accounting / Process Engineering — P754 compliance authority) | Pillar 4 (weighbridge_transaction and shiploader_belt_weigher_telemetry are P754 measurement points), Pillar 5 (instrument calibration work orders reference P754 measurement point IDs) | The AMIRA P754 measurement point register spans Pillars 3, 4, and 5. Every measurement instrument used in the mine-to-vessel mass balance must have a P754 measurement point designation, a calibration status (Pillar 5 work order), and appear in the mass balance model (Pillar 3). | Single Collibra asset type for `amira_measurement_point`. Attributes from all three pillars feed this record: measurement method (Pillar 3), calibration certificate reference (Pillar 5), custody transfer flag (Pillars 3 and 4), commercial invoice reference (Pillar 4). |
| `work_order` | Pillar 5 (Maintenance — EAM/SAP PM authority) | Pillar 2 (delay_event carries work_order_id for DT classification), Pillar 6 (permit_to_work references work_order_id for maintenance PTWs; incident_record references work_order_id for maintenance-related injuries) | The `work_order` is the central Pillar 5 entity and a key reference in Pillars 2 and 6. The work_order_id must be surfaced in the FMS cab display (so mine controllers can enter it when classifying TUM:DT events) and in the PTW system (so permits are linked to the specific work order they authorise). | Single Collibra Business Term for `work_order`. Data lineage must show: work_order_id → delay_event (Pillar 2), work_order_id → permit_to_work (Pillar 6), work_order_id → equipment_failure_record (Pillar 5). All three are first-class data lineage relationships. |
| `permit_to_work` | Pillar 6 (Health & Safety — PTW system authority) | Pillar 5 (maintenance work orders gate on active PTW; PTW cancellation gates work order closure), Pillar 2 (blast authorisation and geotechnical exclusion zone management are PTW-class controls) | The PTW is a safety gate across Pillars 2, 5, and 6. The `permit_id` must appear in the `work_order` record (Pillar 5) as a mandatory prerequisite field, and in the blast event record (Pillar 2) where applicable. | The permit_to_work entity in Collibra must carry bidirectional links to `work_order` (Pillar 5) and optionally to `blast_event` (Pillar 2). The PTW status lifecycle (Active, Cancelled) must be visible to Pillar 5 work order closure workflow. |

---

## Custody Transfer Point Summary

All points in the value chain where material custody changes hands — either commercially or between internal accounting domains. Ranked by commercial significance.

| CTP # | Description | From | To | Measurement Method | Key Entities | AMIRA P754 | Commercial Significance |
|-------|-------------|------|----|--------------------|-------------|-----------|------------------------|
| **CTP-5** | **Port to Vessel — Final Draft Survey** | Teck Logistics | Buyer | Six-point vessel draft survey (hydrostatic calculation): final displacement − initial displacement − constants = cargo tonnes | `draft_survey_record` (initial + final); `vessel_loading_record`; `bill_of_lading` (final) | **Principles 1, 5, 8, 9 — all applicable**. This is the definitive commercial mass. Belt weigher is a cross-check only and does not override draft survey. P754 Principle 8: surveyor credentials and instrument calibration are mandatory documentation. | **Highest.** Revenue recognition, title transfer, commercial invoice basis. Disputes at this CTP require arbitration under charterparty. Errors directly impact reported revenue. |
| **CTP-4** | **Transport to Port — Port Weighbridge** | Transport Carrier | Teck Port Inventory | Certified static weighbridge (gross − tare = net wet tonnes per vehicle) at port | `weighbridge_transaction` (port receipt); `transit_loss_record`; `port_inventory_record` | Principles 1, 5, 8, 9. Port weighbridge calibration certificate is a mandatory P754 documentation requirement. Transit loss calculation (port tonnes − site BoL tonnes) is a P754 Principle 7 verification check. | **High.** Determines transit loss (carrier liability). Establishes opening port inventory — the denominator of the port-to-vessel mass balance. |
| **CTP-3** | **Site to Transport — Site Weighbridge** | Teck Site Inventory | Transport Carrier / BoL | Certified static weighbridge (gross − tare = net wet tonnes per vehicle load) at mine site | `weighbridge_transaction` (site — tare and gross); `bill_of_lading` (site dispatch) | Principles 1, 3, 5, 8, 9. Site weighbridge calibration is a Pillar 5 statutory maintenance obligation that must reference the P754 measurement point ID. P754 Principle 3: BoL is the documented accountability record. | **High.** BoL quantity is the legal transport document. Site-to-transport BoL vs. port receipt is the transit loss calculation basis. Subject to carrier dispute. |
| **CTP-2** | **Concentrator to Logistics — Filter Cake to Shed** | Teck Processing (Pillar 3) | Teck Logistics (Pillar 4) | Belt weigher on shed feed conveyor (continuous 1-min integration); LIMS batch record (grade, moisture from filter cake discharge) | `concentrate_inventory_record` (receipt event); belt weigher telemetry (PI Historian); LIMS batch record | Principles 5, 9. Mass measurement at this internal CTP is the opening entry of the site-side concentrate inventory ledger. P754 Principle 9: check-in from Processing to Logistics. Shed belt weigher calibration is a Pillar 5 obligation. | **Medium (internal).** Defines the concentrate inventory starting point. Discrepancy between filter production records (Pillar 3) and shed receipt records (Pillar 4) is the Concentrator-to-Shed mass balance closure metric — a key metallurgical accounting KPI. |
| **CTP-1** | **Mine to Concentrator — ROM Ore Delivery** | Teck Mining (Pillar 2) | Teck Processing (Pillar 3) | Sum of haul truck payload estimates (FMS strut pressure) per shift; supplemented by ROM stockpile drone surveys (periodic) and primary crusher belt weigher (continuous) | `stockpile_inventory_movement` (additions); `haul_cycle` (payload estimates); `process_measurement_point` MP-01 (crusher feed belt weigher) | Principles 1, 5, 7. Haul truck payload estimation from strut pressure is a recognised measurement uncertainty — mass is estimated, not certified-weighed. Crusher belt weigher provides the first accurate mass measurement. The difference between strut-estimated delivery and crusher belt weigher intake is a measure of payload estimation bias. | **Medium (internal).** Defines the mine-side ore production record. The mine-to-mill reconciliation (plan grade and tonnes vs. actual crusher intake) is a key strategic performance metric used to calibrate the block model. |

### Internal Material Accounting Boundaries (Not CTPs but Mass Balance Closure Points)

| Boundary | From | To | Measurement Basis | Pillar Reference |
|---------|------|-----|-------------------|-----------------|
| Crusher feed to cyclone overflow | Primary crusher intake | SAG/ball mill circuit product | MP-01 (belt weigher — continuous) | Pillar 3, 3.1 |
| Cyclone overflow to final concentrate | Mill circuit product | Flotation concentrate per commodity | MP-05/11/15 (on-stream XRF + shift composite assay) | Pillar 3, 3.2 |
| Flotation concentrate to tailings | Feed mass | Concentrate mass + tailings mass | Full plant mass balance (P754 shift closure) | Pillar 3, 3.4 |
| Port receipt to vessel loading | Port inventory opening | Draft survey commercial tonnes | Port weighbridge (opening) + draft survey (closing) | Pillar 4, 4.3 |

---

## Standard Alignment Matrix

Full matrix of all six pillars against all applicable standards. Primary = governing standard for that pillar. Secondary = reference standard applicable to specific activities. (-) = not applicable.

| Standard | Pillar 1 Planning | Pillar 2 Operations | Pillar 3 Processing | Pillar 4 Logistics | Pillar 5 Maintenance | Pillar 6 H&S |
|----------|------------------|---------------------|--------------------|--------------------|---------------------|--------------|
| **ISA-95 (IEC 62264)** | Primary (Levels 3-4) | Primary (Levels 0-3) | Primary (Levels 0-3) | Secondary (Levels 3-4) | Secondary (Levels 0-4) | Secondary (Level 3) |
| **AMIRA P754** | Secondary (Principle 2 — mine plan is P754 plan-side reference) | Secondary (Principles 1, 5, 6 — grade control sampling; ROM stockpile CTP) | **Primary — All 10 Principles** | Primary (Principles 1, 3, 5, 8, 9 — CTPs 3, 4, 5) | Secondary (Principle 8 — instrument calibration for P754 measurement points) | — |
| **GMG Time Usage Model (TUM)** | Secondary (planned downtime windows define TUM:DT boundaries) | **Primary — ALL delay events and equipment states** | — | — | Primary (TUM:DT is the Pillar 5 downtime measure — work orders open and close TUM:DT periods) | Secondary (safety-driven stoppages are TUM:OD or SBO — blast exclusion, slope alert) |
| **GMG Mobile Equipment Open Data** | — | **Primary (Pillar 2 all L2 process areas)** | — | — | Secondary (equipment telemetry data elements — condition monitoring) | — |
| **GMG Open Mining Format (OMF v2)** | **Primary (block model, geological domain, spatial data exchange)** | Secondary (dig polygon, blast pattern spatial coordinates) | — | — | — | — |
| **BPMN 2.0** | All L2 process areas — complete | All L2 process areas — complete | All L2 process areas — complete | All L2 process areas — complete | Representative flows — complete | Representative flows — complete |
| **ISO 14224** | — | Secondary (failure mode taxonomy applicable to mobile equipment failures recorded in delay_event) | — | — | **Primary — ALL process areas** | — |
| **ISO 55000 / 55001** | Secondary (LOM capital planning, fleet replacement) | — | — | — | **Primary (asset management system — planning, execution, lifecycle)** | — |
| **SAE JA1011 / JA1012** | — | — | — | — | **Primary (RCM criteria — FMECA, task selection, on-condition task justification)** | — |
| **ISO 45001:2018** | — | — | — | — | Secondary (maintenance safety — PTW gate) | **Primary — ALL process areas** |
| **ICMM H&S Framework** | — | Secondary (fatal hazard controls for vehicle interaction, explosives) | Secondary (fatal hazard controls for confined space, chemicals) | Secondary (fatal hazard controls for vessel loading, dust) | Secondary (maintenance safety — LOTO) | **Primary — ALL process areas** |
| **NI 43-101 / JORC / SEC S-K 1300** | **Primary (mineral reserve disclosure — block model and LOM schedule)** | — | — | — | — | — |
| **IMDG (Dangerous Goods)** | — | — | — | Primary (concentrate transport — marine pollutant classification) | — | Secondary (dangerous goods transport — driver documents) |
| **ISO 31000 (Risk Management)** | — | — | — | — | Secondary (criticality assessment) | Primary (risk assessment methodology for HAZID/HIRA) |

---

## ISA-95 Level Distribution

How the six pillars distribute across the ISA-95 functional hierarchy. The distribution reveals programme architecture: the bottom two rows (Levels 0-1) are dominated by Pillar 2 and Pillar 3; the top two rows (Levels 3-4) are dominated by Pillar 1 and Pillar 4. Pillars 5 and 6 span the full range.

```
ISA-95 Level   │ P1 Planning │ P2 Operations │ P3 Processing │ P4 Logistics │ P5 Maintenance │ P6 H&S
───────────────┼─────────────┼───────────────┼───────────────┼──────────────┼────────────────┼──────────
Level 4        │ ████████████│               │               │ ██████████   │ ████           │ ████████
Business/ERP   │ (dominant)  │               │ (met. acctg)  │ (commercial) │ (asset life)   │ (reg. rpt)
───────────────┼─────────────┼───────────────┼───────────────┼──────────────┼────────────────┼──────────
Level 3        │ ████████    │ ████████      │ ████████████  │ ██████████   │ ████████████   │ ████████
Operations Mgt │ (sched.)    │ (dispatch,    │ (LIMS, met.   │ (ERP, port   │ (dominant —    │ (dominant
               │             │  reporting)   │  acctg, QA)   │  mgmt, BoL)  │  EAM, CMMS)    │ PTW, IMS)
───────────────┼─────────────┼───────────────┼───────────────┼──────────────┼────────────────┼──────────
Level 2        │             │ ████████████  │ ████████████  │ ██ (weigh-   │ ████ (cond.    │ ██ (gas
Monitoring /   │             │ (FMS, GPS,    │ (DCS, SCADA,  │  bridge,     │  monitoring    │  detect.)
Control        │             │  Control)     │  OSA, alarms) │  shiploader) │  DCS alerts)   │
───────────────┼─────────────┼───────────────┼───────────────┼──────────────┼────────────────┼──────────
Level 1        │             │ ████████████  │ ████████████  │ ██ (weigh-   │ ████ (vibr.    │ ████
Sensing /      │ (survey GPS │ (dominant —   │ (dominant —   │  bridge      │  temp, current │ (dust, noise
Manipulation   │  as input)  │  MWD, strut,  │  belt wghrs,  │  scale,      │  sensors)      │  dosimeters,
               │             │  GPS)         │  density,pH)  │  belt sampl) │                │  XRF)
───────────────┼─────────────┼───────────────┼───────────────┼──────────────┼────────────────┼──────────
Level 0        │             │ ████████████  │ ████████████  │ ██ (filter   │ ████████████   │ ████
Physical       │             │ (rock, trucks │ (ore, slurry, │  cake, shed  │ (physical       │ (physical
Process        │             │  shovels)     │  concentrate, │  FEL)        │  repair, PM)   │ exposure,
               │             │               │  tailings)    │              │                │ inspection)
```

**Key observations:**
- **Pillar 1 is the only pillar with no Level 0-1 activity** — it is a pure IT/model domain
- **Pillars 2 and 3 are the dominant Level 0-1 data generators** — the highest-velocity raw data in the programme
- **Pillar 4's Level 0-2 touchpoints are all measurement instruments** (weighbridge, belt weigher, belt sampler) — not process control
- **Pillars 5 and 6 span the full range** — from physical inspection/repair (Level 0) to regulatory reporting (Level 4)
- **The DDVC Capture layer** maps to ISA-95 Levels 0-2 (raw sensor and control data)
- **The DDVC Curate layer** maps to ISA-95 Level 3 (operations management systems — FMS, EAM, LIMS, metallurgical accounting)
- **The DDVC Contextualize layer** maps to ISA-95 Level 4 (business analytics, KPIs, commercial documents)

---

## Cross-Pillar Process: Mine-to-Mill-to-Vessel Reconciliation

The reconciliation feedback loop is the most strategically important cross-pillar process in the programme. It spans Pillars 1, 2, 3, and 4, and its data quality depends on Pillars 5 and 6 maintaining instrument calibration and preventing safety incidents from corrupting production data. This process is not decomposed to L4 in any individual pillar because it belongs to no single pillar — it is the connective tissue of the DDVC architecture.

```
MINE-TO-MILL RECONCILIATION (monthly/quarterly)
─────────────────────────────────────────────────
Pillar 1 Block Model Grade Prediction
  → for each dig polygon: predicted tonnes × predicted grade
  [comparison]
Pillar 2 Grade Control Assay Result
  → for each blast pattern: actual tonnes × actual grade (from grade_control_sample)
  [comparison]
Pillar 3 Crusher Feed Belt Weigher (MP-01) + Head Grade Assay
  → actual crusher intake tonnes × actual head grade

RECONCILIATION QUESTION: Why does the block model prediction differ from grade control?
ANSWER: Geological model estimation error, blast dilution, ore loss, material misclassification
ACTION: Block model recalibration (Pillar 1, 1.1.2) — the reconciliation loop closes here.

MILL-TO-VESSEL RECONCILIATION (per shipment lot)
──────────────────────────────────────────────────
Pillar 3 shift_mass_balance (plant-side):
  → metal produced per period (dry tonnes × grade from shift composite assay)
  [comparison]
Pillar 4 commercial_invoice (vessel-side):
  → metal shipped per vessel (draft survey dry tonnes × CoA grade from umpire assay)

RECONCILIATION QUESTION: Why does plant production differ from vessel commercial tonnes?
ANSWER: Inventory change (shed and port stockpile), moisture variation, sampling and
        measurement differences (shift composite assay vs. umpire belt sample assay)
ACTION: Metallurgical accounting monthly close (Pillar 3, 3.4.3.3) — reconcile and explain.
```

This reconciliation loop requires the following entities to be accessible and joinable in the Contextualized layer:
- `shift_mass_balance` (Pillar 3) — plant production by period
- `vessel_loading_record` and `commercial_invoice` (Pillar 4) — shipped tonnes and commercial grade
- `concentrate_inventory_record` (Pillars 3 and 4) — opening and closing inventory at shed and port
- `block_model` grade predictions by dig polygon (Pillar 1)
- `grade_control_sample` results by blast pattern (Pillar 2)
- `shift_production_report` ore tonnes by area (Pillars 1 and 2)

---

## Programme-Wide Gap Register

Consolidated from all six pillars. Ranked by cross-pillar impact — gaps affecting multiple pillars or blocking multiple data products are listed first.

| Priority | Gap ID | Gap Description | Pillars Affected | Resolution Path |
|----------|--------|-----------------|-----------------|-----------------|
| **P1** | XP-01 | **work_order_id → delay_event linkage not enforced** — FMS mine controllers classify TUM:DT without entering a work order number. Without this linkage, downtime analytics cannot explain why equipment was down (failure mode, component, repair type). The MFD Contextualized product is fundamentally limited without it. | Pillars 2, 5 | BEAM workshop Pillar 2+5 joint session must produce a decision on enforcement mechanism: (a) FMS prompt at DT classification; (b) EAM notification to FMS on work order open/close; (c) time-window join in curated product (lowest quality, acceptable only as transitional). Decision needed before MFD data product contract is authored. |
| **P1** | XP-02 | **TUM OD vs. SBO classification is under-governed** — the distinction (brief inherent delay vs. management decision to not operate) is the most analytically significant TUM classification distinction but the most commonly collapsed. No site-standard decision table exists. If left to individual mine controller judgment, the data is not comparable across shifts, sites, or time periods. | Pillars 2, 5, 6 | BEAM workshop Pillar 2 session must produce a decision table: observable conditions → TUM category mapping. This table must be implemented as a business rule layer in FMS or as a mandatory classification workflow, not left as an unguided mine controller judgment. |
| **P1** | XP-03 | **Block model version governance across multiple use cases** — the block model is released for operational use (FMS, grade control) and for reserve reporting (QP-signed, regulatory disclosure). These two release types may require different versions simultaneously, and current practice at most mining companies does not formally separate them. | Pillars 1, 2 | Data product contract for `block_model` must define two release workflows: operational release (mine planning engineer authority) and reserve-quality release (QP/CP authority, immutable after regulatory filing). Collibra must support both release types as distinct lifecycle states on the same asset. |
| **P1** | XP-04 | **PI Historian as a cross-pillar data asset with no governance** — PI Historian (OSIsoft/AVEVA) archives telemetry data for Pillars 2, 3, and 5. It is the physical data repository for condition monitoring (Pillar 5), equipment telemetry (Pillar 2), and process measurement (Pillar 3). But PI Historian has no Collibra presence, no tag dictionary governance, no canonical tag naming convention, and no data quality monitoring. The DDVC Raw layer's integrity depends on PI Historian's data quality, which is currently ungoverned. | Pillars 2, 3, 5 | PI Historian tag governance is a prerequisite for all Raw layer data products. Define a PI Historian tag dictionary in Collibra (tag name → sensor description → process node → pillar → measurement units → AMIRA P754 measurement point reference where applicable). Tag naming convention must be standardised. Decommissioned tags must be marked inactive, not deleted. |
| **P2** | XP-05 | **Metallurgical accounting software system not specified** — the curated `shift_mass_balance` and `metallurgical_accounting_report` entities are designed as canonical curated products independent of the vendor system. But in practice, the metallurgical accounting system (vendor TBD — Interlaken, Metsim, or custom Excel-based) already performs these calculations. The relationship between the curated data product and the metallurgical accounting system must be resolved: does the data product replace it, consume its output, or co-exist? | Pillar 3 | Stakeholder decision required before BEAM workshop Pillar 3 — Chief Metallurgist and programme sponsor must agree on whether the curated `shift_mass_balance` entity is an input to the existing metallurgical accounting system or a replacement for it. |
| **P2** | XP-06 | **Antamina slurry pipeline transport mode** — the `transport_dispatch_record` and `weighbridge_transaction` entity designs assume road or rail transport. Antamina uses a slurry pipeline from the mine to Huarmey port. The pipeline replaces the weighbridge tare/gross cycle with pipeline mass flow measurement (magnetic flowmeter + density gauge). A pipeline transport variant of these entities is required. | Pillars 3, 4 | Define `pipeline_transport_record` as a site-specific entity variant for Antamina. Flag as an Antamina-specific extension in Collibra — not part of the canonical entity design, but a valid specialisation. |
| **P2** | XP-07 | **Red Dog Arctic accounting cadence** — Red Dog's concentrate is stockpiled for up to 9 months before shipping. Monthly reconciliation of inventory and shipped metal is not applicable; the accounting period is the shipping season (annual). The `commercial_invoice`, `metallurgical_accounting_report`, and `concentrate_inventory_record` entities need a `settlement_period_type` attribute to accommodate this. | Pillars 3, 4 | Flag in commercial/metallurgical accounting system configuration as a site-specific parameter. The `concentrate_inventory_record` for Red Dog must support multi-month open inventory positions without triggering false balance errors in the monthly reconciliation process. |
| **P2** | XP-08 | **AMIRA P754 instrument calibration cross-reference** — all P754 measurement points (MP-01 through MP-15 in Pillar 3 plus CTPs 3-5 in Pillar 4) require current calibration certificates for the instruments that generate their measurements. These calibration records are Pillar 5 maintenance work orders (statutory inspection category). The linkage between the `amira_measurement_point` entity (Pillar 3) and the calibration work order in SAP PM (Pillar 5) must be implemented. | Pillars 3, 4, 5 | The `amira_measurement_point` entity must carry a `calibration_work_order_ref` attribute populated from SAP PM. This requires a system integration: SAP PM statutory inspection work order completion must update the calibration currency status in the Collibra `amira_measurement_point` record. |
| **P3** | XP-09 | **Processing plant equipment in SAP PM** — Pillar 3 fixed plant equipment (mills, cells, conveyors, thickeners, filters) must be registered in SAP PM as functional locations to generate PM work orders (Pillar 5). Many mining operations have a gap here — mobile equipment is well-tracked in EAM, fixed plant is managed informally or in a standalone CMMS. If fixed plant is not in SAP PM, Pillar 5 Reliability Engineering cannot perform MTBF/MTTR analysis on processing plant equipment. | Pillars 3, 5 | Confirm with Teck maintenance team at each site whether fixed plant equipment is registered in SAP PM. If not, establish a migration plan. The `process_node` (Pillar 3) to SAP PM functional location mapping is a prerequisite. |
| **P3** | XP-10 | **PTW system type (digital vs. paper) at each site** — the `permit_to_work` entity assumes digital PTW. Paper-based PTW at any site means no real-time data and retrospective data entry only. The safety data completeness and timeliness depends on resolving this. | Pillar 6 | Audit PTW system type at each site as the first step of BEAM workshop Pillar 6 data audit. Paper PTW at any site should trigger an evaluation of whether digital PTW deployment is feasible and cost-effective within the programme timeline. |
| **P3** | XP-11 | **Contractor safety data inclusion** — LTIFR/TRIFR denominators must include contractor hours worked to be comparable with ICMM industry benchmarking. If contractor incident records are not in Teck's safety management system, or if contractor hours worked are not tracked, the programme-level safety KPIs will be systematically understated. | Pillar 6 | Confirm with corporate HSE whether contractor incidents are included in the site safety management system and whether contractor hours worked are tracked in the workforce management system or time-sheeting system. |
| **P4** | XP-12 | **Grade control sample TAT temporal gap** — material is often loaded from a blast pattern before the grade control assay returns from the laboratory (TAT 8-24 hours for fire assay). Haul cycles during this window carry a model-predicted material classification, not an assay-confirmed one. The `haul_cycle` and `material_classification` entities need a `classification_source` flag (assay-confirmed vs. model-predicted) so the Contextualized product can quantify the proportion of production that was classified under uncertainty. | Pillar 2 | Add `classification_source` attribute to `material_classification` entity: values = `assay_confirmed` / `model_predicted` / `expert_judgement`. This flag must be resolved at shift close — any `model_predicted` classifications for which assay results subsequently returned must be updated (or a correction record created) for the shift production report to be accurate. |

---

## Collibra Metamodel — Priority Decisions

The following entity design decisions have cross-pillar implications and must be resolved by the Collibra architect before individual pillar data products can be designed.

| Decision | Options | Recommended | Rationale |
|---|---|---|---|
| **Drill hole entity hierarchy** — resource vs. grade control | (a) Single entity type with a `drill_hole_purpose` attribute; (b) Two separate entity types sharing a parent | (b) Two specialisations of a parent `drill_hole` type | Sampling standards, QA/QC requirements, and data governance obligations differ fundamentally between resource (QP-governed, JORC/NI 43-101) and grade control (operational, internal standard). Conflating them in a single entity creates inappropriate governance. |
| **Equipment identity** — FMS vs. EAM canonical key | (a) FMS fleet number is canonical; (b) SAP PM equipment number is canonical; (c) New canonical ID independent of both | (c) New canonical ID in Collibra, with mappings to both FMS fleet number and SAP PM equipment number | Neither FMS nor SAP PM has full coverage of all equipment types. A Collibra-managed canonical equipment ID prevents either system from becoming the de facto master by default, which is a governance risk. |
| **Location hierarchy** — in-pit, plant, logistics, port | (a) Single `location` entity with a type attribute; (b) Separate entity types per location class | (a) Single `location` entity with `location_type` classification and ISA-95 level tag | The ISA-95 equipment hierarchy (Enterprise → Site → Area → Process Cell → Unit) provides a standard framework that accommodates all location types. Single entity with typed attributes is simpler to govern and query. |
| **TUM OD vs. SBO** — data model or business rule | (a) Separate TUM category codes in the entity; (b) Single `tum_category` with an `override_basis` attribute | (a) Separate codes (OD and SBO are distinct TUM categories per the standard) | OD and SBO have different analytical implications (OD = inherent operational inefficiency; SBO = fleet sizing excess or management decision). Conflating them defeats the purpose of the TUM. The distinction must be preserved in the data model, with a business rule layer enforcing correct classification. |
| **Shift mass balance vs. metallurgical accounting system** — data product scope | (a) Curated `shift_mass_balance` entity replaces the metallurgical accounting system; (b) Curated entity consumes output from the metallurgical accounting system | (b) Consume output — at programme maturity level 1.5-2, replacing the metallurgical accounting system is premature | The metallurgical accounting system holds site-specific business rules, historical data, and operator familiarity. Replacing it is a separate project. The curated `shift_mass_balance` should be populated from the metallurgical accounting system's output, with lineage documented in Collibra. Revisit at maturity level 3+. |

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total pillars | 6 |
| Total L2 Process Areas | 24 |
| Total L4 activities (approximate) | ~185 |
| Total entities defined (master, reference, transactional, time-series) | ~95 |
| Cross-pillar shared entities | 14 |
| AMIRA P754 Measurement Points (Cu/Zn/Pb circuits) | 15 (MP-01 through MP-15) |
| Custody transfer points (commercial) | 3 (CTPs 3, 4, 5) |
| Custody transfer points (internal) | 2 (CTPs 1, 2) |
| Programme-wide gaps registered | 12 |
| Governing standards (primary or secondary across any pillar) | 14 |
| Commodity variants documented | Cu porphyry, Cu-Zn polymetallic, Zn-Pb Arctic |
| Teck sites in scope | QB, HVC, Antamina (22.5%), CdA, Red Dog |

---

*End of 00: Cross-Reference and Summary. Produced per Open-Pit Mining Value Chain Process Model Development Specification v1.0 (extended to six pillars).*
