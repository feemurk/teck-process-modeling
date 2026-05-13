# Pillar 3: Processing & Beneficiation — BPMN Generation Specification

## Purpose
Use alongside `03-processing-and-beneficiation.md` to generate Lucidchart BPMN 2.0 XML.
Same ID convention — prefix P3. AMIRA P754 measurement points are annotated on relevant tasks.

## Diagram Inventory
| Diagram ID | Level | Title | L3 Sub-diagrams |
|------------|-------|-------|-----------------|
| P3_L2_COM | L2 | Comminution | P3_L3_PRC, P3_L3_SCR, P3_L3_GRD |
| P3_L2_FLT | L2 | Concentration (Flotation) | P3_L3_RGT, P3_L3_CUF, P3_L3_ZNF, P3_L3_PBF |
| P3_L2_DWT | L2 | Dewatering & Product Handling | P3_L3_THK, P3_L3_FIL, P3_L3_TLG |
| P3_L2_MET | L2 | Metallurgical Accounting & Quality | P3_L3_SMP, P3_L3_ASY, P3_L3_MBA |

---

## P3_L2_COM — Comminution (L2)

### Pool & Lanes
| ID | Name |
|----|------|
| P3_L2_COM_PL | Comminution |
| P3_L2_COM_LN_DCS | DCS / Auto-control |
| P3_L2_COM_LN_OPR | Control Room Operator |
| P3_L2_COM_LN_MET | Metallurgist |
| P3_L2_COM_LN_FMS | FMS (ROM interface) |

### Element Inventory
| ID | Type | Name | Lane | Notes |
|----|------|------|------|-------|
| P3_L2_COM_SE | startEvent (message) | ROM ore available at crusher pocket; plant running | P3_L2_COM_LN_FMS | |
| P3_L2_COM_SP01 | subProcess (collapsed) | Primary Crushing (3.1.1) | P3_L2_COM_LN_OPR | Ref P3_L3_PRC; P754 MP-01 |
| P3_L2_COM_XGW01 | exclusiveGateway | SABC circuit (Cu sites) or 3-stage crush (Red Dog/Zn)? | P3_L2_COM_LN_MET | Commodity branch |
| P3_L2_COM_SP02 | subProcess (collapsed) | Secondary/Tertiary Crushing & Screening (3.1.2) [Zn/Red Dog] | P3_L2_COM_LN_DCS | Ref P3_L3_SCR |
| P3_L2_COM_SP03 | subProcess (collapsed) | Grinding & Classification (3.1.3) | P3_L2_COM_LN_DCS | Ref P3_L3_GRD |
| P3_L2_COM_XGW02 | exclusiveGateway | Cyclone overflow P80 on target? | P3_L2_COM_LN_MET | |
| P3_L2_COM_T01 | task | Adjust mill throughput / cyclone apex / feed density | P3_L2_COM_LN_MET | |
| P3_L2_COM_EE01 | endEvent | Cyclone overflow at target P80 feeding flotation | P3_L2_COM_LN_DCS | |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P3_L2_COM_F01 | P3_L2_COM_SE | P3_L2_COM_SP01 | |
| P3_L2_COM_F02 | P3_L2_COM_SP01 | P3_L2_COM_XGW01 | |
| P3_L2_COM_F03 | P3_L2_COM_XGW01 | P3_L2_COM_SP02 | Zn / Red Dog — 3-stage circuit |
| P3_L2_COM_F04 | P3_L2_COM_XGW01 | P3_L2_COM_SP03 | Cu SABC — direct to grinding |
| P3_L2_COM_F05 | P3_L2_COM_SP02 | P3_L2_COM_SP03 | |
| P3_L2_COM_F06 | P3_L2_COM_SP03 | P3_L2_COM_XGW02 | |
| P3_L2_COM_F07 | P3_L2_COM_XGW02 | P3_L2_COM_EE01 | P80 on target |
| P3_L2_COM_F08 | P3_L2_COM_XGW02 | P3_L2_COM_T01 | P80 off target |
| P3_L2_COM_F09 | P3_L2_COM_T01 | P3_L2_COM_SP03 | Adjusted — retry |

---

## P3_L3_PRC — Primary Crushing (L3) | P3_L3_SCR — Secondary/Tertiary Crushing (L3) | P3_L3_GRD — Grinding (L3)

### P3_L3_PRC (Lanes: FMS/ROM LN_FMS | DCS LN_DCS | Operator LN_OPR)
| ID | Type | Name | Lane | P754 |
|----|------|------|------|------|
| P3_L3_PRC_SE | startEvent | Haul truck tip event; apron feeder active | LN_FMS | |
| P3_L3_PRC_T01 | serviceTask | Receive ROM Feed at Crusher; Record MP-01 Mass (3.1.1.1) | LN_DCS | P754 MP-01 CTP |
| P3_L3_PRC_T02 | task | Execute Primary Crushing; Monitor CSS and Power (3.1.1.2) | LN_DCS | |
| P3_L3_PRC_T03 | serviceTask | Transport via Discharge Conveyor; Record Belt Weigher (3.1.1.3) | LN_DCS | P754 cross-check |
| P3_L3_PRC_T04 | task | Manage Coarse Ore Stockpile Level (3.1.1.4) | LN_OPR | |
| P3_L3_PRC_XGW01 | exclusiveGateway | COS level below minimum? | LN_DCS | |
| P3_L3_PRC_T05 | task | Throttle SAG mill feed rate (DCS auto) | LN_DCS | |
| P3_L3_PRC_EE01 | endEvent | COS level stable; ore feeding to SAG/secondary crusher | LN_OPR | |

Flows: SE→T01→T02→T03→T04→XGW01 | XGW01→EE01[OK] | XGW01→T05[Low] | T05→T04[Loop]

### P3_L3_SCR — Secondary/Tertiary Crushing (Zn/Red Dog only)
Lanes: DCS LN_DCS | Operator LN_OPR
T01: Classify Ore by Screen (3.1.2.1) | T02: Execute Secondary/Tertiary Crushing (3.1.2.2)
XGW01: Oversize returned to crusher? [Yes→T02 loop] [No→T03]
T03: Execute Pebble Crushing [Cu SABC only] (3.1.2.3) — parallel if pebble crusher installed

### P3_L3_GRD — Grinding & Classification (Lanes: DCS LN_DCS | Operator LN_OPR | Metallurgist LN_MET)
| ID | Type | Name | Lane |
|----|------|------|------|
| P3_L3_GRD_SE | startEvent | COS reclaim feeding SAG / ball mill feed | LN_DCS |
| P3_L3_GRD_T01 | task | Operate SAG Mill — speed, bearing pressure, water (3.1.3.1) | LN_DCS |
| P3_L3_GRD_T02 | task | Operate Ball Mill — sump level, cyclone feed (3.1.3.2) | LN_DCS |
| P3_L3_GRD_T03 | task | Classify Slurry by Hydrocyclone (3.1.3.3) | LN_DCS |
| P3_L3_GRD_T04 | task | Add Grinding Media per Schedule (3.1.3.4) | LN_OPR |
| P3_L3_GRD_PGW01 | parallelGateway | [FORK] Media addition parallel to cyclone operation | LN_OPR |
| P3_L3_GRD_PGW02 | parallelGateway | [JOIN] | LN_DCS |
| P3_L3_GRD_EE01 | endEvent | Cyclone overflow at target P80 to flotation feed | LN_DCS |

Flows: SE→T01→T02→PGW01 | PGW01→T03[P1] | PGW01→T04[P2] | T03→PGW02 | T04→PGW02 | PGW02→EE01

---

## P3_L2_FLT — Concentration / Flotation (L2)

### Pool & Lanes
| ID | Name |
|----|------|
| P3_L2_FLT_PL | Concentration (Flotation) |
| P3_L2_FLT_LN_DCS | DCS / Auto-control |
| P3_L2_FLT_LN_MET | Metallurgist |
| P3_L2_FLT_LN_SMP | Auto-sampler / Sampler |

### Element Inventory
| ID | Type | Name | Lane | Notes |
|----|------|------|------|-------|
| P3_L2_FLT_SE | startEvent | Cyclone overflow feeding flotation feed sump; reagents dosed | P3_L2_FLT_LN_DCS | |
| P3_L2_FLT_SP01 | subProcess (collapsed) | Reagent Management (3.2.1) | P3_L2_FLT_LN_MET | Ref P3_L3_RGT |
| P3_L2_FLT_SP02 | subProcess (collapsed) | Copper Flotation Circuit (3.2.2) | P3_L2_FLT_LN_DCS | Ref P3_L3_CUF [COPPER-SPECIFIC] |
| P3_L2_FLT_XGW01 | exclusiveGateway | Polymetallic site (Antamina / Red Dog)? | P3_L2_FLT_LN_MET | Commodity branch |
| P3_L2_FLT_SP03 | subProcess (collapsed) | Zinc Flotation Circuit (3.2.3) [where applicable] | P3_L2_FLT_LN_DCS | Ref P3_L3_ZNF [ZINC-SPECIFIC] |
| P3_L2_FLT_SP04 | subProcess (collapsed) | Lead Flotation Circuit (3.2.4) [where applicable] | P3_L2_FLT_LN_DCS | Ref P3_L3_PBF [LEAD-SPECIFIC] |
| P3_L2_FLT_PGW01 | parallelGateway | [JOIN] All applicable circuits complete | P3_L2_FLT_LN_DCS | |
| P3_L2_FLT_T01 | serviceTask | Collect and Submit Shift Composite Samples | P3_L2_FLT_LN_SMP | per commodity per circuit |
| P3_L2_FLT_EE01 | endEvent | Shift end; concentrates flowing to thickeners; composites submitted | P3_L2_FLT_LN_SMP | |

### Sequence Flows
| ID | From | To | Condition |
|----|------|----|-----------|
| P3_L2_FLT_F01 | P3_L2_FLT_SE | P3_L2_FLT_SP01 | Reagents must be ready first |
| P3_L2_FLT_F02 | P3_L2_FLT_SP01 | P3_L2_FLT_SP02 | |
| P3_L2_FLT_F03 | P3_L2_FLT_SP02 | P3_L2_FLT_XGW01 | Cu circuit complete for this time step |
| P3_L2_FLT_F04 | P3_L2_FLT_XGW01 | P3_L2_FLT_SP03 | Yes — Antamina or Red Dog |
| P3_L2_FLT_F05 | P3_L2_FLT_XGW01 | P3_L2_FLT_PGW01 | No — Cu only site |
| P3_L2_FLT_F06 | P3_L2_FLT_SP03 | P3_L2_FLT_SP04 | Zn complete; Pb next [where applicable] |
| P3_L2_FLT_F07 | P3_L2_FLT_SP04 | P3_L2_FLT_PGW01 | |
| P3_L2_FLT_F08 | P3_L2_FLT_PGW01 | P3_L2_FLT_T01 | |
| P3_L2_FLT_F09 | P3_L2_FLT_T01 | P3_L2_FLT_EE01 | |

---

## P3_L3_RGT — Reagent Management | P3_L3_CUF — Cu Flotation | P3_L3_ZNF — Zn Flotation | P3_L3_PBF — Pb Flotation

### P3_L3_RGT (Lanes: DCS LN_DCS | Metallurgist LN_MET | Plant Chemist LN_CHM)
T01: Manage Reagent Inventory and Preparation (3.2.1.1) | T02: Adjust Pulp pH with Lime (3.2.1.2)
T03: Dose Collector/Frother/Depressant (3.2.1.3) | XGW01: pH on target? [No → adjust lime dosing loop]
All three T01-T03 run continuously as parallel DCS-controlled loops during plant operation

### P3_L3_CUF — Cu Flotation Circuit [COPPER-SPECIFIC] (Lanes: DCS, Metallurgist, OSA, Sampler)
| ID | Type | Name | Lane | P754 |
|----|------|------|------|------|
| P3_L3_CUF_SE | startEvent | Conditioned feed at target pH; cells running | LN_DCS | |
| P3_L3_CUF_T01 | task | Operate Cu Rougher Flotation (3.2.2.1) | LN_DCS | P754 MP-02 OSA |
| P3_L3_CUF_T02 | task | Operate Cu Scavenger Flotation (3.2.2.2) | LN_DCS | P754 MP-04 key loss |
| P3_L3_CUF_T03 | task | Operate Cu Regrind Mill [if installed] (3.2.2.4) | LN_DCS | |
| P3_L3_CUF_T04 | task | Operate Cu Cleaner Flotation (3.2.2.3) | LN_DCS | P754 MP-05 CTP |
| P3_L3_CUF_XGW01 | exclusiveGateway | Cu final concentrate grade below smelter spec? | LN_MET | |
| P3_L3_CUF_T05 | task | Adjust froth depth / depressant / cleaner stages | LN_MET | |
| P3_L3_CUF_T06 | task | Collect Shift Composite — Cu Final Concentrate | LN_SMP | P754 MP-05 primary grade |
| P3_L3_CUF_EE01 | endEvent | Cu concentrate flowing to thickener; composite submitted | LN_SMP | |

Flows: SE→T01→T02→T03→T04→XGW01 | XGW01→T06[OK] | XGW01→T05[Off-spec]
T05→T04[Adjust and recheck] | T06→EE01

### P3_L3_ZNF — Zn Flotation Circuit [ZINC-SPECIFIC] — mirrors CUF structure
Key differences: SE has CuSO4 activation step before rougher | P754 MP-11 is the Zn CTP | NaCN depressant used in cleaner | Zn scavenger tail is the key Zn loss stream (P754 MP-10)

### P3_L3_PBF — Pb Flotation Circuit [LEAD-SPECIFIC] — mirrors ZNF structure
Key differences: SE starts from Zn circuit tails (Antamina) or mill product at pH 7-8 (Red Dog) | P754 MP-15 is the Pb CTP | Ag is a payable by-product tracked through OSA

---

## P3_L2_DWT — Dewatering & Product Handling (L2)

### Pool & Lanes: DCS LN_DCS | Operator LN_OPR | Process Technician LN_TCH | Environmental LN_ENV

| ID | Type | Name | Lane | Notes |
|----|------|------|------|-------|
| P3_L2_DWT_SE | startEvent | Flotation concentrate flowing to thickener feed pumps | P3_L2_DWT_LN_DCS | |
| P3_L2_DWT_PGW01 | parallelGateway | [FORK] Separate dewatering trains per commodity + tailings | P3_L2_DWT_LN_DCS | |
| P3_L2_DWT_SP01 | subProcess (collapsed) | Concentrate Thickening — per commodity (3.3.1) | P3_L2_DWT_LN_DCS | Ref P3_L3_THK |
| P3_L2_DWT_SP02 | subProcess (collapsed) | Concentrate Filtration — per commodity (3.3.2) | P3_L2_DWT_LN_OPR | Ref P3_L3_FIL |
| P3_L2_DWT_SP03 | subProcess (collapsed) | Tailings Management (3.3.3) | P3_L2_DWT_LN_ENV | Ref P3_L3_TLG; continuous |
| P3_L2_DWT_PGW02 | parallelGateway | [JOIN] Shift end | P3_L2_DWT_LN_OPR | |
| P3_L2_DWT_EE01 | endEvent | Filter cake in concentrate shed; tailings at TSF | P3_L2_DWT_LN_OPR | |

Flows: SE→PGW01 | PGW01→SP01[concentrate] | PGW01→SP03[tailings — parallel]
SP01→SP02→PGW02 | SP03→PGW02 | PGW02→EE01

### P3_L3_THK — Thickening (Lanes: DCS, Operator)
T01: Feed Concentrate to Thickener; Record MP feed mass (3.3.1.1) P754 partial
T02: Dose Flocculant (3.3.1.2) | T03: Pump Thickener Underflow to Filter (3.3.1.3)
XGW01: Underflow density on target? [No → increase flocculant; loop]

### P3_L3_FIL — Filtration (Lanes: DCS, Operator, Process Technician, LIMS)
| ID | Type | Name | Lane | P754 |
|----|------|------|------|------|
| P3_L3_FIL_T01 | task | Operate Filter Press/Disc Filter (3.3.2.1) | LN_DCS | |
| P3_L3_FIL_T02 | task | Discharge Filter Cake; Record Belt Weigher (3.3.2.2) | LN_OPR | P754 CTP — filter cake dry tonnes |
| P3_L3_FIL_T03 | task | Collect Moisture Sample; Submit to Lab (3.3.2.3) | LN_TCH | P754 moisture — P5,P7,P8 |
| P3_L3_FIL_XGW01 | exclusiveGateway | Moisture within specification? | LN_MET | |
| P3_L3_FIL_T04 | task | Adjust filter cycle; investigate thickener underflow | LN_MET | |
| P3_L3_FIL_EE01 | endEvent | Filter cake accepted; transferred to concentrate shed (Pillar 4) | LN_OPR | |

Flows: T01→T02→T03→XGW01 | XGW01→EE01[OK] | XGW01→T04[Fail] | T04→T01[Adjust loop]

### P3_L3_TLG — Tailings Management (Lanes: DCS/SCADA, Environmental Officer)
T01: Thicken Tailings (3.3.3.1) | T02: Pump Tailings to TSF (3.3.3.2)
T03: Deposit at TSF; Monitor Freeboard (3.3.3.3) | T04: Recover Process Water from TSF (3.3.3.4)
XGW01: TSF freeboard below minimum? [Yes → reduce input rate; emergency response]
All run as continuous parallel loops during plant operation

---

## P3_L2_MET — Metallurgical Accounting & Quality (L2)

### Pool & Lanes: Auto-samplers/Instruments LN_AUT | Laboratory LN_LAB | Metallurgist LN_MET | Chief Metallurgist LN_CHF | ERP/Systems LN_SYS

| ID | Type | Name | Lane |
|----|------|------|------|
| P3_L2_MET_SE | startEvent (timer) | Shift start; all auto-samplers active | P3_L2_MET_LN_AUT |
| P3_L2_MET_SP01 | subProcess (collapsed) | Sampling (3.4.1) | P3_L2_MET_LN_AUT | Ref P3_L3_SMP; continuous during shift |
| P3_L2_MET_SP02 | subProcess (collapsed) | Assay & Analysis (3.4.2) | P3_L2_MET_LN_LAB | Ref P3_L3_ASY |
| P3_L2_MET_SP03 | subProcess (collapsed) | Mass Balance & Reconciliation (3.4.3) | P3_L2_MET_LN_CHF | Ref P3_L3_MBA |
| P3_L2_MET_XGW01 | exclusiveGateway | QC batch accepted? | P3_L2_MET_LN_LAB | |
| P3_L2_MET_T01 | task | Issue Re-assay Instruction; Hold Batch | P3_L2_MET_LN_LAB | |
| P3_L2_MET_XGW02 | exclusiveGateway | Shift balance error within tolerance? | P3_L2_MET_LN_CHF | |
| P3_L2_MET_T02 | task | Investigate Discrepancy; Escalate to Chief Metallurgist | P3_L2_MET_LN_MET | |
| P3_L2_MET_EE01 | endEvent | Shift mass balance accepted; daily/monthly reconciliation feeds upstream | P3_L2_MET_LN_CHF | |

Flows: SE→SP01 [continuous] | SP01→SP02 [at shift end, composites submitted] | SP02→XGW01
XGW01→SP03[Pass] | XGW01→T01[Fail] | T01→SP02[Loop — re-assay] | SP03→XGW02
XGW02→EE01[Within tolerance] | XGW02→T02[Outside] | T02→EE01[Resolved or escalated]

### P3_L3_SMP through P3_L3_MBA (L3 elements)
**P3_L3_SMP** — Sampling: T01: Collect Auto-Sampler Increments (3.4.1.1) [continuous loop per interval]
T02: Collect Grab/Composite Samples (3.4.1.2) | T03: Prepare Samples in Lab (3.4.1.3) | Insert QC at preparation

**P3_L3_ASY** — Assay & Analysis: T01: Perform Lab Assay (3.4.2.1) [ICP/XRF/fire assay]
T02: Monitor OSA in real-time (3.4.2.2) [parallel continuous stream]
T03: Perform QA/QC — CRM, duplicate, blank (3.4.2.3) | XGW01: QC pass? [loop back if fail]

**P3_L3_MBA** — Mass Balance: T01: Close Shift Mass Balance (3.4.3.1) [shift end trigger]
T02: Daily/Weekly Reconciliation (3.4.3.2) | T03: Monthly Metal Accounting Report (3.4.3.3) [monthly trigger]
T04: Conduct Inventory Adjustment and Stocktake (3.4.3.4) [monthly/quarterly]
ICE01: Monthly period end intermediate timer event
