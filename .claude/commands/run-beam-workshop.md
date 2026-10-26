# Run BEAM Workshop for [product-name]
# .claude/commands/run-beam-workshop.md
#
# Runs the AI-facilitated BEAM workshop for an existing product scope.
# Requires process-model-ref.md to exist before running.

1. Confirm that `workshops/[product-name]/process-model-ref.md` exists.
   If it does not exist, respond:
   "Run 'extract entities for [product-name]' first to define the entity scope.
   The workshop cannot proceed without a confirmed process-model-ref.md."

   If `workshops/[product-name]/inputs/` contains files but there is no
   `process-configuration.draft.yaml`, or the draft has `draft_status: draft` (not yet
   reviewed), respond:
   "There is evidence in inputs/ that has not been drafted and reviewed. Run 'prepare
   configuration for [product-name]' first so Section D.1a starts from the evidence."
   Proceed without a draft only if inputs/ is empty, or the analyst explicitly says to.

2. Read the following files before saying anything to the user:
   - `workshops/[product-name]/process-model-ref.md`
   - `workshops/[product-name]/process-configuration.draft.yaml` (if present)
   - `standards/teck-vocabulary-master.md`
   - `templates/beam-workshop.md`
   - `templates/beam-overlay-schema.yaml`
   
   Also check for a prior session log:
   - `workshops/[product-name]/session-log.md`
   If a prior session log exists, read it and note which sections were completed
   in previous sessions so you do not repeat completed work.

3. Open the workshop per the pre-workshop setup instructions in `templates/beam-workshop.md`.
   State what you have read and what you will focus on.

4. Run the five workshop sections in order:
   A — Process Anchor and Stories
   B — Entity Sign-Off
   C — Event Canvas HOW MANY and WHY
   D — Site Variants
   E — Validation and Overlay Generation

   Follow the facilitation logic and stakeholder coaching guidance in
   `templates/beam-workshop.md` exactly for each section.

5. At the end of each section, produce the structured section summary and
   ask for explicit confirmation before proceeding to the next section.

6. At Section E:
   a. Write `workshops/[product-name]/beam-overlay.yaml` using the schema
      from `templates/beam-overlay-schema.yaml`.
   b. Run the validate-overlay protocol automatically.
   c. Present the validation report.
   d. Write vocabulary additions to `standards/teck-vocabulary-master.md`.
   e. If a configuration draft was used, set its `draft_status: consumed-by-workshop`.
      Leave its entries as they were — the overlay is now the record.
   f. Write the session log via `log session`.
   g. Present the handoff summary.

7. At session end, remind the analyst:
   "Before you close this session, check whether any CORRECTION: messages were
   sent that haven't been logged. Type 'log learning' to capture them.
   Run 'triage learnings' before committing."
