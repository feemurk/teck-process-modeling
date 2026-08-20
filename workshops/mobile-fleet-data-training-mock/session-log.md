# Session Log — mobile-fleet-data-training-mock

# ============================================================================
# ⚠ MOCK EXERCISE — NOT A LEGITIMATE PRODUCT. DO NOT HAND OFF TO STAGE 2. ⚠
# ============================================================================
# Every file under workshops/mobile-fleet-data-training-mock/ was generated without any
# live stakeholder engagement, at the explicit direction of the requester, purely to give
# a data-modeler training exercise a realistic set of Stage 1 artifacts to teach from —
# how process-model-ref.md, beam-overlay.yaml, and validate-overlay's report actually look,
# and how a Curated layer relates to a Contextualized one. It is not a scoped, workshopped,
# or validated data product. validate-overlay's own report on this overlay returns BLOCK,
# not PASS, and stays that way by design (see OI-007: no domain owner in this file was ever
# confirmed by a named person, because none was ever in the room).
#
# Do not copy these files to teck-data-modeling/products/mobile-fleet-data-training-mock/
# inputs/. Do not treat any entity, measure, KPI, or dimensional-model element here as
# confirmed. If a real Mobile Fleet Data (MFD) product is scoped later, per
# standards/teck-vocabulary-master.md's own repeated references to "the MFD data product,"
# it should be run as a genuine BEAM workshop with named participants — this mock's product
# name was deliberately chosen (mobile-fleet-data-TRAINING-MOCK, not mobile-fleet-data) so
# it cannot collide with that real workshop's folder.
# ============================================================================

*Written per CLAUDE.md's `log session` entry schema. This product was run as a single
continuous mock covering entity extraction, the BEAM workshop, and validation in one pass —
normally three separate commands / sessions with independent log entries. Logged as one
entry below with that deviation noted explicitly, rather than fabricating three separate
entries to look like three separate real sessions.*

```yaml
- id: "2026-08-06-mobile-fleet-data-training-mock-MOCK-FULL-PASS"
  date: "2026-08-06"
  product: "mobile-fleet-data-training-mock"
  session_type: "ENTITY-EXTRACTION | BEAM-WORKSHOP | VALIDATION"  # all three, mocked in one pass — see note
  participants: []  # none — no live stakeholder engagement; explicitly a training mock
  sections_completed:
    - "extract-entities: scope proposal and process-model-ref.md write"
    - "BEAM Section A equivalent: process anchor (2.2 Load & Haul, HVC primary + QB)"
    - "BEAM Section B equivalent: entity register for all 10 entities (natural key, source system, SCD, domain owner)"
    - "BEAM Section C equivalent: event canvas for 5 Transactional entities (haul_cycle, haul_cycle_stage_event, delay_event, operator_shift_assignment, stockpile_inventory_movement)"
    - "BEAM Section D equivalent: site variants for 5 of 10 entities"
    - "BEAM Section E: beam-overlay.yaml written; validate-overlay run; vocabulary additions drafted"
  sections_parked:
    - "BEAM Section D: site variants for equipment_class, location, haul_cycle_stage_event, operator_shift_assignment, stockpile_inventory_movement — not checked either way"
    - "Live confirmation of any domain_owner, natural_key stability, or grain statement with a named stakeholder — none occurred in this run at all"
  open_items:
    - "OI-001 through OI-008 — see beam-overlay.yaml Section 5 and validate-overlay-report.md for full detail"
  overlay_status: "complete"  # written and internally consistent, but NOT validated to PASS — see validate-overlay-report.md (status: BLOCK)
  next_session_plan: "A real BEAM workshop with named HVC/QB stakeholders and the FMS system owner must be run before this scope is used for an actual Stage 2 handoff. Priority items for that session: (1) confirm whether queue_dump_start_utc/spot_dump_utc and haul_cycle_stage_event actually exist at FMS source [OI-001, OI-002]; (2) name and confirm a domain owner per entity [OI-007]; (3) resolve the 5 outstanding site-variant checks; (4) resolve the 5 warn-stage2 open items (work_order_id linkage, calibration factor, shift boundary, delay code harmonisation, operator authorization by site)."
```

## Session 2 — Refresh: Source/Map entity types (2026-08-06, same day)

`templates/beam-workshop.md`, `.claude/commands/extract-entities.md`,
`templates/entity-extraction.md`, `templates/beam-overlay-schema.yaml`, and
`standards/teck-vocabulary-master.md` were updated to introduce two Teck-specific entity
types beyond the standard Master | Reference | Transactional | Time-Series set: **Source**
(a raw, per-source-system record, duplicates intact) and **Map** (a crosswalk from a
governed Master ID to one or more Source IDs, with a validity window). The trigger scenario
is now documented as confirmed at HVC in `standards/teck-vocabulary-master.md` §3.5: HVC
runs both Minestar and Wenco concurrently against the same equipment concept, with no MDM
engine reconciling them, each holding duplicate rows all marked "active."

```yaml
- id: "2026-08-06-mobile-fleet-data-training-mock-REFRESH-SOURCE-MAP"
  date: "2026-08-06"
  product: "mobile-fleet-data-training-mock"
  session_type: "BEAM-WORKSHOP"  # refresh of Section B (Entity Sign-Off) for one entity family
  participants: []  # still no live stakeholder engagement — training mock
  sections_completed:
    - "Re-derived mobile_equipment as entity_type: Master, redefining its natural key and source system to reflect governance-by-file rather than direct system sourcing"
    - "Added mobile_equipment_source_minestar and mobile_equipment_source_wenco (entity_type: Source)"
    - "Added mobile_equipment_source_xref (entity_type: Map)"
    - "Corrected a mis-application of multi_source_key_conflict/xref_required on stockpile_inventory_movement, found while fixing mobile_equipment for real"
    - "Re-ran mechanical schema verification (verify_overlay.py) — 0 REQUIRED-field failures across 13 entities"
    - "Regenerated validate-overlay-report.md — status BLOCK (4 items, up from 3 — see report for why that's the correct direction, not a regression)"
  sections_parked:
    - "Whether the same multi-FMS mastering pattern applies to operator or location was raised as a plausible risk but NOT modeled — the trigger scenario named equipment specifically, and extending the pattern to other entities without evidence would have been guessing, not extraction. Left as OI-012's spirit but not separately built out."
  open_items:
    - "OI-009 through OI-012 added — see beam-overlay.yaml Section 5. OI-009 (the governance process itself doesn't exist) is the most consequential: it's an organizational commitment, not a data-modeling question, and blocks Stage 2 on its own."
  overlay_status: "complete"  # still not validated to PASS — see validate-overlay-report.md
  next_session_plan: "Unchanged in substance from Session 1's next_session_plan, with OI-009 (stand up the site-steward + product-team mastering process) now the top-priority item — nothing about equipment identity is safe to build on until that exists."
```

---

## Session 3 — ERD generation, reorganization, and Contextualized dimensional model (2026-08-06/07)

Two follow-on asks, both independent of the standard BEAM workflow and both explicitly
flagged by the requester as outside CLAUDE.md's normal scope for this repo, for the same
training purpose as the rest of this mock:

1. An entity-relationship diagram of `process-model-ref.md`, generated as a draw.io/mxGraph
   XML file importable into Lucidchart. First pass used single-column auto-routed edges;
   several crossed entity boxes on import. Rebuilt around a two-row + dedicated-lane layout
   with fully explicit, hand-computed edge waypoints (no auto-routing) and a real geometric
   segment-vs-box collision check in a companion verifier
   (`BPMN-generator/tools/erd_layout.py` / `erd_verify.py`) — the same discipline already
   established for the BPMN diagrams. A color legend was added per entity type.
2. `beam-overlay.yaml` Section 7 (the non-standard Contextualized KPI addendum) was found to
   have KPI formulas but no actual dimensional model underneath them. Rebuilt as a real
   fact/dimension structure — 7 dimensions, 2 facts (`fct_equipment_time_usage`,
   `fct_material_movement`), 9 KPIs re-expressed against those facts — at the minimal
   analytical grain directed (site, shift, equipment, operator), with an explicit, reasoned
   decision on whether location belongs in that grain (not required for TUM
   availability/reliability metrics; required for material movement metrics — see Section
   7's own header comment for the full rationale). This dimensional model was then rendered
   as a second tab in the same `erd.drawio` file, reusing the same layout/verification
   tooling rather than inventing new geometry.

```yaml
- id: "2026-08-07-mobile-fleet-data-training-mock-ERD-AND-DIMENSIONAL-MODEL"
  date: "2026-08-07"
  product: "mobile-fleet-data-training-mock"
  session_type: "BEAM-WORKSHOP"  # extension of Section C/E — dimensional model is a natural continuation of the event canvas, not a new workflow
  participants: []  # still no live stakeholder engagement — training mock
  sections_completed:
    - "erd.drawio Tab 1: Curated ER model, 15 entities (13 real + 2 cross-pillar external), 21 relationships, verified 0 box-crossings"
    - "beam-overlay.yaml Section 7 rebuilt: 7 dimensions, 2 facts, 9 KPIs re-expressed against the facts"
    - "erd.drawio Tab 2: Contextualized dimensional model (star schema), 12 entities, 15 relationships, verified 0 box-crossings"
    - "Generalized erd_layout.py/erd_verify.py to support N diagram tabs in one file, not just one"
  sections_parked: []
  open_items:
    - "No new OI numbers — this session restructured existing KPI content and added a visualization; it did not surface new unresolved business questions beyond what OI-001 through OI-012 already cover"
  overlay_status: "complete"  # still not validated to PASS — see validate-overlay-report.md (status: BLOCK, unchanged from Session 2)
  next_session_plan: "n/a — see SESSION CLOSED below. If a real MFD product is scoped later, none of this mock's content should be reused as-is; it should be re-derived from a genuine workshop."
```

---

## SESSION CLOSED — 2026-08-07

This workshop is closed. `mobile-fleet-data-training-mock` is a **training mock, not a
legitimate data product** — see the banner at the top of this file. No further sessions are
planned against this product name. `overlay_status` remains `complete` (internally
consistent, all files cross-reference correctly) but **not validated** — `validate-overlay`
returns BLOCK, and that is the correct, intended final state for this exercise, not an
unfinished task.

Deliverables produced across Sessions 1–3, all under
`workshops/mobile-fleet-data-training-mock/`: `process-model-ref.md`, `beam-overlay.yaml`,
`session-log.md` (this file), `validate-overlay-report.md`, `erd.drawio`.

Reusable, non-mock work product from this exercise (legitimate, not flagged): the
Source/Map entity-type extension to `templates/beam-workshop.md`,
`.claude/commands/extract-entities.md`, `templates/entity-extraction.md`,
`templates/beam-overlay-schema.yaml`, and `standards/teck-vocabulary-master.md`; the
Curated/Contextualized product-type formalization in `CLAUDE.md`; and the
`erd_layout.py`/`erd_verify.py` tooling in `BPMN-generator/tools/`. These apply to any
future real workshop and are not specific to this mock.

---

## Deviations from a real BEAM session (recorded per CLAUDE.md's session-log discipline)

This run was explicitly commissioned as a fast mock for a data-modeler training exercise —
not a production Stage 1 deliverable. Deviations from the real protocol, all at the
requester's explicit direction:

1. **No live stakeholder engagement.** All three commands (`extract-entities`,
   `run-beam-workshop`, `validate-overlay`) were run as a single drafting pass rather than
   as separate, stakeholder-facing sessions with confirmation gates.
2. **Natural key and SCD shortcuts applied uniformly** rather than elicited per entity:
   every natural key assumed to be the documented system identifier field, assumed stable;
   every entity (including Transactional/event entities) given `scd_policy: Type2` on its
   full attribute set, reasoned as serving both Type-1 and Type-2 consumption needs and as
   necessary even on event tables because FMS permits post-hoc edits/corrections.
3. **A new entity (`haul_cycle_stage_event`) and two new `haul_cycle` attributes
   (`queue_dump_start_utc`, `spot_dump_utc`) were proposed** to make every haul-cycle
   lifecycle-stage duration auditable from explicit start/end timestamps, closing a gap in
   the standard pillar model — both flagged `needs-workshop` pending confirmation that they
   actually exist (or can be built) at the FMS source.
4. **A non-standard Section 7 (Contextualized KPI Addendum)** was added to
   `beam-overlay.yaml`, containing actual GMG TUM / reliability / material-movement KPI
   formulas. CLAUDE.md states this belongs to Stage 2, not this repo — Section 7 exists
   here anyway, at explicit request, specifically so the training audience can see how a
   Contextualized layer is built on top of a Curated one in a single artifact. It is
   clearly labeled in the file itself as non-standard and outside `validate-overlay`'s
   schema checks.

None of these deviations were silently absorbed — each is flagged inline in
`beam-overlay.yaml`, in `process-model-ref.md`, and here.
