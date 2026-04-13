# Workshop Folder — [product-name]

This folder is created automatically by `extract entities for [product-name]`.
It holds the three files that cross the Stage 1 → Stage 2 boundary.

---

## Expected Contents

```
workshops/[product-name]/
├── process-model-ref.md    ← produced by: extract entities for [product-name]
├── beam-overlay.yaml       ← produced by: run beam workshop for [product-name]
└── session-log.md          ← produced by: log session (at every workshop close)
```

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
