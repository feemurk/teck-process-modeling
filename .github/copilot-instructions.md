# Copilot Instructions for teck-process-modeling

This repository uses Claude workflow assets as the governing source of truth.
GitHub Copilot is a secondary assistant and must follow these rules.

## Assistant Priority Model

1. Primary workflow authority: `CLAUDE.md`.
2. Command-level authority: `.claude/commands/*.md`.
3. Template/schema authority: `templates/*.md` and `templates/*.yaml`.
4. Vocabulary and standards authority: `standards/*.md`.

If Copilot guidance conflicts with any file above, the files above win.

## Mandatory Read Order Before Responding

Before answering any request about process modeling workflows, read in this order:

1. `CLAUDE.md`
2. Relevant command file(s) in `.claude/commands/`
3. Relevant template/schema in `templates/`
4. Relevant standards in `standards/`
5. Existing workshop files under `workshops/[product-name]/` when scoped to a product

If a required file is missing, say exactly what is missing and stop.
Do not invent defaults that are not present in these assets.

## Scope Guardrails

This repo is Stage 1 only.
Do not generate Stage 2 or Stage 3 outputs in this repository.

Allowed outputs here:
- `workshops/[product-name]/process-model-ref.md`
- `workshops/[product-name]/beam-overlay.yaml`
- `workshops/[product-name]/session-log.md`

Disallowed outputs here:
- ODCS contracts
- dbt or DLT implementation specs
- physical or logical data models
- KPI calculation artifacts

## Command Mapping for Copilot

When user intent matches the following, apply the associated workflow file exactly:

- "extract entities for [product-name]" -> `.claude/commands/extract-entities.md`
- "run beam workshop for [product-name]" -> `.claude/commands/run-beam-workshop.md`
- "validate overlay for [product-name]" -> `.claude/commands/validate-overlay.md`

Always run command steps in sequence. Do not skip confirmations.

## Behavioral Requirements

- Confirm required prerequisites before any write operation.
- Use explicit section-by-section confirmations during workshop flow.
- Preserve pillar model authority: treat `pillar-models/` as stable unless explicitly told to correct an industry-standard error.
- Capture Teck-specific deviations in overlay overrides, not by editing pillar models.
- Keep process groups generic (CLAUDE.md, "PROCESS GROUPS ARE GENERIC"): never name, split or re-scope a process group by mineral or site, and never delete or renumber pillar process groups for a product; record site specifics as configuration in the overlay.
- Use terminology from `standards/teck-vocabulary-master.md`.
- Flag uncertainties as open items; do not present assumptions as confirmed facts.

## Validation Requirement

Before declaring workshop output complete, run overlay validation against:
- `templates/beam-overlay-schema.yaml`
- `workshops/[product-name]/process-model-ref.md`
- `standards/teck-vocabulary-master.md`

Return PASS, WARN, or BLOCK with concrete blocking paths.

## Handoff Discipline

Only hand off these files to Stage 2 inputs:
- `workshops/[product-name]/process-model-ref.md`
- `workshops/[product-name]/beam-overlay.yaml`
- `workshops/[product-name]/session-log.md`

No other files in this repository are Stage 1 handoff artifacts.
