# Metric-to-Process Crosswalk — Water-and-Tailings

Status: working draft, analyst review. Not a Stage 2 handoff file.
Sources cross-referenced:
- `inputs/QB_Reporting_List_Foundation_v06_Carol_Review.xlsx` (Sheet 1 rows 12–49; Measurement Points tab MP-01 to MP-22; Assessment Sources tab)
- `inputs/QB_DA_Discovery_Brief_v09_With_Architecture_Appendices.docx` (working draft v0.8 in document text)
- Pasted Teck KPI list (38 rows, Spanish originals and suggested names)
- `process-model-ref.md` (entities, TP/WP roles, dependencies D1–D9, phasing, workshop question inventory)

Numbering in Part 1 follows the pasted Teck list. Workbook row numbers are given in Part 4.

Nothing here is a KPI definition or formula. Derived metrics are listed with their inputs only (CLAUDE.md: metric calculations belong in Stage 2).

---

## Part 1 — 38-metric matrix

Columns: pillar home (process-model-ref group or dependency), entity or measurement point that would carry the input, and the open point that blocks completeness.

| # | Metric | Pillar home | Entity / measurement point | Open point |
|---|---|---|---|---|
| 1 | RWS Availability | D5 (Pillar 5, Release 2); reclaim pumps 3.6.2 | MP-13 (equipment, not a meter) | Pillar 5 has no owner; process boundary open (Carol) |
| 2 | RWS Utilization | 3.6.2 | MP-13 | Denominator needs rated capacity, which no entity holds (G8); not in the Release 2 list in process-model-ref |
| 3 | Seepage Availability | D5; 3.6.3.3 recovery pumps | MP-17 (equipment) | Included pump population undefined |
| 4 | Seepage MTBF | D5; D6 (Teck definition) | MP-17 | Teck standard wording not yet obtained |
| 5 | Seepage MTTR | D5; D6 | MP-17 | As row 4 |
| 6 | Desalination Plant Availability | D5; 3.6.1.2 treatment (water_system, source seawater) | MP-22 | Equipment population undefined |
| 7 | Desalination Plant MTBF | D5; D6 | MP-22 | As row 6 |
| 8 | Desalination Plant MTTR | D5; D6 | MP-22 | As row 6 |
| 9 | Tailings Generated | 3.3.1 tailings duty (underflow to 3.5) | TP-01 (MP-02, MP-04); alternative is AMIRA MP-06 (out of product) | No plant-side entity: `tailings_deposition_record` is deposition-only (G1). Boundary choice open |
| 10 | Tailings | 3.3.1 / 3.5.2 | Unresolved (MP-09, MP-11 are candidates) | Definition open; name truncated in source ("Tailings (need") |
| 11 | % Solids in | 3.3.1 feed | MP-01 (equivalent to AMIRA MP-06 feed) | Stream not identified; name truncated; no Spanish source name |
| 12 | % Solids in Thickened Tailings | 3.3.1.3 underflow | TP-01 (density) via MP-02 | `pct_solids` sits on the deposition record, not on the transfer |
| 13 | Tailings Thickener Solids | 3.3.1.3 | TP-01 | Concentration or mass flow? Two measures under one name; uom unclear |
| 14 | Deposited Sands | 3.5.4.1 construction placement | TP-04; `construction_placement_record` (classified_sand, paddock) | Clean fit; uom (m or m³) open |
| 15 | Fine Sands | 3.5.2 fines | TP-03; `tailings_deposition_record` stream = fines, if overflow | Meaning unresolved (overflow, quality fraction, or deposit category) |
| 16 | Sand Production | 3.5.2.2 classification | TP-02; **no entity** | Classification output recorded nowhere (G2) |
| 17 | Sand/Tailings Ratio | Derived from 3.5.2 | Inputs: TP-02 and TP-01 | Stage 2 derived metric; inputs unrecorded until G1 and G2 close |
| 18 | Produced Sand/Tailings Ratio | Derived from 3.5.2 | Inputs: TP-02 and TP-01 | As row 17 |
| 19 | Bench Deposition | 3.5.4.1 | `construction_placement_record` (rockfill, bench location) | "bench" not in `facility_location.location_type` (G3). Unit unresolved. Duplicate concept with row 20 |
| 20 | Bench Deposition (m³) | 3.5.4.1 | `construction_placement_record.volume_m3` | As row 19 |
| 21 | Prism Deposition | 3.5.4.1 | `construction_placement_record` (classified_sand, embankment zone) | Prism geometry and material unverified; no location type (G3) |
| 22 | Paddock 1 Growth (m) | 3.5.4 | `facility_location` (paddock) + `facility_survey_record` | No elevation per location in survey record (G4); MP-19 untagged |
| 23 | Rockfill (m³) | 3.5.4.1; D8 | `construction_placement_record` (rockfill) | Source open (Brief VQ-06); D8 non-blocking |
| 24 | Freeboard at Month-End | 3.5.5.1 storage and safety | `tsf_inventory_record.freeboard_m` and `freeboard_criterion_m`; crest from `facility_survey_record` | Best fit in the set. Criterion snapshot (WQ-F2), datum, Pillar 6 link (D7) |
| 25 | Lagoon Growth | 3.5.5.1 | `tsf_inventory_record` pond fields, or `facility_survey_record` pond area and volume | "Lagoon" is not pillar vocabulary (pillar says "pond"); three possible definitions; none selected |
| 26 | Fresh Water Make-Up | 3.6.1.4–3.6.1.5 | `water_transfer_record` into makeup system at WP-04 | Vocabulary master: "fresh" describes the source, not the role. Rename candidate, e.g. "Makeup Water Received" |
| 27 | Total Concentrator Water | Derived from 3.6.4 | Sum of transfers into the concentrator water system; WP-10 | No concentrator `water_system` defined; WP-10 has no candidate (G9); concentrate-duty recovered water (WP-05, WP-06) in or out of scope |
| 28 | Pumped Water | 3.6.1.4 | `water_transfer_record` at WP-04 | Source unknown (Carol: from desalinated storage?); same water as rows 26, 37, 38 at other boundaries |
| 29 | Pumped Water Excluding Collahuasi | 3.6.1.4 plus `shared_with` | `water_transfer_record.allocation_rule`; `water_system.shared_with` | "Diverted to Collahuasi" has no system type (G5); allocation rule unconfirmed (WQ-W1) |
| 30 | RWS Recycled Water | 3.6.2 (WP-07 or WP-08), internal recycle | `water_transfer_record` (facility_water → process_water, `internal_recycle_flag`); MP-05 | WP-07 or WP-08 unresolved; line direction and equipment tags unverified |
| 31 | RWS Recycled Water per Ton | 3.6.2 divided by tonnes | Row 30 ÷ mill throughput | **No owner for the throughput denominator** in D1–D9 (G7, new D10) |
| 32 | RWS Flow Rate | 3.6.2 (WP-07, WP-08) | MP-05 (flow) | A rate, not a volume; needs D2 (G6) |
| 33 | MWS Flow Rate | 3.6.1.4 | MP-21 (flow) | MP-21 is in neither supplied drawing; rate (G6) |
| 34 | Seepage Pond 1 Level | 3.6.3.2 monitor ponds; WP-11 store level | Level on `facility_location` (seepage_pond); MP-14 | Datum unknown; tailings pond inventory does not cover seepage ponds |
| 35 | Seepage Pond 2 Level | As row 34 | MP-15 | As row 34 |
| 36 | Seepage Flow (m³/h) | 3.6.3.3 recovery pumping (WP-09) | MP-16 (flow) | No verified seepage header; rate (G6); Pillar 6 surveillance input (D7) |
| 37 | Desalinated Water Produced | 3.6.1.2 treatment (WP-02) | MP-21 only | No dedicated candidate |
| 38 | Desalinated Water Pumped | 3.6.1.4 (WP-04) | `water_transfer_record` (desal → makeup system); MP-21 | Overlaps rows 26 and 28 |

---

## Part 2 — Overlap clusters

Metrics that read the same physical stream, or the same equipment and survey records. Each cluster should be modelled once, with the metrics as views on it.

- **Makeup chain (26, 28, 29, 33, 37, 38):** one physical water path measured at several boundaries, ending in an allocation step. Carol's notes ask the same identity question. Model one boundary chain with measurement points.
- **Tailings solids (9–13, 17, 18):** one underflow stream with three solids measures (% Solids in, % Solids in Thickened Tailings, Tailings Thickener Solids). Carol's notes say they must not be equated without validation.
- **Sand (14–18):** pillar identity TP-02 = TP-04 + rejected sand + change in cell inventory. The ratios and deposited-sand metrics all depend on it.
- **Dam geometry (19–25):** survey and construction records. Freeboard and Lagoon Growth both derive from pond level; the workbook already says to avoid duplicating them.
- **Reclaim (1, 2, 30, 31, 32):** one system. Utilization and flow share the same meter candidate (MP-05, MP-13).
- **Seepage (3–5, 34–36):** the same pumps and ponds (MP-14 to MP-17).
- **Desalination (6–8, 26, 37, 38):** the same plant and transmission path.
- **Composite (27):** a sum over the other streams. This is the double-count risk the brief warns about; internal recycles (WP-05 to WP-09) must be counted once.

---

## Part 3 — Gaps the process model cannot yet hold

| ID | Gap | Affects | Suggested route |
|---|---|---|---|
| G1 | No entity holds plant-side tailings generated before deposition. `tailings_deposition_record` is deposition-grain only, although its pillar description says it separates generated from deposited | 9, 10, 13, 17 | Workshop question; decide between a transfer record or a measurement-only home |
| G2 | Sand produced (TP-02) has no record. The deposition stream enum has no sand value, and construction placement starts at placement. Pillar 3.5.2 has no output entity | 16, 17, 18 | Workshop question; `log learning` candidate (generic: any site with classification) |
| G3 | `facility_location.location_type` has no bench or prism value | 19, 20, 21 | Workshop question (WQ-L1); a generic construction-zone value, not a site-specific name |
| G4 | `facility_survey_record` holds crest elevation only; no elevation per location | 22 | Attribute proposal for the entity note |
| G5 | `water_system.system_type` has no value for a non-Teck shared party | 29 | Depends on WQ-W1 |
| G6 | `water_transfer_record` holds volume only; rate metrics need measurement telemetry | 32, 33, 36 | Already D2 (Curated measurement events) |
| G7 | Mill throughput denominator is not in the cross-pillar dependency list | 31 (and any tonnage ratio) | Add as new dependency D10; owner to be named |
| G8 | Utilization denominators need rated capacity; no entity holds it | 2, 32 (context) | Attribute proposal; check D1 minimum key contract |
| G9 | WP-10 (process water distributed per user) has no measurement candidate | 27 | Add candidate MP; needed for the concentrator boundary |

**Pillar roles with no candidate measurement:** TP-05 (tailings deposited in impoundment), WP-01 (raw water abstracted), WP-03 (treatment residue discharged), WP-10 (process water distributed). WP-02 is covered only by MP-21, and WP-08 only by the ambiguous MP-05.

**Pillar role gaps for `log learning`:** a classification-feed role (cyclone feed, MP-09 candidate, has no TP role) and a classifier output record (G2).

---

## Part 4 — Measurement point candidates against pillar roles

Workbook Measurement Points tab, MP-01 to MP-22.

| Candidate | Workbook boundary | Pillar role | Result |
|---|---|---|---|
| MP-01 | Tailings thickener feed | AMIRA MP-06 (out of product) | Same point under another ID; rename |
| MP-02 | Thickener underflow to TMF | TP-01 | Clean |
| MP-03 | Thickener overflow recovered | WP-05 | Clean (concentrate duty, see Part 6) |
| MP-04 | Tailings transferred to TMF | TP-01 | Duplicates MP-02 (workbook asks this itself) |
| MP-05 | TMF recovered-water return | WP-07 or WP-08 | Partial; role choice open |
| MP-06 | TMF pond observation | WP-11 plus survey | Partial; overlaps MP-20 |
| MP-07 | Copper concentrate thickener overflow | WP-05 (concentrate duty) | Out of product scope as a process |
| MP-08 | Port filtrate | WP-06 (concentrate filtration) | Out of product scope as a process; remote water system |
| MP-09 | Cyclone feed to BHC-1/BHC-2 | No pillar role | Pillar gap (Part 3) |
| MP-10 | Cyclone underflow sand product | TP-02 | Clean |
| MP-11 | Cyclone overflow fines | TP-03 | Clean |
| MP-12 | Sand placed in paddocks | TP-04 | Clean |
| MP-13 | Reclaim pumping equipment | None (equipment) | Not a meter; move to D1/D5 |
| MP-14 | Seepage pond 1 level | WP-11 | Clean; datum open |
| MP-15 | Seepage pond 2 level | WP-11 | Clean; datum open |
| MP-16 | Seepage recovery pumping discharge | WP-09 | Clean; no verified header |
| MP-17 | Seepage pumping reliability | None (equipment) | Not a meter; D5 |
| MP-18 | Embankment, bench, prism survey | None (survey event) | `facility_survey_record` and `construction_placement_record` |
| MP-19 | Paddock 1 growth | None (survey event) | `facility_survey_record`; elevation gap (G4) |
| MP-20 | Crest and controlling pond survey | None (survey event) | `facility_survey_record`; overlaps MP-06 |
| MP-21 | Desalination and MWS meters | WP-02, WP-04 | Partial; not in either drawing |
| MP-22 | Desalination reliability | None (equipment) | Not a meter; D5 |

Result: 9 clean (one duplicate), 3 partial, 2 out-of-scope duties, 1 equivalent to AMIRA MP-06, 1 with no pillar role, 6 not meters.

---

## Part 5 — Metrics the sources do not cover

Candidates for the analyst to decide. None is in the 38.

- **M1 Tailings deposited (TP-05):** the pillar's final sink has no metric.
- **M2 Available storage capacity** (`tsf_inventory_record.available_capacity_m3`, `capacity_status`): output of 3.5.5.2, no metric.
- **M3 Operating constraints** issued and active (`facility_operating_constraint`): no metric. WQ-C8 covers whether needed for Release 1.
- **M4 Water balance closure and error** (`water_balance_record.balance_error_m3`): no metric. Total Concentrator Water is the nearest, and it is a composite.
- **M5 Brine and raw abstraction** (WP-03 residue, WP-01 intake): the brief describes brine disposal; neither has a metric or candidate.

---

## Part 6 — Scope and dependency notes

- **Concentrate-duty water:** rows 27 and MP-03 depend on recovered water from concentrate thickening and filtration (3.3.1 concentrate duties, 3.3.2.4). Those are out of product scope as processes, but their recovered water enters as `water_transfer_record`. Confirm whether MP-03, MP-07 and MP-08 stay in this product.
- **Desalination location:** no process-model-ref line names desalination. It sits under 3.6.1 (treatment WP-02, residue WP-03, transmission WP-04) with source type seawater. Confirm this reading at the workshop.
- **Reliability (rows 1–8):** all depend on Pillar 5 (D5) and the Teck definitions (D6). RWS Utilization is not named in the Release 2 list; assign its phase.

---

## Part 7 — Source conflicts

1. **MP ID collision:** workbook uses MP-01 to MP-22. Process-model-ref and the pillar use MP-06 for the thickener feed. The workbook's MP-06 is the TMF pond. Rename workbook IDs.
2. **Sheet 1 count:** brief says 38 metrics on Sheet 1. Sheet 1 has 74 rows; 38 are Tailings & Water, 36 are Mine, Filtration and Port.
3. **S1 year:** brief says NI 43-101 effective 31 December 2023; workbook says (2024). The URL file name says 12312023.
4. **Brief version:** file name v09; document text says Working Draft v0.8.
5. **Acronym:** workbook note "Reclaimed Water System (RMS)"; brief and pillar use Reclaim Water System (RWS).
6. **Vocabulary master:** "Bench" is TBC; this crosswalk uses "bench" as in the workbook pending confirmation.
7. **Pasted list:** suggested names for rows 4, 5, 7, 8 have typos ("Faliures") and inconsistent capitals. Row 11 has no Spanish name and its name is truncated. Rows 22 (Paddock 1 Growth) and 23 (Rockfill) have English-only Spanish originals.
8. **Workbook Spanish column:** 7 of 38 populated. Bench (m³) and Prism Spanish terms differ from the pasted originals.

---

## Part 8 — Metadata coverage

| Field | Pasted list | Workbook Sheet 1 | Process-model-ref |
|---|---|---|---|
| Spanish name | 37 of 38 | 7 of 38 | — |
| Hierarchy | L1, L2, L3 on all 38 | Area and Category on all 38 | Process group (not per metric) |
| Enterprise priority | — | 12 of 38 | — |
| Definition | — | 38 | Entity definitions |
| Calculation | — | 38 (illustrative; 2 "not selected") | — |
| UOM | — | 38 candidate; 6 unresolved (Tailings, Fine Sands, Bench, Prism, Lagoon Growth, Total Concentrator Water); Thickener Solids unclear | Units per attribute |
| Source confidence | — | 38, all "Engineering working interpretation". None carries a T, I, H or V code | — |
| Validation question | — | 38 (Carol) | — |
| Owner | None | None | — |
| Source system | None | None | Per entity |
| Frequency and time basis | None | None | Period grain per entity |
| Phase | — | — | Release 2 list omits RWS Utilization |

**Taxonomy conflicts:** Freeboard is "Sustainability" in the pasted list and "Safety" in the workbook. Seepage Flow is "Sustainability" vs "Environment". Bench is "Sustainability" vs "Site Operational". The pasted L3 names can serve as a crosswalk to pillar process IDs.

---

## Part 9 — Next steps

1. Rename workbook MP IDs; add a column mapping each to a pillar role or "not a meter"; merge MP-02 with MP-04 and bench rows 19 and 20.
2. Add workshop questions to the Water-and-Tailings inventory (via `extract entities`, not by hand): plant-side tailings boundary (G1); sand-produced record (G2); bench and prism location types (G3); WP-10 and the concentrator system (G9); Collahuasi destination (G5); RWS Utilization phase; D10 throughput owner; disposition of M1–M5.
3. Log two pillar gaps with `log learning`: classification-feed role and classifier output record.
4. Backfill Spanish names from the pasted list; correct the typos; add owner, source system and T/I/H/V codes per metric.
5. Correct brief inconsistencies (Part 7) before the pre-read is circulated.
