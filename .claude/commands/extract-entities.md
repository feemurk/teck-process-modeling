# Extract Entities for [product-name]
# .claude/commands/extract-entities.md
#
# Scopes the entity list for a new product and writes process-model-ref.md.
# Run this before `run beam workshop for [product-name]`.

1. Read `templates/entity-extraction.md` in full before proceeding.

2. Collect the required scoping inputs:
   - Product name (must match intended teck-data-modeling folder name)
   - DDVC layer (curated | contextualized)
   - Product purpose statement (one sentence)
   - Pillar(s) in scope
   - Process areas within those pillars
   - Sites in scope (HVC | QB | ANTAMINA | CDA | RED_DOG)
   - Primary site (the canonical reference site for the model)

3. Read the Entity Catalog sections of the specified pillar model(s) from
   `pillar-models/`. Apply the inclusion and exclusion rules in the extraction template.

4. Propose the scoped entity list with rationale. Do not write any files yet.
   Present the proposal and ask for explicit confirmation.

5. On confirmation: write `workshops/[product-name]/process-model-ref.md`
   using the output format defined in `templates/entity-extraction.md`.
   Create the `workshops/[product-name]/` directory if it does not exist.

6. Confirm to the user:
   "Entity scope confirmed for [product-name]. [N] entities extracted from
   [pillar(s)]. process-model-ref.md written to workshops/[product-name]/.
   
   Run 'run beam workshop for [product-name]' to begin the BEAM workshop."

7. Do not proceed to the workshop in the same command invocation.
   The workshop is a separate session that may involve different participants.
