# Pillar 1: Mine Planning & Scheduling — BPMN Generation Specification

## Purpose
Use alongside `01-mine-planning-and-scheduling.md` to generate Lucidchart BPMN 2.0 XML.
Same ID convention as Pillar 2 spec — prefix P1.

## Diagram Inventory
| Diagram ID | Level | Title | L3 Sub-diagrams |
|------------|-------|-------|-----------------|
| P1_L2_LOM | L2 | Strategic & Long-Term Planning | P1_L3_GEO, P1_L3_BLK, P1_L3_UPL, P1_L3_LOM, P1_L3_COG |
| P1_L2_MTP | L2 | Medium-Term Planning | P1_L3_PBS, P1_L3_FLT, P1_L3_BLD, P1_L3_GTC |
| P1_L2_STP | L2 | Short-Term Planning | P1_L3_POL, P1_L3_DPT, P1_L3_TGT, P1_L3_DST |
| P1_L2_SED | L2 | Shift Execution & Dispatch | P1_L3_RST, P1_L3_ASN, P1_L3_DIS, P1_L3_TRK |

---

## P1_L2_LOM — Strategic & Long-Term Planning (L2)

### Pool & Lanes
| ID | Name |
|----|------|
| P1_L2_LOM_PL | Strategic Planning |
| P1_L2_LOM_LN_GEO | Resource Geology |
| P1_L2_LOM_LN_GST | Geostatistics |
| P1_L2_LOM_LN_PLN | Mine Planning |
| P1_L2_LOM_LN_MGT | Management / QP |

### Element Inventory
| ID | BPMN Type | Name | Lane | Notes |
|----|-----------|------|------|-------|
| P1_L2_LOM_SE | startEvent (timer) | Annual LOM review or material trigger (>15% price change) | P1_L2_LOM_LN_MGT | |
| P1_L2_LOM_SP01 | subProcess (collapsed) | Geological Model Management (1.1.1) | P1_L2_LOM_LN_GEO | Ref P1_L3_GEO |
| P1_L2_LOM_SP02 | subProcess (collapsed) | Block Model Interpolation & Update (1.1.2) | P1_L2_LOM_LN_GST | Ref P1_L3_BLK |
| P1_L2_LOM_XGW01 | exclusiveGateway | Block model validation accepted? | P1_L2_LOM_LN_GST | |
| P1_L2_LOM_T01 | task | Re-estimate with corrected parameters | P1_L2_LOM_LN_GST | Loop back to SP02 |
| P1_L2_LOM_SP03 | subProcess (collapsed) | Ultimate Pit Limit Optimisation (1.1.3) | P1_L2_LOM_LN_PLN | Ref P1_L3_UPL |
| P1_L2_LOM_SP04 | subProcess (collapsed) | Life-of-Mine Schedule Generation (1.1.4) | P1_L2_LOM_LN_PLN | Ref P1_L3_LOM |
| P1_L2_LOM_SP05 | subProcess (collapsed) | Cut-Off Grade Calculation & Review (1.1.5) | P1_L2_LOM_LN_PLN | Ref P1_L3_COG |
| P1_L2_LOM_PGW01 | parallelGateway | [FORK] Schedule and COG calculated concurrently | P1_L2_LOM_LN_PLN | |
| P1_L2_LOM_PGW02 | parallelGateway | [JOIN] Both complete | P1_L2_LOM_LN_PLN | |
| P1_L2_LOM_T02 | task | Estimate and File Mineral Reserves (QP sign-off) | P1_L2_LOM_LN_MGT | |
| P1_L2_LOM_EE01 | endEvent | Block model released; UPL approved; LOM committed; Reserves filed | P1_L2_LOM_LN_MGT | |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P1_L2_LOM_F01 | P1_L2_LOM_SE | P1_L2_LOM_SP01 | |
| P1_L2_LOM_F02 | P1_L2_LOM_SP01 | P1_L2_LOM_SP02 | |
| P1_L2_LOM_F03 | P1_L2_LOM_SP02 | P1_L2_LOM_XGW01 | |
| P1_L2_LOM_F04 | P1_L2_LOM_XGW01 | P1_L2_LOM_SP03 | Yes — validation accepted |
| P1_L2_LOM_F05 | P1_L2_LOM_XGW01 | P1_L2_LOM_T01 | No — re-estimate |
| P1_L2_LOM_F06 | P1_L2_LOM_T01 | P1_L2_LOM_SP02 | Loop back |
| P1_L2_LOM_F07 | P1_L2_LOM_SP03 | P1_L2_LOM_PGW01 | |
| P1_L2_LOM_F08 | P1_L2_LOM_PGW01 | P1_L2_LOM_SP04 | Parallel branch 1 |
| P1_L2_LOM_F09 | P1_L2_LOM_PGW01 | P1_L2_LOM_SP05 | Parallel branch 2 |
| P1_L2_LOM_F10 | P1_L2_LOM_SP04 | P1_L2_LOM_PGW02 | |
| P1_L2_LOM_F11 | P1_L2_LOM_SP05 | P1_L2_LOM_PGW02 | |
| P1_L2_LOM_F12 | P1_L2_LOM_PGW02 | P1_L2_LOM_T02 | |
| P1_L2_LOM_F13 | P1_L2_LOM_T02 | P1_L2_LOM_EE01 | |

---

## P1_L3_GEO — Geological Model Management (L3)

### Lanes: Resource Geology (P1_L3_GEO_LN_GEO) | DB Admin (P1_L3_GEO_LN_DBA) | QP (P1_L3_GEO_LN_QP)

| ID | Type | Name | Lane |
|----|------|------|------|
| P1_L3_GEO_SE | startEvent (message) | New drill data submitted | P1_L3_GEO_LN_DBA |
| P1_L3_GEO_T01 | task | Validate and Import Drill Hole Data (1.1.1.1) | P1_L3_GEO_LN_DBA |
| P1_L3_GEO_XGW01 | exclusiveGateway | Validation passed? | P1_L3_GEO_LN_DBA |
| P1_L3_GEO_T02 | task | Issue Data Query; Await Correction | P1_L3_GEO_LN_DBA |
| P1_L3_GEO_T03 | task | Interpret and Update Geological Domains (1.1.1.2) | P1_L3_GEO_LN_GEO |
| P1_L3_GEO_T04 | task | Classify Mineral Resources (1.1.1.3) | P1_L3_GEO_LN_QP |
| P1_L3_GEO_EE01 | endEvent | Geological model updated; resource classification applied | P1_L3_GEO_LN_QP |

Flows: SE→T01 | T01→XGW01 | XGW01→T03[Pass] | XGW01→T02[Fail] | T02→T01[Loop — resubmit]
T03→T04 | T04→EE01

---

## P1_L3_BLK — Block Model Interpolation (L3)

### Lanes: Resource Geology (LN_GEO) | Geostatistics (LN_GST) | QP (LN_QP)

| ID | Type | Name | Lane |
|----|------|------|------|
| P1_L3_BLK_SE | startEvent | Geological model update released | P1_L3_BLK_LN_GEO |
| P1_L3_BLK_T01 | task | Composite Drill Hole Intervals (1.1.2.1) | P1_L3_BLK_LN_GEO |
| P1_L3_BLK_T02 | task | Model Variogram and Spatial Continuity (1.1.2.2) | P1_L3_BLK_LN_GST |
| P1_L3_BLK_T03 | task | Interpolate Block Grades (1.1.2.3) | P1_L3_BLK_LN_GST |
| P1_L3_BLK_T04 | task | Validate Block Model — swath plots, global mean (1.1.2.4) | P1_L3_BLK_LN_QP |
| P1_L3_BLK_XGW01 | exclusiveGateway | Validation accepted? | P1_L3_BLK_LN_QP |
| P1_L3_BLK_T05 | task | Re-estimate with corrected parameters | P1_L3_BLK_LN_GST |
| P1_L3_BLK_EE01 | endEvent | Block model validated and released | P1_L3_BLK_LN_QP |

Flows: SE→T01→T02→T03→T04→XGW01 | XGW01→EE01[Pass] | XGW01→T05[Fail] | T05→T03[Loop]

---

## P1_L3_UPL — Ultimate Pit Limit Optimisation (L3)

### Lanes: Mine Planning (LN_PLN) | VP Mining / Management (LN_MGT)

| ID | Type | Name | Lane |
|----|------|------|------|
| P1_L3_UPL_SE | startEvent | Block model released; price deck approved | P1_L3_UPL_LN_PLN |
| P1_L3_UPL_T01 | task | Parameterise Pit Optimisation (1.1.3.1) | P1_L3_UPL_LN_PLN |
| P1_L3_UPL_T02 | serviceTask | Generate Nested Pit Shells (LG algorithm) (1.1.3.2) | P1_L3_UPL_LN_PLN |
| P1_L3_UPL_T03 | task | Select Economic Pit Limit with VP sign-off (1.1.3.3) | P1_L3_UPL_LN_MGT |
| P1_L3_UPL_EE01 | endEvent | UPL selected and approved | P1_L3_UPL_LN_MGT |

Flows: SE→T01→T02→T03→EE01

---

## P1_L3_LOM — LOM Schedule Generation (L3)

### Lanes: Mine Planning (LN_PLN) | QP (LN_QP)

| ID | Type | Name | Lane |
|----|------|------|------|
| P1_L3_LOM_SE | startEvent | UPL selected | P1_L3_LOM_LN_PLN |
| P1_L3_LOM_T01 | task | Design Phase and Pushback Sequence (1.1.4.1) | P1_L3_LOM_LN_PLN |
| P1_L3_LOM_T02 | serviceTask | Schedule Ore and Waste by Period (optimiser) (1.1.4.2) | P1_L3_LOM_LN_PLN |
| P1_L3_LOM_T03 | task | Estimate and File Mineral Reserves (1.1.4.3) | P1_L3_LOM_LN_QP |
| P1_L3_LOM_EE01 | endEvent | LOM schedule committed; reserves filed | P1_L3_LOM_LN_QP |

Flows: SE→T01→T02→T03→EE01

---

## P1_L3_COG — Cut-Off Grade Calculation (L3)

### Lanes: Mine Planning (LN_PLN) | Finance (LN_FIN)

| ID | Type | Name | Lane |
|----|------|------|------|
| P1_L3_COG_SE | startEvent | Annual review or price/cost change trigger | P1_L3_COG_LN_PLN |
| P1_L3_COG_T01 | task | Calculate Break-Even Cut-Off Grade (1.1.5.1) | P1_L3_COG_LN_PLN |
| P1_L3_COG_T02 | task | Apply COG to Block Model; Review Ore Tonne Impact (1.1.5.2) | P1_L3_COG_LN_PLN |
| P1_L3_COG_XGW01 | exclusiveGateway | Material change to ore tonnes (>5%)? | P1_L3_COG_LN_PLN |
| P1_L3_COG_T03 | task | Trigger LOM Schedule Revision | P1_L3_COG_LN_PLN |
| P1_L3_COG_T04 | task | Approve and Publish COG Schedule | P1_L3_COG_LN_FIN |
| P1_L3_COG_EE01 | endEvent | COG schedule published; active for grade control | P1_L3_COG_LN_FIN |

Flows: SE→T01→T02→XGW01 | XGW01→T03[Yes] | XGW01→T04[No] | T03→T04 | T04→EE01

---

## P1_L2_MTP — Medium-Term Planning (L2)

### Pool & Lanes
| ID | Name |
|----|------|
| P1_L2_MTP_PL | Medium-Term Planning |
| P1_L2_MTP_LN_PLN | Senior Mine Planner |
| P1_L2_MTP_LN_GTC | Geotechnical Engineer |
| P1_L2_MTP_LN_MET | Chief Metallurgist |

### Element Inventory
| ID | Type | Name | Lane |
|----|------|------|------|
| P1_L2_MTP_SE | startEvent (timer) | Monthly planning cycle initiated | P1_L2_MTP_LN_PLN |
| P1_L2_MTP_SP01 | subProcess (collapsed) | Geotechnical Constraint Integration (1.2.4) | P1_L2_MTP_LN_GTC | Ref P1_L3_GTC; runs first |
| P1_L2_MTP_SP02 | subProcess (collapsed) | Phase/Pushback Sequencing (1.2.1) | P1_L2_MTP_LN_PLN | Ref P1_L3_PBS |
| P1_L2_MTP_SP03 | subProcess (collapsed) | Equipment Fleet Sizing & Allocation (1.2.2) | P1_L2_MTP_LN_PLN | Ref P1_L3_FLT |
| P1_L2_MTP_SP04 | subProcess (collapsed) | Blend Target Determination (1.2.3) | P1_L2_MTP_LN_MET | Ref P1_L3_BLD |
| P1_L2_MTP_PGW01 | parallelGateway | [FORK] Sequencing, Fleet, and Blend run in parallel | P1_L2_MTP_LN_PLN |
| P1_L2_MTP_PGW02 | parallelGateway | [JOIN] All three streams complete | P1_L2_MTP_LN_PLN |
| P1_L2_MTP_T01 | task | Publish Monthly Mine Plan | P1_L2_MTP_LN_PLN |
| P1_L2_MTP_EE01 | endEvent | Monthly plan approved; FMS configured; blend target issued | P1_L2_MTP_LN_PLN |

Flows: SE→SP01→PGW01 | PGW01→SP02[P1] | PGW01→SP03[P2] | PGW01→SP04[P3]
SP02→PGW02 | SP03→PGW02 | SP04→PGW02 | PGW02→T01→EE01

---

## P1_L3_PBS — Phase/Pushback Sequencing (L3) | P1_L3_FLT — Fleet Sizing (L3) | P1_L3_BLD — Blend Target (L3) | P1_L3_GTC — Geotechnical Constraints (L3)

### P1_L3_PBS (Lanes: Senior Mine Planner LN_PLN | Geotech LN_GTC)
T01: Define Active Bench/Phase Boundaries (1.2.1.1) | T02: Sequence Bench Advance for Grade/Blend (1.2.1.2)
Start: As-mined survey available + monthly plan active | End: Active bench list and advance sequence issued

### P1_L3_FLT (Lanes: Senior Mine Planner LN_PLN | Mine Superintendent LN_SUP)
T01: Calculate Fleet Requirement from Mining Rate (1.2.2.1) | T02: Allocate Equipment Units to Mining Areas (1.2.2.2)
Start: Monthly mining rate target set | End: Equipment allocation in FMS; planned downtime windows to Pillar 5

### P1_L3_BLD (Lanes: Senior Mine Planner LN_PLN | Chief Metallurgist LN_MET)
T01: Inventory Available Ore Sources and Grades (1.2.3.1) | T02: Optimise Feed Blend to Meet Mill Targets (1.2.3.2)
Start: Monthly plan start; stockpile grade model current | End: Mill feed blend plan issued to Processing

### P1_L3_GTC (Lanes: Geotech Engineer LN_GTC | Mine Planning LN_PLN)
T01: Review Slope Monitoring Trends vs. Design (1.2.4.1) | XGW01: Constraint change required? |
T02: Update Slope Design and Issue Constraints (1.2.4.2) [if Yes] | End: Constraints updated in mine planning software

---

## P1_L2_STP — Short-Term Planning (L2)

### Pool & Lanes: Mine Planning Engineer (LN_ENG) | Grade Control Geologist (LN_GCG) | Survey (LN_SRV) | FMS Interface (LN_FMS)

| ID | Type | Name | Lane |
|----|------|------|------|
| P1_L2_STP_SE | startEvent (message) | Blast completion report received OR weekly/daily cycle | P1_L2_STP_LN_ENG |
| P1_L2_STP_SP01 | subProcess (collapsed) | Polygon/Face Design & Sequencing (1.3.1) | P1_L2_STP_LN_ENG | Ref P1_L3_POL |
| P1_L2_STP_SP02 | subProcess (collapsed) | Drill Pattern Generation (1.3.2) | P1_L2_STP_LN_ENG | Ref P1_L3_DPT |
| P1_L2_STP_SP03 | subProcess (collapsed) | Daily Production Target Setting (1.3.3) | P1_L2_STP_LN_ENG | Ref P1_L3_TGT |
| P1_L2_STP_SP04 | subProcess (collapsed) | Material Destination Assignment (1.3.4) | P1_L2_STP_LN_ENG | Ref P1_L3_DST |
| P1_L2_STP_PGW01 | parallelGateway | [FORK] Drill pattern briefs + targets + destinations in parallel | P1_L2_STP_LN_ENG |
| P1_L2_STP_PGW02 | parallelGateway | [JOIN] | P1_L2_STP_LN_ENG |
| P1_L2_STP_ICE01 | intermediateCatchEvent (message) | Grade control assay results returned | P1_L2_STP_LN_GCG |
| P1_L2_STP_XGW01 | exclusiveGateway | Classification differs from model? | P1_L2_STP_LN_GCG |
| P1_L2_STP_T01 | task | Revise FMS Destination; Log Change Event | P1_L2_STP_LN_ENG |
| P1_L2_STP_EE01 | endEvent | Polygons in FMS; drill briefs issued; targets loaded; destinations active | P1_L2_STP_LN_FMS |

Flows: SE→SP01 | SP01→PGW01 | PGW01→SP02[P1] | PGW01→SP03[P2] | PGW01→SP04[P3]
SP02→PGW02 | SP03→PGW02 | SP04→PGW02 | PGW02→ICE01 | ICE01→XGW01
XGW01→T01[Yes] | XGW01→EE01[No] | T01→EE01

---

## P1_L3_POL through P1_L3_DST (L3 detail)

### P1_L3_POL — Polygon/Face Design (Lanes: Mine Planning Eng LN_ENG | Survey LN_SRV | Senior Mine Planner LN_SNR | FMS LN_FMS)
T01: Update As-Mined Surface (1.3.1.1) — Survey | T02: Design and Approve Dig Polygons (1.3.1.2) — Eng/SNR
T03: Upload Polygons to FMS and Blast Design Software — FMS | XGW01: All polygons approved? [No → rework]
Start: Survey data available; blast completion reported | End: All polygons uploaded to FMS

### P1_L3_DPT — Drill Pattern Generation (Lanes: Mine Planning Eng LN_ENG)
T01: Specify Drill Pattern Parameters from Polygon (1.3.2.1) | T02: Issue Drill Pattern Brief to D&B Engineer
Start: Dig polygons approved | End: Brief issued (triggers Pillar 2, 2.1.1)

### P1_L3_TGT — Daily Production Target Setting (Lanes: Mine Planning Eng LN_ENG | Mine Controller LN_MCT | FMS LN_FMS)
T01: Allocate Daily Ore/Waste Targets by Area (1.3.3.1) | T02: Issue Targets to Mine Controller; Upload to FMS (1.3.3.2)
Start: Daily planning cycle | End: Targets active in FMS production dashboard

### P1_L3_DST — Material Destination Assignment (Lanes: Mine Planning Eng LN_ENG | Grade Control LN_GCG | FMS LN_FMS)
T01: Assign Destination Based on Material Type and Blend (1.3.4.1) | T02: Upload to FMS
XGW01: Grade control revision required? | T03: Revise Destination Following GC Results (1.3.4.2) [if Yes]
Start: Polygons approved | End: Destinations active in FMS

---

## P1_L2_SED — Shift Execution & Dispatch (L2)

### Pool & Lanes: Shift Supervisor (LN_SUP) | Mine Controller (LN_MCT) | FMS Auto-dispatch (LN_FMS) | Operators (LN_OPR)

| ID | Type | Name | Lane |
|----|------|------|------|
| P1_L2_SED_SE | startEvent (timer) | Shift start time reached | P1_L2_SED_LN_SUP |
| P1_L2_SED_SP01 | subProcess (collapsed) | Shift Roster Generation (1.4.1) | P1_L2_SED_LN_SUP | Ref P1_L3_RST |
| P1_L2_SED_SP02 | subProcess (collapsed) | Operator-to-Equipment Assignment (1.4.2) | P1_L2_SED_LN_MCT | Ref P1_L3_ASN |
| P1_L2_SED_SP03 | subProcess (collapsed) | Fleet Dispatch Optimisation — continuous (1.4.3) | P1_L2_SED_LN_FMS | Ref P1_L3_DIS; loop marker |
| P1_L2_SED_SP04 | subProcess (collapsed) | Real-Time Production Tracking & Adjustment (1.4.4) | P1_L2_SED_LN_MCT | Ref P1_L3_TRK; parallel with SP03 |
| P1_L2_SED_PGW01 | parallelGateway | [FORK] Dispatch and Tracking run concurrently | P1_L2_SED_LN_MCT |
| P1_L2_SED_PGW02 | parallelGateway | [JOIN] Shift end | P1_L2_SED_LN_MCT |
| P1_L2_SED_T01 | task | Generate and Commit Shift Production Report (1.4.4.3) | P1_L2_SED_LN_MCT |
| P1_L2_SED_EE01 | endEvent | Shift report committed; actuals uploaded | P1_L2_SED_LN_MCT |

Flows: SE→SP01→SP02→PGW01 | PGW01→SP03[P1] | PGW01→SP04[P2]
SP03→PGW02[shift end] | SP04→PGW02 | PGW02→T01→EE01

### P1_L3_RST — Roster Generation | P1_L3_ASN — Assignment | P1_L3_DIS — Dispatch | P1_L3_TRK — Tracking

**P1_L3_RST** (Lanes: Shift Supervisor LN_SUP | FMS LN_FMS): T01: Compile Operator Availability (1.4.1.1) | T02: Finalise and Publish Roster (1.4.1.2) | XGW01: Shortfall? → contractor call-in

**P1_L3_ASN** (Lanes: Mine Controller LN_MCT | Operators LN_OPR | FMS LN_FMS):
T01: Conduct Equipment Pre-Use Check (1.4.2.1) | XGW01: Unserviceable? → P5 corrective WO + fleet adjustment
T02: Log Operator-Equipment Assignment in FMS (1.4.2.2) | End: operator_shift_assignment records committed

**P1_L3_DIS** (Lanes: FMS Auto-dispatch LN_FMS | Mine Controller LN_MCT):
T01: Execute Automatic Truck-to-Shovel Assignment (1.4.3.1) [loop per dispatch cycle — 30-60 sec]
XGW01: Production exception event? | T02: Override Dispatch; Record Reason Code (1.4.3.2) [if Yes]
Loop: continues until shift end event

**P1_L3_TRK** (Lanes: Mine Controller LN_MCT | Mine Planning Eng LN_ENG):
T01: Monitor Hourly Production Rate vs. Target (1.4.4.1) | XGW01: >10% behind? | T02: Adjust Operations (1.4.4.2) [if Yes]
ICE01: Slope alert intermediate event | T03: Classify TUM and enforce exclusion
ICE02: Crusher offline event | T04: Redirect ore trucks to ROM stockpile
Loop: continues until shift end
