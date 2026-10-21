# Applied Learnings — Audit Trail
# standards/applied-learnings.md
#
# Append-only audit trail of all learning entries that have been applied to
# templates, standards, or CLAUDE.md in this repo.
#
# Claude Code: append entries here when `apply learning` or `apply all learnings`
# is issued. Update the corresponding entry in lessons-learned.md to status: applied.

---

## Entry Schema Reference

```yaml
- id: LL-[NNN]
  applied_date: YYYY-MM-DD
  applied_by: "[modeler name | Claude Code]"
  files_modified:
    - "[relative file path]"
  summary: "[one-line description of what was changed and why]"
```

---

## Applied Entries

<!-- Claude Code appends entries here. Do not add entries manually. -->

```yaml
- id: LL-001
  applied_date: 2026-10-21
  applied_by: "Claude Code"
  files_modified:
    - "pillar-models/bpmn/02-mining-operations-extraction/README.md"
  summary: "Added a Naming standard section covering folder, file, pool, task, lane, gateway, event and XML ID patterns, inferred from the existing diagrams."

- id: LL-002
  applied_date: 2026-10-21
  applied_by: "Claude Code"
  files_modified:
    - "pillar-models/bpmn/02-mining-operations-extraction/README.md"
  summary: "Replaced the shortened 2.1.1.2 title with the decomposition title 'Design Hole Layout Parameters'."
```
