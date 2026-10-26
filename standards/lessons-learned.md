# Lessons Learned — teck-process-models
# standards/lessons-learned.md
#
# Append-only register of open and applied learnings captured during
# process modeling and BEAM workshop sessions.
#
# Claude Code: append entries via `log learning`. Never edit existing entries.
# Read all open entries at `triage learnings`.
# Update status to 'applied' via `apply learning LL-[id]`.
#
# SCOPE: Programme-wide — not product-scoped.
# Covers corrections to: pillar model content, beam-workshop.md facilitation logic,
# beam-overlay-schema.yaml field definitions, entity-extraction.md scoping rules,
# teck-vocabulary-master.md entries, and CLAUDE.md behaviour.

---

## Entry Schema Reference

```yaml
- id: LL-[NNN]
  date: YYYY-MM-DD
  session: "[YYYY-MM-DD]-[product-name]-[session-type] | ad-hoc"
  product: "[product-name] | programme-wide"
  captured_by: "[modeler name | unknown]"
  status: "open"    # open | approved | applied | rejected

  what_happened: >
    [What was wrong, incomplete, or suboptimal. Specific — reference the file,
     section, and the exact issue.]

  correct_approach: >
    [The correct approach written as a rule or instruction.
     This becomes the standard text if applied.]

  affects:
    - file: "[relative path]"
      section: "[section name]"
      change_type: "fix | addition | removal | clarification | new_rule | behaviour"

  integration_notes: >
    [Optional: nuance needed when applying — edge cases, exceptions, dependencies.]
```

---

## Open Entries

<!-- Claude Code appends entries here. Do not add entries manually. -->

# LL-001 to LL-004 were inferred from the BPMN files and README on 2026-10-21, not
# from a recorded correction session. The BPMN files were untracked in git, so no
# before/after diff existed. Confirm against the modeler's recollection.

```yaml
- id: LL-001
  date: 2026-10-21
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Claude Code (inferred from files)"
  status: "applied"

  what_happened: >
    The BPMN diagrams in pillar-models/bpmn/02-mining-operations-extraction/ follow a
    consistent naming pattern for files, pools, tasks, lanes and XML IDs, but the
    README only documented task naming. The pattern was not written down as a
    standard, so later diagrams for other pillars could drift from it.

  correct_approach: >
    BPMN files follow the naming standard in the folder README: folder named after the
    pillar model file; file `[ID]_[kebab-case title].bpmn` with `&` written as `and`;
    pool and task names `[ID] [Title]` copied from the decomposition table, with ` (L2)`
    on L2 pools; narrative-only steps carry no ID; lanes use the Actor column; gateways
    are questions; XML IDs are `[Type]_L[level]_[ID with underscores]`.

  affects:
    - file: "pillar-models/bpmn/02-mining-operations-extraction/README.md"
      section: "Naming standard"
      change_type: "new_rule"

  integration_notes: >
    Applies to every pillar's bpmn folder. Pillar model content is not affected.

- id: LL-002
  date: 2026-10-21
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Claude Code (inferred from files)"
  status: "applied"

  what_happened: >
    The README's resolution note for 2.1.1 called task 2.1.1.2 "Design Hole Layout".
    The decomposition table and the diagram name it "Design Hole Layout Parameters".
    The shortened title broke the rule that titles match the decomposition.

  correct_approach: >
    Use the decomposition title in full wherever a step is named, in diagrams and in
    documentation.

  affects:
    - file: "pillar-models/bpmn/02-mining-operations-extraction/README.md"
      section: "How the diagrams resolve the source-model issues"
      change_type: "fix"

  integration_notes: >
    Pillar model line 326 also labels 2.1.1.3 "Explosive Selection", while the
    decomposition says "Select Explosive Product". That is in the pillar model and
    is not changed here. See LL-003.

- id: LL-003
  date: 2026-10-21
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Claude Code (inferred from files)"
  status: "open"

  what_happened: >
    In pillar-models/02-mining-operations-extraction.md, the 2.1.1 triggers contradict
    each other. 2.1.1.1 Survey & Stake Pattern is triggered by "Approved blast pattern
    file", but 2.1.1.2 Design Hole Layout Parameters is triggered by "Survey completion
    confirmation", so each waits on the other. 2.1.1.3 Select Explosive Product lists
    "hole water measurement available" as a trigger, which only exists after drilling
    (2.1.2.3). The 2.1.1.3 title also differs between the decomposition row and line 326
    ("Explosive Selection").

  correct_approach: >
    Design precedes survey: 2.1.1.2 starts from the geotechnical assessment, 2.1.1.1
    starts from the approved pattern design, and 2.1.1.3 uses design-time water
    conditions with per-hole confirmation at charging. Use one title for 2.1.1.3.

  affects:
    - file: "pillar-models/02-mining-operations-extraction.md"
      section: "Process Decomposition (2.1.1.1 to 2.1.1.3); line 326 label"
      change_type: "fix"

  integration_notes: >
    The diagram 2.1.1_blast-design-and-pattern-layout.bpmn already follows the corrected
    order. Do not apply without explicit confirmation that this is an error in the
    industry standard and not a Teck-specific practice.

- id: LL-004
  date: 2026-10-21
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Claude Code (inferred from files)"
  status: "open"

  what_happened: >
    Some steps in the Process Flow Narratives of pillar 2 have no L4 row, so they have
    no ID, inputs/outputs, TUM state or DDVC layer. The BPMN diagrams draw them as
    unnumbered tasks: Remediate or redesign rejected holes (2.1.2); Flag payload
    exception for review (2.2.2); Classify breakdown as TUM: DT (2.2.3); Assess
    stability event and Issue operational constraint (2.3.3). Submit to Laboratory
    (2.1.5) is not drawn at all. Haul road steps in 2.3.1 are also not drawn.

  correct_approach: >
    Add L4 rows for the narrative-only steps that change the flow, then rename the
    BPMN tasks to carry the new IDs.

  affects:
    - file: "pillar-models/02-mining-operations-extraction.md"
      section: "Process Decomposition"
      change_type: "addition"
    - file: "pillar-models/bpmn/02-mining-operations-extraction/"
      section: "affected L3 diagrams"
      change_type: "fix"

  integration_notes: >
    Needs explicit instruction before the pillar model is changed. Until then the
    README's L4 gaps table is the record.
```

```yaml
- id: LL-005
  date: 2026-10-23
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Fahim Kanji (with Claude Code)"
  status: "applied"

  what_happened: >
    Pillar 3 decomposed flotation into commodity-specific process groups — 3.2.2 Copper
    Flotation Circuit, 3.2.3 Zinc Flotation Circuit, 3.2.4 Lead Flotation Circuit — although
    their L4 steps were the same pattern (rougher, scavenger, regrind, cleaner; the BPMN spec
    even said Zn "mirrors CUF structure"). Mineral-specific content (CuSO4 activation, pH,
    depressants, specs) was built into process groups, and sites were named in process rows
    and gateways ("Polymetallic site (Antamina / Red Dog)?"). Molybdenum by-product recovery
    had no home (gap G1) because it is a bulk-then-separate pattern, not a fourth commodity.
    The first QB Water-and-Tailings adaptation repeated the error by deleting and renaming
    process groups to describe the QB instance.

  correct_approach: >
    Process groups and L4 steps are site- and mineral-agnostic business processes. Where the
    same steps recur for different minerals or sites, model one reusable pattern and treat
    the differences as configuration. Flotation is two patterns: Flotation Circuit (3.2.2),
    run once per target mineral or bulk concentrate and chained through each circuit's
    tailings; and Concentrate Separation (3.2.3), which splits a bulk concentrate. The order
    of circuits is set by mineral floatability, not by economic primacy (Pb is floated before
    Zn in Pb-Zn ore; Cu-Mo is floated together, then separated). Which pattern instances a
    site runs, in what order, with what reagent scheme and product specification, is
    configuration data (flotation_circuit, process_node, concentrate_type) recorded in the
    overlay. Mineral and site names may appear only as illustrations and in the
    configuration variants table.

  affects:
    - file: "pillar-models/03-processing-and-beneficiation.md"
      section: "Overview; 3.2 decomposition; 3.3.4 (new); Mass Balance Node Maps; SIPOC 3.2; Entity Catalog (flotation_circuit); Narratives 3.1 to 3.3; Circuit Configuration Variants; Gap G1; Revision Notes"
      change_type: "fix"
    - file: "pillar-models/00-cross-reference-and-summary.md"
      section: "Pillar 3 flow diagram; mass balance boundaries; XP-08; summary statistics"
      change_type: "fix"
    - file: "pillar-models/bpmn/03-processing-and-beneficiation/"
      section: "3.2 diagrams replaced by pattern diagrams; 3.3 and 3.3.4; L1; README"
      change_type: "fix"
    - file: "BPMN-generator/03-processing-bpmn-spec.md"
      section: "P3_L2_FLT; P3_L3_RGT, FLC, SEP; P3_L2_DWT; P3_L2_COM gateway"
      change_type: "fix"
    - file: "standards/teck-vocabulary-master.md"
      section: "3.5 Process Patterns and Configuration"
      change_type: "addition"

  integration_notes: >
    Confirmed by the modeler as a correction to the industry-standard model, not a Teck
    variant. Measurement points became roles (MP-01 to MP-10) instantiated per circuit;
    MP-01 to MP-06 keep their former Cu-circuit meaning as roles, MP-07 is any later
    circuit's feed, MP-08 to MP-10 are separation points; former MP-08 to MP-15 retired.
    ID mapping in the pillar's Revision Notes. Open recommendation: shift_mass_balance,
    concentrate_production_record and osa_grade_telemetry still carry fixed per-metal
    columns (cu_, zn_, pb_); they should key metals as data.

- id: LL-006
  date: 2026-10-23
  session: "ad-hoc"
  product: "Water-and-Tailings"
  captured_by: "Fahim Kanji (with Claude Code)"
  status: "applied"

  what_happened: >
    Asked to adapt Pillar 3 for the QB Water-and-Tailings product, Claude Code "narrowed"
    the model to the QB instance: it removed process groups QB does not run, renamed and
    re-scoped others after QB equipment (molybdenum separation, port filtration, QB
    pipeline), and left ID gaps (3.2.2 to 3.2.5). The result described one site, not the
    business process, and could not be reused at another site.

  correct_approach: >
    A product or site adaptation never deletes, renames or re-scopes a pillar process
    group. Site specifics are configuration: which optional groups run, how many pattern
    instances, in what order, and the site's equipment, names, routes and measurement
    points. Record them in the overlay (site_overrides, process_model_overrides) or a
    configuration section keyed to unchanged pillar IDs. If the pillar lacks a generic
    process the product needs, propose a generic pillar addition (log learning) rather
    than inventing a site-specific group in the product.

  affects:
    - file: "CLAUDE.md"
      section: "PROCESS GROUPS ARE GENERIC; NEVER DO"
      change_type: "new_rule"

  integration_notes: >
    The QB adaptation in workshops/Water-and-Tailings/process-model/ predates this rule
    and is under review before any rework.

- id: LL-007
  date: 2026-10-23
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Claude Code"
  status: "applied"

  what_happened: >
    In pillar-models/03-processing-and-beneficiation.md the P754 annotations used
    unescaped pipe characters inside table cells, so the decomposition tables did not render
    as tables and could not be parsed reliably. Row 3.3.3.2 had no Primary Actor(s) cell
    (10 cells instead of 11), shifting its later cells left; seven other rows with the same
    defect were the retired Zn and Pb rows.

  correct_approach: >
    Escape the pipe character as a backslash-pipe inside any table cell. Every
    decomposition row has exactly 11 cells; BPMN builds parse the tables and skip malformed
    rows, so a missing cell drops a step.

  affects:
    - file: "pillar-models/03-processing-and-beneficiation.md"
      section: "Process Decomposition (all P754 annotations); row 3.3.3.2"
      change_type: "fix"

  integration_notes: >
    Other pillar files were not checked for the same defect in this session.
```

```yaml
- id: LL-008
  date: 2026-10-26
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Fahim Kanji (with Claude Code)"
  status: "applied"

  what_happened: >
    After LL-005, a flotation circuit's concentrate could only be saleable or a bulk
    concentrate for separation. A circuit that floats a waste mineral (e.g., pyrite removed
    to make low-sulphur tailings) had no destination, although it matters for tailings and
    water products.

  correct_approach: >
    A Flotation Circuit's concentrate destination is configuration with three values:
    saleable (to dewatering), bulk (to Concentrate Separation) or waste (to tailings
    management). The 3.2 L2 gateway is 'Concentrate destination?'.

  affects:
    - file: "pillar-models/03-processing-and-beneficiation.md"
      section: "3.2, 3.2.2, 3.2.2.4; Narrative 3.2; Circuit Configuration Variants (sulphide removal row)"
      change_type: "fix"
    - file: "pillar-models/bpmn/03-processing-and-beneficiation/3.2_concentration-flotation.bpmn"
      section: "Concentrate destination gateway"
      change_type: "fix"

  integration_notes: >
    flotation_circuit.concentrate_output gains waste_to:tailings_stream. MP-05 is not a
    custody transfer point for a waste concentrate.

- id: LL-009
  date: 2026-10-26
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Fahim Kanji (with Claude Code)"
  status: "applied"

  what_happened: >
    The LL-005 model chained flotation circuits only in sequence and assumed one fixed
    configuration. Split-feed parallel circuits (e.g., coarse-particle flotation alongside
    conventional) and ore-type campaigns that switch the active configuration were not
    representable.

  correct_approach: >
    Flotation Circuit instances may run in parallel on split feeds, each with its own
    feed_source, and the active configuration may change by ore-type campaign. Both are
    configuration on flotation_circuit (feed_source split_of:stream, operating_mode,
    effective_from, effective_to), not new process groups.

  affects:
    - file: "pillar-models/03-processing-and-beneficiation.md"
      section: "3.2, 3.2.2; Narrative 3.2 note; Circuit Configuration Variants; flotation_circuit entity"
      change_type: "fix"

  integration_notes: >
    No diagram change: the 3.2 L2 diagram shows the sequential loop; parallel and campaign
    instances are documented on the pattern.

- id: LL-010
  date: 2026-10-26
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Fahim Kanji (with Claude Code)"
  status: "applied"

  what_happened: >
    Reagent conditioning sat in two places: 3.2.1 for flotation circuits and inside 3.2.3.1
    (depressant dosing) for Concentrate Separation, so the same business step was described
    twice.

  correct_approach: >
    All reagent conditioning sits in 3.2.1 Reagent Management & Pulp Conditioning; other
    patterns refer to it. 3.2.3.1 is 'Prepare Bulk Concentrate for Separation' (thickening
    via 3.3.1, reagent removal), followed by conditioning through 3.2.1.

  affects:
    - file: "pillar-models/03-processing-and-beneficiation.md"
      section: "3.2.1, 3.2.3, 3.2.3.1, 3.2.3.2; Narrative 3.2"
      change_type: "fix"
    - file: "pillar-models/bpmn/03-processing-and-beneficiation/3.2.3_concentrate-separation.bpmn"
      section: "Narrative step 'Condition pulp for separation (3.2.1)'"
      change_type: "fix"

  integration_notes: >
    The 3.2.3 diagram shows the call to 3.2.1 as a narrative-only step, because a collapsed
    sub-process can be drawn only once in the set.

- id: LL-011
  date: 2026-10-26
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Fahim Kanji (with Claude Code)"
  status: "applied"

  what_happened: >
    Pillar 3 entities hard-coded metals as columns: shift_mass_balance (cu_, zn_, pb_
    produced, recovery and balance error), concentrate_production_record (grade_cu_pct,
    grade_zn_pct, grade_pb_pct, grade_ag_g_t, grade_au_g_t) and osa_grade_telemetry
    (grade_cu_pct ... grade_fe_pct). A Cu-Mo or Cd-penalty site could not be represented
    without new columns — the entity-level form of the LL-005 error (LL-005 integration
    note).

  correct_approach: >
    Metals and analytes are data, not columns. shift_mass_balance keeps the header; per-
    metal results are rows of a new shift_metal_balance entity (one row per shift per site
    per metal). concentrate_production_record holds grades as child rows (analyte, value,
    unit, basis). osa_grade_telemetry grain is per stream per scan per analyte.

  affects:
    - file: "pillar-models/03-processing-and-beneficiation.md"
      section: "Entity Catalog: shift_mass_balance, shift_metal_balance (new), concentrate_production_record, osa_grade_telemetry"
      change_type: "fix"

  integration_notes: >
    Pillar 4 commercial entities (e.g., Cd for Zn concentrate) were not reviewed for the
    same pattern in this session.

- id: LL-012
  date: 2026-10-26
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Fahim Kanji (with Claude Code)"
  status: "applied"

  what_happened: >
    Thickening was described three times with the same steps: concentrate thickening
    (3.3.1), bulk concentrate thickening (inside 3.2.3.1) and tailings thickening (3.3.3.1).
    Overflow water recovery had no step of its own.

  correct_approach: >
    3.3.1 Thickening is a reusable pattern with one instance per thickener duty (saleable
    concentrate, bulk concentrate, tailings): Feed Slurry to Thickener, Dose Flocculant,
    Pump Thickener Underflow (to its configured destination), Recover Thickener Overflow
    Water. Filtration also gains 3.3.2.4 Recover Filtrate Water.

  affects:
    - file: "pillar-models/03-processing-and-beneficiation.md"
      section: "3.3, 3.3.1, 3.3.1.1 to 3.3.1.4, 3.3.2.4; Narrative 3.3; SIPOC 3.3"
      change_type: "fix"
    - file: "pillar-models/bpmn/03-processing-and-beneficiation/"
      section: "3.3 L2, 3.3.1_thickening, 3.3.2"
      change_type: "fix"

  integration_notes: >
    Old 3.3.3.1 Thicken Tailings is now the tailings duty of 3.3.1. Concentrate Drying &
    Packaging moved from 3.3.4 (2026-10-23, never committed) to 3.3.3.

- id: LL-013
  date: 2026-10-26
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Fahim Kanji (with Claude Code)"
  status: "applied"

  what_happened: >
    Pillar 4 named each site's transport mode inside the 4.2.2 description and framed slurry
    pipeline transport as 'an Antamina-specific requirement' (G1), although it is a
    transport mode any site can configure (QB's 2019 drawing also shows a concentrate
    pipeline).

  correct_approach: >
    Transport mode (road, rail, slurry pipeline) is configuration. Site modes belong in the
    variants table, marked indicative and confirmed in each overlay; entity variants for
    pipeline transport apply wherever the mode is configured.

  affects:
    - file: "pillar-models/04-logistics-and-outbound.md"
      section: "4.2.2 description; variants 4.2.2 Transport Mode; G1"
      change_type: "fix"

  integration_notes: >
    The 4.2.2 L4 steps still describe road and rail only; decomposing transport as a pattern
    with modes is LL-018 (open). Pillar 4 says QB uses road haul; this conflicts with QB
    evidence and is flagged for confirmation, not changed.

- id: LL-014
  date: 2026-10-26
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Fahim Kanji (with Claude Code)"
  status: "applied"

  what_happened: >
    Pillar 3 covered tailings with one thin L3 (3.3.3, four L4 steps) and treated water
    management as out of scope. The QB Water-and-Tailings product needed tailings transport,
    classification, deposition, embankment construction, storage and safety monitoring,
    makeup water, reclaim, seepage, process water and the site water balance — all generic
    to any site with a tailings facility and a water balance, so they belong in the pillar,
    not in a product-specific model.

  correct_approach: >
    Pillar 3 has two generic L2 areas: 3.5 Tailings Management (3.5.1 Transport &
    Distribution, 3.5.2 Classification [conditional], 3.5.3 Deposition, 3.5.4 Embankment
    Construction, 3.5.5 Facility Storage & Safety Monitoring) and 3.6 Water Management
    (3.6.1 Makeup Water Supply, 3.6.2 Reclaim Water, 3.6.3 Seepage & Drainage Collection,
    3.6.4 Process Water Supply & Distribution, 3.6.5 Site Water Balance & Reconciliation).
    Facility and water-system differences are configuration (tailings_facility,
    water_system). Tailings and water measurement roles TP-01 to TP-05 and WP-01 to WP-11.

  affects:
    - file: "pillar-models/03-processing-and-beneficiation.md"
      section: "Overview; 3.5; 3.6; TP / WP roles and node maps; SIPOC 3.5, 3.6; Entity Catalog (tailings and water entities); Interaction maps; Narratives 3.5, 3.6; variants; standard alignment; completeness; gaps G4, G6, G7; cross-pillar"
      change_type: "addition"
    - file: "pillar-models/00-cross-reference-and-summary.md"
      section: "Pillar 3 summary, flow box, boundaries, statistics"
      change_type: "fix"
    - file: "pillar-models/bpmn/03-processing-and-beneficiation/"
      section: "3.5 and 3.6 L2 and L3 diagrams; L1; README"
      change_type: "addition"
    - file: "BPMN-generator/03-processing-bpmn-spec.md"
      section: "P3_L2_TSF, P3_L2_WAT"
      change_type: "addition"

  integration_notes: >
    Confirmed by the modeler (decision 2026-10-26). Old 3.3.3 rows map to 3.3.1 [tailings],
    3.5.1.1, 3.5.3.1, 3.5.5.1 and 3.6.2.1 (Revision Notes). Pillar 2 (mine dewatering) is
    out of scope for this revision; see LL-017.

- id: LL-015
  date: 2026-10-26
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Fahim Kanji (with Claude Code)"
  status: "applied"

  what_happened: >
    With process groups generic (LL-005, LL-006), a site's configuration — which optional
    groups run, which pattern instances, in what order, with what site names and measurement
    points — had no home in the overlay. site_overrides records entity field differences,
    not process configuration.

  correct_approach: >
    beam-overlay-schema.yaml has Section 1A process_configuration: one entry per site per
    pillar group or pattern instance, keyed to unchanged pillar IDs, with enabled, sequence,
    feed_from, outputs_to, parameters, steps_not_applicable, site_terms, measurement_points
    (role to site reference), evidence class and status. validate-overlay checks it.

  affects:
    - file: "templates/beam-overlay-schema.yaml"
      section: "Section 1A"
      change_type: "addition"
    - file: ".claude/commands/validate-overlay.md"
      section: "Process configuration checks"
      change_type: "addition"
    - file: "CLAUDE.md"
      section: "PROCESS GROUPS ARE GENERIC"
      change_type: "clarification"

  integration_notes: >
    templates/beam-workshop.md has uncommitted edits by the modeler and was not changed;
    Section D (site variants) should elicit process_configuration — apply when that file is
    next edited.

- id: LL-016
  date: 2026-10-26
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Claude Code"
  status: "open"

  what_happened: >
    Filtered tailings (dry stacking) need a filtration step for tailings. 3.3.2 is written
    as Concentrate Filtration, so a filtered-tailings facility has no generic filtration
    step.

  correct_approach: >
    Generalise 3.3.2 into a Filtration pattern with concentrate and tailings duties (as for
    Thickening), or add a tailings filtration duty, when a site needs it.

  affects:
    - file: "pillar-models/03-processing-and-beneficiation.md"
      section: "3.3.2; 3.5.3 (filtered deposition)"
      change_type: "addition"

  integration_notes: >
    Pillar gap G6.

- id: LL-017
  date: 2026-10-26
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Claude Code"
  status: "open"

  what_happened: >
    Mine dewatering (Pillar 2, 2.3.2) is a water input to the site water balance, but Pillar
    2 does not connect to 3.6. The modeler placed Pillar 2 out of scope for the 2026-10-26
    revision.

  correct_approach: >
    In a Pillar 2 revision, link 2.3.2 Pit Dewatering outputs to 3.6 as a makeup or process
    water source (water_transfer_record from a dewatering water_system), with WP roles.

  affects:
    - file: "pillar-models/02-mining-operations-extraction.md"
      section: "2.3.2 Pit Dewatering"
      change_type: "addition"
    - file: "pillar-models/03-processing-and-beneficiation.md"
      section: "3.6 (boundary note)"
      change_type: "clarification"

  integration_notes: >
    Pillar gap G7.

- id: LL-018
  date: 2026-10-26
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Claude Code"
  status: "applied"

  what_happened: >
    Pillar 4 4.2.2 'Road/Rail Transport' has L4 steps for trucks and wagons only; slurry
    pipeline transport is now recognised as a configured mode (LL-013) but has no steps.

  correct_approach: >
    Decompose inland transport as a generic pattern with road, rail and pipeline modes,
    keeping site modes in the variants table and the overlay.

  affects:
    - file: "pillar-models/04-logistics-and-outbound.md"
      section: "4.2.2 and its L4 rows"
      change_type: "fix"

  integration_notes: >
    Needs explicit instruction before Pillar 4 is restructured.

```

```yaml
- id: LL-019
  date: 2026-10-26
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Claude Code"
  status: "open"

  what_happened: >
    Pillar 4 commercial entities hard-code metals as columns, as Pillar 3 did before
    LL-011: concentrate_inventory_record and dispatch_lot_record (grade_cu_pct,
    grade_zn_pct, grade_pb_pct), certificate_of_analysis (grade_cu_pct ... grade_as_pct),
    commercial_invoice (payable_cu_t, payable_zn_t, cu_price_usd, zn_price_usd) and
    smelter_contract (payability_cu_pct, payability_ag_pct). A Mo, Cd-penalty or other
    product needs new columns.

  correct_approach: >
    Hold grades, payable quantities, prices and payability terms per element as child
    rows (element, value, unit, basis), as LL-011 did for Pillar 3.

  affects:
    - file: "pillar-models/04-logistics-and-outbound.md"
      section: "Entity Catalog (concentrate_inventory_record, dispatch_lot_record, certificate_of_analysis, commercial_invoice, smelter_contract)"
      change_type: "fix"

  integration_notes: >
    Found while applying LL-018 on 2026-10-26; not applied — outside the transport scope
    the modeler asked for.
```

```yaml
- id: LL-020
  date: 2026-10-26
  session: "ad-hoc"
  product: "programme-wide"
  captured_by: "Fahim Kanji (with Claude Code)"
  status: "applied"

  what_happened: >
    For the QB Water-and-Tailings product, site evidence (drawings, a discovery brief) was
    read and a configuration preview written ad hoc. No command, template, README or
    CLAUDE.md rule described where evidence goes, how it becomes configuration, or whether
    it is committed, so the next product would improvise again. The Copilot instructions
    also listed only the three handoff files as allowed outputs.

  correct_approach: >
    Workshop evidence goes in workshops/[product-name]/inputs/ and is always committed. A
    separate step, `prepare configuration for [product-name]`, runs after entity
    extraction: it reads inputs/ for the in-scope pillar areas and writes
    process-configuration.draft.yaml (evidence register, Section 1A entries with evidence
    class, draft open items, vocabulary candidates, pillar gaps) for analyst review. The
    workshop confirms the draft at Section D.1a into the overlay. Inputs and draft stay in
    Stage 1 as the evidence trail; Stage 2 still receives only the three handoff files.

  affects:
    - file: "CLAUDE.md"
      section: "Relationship to downstream repos; WORKFLOW; prepare configuration; run beam workshop; log session; NEVER DO; commit work"
      change_type: "new_rule"
    - file: ".claude/commands/prepare-configuration.md"
      section: "new command"
      change_type: "addition"
    - file: "templates/process-configuration-draft.yaml"
      section: "new template"
      change_type: "addition"
    - file: ".claude/commands/extract-entities.md; .claude/commands/run-beam-workshop.md; templates/entity-extraction.md; templates/beam-workshop.md"
      section: "inputs and draft handling"
      change_type: "behaviour"
    - file: "workshops/[product-name]/README.md; .github/copilot-instructions.md; .github/prompts/"
      section: "sequence, allowed outputs, prompts"
      change_type: "clarification"

  integration_notes: >
    The modeler chose a separate step (option A) over folding configuration into
    extract-entities, so the draft covers only confirmed scope and can be refreshed when
    evidence arrives later. Pre-existing inconsistency noted, not changed: CLAUDE.md lists
    session-log.md as crossing to Stage 2; workshops/[product-name]/README.md says it stays
    in Stage 1.
```
