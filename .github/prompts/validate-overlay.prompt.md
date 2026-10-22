# Validate Overlay (Claude-Aligned)

Use this prompt when you want Copilot to validate a workshop overlay with Claude-equivalent rigor.

## Instructions

1. Read `CLAUDE.md`.
2. Read `.claude/commands/validate-overlay.md`.
3. Read:
   - `workshops/[product-name]/beam-overlay.yaml`
   - `templates/beam-overlay-schema.yaml`
   - `workshops/[product-name]/process-model-ref.md`
   - `standards/teck-vocabulary-master.md`
4. Run all REQUIRED, RECOMMENDED, vocabulary, cross-reference, and open-item checks in command spec order.
5. Produce status:
   - BLOCK for required check failures or unresolved block-stage2 items
   - WARN for recommended check gaps
   - PASS for full compliance

## Output Contract

Return the exact report structure:
- OVERLAY VALIDATION — [product-name]
- Generated timestamp
- Status PASS/WARN/BLOCK
- BLOCKS
- WARNINGS
- PASS checks summary
- Schema version reference
