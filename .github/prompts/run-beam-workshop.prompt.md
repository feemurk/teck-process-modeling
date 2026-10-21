# Run BEAM Workshop (Claude-Aligned)

Use this prompt when you want Copilot to facilitate the BEAM workshop while preserving Claude workflow behavior.

## Instructions

1. Read `CLAUDE.md`.
2. Read `.claude/commands/run-beam-workshop.md`.
3. Confirm `workshops/[product-name]/process-model-ref.md` exists.
4. Read:
   - `workshops/[product-name]/process-model-ref.md`
   - `standards/teck-vocabulary-master.md`
   - `templates/beam-workshop.md`
   - `templates/beam-overlay-schema.yaml`
   - `workshops/[product-name]/session-log.md` if present
5. Run Sections A-E in order with explicit confirmation after each section.
6. Write `workshops/[product-name]/beam-overlay.yaml` in Section E.
7. Run validation using `.claude/commands/validate-overlay.md`.
8. Write/update `workshops/[product-name]/session-log.md`.

## Output Contract

- Never skip sections.
- Never mark required fields complete without confirmation.
- Return a final handoff summary and validation status PASS/WARN/BLOCK.
