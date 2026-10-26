# Workshop Folder — [product-name]

One folder per data product. It holds the site evidence, the working files that build the
overlay, and the three files that cross the Stage 1 → Stage 2 boundary.

---

## Expected Contents

```
workshops/[product-name]/
├── inputs/                              ← added by the analyst: site evidence (drawings, briefs, registers)
├── process-model-ref.md                 ← extract entities for [product-name]          → Stage 2
├── process-configuration.draft.yaml     ← prepare configuration for [product-name]     (stays here)
├── beam-overlay.yaml                    ← run beam workshop for [product-name]          → Stage 2
└── session-log.md                       ← log session (at every step and workshop close)
```

`inputs/` and the configuration draft are the evidence trail behind the overlay. They are
committed with the workshop files and never handed to Stage 2. Do not edit or delete input
files; add a new file when evidence changes.

## Sequence

| # | Command | Reads | Writes | Gate |
|---|---|---|---|---|
| 0 | *(set up)* add source files to `inputs/` | — | `inputs/*` | Optional — skip if there is no evidence yet |
| 1 | `extract entities for [product-name]` | Pillar entity catalogs; `inputs/` (to suggest scope) | `process-model-ref.md` | Analyst confirms the entity scope |
| 2 | `prepare configuration for [product-name]` | `process-model-ref.md`; in-scope pillar areas; `inputs/` | `process-configuration.draft.yaml` | Analyst reviews the draft; pillar gaps are logged as learnings |
| 3 | `commit work` | Session log | Commit of `inputs/`, ref and draft | `verify git` passes |
| 4 | `run beam workshop for [product-name]` | Ref; draft; vocabulary master | `beam-overlay.yaml` | Every section confirmed; D.1a confirms the draft into Section 1A |
| 5 | `validate overlay for [product-name]` | Overlay; schema; ref | Validation report | PASS or WARN to hand off |
| 6 | `log session` / `commit work` | — | `session-log.md`; commit | — |

Re-run step 2 whenever new evidence arrives — it keeps reviewed entries and reports what
changed. Without evidence, skip step 2: the workshop builds the configuration in the room.

The process model is never copied or adapted into this folder. Site differences are
configuration (`process_configuration` in the draft and the overlay), keyed to unchanged
pillar IDs. A process the pillar lacks becomes a learning proposing a generic pillar
addition (CLAUDE.md, "PROCESS GROUPS ARE GENERIC").

## Stage 2 Handoff

When `validate overlay for [product-name]` returns PASS or WARN status,
copy these two files to the data modeling repo:

```
teck-data-modeling/products/[product-name]/inputs/process-model-ref.md
teck-data-modeling/products/[product-name]/inputs/beam-overlay.yaml
```

The session-log.md stays here for reference and continuity.
The data modeler runs `start session CONCEPTUAL for [product-name]` in teck-data-modeling
and the agent reads both files automatically at session start.
