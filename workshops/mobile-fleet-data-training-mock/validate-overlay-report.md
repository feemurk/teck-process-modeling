# validate-overlay report — mobile-fleet-data-training-mock

*Produced per `.claude/commands/validate-overlay.md`. Regenerated after refreshing this
mock against the updated `templates/beam-workshop.md` (new Source/Map entity types) and
`standards/teck-vocabulary-master.md` §3.5 (HVC Minestar/Wenco mastering gap). This file is
not part of the standard three-file Stage 1 handoff set — saved here for training review
since this run had no live workshop session to present the report to interactively.*

```
OVERLAY VALIDATION — mobile-fleet-data-training-mock
Generated: 2026-08-06 (refreshed same day — Source/Map entity types added)
Status: BLOCK (4 items)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BLOCKS — must resolve before Stage 2 (4):

  OI-001 (haul_cycle): queue_dump_start_utc and spot_dump_utc were added during this
  workshop to close an auditability gap, but their existence in FMS is unconfirmed.

  OI-002 (haul_cycle_stage_event): whether this entity has a real FMS source event
  stream, or must be derived from haul_cycle timestamps, is unconfirmed.

  OI-007 (ALL entities): every domain_owner in this overlay is a role-based placeholder —
  no live stakeholder confirmed ownership of any of the 13 entities.

  OI-009 (mobile_equipment, mobile_equipment_source_xref): the governed master file and
  site-steward mapping process this workshop proposed do not exist yet. Every haul_cycle,
  delay_event, and operator_shift_assignment record referencing equipment_id inherits this
  ambiguity until it is built, confirmed, and owned.

WARNINGS — should resolve; will appear as Stage 2 open items (15):

  workshop_participants (Section 1): empty — no live stakeholder session was run.

  entities[equipment_class].site_overrides,
  entities[location].site_overrides,
  entities[haul_cycle_stage_event].site_overrides,
  entities[operator_shift_assignment].site_overrides,
  entities[stockpile_inventory_movement].site_overrides,
  entities[mobile_equipment_source_xref].site_overrides: all empty though sites_in_scope
  has 2 sites (HVC, QB) — not checked either way. (6 items)

  OI-003 (delay_event): work_order_id not enforced on TUM:DT records at source
  (programme Gap XP-01).

  OI-004 (haul_cycle): strut-pressure-to-payload calibration factor undocumented
  (pillar model Known Gap G2).

  OI-005 (shift): shift boundary local-vs-UTC handling by site unresolved programme-wide.

  OI-006 (delay_event): no cross-site delay reason code harmonisation between HVC and QB.

  OI-008 (operator): QB labour agreement/authorization framework vs. HVC unconfirmed.

  OI-010 (haul_cycle): FMS evidently DOES resolve equipment identity operationally today
  (event data attributes to only one row despite duplicate active source rows) — HOW it
  does this is unknown and unrecorded, and the eventual Master/Map governance process must
  either match or deliberately change whatever that implicit behaviour is.

  OI-011 (mobile_equipment): standards/teck-vocabulary-master.md §1 (HVC=Minestar only)
  and §3.5 (HVC=Minestar+Wenco) conflict and have not been reconciled with each other.

  OI-012 (mobile_equipment_source_minestar/wenco): whether QB or other sites have an
  equivalent multi-FMS mastering gap to HVC's is unconfirmed, not confirmed-absent.

PASS:
  0 REQUIRED schema-field failures across 13 entities and 5 event_canvas entries
    (verified mechanically via verify_overlay.py — see this session's tool output)
  13 of 13 entities: accounted for in 1:1 correspondence with process-model-ref.md
  7 of 13 entities: site variants documented (checked-and-cleared or genuinely flagged) —
    mobile_equipment, shift, haul_cycle, delay_event, operator,
    mobile_equipment_source_minestar, mobile_equipment_source_wenco
  0 of 12 open items resolved (all freshly logged — expected for a first pass)

SCHEMA VERSION: templates/beam-overlay-schema.yaml (entity_type now includes
  Source | Map per the update reflected in this refresh)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## What changed from the first pass, and why the block count went up, not down

The refresh added a 4th BLOCK (OI-009) rather than resolving any of the original 3. That's
the correct outcome, not a regression: the Minestar/Wenco mastering gap was **already
present and already blocking** in the first pass — it was simply mis-modeled there.
`mobile_equipment` originally listed a single blended `"FMS (Minestar, Wenco, Modular)"`
source with `key_stability: stable`, `multi_source_key_conflict: false` — which asserted a
confidence about equipment identity that was never actually justified, given
`standards/teck-vocabulary-master.md` §3.5 now confirms HVC runs both systems concurrently
with duplicate, unreconciled "active" rows. The refresh didn't introduce a new problem; it
stopped hiding an existing one behind an incorrect `stable`/`false` pairing.

Two corrections worth flagging explicitly, since a validate-overlay report should surface
its own mistakes as readily as the workshop's:

1. **`mobile_equipment`'s original entry was wrong**, not just incomplete. It's now
   `status: needs-workshop` (escalated from `provisional`) and its natural key changed
   entirely — from `fleet_number` (a source-system field) to `equipment_master_id`
   (a proposed governed surrogate that doesn't exist yet).
2. **`stockpile_inventory_movement`'s `xref_required: true` was a genuine mis-application**
   of the same pattern, caught while fixing `mobile_equipment` for real. It described a
   measurement-reconciliation problem (FMS mass vs. periodic survey volume — pillar model
   Known Gap G5) as if it were an identity-mastering problem. Corrected to `false`; no Map
   entity needed there.

## Remediation paths (per `.claude/commands/validate-overlay.md` step 6)

Unchanged from the first pass — still applies. The realistic path is a follow-up workshop
with named HVC stakeholders, the FMS system owner (for OI-002/OI-010), and whoever is
positioned to actually stand up the site-steward mastering process (OI-009) — that last one
is an organizational commitment, not just a data-modeling question, and is the biggest
genuine gap this refresh surfaced.
