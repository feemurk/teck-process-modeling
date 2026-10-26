# Teck Vocabulary Master
# standards/teck-vocabulary-master.md
#
# Living register of Teck-specific terminology overlays on the industry-standard
# process models. Maintained collaboratively across workshop sessions.
#
# Claude Code: read this file at the start of every BEAM workshop session.
# When a workshop surfaces a new term or a conflict with an existing entry,
# add it to the vocabulary_additions section of beam-overlay.yaml.
# Apply confirmed additions here via `apply learning` after triage review.
#
# SECTIONS:
#   1. Source System Name Canonicalisation
#   2. Site-Specific Vocabulary
#   3. Business Concept Registry (where Teck usage differs from industry standard)
#   4. Abbreviations and Acronyms
#
# ENTRY STATUS:
#   confirmed   — verified with named authority, safe to use in overlays and models
#   provisional — in use but not yet formally verified
#   deprecated  — no longer in use; retained for historical overlay compatibility

---

## 1. SOURCE SYSTEM NAME CANONICALISATION

Canonical system names as used in process models and overlay files,
with their Teck-internal names and site-specific variants.

| Canonical Name (Process Model) | Teck Internal Name(s) | Sites | Status |
|-------------------------------|----------------------|-------|--------|
| PI Historian | ParcView HVC, Capstone Historian, PI Historian, Wonderware | All | confirmed |
| FMS (Fleet Management System) | Minestar, Wenco, Modular/Dispatch | HVC=Minestar, QB=TBC, RED_DOG=TBC | provisional |
| LIMS | Assay HVC, LIMS | HVC confirmed; others TBC | provisional |
| ERP | SAP, JDE | All | confirmed |
| EAM / CMMS | SAP PM | All | provisional |
| Mine Planning Software | Deswik, MinePlan | Site-specific; confirm per product | provisional |
| Blast Design Software | SHOTPlus, BlastLogic | Site-specific | provisional |
| Drill Guidance System | Thunderbird, AMT, Aquila | Site-specific | provisional |
| Geological Modeling Software | Leapfrog, Vulcan, GEMS | Site-specific | provisional |

> Claude Code: when a workshop participant names a source system, check this table.
> If the name is not in the Teck Internal Name column, add it as a vocabulary_addition
> in the overlay and flag for confirmation.

---

## 2. SITE-SPECIFIC VOCABULARY

Terms, codes, or naming conventions that differ meaningfully by site.
Populated progressively as workshops are completed.

### 2.1 Shift Definitions

| Site | Day Shift | Night Shift | Third Shift | UTC Offset | Notes |
|------|-----------|-------------|-------------|------------|-------|
| HVC | 06:00–18:00 local | 18:00–06:00 local | None | UTC-8 (UTC-7 DST) | Confirm DST handling |
| QB | TBC | TBC | TBC | UTC-4 | No DST in Chile |
| ANTAMINA | TBC | TBC | TBC | UTC-5 | No DST in Peru |
| CDA | TBC | TBC | TBC | UTC-4 | No DST in Chile |
| RED_DOG | TBC | TBC | TBC | UTC-9 (UTC-8 DST) | Seasonal ops — confirm |

> Claude Code: always ask about shift boundary and timezone in Section D (Site Variants)
> for any product that includes the `shift` entity. Do not assume UTC-8 for HVC.

### 2.2 Equipment Classification (TBC — populate per workshop)

| Canonical Class (Process Model) | HVC Term | QB Term | RED_DOG Term | Notes |
|---------------------------------|----------|---------|--------------|-------|
| Rigid Body Haul Truck — 220t class | TBC | TBC | TBC | |
| Rope Shovel — 55m3 bucket | TBC | TBC | N/A (hydraulic excavators) | Red Dog uses hydraulic excavators |
| Hydraulic Excavator | TBC | TBC | TBC | |
| Motor Grader | TBC | TBC | TBC | |
| Water Truck | TBC | TBC | TBC | |

### 2.3 Location Naming (TBC — populate per workshop)

| Canonical Concept | HVC | QB | RED_DOG | Notes |
|-------------------|-----|-----|---------|-------|
| Pit | TBC | TBC | TBC | |
| Bench | TBC | TBC | TBC | |
| Shovel Face | TBC | TBC | TBC | |
| ROM Stockpile | TBC | TBC | TBC | |
| Waste Dump | TBC | TBC | TBC | |

---

## 3. BUSINESS CONCEPT REGISTRY

Where Teck's usage of a term differs from the industry-standard definition
in the process models. These differences drive `process_model_overrides` in overlays.

### 3.1 Payload

| Concept | Industry Standard (Process Model) | Teck Usage | Sites | Impact |
|---------|-----------------------------------|------------|-------|--------|
| Payload measurement source | Strut pressure sensors → estimated payload | HVC: strut pressure confirmed; others TBC | HVC confirmed | Payload is estimated, not certified. UOM = _wmt (estimated). Calibration model per equipment class. |
| Payload unit | Wet metric tonnes | Wet metric tonnes | All | No deviation |

### 3.2 GMG TUM Classification

| TUM Category | Standard Definition | Teck Usage Notes | Classification Authority |
|-------------|-------------------|-----------------|-------------------------|
| Operating Delay (OD) | Brief inherent interruption — queue at face, fuelling, short blast wait | In use at HVC; definition alignment with standard TBC at other sites | Mine Controller |
| Operating Standby (SBO) | Management decision not to operate — excess fleet, face unavailable | Critical: must be distinguished from OD. Not automatically classified by FMS. Requires mine controller decision. | Mine Controller (explicit decision) |
| Downtime (DT) | Equipment not available — breakdown, PM, tire change | Work order link to FMS delay record: not yet implemented at HVC — Gap XP-01 from cross-reference | Mine Controller + Maintenance |

> Claude Code: in any workshop involving delay_event entities, always probe the
> OD vs. SBO distinction explicitly using the coaching language in Section C.3
> of beam-workshop.md. Never accept an answer that conflates the two.

### 3.3 Grade Control (TBC — populate at Pillar 2 workshops)

| Concept | Industry Standard | Teck HVC Usage | Teck Red Dog Usage | Notes |
|---------|------------------|----------------|-------------------|-------|
| Cut-off grade | Parameter calculated from price deck and costs | TBC | TBC | COG changes with price deck |
| Grade control sample TAT | 8-24 hours for fire assay | TBC | TBC | |
| Material classification basis | Assay-confirmed vs. model-predicted | TBC | TBC | Classification_source flag needed |

### 3.4 Concentrate / Mill (TBC — populate at Pillar 3 workshops)

| Concept | Industry Standard | Teck Usage | Notes |
|---------|------------------|------------|-------|
| Payload unit for concentrate | Wet metric tonnes (WMT) / Dry metric tonnes (DMT) | TBC — moisture correction at which layer? | |
| P80 | Standard particle size distribution metric | TBC — does Teck use different fragmentation targets by site? | |

### 3.5 Process Patterns and Configuration (LL-005)

Process groups are site- and mineral-agnostic. Use these terms for the reusable patterns
and for what varies between sites. Do not name a process group after a mineral or a site.

| Term | Definition | Do not confuse with | Status |
|------|-----------|---------------------|--------|
| Process pattern | A process group whose L4 steps are reused unchanged wherever the business process recurs (e.g., Flotation Circuit, Concentrate Separation) | A site's circuit, which is an instance of a pattern | confirmed |
| Configuration | Which optional process groups a site runs, how many pattern instances, in what order, and their reagent scheme, equipment and product specification. Held as data and in the overlay | A process deviation (`process_model_overrides`), which is a change to the steps themselves | confirmed |
| Flotation Circuit (3.2.2) | Pattern: rougher, scavenger, regrind (optional), cleaner flotation recovering one target mineral or a bulk concentrate from a feed | "Copper / zinc / lead circuit" — these are instances, written 3.2.2 [Cu] | confirmed |
| Concentrate Separation (3.2.3) | Pattern: splitting a bulk concentrate into a float product and a sink product by depressing one mineral | Cleaning stages within a Flotation Circuit | confirmed |
| Target mineral | The mineral (or minerals, for a bulk concentrate) a Flotation Circuit instance floats | The primary metal of the site — circuit order follows floatability, not value | confirmed |
| Bulk concentrate | A concentrate holding two or more payable minerals, floated together to be separated later (e.g., Cu-Mo) | A saleable concentrate | confirmed |
| Sequential flotation | Circuits chained so each is fed by the previous circuit's tailings (e.g., Cu → Zn; Pb → Zn) | Bulk-then-separate configuration | confirmed |
| Float product / sink product | The two outputs of a Concentrate Separation: the mineral floated and the mineral depressed | Concentrate / tailings of a Flotation Circuit | confirmed |
| Measurement point role (MP-01 to MP-10) | A P754 measurement position defined by role in a pattern, instantiated per circuit as `MP-05[Cu]` | A fixed numbered instrument at one site | confirmed |
| Tailings and water roles (TP-01 to TP-05, WP-01 to WP-11) | Tailings mass and water measurement positions defined by role, instantiated per stream, user or destination, e.g. `WP-05[tailings thickener]` | Site candidate IDs (e.g., E3-03), which map to a role in the overlay | confirmed |
| Thickening (3.3.1) | Pattern: feed, flocculate, pump underflow, recover overflow — one instance per thickener duty | "Concentrate thickening" / "tailings thickening" — these are duties (instances) | confirmed |
| Thickener duty | The stream a thickening instance handles: a saleable concentrate, a bulk concentrate, or the tailings | A specific thickener asset (a `process_node`) | confirmed |
| Tailings Storage Facility (TSF) | Canonical pillar term for the facility that stores tailings and supernatant water | TMF (site synonym, below) | confirmed |
| Tailings classification (3.5.2) | Splitting tailings by hydrocyclone into sand for construction and fines for deposition; optional | Hydrocyclone classification in grinding (3.1.3.3) | confirmed |
| Deposition method / construction method | Facility configuration: conventional, thickened or paste deposition; upstream, centreline or downstream construction | Process groups — both are configuration on `tailings_facility` | confirmed |
| Makeup water | New water brought into the site water system from a configured source; "fresh" and "desalinated" describe the source or treatment, not the role | Reclaim or recovered water | confirmed |
| Internal recycle | Water moving between systems inside the site (WP-05 to WP-09); counted once in the water balance, never as an input | Makeup water (an input) | confirmed |
| Water system | An accounting boundary for water: supply, process water, reclaim, seepage collection, facility water, or a remote location | A single pump or pipeline (a `process_node`) | confirmed |
| Transport leg (4.2.2) | Pattern: one segment of a site's route from mine to export port, with a configured mode, carrier and measurement method at each end | A whole route, which is a sequence of legs | confirmed |
| Transport mode | Road (trucks), rail (wagons), slurry pipeline, or sea (barge or coastal vessel) — configuration on `transport_leg` | A process group; there is no "road transport" or "pipeline transport" group | confirmed |
| Lightering | Loading a vessel at anchor from barges loaded at the port, where depth or ice prevents berthing; a vessel loading method | Direct loading at berth | confirmed |
| TMF | Tailings Management Facility — QB term for the pillar's Tailings Storage Facility (TSF) | — | provisional (QB discovery brief, 2026-10-20) |

---

## 4. ABBREVIATIONS AND ACRONYMS

Teck-specific abbreviations encountered in workshops. Listed here so the agent
does not interpret them as industry-standard terms.

| Abbreviation | Full Form | Context | Sites |
|-------------|-----------|---------|-------|
| HVC | Highland Valley Copper | Primary copper mine in BC, Canada | All |
| QB | Quebrada Blanca | Copper mine in Chile | All |
| CDA | Carmen de Andacollo | Copper mine in Chile | All |
| RED_DOG | Red Dog | Zinc-lead mine in Alaska | All |
| GDO | Global Data Owner | Programme governance role | All |
| DDVC | Data-Driven Value Chain | Teck's data architecture framework | All |
| MFD | Mobile Fleet Data | First curated data product in scope | All |
| TUM | Time Usage Model | GMG standard for equipment time classification | All |
| BEAM | Business Event Analysis & Modeling | Workshop methodology | All |
| ODCS | Open Data Contract Standard (v3) | Contract format used in teck-data-modeling | All |
| CDF | Change Data Feed | Databricks Delta feature for CDC | All |
| DLT | Delta Live Tables | Databricks streaming/batch pipeline framework | All |
| MDM | Master Data Management | Cross-system entity mastering | All |
| SCD | Slowly Changing Dimension | Historical tracking strategy for master entities | All |
| UC | Unity Catalog | Databricks data governance and cataloguing | All |
| DAB | Databricks Asset Bundle | Databricks CI/CD deployment unit | All |

---

## CHANGE LOG

Append-only. One row per confirmed addition or modification.

| Date | Entry | Changed By | Session | Notes |
|------|-------|------------|---------|-------|
| 2026-04-12 | Initial vocabulary master created | Programme setup | — | Seed entries from cross-reference summary and programme memory |
| 2026-10-23 | Added 3.5 Process Patterns and Configuration (pattern, configuration, Flotation Circuit, Concentrate Separation, target mineral, bulk concentrate, sequential flotation, float / sink product, MP roles; TMF provisional) | Fahim Kanji | ad-hoc (LL-005) | Terms follow the Pillar 3 restructure into generic process patterns |
| 2026-10-26 | Added to 3.5: TP / WP roles, Thickening and thickener duty, TSF (canonical), tailings classification, deposition / construction method, makeup water, internal recycle, water system | Fahim Kanji | ad-hoc (LL-012, LL-014) | Pillar 3 tailings and water management areas |
| 2026-10-26 | Added to 3.5: transport leg, transport mode, lightering | Fahim Kanji | ad-hoc (LL-018) | Pillar 4 generic transport |
