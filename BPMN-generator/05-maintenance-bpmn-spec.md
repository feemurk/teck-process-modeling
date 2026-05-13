# Pillar 5: Maintenance & Reliability — BPMN Generation Specification

## Diagram Inventory
| Diagram ID | Level | Title | L3 Sub-diagrams |
|------------|-------|-------|-----------------|
| P5_L2_MPS | L2 | Maintenance Planning & Scheduling | P5_L3_CRT, P5_L3_PMM, P5_L3_WOR |
| P5_L2_PMX | L2 | PM & Predictive Maintenance Execution | P5_L3_SVC, P5_L3_CDM |
| P5_L2_CMX | L2 | Corrective / Reactive Maintenance | P5_L3_FDN, P5_L3_RPR, P5_L3_EPS |
| P5_L2_REL | L2 | Reliability Engineering & Asset Life | P5_L3_FMC, P5_L3_ALC |

---

## P5_L2_MPS — Maintenance Planning & Scheduling (L2)

### Pool & Lanes: Reliability Engineer LN_REL | Maintenance Planner LN_PLN | Maintenance Superintendent LN_SUP | EAM/SAP PM LN_EAM

| ID | Type | Name | Lane |
|----|------|------|------|
| P5_L2_MPS_SE | startEvent (timer) | Rolling planning cycle (weekly/monthly) | P5_L2_MPS_LN_PLN |
| P5_L2_MPS_SP01 | subProcess (collapsed) | Equipment Criticality Classification (5.1.1) | P5_L2_MPS_LN_REL | Ref P5_L3_CRT; annual |
| P5_L2_MPS_SP02 | subProcess (collapsed) | PM Program Management (5.1.2) | P5_L2_MPS_LN_PLN | Ref P5_L3_PMM |
| P5_L2_MPS_SP03 | subProcess (collapsed) | Work Order Prioritisation and Release (5.1.3) | P5_L2_MPS_LN_SUP | Ref P5_L3_WOR |
| P5_L2_MPS_T01 | serviceTask | Communicate Planned Downtime Windows to Pillar 1 | P5_L2_MPS_LN_PLN | Key cross-pillar output |
| P5_L2_MPS_EE01 | endEvent | Released work orders in queue; planned downtime issued | P5_L2_MPS_LN_PLN | |

Flows: SE→SP01→SP02→SP03→T01→EE01

### P5_L3_CRT — Criticality Classification (Lanes: Reliability Engineer, Maintenance Superintendent)
T01: Assess Production Consequence of Failure (5.1.1.1) | T02: Classify Asset Criticality A/B/C; Assign Strategy (5.1.1.2)
XGW01: Material change to criticality rating? [Yes → update PM program] [No → confirm existing]

### P5_L3_PMM — PM Program Management (Lanes: Maintenance Planner, Reliability Engineer, EAM)
T01: Define PM Tasks from OEM and Regulatory Schedule (5.1.2.1)
T02: Schedule PM Work Orders; Level Resources (5.1.2.2)
XGW01: Resource conflict with production schedule? [Yes → negotiate downtime window with Pillar 1]

### P5_L3_WOR — Work Order Prioritisation (Lanes: Maintenance Supervisor, Warehouse, EAM)
T01: Prioritise Work Orders P1-P4 (5.1.3.1) | T02: Kit Parts and Release Work Order (5.1.3.2)
XGW01: Parts in stock? [No → emergency procurement triggers P5_L3_EPS]

---

## P5_L2_PMX — PM & Predictive Maintenance Execution (L2)

### Pool & Lanes: FMS/EAM LN_SYS | Maintenance Supervisor LN_SUP | Tradesperson LN_TRD | Equipment Operator LN_OPR | Mine Controller (Pillar 2) LN_MCT

| ID | Type | Name | Lane | Notes |
|----|------|------|------|-------|
| P5_L2_PMX_SE | startEvent (message) | PM trigger fires; work order released; parts kitted | P5_L2_PMX_LN_SYS | |
| P5_L2_PMX_PGW01 | parallelGateway | [FORK] PM execution + continuous condition monitoring | P5_L2_PMX_LN_SYS | |
| P5_L2_PMX_SP01 | subProcess (collapsed) | Scheduled Service Execution (5.2.1) | P5_L2_PMX_LN_TRD | Ref P5_L3_SVC |
| P5_L2_PMX_SP02 | subProcess (collapsed) | Condition Monitoring (5.2.2) | P5_L2_PMX_LN_SYS | Ref P5_L3_CDM; continuous loop |
| P5_L2_PMX_PGW02 | parallelGateway | [JOIN] | P5_L2_PMX_LN_SYS | |
| P5_L2_PMX_EE01 | endEvent | Equipment returned to available fleet; work order closed | P5_L2_PMX_LN_MCT | |

Flows: SE→PGW01 | PGW01→SP01[PM execution] | PGW01→SP02[CM monitoring — parallel continuous]
SP01→PGW02 | SP02→PGW02[loop until shift end] | PGW02→EE01

### P5_L3_SVC — Scheduled Service Execution (Lanes: Supervisor, Tradesperson, Operator, Mine Controller/FMS)
| ID | Type | Name | Notes |
|----|------|------|-------|
| P5_L3_SVC_T01 | task | Take Equipment Out of Service; Notify FMS (5.2.1.1) | TUM:DT begins; work_order_id linked to delay_event |
| P5_L3_SVC_T02 | task | Obtain Permit to Work from Pillar 6 | Gate condition — P6 PTW required |
| P5_L3_SVC_T03 | task | Execute PM Tasks; Record Findings (5.2.1.2) | findings → potential additional WOs |
| P5_L3_SVC_XGW01 | exclusiveGateway | Safety defect found during service? | |
| P5_L3_SVC_T04 | task | Raise P1 Corrective WO; Notify Pillar 6 Safety | |
| P5_L3_SVC_T05 | task | Function Test; Pre-Start Inspection | |
| P5_L3_SVC_XGW02 | exclusiveGateway | Function test passed? | |
| P5_L3_SVC_T06 | task | Fault diagnosis — enters corrective flow (P5_L2_CMX) | |
| P5_L3_SVC_T07 | task | Cancel PTW; Return Equipment to Service; Update FMS (5.2.1.3) | TUM:DT ends |
| P5_L3_SVC_T08 | task | Close Work Order in EAM with Actuals | |
| P5_L3_SVC_EE01 | endEvent | Equipment in Available fleet; WO closed; TUM:DT closed | |

Flows: SE→T01→T02→T03→XGW01 | XGW01→T04[Safety defect] | XGW01→T05[Normal]
T04→T05 | T05→XGW02 | XGW02→T07[Pass] | XGW02→T06[Fail — corrective]
T07→T08→EE01

### P5_L3_CDM — Condition Monitoring (Lanes: Condition Monitoring Tech, Reliability Engineer, EAM)
T01: Monitor Continuous Condition Signals (5.2.2.1) [PI Historian — loop per sensor interval]
T02: Collect Periodic Condition Samples — oil, vibration, thermography (5.2.2.2) [schedule-triggered]
XGW01: Warning threshold exceeded? | T03: Generate Predictive Work Order (5.2.2.3) [if Yes]

---

## P5_L2_CMX — Corrective / Reactive Maintenance (L2)

### Pool & Lanes: Equipment Operator LN_OPR | Mine Controller LN_MCT | Maintenance Supervisor LN_SUP | Tradesperson LN_TRD | Procurement LN_PRC | Pillar 6 PTW LN_PTW

| ID | Type | Name | Lane | Notes |
|----|------|------|------|-------|
| P5_L2_CMX_SE | startEvent (message) | Equipment failure detected | P5_L2_CMX_LN_OPR | Operator report or automated alarm |
| P5_L2_CMX_SP01 | subProcess (collapsed) | Failure Detection and Notification (5.3.1) | P5_L2_CMX_LN_MCT | Ref P5_L3_FDN; TUM:DT initiated |
| P5_L2_CMX_SP02 | subProcess (collapsed) | Fault Diagnosis and Repair (5.3.2) | P5_L2_CMX_LN_TRD | Ref P5_L3_RPR |
| P5_L2_CMX_XGW01 | exclusiveGateway | Parts in site inventory? | P5_L2_CMX_LN_TRD | |
| P5_L2_CMX_SP03 | subProcess (collapsed) | Emergency Parts and Logistics (5.3.3) | P5_L2_CMX_LN_PRC | Ref P5_L3_EPS; extends TUM:DT |
| P5_L2_CMX_T01 | task | Execute Repair; Record ISO 14224 Failure Mode | P5_L2_CMX_LN_TRD | |
| P5_L2_CMX_T02 | task | Cancel PTW; Return to Service; Update FMS | P5_L2_CMX_LN_MCT | TUM:DT ends |
| P5_L2_CMX_T03 | task | Close Corrective Work Order with All Actuals | P5_L2_CMX_LN_SUP | equipment_failure_record committed |
| P5_L2_CMX_EE01 | endEvent | Equipment available; TUM:DT closed; failure record committed | P5_L2_CMX_LN_MCT | |

Flows: SE→SP01→SP02→XGW01 | XGW01→T01[Parts available] | XGW01→SP03[Parts not available]
SP03→T01 | T01→T02→T03→EE01

### P5_L3_FDN — Failure Detection (Lanes: Operator, Mine Controller/DCS, Maintenance Supervisor, EAM)
T01: Report Failure; Initiate TUM:DT Record in FMS (5.3.1.1) [work_order_id must be linked]
T02: Assess Failure; Dispatch Maintenance Team (5.3.1.2) | T03: Obtain PTW from Pillar 6 (P6 gate)
XGW01: Priority P1 (safety or Class A)? [Yes → immediate; No → prioritise]

### P5_L3_RPR — Fault Diagnosis and Repair (Lanes: Tradesperson, Maintenance Supervisor, EAM)
T01: Diagnose Fault; Record ISO 14224 Failure Mode Code (5.3.2.1) [pre-repair state documented]
T02: Execute Repair; Record Parts Consumed (5.3.2.2) [part number, quantity against WO]
T03: Function Test | XGW01: Test passed? [No → diagnose again; loop] [Yes → T04]
T04: Return Equipment to Service; Close WO (5.3.2.3)

### P5_L3_EPS — Emergency Parts (Lanes: Maintenance Supervisor, Procurement, Warehouse, ERP)
T01: Identify Part and Check Site Inventory (5.3.3.1) | [Already confirmed not in stock]
T02: Execute Emergency Procurement; Coordinate Freight (5.3.3.2)
ICE01: timerEvent — parts arrival (hours to days depending on site remoteness)
T03: Parts received; issue from receiving → repair can proceed

---

## P5_L2_REL — Reliability Engineering & Asset Life (L2)

### Pool & Lanes: Reliability Engineer LN_REL | Maintenance Superintendent LN_SUP | Finance LN_FIN | EAM/Analytics LN_EAM

| ID | Type | Name | Lane |
|----|------|------|------|
| P5_L2_REL_SE | startEvent (timer) | Monthly/quarterly reliability review | P5_L2_REL_LN_REL |
| P5_L2_REL_SP01 | subProcess (collapsed) | FMECA Update (5.4.1) | P5_L2_REL_LN_REL | Ref P5_L3_FMC |
| P5_L2_REL_XGW01 | exclusiveGateway | PM program changes required? | P5_L2_REL_LN_REL | |
| P5_L2_REL_T01 | task | Issue PM Program Change Request to EAM | P5_L2_REL_LN_REL | |
| P5_L2_REL_SP02 | subProcess (collapsed) | Asset Lifecycle Management (5.4.2) | P5_L2_REL_LN_REL | Ref P5_L3_ALC |
| P5_L2_REL_XGW02 | exclusiveGateway | Repair-vs-replace threshold reached? | P5_L2_REL_LN_REL | |
| P5_L2_REL_T02 | task | Issue Capital Expenditure Request to Finance | P5_L2_REL_LN_FIN | Feeds Pillar 1 LOM capital plan |
| P5_L2_REL_EE01 | endEvent | FMECA updated; PM program revised; CapEx request submitted | P5_L2_REL_LN_REL | |

Flows: SE→SP01→XGW01 | XGW01→T01[Yes] | XGW01→SP02[No/concurrent]
T01→SP02 | SP02→XGW02 | XGW02→T02[Threshold reached] | XGW02→EE01[Continue]
T02→EE01

### P5_L3_FMC — FMECA Update (Lanes: Reliability Engineer, Maintenance Superintendent)
T01: Analyse Failure History by Equipment Class (5.4.1.1) — MTBF/MTTR/downtime cost
T02: Update FMECA; Revise Maintenance Tasks (5.4.1.2) [change task intervals or add CM tasks]

### P5_L3_ALC — Asset Lifecycle Management (Lanes: Reliability Engineer, Finance)
T01: Track Cumulative Asset Costs vs. Replacement Value (5.4.2.1) [continuous via EAM]
XGW01: Cost-to-replace threshold exceeded? | T02: Conduct Repair-vs-Replace Analysis (5.4.2.2)
T03: Issue Recommendation (major overhaul / component exchange / replace)
