# Pillar 2: Mining Operations — BPMN Generation Specification

## Purpose
This file is the structured BPMN input specification for Pillar 2: Mining Operations (Extraction).
Use alongside `02-mining-operations-extraction.md` (the process model) to generate
Lucidchart-compatible BPMN 2.0 XML. The process model provides business context and entity
definitions; this file provides the formal BPMN element inventory and sequence flows required
for syntactically valid XML generation.

## ID Convention
- Diagram: `P2_{level}_{abbrev}` (e.g. `P2_L2_DB` = Pillar 2, L2, Drill & Blast)
- Pool: `{DiagramID}_PL`
- Lane: `{DiagramID}_LN_{role_abbrev}`
- Task (manual/user): `{DiagramID}_T{nn}`
- Sub-Process (expanded): `{DiagramID}_SP{nn}`
- Exclusive Gateway: `{DiagramID}_XGW{nn}`
- Parallel Gateway: `{DiagramID}_PGW{nn}`
- Start Event: `{DiagramID}_SE`
- End Event: `{DiagramID}_EE{nn}`
- Intermediate Catch Event: `{DiagramID}_ICE{nn}`
- Sequence Flow: `{DiagramID}_F{nn}`
- Message Flow (cross-pool): `{DiagramID}_MF{nn}`

## Lucidchart BPMN 2.0 XML Notes
- Use `isExecutable="false"` on all processes (documentation model, not executable)
- Lucidchart requires `<bpmndi:BPMNDiagram>` block — populate with placeholder coordinates;
  Lucidchart will re-layout on import. Use x=0 y=0 for all shapes and Lucidchart auto-arranges.
- Lane `flowNodeRef` elements must list every task/gateway/event ID that sits in that lane
- All `sequenceFlow` elements must reference valid `sourceRef` and `targetRef` IDs

## Diagram Inventory

| Diagram ID | Level | Title | L3 Sub-diagrams |
|------------|-------|-------|-----------------|
| P2_L2_DB | L2 | Drill & Blast | P2_L3_BDL, P2_L3_DRL, P2_L3_CHG, P2_L3_DET, P2_L3_MPP |
| P2_L2_LH | L2 | Load & Haul | P2_L3_FCP, P2_L3_LDG, P2_L3_HUL, P2_L3_STK |
| P2_L2_MS | L2 | Mine Services | P2_L3_HRM, P2_L3_PDW, P2_L3_SSM |

---

## P2_L2_DB — Drill & Blast (L2)

**Scope**: From short-term plan release through to material classification uploaded to FMS.
Covers all sub-processes at summary level; each L3 below expands individual sub-processes.

### Pool & Lanes
| ID | Name |
|----|------|
| P2_L2_DB_PL | Drill & Blast |
| P2_L2_DB_LN_PLN | Mine Planning (external trigger) |
| P2_L2_DB_LN_ENG | Drill & Blast Engineer |
| P2_L2_DB_LN_OPR | Drill Rig Operator |
| P2_L2_DB_LN_SHT | Shot-firer |
| P2_L2_DB_LN_GCG | Grade Control Geologist |
| P2_L2_DB_LN_SYS | FMS / LIMS / Systems |

### Element Inventory
| ID | BPMN Type | Name | Lane | Marker/Notes |
|----|-----------|------|------|--------------|
| P2_L2_DB_SE | startEvent (message) | Short-term plan released; dig polygon available | P2_L2_DB_LN_PLN | messageStart |
| P2_L2_DB_SP01 | subProcess (collapsed) | Blast Design & Pattern Layout (2.1.1) | P2_L2_DB_LN_ENG | References P2_L3_BDL |
| P2_L2_DB_SP02 | subProcess (collapsed) | Drilling Execution (2.1.2) | P2_L2_DB_LN_OPR | References P2_L3_DRL; loop marker |
| P2_L2_DB_SP03 | subProcess (collapsed) | Charging & Stemming (2.1.3) | P2_L2_DB_LN_SHT | References P2_L3_CHG |
| P2_L2_DB_SP04 | subProcess (collapsed) | Detonation & Assessment (2.1.4) | P2_L2_DB_LN_SHT | References P2_L3_DET |
| P2_L2_DB_SP05 | subProcess (collapsed) | Muck Pile Preparation (2.1.5) | P2_L2_DB_LN_GCG | References P2_L3_MPP |
| P2_L2_DB_XGW01 | exclusiveGateway | All holes QC accepted? | P2_L2_DB_LN_ENG | |
| P2_L2_DB_XGW02 | exclusiveGateway | P80 within specification? | P2_L2_DB_LN_ENG | |
| P2_L2_DB_EE01 | endEvent | Muck pile classified; destinations in FMS | P2_L2_DB_LN_SYS | |

### Sequence Flows
| ID | From | To | Condition / Label |
|----|------|----|-------------------|
| P2_L2_DB_F01 | P2_L2_DB_SE | P2_L2_DB_SP01 | |
| P2_L2_DB_F02 | P2_L2_DB_SP01 | P2_L2_DB_SP02 | |
| P2_L2_DB_F03 | P2_L2_DB_SP02 | P2_L2_DB_XGW01 | |
| P2_L2_DB_F04 | P2_L2_DB_XGW01 | P2_L2_DB_SP03 | Yes — all holes pass QC |
| P2_L2_DB_F05 | P2_L2_DB_XGW01 | P2_L2_DB_SP02 | No — remediate and re-drill; loop back |
| P2_L2_DB_F06 | P2_L2_DB_SP03 | P2_L2_DB_SP04 | |
| P2_L2_DB_F07 | P2_L2_DB_SP04 | P2_L2_DB_XGW02 | |
| P2_L2_DB_F08 | P2_L2_DB_XGW02 | P2_L2_DB_SP05 | Yes — P80 within spec |
| P2_L2_DB_F09 | P2_L2_DB_XGW02 | P2_L2_DB_SP04 | No — re-blast assessment; loop back |
| P2_L2_DB_F10 | P2_L2_DB_SP05 | P2_L2_DB_EE01 | |

---

## P2_L3_BDL — Blast Design & Pattern Layout (L3, sub of 2.1.1)

**Scope**: From dig polygon receipt to approved blast pattern design file ready for drill guidance system.

### Pool & Lanes
| ID | Name |
|----|------|
| P2_L3_BDL_PL | Blast Design & Pattern Layout |
| P2_L3_BDL_LN_ENG | Drill & Blast Engineer |
| P2_L3_BDL_LN_SRV | Survey Technician |
| P2_L3_BDL_LN_SYS | Blast Design Software / FMS |

### Element Inventory
| ID | BPMN Type | Name | Lane |
|----|-----------|------|------|
| P2_L3_BDL_SE | startEvent (message) | Approved dig polygon received | P2_L3_BDL_LN_ENG |
| P2_L3_BDL_T01 | task | Survey & Stake Pattern on Bench (2.1.1.1) | P2_L3_BDL_LN_SRV |
| P2_L3_BDL_T02 | task | Design Hole Layout Parameters — burden, spacing, depth (2.1.1.2) | P2_L3_BDL_LN_ENG |
| P2_L3_BDL_T03 | task | Select Explosive Product per Hole (2.1.1.3) | P2_L3_BDL_LN_ENG |
| P2_L3_BDL_T04 | serviceTask | Upload Pattern Design to Blast Software & FMS | P2_L3_BDL_LN_SYS |
| P2_L3_BDL_EE01 | endEvent | Blast pattern design file available; drill guidance system loaded | P2_L3_BDL_LN_SYS |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P2_L3_BDL_F01 | P2_L3_BDL_SE | P2_L3_BDL_T01 | |
| P2_L3_BDL_F02 | P2_L3_BDL_T01 | P2_L3_BDL_T02 | |
| P2_L3_BDL_F03 | P2_L3_BDL_T02 | P2_L3_BDL_T03 | |
| P2_L3_BDL_F04 | P2_L3_BDL_T03 | P2_L3_BDL_T04 | |
| P2_L3_BDL_F05 | P2_L3_BDL_T04 | P2_L3_BDL_EE01 | |

---

## P2_L3_DRL — Drilling Execution (L3, sub of 2.1.2)

**Scope**: From FMS drill rig dispatch through per-hole MWD capture to pattern QC acceptance.

### Pool & Lanes
| ID | Name |
|----|------|
| P2_L3_DRL_PL | Drilling Execution |
| P2_L3_DRL_LN_FMS | FMS / Drill Guidance System |
| P2_L3_DRL_LN_OPR | Drill Rig Operator |
| P2_L3_DRL_LN_ENG | Drill & Blast Engineer |

### Element Inventory
| ID | BPMN Type | Name | Lane | Notes |
|----|-----------|------|------|-------|
| P2_L3_DRL_SE | startEvent | Drill plan dispatched from FMS | P2_L3_DRL_LN_FMS | |
| P2_L3_DRL_T01 | task | Navigate Drill Rig to Hole Collar (2.1.2.1) — TUM: NP | P2_L3_DRL_LN_OPR | |
| P2_L3_DRL_T02 | task | Drill Hole with MWD Capture (2.1.2.2) — TUM: PT | P2_L3_DRL_LN_OPR | |
| P2_L3_DRL_T03 | task | Measure As-Drilled Depth and Water (2.1.2.3) | P2_L3_DRL_LN_OPR | |
| P2_L3_DRL_XGW01 | exclusiveGateway | More holes in pattern? | P2_L3_DRL_LN_FMS | Loop control |
| P2_L3_DRL_T04 | task | Validate Hole Quality — QC Accept/Reject (2.1.2.4) | P2_L3_DRL_LN_ENG | |
| P2_L3_DRL_XGW02 | exclusiveGateway | All holes pass QC? | P2_L3_DRL_LN_ENG | |
| P2_L3_DRL_T05 | task | Issue Remediation Instruction for Failed Holes | P2_L3_DRL_LN_ENG | |
| P2_L3_DRL_EE01 | endEvent | All holes QC-accepted; pattern ready for charging | P2_L3_DRL_LN_ENG | |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P2_L3_DRL_F01 | P2_L3_DRL_SE | P2_L3_DRL_T01 | |
| P2_L3_DRL_F02 | P2_L3_DRL_T01 | P2_L3_DRL_T02 | |
| P2_L3_DRL_F03 | P2_L3_DRL_T02 | P2_L3_DRL_T03 | |
| P2_L3_DRL_F04 | P2_L3_DRL_T03 | P2_L3_DRL_XGW01 | |
| P2_L3_DRL_F05 | P2_L3_DRL_XGW01 | P2_L3_DRL_T01 | Yes — next hole in pattern (loop) |
| P2_L3_DRL_F06 | P2_L3_DRL_XGW01 | P2_L3_DRL_T04 | No — all holes drilled |
| P2_L3_DRL_F07 | P2_L3_DRL_T04 | P2_L3_DRL_XGW02 | |
| P2_L3_DRL_F08 | P2_L3_DRL_XGW02 | P2_L3_DRL_EE01 | Yes — all pass |
| P2_L3_DRL_F09 | P2_L3_DRL_XGW02 | P2_L3_DRL_T05 | No — failures exist |
| P2_L3_DRL_F10 | P2_L3_DRL_T05 | P2_L3_DRL_T01 | Remediate — loop back to re-drill |

---

## P2_L3_CHG — Charging & Stemming (L3, sub of 2.1.3)

### Pool & Lanes
| ID | Name |
|----|------|
| P2_L3_CHG_PL | Charging & Stemming |
| P2_L3_CHG_LN_FMS | FMS / Mine Controller |
| P2_L3_CHG_LN_SHT | Shot-firer |
| P2_L3_CHG_LN_ETO | Explosive Truck Operator |

### Element Inventory
| ID | BPMN Type | Name | Lane |
|----|-----------|------|------|
| P2_L3_CHG_SE | startEvent | QC-accepted holes; explosive truck available | P2_L3_CHG_LN_FMS |
| P2_L3_CHG_T01 | task | Dispatch Explosive Truck to Pattern (2.1.3.1) — TUM: NP | P2_L3_CHG_LN_FMS |
| P2_L3_CHG_T02 | task | Load Explosive into Holes per Design (2.1.3.2) | P2_L3_CHG_LN_SHT |
| P2_L3_CHG_T03 | task | Apply Stemming to Design Depth (2.1.3.3) | P2_L3_CHG_LN_SHT |
| P2_L3_CHG_T04 | task | Install Initiation System — detonators, delays (2.1.3.4) | P2_L3_CHG_LN_SHT |
| P2_L3_CHG_XGW01 | exclusiveGateway | More holes to charge? | P2_L3_CHG_LN_SHT |
| P2_L3_CHG_EE01 | endEvent | All holes charged, stemmed, initiated; pattern ready to fire | P2_L3_CHG_LN_SHT |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P2_L3_CHG_F01 | P2_L3_CHG_SE | P2_L3_CHG_T01 | |
| P2_L3_CHG_F02 | P2_L3_CHG_T01 | P2_L3_CHG_T02 | |
| P2_L3_CHG_F03 | P2_L3_CHG_T02 | P2_L3_CHG_T03 | |
| P2_L3_CHG_F04 | P2_L3_CHG_T03 | P2_L3_CHG_T04 | |
| P2_L3_CHG_F05 | P2_L3_CHG_T04 | P2_L3_CHG_XGW01 | |
| P2_L3_CHG_F06 | P2_L3_CHG_XGW01 | P2_L3_CHG_T02 | Yes — next hole (loop) |
| P2_L3_CHG_F07 | P2_L3_CHG_XGW01 | P2_L3_CHG_EE01 | No — all holes charged |

---

## P2_L3_DET — Detonation & Assessment (L3, sub of 2.1.4)

### Pool & Lanes
| ID | Name |
|----|------|
| P2_L3_DET_PL | Detonation & Assessment |
| P2_L3_DET_LN_SUP | Drill & Blast Supervisor / Mine Controller |
| P2_L3_DET_LN_SHT | Shot-firer |
| P2_L3_DET_LN_ENG | Drill & Blast Engineer |
| P2_L3_DET_LN_SYS | FMS |

### Element Inventory
| ID | BPMN Type | Name | Lane | Notes |
|----|-----------|------|------|-------|
| P2_L3_DET_SE | startEvent | Initiation network complete; supervisor approval | P2_L3_DET_LN_SUP | |
| P2_L3_DET_T01 | task | Establish & Clear Exclusion Zone (2.1.4.1) | P2_L3_DET_LN_SUP | delay_event TUM:OD or SBO recorded |
| P2_L3_DET_T02 | serviceTask | Record TUM Delay Event for Equipment in Zone | P2_L3_DET_LN_SYS | |
| P2_L3_DET_T03 | task | Initiate Blast (2.1.4.2) | P2_L3_DET_LN_SHT | blast_event timestamp UTC |
| P2_L3_DET_ICE01 | intermediateCatchEvent (timer) | Re-entry waiting period (smoke clearance) | P2_L3_DET_LN_SHT | timerEvent |
| P2_L3_DET_T04 | task | Conduct Post-Blast Safety Inspection (2.1.4.3) | P2_L3_DET_LN_SHT | |
| P2_L3_DET_XGW01 | exclusiveGateway | Misfire detected? | P2_L3_DET_LN_SHT | |
| P2_L3_DET_T05 | task | Activate Misfire Protocol (safety — out of scope detail) | P2_L3_DET_LN_SUP | |
| P2_L3_DET_T06 | task | Issue Safety Clearance for Equipment Re-entry | P2_L3_DET_LN_SUP | |
| P2_L3_DET_T07 | task | Assess Fragmentation Quality — P80 vs. target (2.1.4.4) | P2_L3_DET_LN_ENG | |
| P2_L3_DET_XGW02 | exclusiveGateway | P80 within specification? | P2_L3_DET_LN_ENG | |
| P2_L3_DET_T08 | task | Issue Re-blast Assessment for Oversize | P2_L3_DET_LN_ENG | |
| P2_L3_DET_EE01 | endEvent | Blast assessed; safety clearance issued; muck pile ready | P2_L3_DET_LN_SUP | |
| P2_L3_DET_EE02 | endEvent (error) | Misfire protocol active — escalated | P2_L3_DET_LN_SUP | |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P2_L3_DET_F01 | P2_L3_DET_SE | P2_L3_DET_T01 | |
| P2_L3_DET_F02 | P2_L3_DET_T01 | P2_L3_DET_T02 | |
| P2_L3_DET_F03 | P2_L3_DET_T02 | P2_L3_DET_T03 | |
| P2_L3_DET_F04 | P2_L3_DET_T03 | P2_L3_DET_ICE01 | |
| P2_L3_DET_F05 | P2_L3_DET_ICE01 | P2_L3_DET_T04 | Timer elapsed |
| P2_L3_DET_F06 | P2_L3_DET_T04 | P2_L3_DET_XGW01 | |
| P2_L3_DET_F07 | P2_L3_DET_XGW01 | P2_L3_DET_T05 | Yes — misfire |
| P2_L3_DET_F08 | P2_L3_DET_XGW01 | P2_L3_DET_T06 | No — clear |
| P2_L3_DET_F09 | P2_L3_DET_T05 | P2_L3_DET_EE02 | |
| P2_L3_DET_F10 | P2_L3_DET_T06 | P2_L3_DET_T07 | |
| P2_L3_DET_F11 | P2_L3_DET_T07 | P2_L3_DET_XGW02 | |
| P2_L3_DET_F12 | P2_L3_DET_XGW02 | P2_L3_DET_EE01 | Yes — within spec |
| P2_L3_DET_F13 | P2_L3_DET_XGW02 | P2_L3_DET_T08 | No — oversize |
| P2_L3_DET_F14 | P2_L3_DET_T08 | P2_L3_DET_EE01 | Re-blast planned separately |

---

## P2_L3_MPP — Muck Pile Preparation (L3, sub of 2.1.5)

### Pool & Lanes
| ID | Name |
|----|------|
| P2_L3_MPP_PL | Muck Pile Preparation |
| P2_L3_MPP_LN_GCG | Grade Control Geologist |
| P2_L3_MPP_LN_LAB | LIMS / Laboratory |
| P2_L3_MPP_LN_FMS | FMS / Mine Controller |

### Element Inventory
| ID | BPMN Type | Name | Lane | Notes |
|----|-----------|------|------|-------|
| P2_L3_MPP_SE | startEvent | Safety clearance issued; muck pile accessible | P2_L3_MPP_LN_GCG | |
| P2_L3_MPP_T01 | task | Collect Grade Control Samples (2.1.5.1) | P2_L3_MPP_LN_GCG | |
| P2_L3_MPP_T02 | serviceTask | Submit Samples to LIMS | P2_L3_MPP_LN_LAB | |
| P2_L3_MPP_ICE01 | intermediateCatchEvent (timer) | Lab TAT — assay turnaround (8-24 hrs) | P2_L3_MPP_LN_LAB | timerEvent |
| P2_L3_MPP_T03 | task | Classify Material and Assign Destination (2.1.5.2) | P2_L3_MPP_LN_GCG | |
| P2_L3_MPP_T04 | serviceTask | Upload Destination Assignment to FMS | P2_L3_MPP_LN_FMS | |
| P2_L3_MPP_EE01 | endEvent | Material classified; FMS destinations active; Load & Haul can commence | P2_L3_MPP_LN_FMS | |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P2_L3_MPP_F01 | P2_L3_MPP_SE | P2_L3_MPP_T01 | |
| P2_L3_MPP_F02 | P2_L3_MPP_T01 | P2_L3_MPP_T02 | |
| P2_L3_MPP_F03 | P2_L3_MPP_T02 | P2_L3_MPP_ICE01 | |
| P2_L3_MPP_F04 | P2_L3_MPP_ICE01 | P2_L3_MPP_T03 | Results received |
| P2_L3_MPP_F05 | P2_L3_MPP_T03 | P2_L3_MPP_T04 | |
| P2_L3_MPP_F06 | P2_L3_MPP_T04 | P2_L3_MPP_EE01 | |

---

## P2_L2_LH — Load & Haul (L2)

**Scope**: From shift start through to committed shift production report. The haul cycle loop
is the central repeating structure. Multiple parallel instances execute concurrently across fleet.

### Pool & Lanes
| ID | Name |
|----|------|
| P2_L2_LH_PL | Load & Haul |
| P2_L2_LH_LN_MCT | Mine Controller / FMS |
| P2_L2_LH_LN_SHV | Shovel Operator |
| P2_L2_LH_LN_DZR | Dozer Operator |
| P2_L2_LH_LN_TRK | Truck Operator |

### Element Inventory
| ID | BPMN Type | Name | Lane | Notes |
|----|-----------|------|------|-------|
| P2_L2_LH_SE | startEvent | Shift start; targets loaded; muck pile classified | P2_L2_LH_LN_MCT | |
| P2_L2_LH_T01 | task | Assign Equipment to Shift | P2_L2_LH_LN_MCT | |
| P2_L2_LH_PGW01 | parallelGateway | [FORK] Multiple trucks and shovels operate concurrently | P2_L2_LH_LN_MCT | parallelFork |
| P2_L2_LH_SP01 | subProcess (collapsed) | Face Preparation (2.2.1) | P2_L2_LH_LN_SHV | References P2_L3_FCP |
| P2_L2_LH_SP02 | subProcess (collapsed) | Loading (2.2.2) | P2_L2_LH_LN_SHV | References P2_L3_LDG |
| P2_L2_LH_SP03 | subProcess (collapsed) | Hauling (2.2.3) | P2_L2_LH_LN_TRK | References P2_L3_HUL; loop marker |
| P2_L2_LH_XGW01 | exclusiveGateway | Shift end or face exhausted? | P2_L2_LH_LN_MCT | |
| P2_L2_LH_PGW02 | parallelGateway | [JOIN] All trucks report cycle complete | P2_L2_LH_LN_MCT | parallelJoin |
| P2_L2_LH_SP04 | subProcess (collapsed) | Stockpile Management (2.2.4) | P2_L2_LH_LN_MCT | References P2_L3_STK; parallel stream |
| P2_L2_LH_T02 | task | Reconcile Open Haul Cycle Records | P2_L2_LH_LN_MCT | |
| P2_L2_LH_T03 | task | Generate and Commit Shift Production Report | P2_L2_LH_LN_MCT | |
| P2_L2_LH_EE01 | endEvent | Shift report committed; actuals uploaded | P2_L2_LH_LN_MCT | |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P2_L2_LH_F01 | P2_L2_LH_SE | P2_L2_LH_T01 | |
| P2_L2_LH_F02 | P2_L2_LH_T01 | P2_L2_LH_PGW01 | |
| P2_L2_LH_F03 | P2_L2_LH_PGW01 | P2_L2_LH_SP01 | Parallel branch 1 — shovel |
| P2_L2_LH_F04 | P2_L2_LH_PGW01 | P2_L2_LH_SP04 | Parallel branch 2 — stockpile mgmt (continuous) |
| P2_L2_LH_F05 | P2_L2_LH_SP01 | P2_L2_LH_SP02 | |
| P2_L2_LH_F06 | P2_L2_LH_SP02 | P2_L2_LH_SP03 | |
| P2_L2_LH_F07 | P2_L2_LH_SP03 | P2_L2_LH_XGW01 | Cycle complete |
| P2_L2_LH_F08 | P2_L2_LH_XGW01 | P2_L2_LH_SP02 | No — continue cycling |
| P2_L2_LH_F09 | P2_L2_LH_XGW01 | P2_L2_LH_PGW02 | Yes — shift end or face exhausted |
| P2_L2_LH_F10 | P2_L2_LH_SP04 | P2_L2_LH_PGW02 | Stockpile stream joins at shift end |
| P2_L2_LH_F11 | P2_L2_LH_PGW02 | P2_L2_LH_T02 | |
| P2_L2_LH_F12 | P2_L2_LH_T02 | P2_L2_LH_T03 | |
| P2_L2_LH_F13 | P2_L2_LH_T03 | P2_L2_LH_EE01 | |

---

## P2_L3_FCP — Face Preparation (L3, sub of 2.2.1)

### Pool & Lanes
| ID | Name |
|----|------|
| P2_L3_FCP_PL | Face Preparation |
| P2_L3_FCP_LN_MCT | Mine Controller / FMS |
| P2_L3_FCP_LN_SHV | Shovel Operator |
| P2_L3_FCP_LN_DZR | Dozer Operator |

### Element Inventory
| ID | BPMN Type | Name | Lane |
|----|-----------|------|------|
| P2_L3_FCP_SE | startEvent | Face assignment issued from FMS | P2_L3_FCP_LN_MCT |
| P2_L3_FCP_T01 | task | Tram Shovel to Dig Face (2.2.1.1) — TUM: NP | P2_L3_FCP_LN_SHV |
| P2_L3_FCP_PGW01 | parallelGateway | [FORK] Shovel arrives; dozer dispatched concurrently | P2_L3_FCP_LN_MCT |
| P2_L3_FCP_T02 | task | Clean and Dress Dig Face — dozer (2.2.1.2) — TUM: WT | P2_L3_FCP_LN_DZR |
| P2_L3_FCP_PGW02 | parallelGateway | [JOIN] Face ready; shovel in position | P2_L3_FCP_LN_MCT |
| P2_L3_FCP_EE01 | endEvent | Face prepared; shovel in position; loading can commence | P2_L3_FCP_LN_SHV |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P2_L3_FCP_F01 | P2_L3_FCP_SE | P2_L3_FCP_T01 | |
| P2_L3_FCP_F02 | P2_L3_FCP_T01 | P2_L3_FCP_PGW01 | |
| P2_L3_FCP_F03 | P2_L3_FCP_PGW01 | P2_L3_FCP_T02 | Parallel — dozer |
| P2_L3_FCP_F04 | P2_L3_FCP_T02 | P2_L3_FCP_PGW02 | |
| P2_L3_FCP_F05 | P2_L3_FCP_PGW01 | P2_L3_FCP_PGW02 | Shovel in position (arrives same time) |
| P2_L3_FCP_F06 | P2_L3_FCP_PGW02 | P2_L3_FCP_EE01 | |

---

## P2_L3_LDG — Loading (L3, sub of 2.2.2)

### Pool & Lanes
| ID | Name |
|----|------|
| P2_L3_LDG_PL | Loading |
| P2_L3_LDG_LN_MCT | Mine Controller / FMS |
| P2_L3_LDG_LN_SHV | Shovel Operator |
| P2_L3_LDG_LN_TRK | Truck Operator |

### Element Inventory
| ID | BPMN Type | Name | Lane | Notes |
|----|-----------|------|------|-------|
| P2_L3_LDG_SE | startEvent | Truck dispatched to face; shovel and face ready | P2_L3_LDG_LN_MCT | |
| P2_L3_LDG_T01 | task | Queue Truck at Shovel (2.2.2.1) — TUM: OD or SBO | P2_L3_LDG_LN_TRK | |
| P2_L3_LDG_XGW01 | exclusiveGateway | Queue duration exceeds OD threshold? | P2_L3_LDG_LN_MCT | OD vs. SBO decision |
| P2_L3_LDG_T02 | task | Classify Queue as SBO — mine controller decision | P2_L3_LDG_LN_MCT | TUM: SBO |
| P2_L3_LDG_T03 | task | Spot Truck at Shovel (2.2.2.2) — TUM: NP | P2_L3_LDG_LN_TRK | |
| P2_L3_LDG_T04 | task | Load Truck with Shovel (2.2.2.3) — TUM: PT (shovel) / WT (truck) | P2_L3_LDG_LN_SHV | |
| P2_L3_LDG_T05 | serviceTask | Verify Payload and Issue FMS Dispatch (2.2.2.4) | P2_L3_LDG_LN_MCT | haul_cycle record initiated |
| P2_L3_LDG_XGW02 | exclusiveGateway | Payload within tolerance? | P2_L3_LDG_LN_MCT | |
| P2_L3_LDG_T06 | task | Adjust Load — add or remove bucket pass | P2_L3_LDG_LN_SHV | |
| P2_L3_LDG_EE01 | endEvent | Truck loaded and dispatched; haul_cycle record initiated | P2_L3_LDG_LN_MCT | |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P2_L3_LDG_F01 | P2_L3_LDG_SE | P2_L3_LDG_T01 | |
| P2_L3_LDG_F02 | P2_L3_LDG_T01 | P2_L3_LDG_XGW01 | |
| P2_L3_LDG_F03 | P2_L3_LDG_XGW01 | P2_L3_LDG_T03 | No — within OD threshold |
| P2_L3_LDG_F04 | P2_L3_LDG_XGW01 | P2_L3_LDG_T02 | Yes — exceeds threshold; SBO decision |
| P2_L3_LDG_F05 | P2_L3_LDG_T02 | P2_L3_LDG_T03 | After SBO classification |
| P2_L3_LDG_F06 | P2_L3_LDG_T03 | P2_L3_LDG_T04 | |
| P2_L3_LDG_F07 | P2_L3_LDG_T04 | P2_L3_LDG_T05 | |
| P2_L3_LDG_F08 | P2_L3_LDG_T05 | P2_L3_LDG_XGW02 | |
| P2_L3_LDG_F09 | P2_L3_LDG_XGW02 | P2_L3_LDG_EE01 | Within tolerance |
| P2_L3_LDG_F10 | P2_L3_LDG_XGW02 | P2_L3_LDG_T06 | Out of tolerance |
| P2_L3_LDG_F11 | P2_L3_LDG_T06 | P2_L3_LDG_T05 | Re-verify |

---

## P2_L3_HUL — Hauling (L3, sub of 2.2.3)

### Pool & Lanes
| ID | Name |
|----|------|
| P2_L3_HUL_PL | Hauling |
| P2_L3_HUL_LN_MCT | Mine Controller / FMS |
| P2_L3_HUL_LN_TRK | Truck Operator |

### Element Inventory
| ID | BPMN Type | Name | Lane | Notes |
|----|-----------|------|------|-------|
| P2_L3_HUL_SE | startEvent | Truck loaded and dispatched | P2_L3_HUL_LN_TRK | |
| P2_L3_HUL_T01 | task | Execute Loaded Haul (2.2.3.1) — TUM: WT | P2_L3_HUL_LN_TRK | |
| P2_L3_HUL_ICE01 | intermediateCatchEvent (error) | Breakdown during haul | P2_L3_HUL_LN_TRK | errorEvent — boundary on T01 |
| P2_L3_HUL_T02 | task | Classify TUM: DT; notify maintenance | P2_L3_HUL_LN_MCT | Links to P5 work_order |
| P2_L3_HUL_T03 | task | Queue at Destination (2.2.3.2) — TUM: OD or SBO | P2_L3_HUL_LN_TRK | |
| P2_L3_HUL_XGW01 | exclusiveGateway | Queue at destination — OD or SBO? | P2_L3_HUL_LN_MCT | |
| P2_L3_HUL_T04 | task | Classify Queue as SBO; record mine controller decision | P2_L3_HUL_LN_MCT | |
| P2_L3_HUL_T05 | task | Spot Truck at Dump (2.2.3.3) — TUM: NP | P2_L3_HUL_LN_TRK | |
| P2_L3_HUL_T06 | task | Dump Load (2.2.3.4) — TUM: WT | P2_L3_HUL_LN_TRK | haul_cycle dump event |
| P2_L3_HUL_T07 | task | Execute Empty Return (2.2.3.5) — TUM: NP | P2_L3_HUL_LN_TRK | |
| P2_L3_HUL_EE01 | endEvent | Cycle complete; truck returns to face; haul_cycle record closed | P2_L3_HUL_LN_MCT | |
| P2_L3_HUL_EE02 | endEvent (error) | Equipment in TUM: DT — awaiting maintenance | P2_L3_HUL_LN_MCT | |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P2_L3_HUL_F01 | P2_L3_HUL_SE | P2_L3_HUL_T01 | |
| P2_L3_HUL_F02 | P2_L3_HUL_T01 | P2_L3_HUL_T03 | Normal — no breakdown |
| P2_L3_HUL_F03 | P2_L3_HUL_ICE01 | P2_L3_HUL_T02 | Breakdown detected |
| P2_L3_HUL_F04 | P2_L3_HUL_T02 | P2_L3_HUL_EE02 | Awaiting maintenance |
| P2_L3_HUL_F05 | P2_L3_HUL_T03 | P2_L3_HUL_XGW01 | |
| P2_L3_HUL_F06 | P2_L3_HUL_XGW01 | P2_L3_HUL_T05 | Within OD threshold |
| P2_L3_HUL_F07 | P2_L3_HUL_XGW01 | P2_L3_HUL_T04 | Exceeds threshold |
| P2_L3_HUL_F08 | P2_L3_HUL_T04 | P2_L3_HUL_T05 | After SBO classification |
| P2_L3_HUL_F09 | P2_L3_HUL_T05 | P2_L3_HUL_T06 | |
| P2_L3_HUL_F10 | P2_L3_HUL_T06 | P2_L3_HUL_T07 | |
| P2_L3_HUL_F11 | P2_L3_HUL_T07 | P2_L3_HUL_EE01 | |

---

## P2_L3_STK — Stockpile Management (L3, sub of 2.2.4)

### Pool & Lanes
| ID | Name |
|----|------|
| P2_L3_STK_PL | Stockpile Management |
| P2_L3_STK_LN_MCT | Mine Controller |
| P2_L3_STK_LN_GEO | Mine Geologist |
| P2_L3_STK_LN_OPR | Stockpile Controller / FEL Operator |

### Element Inventory
| ID | BPMN Type | Name | Lane |
|----|-----------|------|------|
| P2_L3_STK_SE | startEvent | Trucks dumping to stockpile zone | P2_L3_STK_LN_MCT |
| P2_L3_STK_T01 | task | Build ROM Stockpile — track zone increments (2.2.4.1) | P2_L3_STK_LN_MCT |
| P2_L3_STK_T02 | task | Track Stockpile Grade per Zone (2.2.4.2) | P2_L3_STK_LN_GEO |
| P2_L3_STK_ICE01 | intermediateCatchEvent (message) | Blend plan / reclaim instruction received | P2_L3_STK_LN_OPR |
| P2_L3_STK_T03 | task | Reclaim Material and Blend to Mill Feed (2.2.4.3) | P2_L3_STK_LN_OPR |
| P2_L3_STK_EE01 | endEvent | ROM material delivered to primary crusher | P2_L3_STK_LN_OPR |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P2_L3_STK_F01 | P2_L3_STK_SE | P2_L3_STK_T01 | |
| P2_L3_STK_F02 | P2_L3_STK_T01 | P2_L3_STK_T02 | |
| P2_L3_STK_F03 | P2_L3_STK_T02 | P2_L3_STK_ICE01 | Awaiting reclaim instruction |
| P2_L3_STK_F04 | P2_L3_STK_ICE01 | P2_L3_STK_T03 | Reclaim instruction received |
| P2_L3_STK_F05 | P2_L3_STK_T03 | P2_L3_STK_EE01 | |

---

## P2_L2_MS — Mine Services (L2)

**Scope**: All three Mine Services process areas running as parallel continuous streams during the shift.

### Pool & Lanes
| ID | Name |
|----|------|
| P2_L2_MS_PL | Mine Services |
| P2_L2_MS_LN_SUP | Services Supervisor |
| P2_L2_MS_LN_OPR | Road Maintenance Operator |
| P2_L2_MS_LN_DWA | Dewatering Operator / SCADA |
| P2_L2_MS_LN_GEO | Geotechnical Engineer |
| P2_L2_MS_LN_MCT | Mine Controller |

### Element Inventory
| ID | BPMN Type | Name | Lane | Notes |
|----|-----------|------|------|-------|
| P2_L2_MS_SE | startEvent | Shift start; services active | P2_L2_MS_LN_SUP | |
| P2_L2_MS_PGW01 | parallelGateway | [FORK] Three service streams run concurrently | P2_L2_MS_LN_SUP | |
| P2_L2_MS_SP01 | subProcess (collapsed) | Haul Road Maintenance (2.3.1) | P2_L2_MS_LN_OPR | References P2_L3_HRM |
| P2_L2_MS_SP02 | subProcess (collapsed) | Pit Dewatering (2.3.2) | P2_L2_MS_LN_DWA | References P2_L3_PDW; loop marker |
| P2_L2_MS_SP03 | subProcess (collapsed) | Slope Stability Monitoring (2.3.3) | P2_L2_MS_LN_GEO | References P2_L3_SSM; loop marker |
| P2_L2_MS_PGW02 | parallelGateway | [JOIN] Shift end — all streams complete | P2_L2_MS_LN_SUP | |
| P2_L2_MS_EE01 | endEvent | Shift end; service records submitted | P2_L2_MS_LN_SUP | |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P2_L2_MS_F01 | P2_L2_MS_SE | P2_L2_MS_PGW01 | |
| P2_L2_MS_F02 | P2_L2_MS_PGW01 | P2_L2_MS_SP01 | Parallel stream 1 |
| P2_L2_MS_F03 | P2_L2_MS_PGW01 | P2_L2_MS_SP02 | Parallel stream 2 |
| P2_L2_MS_F04 | P2_L2_MS_PGW01 | P2_L2_MS_SP03 | Parallel stream 3 |
| P2_L2_MS_F05 | P2_L2_MS_SP01 | P2_L2_MS_PGW02 | |
| P2_L2_MS_F06 | P2_L2_MS_SP02 | P2_L2_MS_PGW02 | |
| P2_L2_MS_F07 | P2_L2_MS_SP03 | P2_L2_MS_PGW02 | |
| P2_L2_MS_F08 | P2_L2_MS_PGW02 | P2_L2_MS_EE01 | |

---

## P2_L3_HRM — Haul Road Maintenance (L3, sub of 2.3.1)

### Element Inventory (Pool: P2_L3_HRM_PL | Lanes: Supervisor, Road Maint. Operator)
| ID | BPMN Type | Name | Lane |
|----|-----------|------|------|
| P2_L3_HRM_SE | startEvent | Shift start or condition call | P2_L3_HRM_LN_SUP |
| P2_L3_HRM_T01 | task | Assess Road Condition; Prioritise Segments | P2_L3_HRM_LN_SUP |
| P2_L3_HRM_T02 | task | Assign Grader and Water Truck | P2_L3_HRM_LN_SUP |
| P2_L3_HRM_T03 | task | Grade Road Segment (2.3.1.1) — TUM: WT (grader) | P2_L3_HRM_LN_OPR |
| P2_L3_HRM_T04 | task | Apply Dust Suppression (2.3.1.2) — TUM: WT (water truck) | P2_L3_HRM_LN_OPR |
| P2_L3_HRM_XGW01 | exclusiveGateway | More segments assigned? | P2_L3_HRM_LN_SUP |
| P2_L3_HRM_EE01 | endEvent | Shift complete; road maintenance records submitted | P2_L3_HRM_LN_SUP |

### Sequence Flows (P2_L3_HRM)
F01: SE→T01 | F02: T01→T02 | F03: T02→T03 | F04: T03→T04 | F05: T04→XGW01
F06: XGW01→T03 [Yes — next segment loop] | F07: XGW01→EE01 [No — all segments complete]

---

## P2_L3_PDW — Pit Dewatering (L3, sub of 2.3.2)

### Element Inventory (Pool: P2_L3_PDW_PL | Lanes: SCADA/Auto, Dewatering Operator)
| ID | BPMN Type | Name | Lane |
|----|-----------|------|------|
| P2_L3_PDW_SE | startEvent (timer) | Continuous — SCADA monitors sump level | P2_L3_PDW_LN_SCA |
| P2_L3_PDW_XGW01 | exclusiveGateway | Sump level above high setpoint? | P2_L3_PDW_LN_SCA |
| P2_L3_PDW_T01 | serviceTask | Start Pump (SCADA auto or operator manual) (2.3.2.1) | P2_L3_PDW_LN_SCA |
| P2_L3_PDW_T02 | task | Monitor Pump Operation and Telemetry | P2_L3_PDW_LN_OPR |
| P2_L3_PDW_XGW02 | exclusiveGateway | Pump fault alarm? | P2_L3_PDW_LN_OPR |
| P2_L3_PDW_T03 | task | Respond to Fault; Notify Maintenance | P2_L3_PDW_LN_OPR |
| P2_L3_PDW_XGW03 | exclusiveGateway | Sump level below low setpoint? | P2_L3_PDW_LN_SCA |
| P2_L3_PDW_T04 | serviceTask | Stop Pump; Record Run Time | P2_L3_PDW_LN_SCA |
| P2_L3_PDW_EE01 | endEvent | Pump stopped; run time recorded | P2_L3_PDW_LN_SCA |

### Sequence Flows (P2_L3_PDW)
F01: SE→XGW01 | F02: XGW01→T01 [Above setpoint] | F03: XGW01→SE [Below setpoint — loop/wait]
F04: T01→T02 | F05: T02→XGW02 | F06: XGW02→T03 [Fault] | F07: XGW02→XGW03 [Normal]
F08: T03→EE01 [Fault handled — pump offline] | F09: XGW03→SE [Above low — continue]
F10: XGW03→T04 [Below low setpoint] | F11: T04→EE01

---

## P2_L3_SSM — Slope Stability Monitoring (L3, sub of 2.3.3)

### Element Inventory (Pool: P2_L3_SSM_PL | Lanes: Auto/Monitoring System, Geotech Engineer, Mine Controller)
| ID | BPMN Type | Name | Lane |
|----|-----------|------|------|
| P2_L3_SSM_SE | startEvent (timer) | Scheduled scan interval (15-60 min) | P2_L3_SSM_LN_SYS |
| P2_L3_SSM_T01 | serviceTask | Collect Prism/Radar Displacement Data (2.3.3.1) | P2_L3_SSM_LN_SYS |
| P2_L3_SSM_T02 | task | Review Displacement Data vs. Alert Threshold | P2_L3_SSM_LN_GEO |
| P2_L3_SSM_XGW01 | exclusiveGateway | Alert threshold exceeded? | P2_L3_SSM_LN_GEO |
| P2_L3_SSM_T03 | task | Assess Stability Event; Determine Risk Level | P2_L3_SSM_LN_GEO |
| P2_L3_SSM_XGW02 | exclusiveGateway | Operational constraint required? | P2_L3_SSM_LN_GEO |
| P2_L3_SSM_T04 | task | Issue Exclusion Zone / Access Restriction | P2_L3_SSM_LN_GEO |
| P2_L3_SSM_T05 | task | Enforce Exclusion; Record TUM: OD or SBO | P2_L3_SSM_LN_MCT |
| P2_L3_SSM_ICE01 | intermediateCatchEvent (timer) | Await next scan interval | P2_L3_SSM_LN_SYS |
| P2_L3_SSM_EE01 | endEvent | Normal reading logged; continue monitoring | P2_L3_SSM_LN_SYS |
| P2_L3_SSM_EE02 | endEvent | Exclusion zone active; mine controller enforcing | P2_L3_SSM_LN_MCT |

### Sequence Flows (P2_L3_SSM)
F01: SE→T01 | F02: T01→T02 | F03: T02→XGW01 | F04: XGW01→EE01 [No — normal; loop to ICE01]
F05: XGW01→T03 [Alert] | F06: T03→XGW02 | F07: XGW02→ICE01 [No constraint needed]
F08: XGW02→T04 [Constraint needed] | F09: T04→T05 | F10: T05→EE02
F11: ICE01→SE [Next scan — loop back]
