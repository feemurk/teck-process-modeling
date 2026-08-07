# Pillar 4: Logistics & Outbound — BPMN Generation Specification

## Lucidchart BPMN 2.0 XML Notes
- Use `isExecutable="false"` on all processes (documentation model, not executable)
- Lane `flowNodeRef` elements must list every task/gateway/event ID that sits in that lane
- All `sequenceFlow` elements must reference valid `sourceRef` and `targetRef` IDs

### DI geometry — Lucidchart does NOT auto-layout
**Lucidchart honours the `<bpmndi:BPMNDiagram>` coordinates literally.** It does not
re-arrange anything on import. Placeholder coordinates (`x="0" y="0"` on every shape)
produce an import in which every shape is stacked on a single point in the corner and the
lanes render empty. Real computed coordinates are mandatory.

Do not hand-compute the geometry. Emit the model XML first, then run the repo tooling:

```
python tools/bpmn_layout.py output/pillar-04     # computes DI geometry in place
python tools/bpmn_verify.py output/pillar-04     # must PASS before any import
```

`bpmn_layout.py` derives the layout from the sequence-flow graph and rewrites only the
DI block — all model XML and inline comments stay byte-identical, so it is safe to re-run.
See the Verification Gate section of `00-bpmn-prompt-template.md` for the full protocol.

## Diagram Inventory
| Diagram ID | Level | Title | L3 Sub-diagrams |
|------------|-------|-------|-----------------|
| P4_L2_CHD | L2 | Concentrate Handling | P4_L3_STG, P4_L3_RCL |
| P4_L2_TRP | L2 | Inland Transport | P4_L3_WBG, P4_L3_HDL |
| P4_L2_PRT | L2 | Port Operations | P4_L3_RCP, P4_L3_VLD |
| P4_L2_COM | L2 | Commercial Documentation | P4_L3_COA, P4_L3_BOL, P4_L3_INV |

---

## P4_L2_CHD — Concentrate Handling (L2)

### Pool & Lanes: Filter Plant Interface LN_FLT | Shed Operator LN_SHD | Logistics Coordinator LN_LOG | Metallurgist LN_MET | FEL Operator LN_FEL

| ID | Type | Name | Lane | Notes |
|----|------|------|------|-------|
| P4_L2_CHD_SE | startEvent (message) | Filter cake being discharged from filter plant | P4_L2_CHD_LN_FLT | Pillar 3 handoff |
| P4_L2_CHD_SP01 | subProcess (collapsed) | Concentrate Storage (4.1.1) | P4_L2_CHD_LN_SHD | Ref P4_L3_STG; P754 CTP-2 |
| P4_L2_CHD_ICE01 | intermediateCatchEvent (message) | Dispatch instruction received | P4_L2_CHD_LN_LOG | |
| P4_L2_CHD_SP02 | subProcess (collapsed) | Stockpile Reclaim (4.1.2) | P4_L2_CHD_LN_FEL | Ref P4_L3_RCL |
| P4_L2_CHD_EE01 | endEvent | Transport vehicle loaded; ready for weighbridge | P4_L2_CHD_LN_LOG | |

Flows: SE→SP01 | SP01→ICE01[continuous storage while awaiting dispatch]
ICE01→SP02 | SP02→EE01

### P4_L3_STG — Concentrate Storage (Lanes: Shed Operator, Metallurgist, DCS belt weigher)
| ID | Type | Name | P754 |
|----|------|------|------|
| P4_L3_STG_T01 | serviceTask | Receive Filter Cake at Shed; Record Belt Weigher (4.1.1.1) | CTP-2 — Concentrator to Logistics |
| P4_L3_STG_T02 | task | Build Shed Stockpile by Grade Zone (4.1.1.2) | |
| P4_L3_STG_T03 | task | Monitor and Manage Moisture During Storage (4.1.1.3) | P754 P7,P8 |
| P4_L3_STG_XGW01 | exclusiveGateway | Moisture approaching contract maximum? | |
| P4_L3_STG_T04 | task | Initiate Corrective Action [turning, expedite dispatch] | |
| P4_L3_STG_ICE01 | intermediateCatchEvent (timer) | Scheduled moisture sampling interval (weekly) | |

Flows: SE→T01→T02→ICE01[loop] | ICE01→T03→XGW01 | XGW01→ICE01[Normal] | XGW01→T04[Alert] | T04→ICE01

### P4_L3_RCL — Stockpile Reclaim (Lanes: Logistics Coordinator, Metallurgist, FEL Operator)
T01: Optimise Blend for Dispatch Specification (4.1.2.2) [first — plan the blend]
T02: Execute FEL Reclaim per Zone (4.1.2.1) [per zone in planned proportion]
XGW01: More zones to reclaim? [Yes → T02 loop] [No → EE01]
End: Dispatch lot loaded; inventory decremented in ERP

---

## P4_L2_TRP — Inland Transport (L2)

### Pool & Lanes: Weighbridge Operator LN_WBG | Logistics Coordinator LN_LOG | Transport Carrier LN_TRP | ERP LN_ERP

| ID | Type | Name | Lane | Notes |
|----|------|------|------|-------|
| P4_L2_TRP_SE | startEvent | Vehicle loaded; ready for weighbridge | P4_L2_TRP_LN_LOG | |
| P4_L2_TRP_SP01 | subProcess (collapsed) | Weighbridge Operations (4.2.1) | P4_L2_TRP_LN_WBG | Ref P4_L3_WBG; P754 CTP-3 |
| P4_L2_TRP_T01 | serviceTask | Generate Bill of Lading in ERP (4.2.1.4) | P4_L2_TRP_LN_ERP | |
| P4_L2_TRP_SP02 | subProcess (collapsed) | Road/Rail Transport (4.2.2) | P4_L2_TRP_LN_TRP | Ref P4_L3_HDL |
| P4_L2_TRP_XGW01 | exclusiveGateway | More vehicles in dispatch lot? | P4_L2_TRP_LN_LOG | |
| P4_L2_TRP_EE01 | endEvent | All vehicles dispatched; BoL issued; in transit | P4_L2_TRP_LN_LOG | |

Flows: SE→SP01→XGW01 | XGW01→SP01[Yes — next vehicle in lot] | XGW01→T01[No — lot complete]
T01→SP02→EE01

### P4_L3_WBG — Weighbridge Operations (Lanes: Weighbridge Op, Logistics Coordinator, ERP)
| ID | Type | Name | P754 |
|----|------|------|------|
| P4_L3_WBG_T01 | task | Weigh Vehicle Tare (4.2.1.1) | CTP-3 component |
| P4_L3_WBG_T02 | task | Load Concentrate to Transport Vehicle (4.2.1.2) | |
| P4_L3_WBG_T03 | task | Weigh Loaded Vehicle Gross; Calculate Net Wet Tonnes (4.2.1.3) | CTP-3 — primary mass |
| P4_L3_WBG_T04 | serviceTask | Record Weighbridge Ticket in System; Update ERP Inventory | |
| P4_L3_WBG_EE01 | endEvent | Net wet tonnes confirmed; weighbridge ticket issued | |

### P4_L3_HDL — Road/Rail Transport (Lanes: Logistics Coordinator, Transport Carrier, GPS/Telematics)
T01: Dispatch Vehicle; Issue Transport Documents (4.2.2.1) [dangerous goods declaration]
T02: Track In-Transit Shipment via GPS/Rail Tracking (4.2.2.2) [continuous until arrival]
XGW01: ETA deviation? [Yes → notify port/vessel scheduling] [No → continue]
T03: Vehicle Arrives at Port → triggers P4_L2_PRT Port Reception
T04: Calculate Transit Loss — port weighbridge vs. site BoL (4.2.2.3)

---

## P4_L2_PRT — Port Operations (L2)

### Pool & Lanes: Port Logistics Manager LN_PLM | Port Weighbridge Operator LN_PWB | Port Operator LN_OPR | Shiploader Operator LN_SHL | Independent Surveyor LN_SRV | Sampling Technician LN_SMP

| ID | Type | Name | Lane | Notes |
|----|------|------|------|-------|
| P4_L2_PRT_SE | startEvent (message) | Transport vehicles arriving at port; vessel arrival per schedule | P4_L2_PRT_LN_PLM | |
| P4_L2_PRT_PGW01 | parallelGateway | [FORK] Reception and vessel preparation concurrent | P4_L2_PRT_LN_PLM | |
| P4_L2_PRT_SP01 | subProcess (collapsed) | Port Reception (4.3.1) | P4_L2_PRT_LN_PWB | Ref P4_L3_RCP; P754 CTP-4 |
| P4_L2_PRT_T01 | task | Assign Berth and Complete Pre-Loading Checks (4.3.2.1) | P4_L2_PRT_LN_SRV | Parallel with reception |
| P4_L2_PRT_PGW02 | parallelGateway | [JOIN] Reception complete and vessel cleared | P4_L2_PRT_LN_PLM | |
| P4_L2_PRT_SP02 | subProcess (collapsed) | Vessel Loading (4.3.2) | P4_L2_PRT_LN_SHL | Ref P4_L3_VLD; P754 CTP-5 |
| P4_L2_PRT_EE01 | endEvent | Vessel loaded and departed; draft survey complete; umpire sample dispatched | P4_L2_PRT_LN_SRV | |

Flows: SE→PGW01 | PGW01→SP01[P1 reception stream] | PGW01→T01[P2 vessel prep]
SP01→PGW02 | T01→PGW02 | PGW02→SP02→EE01

### P4_L3_RCP — Port Reception (Lanes: Port Weighbridge Op, Port Logistics Manager, ERP)
T01: Weigh Arriving Vehicles at Port Weighbridge (4.3.1.1) P754 CTP-4
T02: Calculate Transit Loss vs. BoL | T03: Log Port Receipt; Update Port Inventory (4.3.1.2)
T04: Assign Port Shed Zone; Manage Port Stockpile (4.3.1.3)
XGW01: More vehicles to receive? [Yes → T01 loop] [No → EE]

### P4_L3_VLD — Vessel Loading (Lanes: Surveyor, Shiploader Operator, Sampling Technician, Port Logistics Manager, Vessel Master)
| ID | Type | Name | Lane | P754 |
|----|------|------|------|------|
| P4_L3_VLD_T01 | task | Conduct Initial Draft Survey (4.3.2.2) | LN_SRV | CTP-5 baseline |
| P4_L3_VLD_PGW01 | parallelGateway | [FORK] Loading + sampling concurrent | LN_SHL | |
| P4_L3_VLD_T02 | task | Execute Shiploader Operations — belt weigher cross-check (4.3.2.3) | LN_SHL | P754 P1,P7 cross-check only |
| P4_L3_VLD_T03 | task | Collect Continuous Belt Sample throughout Loading (4.3.2.4) | LN_SMP | P754 CTP-5 commercial grade |
| P4_L3_VLD_PGW02 | parallelGateway | [JOIN] Loading and sampling both complete | LN_SHL | |
| P4_L3_VLD_ICE01 | intermediateCatchEvent (error) | Loading interrupted | LN_SHL | Delay documented in Statement of Facts |
| P4_L3_VLD_T04 | task | Seal Hatches; Issue Statement of Facts (4.3.2.5) | LN_PLM | Laytime |
| P4_L3_VLD_T05 | task | Conduct Final Draft Survey (4.3.2.6) | LN_SRV | P754 CTP-5 PRIMARY commercial mass |
| P4_L3_VLD_T06 | task | Split and Seal Belt Sample — 3 portions | LN_SMP | |
| P4_L3_VLD_T07 | task | Dispatch Umpire Sample to Independent Lab | LN_PLM | |
| P4_L3_VLD_EE01 | endEvent | Vessel loading record committed; umpire sample dispatched | LN_SRV | |

Flows: T01→PGW01 | PGW01→T02[P1] | PGW01→T03[P2]
T02→PGW02 | T03→PGW02 | PGW02→T04→T05→T06→T07→EE01
ICE01 [boundary on T02]: interrupts loading → document in Statement of Facts → resume at T02

---

## P4_L2_COM — Commercial Documentation (L2)

### Pool & Lanes: Commercial Manager LN_CMR | Metallurgist LN_MET | Independent Umpire Lab LN_LAB | ERP/Finance LN_ERP | Carrier LN_CAR

| ID | Type | Name | Lane |
|----|------|------|------|
| P4_L2_COM_SE | startEvent (message) | Vessel loaded; umpire sample dispatched | P4_L2_COM_LN_CMR |
| P4_L2_COM_SP01 | subProcess (collapsed) | Certificate of Analysis Generation (4.4.1) | P4_L2_COM_LN_LAB | Ref P4_L3_COA |
| P4_L2_COM_SP02 | subProcess (collapsed) | Bill of Lading Finalization (4.4.2) | P4_L2_COM_LN_CAR | Ref P4_L3_BOL; parallel with CoA |
| P4_L2_COM_PGW01 | parallelGateway | [FORK] CoA and BoL processed concurrently | P4_L2_COM_LN_CMR | |
| P4_L2_COM_PGW02 | parallelGateway | [JOIN] Both CoA and BoL confirmed | P4_L2_COM_LN_CMR | |
| P4_L2_COM_SP03 | subProcess (collapsed) | Commercial Invoice Preparation (4.4.3) | P4_L2_COM_LN_ERP | Ref P4_L3_INV |
| P4_L2_COM_EE01 | endEvent | Invoice issued; revenue recognition posted in ERP | P4_L2_COM_LN_ERP | |

Flows: SE→PGW01 | PGW01→SP01[P1] | PGW01→SP02[P2]
SP01→PGW02 | SP02→PGW02 | PGW02→SP03→EE01

### P4_L3_COA — Certificate of Analysis (Lanes: Commercial Manager, Metallurgist, Independent Umpire Lab)
T01: Submit Belt Sample to Umpire Lab (4.4.1.1) [already dispatched — receipt confirmed]
ICE01: timerEvent — umpire lab TAT (10-21 days)
T02: Compare Assay Results; Apply Split Decision (4.4.1.2) | XGW01: Within split limit?
[Yes — average] [No — use umpire] | T03: Issue Agreed CoA (4.4.1.3)

### P4_L3_BOL — Bill of Lading Finalization (Lanes: Logistics Coordinator, Carrier, Commercial Manager)
T01: Confirm Commercial Quantity with Carrier (4.4.2.1) [draft survey commercial tonnes]
T02: Issue and Distribute Final Bill of Lading (4.4.2.2) [3 originals]

### P4_L3_INV — Commercial Invoice (Lanes: Commercial Manager, Finance, LME/COMEX Price Feed)
T01: Calculate Payable Metal Content; Apply Smelter Contract (4.4.3.1)
T02: Apply QP Metal Price; Issue Provisional Invoice (4.4.3.2)
ICE01: timerEvent — Quotational Period closes (30-90 days after shipment)
T03: Issue Final Invoice at Confirmed QP Price | XGW01: Buyer dispute?
[Yes — dispute resolution; hold final invoice] [No — invoice accepted; payment per terms]
