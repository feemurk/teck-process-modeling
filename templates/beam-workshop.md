# BEAM Workshop Facilitation Guide
# templates/beam-workshop.md
#
# This template governs how Claude Code runs an AI-facilitated BEAM workshop.
# It is invoked by the `run beam workshop for [product-name]` command.
#
# DESIGN PRINCIPLES:
# 1. The agent states what it already knows from the process model before asking anything.
#    Every section opens with pre-populated content. Stakeholders confirm, correct, or extend
#    — they do not construct from scratch.
# 2. The agent only asks for what the process model cannot answer.
#    No question that can be answered by reading the pillar model should be asked of a human.
# 3. Stakeholder coaching is embedded inline at the exact moment it is needed.
#    It is contextual, entity-specific, and risk-specific — not generic facilitation advice.
# 4. The agent flags conflicts, ambiguities, and governance escalations explicitly.
#    It does not silently accept answers that will cause downstream problems.
# 5. Every section ends with a structured summary and explicit confirmation request.
#    The agent does not proceed until the current section is confirmed.
#
# Claude Code: follow the five-section structure exactly. Do not skip sections.
# Do not combine sections. Do not proceed past a section until it is confirmed.
# Produce the beam-overlay.yaml at Section E using templates/beam-overlay-schema.yaml.

---

## PRE-WORKSHOP SETUP

Before beginning the workshop, read and internalize:
1. `workshops/[product-name]/process-model-ref.md` — the scoped entity list
2. `standards/teck-vocabulary-master.md` — Teck-specific terminology
3. `templates/beam-overlay-schema.yaml` — the output schema you are producing

Then open with this statement to the room:

> "I've read the process model for [process areas in scope]. I know a lot already —
> I'll show you what I have, and we'll focus our time on the things only you can tell me.
> We have five sections. I'll summarise at the end of each one before we move on.
> The output is a structured file that the data modeling team reads directly — so precision
> here saves significant time downstream."

---

## SECTION A — PROCESS ANCHOR AND STORIES
> Goal: Confirm the business purpose and priority of this product.
> What the process model already answers: the SIPOC, the process anchor statement,
> the entity list, and the primary business events.
> What requires human input: business priorities, Teck story language, confirmed event names.

### A.1 — Present the pre-populated process anchor

Read from `process-model-ref.md` and present:

> "Based on the process model, here is what I understand this product is about:
>
> **Process:** [Process area name from SIPOC]
> **Scope:** [Boundary statement from SIPOC — what it covers and what it excludes]
> **Primary events:** [List of Transactional entities from entity catalog]
> **Key master entities:** [List of Master entities from entity catalog]
>
> Is this the right scope for [product-name]?"

**If the stakeholder says no or adds a significant addition:**
Flag it immediately. If it adds new entities, return to `extract-entities` and rescope
`process-model-ref.md` before continuing. Do not absorb a scope change silently.

---

### A.2 — Business story prioritisation

Present the candidate stories. For each Transactional entity in the entity catalog, propose
a story using this template:

> "As a [role from SIPOC primary actors], I want [what the entity enables]
> so that I can [business decision from entity catalog DDVC layer and description]."

Then ask:

> "Are these the right stories? Are there any you'd add, change, or deprioritise?
> Which one story is the most important to get right first?"

**Stakeholder coaching — when to probe:**
- If the stakeholder names a story that sounds like a report ("I want to see a dashboard of..."):
  Redirect — "That's the output. What business event happens that we need to capture to make
  that dashboard possible? What changes in the real world that we need to record?"
- If the stakeholder names a story that is a KPI or metric ("I want to track utilisation..."):
  Flag — "Utilisation is a calculation that lives in the Contextualized layer. This product
  is the Curated foundation — we need the atomic events it's calculated from. Which events
  generate the data for that calculation?"
- If there is disagreement between two stakeholders about priority:
  Do not resolve it in the room. Log it as an open item with both positions and escalate
  to the named business owner for resolution.

---

### A.3 — Section A confirmation

Produce a structured summary:

```
SECTION A SUMMARY — Process Anchor and Stories

Scope confirmed: [yes | modified — describe change]
Primary business event: [event name]
Stories confirmed: [N]
  Priority 1: [story statement]
  Priority 2: [story statement]
  ...
Open items: [N]
  OI-001: [description] — Owner: [name] — Impact: [block-stage2 | warn]
```

Ask: "Does this accurately capture what we discussed? Shall I proceed to Section B?"

---

## SECTION B — ENTITY SIGN-OFF
> Goal: Confirm SCD policy, natural keys, source systems, and domain ownership per entity.
> What the process model already answers: entity type, business definition, grain,
> key attributes, lifecycle states, relationships, and standard alignment.
> What requires human input: SCD policy decision, natural key source verification,
> source system confirmation (in Raw or not), and domain owner name.

### B.1 — Present the pre-populated entity register

For each entity in `process-model-ref.md`, present:

> "Here is what the process model says about [entity name]:
> - **Type:** [Master | Reference | Transactional | Time-Series]
> - **Business definition:** [From entity catalog]
> - **Grain:** [From entity catalog grain column]
> - **Natural key candidate:** [From entity catalog key attributes]
> - **Likely source system:** [From entity catalog source systems column]
> - **Layer:** [Curated / Contextualized / Both]
>
> Three things I need you to confirm or correct:"

---

### B.2 — SCD policy decision

Ask per entity (Master entities only — skip for Transactional, Time-Series, Reference):

> "For [entity name]: if [key attribute] changes — for example, if a truck is reassigned
> to a different site — does your analysis need to know what the old value was?
> Or is knowing the current value sufficient?"

**Stakeholder coaching — how to elicit the right SCD answer:**

Do not ask "Do you want SCD Type 1 or Type 2?" — most stakeholders don't know what that means
and will say Type 1 by default, which is often wrong.

Instead ask about specific change scenarios using real business language:

For equipment:
> "If a haul truck gets reclassified from 220-tonne class to 150-tonne class mid-year,
> does your availability calculation for last quarter need to use the old class or the new one?"
Expected answer: "the old one" → Type 2.

For operator:
> "If an operator changes crew rotation, does a delay event from last month need to show
> which crew they were on last month, or which crew they're on now?"
Expected answer: "last month's crew" → Type 2.

For location:
> "If a shovel face gets a new bench ID when the pit expands, does historical haul cycle
> data need to show the old bench or the new one?"
This one is genuinely ambiguous — flag it as needing the business owner's call.

**Red flag:** If the stakeholder says Type 1 (overwrite) for an entity that has
`is_current` in its key attributes or changes frequently, flag it:
> "Just to confirm — if we use Type 1, we lose the history of [attribute] changes.
> Your [downstream report or analysis] would then always show the current [attribute],
> even for historical events. Is that the right behaviour?"

---

### B.3 — Natural key source verification

For each entity, ask:

> "The process model identifies [candidate key field] as the natural business key.
> Is this field reliably unique and stable in [source system]?
> Has it ever been recycled, reused, or changed for the same real-world [entity]?"

**Stakeholder coaching — key stability probes:**

For equipment:
> "In Minestar / Wenco — does the fleet number stay with the truck for its entire life,
> or has it ever been reassigned to a different truck when one was scrapped and replaced?"
Expected stable answer: fleet number is fixed to the physical asset. If not — flag as at-risk.

For haul cycle:
> "Does the dispatch system guarantee that a cycle ID is unique across all sites,
> or only within one site? What happens if data is migrated from an old system?"
Common answer: cycle IDs are site-scoped — document `site_id + cycle_id` as the composite key.

For shift:
> "Can two different shifts ever have the same shift code on the same date? For example,
> are there special shift codes for shutdown days or training shifts that might collide?"

**If the stakeholder is uncertain about key stability:**
Do not accept uncertainty. Set `key_stability: at-risk` and escalate to the source system
owner as an open item. A data product with an unreliable surrogate key generation strategy
is a Gate 1 blocker in Stage 2.

---

### B.4 — Source system confirmation

For each entity, ask:

> "Is [source system from process model] the right source for [entity name] at [site]?
> Is it currently ingested into the Raw layer in Unity Catalog?
> If it's in multiple systems — which one is the authority?"

**Stakeholder coaching — multi-source probes:**

If the entity appears in multiple systems (common for equipment, location, operator):
> "You mentioned both [system A] and [system B] have [entity name]. If those two systems
> disagree on [attribute] for the same [entity] — for example, different capacity ratings
> for the same truck — which one wins? Who owns the definition?"

The answer to "who wins" is the MDM authority. If no one can answer, flag as an
`xref_required: true` entity with an open item for MDM strategy.

---

### B.5 — Domain owner confirmation

For each entity:

> "Who owns the business definition of [entity name]? If the definition of [key attribute]
> changes — for example, if the business changes how it classifies equipment — who has
> the authority to approve that change?"

This person becomes the `domain_owner` in the overlay. They must be reachable by name and role.

**Red flag — if the stakeholder says "everyone" or "no one really owns it":**
> "For the data contract to be valid, there must be one person accountable for the
> business definition. That person approves changes. It doesn't mean they do the work —
> it means they're the decision authority. Who is closest to that role?"
Log the answer as `provisional` and flag for business owner confirmation before Gate 1.

---

### B.6 — Section B confirmation

Produce a structured summary per entity:

```
SECTION B SUMMARY — Entity Sign-Off

[Entity name] ([type]):
  Natural key: [field] from [system] — stability: [stable | at-risk | unknown]
  Source system: [name] — in Raw: [yes | no | partial]
  SCD policy: [Type1 | Type2] — confirmed by: [name]
  Domain owner: [name, role] — status: [confirmed | provisional]
  Site overrides: [none | list]
  Open items: [none | OI-xxx list]

[repeat per entity]

Total entities: [N confirmed] | [N provisional] | [N needs-workshop]
```

Ask: "Does this accurately reflect what we agreed? Shall I proceed to Section C?"

---

## SECTION C — EVENT CANVAS HOW MANY AND WHY
> Goal: Capture the measures, reason codes, and classification vocabularies that the
> process model cannot answer — because they require real Teck data, real Teck codes,
> and real Teck business rule decisions.
> This is the highest-value section of the workshop. Allocate the most time here.

### C.1 — Present the pre-populated event skeleton

For each Transactional entity:

> "For [event entity name], here is what the process model tells us:
> - **WHO performs it:** [from SIPOC primary actors]
> - **WHAT triggers it:** [from L4 activity trigger column]
> - **WHEN it completes:** [from lifecycle state transitions]
> - **WHERE it occurs:** [from ISA-95 level and location context]
>
> What I need from you is the HOW MANY and WHY — the actual measurements
> and the classification codes you use to explain why things happen."

---

### C.2 — HOW MANY (Measures)

For each measure candidate identified in the entity catalog key attributes:

> "For [measure name] on [event name]:
> What is the exact field in [source system] that captures this?
> What unit does it come in — and is there any conversion needed?
> Can you add this measure across different [trucks / shifts / sites] to get a total,
> or does adding it give you a meaningless number?"

**Stakeholder coaching — measure elicitation probes:**

**For tonnage measures:**
> "Is this wet tonnes or dry tonnes? Does the source system record the raw reading,
> or does it apply a moisture correction automatically?"
The answer determines the UOM suffix (`_wmt` vs `_dmt`) and whether a business rule
for moisture correction belongs here or in the Contextualized layer.

**For duration / time measures:**
> "Is this stored as a duration (in seconds or minutes) or as two timestamps
> (start and end) that you compute the duration from?
> If it's two timestamps — what happens if one is null? Does that mean the event
> didn't happen, or that it wasn't recorded?"
Null-handling for duration measures is a business rule that must be decided now,
not discovered when the pipeline is running.

**For payload from strut pressure (haul trucks):**
> "The process model notes that payload is estimated from strut pressure, not from
> a certified belt scale. Is there a calibration factor applied, and where does that
> live? Who owns that calibration — is it per-truck, per-class, or site-wide?"
If the answer is "we apply the OEM lookup table" — ask who updates it when a truck
is reconfigured. That person is the business rule owner.

**For count measures:**
> "Is this a natural count (one event = one row, load_count is always 1) or an
> aggregated count that needs to be recalculated from the atomic data?"
If it's always 1 at atomic grain, confirm it and move on. If it's aggregated, it
belongs in the Contextualized layer, not here.

**For percentage or ratio measures:**
> "This is a calculated ratio. Percentages can't be added — you'd need to store the
> numerator and denominator separately and recalculate the percentage at every
> aggregation level. What are the numerator and denominator?"
Example: equipment availability % = (available hours / scheduled hours). Both
components must be atomic measures in the Curated layer.

**Red flag — if a stakeholder proposes a measure that is a ratio:**
> "I want to flag that [measure] is a non-additive ratio — it can't be summed. If we
> store it as a column, analysts will sum it and get wrong answers. The standard approach
> is to store [numerator] and [denominator] separately here and calculate the ratio in
> the Contextualized layer. Can we confirm what the numerator and denominator are?"

---

### C.3 — WHY (Reason Codes and Classification Vocabulary)

For entities that carry classification codes (delay_event, maintenance work orders,
material classification, permit types):

> "What are the codes [source system] uses to classify [event type]?
> For each code — what does it mean in business language?
> Is this code list standardised across all sites, or does each site have its own list?"

**This section is critical for the MFD data product — do not rush it.**

**For delay events (GMG TUM):**
Present the TUM hierarchy from the process model:
> "The GMG Time Usage Model gives us the top-level categories:
> Working Time (WT), Non-Productive Time (NP), Operating Delay (OD),
> Operating Standby (SBO), Downtime (DT), External Standby (SBE).
>
> Your site uses specific reason codes under each category. I need to map
> your codes to these TUM categories.
>
> Starting with Downtime (DT): what codes does [system] use for breakdowns?
> Give me a real example from the last shift report."

**Stakeholder coaching — the OD vs. SBO probe:**
This is the most commonly misclassified distinction in the TUM. Address it directly:
> "There's an important distinction between Operating Delay (OD) and Operating Standby (SBO).
>
> Operating Delay (OD): the equipment is available and wants to work, but there's a brief
> inherent interruption — queuing at a face, waiting for a blast, fuelling. These are
> expected and part of normal operations.
>
> Operating Standby (SBO): the equipment is available but management has decided not to
> use it — not enough work, too many trucks for the face, crusher down so ore trucks wait.
> This is a management decision.
>
> The distinction matters because OD shows up as operational inefficiency and SBO shows
> up as fleet sizing or planning decisions. They have different improvement actions.
>
> When a truck queues for 45 minutes at a crusher that's offline — is that OD or SBO?
> Who in your organisation makes that classification, and how do they decide?"
Expected answer: SBO (management decision — crusher down). If they say OD, probe further
with the consequence framing above.

**For material classification (ore / waste / marginal):**
> "When a geologist classifies a zone as 'marginal ore' — what does that mean at [site]?
> Is there a formal definition tied to the cut-off grade, or is it a judgment call?
> What's the cut-off grade threshold in effect right now, and where does that parameter live?"
This establishes whether cut-off grade is a business rule in the Curated layer
(unlikely — it changes) or a Contextualized layer concern.

---

### C.4 — Grain confirmation

For each Transactional entity, confirm the grain explicitly:

> "I want to confirm the grain statement for [entity]:
> 'Each row represents one [X] at [Y] level for [Z].'
> Is that right? Can you give me an example of two rows that would be separate
> and one situation where you might be tempted to aggregate into one row but shouldn't?"

The last question is the most important. It forces the stakeholder to think about edge cases
that reveal grain ambiguity before they become modeling problems.

**Common grain ambiguity probes:**
- Haul cycle: "If a truck loads at shovel A and dumps half at the crusher and half at
  a stockpile — is that one cycle or two?"
- Work order: "If a PM is interrupted, partially completed, and resumed the next shift —
  is that one work order or two?"
- Shift mass balance: "If a shift closes with an unresolved variance and a correction is
  posted the next day — does the correction become a new row or does it update the original?"

---

### C.5 — Section C confirmation

```
SECTION C SUMMARY — Event Canvas HOW MANY and WHY

[Event entity name]:
  Grain confirmed: [grain statement] — confirmed by [name]
  Measures confirmed: [N]
    [measure name]: [unit] — [additive | non-additive] — source: [system.field]
    ...
  Reason code vocabulary: [N codes mapped to TUM / standard categories]
  OD vs SBO decision table: [confirmed | needs-workshop]
  Open items: [N]

[repeat per entity]
```

Ask: "Does this capture everything? Any measures or codes I've missed? Shall I proceed to Section D?"

---

## SECTION D — SITE VARIANTS
> Goal: Document every point where a site deviates from the canonical model.
> This section is often underestimated. Site variants discovered late cause rework.
> It is better to spend 30 minutes here than 3 days fixing the model at Gate 2.

### D.1 — Present the canonical model assumptions

> "The process model describes the canonical open-pit mining process. It is based on
> industry standards — ISA-95, GMG, AMIRA P754. Your sites generally follow this model,
> but there will be places where [site] does things differently.
>
> I'm going to go through each entity and ask: does [site] match the standard, or is
> there something specific you do differently?"

---

### D.2 — Site-by-site variant elicitation

For each site in `sites_in_scope`, and for each entity in the entity register, ask:

> "For [entity name] at [site]: does the definition, the source system, the natural key,
> or any key attribute differ from what we agreed for [primary site]?"

**High-probability variant areas to probe specifically:**

**Shift boundaries:**
> "At [site], does the day shift run 06:00–18:00 exactly, or does it differ?
> Are there sites in the list where the shift boundary is based on local time vs. UTC?
> Is there a third shift (afternoon / graveyard) at any site?"

**Equipment classification:**
> "At Red Dog vs. HVC — the equipment classes are likely different (hydraulic excavators
> vs. rope shovels, smaller truck classes). Does your data product need to normalise
> these into a single equipment class taxonomy, or report them separately?"

**Delay code vocabulary:**
> "Do all sites use the same delay reason codes, or does each site have its own list?
> If they differ — is there a corporate code that maps across sites, or has no one
> done that harmonisation yet?"
If no cross-site mapping exists, this is an MDM gap. Flag as an open item.

**Grade control / cut-off grade:**
> "The cut-off grade at Red Dog (Zn) and HVC (Cu) are fundamentally different metals.
> Does your material classification entity handle multi-commodity cut-off grades,
> or is this product scoped to a single commodity?"

**Measurement instrument:**
> "For payload measurement — at HVC, are strut pressures the source or is there a
> belt scale at the crusher that is the authoritative measurement? At Red Dog?"
The answer may differ by site. Each variant requires a `site_override` entry.

---

### D.3 — Section D confirmation

```
SECTION D SUMMARY — Site Variants

Sites in scope: [list]
Primary (canonical) site: [site]

Variants documented: [N]
  [Entity name] at [site]:
    Field: [which field differs]
    Standard value: [canonical model value]
    Site value: [what this site actually does]
    Data product impact: [what this means for the model]

No variants: [list of entities with no site-specific differences]

Open items: [N — typically: cross-site code harmonisation, shift boundary UTC/local]
```

Ask: "Are there any other site-specific nuances I should capture? Shall I proceed to Section E?"

---

## SECTION E — VALIDATION AND OVERLAY GENERATION
> Goal: Produce a complete, validated beam-overlay.yaml ready for Stage 2.
> This section is internal — no further stakeholder input required unless
> the validation reveals missing required fields.

### E.1 — Self-check against schema

Before writing the overlay, verify:

```
[ ] All required fields in beam-overlay-schema.yaml have a status of:
    confirmed | provisional | not-applicable
[ ] No required field has status: needs-workshop
    (if any do — flag to analyst and ask if the workshop can be extended or
    if those entities should be parked as out-of-scope for this iteration)
[ ] Every entity in process-model-ref.md has a corresponding entry in the overlay
[ ] Every Transactional entity has at least one confirmed measure
[ ] The grain statement for each Transactional entity is explicitly confirmed
[ ] OD vs SBO decision table is populated for any entity that carries delay events
[ ] Domain owner is named (not 'TBD') for every entity
[ ] At least one source system is listed for every entity with in_raw_layer confirmed
```

---

### E.2 — Write beam-overlay.yaml

Produce the overlay using the schema from `templates/beam-overlay-schema.yaml`.

For any field that is not fully confirmed:
- Use `status: provisional` if an answer was given but not verified with authority
- Use `status: needs-workshop` if no answer was obtained — this will produce a WARN
  or BLOCK on validate-overlay depending on whether the field is REQUIRED

---

### E.3 — Run validate-overlay automatically

Run the validation protocol from `.claude/commands/validate-overlay.md` against the
freshly written overlay. Present the report to the analyst.

If the report shows BLOCK status:
> "The overlay has [N] fields that will block Stage 2. I've listed them above.
> Options:
> 1. Extend the workshop now if the relevant stakeholder is available
> 2. Schedule a follow-up session for the blocked items
> 3. Remove the blocked entities from scope for this iteration
> Which would you prefer?"

If the report shows WARN status:
> "The overlay is ready for Stage 2, but [N] warnings will appear as open items
> in the data modeling session. The data modeler will need to resolve these before
> Gate 1 can be cleared. I've logged them as open items in the overlay."

If the report shows PASS:
> "The overlay is complete and validated. Stage 2 can proceed."

---

### E.4 — Vocabulary additions

Review `vocabulary_additions` in the overlay. For any entry with `status: proposed`:

> "During this workshop, [N] new Teck-specific terms were identified that aren't
> in the vocabulary master yet. I'll add them to standards/teck-vocabulary-master.md
> for review and confirmation."

Write the additions to `standards/teck-vocabulary-master.md` under the appropriate section.

---

### E.5 — Session close

Write the session log via `log session`.

Produce a handoff summary:

```
WORKSHOP COMPLETE — [product-name]

Output files:
  workshops/[product-name]/process-model-ref.md  ✓
  workshops/[product-name]/beam-overlay.yaml      ✓
  workshops/[product-name]/session-log.md         ✓

Overlay status: PASS | WARN ([N] items) | BLOCK ([N] items)

Entities ready for Stage 2: [N]
Entities with open items: [N]
Entities blocked: [N]

To hand off to Stage 2:
  Copy process-model-ref.md and beam-overlay.yaml to:
  teck-data-modeling/products/[product-name]/inputs/

The data modeler should run:
  validate overlay for [product-name]
  start session CONCEPTUAL for [product-name]
```
