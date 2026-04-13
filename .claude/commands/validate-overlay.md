# Validate Overlay for [product-name]
# .claude/commands/validate-overlay.md
#
# Validates workshops/[product-name]/beam-overlay.yaml against the schema and standards.
# Produces a structured pass/warn/block report.
# Run automatically at the end of every workshop. Can also be run standalone.

1. Read the following files:
   - `workshops/[product-name]/beam-overlay.yaml`
   - `templates/beam-overlay-schema.yaml`
   - `workshops/[product-name]/process-model-ref.md`
   - `standards/teck-vocabulary-master.md`

2. Run the following checks in order:

   SCHEMA COMPLETENESS CHECKS (REQUIRED fields — BLOCK if status = needs-workshop):
   
   [ ] overlay_status is 'complete' or 'validated'
   [ ] All entities in process-model-ref.md have a corresponding entry in
       beam-overlay.yaml Section 2 (entities)
   [ ] Per entity:
       [ ] natural_key.status is not 'needs-workshop'
       [ ] natural_key.source_system is populated
       [ ] scd_status is not 'needs-workshop'
       [ ] domain_owner.status is not 'needs-workshop'
       [ ] At least one source_system entry with in_raw_layer populated
   [ ] Per transactional entity:
       [ ] At least one measure entry in event_canvas with status 'confirmed'
       [ ] grain_status is 'confirmed'
       [ ] grain_statement is not empty
   
   SCHEMA COMPLETENESS CHECKS (RECOMMENDED fields — WARN if missing):
   
   [ ] workshop_participants is populated (minimum 1 entry)
   [ ] Per entity: source_systems[].raw_schema_path is populated if in_raw_layer = yes
   [ ] Per entity: scd_rationale is not empty
   [ ] Per entity: domain_owner.contact is populated
   [ ] Per transactional entity: measure.source_field is populated for each measure
   [ ] Per transactional entity with delay codes: tum_classification_rules is populated
   [ ] Per entity with sites_in_scope > 1: site_overrides is populated or explicitly
       noted as 'no variants confirmed'
   
   VOCABULARY CHECKS:
   
   [ ] All source_system names used in the overlay match entries in
       teck-vocabulary-master.md system_names section (WARN if not found)
   [ ] All reason codes in reason_code_vocabulary have a standard_mapping entry (WARN if not)
   
   CROSS-REFERENCE CHECKS:
   
   [ ] Every entity in beam-overlay.yaml exists in process-model-ref.md
       (flag any overlay entities not in the process model ref as unexpected)
   [ ] The product_name in the overlay matches the folder name
   [ ] The ddvc_layer in the overlay matches the declaration in process-model-ref.md
   
   OPEN ITEMS ASSESSMENT:
   
   [ ] For each open_item with gate_impact = 'block-stage2':
       Flag as a BLOCK if status is not 'resolved'
   [ ] For each open_item with gate_impact = 'warn-stage2':
       Flag as a WARN if status is not 'resolved'

3. Determine overall status:
   - BLOCK: any REQUIRED field check failed, or any open_item with gate_impact = 'block-stage2'
     is not resolved
   - WARN: all REQUIRED checks pass, but one or more RECOMMENDED checks failed or warn-stage2
     open items exist
   - PASS: all REQUIRED and RECOMMENDED checks pass; all block-stage2 open items resolved

4. Produce the validation report:

```
OVERLAY VALIDATION — [product-name]
Generated: [YYYY-MM-DD HH:MM]
Status: PASS | WARN ([N] items) | BLOCK ([N] items)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BLOCKS — must resolve before Stage 2 ([N]):
  [entity.field.path]: [what is missing or wrong and why it blocks]
  [entity.field.path]: [description]

WARNINGS — should resolve; will appear as Stage 2 open items ([N]):
  [entity.field.path]: [what is missing and what risk it creates]
  [entity.field.path]: [description]

PASS ([N] checks):
  [N] required fields: all populated and confirmed
  [N] entities: all accounted for from process-model-ref.md
  [N] site variants: documented or confirmed as none
  [N] open items: all resolved or assessed as warn-only

SCHEMA VERSION: templates/beam-overlay-schema.yaml
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

5. If status is PASS:
   "This overlay is ready for Stage 2. Copy the following files to
   teck-data-modeling/products/[product-name]/inputs/:
   - workshops/[product-name]/process-model-ref.md
   - workshops/[product-name]/beam-overlay.yaml"

6. If status is WARN:
   "This overlay can proceed to Stage 2, but [N] items will be flagged as open
   items in the data modeling session. The data modeler will need to resolve them
   before Gate 1 can be cleared in teck-data-modeling."

7. If status is BLOCK:
   "Stage 2 cannot proceed until the [N] blocking items are resolved.
   Options:
   1. Schedule a follow-up workshop session to address the blocked items
   2. Remove the blocked entities from scope for this iteration
   3. Mark them as 'needs-workshop' explicitly in the overlay and proceed to Stage 2
      with those entities flagged as out-of-scope for the first iteration"
