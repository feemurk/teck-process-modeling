# Process Model Reference — mobile-fleet-data-training-mock
# Scoped entity extract from Teck Process Models.
# Generated: 2026-08-06
# Source pillar(s): 02-mining-operations-extraction
# Process areas in scope: 2.2 Load & Haul
# This file is the foundation for the BEAM workshop — read at workshop start.
# Do not modify manually — regenerate via `extract entities for [product-name]`.
#
# TRAINING MOCK — NOT A PRODUCTION ARTIFACT. Generated without live stakeholder
# engagement, per explicit instruction, to illustrate Stage 1 file shapes and the
# Curated/Contextualized DDVC boundary for a data-modeler training exercise. A real
# BEAM workshop with named participants must be run before this scope is used for
# an actual Stage 2 handoff.

---

## Product Scope

**Product name:** mobile-fleet-data-training-mock
**DDVC layer:** curated (see `beam-overlay.yaml` Section 7 for a flagged, non-standard
Contextualized KPI addendum built on top of this Curated scope, for training purposes only)
**Product purpose:** Canonical haul cycle, delay, and equipment time data supporting fleet
productivity and availability analysis at HVC. (Training mock — not a production artifact.)
**Sites in scope:** HVC, QB
**Primary site:** HVC

---

## Entity Summary

| Entity Name | Type | DDVC Layer | Grain | Source System(s) | Pillar Ref |
|-------------|------|------------|-------|-------------------|------------|
| `mobile_equipment` | Master | curated | One row per physical equipment unit (governed, deduplicated) | Governed master file (product team + site steward) — see §3.5 note below | §2.2 |
| `mobile_equipment_source_minestar` *(proposed — see Custom Entities)* | Source | curated | One row per equipment record as Minestar itself holds it, duplicates intact | Minestar | §2.2 |
| `mobile_equipment_source_wenco` *(proposed — see Custom Entities)* | Source | curated | One row per equipment record as Wenco itself holds it, duplicates intact | Wenco | §2.2 |
| `mobile_equipment_source_xref` *(proposed — see Custom Entities)* | Map | curated | One row per (master ID, source system, source ID) association, per validity window | Governed master file (product team + site steward) | §2.2 |
| `equipment_class` | Reference | curated | One row per equipment class definition | FMS fleet reference data | §2.2 |
| `operator` | Master | curated | One row per person per role | FMS (operator assignment module) | §2.2 |
| `location` | Reference | curated | One row per named destination node | FMS (location/destination master) | §2.2 |
| `shift` | Reference | curated | One row per shift instance per site | FMS (shift scheduling module) | §2.2 |
| `haul_cycle` | Transactional | curated | One row per truck trip, loading to return | FMS (Minestar dispatch module); PI Historian; strut pressure sensors | §2.2.2, §2.2.3 |
| `haul_cycle_stage_event` *(proposed — see Custom Entities)* | Transactional | curated | One row per lifecycle stage per haul cycle | FMS (state-transition event stream, if available) / derived from `haul_cycle` timestamps | §2.2.2, §2.2.3 |
| `delay_event` | Transactional | curated | One row per discrete delay occurrence per equipment unit | FMS (queue/delay tracking) | §2.2.2.1, §2.2.3.2, §2.3.3 |
| `operator_shift_assignment` | Transactional | curated | One row per operator per equipment per shift | FMS | §2.2 |
| `stockpile_inventory_movement` | Transactional | curated | One row per movement event | FMS (tonnes); survey system (volume); mine planning software | §2.2.4 |

---

## Entity Catalog (Full Extract)

### mobile_equipment

> *Extracted from 02-mining-operations-extraction.md Entity Catalog, then revised during
> this workshop per `standards/teck-vocabulary-master.md` §3.5 (Source System Mastering
> Gap). The standard pillar model lists `mobile_equipment`'s source as a single blended
> "FMS (Minestar, Wenco, Modular)" — but at HVC, Minestar and Wenco run concurrently
> against the same equipment concept with no MDM engine reconciling them, each holding
> duplicate rows all marked "active." Treating `mobile_equipment` as directly sourced from
> either system was wrong; it must be the governed output of a mastering process, with the
> two systems' raw views and the mapping between them modeled as their own entities — see
> `mobile_equipment_source_minestar`, `mobile_equipment_source_wenco`, and
> `mobile_equipment_source_xref` below, and the Custom Entities section.*

**Entity Type:** Master
**Business Definition:** A physical piece of self-propelled mining equipment identified by a unique fleet number, make, model, and payload/bucket capacity class. Persists across the life of the asset; flagged inactive on decommissioning. **Revised scope**: this is the single governed, deduplicated representation — one row per real-world equipment unit — produced by reconciling the per-system Source entities, not a direct extract from any one operational system.
**Grain:** One row per physical equipment unit (post-mastering — i.e. per real-world asset, not per source-system record)
**Key Attributes:** `equipment_master_id` (governed surrogate — see note below), `fleet_number`, `equipment_class`, `make`, `model`, `nominal_payload_t`, `equipment_status`
**Lifecycle / State Transitions:** Active → Standby → Decommissioned
**Key Relationships:** PERFORMS `haul_cycle`; ASSIGNED_TO `operator` per shift; CLASSIFIED under `equipment_class`; PRESENT AT `location`; RESOLVED FROM `mobile_equipment_source_minestar` and `mobile_equipment_source_wenco` VIA `mobile_equipment_source_xref` (one-to-many: one master row may map to one row in each contributing source system)
**Source System(s):** Governed master file, maintained jointly by the product team and the HVC site steward — **not** Minestar or Wenco directly (see note above). This file and process do not yet exist; this is a proposed governance pattern, not a confirmed one.
**Standard Alignment:** GMG TUM (equipment is the subject of all TUM time classification); GMG Mobile Equipment Open Data; ISA-95 Level 3
**DDVC Layer:** curated

---

### mobile_equipment_source_minestar *(proposed — see Custom Entities section)*

> *Not in the standard pillar model. Proposed during this workshop per
> `templates/entity-extraction.md` Step 4's guidance for sites running duplicate/overlapping
> source systems with no MDM engine — see `standards/teck-vocabulary-master.md` §3.5.*

**Entity Type:** Source
**Business Definition:** The equipment record exactly as Minestar itself holds it — including any duplicate rows for the same physical asset and Minestar's own `active` status flag — with no cross-system deduplication applied. Exists because operators still need Minestar-specific attributes for operational reporting that the governed `mobile_equipment` Master, by design, will not carry.
**Grain:** One row per equipment record as Minestar's own database holds it (may be more than one row per real-world asset if Minestar itself carries unresolved duplicates)
**Key Attributes:** `minestar_unit_id`, `minestar_status` (Minestar's own active/inactive flag — not to be confused with the Master's `equipment_status`), plus all Minestar-native equipment attributes
**Lifecycle / State Transitions:** Mirrors Minestar's own record lifecycle; not independently governed
**Key Relationships:** RESOLVED TO `mobile_equipment` VIA `mobile_equipment_source_xref`
**Source System(s):** Minestar
**Standard Alignment:** None — Teck-specific, exists only because no MDM engine reconciles Minestar and Wenco
**DDVC Layer:** curated

---

### mobile_equipment_source_wenco *(proposed — see Custom Entities section)*

> *Not in the standard pillar model. Proposed during this workshop, mirroring
> `mobile_equipment_source_minestar` above for Wenco.*

**Entity Type:** Source
**Business Definition:** The equipment record exactly as Wenco itself holds it — including any duplicate rows for the same physical asset and Wenco's own `active` status flag — with no cross-system deduplication applied.
**Grain:** One row per equipment record as Wenco's own database holds it (may be more than one row per real-world asset if Wenco itself carries unresolved duplicates)
**Key Attributes:** `wenco_unit_id`, `wenco_status` (Wenco's own active/inactive flag), plus all Wenco-native equipment attributes
**Lifecycle / State Transitions:** Mirrors Wenco's own record lifecycle; not independently governed
**Key Relationships:** RESOLVED TO `mobile_equipment` VIA `mobile_equipment_source_xref`
**Source System(s):** Wenco
**Standard Alignment:** None — Teck-specific, exists only because no MDM engine reconciles Minestar and Wenco
**DDVC Layer:** curated

---

### mobile_equipment_source_xref *(proposed — see Custom Entities section)*

> *Not in the standard pillar model. Proposed during this workshop per
> `templates/beam-workshop.md` §B.0's definition of the Map entity type — the crosswalk
> that makes it possible to join a Source row to the correct Master row for a given period,
> since which source row is "the" active one is a governed business decision, not something
> derivable automatically without an MDM engine.*

**Entity Type:** Map
**Business Definition:** The association between one governed `equipment_master_id` and one (source system, source-system equipment ID) pair, for a specific validity window. This is what lets a Curated product resolve "which Minestar or Wenco row is this master truck, right now" — a decision the site steward makes and that can change over time (e.g. if a duplicate is later found to actually belong to a different physical asset).
**Grain:** One row per (master ID, source system, source-system ID, validity window) association
**Key Attributes:** `xref_id`, `equipment_master_id` (FK to `mobile_equipment`), `source_system_name` (Minestar | Wenco), `source_system_equipment_id` (FK to `mobile_equipment_source_minestar.minestar_unit_id` or `mobile_equipment_source_wenco.wenco_unit_id`), `valid_from_utc`, `valid_to_utc`, `is_authoritative`, `decided_by`, `decision_rationale`
**Lifecycle / State Transitions:** Open (association active) → Closed (superseded by a later mapping decision, `valid_to_utc` set)
**Key Relationships:** MAPS `mobile_equipment` TO `mobile_equipment_source_minestar` and `mobile_equipment_source_wenco`
**Source System(s):** Governed master file, maintained jointly by the product team and the HVC site steward — the same governance artifact as `mobile_equipment` itself; this mapping is not derivable from either operational system automatically
**Standard Alignment:** None — Teck-specific, exists only because no MDM engine reconciles Minestar and Wenco
**DDVC Layer:** curated

---

### equipment_class

> *Extracted from 02-mining-operations-extraction.md Entity Catalog*

**Entity Type:** Reference
**Business Definition:** A classification grouping of mobile equipment by functional type, manufacturer family, and payload or bucket capacity tier (e.g., "Rigid Body Haul Truck — 220t class", "Rope Shovel — 55 m³ bucket"). Used for fleet planning, benchmarking, and performance normalisation.
**Grain:** One row per equipment class definition
**Key Attributes:** `class_id`, `functional_type`, `nominal_capacity`, `capacity_unit`, `typical_make_model`
**Lifecycle / State Transitions:** Static reference; versioned when capacity standards change
**Key Relationships:** CLASSIFIES `mobile_equipment`
**Source System(s):** FMS fleet reference data
**Standard Alignment:** GMG Mobile Equipment Open Data (equipment taxonomy)
**DDVC Layer:** curated

---

### operator

> *Extracted from 02-mining-operations-extraction.md Entity Catalog*

**Entity Type:** Master
**Business Definition:** A mine employee or contractor authorised to operate one or more categories of mobile equipment in the active mine. Operator identity is the party of record for all shift-level operating events.
**Grain:** One row per person per role
**Key Attributes:** `operator_id`, `operator_name`, `authorization_classes`, `employment_type`, `active_flag`
**Lifecycle / State Transitions:** Active → Inactive
**Key Relationships:** ASSIGNED_TO `mobile_equipment` per shift; RECORDS `delay_event`; EXECUTES `haul_cycle`
**Source System(s):** FMS (operator assignment module)
**Standard Alignment:** ISA-95 Level 3 (personnel resource)
**DDVC Layer:** curated

---

### location

> *Extracted from 02-mining-operations-extraction.md Entity Catalog*

**Entity Type:** Reference
**Business Definition:** A named, spatially-anchored destination point in the mine — primary crusher, ROM stockpile zone, waste dump bench, or fuel bay. Used as destination reference in FMS dispatch.
**Grain:** One row per named destination node
**Key Attributes:** `location_id`, `location_name`, `location_type` (crusher/stockpile/waste/fuel/maintenance), `coordinates_wgs84`, `active_flag`
**Lifecycle / State Transitions:** Active → Inactive (as mine design evolves)
**Key Relationships:** RECEIVES material from `haul_cycle`; ASSOCIATED WITH `stockpile_inventory`
**Source System(s):** FMS (location/destination master)
**Standard Alignment:** ISA-95 Level 3 (area/process cell in equipment hierarchy)
**DDVC Layer:** curated

---

### shift

> *Extracted from 02-mining-operations-extraction.md Entity Catalog*

**Entity Type:** Reference
**Business Definition:** A defined period of scheduled work, bounded by start and end timestamps, constituting the primary temporal reporting grain for mine operations. Shifts are the smallest independently schedulable unit of human and equipment time.
**Grain:** One row per shift instance per site
**Key Attributes:** `shift_id`, `shift_date`, `shift_type` (day/night), `shift_start_utc`, `shift_end_utc`, `site_id`
**Lifecycle / State Transitions:** Planned → Active → Closed → Reconciled
**Key Relationships:** CONTAINS `haul_cycle`, `delay_event`, `operator_assignment`, `blast_event`
**Source System(s):** FMS (shift scheduling module)
**Standard Alignment:** ISA-95 Level 3 (scheduling); GMG TUM (shift is the Calendar Time boundary for TUM calculation)
**DDVC Layer:** curated

---

### haul_cycle

> *Extracted from 02-mining-operations-extraction.md Entity Catalog, with two attributes
> added during this workshop (marked below) to close a gap identified during Section C —
> the standard model has no explicit timestamp for arrival at the dump queue or for
> reaching the dump spot, only a single `dump_utc`, which makes the queue-at-dump and
> spot-at-dump durations impossible to re-derive.*

**Entity Type:** Transactional
**Business Definition:** A single, complete sequence of loading, hauling, dumping, and returning empty for one haul truck. The fundamental unit of production measurement for Load & Haul. One haul cycle = one payload delivery event.
**Grain:** One row per truck trip from loading to return to shovel
**Key Attributes:** `cycle_id`, `truck_id`, `shovel_id`, `shift_id`, `material_type`, `payload_est_t`, `origin_polygon_id`, `destination_location_id`, `queue_shovel_start_utc`, `spot_shovel_utc`, `load_start_utc`, `load_end_utc`, `haul_start_utc`, **`queue_dump_start_utc` (added)**, **`spot_dump_utc` (added)**, `dump_utc`, `return_end_utc`, `cycle_duration_s`
**Lifecycle / State Transitions:** Initiated (load begin) → Loaded → In Transit → Dumped → Returned (closed)
**Key Relationships:** PERFORMED BY `mobile_equipment` (truck); LOADED BY `mobile_equipment` (shovel); ORIGINATES FROM `dig_polygon` (Pillar 1, cross-pillar); DELIVERS TO `location`; OCCURS WITHIN `shift`; PARENT OF `haul_cycle_stage_event` (one-to-many)
**Source System(s):** FMS (Minestar dispatch module); PI Historian (telemetry archive); strut pressure sensors
**Standard Alignment:** GMG TUM (time components map to TUM categories); GMG Mobile Equipment Open Data
**DDVC Layer:** curated

---

### haul_cycle_stage_event *(proposed — see Custom Entities section)*

> *Not in the standard pillar model. Proposed during this workshop to make every
> lifecycle-stage duration on `haul_cycle` auditable from explicit start/end boundaries
> rather than a single derived duration column.*

**Entity Type:** Transactional
**Business Definition:** A single lifecycle-stage occurrence within one haul cycle — queue at shovel, spot at shovel, load, haul, queue at dump, spot at dump, dump, or empty return — bounded by an explicit start and end timestamp, so the duration of any stage is re-derivable and auditable rather than stored only as a pre-computed number.
**Grain:** One row per lifecycle stage per haul cycle (up to 8 rows per `haul_cycle`)
**Key Attributes:** `stage_event_id`, `haul_cycle_id` (FK), `stage_type` (queue_shovel | spot_shovel | load | haul | queue_dump | spot_dump | dump | empty_return), `start_ts`, `end_ts`, `duration_s` (computed: `end_ts − start_ts`), `equipment_id`, `tum_category`
**Lifecycle / State Transitions:** Open (start recorded) → Closed (end recorded)
**Key Relationships:** CHILD OF `haul_cycle` (many-to-one via `haul_cycle_id`); ASSOCIATED WITH `mobile_equipment`; each row's `tum_category` corresponds to the TUM state that stage represents (e.g. `queue_shovel` → OD or SBO, `load` → PT/WT, `haul` → WT)
**Source System(s):** FMS state-transition event stream if the source system emits one; otherwise derived by rule from `haul_cycle`'s own timestamp columns (see `beam-overlay.yaml` `event_canvas` for the derivation rule and an open item on which path is actually true at HVC — this needs live confirmation)
**Standard Alignment:** GMG TUM (each stage maps directly to a TUM category — this entity is the auditable evidence trail behind `haul_cycle`'s and `delay_event`'s TUM classifications)
**DDVC Layer:** curated

---

### delay_event

> *Extracted from 02-mining-operations-extraction.md Entity Catalog*

**Entity Type:** Transactional
**Business Definition:** A recorded interruption or deviation from productive operation for a piece of mobile equipment, classified against the GMG TUM taxonomy. Every non-productive state transition generates a delay_event record. Primary entity for fleet availability and utilisation analysis.
**Grain:** One row per discrete delay occurrence per equipment unit
**Key Attributes:** `delay_id`, `equipment_id`, `shift_id`, `delay_start_utc`, `delay_end_utc`, `duration_s`, `tum_category` (CT/ST/AT/OT/WT/PT/NP/OD/SBO/DT/UT/SBE), `tum_category_l2`, `delay_reason_code`, `delay_description`, `recorded_by`
**Lifecycle / State Transitions:** Active (delay in progress) → Closed (equipment returns to productive state)
**Key Relationships:** ASSOCIATED WITH `mobile_equipment`; OCCURS WITHIN `shift`; MAY BE LINKED TO `haul_cycle`; SHOULD BE LINKED TO `work_order` (Pillar 5, cross-pillar) when `tum_category = DT` — see Cross-Pillar Dependencies below
**Source System(s):** FMS (queue/delay tracking)
**Standard Alignment:** GMG TUM (mandatory) — every delay_event MUST carry a TUM category. Sub-categories required (OD vs. SBO is the critical distinction)
**DDVC Layer:** curated

---

### operator_shift_assignment

> *Extracted from 02-mining-operations-extraction.md Entity Catalog*

**Entity Type:** Transactional
**Business Definition:** The assignment of a specific operator to a specific piece of equipment for the duration of a shift. Party-of-record for all haul cycles, delay events, and operating time records within that shift for that equipment unit.
**Grain:** One row per operator per equipment per shift
**Key Attributes:** `assignment_id`, `operator_id`, `equipment_id`, `shift_id`, `assignment_start_utc`, `assignment_end_utc`, `assignment_status`
**Lifecycle / State Transitions:** Planned → Active → Closed
**Key Relationships:** LINKS `operator` to `mobile_equipment` for a `shift`
**Source System(s):** FMS
**Standard Alignment:** ISA-95 Level 3; GMG TUM
**DDVC Layer:** curated

---

### stockpile_inventory_movement

> *Extracted from 02-mining-operations-extraction.md Entity Catalog*

**Entity Type:** Transactional
**Business Definition:** An incremental change to a stockpile zone's inventory — either an addition (haul cycle dump) or a drawdown (reclaim). Running sum of movements constitutes current stockpile inventory state.
**Grain:** One row per movement event
**Key Attributes:** `movement_id`, `stockpile_zone_id`, `movement_type` (addition/drawdown), `movement_timestamp_utc`, `mass_t`, `grade_cu_pct`, `grade_zn_pct`, `source_polygon_id`, `equipment_id`, `shift_id`
**Lifecycle / State Transitions:** Single atomic event
**Key Relationships:** MODIFIES `stockpile_inventory`; LINKED TO `haul_cycle` (additions) or reclaim record (drawdowns)
**Source System(s):** FMS (tonnes); survey system (volume); mine planning software
**Standard Alignment:** AMIRA P754 Principle 5 (custody transfer measurement)
**DDVC Layer:** curated

---

## Process Flow Context

*Extracted from 02-mining-operations-extraction.md Process Flow Narratives — 2.2 Load & Haul*

**Pool**: Load & Haul | **Lanes**: Mine Controller / FMS, Shovel Operator, Dozer Operator, Truck Operator

**Start Event**: Shift start — roster active; dig face assignment from FMS; muck pile classified and available.

**[PARALLEL FORK]** — Multiple haul trucks and shovel(s) operate concurrently. The following describes one truck's repeating haul cycle. Multiple instances execute in parallel across the active fleet.

1. **Assign Equipment to Shift** (Mine Controller + FMS) — operator-equipment assignments loaded; shift plan active.
2. **Tram Shovel to Dig Face** (Shovel Operator + FMS) — **TUM: NP** during tram.
3. **Clean and Dress Dig Face** (Dozer Operator) — grades approach ramp and floor; **TUM: WT** for dozer.
4. **Dispatch Truck to Face** (FMS Auto-dispatch or Mine Controller) — truck receives face assignment on cab display; en route.
5. **Queue Truck at Shovel** (Truck Operator) — arrives at face; enters queue if shovel occupied.
   - *[GATEWAY — Queue duration vs. OD threshold?]* → Below threshold: **TUM: OD**. Threshold exceeded + management decision: **TUM: SBO** — mine controller must explicitly classify.
6. **Spot Truck at Shovel** (Truck Operator + Shovel Operator) — manoeuvres to loading position; **TUM: NP**.
7. **Load Truck** (Shovel Operator) — successive bucket passes; strut pressure telemetry confirms accumulation; **TUM: PT** for shovel, **TUM: WT** for truck.
8. **Verify Payload and Issue Dispatch** (FMS) — payload estimated from strut pressures; destination issued; haul_cycle record initiated.
   - *[GATEWAY — Payload within tolerance?]* → Overloaded: shovel operator removes partial pass (or continues with flag). Underloaded: FMS flags for review.
9. **Execute Loaded Haul** (Truck Operator + FMS tracks) — truck travels to destination; **TUM: WT**.
   - *[INTERMEDIATE EVENT — Breakdown during haul?]* → Truck stops; mine controller classifies **TUM: DT**; haul_cycle suspended.
10. **Queue at Destination** (Truck Operator) — arrives; queues if access blocked.
    - *[GATEWAY — Queue classification?]* → **TUM: OD** (inherent brief wait) or **TUM: SBO** (management decision — crusher shutdown, access congestion).
11. **Spot Truck at Dump** (Truck Operator) — manoeuvre to dump position; safety berm confirmed; **TUM: NP**.
12. **Dump Load** (Truck Operator) — hydraulic dump; strut pressure drop confirms empty; dump event timestamp and haul_cycle dump record written to FMS; **TUM: WT** (dumping is productive function).
13. **Execute Empty Return** (Truck Operator + FMS) — truck body lowered; new dispatch assignment received; travels empty; **TUM: NP**.
    - *[INTERMEDIATE EVENT — Operational delay en route?]* → Fuelling, operator change, short wait → **TUM: OD**.

**[LOOP BACK]** — Empty return completes one haul_cycle record. Loop repeats until: shift end; fuel/service interval; face exhausted; equipment breakdown.

**[PARALLEL JOIN]** — At shift end, mine controller reconciles all open haul_cycle records; shift-level production committed to FMS.

**End Event**: Shift end — all open haul_cycle records closed; shift production total committed to FMS database.

---

## SIPOC Reference

*Extracted from 02-mining-operations-extraction.md SIPOC Artifacts — SIPOC 2.2 Load & Haul*

| Element | Content |
|---------|---------|
| **Suppliers** | Drill & Blast (2.1) — classified muck pile with material designation and destination assignment; Mine Planning (1.4) — shift roster, fleet assignment, production targets; Mine Services (2.3) — maintained haul roads and dewatered pit; Maintenance (out of scope as domain) — serviceable equipment fleet |
| **Inputs** | Fragmented, classified muck pile (ore/waste/marginal by zone); haul trucks (operational, fuelled, assigned operators); rope shovel or hydraulic excavator (operational, face-assigned); FMS dispatch instructions; haul road network (maintained, accessible); destination locations (crusher open, stockpile zones designated, waste dump bench prepared) |
| **Process** | Execute the repeating haul cycle: prepare face → load trucks from shovel → haul to destination → dump → return empty. Track all equipment time against GMG TUM categories. Deliver classified material tonnage to primary crusher, ROM stockpile, or waste dump per plan. |
| **Outputs** | Tonnes delivered to destination by material type, per shift, per truck; haul cycle records (truck ID, shovel ID, material type, estimated payload, origin zone, destination, cycle time components, all timestamps in UTC); delay event records (TUM-classified); equipment time utilisation records (by asset, by shift); ROM stockpile inventory update (mass and grade increments) |
| **Customers** | Processing & Beneficiation (Pillar 3) — ROM ore tonnes delivered to crusher/stockpile; Mine Planning (1.4.4) — production actuals vs. plan; Metallurgical Accounting — ore tonnes and estimated grade delivered; MFD data product (primary consumer of all haul truck, shovel, and delay_event records) |

---

## Cross-Pillar Dependencies

Entities referenced but not owned by this product:

| Entity | Owned By | Relationship |
|--------|----------|--------------|
| `dig_polygon` | Pillar 1 (Mine Planning & Scheduling) | `haul_cycle.origin_polygon_id` — FK reference, not modeled here |
| `work_order` | Pillar 5 (Maintenance & Reliability) | `delay_event` with `tum_category = DT` should carry a `work_order_id` FK to the corrective work order that addressed the failure. Per the programme Gap Register (Gap XP-01), this linkage is not currently enforced in FMS and is the single most critical cross-pillar gap for downtime analytics — without it, DT events show *that* equipment was down but not *why*. Carried into `beam-overlay.yaml` as an open item. |
| `blast_pattern` / `material_classification` | Pillar 2, process area 2.1 (Drill & Blast) | `haul_cycle.material_type` and destination assignment originate from 2.1's material classification gate — referenced, not owned, by this Load & Haul product |

---

## Custom Entities (Teck-Specific)

*Entities not in the industry-standard process model, proposed during this workshop.*

| Entity Name | Entity Type | Description | Reason Not in Standard Model |
|-------------|-------------|--------------|-------------------------------|
| `haul_cycle_stage_event` | Transactional | One row per lifecycle stage per haul cycle (queue-shovel, spot-shovel, load, haul, queue-dump, spot-dump, dump, empty-return), each with explicit start/end timestamps and a `duration_s` computed from them, FK'd to the parent `haul_cycle`. | The standard pillar model carries stage timing only as timestamp *columns* on `haul_cycle` itself (and is missing two of them — see the `haul_cycle` entity note above). Decomposing into discrete, auditable stage-event rows was requested explicitly during this workshop so every duration is traceable to an explicit start/end boundary rather than a single opaque number, and so each stage's TUM category can be assigned and audited independently. Whether the source system (FMS) actually emits a discrete event per stage, or whether this entity must be *derived* by rule from `haul_cycle`'s own timestamp columns, is an open item requiring live confirmation with the FMS system owner. |
| `mobile_equipment_source_minestar` | Source | Minestar's own, un-reconciled equipment record — duplicates and Minestar-native status flags intact. | The standard pillar model treats `mobile_equipment` as if a single "FMS" system were the source. At HVC, Minestar and Wenco run concurrently against the same equipment concept with no MDM engine, and operators need Minestar-specific attributes for operational reporting that the governed Master will not carry. Per `templates/beam-workshop.md` §B.0 and `standards/teck-vocabulary-master.md` §3.5. |
| `mobile_equipment_source_wenco` | Source | Wenco's own, un-reconciled equipment record — duplicates and Wenco-native status flags intact. | Mirrors `mobile_equipment_source_minestar` for Wenco. Same rationale. |
| `mobile_equipment_source_xref` | Map | Crosswalk associating one governed `equipment_master_id` with one (source system, source-system ID) pair, per validity window. | Required wherever Master records are hand-governed rather than produced by an MDM engine — which source row is "the" active one for a given master is a business decision the site steward makes, and that decision itself needs to be tracked and can change over time. Per `templates/beam-workshop.md` §B.0 and `standards/teck-vocabulary-master.md` §3.5. |
