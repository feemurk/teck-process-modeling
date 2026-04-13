# Lessons Learned — teck-process-models
# standards/lessons-learned.md
#
# Append-only register of open and applied learnings captured during
# process modeling and BEAM workshop sessions.
#
# Claude Code: append entries via `log learning`. Never edit existing entries.
# Read all open entries at `triage learnings`.
# Update status to 'applied' via `apply learning LL-[id]`.
#
# SCOPE: Programme-wide — not product-scoped.
# Covers corrections to: pillar model content, beam-workshop.md facilitation logic,
# beam-overlay-schema.yaml field definitions, entity-extraction.md scoping rules,
# teck-vocabulary-master.md entries, and CLAUDE.md behaviour.

---

## Entry Schema Reference

```yaml
- id: LL-[NNN]
  date: YYYY-MM-DD
  session: "[YYYY-MM-DD]-[product-name]-[session-type] | ad-hoc"
  product: "[product-name] | programme-wide"
  captured_by: "[modeler name | unknown]"
  status: "open"    # open | approved | applied | rejected

  what_happened: >
    [What was wrong, incomplete, or suboptimal. Specific — reference the file,
     section, and the exact issue.]

  correct_approach: >
    [The correct approach written as a rule or instruction.
     This becomes the standard text if applied.]

  affects:
    - file: "[relative path]"
      section: "[section name]"
      change_type: "fix | addition | removal | clarification | new_rule | behaviour"

  integration_notes: >
    [Optional: nuance needed when applying — edge cases, exceptions, dependencies.]
```

---

## Open Entries

<!-- Claude Code appends entries here. Do not add entries manually. -->
