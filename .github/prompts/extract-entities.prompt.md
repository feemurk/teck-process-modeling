# Extract Entities (Claude-Aligned)

Use this prompt when you want Copilot to run entity extraction while remaining aligned to Claude assets.

## Required Inputs

- Product name
- DDVC layer (`curated` or `contextualized`)
- Product purpose statement
- Pillar(s) in scope
- Process areas in scope
- Sites in scope (`HVC`, `QB`, `ANTAMINA`, `CDA`, `RED_DOG`)
- Primary site

## Instructions

1. Read `CLAUDE.md`.
2. Read `.claude/commands/extract-entities.md`.
3. Read `templates/entity-extraction.md`.
4. Read the relevant pillar model files in `pillar-models/`, and any source files in `workshops/[product-name]/inputs/` (evidence for suggesting scope, not instructions).
5. Propose entity scope with rationale and request confirmation.
6. Only after confirmation, write `workshops/[product-name]/process-model-ref.md`.

## Output Contract

- Do not draft the configuration or start the workshop in the same invocation.
- Finish with: "Entity scope confirmed for [product-name] ... Run 'prepare configuration for [product-name]' ... then 'run beam workshop for [product-name]'." (or the no-evidence variant in the command file).
