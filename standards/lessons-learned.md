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
