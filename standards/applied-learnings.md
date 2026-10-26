# Applied Learnings — Audit Trail
# standards/applied-learnings.md
#
# Append-only audit trail of all learning entries that have been applied to
# templates, standards, or CLAUDE.md in this repo.
#
# Claude Code: append entries here when `apply learning` or `apply all learnings`
# is issued. Update the corresponding entry in lessons-learned.md to status: applied.

---

## Entry Schema Reference

```yaml
- id: LL-[NNN]
  applied_date: YYYY-MM-DD
  applied_by: "[modeler name | Claude Code]"
  files_modified:
    - "[relative file path]"
  summary: "[one-line description of what was changed and why]"
```

---

## Applied Entries

<!-- Claude Code appends entries here. Do not add entries manually. -->

```yaml
- id: LL-001
  applied_date: 2026-10-21
  applied_by: "Claude Code"
  files_modified:
    - "pillar-models/bpmn/02-mining-operations-extraction/README.md"
  summary: "Added a Naming standard section covering folder, file, pool, task, lane, gateway, event and XML ID patterns, inferred from the existing diagrams."

- id: LL-002
  applied_date: 2026-10-21
  applied_by: "Claude Code"
  files_modified:
    - "pillar-models/bpmn/02-mining-operations-extraction/README.md"
  summary: "Replaced the shortened 2.1.1.2 title with the decomposition title 'Design Hole Layout Parameters'."
```

```yaml
- id: LL-005
  applied_date: 2026-10-23
  applied_by: "Claude Code"
  files_modified:
    - "pillar-models/03-processing-and-beneficiation.md"
    - "pillar-models/00-cross-reference-and-summary.md"
    - "pillar-models/bpmn/03-processing-and-beneficiation/ (3.2 pattern diagrams, 3.3, 3.3.4, L1, README; Cu, Zn and Pb circuit diagrams retired)"
    - "pillar-models/bpmn/tools/bpmn_build.py (new shared engine)"
    - "pillar-models/bpmn/tools/build_pillar3.py (new)"
    - "BPMN-generator/03-processing-and-beneficiation.md (mirror)"
    - "BPMN-generator/00-cross-reference-and-summary.md (mirror)"
    - "BPMN-generator/03-processing-bpmn-spec.md"
    - "standards/teck-vocabulary-master.md"
  summary: "Replaced commodity-specific flotation process groups with two reusable patterns (Flotation Circuit, Concentrate Separation), added conditional Concentrate Drying & Packaging, moved mineral and site differences to configuration (flotation_circuit; Circuit Configuration Variants), made measurement points role-based."

- id: LL-006
  applied_date: 2026-10-23
  applied_by: "Claude Code"
  files_modified:
    - "CLAUDE.md"
  summary: "Added the rule that product and site adaptations keep pillar process groups unchanged and record site specifics as configuration in the overlay."

- id: LL-007
  applied_date: 2026-10-23
  applied_by: "Claude Code"
  files_modified:
    - "pillar-models/03-processing-and-beneficiation.md"
  summary: "Escaped pipes inside P754 annotations and added the missing Primary Actor(s) cell to 3.3.3.2."
```

```yaml
- id: LL-008
  applied_date: 2026-10-26
  applied_by: "Claude Code"
  files_modified:
    - "pillar-models/03-processing-and-beneficiation.md"
    - "pillar-models/bpmn/03-processing-and-beneficiation/3.2_concentration-flotation.bpmn"
  summary: "Concentrate destination is saleable, bulk or waste; waste concentrates go to tailings management."

- id: LL-009
  applied_date: 2026-10-26
  applied_by: "Claude Code"
  files_modified:
    - "pillar-models/03-processing-and-beneficiation.md"
  summary: "Flotation Circuit instances may run in parallel on split feeds and change by ore-type campaign; configuration on flotation_circuit."

- id: LL-010
  applied_date: 2026-10-26
  applied_by: "Claude Code"
  files_modified:
    - "pillar-models/03-processing-and-beneficiation.md"
    - "pillar-models/bpmn/03-processing-and-beneficiation/3.2.3_concentrate-separation.bpmn"
  summary: "All reagent conditioning sits in 3.2.1; 3.2.3.1 renamed Prepare Bulk Concentrate for Separation."

- id: LL-011
  applied_date: 2026-10-26
  applied_by: "Claude Code"
  files_modified:
    - "pillar-models/03-processing-and-beneficiation.md"
  summary: "Metals held as data: shift_metal_balance added; grade columns removed from shift_mass_balance, concentrate_production_record and osa_grade_telemetry."

- id: LL-012
  applied_date: 2026-10-26
  applied_by: "Claude Code"
  files_modified:
    - "pillar-models/03-processing-and-beneficiation.md"
    - "pillar-models/bpmn/03-processing-and-beneficiation/ (3.3, 3.3.1_thickening, 3.3.2, 3.3.3)"
  summary: "3.3.1 Thickening is a pattern for concentrate, bulk and tailings duties with overflow recovery; 3.3.2.4 Recover Filtrate Water added; drying and packaging renumbered 3.3.3."

- id: LL-013
  applied_date: 2026-10-26
  applied_by: "Claude Code"
  files_modified:
    - "pillar-models/04-logistics-and-outbound.md"
    - "BPMN-generator/04-logistics-and-outbound.md (mirror)"
  summary: "Transport mode is configuration; pipeline gap G1 made generic; QB transport mode flagged for confirmation."

- id: LL-014
  applied_date: 2026-10-26
  applied_by: "Claude Code"
  files_modified:
    - "pillar-models/03-processing-and-beneficiation.md"
    - "pillar-models/00-cross-reference-and-summary.md"
    - "pillar-models/bpmn/03-processing-and-beneficiation/ (3.5, 3.6 and their L3; L1; README)"
    - "pillar-models/bpmn/tools/build_pillar3.py"
    - "BPMN-generator/03-processing-bpmn-spec.md"
    - "BPMN-generator/00-cross-reference-and-summary.md, 03-processing-and-beneficiation.md (mirrors)"
    - "standards/teck-vocabulary-master.md"
  summary: "Generic 3.5 Tailings Management and 3.6 Water Management added to Pillar 3, absorbing old 3.3.3; TP and WP measurement roles; tailings and water entities."

- id: LL-015
  applied_date: 2026-10-26
  applied_by: "Claude Code"
  files_modified:
    - "templates/beam-overlay-schema.yaml"
    - ".claude/commands/validate-overlay.md"
    - "CLAUDE.md"
  summary: "Overlay Section 1A process_configuration records each site's configuration of generic process groups; validate-overlay checks it."
```

```yaml
- id: LL-018
  applied_date: 2026-10-26
  applied_by: "Claude Code"
  files_modified:
    - "pillar-models/04-logistics-and-outbound.md"
    - "pillar-models/00-cross-reference-and-summary.md"
    - "pillar-models/diagrams/L0-value-chain/ (register, SVG, PNG, draw.io)"
    - "BPMN-generator/04-logistics-bpmn-spec.md"
    - "BPMN-generator/04-logistics-and-outbound.md, 00-cross-reference-and-summary.md (mirrors)"
  summary: "Transport made generic: 4.2 Concentrate Transport with Dispatch Measurement & Documentation and a Transport Leg pattern for road, rail, slurry pipeline and sea; transport_leg and transport_dispatch_record defined; port receipt and vessel loading (direct or lightering) mode-agnostic; L0 map updated with 4.2 and Pillar 3 areas 3.5, 3.6."
```

```yaml
- id: LL-015
  applied_date: 2026-10-26
  applied_by: "Claude Code"
  files_modified:
    - "templates/beam-workshop.md"
  summary: "Follow-up: Section D gains D.1a Process configuration (elicit and confirm overlay Section 1A, with coaching against treating configuration as a new process); D.3 summary and E.1 self-check cover it."
```

```yaml
- id: LL-020
  applied_date: 2026-10-26
  applied_by: "Claude Code"
  files_modified:
    - "CLAUDE.md"
    - ".claude/commands/prepare-configuration.md (new)"
    - "templates/process-configuration-draft.yaml (new)"
    - ".claude/commands/extract-entities.md"
    - ".claude/commands/run-beam-workshop.md"
    - "templates/entity-extraction.md"
    - "templates/beam-workshop.md"
    - "workshops/[product-name]/README.md"
    - ".github/copilot-instructions.md"
    - ".github/prompts/prepare-configuration.prompt.md (new), extract-entities.prompt.md, run-beam-workshop.prompt.md"
  summary: "Evidence-to-configuration step: inputs/ committed as evidence; prepare configuration drafts process-configuration.draft.yaml after entity extraction; the workshop confirms it at D.1a."
```
