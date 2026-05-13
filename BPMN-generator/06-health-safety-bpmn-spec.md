# Pillar 6: Health & Safety — BPMN Generation Specification

## Diagram Inventory
| Diagram ID | Level | Title | L3 Sub-diagrams |
|------------|-------|-------|-----------------|
| P6_L2_HZD | L2 | Hazard Identification & Risk Control | P6_L3_HIR, P6_L3_FLA |
| P6_L2_PTW | L2 | Permit to Work | P6_L3_ISO, P6_L3_ISS, P6_L3_CAN |
| P6_L2_INC | L2 | Incident Management | P6_L3_DET, P6_L3_INV, P6_L3_CAT |
| P6_L2_OHM | L2 | Occupational Health Monitoring | P6_L3_DST, P6_L3_NOS |
| P6_L2_SPC | L2 | Safety Performance & Regulatory Compliance | (tasks at L3 directly) |

---

## P6_L2_HZD — Hazard Identification & Risk Control (L2)

### Pool & Lanes: Safety Officer LN_SAF | Area Superintendent LN_SUP | Work Team LN_WRK | Facilitator LN_FAC

| ID | Type | Name | Lane |
|----|------|------|------|
| P6_L2_HZD_SE | startEvent (message) | New work area/activity or scheduled HAZID review | P6_L2_HZD_LN_SAF |
| P6_L2_HZD_SP01 | subProcess (collapsed) | Formal Risk Assessment — HAZID/HIRA (6.1.1) | P6_L2_HZD_LN_FAC | Ref P6_L3_HIR |
| P6_L2_HZD_SP02 | subProcess (collapsed) | Field-Level Hazard Assessment — FLHA (6.1.2) | P6_L2_HZD_LN_WRK | Ref P6_L3_FLA; before every task |
| P6_L2_HZD_XGW01 | exclusiveGateway | Unacceptable residual hazard identified? | P6_L2_HZD_LN_SAF | |
| P6_L2_HZD_T01 | task | Issue Stop-Work; Escalate to Supervisor | P6_L2_HZD_LN_WRK | |
| P6_L2_HZD_EE01 | endEvent | Risk register updated; FLHA complete; work may proceed | P6_L2_HZD_LN_SAF | |
| P6_L2_HZD_EE02 | endEvent (error) | Stop-work in effect; hazard not controlled | P6_L2_HZD_LN_SUP | |

Flows: SE→SP01→SP02→XGW01 | XGW01→EE01[Acceptable] | XGW01→T01[Unacceptable] | T01→EE02

### P6_L3_HIR — Formal Risk Assessment / HAZID-HIRA (Lanes: Safety Officer, Area Superintendent, Facilitator, SME)
T01: Identify Hazards for Activity or Area (6.1.1.1) [structured prompts, ICMM 13 fatal hazard categories]
T02: Rate Risk; Assign Controls (6.1.1.2) [hierarchy of controls; inherent → residual risk]
XGW01: Residual risk below tolerable threshold? [No → escalate to engineering control] [Yes → document]
T03: Update Risk Register; Assign Control Owners; Set Review Date

### P6_L3_FLA — Field-Level Hazard Assessment (Lanes: Supervisor, Work Team)
T01: Conduct Pre-Task FLHA at Work Location (6.1.2.1) [What? What can go wrong? Controls? Adequate?]
T02: All Workers Sign FLHA | XGW01: Any worker identifies uncontrolled hazard?
[Yes → stop work; escalate] [No → proceed with task]

---

## P6_L2_PTW — Permit to Work (L2)

### Pool & Lanes: Issuing Authority (Area Superintendent) LN_ISS | Permit Holder (Tradesperson/Operator) LN_HLD | Authorised Isolator LN_ISO | PTW System LN_SYS

**CROSS-PILLAR NOTE**: This process gates Pillar 5 (maintenance work order execution) and
constrains Pillar 2 (blast exclusion, geotechnical exclusion). The permit_id must appear
in the associated work_order_id record (Pillar 5) and blast_event_id (Pillar 2 where applicable).

| ID | Type | Name | Lane | Notes |
|----|------|------|------|-------|
| P6_L2_PTW_SE | startEvent (message) | Work request received for high-risk activity | P6_L2_PTW_LN_ISS | From Pillar 5 WO or Pillar 2 blast plan |
| P6_L2_PTW_SP01 | subProcess (collapsed) | Permit Preparation & Hazard Control Verification (6.2.1) | P6_L2_PTW_LN_ISS | Ref P6_L3_ISO |
| P6_L2_PTW_T01 | serviceTask | Issue Permit to Work; Record Active Status in PTW System (6.2.1.2) | P6_L2_PTW_LN_SYS | |
| P6_L2_PTW_ICE01 | intermediateCatchEvent (message) | Work complete signal from Permit Holder | P6_L2_PTW_LN_HLD | |
| P6_L2_PTW_ICE02 | intermediateCatchEvent (signal) | Conditions changed — permit suspension required | P6_L2_PTW_LN_ISS | errorBoundary on ICE01 |
| P6_L2_PTW_T02 | task | Suspend Permit; Re-verify Conditions | P6_L2_PTW_LN_ISS | Conditions must be re-confirmed |
| P6_L2_PTW_SP02 | subProcess (collapsed) | Permit Cancellation (6.2.2) | P6_L2_PTW_LN_ISS | Ref P6_L3_CAN |
| P6_L2_PTW_EE01 | endEvent | Permit cancelled; isolation removed; equipment serviceable | P6_L2_PTW_LN_SYS | Pillar 5 WO may now proceed to close |

Flows: SE→SP01→T01 | T01→ICE01[Awaiting work complete signal]
ICE02→T02[Suspension] | T02→T01[Re-issue after re-verification]
ICE01→SP02→EE01

### P6_L3_ISO — Isolation & Pre-conditions (Lanes: Issuing Authority, Authorised Isolator, PTW System)
T01: Verify Isolation Points from Energy Isolation Register | T02: Apply LOTO Devices
T03: Test-Before-Touch — confirm energy is dead | XGW01: All energy sources isolated and confirmed?
[Yes → issue isolation certificate] [No → isolate remaining sources; loop]
T04: Issue Isolation Certificate | T05: Complete Pre-conditions Checklist; Sign

### P6_L3_ISS — Permit Issuance (detail — within SP01 above)
T01: Review Pre-conditions Checklist (all items signed) | T02: Confirm Workers Briefed; PPE Available
T03: Sign and Issue Permit | T04: Hand Permit to Permit Holder

### P6_L3_CAN — Permit Cancellation (Lanes: Permit Holder, Issuing Authority, Authorised Isolator)
T01: Confirm All Workers Clear; Area Safe | T02: Return Permit to Issuing Authority
T03: Issuing Authority Signs Cancellation Section | T04: Remove LOTO; Restore Energy
T05: Confirm Equipment Serviceable | T06: Update PTW System Status to Cancelled

---

## P6_L2_INC — Incident Management (L2)

### Pool & Lanes: Worker/Operator LN_WRK | Supervisor LN_SUP | Safety Officer LN_SAF | Incident Investigator LN_INV | Regulatory Authority LN_REG

| ID | Type | Name | Lane | Notes |
|----|------|------|------|-------|
| P6_L2_INC_SE | startEvent (signal) | Incident or near-miss occurs | P6_L2_INC_LN_WRK | |
| P6_L2_INC_SP01 | subProcess (collapsed) | Incident Detection and Notification (6.3.1) | P6_L2_INC_LN_SUP | Ref P6_L3_DET |
| P6_L2_INC_T01 | task | Classify Severity; Determine Regulatory Notification | P6_L2_INC_LN_SAF | |
| P6_L2_INC_XGW01 | exclusiveGateway | Regulatory notification required? | P6_L2_INC_LN_SAF | Jurisdiction-specific timeframe |
| P6_L2_INC_T02 | task | Submit Regulatory Notification within Mandated Timeframe | P6_L2_INC_LN_REG | MSHA 8hr/WorkSafeBC immediate/SERNAGEOMIN 24hr |
| P6_L2_INC_SP02 | subProcess (collapsed) | Incident Investigation (6.3.2) | P6_L2_INC_LN_INV | Ref P6_L3_INV |
| P6_L2_INC_SP03 | subProcess (collapsed) | Corrective Action Tracking (6.3.3) | P6_L2_INC_LN_SAF | Ref P6_L3_CAT |
| P6_L2_INC_EE01 | endEvent | Incident investigated; corrective actions assigned; regulatory notifications filed | P6_L2_INC_LN_SAF | |

Flows: SE→SP01→T01→XGW01 | XGW01→T02[Required] | XGW01→SP02[Not required]
T02→SP02 | SP02→SP03→EE01

### P6_L3_DET — Detection & Notification (Lanes: Worker, Supervisor, Safety Officer, DCS/FMS)
T01: Report Incident; Secure Scene (6.3.1.1) | T02: Site Manager Notified | T03: FLHA and PTW records secured as evidence
XGW01: Emergency response required? [Yes → first aid/emergency services; parallel path]

### P6_L3_INV — Incident Investigation (Lanes: Investigator, Safety Officer, Area Superintendent)
T01: Collect Evidence; Retrieve Operational Data (6.3.2.1) [FMS from P2, PI Historian from P3, PTW from P6]
T02: Conduct Witness Interviews | T03: Determine Causes — ICAM/5-Why/Bowtie (6.3.2.2)
T04: Develop Corrective Actions — specific, assigned, time-bound
XGW01: Investigation level — independent (fatality/serious) or supervisor (recordable/near-miss)?

### P6_L3_CAT — Corrective Action Tracking (Lanes: Safety Officer, Responsible Person)
T01: Monitor Action Register; Alert on Approaching Due Dates | T02: Responsible Person Updates Status
XGW01: Action implemented and verified? [Yes → close] [No → escalate if overdue]
T03: Verify Implementation Effectiveness | T04: Close Action in Safety Management System

---

## P6_L2_OHM — Occupational Health Monitoring (L2)

### Pool & Lanes: Occupational Hygienist LN_HYG | External Laboratory LN_LAB | Safety Officer LN_SAF | Workers LN_WRK

| ID | Type | Name | Lane |
|----|------|------|------|
| P6_L2_OHM_SE | startEvent (timer) | Scheduled monitoring interval | P6_L2_OHM_LN_HYG |
| P6_L2_OHM_PGW01 | parallelGateway | [FORK] Dust/chemical + noise/vibration monitoring concurrent | P6_L2_OHM_LN_HYG |
| P6_L2_OHM_SP01 | subProcess (collapsed) | Dust and Airborne Contaminant Monitoring (6.4.1) | P6_L2_OHM_LN_HYG | Ref P6_L3_DST |
| P6_L2_OHM_SP02 | subProcess (collapsed) | Noise and Vibration Monitoring (6.4.2) | P6_L2_OHM_LN_HYG | Ref P6_L3_NOS |
| P6_L2_OHM_PGW02 | parallelGateway | [JOIN] Both monitoring types complete | P6_L2_OHM_LN_HYG |
| P6_L2_OHM_T01 | task | Compare Results to OELs; Determine Compliance Status | P6_L2_OHM_LN_SAF |
| P6_L2_OHM_XGW01 | exclusiveGateway | OEL exceedance identified? | P6_L2_OHM_LN_SAF |
| P6_L2_OHM_T02 | task | Issue Corrective Action; Engineering Control Recommendation | P6_L2_OHM_LN_SAF |
| P6_L2_OHM_T03 | task | Communicate Results to Workers; Enrol in Medical Surveillance | P6_L2_OHM_LN_WRK |
| P6_L2_OHM_EE01 | endEvent | Exposure monitoring records in safety management system | P6_L2_OHM_LN_HYG |

Flows: SE→PGW01 | PGW01→SP01[P1] | PGW01→SP02[P2]
SP01→PGW02 | SP02→PGW02 | PGW02→T01→XGW01
XGW01→T02[Exceedance] | XGW01→T03[Compliant] | T02→T03→EE01

### P6_L3_DST — Dust Monitoring (Lanes: Hygienist, External Lab, Safety Officer)
T01: Attach Personal Air Sampling Pump to Worker | T02: Collect PBZ Sample for Full Shift
T03: Submit to NATA-Accredited Lab | ICE01: timerEvent — lab TAT
T04: Compare to OEL (Red Dog: MSHA 30 CFR Part 57; HVC: WorkSafeBC; QB/CdA: SERNAGEOMIN)

### P6_L3_NOS — Noise Monitoring (Lanes: Hygienist, Workers, Safety Officer)
T01: Attach Noise Dosimeter to Worker | T02: Collect Shift Noise Dose
T03: Calculate dB(A) TWA | XGW01: Exceeds 85 dB(A) action level?
[Yes → enrol in hearing conservation programme; engineering noise control review]

---

## P6_L2_SPC — Safety Performance & Regulatory Compliance (L2)

### Pool & Lanes: Safety Manager LN_MGR | Safety Officer LN_SAF | Regulatory Authority LN_REG | Corporate HSE LN_CHR

| ID | Type | Name | Lane |
|----|------|------|------|
| P6_L2_SPC_SE | startEvent (timer) | Monthly reporting cycle OR regulatory inspection event | P6_L2_SPC_LN_MGR |
| P6_L2_SPC_PGW01 | parallelGateway | [FORK] KPI reporting + regulatory management concurrent | P6_L2_SPC_LN_MGR |
| P6_L2_SPC_T01 | task | Calculate Safety KPIs — LTIFR, TRIFR, near-miss rate (6.5.1) | P6_L2_SPC_LN_SAF |
| P6_L2_SPC_T02 | task | Produce Monthly KPI Report; Submit to Corporate HSE | P6_L2_SPC_LN_MGR |
| P6_L2_SPC_T03 | task | Manage Regulatory Inspection Response (6.5.2) | P6_L2_SPC_LN_REG |
| P6_L2_SPC_XGW01 | exclusiveGateway | Citation or order issued? | P6_L2_SPC_LN_MGR |
| P6_L2_SPC_T04 | task | Submit Formal Response within Mandated Timeframe | P6_L2_SPC_LN_REG |
| P6_L2_SPC_T05 | task | Raise Corrective Actions from Citation | P6_L2_SPC_LN_SAF |
| P6_L2_SPC_PGW02 | parallelGateway | [JOIN] | P6_L2_SPC_LN_MGR |
| P6_L2_SPC_EE01 | endEvent | KPI report issued; regulatory compliance status updated | P6_L2_SPC_LN_MGR |

Flows: SE→PGW01 | PGW01→T01→T02[KPI stream] | PGW01→T03[Reg stream]
T03→XGW01 | XGW01→T04→T05[Citation issued] | XGW01→PGW02[No citation]
T05→PGW02 | T02→PGW02 | PGW02→EE01
