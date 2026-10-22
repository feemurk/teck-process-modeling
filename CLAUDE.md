# CLAUDE.md — Teck Process Models
# Governing instructions for Claude Code in this repository.
# Read this file in full before responding to any request.
# All outputs must comply with the standards and workflow defined here.

---

## PURPOSE OF THIS REPO

This repository is **Stage 1** of the Teck data product pipeline. Its single purpose is to
produce `beam-overlay.yaml` files that `teck-data-modeling` (Stage 2) consumes as structured
inputs to data product design sessions.

It does this by combining two things:
1. **Industry-standard process models** (`pillar-models/`) — the authoritative decomposition
   of the open-pit mining value chain, pre-answering ~60% of the BEAM workshop discovery
   questions for every entity across all six pillars.
2. **AI-facilitated BEAM workshops** — structured dialogues that elicit the Teck-specific
   40% that the industry standard cannot answer: source system verification, natural key
   confirmation, site variants, owner names, business rule arbitration, and reason code
   vocabularies.

**This repo does not produce:**
- Data models (DDL, logical models, physical specs)
- ODCS contracts
- dbt models or DLT pipeline specs
- KPI definitions or metric calculations
- Anything that belongs to Stage 2 or Stage 3

---

## RELATIONSHIP TO DOWNSTREAM REPOS

```
teck-process-modeling (this repo)
        │
        │  workshops/[product-name]/process-model-ref.md
        │  workshops/[product-name]/beam-overlay.yaml
        │
        ▼
teck-data-modeling (Stage 2)
        │
        │  products/[product-name]/contract/odcs-contract.yaml
        │
        ▼
teck-dbt / teck-dlt (Stage 3)
```

The three files that cross the Stage 1 → Stage 2 boundary are:
1. `workshops/[product-name]/process-model-ref.md` — scoped entity extract from the pillar model
2. `workshops/[product-name]/beam-overlay.yaml` — Teck-specific adaptations
3. `workshops/[product-name]/session-log.md` — workshop record for continuity

Nothing else. Stage 2 reads these three files and nothing else from this repo.

---

## PILLAR MODEL AUTHORITY

The pillar models in `pillar-models/` are **authoritative and stable**. They represent
industry-standard process decompositions validated against ISA-95, AMIRA P754, GMG TUM,
GMG Mobile Equipment Open Data, ISO 14224, ISO 45001, and ICMM frameworks.

**Do not modify pillar model content without explicit instruction.**

When a workshop reveals that Teck's actual practice deviates from the industry-standard
model, that deviation is captured in `beam-overlay.yaml` as an `override` entry — it is
not applied back to the pillar model. The pillar model remains the industry standard.
Teck-specific adaptations live in the overlay.

The one exception: when the industry-standard model is **wrong** — not just different from
Teck practice, but factually incorrect about the standard itself. Use `CORRECTION:` to
flag this; it will be captured via `log learning` and reviewed before being applied.

---

## PILLAR MODEL INVENTORY

| File | Pillar | Status |
|------|--------|--------|
| `pillar-models/01-mine-planning-and-scheduling.md` | Mine Planning & Scheduling | Complete |
| `pillar-models/02-mining-operations-extraction.md` | Mining Operations (Extraction) | Complete |
| `pillar-models/03-processing-and-beneficiation.md` | Processing & Beneficiation | Complete |
| `pillar-models/04-logistics-and-outbound.md` | Logistics & Outbound Supply Chain | Complete |
| `pillar-models/05-maintenance-and-reliability.md` | Maintenance & Reliability | Complete |
| `pillar-models/06-health-and-safety.md` | Health & Safety | Complete |
| `pillar-models/00-cross-reference-and-summary.md` | Cross-Reference & Summary | Complete |

---

## TWO-COMMAND WORKFLOW

Every product scope goes through exactly two commands in sequence:

```
1. extract-entities     →  produces process-model-ref.md
2. run-beam-workshop    →  produces beam-overlay.yaml
```

A third command validates the overlay before handoff to Stage 2:

```
3. validate-overlay     →  pass / warn / block report
```

**Do not begin a workshop without a confirmed `process-model-ref.md`.**
**Do not hand off to Stage 2 without a passing `validate-overlay` report.**

---

## WORKSHOP SESSION COMMANDS

### `extract entities for [product-name]`

Scopes the entity list for a new product. See `.claude/commands/extract-entities.md`.

When this command is issued:
1. Ask for: product name, pillar(s) in scope, process area(s) in scope, and a one-sentence
   statement of the product's purpose (e.g., "Canonical mobile equipment and haul cycle data
   supporting fleet availability analytics at HVC").
2. Read the relevant pillar model(s) — specifically the Entity Catalog section.
3. Propose a scoped entity list with rationale for inclusion or exclusion.
4. Present the proposed scope to the user for confirmation. Do not write the file
   until confirmed.
5. On confirmation: write `workshops/[product-name]/process-model-ref.md`.
6. Confirm: `"Entity scope confirmed. process-model-ref.md written. Run 'run beam workshop
   for [product-name]' to begin the workshop."`

**Do not include entities that belong to a different DDVC layer than the product being scoped.**
Curated product → Curated-layer entities only. Contextualized entities are not in scope
for a curated product workshop.

---

### `run beam workshop for [product-name]`

Runs the AI-facilitated BEAM workshop. See `templates/beam-workshop.md` for full
facilitation logic, section-by-section elicitation protocol, and inline stakeholder
coaching guidance.

When this command is issued:
1. Confirm `workshops/[product-name]/process-model-ref.md` exists. If not, redirect:
   `"Run 'extract entities for [product-name]' first."`
2. Read `process-model-ref.md` in full.
3. Read `standards/teck-vocabulary-master.md` — use it to align workshop language to
   confirmed Teck terminology.
4. Run the five workshop sections per `templates/beam-workshop.md`.
5. At the end of each section, produce a structured summary and ask for confirmation
   before proceeding.
6. At Section E (validation and output), produce `beam-overlay.yaml` using the schema
   in `templates/beam-overlay-schema.yaml`.
7. Run `validate-overlay` automatically before declaring the workshop complete.
8. Write `workshops/[product-name]/session-log.md` via `log session`.

**Never skip a section.** If a stakeholder is not available for a section, park it as an
open item and proceed to the next section where information is available. Do not produce
`beam-overlay.yaml` with unpopulated required fields — use `status: needs-workshop` to
mark sections where elicitation is incomplete.

---

### `validate overlay for [product-name]`

Validates `workshops/[product-name]/beam-overlay.yaml` against the schema and standards.
See `.claude/commands/validate-overlay.md`.

When this command is issued:
1. Read `workshops/[product-name]/beam-overlay.yaml`.
2. Read `templates/beam-overlay-schema.yaml` — check every required field.
3. Read `standards/teck-vocabulary-master.md` — flag any terms in the overlay that
   conflict with confirmed vocabulary.
4. Read `workshops/[product-name]/process-model-ref.md` — check that every entity in
   the process-model-ref is represented in the overlay.
5. Produce a validation report:

```
OVERLAY VALIDATION — [product-name]
Status: PASS | WARN | BLOCK

BLOCKS (must resolve before Stage 2):
  - [field path]: [reason]

WARNINGS (should resolve; Stage 2 will flag as open items):
  - [field path]: [reason]

PASS:
  [N] required fields populated
  [N] entities validated
  [N] site variants documented
```

6. A `BLOCK` status means Stage 2 cannot proceed. A `WARN` status means Stage 2 can
   proceed but will carry open items. A `PASS` means the overlay is ready for handoff.

---

### `log session`

Writes a session log entry to `workshops/[product-name]/session-log.md`.

Entry schema:

```yaml
- id: "[YYYY-MM-DD]-[product-name]-[WORKSHOP-SECTION]"
  date: "YYYY-MM-DD"
  product: "[product-name]"
  session_type: "ENTITY-EXTRACTION | BEAM-WORKSHOP | VALIDATION"
  participants: []
  sections_completed: []
  sections_parked: []
  open_items: []
  overlay_status: "not-started | in-progress | complete | validated"
  next_session_plan: ""
```

---

### `log learning`

Appends a structured entry to `standards/lessons-learned.md`.
Same schema as `teck-data-modeling`. Assign sequential LL-[NNN] IDs.
Confirm: `"Logged as LL-[id]. Status: open. Type 'triage learnings' to review."`

---

### `triage learnings`

Reads all `status: open` entries in `standards/lessons-learned.md`.
Same triage report format as `teck-data-modeling`.
Scan workshop session logs for uncaptured `CORRECTION:` markers.

---

### `apply learning LL-[id]` / `apply all learnings`

Applies learning entries to their target files.
Same protocol as `teck-data-modeling`.
Never modify pillar model files without explicit user confirmation that the correction
applies to the industry standard (not just Teck practice).

---

## CORRECTION: TRIGGER WORD

Same mechanism as `teck-data-modeling`. During any session, prefix a message with
`CORRECTION:` to flag that Claude Code produced something wrong or incomplete.

When `CORRECTION:` is received:
1. Acknowledge and apply to current work.
2. Prompt: `"Should I log this as a learning? Type 'log learning' to capture it."`
3. Ensure it appears in the session log's open items.

---

## NEVER DO

- Modify pillar model content without explicit instruction and a `CORRECTION:` justification
- Produce `beam-overlay.yaml` with required fields empty rather than marked `needs-workshop`
- Skip the entity extraction step and go directly to workshop
- Allow an overlay with `BLOCK` status to be handed to Stage 2
- Use medallion architecture terminology (bronze/silver/gold)
- Put KPI definitions or metric calculations in the overlay — those belong in Stage 2
- Accept a stakeholder answer that would embed business logic in the Curated layer
  (flag it, document it as a Contextualized concern, park it as an open item)
- Conflate Teck-specific process variants with errors in the industry-standard model

---

## VOCABULARY DISCIPLINE

Always read `standards/teck-vocabulary-master.md` before beginning any workshop.

When a stakeholder uses a term not in the vocabulary master, either:
- Match it to a confirmed canonical term and note the synonym, or
- Flag it as a new term candidate and ask for a definition before proceeding

Do not assume a term means what it sounds like. Mining terminology is highly
site-specific. "Payload" at Red Dog has specific regulatory implications that
"payload" at HVC does not.

---

## GIT WORKFLOW

### `verify git`

Expected values:
- `user.email` → `feemurk@gmail.com`
- `remote origin` → `https://github.com/feemurk/teck-process-modeling.git`

Block all commits if either check fails.

### `commit work`

Same protocol as `teck-data-modeling`. Read session log to generate commit message.
Format: `[session-type] [product-name]: [one-line summary]`
Example: `BEAM-WORKSHOP MFD-Curated: complete entity sign-off and event canvas`
