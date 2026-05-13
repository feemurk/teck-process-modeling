# Pillar 3: Processing & Beneficiation

---

## Overview

Processing & Beneficiation transforms Run-of-Mine (ROM) ore delivered from mine extraction into saleable concentrate product. The pillar spans four process areas: Comminution (size reduction), Concentration by flotation (selective mineral recovery), Dewatering & Product Handling (moisture reduction to specification), and Metallurgical Accounting & Quality (mass balance closure and commercial metal accounting). The process boundary opens at ROM ore receipt at the primary crusher and closes at filter cake delivery to the concentrate shed and tailings deposition at the Tailings Storage Facility (TSF).

This pillar is governed by a continuous process paradigm: unlike the discrete, event-driven Load & Haul cycle, processing operates as a flowing system with feed entering, products and tailings exiting, and recirculating loads creating closed circuits within the plant. ISA-95 Levels 0–2 dominate — physical process, sensors, and SCADA/DCS control loops. Level 3 functions (metallurgical accounting, LIMS, quality management, shift reporting) are critical but consume data generated at Levels 0–2. Level 4 (production planning, plant utilisation targets) is a consumer rather than a generator within this pillar.

AMIRA P754 is the governing standard for every measurement point involving mass flow, grade, density, or moisture. Every process node in this pillar that generates a measurement is annotated with: measurement type, method, frequency, AMIRA principle(s), and custody transfer status. This annotation discipline is mandatory — it is the design input for the curated data product entities that will underpin metallurgical accounting and reconciliation. The mass balance node maps for each flotation circuit are produced as a separate artifact within this pillar.

Commodity-specific circuit variations are material in this pillar. Copper porphyry operations (QB, HVC, CdA) run a single Cu flotation circuit with optional Mo by-product recovery. Polymetallic copper-zinc operations (Antamina) run sequential Cu then Zn circuits with optional Pb recovery. Zinc-lead operations (Red Dog) run differential flotation to separate Zn and Pb concentrates. One unified process model is used with commodity-specific branches explicitly marked.

---

## Process Decomposition

> **AMIRA P754 Annotation Convention** — Activities involving measurement points carry an additional annotation block in the Description column formatted as:
> `[P754: type | method | frequency | principles | custody_transfer_point?]`

### 3.1 Comminution

| ID | Activity Name | Description | ISA-95 Level | Trigger | Inputs | Outputs | Primary Actor(s) | Source System(s) | Standard Alignment | DDVC Layer |
|----|---------------|-------------|--------------|---------|--------|---------|-----------------|------------------|--------------------|------------|
| **3.1** | **Comminution** | *L2 Process Area. Progressive size reduction of ROM ore from run-of-mine fragmentation (typically P80 150–250 mm) to a target grind size suitable for flotation (P80 75–150 µm depending on ore and circuit). Encompasses primary crushing, secondary/tertiary crushing and screening where applicable, SAG and ball milling, and hydrocyclone classification.* | 0–3 | ROM ore available at crusher feed; plant operating | ROM ore (from mine haul trucks or ROM stockpile reclaim); grinding media; process water | Ground slurry (P80 target achieved); mill operating data (power draw, throughput, bearing pressures); belt scale mass data | Plant Metallurgist; Control Room Operator; DCS Auto-control | DCS (ABB, Honeywell, Yokogawa); PI Historian; FMS (ROM delivery interface) | ISA-95 Levels 0–3; AMIRA P754 Principles 1, 2, 5 | Raw (time-series); Curated (process_node, equipment_operating_record) |
| **3.1.1** | **Primary Crushing** | *L0/L1/L2 Process. Jaw or gyratory crusher reduces ROM ore from truck-tipped fragmentation (typically P80 150–350 mm) to a product suitable for conveying and secondary crushing or direct SAG mill feed (P80 80–150 mm). The primary crusher is the first fixed measurement point in the process.* | 0–2 | Haul truck tip event; plant running; crusher clear | ROM ore (truck tipped at crusher pocket); primary crusher (operational) | Crushed ore product (P80 80–150 mm); crusher throughput (belt scale); ore flow to downstream conveyor | Control Room Operator; DCS Auto-control | DCS; PI Historian; belt weigh feeder → PI Historian; crusher management system | ISA-95 Levels 0–2; AMIRA P754 Principles 1, 5 | Raw (time-series); Curated (process_measurement_point) |
| 3.1.1.1 | Receive ROM Feed at Crusher | Haul trucks tip ROM ore into the primary crusher dump pocket. Tip event is recorded by the crusher management system or FMS when a truck dumps (GPS + crusher proximity sensor). Belt weigh feeder on the apron/pan feeder below the dump pocket measures ore feed rate continuously. This measurement point is the opening of the plant-side mass balance and the internal mine-to-mill custody transfer. [P754: mass | belt weigh feeder / apron feeder scale | continuous (1-min integration) | Principles 1, 5 | YES — internal custody transfer: Mine Operations to Processing] | 1 / 3 | Haul truck tip event; dump pocket level above minimum | ROM ore (from haul truck or stockpile reclaim dozer); dump pocket (physical); apron feeder (operational) | Ore in dump pocket (physical); tip event record (truck ID, timestamp, FMS-estimated payload); belt weigh feeder mass rate (t/hr); cumulative ore received (t) | Control Room Operator; Automated DCS | DCS; belt weigh feeder → PI Historian; FMS (tip event) | ISA-95 Levels 1, 3; AMIRA P754 Principles 1, 5 (mass measurement; custody transfer) | Raw; Curated (process_measurement_point — crusher_feed_mass_rate) |
| 3.1.1.2 | Execute Primary Crushing | Gyratory or jaw crusher (depending on site) reduces ROM ore to the target top size. DCS monitors and controls closed-side setting (CSS) to achieve the target product size. Crusher power draw (kW), throughput (t/hr from apron feeder), vibration, and hydraulic pressure are logged at 1-minute intervals to PI Historian. Tramp metal detection upstream protects crusher internals. | 0 / 2 | Crusher running; apron feeder active; CSS set | ROM ore (in dump pocket); crusher (operational, CSS set, lubrication active); tramp metal detector | Crushed ore product (physical, P80 80–150 mm); crusher power draw telemetry (1-min); CSS position record; vibration and pressure telemetry | DCS Auto-control; Control Room Operator | DCS; PI Historian | ISA-95 Levels 0, 2; AMIRA P754 Principle 2 (consistent, transparent system — crusher settings documented) | Raw (time-series: primary_crusher_telemetry) |
| 3.1.1.3 | Transport via Discharge Conveyor | Crushed ore discharges from the crusher onto the main discharge conveyor belt to the coarse ore stockpile (COS) or directly to the SAG mill feed bin. A belt weigher on the discharge conveyor provides a secondary mass measurement (cross-checked against apron feeder). Belt speed, loading, and mass rate are logged continuously. [P754: mass | belt weigher (conveyor) | continuous (1-min integration) | Principles 1, 2, 7 | NO — internal process measurement, not a custody transfer point] | 1 / 2 | Crusher producing; conveyor running | Crushed ore (from crusher); discharge conveyor (running, aligned) | Crushed ore transport to COS or SAG feed bin; belt weigher mass rate record (t/hr); conveyor running hours | DCS Auto-control | DCS; PI Historian (belt weigher) | ISA-95 Levels 1, 2; AMIRA P754 Principles 1, 2, 7 | Raw (time-series) |
| 3.1.1.4 | Manage Coarse Ore Stockpile | COS acts as a buffer between the discontinuous primary crusher (batch-fed by haul trucks) and the continuous SAG mill circuit. Stockpile level is monitored by level sensor or periodic survey. Reclaim feeders pull ore from the COS base onto the SAG mill feed conveyor at a controlled rate. COS inventory (mass) is estimated from level sensor volume plus density assumption; this is a known P754 measurement accuracy limitation. [P754: mass (inventory estimate) | level sensor + density assumption | continuous level / periodic survey | Principles 1, 7, 8 | NO — internal process buffer; not a custody transfer point] | 2 / 3 | COS receiving from discharge conveyor; SAG mill pulling from COS | Crushed ore (from conveyor); COS (physical stockpile); reclaim feeders (operational); level sensor | COS inventory level record (m / estimated t); reclaim feed rate (t/hr from reclaim belt weigher) | Control Room Operator; DCS | DCS; PI Historian (level sensor); belt weigher → PI Historian | ISA-95 Levels 2, 3; AMIRA P754 Principles 1, 7, 8 | Raw; Curated (process_inventory_node) |
| **3.1.2** | **Secondary/Tertiary Crushing & Screening** | *L0/L2 Process. Not all circuits include secondary/tertiary crushing. Where present (typically in three-stage crushing circuits preceding ball mills, or as pebble crushers in SABC circuits), screens classify crushed product and recirculate oversize. This sub-process is conditional — it applies where a dedicated crushing circuit precedes ball milling. [COPPER NOTE: QB and HVC use SABC circuits — pebble crusher applies. ZINC NOTE: Red Dog uses a three-stage crushing circuit preceding the grinding circuit.]* | 0–2 | Crushed ore available from primary; screening circuit running | Primary crushed ore; cone/impact crushers (operational); vibrating screens | Screened product at target top size; screen oversize (recycled to crusher); screen undersize (forward to grinding) | DCS Auto-control; Control Room Operator | DCS; PI Historian | ISA-95 Levels 0, 2; AMIRA P754 Principle 1 | Raw (time-series) |
| 3.1.2.1 | Classify Ore by Screen | Vibrating screen deck(s) classify crushed ore by particle size. Oversize material (> screen aperture) is retained and recycled to crusher. Undersize passes through as the screened product. Screen efficiency (partition curve) and circulating load percentage are key process parameters. Screen deck vibration, throughput, and feed/product size are monitored. | 0 / 2 | Crusher product arriving at screen; screen running | Crushed ore (feed); vibrating screen (operational, correct aperture deck installed) | Screen oversize (recycled); screen undersize product (forward); screen throughput record | DCS Auto-control | DCS; PI Historian | ISA-95 Levels 0, 2 | Raw |
| 3.1.2.2 | Execute Secondary/Tertiary Crushing | Cone or impact crusher reduces screen oversize to within specification. Multiple stages may be applied (secondary then tertiary). Crusher power, throughput, and gap setting are monitored continuously. [ZINC NOTE: Red Dog's three-stage circuit — primary jaw, secondary cone, tertiary cone — is the standard process before ball mill grinding.] | 0 / 2 | Screen oversize feed available; crusher operational | Screen oversize; cone/impact crusher (operational, gap set); lubrication active | Crushed secondary/tertiary product; crusher telemetry (power draw, throughput, gap position) | DCS Auto-control | DCS; PI Historian | ISA-95 Levels 0, 2 | Raw (time-series: secondary_crusher_telemetry) |
| 3.1.2.3 | Execute Pebble Crushing | Pebble crusher handles the "critical size" fraction (typically 20–80 mm) generated by the SAG mill that is too large for efficient ball milling and too small to act as grinding media. Pebbles are diverted from the SAG discharge screen and fed to a cone crusher (pebble crusher); crushed product is returned to the SAG mill feed or ball mill feed. [COPPER NOTE: Critical activity at QB (SABC-A circuit) and HVC — pebble build-up is a key SAG throughput constraint. NOT applicable at Red Dog (three-stage crushing circuit).] | 0 / 2 | SAG discharge screen generating pebbles above threshold; pebble crusher available | SAG discharge screen pebbles; pebble crusher (operational) | Crushed pebble product (returned to circuit); pebble crusher power draw; pebble recirculating load estimate | DCS Auto-control | DCS; PI Historian | ISA-95 Levels 0, 2 | Raw |
| **3.1.3** | **Grinding & Classification** | *L0/L1/L2 Process. SAG and ball mills reduce ore to the target grind size (P80 75–150 µm) in a wet grinding circuit with water addition and steel grinding media. Hydrocyclone clusters classify ground slurry — underflow (coarse) is recycled to the ball mill, overflow (fine) advances to flotation as the mill circuit product. The mill circuit product P80 is the key quality handoff from Comminution to Flotation.* | 0–2 | COS reclaim active; mill running; cyclone feed pump running | Crushed ore; process water; grinding media (balls); slurry from SAG discharge; reagents (frother pre-addition where applicable) | Ground slurry at target P80 (cyclone overflow to flotation); mill discharge (to ball mill or cyclone); mill telemetry (power draw, bearing pressure, load); cyclone underflow recirculating load | Control Room Operator; DCS Auto-control; Metallurgist | DCS; PI Historian; particle size analyser (PSA/PGNA online or periodic sieve) | ISA-95 Levels 0–2; AMIRA P754 Principles 1, 2 | Raw (time-series: mill_telemetry); Curated (process_measurement_point — cyclone_overflow_grade) |
| 3.1.3.1 | Operate SAG Mill | Semi-autogenous grinding (SAG) mill uses ore itself as the primary grinding medium, supplemented by a charge of steel balls (typically 10–15% v/v). DCS controls mill speed (% critical), bearing pressure (proxy for mill load/charge mass), water addition rate, and feed rate. SAG mill power draw is the primary throughput optimisation variable. Mill discharge passes through a discharge screen — pebbles are diverted to pebble crushing; undersize advances to the ball mill. [P754: mass flow (indirect — via feed belt weigher and water flow meter) | belt weigher + flow meter | continuous (1-min) | Principles 1, 2 | NO — internal process node] | 0 / 2 | COS reclaim feeding SAG; SAG charge and water available; mill rotating | Crushed ore (from COS reclaim); steel ball charge; process water; SAG mill (operational) | SAG mill discharge (to discharge screen and ball mill); SAG mill telemetry (1-min: power draw kW, bearing pressure kPa, speed % critical, feed rate t/hr, water addition m³/hr); discharge screen product (pebbles diverted, undersize forward) | DCS Auto-control; Control Room Operator | DCS; PI Historian | ISA-95 Levels 0, 2; AMIRA P754 Principles 1, 2 | Raw (time-series: sag_mill_telemetry) |
| 3.1.3.2 | Operate Ball Mill | Ball mill(s) receive SAG mill undersize discharge (or primary crushed ore at Red Dog three-stage circuit) and grind to the target cyclone feed size using a steel ball charge. DCS controls ball mill speed, water addition, and feed rate. Ball mill power draw is monitored continuously. Sump level (cyclone feed sump) is controlled by variable-speed pump. [P754: mass flow (indirect — via cyclone feed density and flow meter) | nuclear density gauge + magnetic flow meter | continuous (1-min) | Principles 1, 2 | NO — internal process node] | 0 / 2 | SAG mill discharge available or primary crusher discharge (Red Dog); ball mill operational; steel ball charge | Ball mill discharge from SAG (or primary crusher at Red Dog); steel ball charge; process water; ball mill (operational) | Ball mill discharge slurry (to cyclone feed sump); ball mill telemetry (1-min: power draw kW, speed, feed rate, water addition); cyclone feed sump level | DCS Auto-control; Control Room Operator | DCS; PI Historian | ISA-95 Levels 0, 2; AMIRA P754 Principles 1, 2 | Raw (time-series: ball_mill_telemetry) |
| 3.1.3.3 | Classify Slurry by Hydrocyclone | Hydrocyclone cluster(s) classify ball mill discharge slurry by particle size using centrifugal force. Cyclone overflow (fine fraction, P80 target met) advances to flotation conditioning as the mill circuit product — this is the Comminution-to-Flotation handoff. Cyclone underflow (coarse fraction) recirculates to the ball mill. Cyclone feed density and flow rate are monitored; overflow particle size is measured periodically (sieve analysis) or continuously (online PSA). [P754: grade (particle size proxy via density) | nuclear density gauge + periodic PSA | continuous density / periodic size | Principles 1, 2, 7 | NO — internal process classification node] | 2 / 1 | Ball mill discharge available; cyclone feed pump running; cyclones operational | Ball mill discharge slurry; cyclone feed pump (running); process water (for dilution if required) | Cyclone overflow (P80 target — to flotation feed); cyclone underflow (recycled to ball mill); cyclone feed density and flow rate telemetry; periodic particle size analysis result | DCS Auto-control; Control Room Operator | DCS; PI Historian; online PSA (if installed) or LIMS (sieve result) | ISA-95 Levels 1, 2; AMIRA P754 Principles 1, 2, 7 | Raw; Curated (process_measurement_point — mill_circuit_product_p80) |
| 3.1.3.4 | Manage Grinding Media Addition | Steel grinding balls are added to the SAG and ball mills at a controlled rate (t/hr of balls per t/hr of ore processed) to maintain the target ball charge volume and composition. Grinding media consumption is tracked by ball addition count (ball counter or weigh hopper) and is a significant reagent cost input to the processing cost model. Ball addition events are recorded per mill per shift. | 3 | Scheduled ball addition interval or mill power draw below setpoint | Steel balls (inventory by size fraction); ball addition hopper or conveyor; mill running | Ball addition record (mass added per mill per shift); grinding media inventory consumption record | Metallurgist; Plant Operator | DCS (ball counter or weigh hopper sensor); ERP (MM — inventory); PI Historian | ISA-95 Level 3 (inventory management); AMIRA P754 Principle 1 (mass of grinding media is an input to mass balance) | Raw; Curated (reagent_consumption_record) |

### 3.2 Concentration (Flotation)

| ID | Activity Name | Description | ISA-95 Level | Trigger | Inputs | Outputs | Primary Actor(s) | Source System(s) | Standard Alignment | DDVC Layer |
|----|---------------|-------------|--------------|---------|--------|---------|-----------------|------------------|--------------------|------------|
| **3.2** | **Concentration (Flotation)** | *L2 Process Area. Selective separation of valuable minerals (chalcopyrite, sphalerite, galena, molybdenite) from gangue using froth flotation. Air bubbles attach to hydrophobic mineral surfaces made selective by reagents; the loaded froth overflows to concentrate while depressed gangue reports to tailings. This is the primary value-creation process in the plant — metal recovery and concentrate grade are the defining performance variables. Circuit architecture varies by commodity.* | 0–3 | Mill circuit product (cyclone overflow) available; flotation cells operational; reagents dosed | Cyclone overflow slurry (P80 target); reagents (collectors, frothers, depressants, pH modifiers); air (for cell aeration) | Cu concentrate froth; Zn concentrate froth (where applicable); Pb concentrate froth (where applicable); tailings; on-stream assay data; cell operating telemetry | Control Room Operator; Metallurgist; DCS Auto-control | DCS; PI Historian; on-stream analyzer (OSA/XRF); LIMS | ISA-95 Levels 0–3; AMIRA P754 Principles 1, 2, 5, 6, 7 | Raw (time-series); Curated (concentrate_production_record, process_measurement_point) |
| **3.2.1** | **Reagent Management** | *L3/L0 Process. Chemical reagents are the primary selectivity control mechanism in flotation. Collectors attach to target mineral surfaces; frothers stabilise bubble-particle aggregates in the froth; depressants prevent non-target minerals from floating; pH modifiers (lime) control pulp chemistry to enable selective activation and depression.* | 0–3 | Plant operating; reagent inventory available; metallurgist dosage instruction | Reagents (collectors, frothers, depressants, pH modifiers — in reagent tanks); reagent dosing pumps; pulp pH and flow rate | Conditioned flotation feed at target pH; reagent consumption records; pH telemetry | Metallurgist; Control Room Operator; DCS | DCS; PI Historian; ERP (MM — reagent inventory) | ISA-95 Levels 0–3; AMIRA P754 Principles 1, 2 | Raw; Curated (reagent_addition_record) |
| 3.2.1.1 | Manage Reagent Inventory and Preparation | Reagents are received from suppliers in bulk tanks, drums, or bags, inventoried in the ERP, and prepared (diluted to working concentration where required) in the reagent mixing area. Reagent usage is tracked by tank level change (mass = volume × density) per shift. Reagent consumption is a key variable cost and a P754-relevant input to mass balance integrity checks. [P754: mass (reagent consumption) | tank level sensor + density measurement | shift-end reconciliation | Principle 1 (mass of reagent inputs to mass balance) | NO] | 3 | Shift start; reagent tank low-level alert; replenishment schedule | Bulk reagents (from supplier delivery); reagent tanks; mixing equipment | Reagent inventory record (tank level by reagent type); reagent consumption per shift (kg); reagent preparation batch record | Plant Chemist; Metallurgist | ERP (MM — inventory); DCS (tank level sensors) → PI Historian | ISA-95 Level 3; AMIRA P754 Principle 1 | Raw; Curated (reagent_consumption_record) |
| 3.2.1.2 | Adjust Pulp pH with Lime | Quicklime or hydrated lime is added to the grinding circuit or flotation feed conditioning tank to achieve the target pH for the flotation circuit. At Cu-only circuits (QB, HVC), pH is typically maintained at 10–11.5 to depress pyrite. At sequential Cu-Zn circuits (Antamina), Cu flotation operates at elevated pH while Zn activation requires a lower pH adjustment after Cu concentrate removal. DCS controls lime dosing pump speed based on continuous inline pH measurement. [P754: mass (lime) + grade (pH as process parameter) | lime slurry flow meter + inline pH sensor | continuous (1-min) | Principles 1, 2 | NO] | 1 / 2 | Flotation circuit running; pH setpoint set by metallurgist | Lime slurry (from lime storage and slaking); lime dosing pump; inline pH sensor | Target pH achieved in conditioning tank or mill discharge; lime dosing rate record (m³/hr, or kg/hr); pH telemetry (continuous) | DCS Auto-control; Metallurgist | DCS; PI Historian (pH and lime flow) | ISA-95 Levels 1, 2; AMIRA P754 Principles 1, 2 | Raw (time-series: pH_telemetry, lime_dosing_telemetry) |
| 3.2.1.3 | Dose Collector, Frother, and Depressant | Dosing pumps inject collectors (xanthates, dithiophosphates for Cu/Zn; xanthates for Pb), frothers (MIBC, DF250), and depressants (sodium cyanide or zinc sulphate for Zn depression in Cu circuit; sodium silicate for gangue depression) into the flotation feed or individual flotation banks at metered flow rates. Dosage rates are controlled by DCS (flow rate setpoints from metallurgist) and logged continuously to PI Historian. [P754: mass (reagent) | positive displacement dosing pump flow meter | continuous (1-min) | Principles 1, 2 | NO — internal reagent input] | 1 / 2 | Flotation circuit running; reagent tanks loaded; dosing pump operational | Collectors, frothers, depressants (from reagent tanks); dosing pumps (operational); flotation cells (running) | Reagent dosing rate records (mL/min or g/t basis) per reagent per addition point; reagent consumption (shift total) | DCS Auto-control; Metallurgist | DCS; PI Historian (dosing pump flow meters) | ISA-95 Levels 1, 2; AMIRA P754 Principles 1, 2 | Raw (time-series: reagent_dosing_telemetry) |
| **3.2.2** | **Copper Flotation Circuit** | *[COPPER-SPECIFIC] Applies to: QB, HVC, Antamina (Cu circuit first), CdA. L0/L1/L2 Process. The Cu flotation circuit selectively recovers chalcopyrite (CuFeS₂) and bornite (Cu₅FeS₄) from the ground slurry into a high-grade Cu concentrate. The circuit typically comprises rougher, scavenger, and cleaner stages in a standard rougher-scavenger-cleaner (RSC) configuration, with regrinding of cleaner tails or scavenger concentrate where liberation is insufficient.* | 0–2 | Conditioned flotation feed available at target pH and P80; cells operating | Conditioned mill circuit product (cyclone overflow); reagents (collector, frother, depressant); air (flotation cell aeration) | Cu rougher concentrate (to Cu cleaner); Cu final concentrate (from Cu cleaner — to thickening); Cu flotation tailings (to Zn circuit or final tailings); on-stream Cu assays | Control Room Operator; Metallurgist; DCS | DCS; PI Historian; on-stream XRF analyzer | ISA-95 Levels 0–2; AMIRA P754 Principles 1, 2, 5, 6, 7 | Raw (time-series); Curated (concentrate_production_record) |
| 3.2.2.1 | Operate Cu Rougher Flotation | The rougher bank(s) process the full flotation feed and produce a bulk Cu rougher concentrate from the froth overflow. Maximum recovery is the primary objective of the rougher — grade is sacrificed for recovery. Each rougher cell is equipped with a froth scraper or paddled froth crowder; air rate, froth depth, and impeller speed are controlled by DCS per cell. On-stream analysis (XRF) measures feed, concentrate, and tail grades at 2–4 minute intervals. [P754: grade (Cu%, Fe%, S%) | on-stream XRF analyzer | continuous (2–4 min scan interval) | Principles 1, 2, 6, 7 | NO — internal process stream; not a commercial custody transfer point] | 0 / 2 | Flotation feed conditioned; rougher cells operational; air available | Conditioned mill circuit product; collector and frother dosed; air (cell aeration) | Rougher concentrate (froth overflow — to scavenger or cleaner); rougher tailings (cell underflow — to scavenger); cell telemetry (1-min: air rate, froth depth, power, cell level); OSA grade data | DCS Auto-control; Metallurgist | DCS; PI Historian; on-stream XRF analyzer | ISA-95 Levels 0, 2; AMIRA P754 Principles 1, 2, 6, 7 | Raw (time-series: flotation_cell_telemetry, osa_grade_telemetry) |
| 3.2.2.2 | Operate Cu Scavenger Flotation | Scavenger bank(s) process the rougher tailings to maximise recovery of residual Cu minerals. Scavenger concentrate (low grade) is either recycled to the rougher or regrind circuit. Scavenger tailings report to: (a) Cu flotation final tailings at Cu-only sites, or (b) Zn flotation feed at Cu-Zn sequential circuits (Antamina). Additional collector dosing at the scavenger head increases recovery. On-stream analysis monitors scavenger tail grade — this is the Cu recovery loss stream. [P754: grade (Cu% in scavenger tailings — key loss measurement) | on-stream XRF + periodic grab sample | continuous OSA / shift composite | Principles 1, 2, 6, 7 | PARTIAL — scavenger tailings grade at Cu-only sites is the final Cu loss measurement and is material to P754 Principle 7 (verification data)] | 0 / 2 | Rougher tailings available; scavenger cells operational | Rougher tailings; additional collector; air | Scavenger concentrate (recycled to rougher or regrind); scavenger tailings (final Cu tailings or Zn feed); OSA grades | DCS Auto-control; Metallurgist | DCS; PI Historian; on-stream XRF | ISA-95 Levels 0, 2; AMIRA P754 Principles 1, 2, 6, 7 | Raw (time-series) |
| 3.2.2.3 | Operate Cu Cleaner Flotation | Cleaner bank(s) upgrade the rougher concentrate to final Cu concentrate grade specification (typically 25–35% Cu for smelter contract). Multiple cleaner stages may be used (1st cleaner, 2nd cleaner, sometimes 3rd cleaner). Cleaner tails (low-grade middlings) are recycled to rougher or regrind. Final cleaner concentrate is the Cu product stream — its grade and mass flow are the primary Cu production measurement. [P754: grade (Cu%, Fe%, S%, Au g/t, Ag g/t, Mo% where applicable) + mass flow | on-stream XRF + shift composite sample (lab assay) | continuous OSA + shift composite | Principles 1, 2, 5, 6, 7 | YES — Cu cleaner final concentrate is a custody transfer point to thickening/dewatering] | 0 / 2 | Rougher concentrate available; cleaner cells operational; reagent dosing set | Rougher concentrate; depressants (for gangue rejection); air | Final Cu concentrate (to thickening); cleaner tails (recycle to rougher/regrind); OSA grade data (concentrate); shift composite sample (submitted to lab) | DCS Auto-control; Metallurgist | DCS; PI Historian; on-stream XRF; LIMS (shift composite) | ISA-95 Levels 0, 2; AMIRA P754 Principles 1, 2, 5, 6, 7 | Raw; Curated (concentrate_production_record — Cu) |
| 3.2.2.4 | Operate Cu Regrind Mill | Where Cu rougher or scavenger concentrate requires further liberation before cleaning, a regrind mill (typically a stirred media detritor or ball mill) grinds the concentrate to a finer P80 (typically 20–40 µm). Regrind improves cleaner performance by liberating interlocked particles. Not all sites have a dedicated Cu regrind — depends on ore mineralogy and liberation characteristics. [COPPER NOTE: HVC uses regrind for improved Mo circuit feed preparation.] | 0 / 2 | Rougher/scavenger concentrate available for regrind; regrind mill operational | Rougher/scavenger Cu concentrate; regrind mill (operational); process water; grinding media | Reground concentrate (to Cu cleaner); regrind mill telemetry (power draw, feed rate) | DCS Auto-control | DCS; PI Historian | ISA-95 Levels 0, 2 | Raw (time-series: regrind_mill_telemetry) |
| **3.2.3** | **Zinc Flotation Circuit** | *[ZINC-SPECIFIC — where applicable] Applies to: Antamina (sequential after Cu), Red Dog (primary Zn circuit). L0/L1/L2 Process. At polymetallic operations, the Cu flotation tailings (or primary mill product at Red Dog) feed the Zn flotation circuit. Sphalerite (ZnS) must first be activated with copper sulphate (CuSO₄) before it becomes floatable — it is naturally depressed in the Cu circuit. The Zn circuit follows the same RSC architecture as the Cu circuit.* | 0–2 | Cu flotation tailings available (Antamina) or mill circuit product (Red Dog); Zn circuit running; CuSO₄ dosing active | Cu flotation tailings or mill product; CuSO₄ (Zn activator); collector; frother; air | Zn concentrate (to Zn thickening); Zn flotation tailings (to Pb circuit or final tailings) | Control Room Operator; Metallurgist; DCS | DCS; PI Historian; on-stream XRF | ISA-95 Levels 0–2; AMIRA P754 Principles 1, 2, 5, 6, 7 | Raw (time-series); Curated (concentrate_production_record — Zn) |
| 3.2.3.1 | Activate Sphalerite with Copper Sulphate | Copper sulphate (CuSO₄) is dosed into the Zn circuit feed (Cu flotation tailings or conditioning tank) to activate sphalerite surfaces for subsequent collector attachment. Without activation, sphalerite is hydrophilic and will not float. CuSO₄ dosage rate is controlled by DCS and is critical to Zn recovery — under-dosing suppresses Zn recovery; over-dosing can cause Cu re-activation and contaminate Zn concentrate. [P754: mass (CuSO₄) | dosing pump flow meter | continuous (1-min) | Principle 1 | NO] | 1 / 2 | Cu flotation tailings or mill product feeding Zn conditioning tank; CuSO₄ dosing pump operational | Cu flotation tailings; CuSO₄ solution (from reagent tank); dosing pump | CuSO₄-conditioned slurry (Zn flotation feed); CuSO₄ dosing rate record | DCS Auto-control; Metallurgist | DCS; PI Historian | ISA-95 Levels 1, 2; AMIRA P754 Principle 1 | Raw |
| 3.2.3.2 | Operate Zn Rougher Flotation | Zn rougher bank(s) float activated sphalerite from the conditioned feed. Operating philosophy mirrors Cu rougher — maximum Zn recovery priority. On-stream analysis measures Zn%, Pb%, and Fe% in rougher concentrate and tailings. At Red Dog, Pb must be selectively depressed in the Zn rougher to avoid Pb contamination of Zn concentrate (sphalerite/galena separation is critical). [P754: grade (Zn%, Pb%, Fe%) | on-stream XRF | continuous (2–4 min) | Principles 1, 2, 6, 7 | NO] | 0 / 2 | CuSO₄-conditioned Zn feed; Zn rougher cells operational | Conditioned Zn feed; Zn collector (xanthate); frother; air | Zn rougher concentrate; Zn rougher tailings; OSA data | DCS; on-stream XRF → PI Historian | ISA-95 Levels 0, 2; AMIRA P754 Principles 1, 2, 6, 7 | Raw (time-series: flotation_cell_telemetry) |
| 3.2.3.3 | Operate Zn Scavenger Flotation | Zn scavenger recovers residual sphalerite from Zn rougher tailings. Scavenger concentrate recycled to rougher or Zn regrind. Scavenger tailings are the Zn circuit final tailings — Zn grade in scavenger tailings is the key Zn recovery loss measurement. [P754: grade (Zn% in scavenger tailings) | on-stream XRF + periodic grab | continuous OSA / shift | Principles 6, 7 | PARTIAL — key loss measurement] | 0 / 2 | Zn rougher tailings; scavenger cells operational | Zn rougher tailings; additional collector; air | Zn scavenger concentrate (recycled); Zn scavenger tailings (to Pb circuit or final tailings); OSA grades | DCS; on-stream XRF → PI Historian | ISA-95 Levels 0, 2; AMIRA P754 Principles 6, 7 | Raw |
| 3.2.3.4 | Operate Zn Cleaner Flotation | Zn cleaner bank(s) upgrade Zn rougher concentrate to final Zn concentrate grade (typically 50–55% Zn for smelter spec; Red Dog targets 57–60% Zn due to high-grade ore). Final Zn cleaner concentrate is a custody transfer point to Zn thickening. Shift composite sample collected from final Zn cleaner overflow. [P754: grade (Zn%, Pb%, Fe%, Cu%, Cd%) + mass flow | on-stream XRF + shift composite | continuous OSA + shift composite | Principles 1, 2, 5, 6, 7 | YES — Zn cleaner final concentrate is a custody transfer point] | 0 / 2 | Zn rougher concentrate; Zn cleaner cells operational | Zn rougher concentrate; air; depressants (NaCN if Pb present) | Final Zn concentrate (to Zn thickening); Zn cleaner tails (recycled); OSA grade data; shift composite sample | DCS; on-stream XRF; LIMS | ISA-95 Levels 0, 2; AMIRA P754 Principles 1, 2, 5, 6, 7 | Raw; Curated (concentrate_production_record — Zn) |
| 3.2.3.5 | Operate Zn Regrind Mill | Where Zn rougher/scavenger concentrate requires additional liberation, a Zn regrind mill (stirred media or ball mill) grinds concentrate before cleaning. [ZINC NOTE: Common at Red Dog to achieve required Zn concentrate grade from coarser-grained sphalerite.] | 0 / 2 | Zn rougher/scavenger concentrate; regrind mill operational | Zn rougher/scavenger concentrate; regrind mill; grinding media; water | Reground Zn concentrate (to Zn cleaner); regrind mill telemetry | DCS; PI Historian | ISA-95 Levels 0, 2 | Raw |
| **3.2.4** | **Lead Flotation Circuit** | *[LEAD-SPECIFIC — where applicable] Applies to: Antamina (where Pb circuit is activated), Red Dog. L0/L1/L2 Process. At polymetallic operations with galena (PbS), a lead flotation circuit follows the Zn circuit (or in some designs, precedes it in a Cu-Pb-Zn sequential circuit). At Red Dog, Pb and Zn are separated by differential flotation — Pb is floated first at low pH (Pb selectivity over sphalerite), then Zn is activated and floated.* | 0–2 | Zn flotation tailings (Antamina) or mill product (Red Dog differential flotation); Pb circuit running | Zn circuit tailings or mill circuit product (Red Dog); Pb-selective collectors; air | Pb concentrate (to Pb thickening); Pb circuit tailings (to final tailings) | Control Room Operator; Metallurgist; DCS | DCS; PI Historian; on-stream XRF | ISA-95 Levels 0–2; AMIRA P754 Principles 1, 2, 5, 6, 7 | Raw; Curated (concentrate_production_record — Pb) |
| 3.2.4.1 | Operate Pb Rougher Flotation | Pb rougher floats galena from the circuit feed. At Red Dog, differential flotation targets Pb first — pH is maintained at 7–8 to naturally depress sphalerite while galena floats. At Antamina, Pb is recovered from Zn circuit tailings using xanthate collectors. On-stream analysis measures Pb%, Zn%, and Ag% in rougher concentrate. [P754: grade (Pb%, Zn%, Ag g/t) | on-stream XRF | continuous (2–4 min) | Principles 1, 2, 6, 7 | NO] | 0 / 2 | Circuit feed conditioned; Pb rougher cells operational | Circuit feed; Pb-selective collector; air | Pb rougher concentrate; Pb rougher tailings; OSA data | DCS; on-stream XRF → PI Historian | ISA-95 Levels 0, 2; AMIRA P754 Principles 1, 2, 6, 7 | Raw |
| 3.2.4.2 | Operate Pb Cleaner Flotation | Pb cleaner(s) upgrade rougher concentrate to final Pb concentrate grade (typically 60–65% Pb, high Ag credit). Final Pb cleaner concentrate is the Pb product — its mass and grade are custody transfer points to Pb thickening. Shift composite sample collected. [P754: grade (Pb%, Zn%, Ag g/t, Au g/t) + mass flow | on-stream XRF + shift composite | continuous OSA + shift | Principles 1, 2, 5, 6, 7 | YES — Pb cleaner final concentrate is a custody transfer point] | 0 / 2 | Pb rougher concentrate; Pb cleaner cells operational | Pb rougher concentrate; air; depressants (NaCN for sphalerite depression) | Final Pb concentrate (to Pb thickening); Pb cleaner tails (recycled); OSA data; shift composite sample | DCS; on-stream XRF; LIMS | ISA-95 Levels 0, 2; AMIRA P754 Principles 1, 2, 5, 6, 7 | Raw; Curated (concentrate_production_record — Pb) |
| 3.2.4.3 | Operate Pb Regrind Mill | Where required for improved liberation, Pb rougher concentrate is reground before cleaning. [LEAD NOTE: More common at Red Dog where ore mineralogy requires it.] | 0 / 2 | Pb rougher concentrate; regrind mill operational | Pb rougher concentrate; regrind mill; grinding media; water | Reground Pb concentrate (to Pb cleaner); regrind mill telemetry | DCS; PI Historian | ISA-95 Levels 0, 2 | Raw |

### 3.3 Dewatering & Product Handling

| ID | Activity Name | Description | ISA-95 Level | Trigger | Inputs | Outputs | Primary Actor(s) | Source System(s) | Standard Alignment | DDVC Layer |
|----|---------------|-------------|--------------|---------|--------|---------|-----------------|------------------|--------------------|------------|
| **3.3** | **Dewatering & Product Handling** | *L2 Process Area. Reduces moisture content of flotation concentrate from slurry (~40–60% solids w/w) to filter cake suitable for transport (typically 8–12% moisture for Cu; 6–10% for Zn/Pb depending on smelter specification). Separate dewatering trains run per concentrate type. Tailings are thickened and pumped to the TSF with process water recovered.* | 0–2 | Flotation concentrate available from cleaner circuits; thickeners and filters operational | Flotation concentrate slurry (by type: Cu, Zn, Pb); tailings slurry from flotation; flocculant | Filter cake (by type — at target moisture %); process water (recovered); tailings pulp (to TSF) | Control Room Operator; DCS Auto-control; Metallurgist | DCS; PI Historian; LIMS (moisture verification) | ISA-95 Levels 0–2; AMIRA P754 Principles 1, 5, 7 | Raw (time-series); Curated (concentrate_production_record, process_measurement_point) |
| **3.3.1** | **Concentrate Thickening** | *L0/L1/L2 Process. Concentrate thickener(s) settle and compact the dilute flotation concentrate slurry by gravity sedimentation, aided by flocculant addition. Thickener underflow (high-density slurry, typically 55–70% solids) is pumped to the filter. Thickener overflow (clarified process water) is returned to the process water circuit. Separate thickeners are operated per concentrate type at polymetallic operations.* | 0–2 | Flotation cleaner concentrate available; thickener operational | Flotation concentrate slurry (dilute); flocculant; thickener (operational) | Thickened underflow (high-density slurry — to filter); clarified overflow (to process water return); thickener operating data | DCS Auto-control; Control Room Operator | DCS; PI Historian; nuclear density gauge | ISA-95 Levels 0–2; AMIRA P754 Principles 1, 7 | Raw (time-series: thickener_telemetry) |
| 3.3.1.1 | Feed Concentrate to Thickener | Flotation concentrate slurry (Cu, Zn, or Pb cleaner overflow) is pumped from the cleaner circuit to the thickener feedwell. Feed rate (m³/hr and t solids/hr) is measured by magnetic flowmeter and nuclear density gauge on the concentrate feed line. This measurement is the first fixed-instrument mass flow measurement of the final concentrate product stream. [P754: mass flow + density (solids t/hr) | magnetic flowmeter + nuclear density gauge | continuous (1-min) | Principles 1, 2, 7 | PARTIAL — this is the first fixed mass flow measurement of the concentrate product stream] | 1 / 2 | Cleaner concentrate available; feed pump running; thickener operational | Flotation cleaner concentrate slurry; concentrate feed pump; feed flowmeter and density gauge | Thickener feed mass flow record (t/hr slurry; solids t/hr); density record; feed volume record | DCS Auto-control | DCS; PI Historian (flowmeter, density gauge) | ISA-95 Levels 1, 2; AMIRA P754 Principles 1, 2, 7 | Raw (time-series) |
| 3.3.1.2 | Dose Flocculant | Polymer flocculant is dosed into the thickener feedwell to accelerate particle settling and achieve target underflow density. Dosage rate (g/t of solids) is set by the metallurgist and controlled by DCS. Excessive dosing increases cost without benefit; under-dosing produces dilute underflow and reduces filter throughput. Flocculant consumption is tracked per shift (kg or g/t solids). [P754: mass (flocculant consumption) | dosing pump counter + tank level | shift total | Principle 1 | NO] | 1 / 2 | Thickener feed active; flocculant solution prepared and in tank; dosing pump operational | Polymer flocculant solution; dosing pump; thickener (active) | Flocculant dosing rate record (mL/min, g/t equivalent); thickener underflow density response | DCS Auto-control; Metallurgist | DCS; PI Historian | ISA-95 Levels 1, 2; AMIRA P754 Principle 1 | Raw |
| 3.3.1.3 | Pump Thickener Underflow to Filter | Thickener underflow pump transfers high-density concentrate slurry from the thickener cone to the filter feed tank. Underflow density (nuclear density gauge) and flow rate (magnetic flowmeter) are monitored continuously. Underflow density is the primary thickener control variable — target density ensures efficient filter performance. [P754: mass flow + density (solids t/hr) | magnetic flowmeter + nuclear density gauge | continuous (1-min) | Principles 1, 7 | NO — internal transfer] | 1 / 2 | Thickener underflow at target density; underflow pump running; filter feed tank below maximum | Thickened concentrate slurry; underflow pump (running); density and flow sensors | Underflow mass flow (t/hr) to filter feed tank; underflow density record | DCS Auto-control | DCS; PI Historian | ISA-95 Levels 1, 2; AMIRA P754 Principles 1, 7 | Raw (time-series: thickener_telemetry) |
| **3.3.2** | **Concentrate Filtration** | *L0/L1/L2 Process. The filter (disc filter, pressure filter, or belt filter depending on site) removes the majority of remaining process water from the thickened concentrate slurry, producing a filter cake at the target moisture specification. Moisture content verification of the filter cake is mandatory — it is a commercial product specification and a P754 mass measurement requirement. Separate filters run per concentrate type.* | 0–2 | Thickener underflow at target density in filter feed tank; filter operational | Thickened concentrate slurry (from thickener underflow); compressed air (for pressure filters); wash water (where applicable) | Filter cake (physical — target moisture %); filtrate water (to process water return); filter operating data | DCS Auto-control; Control Room Operator | DCS; PI Historian; moisture analyser or lab | ISA-95 Levels 0–2; AMIRA P754 Principles 1, 5, 7, 8 | Raw; Curated (concentrate_production_record — moisture attribute) |
| 3.3.2.1 | Operate Filter Press or Disc Filter | The filter operates on a feed-press-blow-discharge cycle (pressure filter) or a continuous rotary vacuum cycle (disc filter). DCS monitors and controls filtration pressure (kPa), vacuum level, cycle time, and wash water volume. Filter throughput (solids t/hr per filter) and filtrate flow rate are logged. Filter performance is evaluated by filter cake solids content (%) and throughput rate. | 0 / 2 | Filter feed tank loaded; filter operational; compressed air / vacuum available | Thickened concentrate slurry; compressed air or vacuum; wash water (if used) | Filter cake (physical); filtrate water (to return); filter operating data (cycle time, pressure, vacuum, wash water) | DCS Auto-control | DCS; PI Historian | ISA-95 Levels 0, 2; AMIRA P754 Principles 1, 7 | Raw (time-series: filter_telemetry) |
| 3.3.2.2 | Discharge Filter Cake | Filter cake is discharged from the filter onto a conveyor belt or into a transport container (at operations using containers for concentrate export). Discharge event initiates tracking of the filter cake batch as a physical product entity. At some operations, filter cake is weighed on a conveyor belt scale or bin scale at discharge — this is the primary dry tonnes measurement for the final product. [P754: mass (dry tonnes — key commercial measurement) | belt weigher on cake discharge conveyor or bin scale | per batch / continuous | Principles 1, 5, 7, 8 | YES — filter cake discharge is the primary internal dry tonnes measurement of the concentrate product before stockpiling] | 1 / 0 | Filter cycle complete; cake formed; discharge valve/mechanism open | Filter cake (physical, in filter chambers); discharge conveyor or container; belt weigher or bin scale | Filter cake discharged to conveyor/container (physical); filter cake batch mass record (wet tonnes, if belt scale present); filter cycle record | Plant Operator; DCS | DCS; belt weigher → PI Historian | ISA-95 Levels 0, 1; AMIRA P754 Principles 1, 5, 7, 8 | Raw; Curated (concentrate_production_record — batch mass) |
| 3.3.2.3 | Verify Moisture Content | Moisture content of the filter cake is measured against the commercial specification and metallurgical accounting requirement. Method: grab sample taken from the conveyor discharge at defined frequency (typically each filter cycle or each hour), weighed wet and dry (oven dried at 105°C for 4 hours). Moisture % = (wet mass − dry mass) / wet mass × 100. Result is entered into LIMS and compared to smelter contract moisture specification. If out of specification, metallurgist assesses cause and adjusts filter operating parameters. [P754: moisture % (critical commercial parameter) | oven drying (gravimetric) or infrared moisture analyser | per filter cycle (every 1–4 hours) | Principles 1, 5, 7, 8 | YES — moisture % is an essential parameter in the dry tonnes calculation for commercial invoice; P754 Principle 5 (mass measurement at custody transfer)] | 3 | Filter cycle complete; sample taken; lab analysis complete | Filter cake grab sample; oven balance or infrared moisture analyser; LIMS | Moisture % per sample (entered in LIMS); shift average moisture; pass/fail vs. contract specification | Process Technician; Metallurgist | LIMS; PI Historian (if online moisture analyser) | ISA-95 Level 3 (quality management); AMIRA P754 Principles 1, 5, 7, 8 | Raw; Curated (concentrate_production_record — moisture %) |
| **3.3.3** | **Tailings Management** | *L0/L1/L2 Process. Flotation tailings (the mineral and gangue fraction not recovered as concentrate) are thickened, pumped, and deposited in the Tailings Storage Facility (TSF). Process water is recovered from the TSF and returned to the plant water circuit. Tailings represent the major waste stream of the plant and the closure of the plant-side mass balance.* | 0–2 | Flotation tailings available from scavenger circuits; tailings thickener operational; TSF accepting | Flotation tailings slurry (from Cu scavenger, Zn scavenger, or combined tailings); flocculant; process water circuit | Tailings deposited at TSF; recovered process water (returned to plant); tailings density and flow records | Control Room Operator; DCS; Environmental Officer | DCS; PI Historian; SCADA (tailings pump station and TSF) | ISA-95 Levels 0–2; AMIRA P754 Principles 1, 5, 7 | Raw (time-series: tailings_telemetry) |
| 3.3.3.1 | Thicken Tailings | Tailings thickener(s) receive combined flotation tailings and settle solids for densification before pumping. Flocculant is dosed. Underflow density and flow rate are monitored. Thickened tailings underflow is pumped to the tailings pump station. Tailings thickener overflow (clarified water) returns directly to the process water circuit — this is a significant water recovery point. [P754: mass flow + density (t/hr solids) | magnetic flowmeter + nuclear density gauge | continuous (1-min) | Principles 1, 7 | NO] | 0 / 2 | Flotation tailings available; tailings thickener operational | Flotation tailings slurry; flocculant; tailings thickener | Thickened tailings underflow (to tailings pump station); clarified overflow (to process water return); tailings density and flow records | DCS Auto-control | DCS; PI Historian | ISA-95 Levels 0, 2; AMIRA P754 Principles 1, 7 | Raw |
| 3.3.3.2 | Pump Tailings to TSF | Thickened tailings are pumped from the tailings pump station to the TSF via a tailings pipeline. Multiple pump stages may be required depending on head. Pipeline pressure, flow rate, and density are monitored continuously. Pump station DCS/SCADA provides automated control and alarming. Flow interruption (pipeline failure, pump failure) is a critical environmental incident trigger. [P754: mass flow + volume | magnetic flowmeter + nuclear density gauge | continuous (1-min) | Principles 1, 5 | NO — within plant boundary; custody transfer at TSF is environmental, not commercial] | 1 / 2 | Thickened tailings available; tailings pump(s) operational; TSF accepting | Thickened tailings slurry; tailings pump(s); tailings pipeline; TSF receiving cell | Tailings delivered to TSF (t solids/hr, m³/hr); pump station telemetry (pressure, flow, speed); pipeline pressure profile | DCS/SCADA (tailings pump station); PI Historian | ISA-95 Levels 1, 2; AMIRA P754 Principles 1, 5 | Raw (time-series: tailings_pump_telemetry) |
| 3.3.3.3 | Deposit Tailings at TSF | Tailings slurry is discharged at the TSF via spigots on the embankment crest or beach. Discharge point rotation (spigot management) controls beach formation and pond location. TSF freeboard, pond level, seepage, and embankment deformation are monitored continuously by the environmental/geotechnical team. Deposition records (volume, density, cell number) are maintained for TSF mass balance closure. [P754: volume (deposited to TSF) | TSF survey + flow integration | periodic survey / continuous flow | Principles 1, 7 | PARTIAL — TSF is the final sink of the plant-side mass balance; total solids deposited is required for P754 reconciliation] | 0 / 3 | Tailings pump delivering to TSF; discharge spigots open at assigned cell | Tailings slurry (from tailings pump station); TSF embankment and cells (physical) | Tailings deposited (physical); deposition volume record; TSF pond level record; seepage monitoring data | Environmental Officer; TSF Operator | DCS/SCADA (TSF monitoring); TSF geotechnical monitoring system; PI Historian | ISA-95 Levels 0, 3; AMIRA P754 Principles 1, 7 | Raw; Curated (tsf_inventory_record) |
| 3.3.3.4 | Recover Process Water from TSF | Decant water from the TSF pond is returned to the plant via the reclaim water pump station. Reclaim flow rate and volume are measured by flow meter. Reclaim water quality (metal content, pH, suspended solids) is sampled for environmental monitoring. This water return closes the plant water circuit. [P754: volume (water recovery) | magnetic flowmeter on reclaim line | continuous (1-min) | Principles 1, 7 | NO — internal water circuit] | 1 / 2 | TSF pond level above reclaim pump intake; reclaim pump operational | TSF decant pond (physical); reclaim pump; reclaim pipeline | Process water returned to plant (m³/hr, cumulative m³/shift); reclaim water flow record; water quality sample (periodic) | DCS/SCADA; Environmental Officer | DCS/SCADA; PI Historian (reclaim flow meter); LIMS (water quality sample) | ISA-95 Levels 1, 2; AMIRA P754 Principles 1, 7 | Raw |

---

### 3.4 Metallurgical Accounting & Quality

| ID | Activity Name | Description | ISA-95 Level | Trigger | Inputs | Outputs | Primary Actor(s) | Source System(s) | Standard Alignment | DDVC Layer |
|----|---------------|-------------|--------------|---------|--------|---------|-----------------|------------------|--------------------|------------|
| **3.4** | **Metallurgical Accounting & Quality** | *L2/L3 Process Area. Systematic collection of representative samples, chemical analysis, and mass balance closure across the plant. Metallurgical accounting is the mechanism by which all mass flows, grades, and recoveries are reconciled to verify and report plant performance. This process area is governed end-to-end by AMIRA P754 and all 10 of its principles apply within it.* | 2–3 | Continuous sampling; shift-end balance; daily and monthly reconciliation schedule | All plant sample streams (concentrate, tailings, feed, OSA); mass flow data from all P754 measurement points; LIMS assay results | Shift mass balance report; daily/weekly reconciliation report; monthly metal accounting report; stocktake records | Chief Metallurgist; Metallurgist; Plant Chemist; Metallurgical Accounting Analyst | LIMS; metallurgical accounting software; DCS (mass flow data); PI Historian | AMIRA P754 (all 10 principles); ISA-95 Levels 2, 3 | Raw; Curated (shift_mass_balance, metallurgical_accounting_report) |
| **3.4.1** | **Sampling** | *L1/L3 Process. Representative sampling of all plant streams at defined measurement points is the foundation of metallurgical accounting. AMIRA P754 Principle 6 (representative, unbiased sampling) is the governing constraint. Automatic samplers on continuous streams; grab/composite sampling for batch and periodic streams.* | 1–3 | Continuous (auto-samplers); shift schedule (composites); batch event (filter cake) | Process streams (all measurement points); auto-sampling equipment; sample containers | Physical samples (per stream, per interval); sample submission records (LIMS) | Plant Chemist; Process Technician | Auto-sampling equipment (vezin sampler, cross-belt sampler); LIMS (sample registration) | ISA-95 Levels 1, 3; AMIRA P754 Principles 1, 5, 6, 7, 10 | Raw; Curated (sample_submission) |
| 3.4.1.1 | Collect In-Stream Samples via Auto-Sampler | Automatic samplers (cross-stream, vezin-type, or cross-belt) collect primary increments from designated plant streams at timed intervals (typically every 15–60 minutes). Streams sampled: flotation feed, Cu rougher concentrate, Cu final concentrate, Cu tailings, Zn rougher concentrate (where applicable), Zn final concentrate, Zn tailings, Pb final concentrate (where applicable), plant composite tailings. Primary increments are accumulated in a sample cutter over the shift to form a shift composite. [P754: grade (all relevant metals + moisture) | automatic in-stream sampler | continuous increment (every 15–60 min); shift composite assembled | Principles 6, 7, 10 | YES for concentrate final streams; NO for intermediate streams] | 1 | Scheduled sampling interval; plant stream flowing | Plant process stream (flowing); automatic sampler (operational, calibrated); sample collection vessel | Primary increments (physical — accumulated per shift composite); sample cutter operation record (increment count, interval) | Automated (auto-sampler); Plant Chemist (oversight) | Auto-sampler control unit; LIMS (sample event log) | ISA-95 Level 1; AMIRA P754 Principles 6, 7, 10 | Raw; Curated (sample_submission) |
| 3.4.1.2 | Collect Grab and Composite Samples | Operators collect grab samples from specific point locations (filter cake conveyor, concentrate shed, reclaim conveyor) at defined intervals or for batch-specific QC. Composites are formed from multiple grab increments accumulated over the shift. Used where auto-samplers are not installed or for verification sampling. [P754: grade + moisture | grab sample (manual) | defined intervals per sampling plan | Principles 6, 7 | Conditional — depends on stream designation in site sampling plan] | 3 | Sampling schedule; batch-specific trigger (filter cake batch, stockpile increment) | Process stream or physical product; sample bags, containers, labels; sampling tools | Physical grab samples (labeled and submitted to lab); sample submission record in LIMS | Process Technician | LIMS (sample registration) | ISA-95 Level 3 (quality management); AMIRA P754 Principles 6, 7 | Raw |
| 3.4.1.3 | Prepare Samples for Analysis | Physical samples are processed in the sample preparation laboratory: weighed (wet mass), dried (oven at 105°C), re-weighed (dry mass — moisture % calculated), pulverised (ring mill or LM5) to a fine powder, split (riffle splitter or rotary divider) to produce the assay sub-sample, and sealed for dispatch to the primary laboratory. QC samples (duplicates, certified reference materials, blanks) are inserted at the sample preparation stage. [P754: mass (wet and dry mass for moisture %); grain size of prepared pulp | gravimetric balance + oven; ring mill; riffle splitter | per sample received | Principles 6, 7, 10 | NO — sample preparation is internal to the QA/QC process] | 3 | Samples received from field or auto-sampler | Physical samples; drying oven; pulverising mill; splitting equipment; analytical balance; QC reference materials | Dried and pulverised assay sub-samples; moisture % (per sample); QC sample inserts; sample preparation record in LIMS | Laboratory Technician | LIMS (sample preparation workflow) | ISA-95 Level 3; AMIRA P754 Principles 6, 7, 10 | Raw; Curated (sample_submission — preparation attributes) |
| **3.4.2** | **Assay & Analysis** | *L1/L3 Process. Chemical analysis of prepared samples determines the grade (metal content) of each process stream. Two parallel analytical channels exist: (1) the primary laboratory (fire assay for Au, ICP-OES/MS or XRF for base metals) for shift composite, daily composite, and concentrate product samples; (2) on-stream analysis (OSA) using online XRF analyzers for real-time process control.* | 1–3 | Samples available from preparation; OSA continuous | Prepared assay pulps; QC reference materials; on-stream slurry flows | Assay results per sample (metal content %); OSA stream grades (real-time); QA/QC performance report | Laboratory Analyst; Process Metallurgist; LIMS | LIMS; on-stream XRF analyser; ICP-OES/MS; XRF laboratory analyser | ISA-95 Levels 1, 3; AMIRA P754 Principles 1, 5, 6, 7, 8, 10 | Raw; Curated (assay_result, osa_grade_record) |
| 3.4.2.1 | Perform Laboratory Assay | Primary laboratory analysis of prepared assay pulps using: ICP-OES or ICP-MS (for Cu, Zn, Pb, Fe, Mo, and trace elements), XRF (for major element oxides and base metals), or fire assay (for Au, Ag). Results are entered into LIMS with certified reference material results and QC flags. Laboratory TAT is typically 8–24 hours for routine shift composites; 24–48 hours for monthly certification samples. [P754: grade (Cu%, Zn%, Pb%, Ag g/t, Au g/t, Fe%, S%, Mo% where applicable, moisture %) | ICP-OES/ICP-MS, XRF, fire assay | per batch (shift composite, daily composite, certification sample) | Principles 1, 5, 6, 7, 8 | YES for concentrate certification samples; NO for intermediate stream composites] | 3 | Assay pulps received from sample preparation; analytical instruments available | Assay pulps; ICP/XRF/fire assay instruments; certified reference materials; blank and duplicate pairs | Assay results per sample (in LIMS); QC performance metrics (CRM recovery, duplicate precision, blank contamination) | Laboratory Analyst | LIMS; ICP-OES/MS instrument software; XRF instrument software | ISA-95 Level 3; AMIRA P754 Principles 1, 5, 6, 7, 8 | Raw; Curated (assay_result) |
| 3.4.2.2 | Analyse Streams via On-Stream XRF | Online XRF analyzers (multi-stream) continuously analyse slurry streams at 2–4 minute scan intervals, providing near-real-time grade data for process control. Each analyzer handles multiple streams sequentially via a stream sequencer. OSA data is used by the metallurgist for flotation control adjustments (reagent dosage, froth depth, air rate). OSA data is secondary to lab assay for accounting purposes — it provides the high-frequency trend for process control, not the definitive grade for mass balance closure. [P754: grade (Cu%, Zn%, Pb%, Fe%) | online XRF | continuous (2–4 min per stream per scan cycle) | Principles 6, 7 | YES for monitoring; NO for primary accounting — lab assay is primary] | 1 / 2 | Plant streams flowing; OSA analyzer operational; stream sequencer active | Slurry streams (multiple — connected via sample lines to OSA); on-stream XRF analyzer | OSA grade data per stream per scan interval (Cu%, Zn%, Pb%, Fe% — archived in PI Historian); OSA performance diagnostics | DCS (OSA data integration); Metallurgist | On-stream XRF analyzer → PI Historian; DCS (grade control interface) | ISA-95 Levels 1, 2; AMIRA P754 Principles 6, 7 | Raw (time-series: osa_grade_telemetry) |
| 3.4.2.3 | Perform QA/QC on Analytical Results | The laboratory inserts QC samples at a defined rate: certified reference materials (CRMs — typically 1 in 10 samples), field duplicates (1 in 20 samples), and blanks (1 in 20 samples). LIMS compiles QC statistics: CRM accuracy (recovery %), duplicate precision (RPD %), blank contamination. Control charts (Shewhart or CUSUM) flag systematic bias. QA/QC failure triggers re-assay of the affected batch. [P754: bias detection and accuracy | QC statistical analysis in LIMS | per analytical batch | Principles 8, 10 | YES for concentrate certification — failure to meet QC criteria invalidates the associated commercial assay] | 3 | Analytical batch complete; QC results available in LIMS | QC results (CRM, duplicate, blank) in LIMS; analytical batch results; QC acceptance criteria | QC statistics report (per batch); CRM control chart; duplicate RPD chart; batch acceptance/rejection flag; re-assay instruction (if QC failure) | Laboratory Analyst; Chief Metallurgist | LIMS (QC module) | ISA-95 Level 3 (quality management); AMIRA P754 Principles 8, 10 | Raw; Curated (qc_performance_record) |
| **3.4.3** | **Mass Balance & Reconciliation** | *L3 Process Area. Periodic mass balance closure integrates all mass flow measurements (belt weighers, flowmeters, density gauges) and grade measurements (lab assay, OSA) to compute metal produced, metal recovered, metal lost (to tailings), and metal unaccounted for. This is the core deliverable of AMIRA P754 compliance and the primary source of reconciliation data for mine-to-mill and mill-to-port reporting.* | 3 | Shift end; daily schedule; monthly schedule; stocktake trigger | All shift mass flow data (PI Historian); shift composite assay results (LIMS); reagent consumption records; stockpile inventory data | Shift mass balance report; daily/weekly reconciliation report; monthly metal accounting report; inventory variance report | Chief Metallurgist; Metallurgical Accounting Analyst; Plant Manager | Metallurgical accounting software; LIMS; PI Historian; DCS (mass flow data) | AMIRA P754 (all 10 principles); ISA-95 Level 3 | Curated (shift_mass_balance, metallurgical_accounting_report) |
| 3.4.3.1 | Close Shift Mass Balance | At each shift end, the metallurgist runs the shift mass balance calculation: sum of ore feed mass (belt weigher) × feed grade (assay) = sum of concentrate mass (filter cake belt weigher × moisture correction to dry tonnes) × concentrate grade (shift composite assay) + sum of tailings mass × tailings grade. Balance error (%) = (feed metal − products metal) / feed metal × 100. Acceptable shift balance error is site-specific (typically ±5% for shift; tighter at daily). [P754: ALL measurement types — integrates mass, grade, density, moisture | integrates all instrument types | per shift | ALL 10 Principles | YES — shift mass balance is the formal P754 accounting period closure at the shift level] | 3 | Shift end; all shift composite assays returned from lab; mass flow data available | Shift mass flow data (PI Historian — belt weighers, flowmeters); shift composite assay results (LIMS); moisture % results; reagent consumption data | Shift mass balance report (feed tonnes, feed grade, Cu tonnes, Zn tonnes, Pb tonnes produced, recovery %, balance error %); balance error flag (if outside tolerance) | Metallurgist | Metallurgical accounting software; LIMS; PI Historian | ISA-95 Level 3; AMIRA P754 Principles 1–10 (synthesis) | Curated (shift_mass_balance) |
| 3.4.3.2 | Perform Daily and Weekly Reconciliation | Daily and weekly reconciliations aggregate shift mass balances, apply any laboratory result updates (re-assays, late results), and cross-check against independent measurements (stockpile surveys, weighbridge records from incoming concentrate trucks). Discrepancies beyond tolerance thresholds trigger investigation. The daily reconciliation is the primary operational performance report reviewed by the plant manager. | 3 | Daily (previous day actuals available); weekly (weekly close) | Shift mass balance records; updated assay results; stockpile survey (if periodic); weighbridge records (outbound concentrate) | Daily/weekly reconciliation report; discrepancy investigation records; corrected period balance; updated metal inventory position | Chief Metallurgist; Metallurgical Accounting Analyst | Metallurgical accounting software; LIMS; PI Historian; ERP (weighbridge data) | ISA-95 Level 3; AMIRA P754 Principles 2, 3, 7, 8 | Curated (metallurgical_accounting_report) |
| 3.4.3.3 | Produce Monthly Metal Accounting Report | The monthly metal accounting report is the definitive financial-period production record. It aggregates all daily reconciliations, applies the final month-end assay certification results (independent third-party umpire assays for commercial concentrate batches), and closes the formal accounting period. The report is submitted to corporate finance, the audit committee, and relevant regulatory authorities. [P754: ALL Principles — the monthly report is the culmination of full P754 compliance | all instrument types + certification lab assay | monthly period close | ALL 10 Principles | YES — the monthly concentrate production figure is the basis for commercial invoicing and revenue recognition] | 3 | Month end; all certification assays received; stocktake completed; all daily reconciliations closed | All daily reconciliation records; certification assay results (concentrate batches — third party umpire); stocktake results; opening and closing inventory | Monthly metal accounting report (produced metal by metal; shipped metal; inventory change; recovery by metal; balance error %); audit-ready documentation | Chief Metallurgist; Finance; Plant Manager | Metallurgical accounting software; LIMS; ERP (inventory and revenue) | ISA-95 Level 4 (business reporting); AMIRA P754 Principles 1–10 | Curated (metallurgical_accounting_report — monthly); Contextualized (recovered metal by period, recovery %) |
| 3.4.3.4 | Conduct Inventory Adjustment and Stocktake | Physical stocktake of all in-process inventory (COS, flotation feed bins, concentrate sheds, TSF) is conducted periodically (monthly minimum; quarterly formal) to verify the book inventory against physical inventory. Survey methods: drone volumetric survey (COS and concentrate shed), belt weigher integration (conveyors), filter cake batch records (filter output). Inventory adjustments (book vs. physical variances) are recorded as adjustments in the metallurgical accounting system. [P754: mass (physical inventory vs. book inventory) | physical survey (drone + geodetic) + weighbridge records | monthly (minimum) | Principles 3, 9 | YES — inventory is a component of the check-in / check-out mass balance boundary] | 3 | Monthly close; formal quarterly stocktake schedule | Physical inventory (COS, concentrate shed, in-process); survey equipment (drone, GPS, survey instruments); filter cake batch records | Stocktake measurement per inventory location (tonnes, volume, grade); variance report (physical vs. book); inventory adjustment entries; formal stocktake documentation | Chief Metallurgist; Survey Team; Metallurgical Accounting Analyst | Survey system (drone + GPS); metallurgical accounting software; LIMS | ISA-95 Level 3; AMIRA P754 Principles 3, 9 | Curated (stockpile_inventory — physical reconciliation); Curated (metallurgical_accounting_report — inventory adjustment) |

---

## Mass Balance Node Maps

### Mass Balance Node Map: Copper Flotation Circuit
Applies to: QB, HVC, CdA (single Cu circuit); Antamina (Cu circuit first stage)

```
                            [FEED NODE]
                    Cyclone Overflow (Mill Circuit Product)
                    ─────────────────────────────────────
                    Mass:   F_cu t/hr (belt weigher — continuous)
                    Grade:  f_cu% Cu (OSA + shift composite — lab)
                    P754:   Measurement Point MP-01 | Principles 1,2

                            │
                            ▼
            ┌───────────────────────────────┐
            │     Cu ROUGHER BANK          │
            │  Air + Collector + Frother   │
            └──────────────┬───────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
      [ROUGHER CONCENTRATE]    [ROUGHER TAILINGS]
      To Scavenger / Cleaner    To Cu Scavenger
      Grade: OSA (2-4 min)      Grade: OSA (2-4 min)
      P754: MP-02 | P6,P7       P754: MP-03 | P6,P7
              │
              ▼
            ┌───────────────────────────────┐
            │     Cu SCAVENGER BANK        │
            │  Additional Collector        │
            └──────────────┬───────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
     [SCAVENGER CONCENTRATE]  [Cu TAILINGS — FINAL LOSS]
     Recycled to Rougher       To Zn Circuit (polymetallic)
     or Regrind                or Final Tailings (Cu-only)
                               Grade: OSA + grab sample
                               P754: MP-04 | P7 (KEY LOSS)
              │
              ▼ (if Regrind installed)
            ┌───────────────────────────────┐
            │       Cu REGRIND MILL        │
            │  Improve mineral liberation  │
            └──────────────┬───────────────┘
                           │
                           ▼
            ┌───────────────────────────────┐
            │     Cu CLEANER BANK(S)       │
            │  Depressant for selectivity  │
            └──────────────┬───────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
     [Cu FINAL CONCENTRATE]   [CLEANER TAILS — RECYCLE]
     ★ CUSTODY TRANSFER        Back to Rougher or Regrind
     ─────────────────────
     Mass:  C_cu t/hr
            (feed density × flow → flowmeter + densitometer)
     Grade: c_cu% Cu (OSA 2-4 min + shift composite — lab)
     Moisture: m% (lab — oven dry per filter cycle)
     P754: MP-05 | Principles 1,2,5,6,7,8 | CTP = YES
     ─────────────────────

     MASS BALANCE IDENTITY (per shift, per accounting period):
     F_cu × f_cu = C_cu × c_cu + T_cu × t_cu + Δinventory
     Recovery: R_cu = (C_cu × c_cu) / (F_cu × f_cu) × 100
     Balance error: ε = |F_cu×f_cu − C_cu×c_cu − T_cu×t_cu| / (F_cu×f_cu) × 100
```

**Key AMIRA P754 Measurement Points — Cu Circuit:**

| MP | Stream | Measurement Type | Method | Frequency | Principles | CTP? |
|----|--------|-----------------|--------|-----------|------------|------|
| MP-01 | Mill circuit product (cyclone overflow / COS reclaim) | Mass flow + grade | Belt weigher + shift composite assay | Continuous mass / shift grade | 1, 2, 5 | YES — mine-to-mill internal |
| MP-02 | Cu rougher concentrate | Grade (Cu%, Fe%, S%) | On-stream XRF | 2–4 min | 6, 7 | NO |
| MP-03 | Cu rougher tailings | Grade | On-stream XRF | 2–4 min | 6, 7 | NO |
| MP-04 | Cu scavenger tailings (Cu final loss at Cu-only sites) | Grade (Cu% loss) | On-stream XRF + periodic grab | Continuous OSA / shift composite | 6, 7, 10 | PARTIAL |
| MP-05 | Cu final concentrate (cleaner overflow) | Mass flow + grade + moisture | Flowmeter + densitometer + shift composite assay + oven dry moisture | Continuous mass / shift grade / per filter cycle moisture | 1, 2, 5, 6, 7, 8 | **YES** |
| MP-06 | Combined tailings (to TSF) | Mass flow + grade | Flowmeter + densitometer + shift composite assay | Continuous mass / shift grade | 1, 5, 7 | PARTIAL (plant-TSF boundary) |

---

### Mass Balance Node Map: Zinc Flotation Circuit
Applies to: Antamina (sequential after Cu); Red Dog (primary Zn circuit after differential Pb flotation)

```
                            [ZN CIRCUIT FEED NODE]
                    Cu Scavenger Tailings (Antamina)
                    OR Mill Circuit Product post-Pb circuit (Red Dog)
                    ────────────────────────────────────────────────
                    Mass:   F_zn t/hr (flowmeter + densitometer)
                    Grade:  f_zn% Zn (OSA + composite)
                    P754:   MP-07 | Principles 1,2,7

                            │
                            ▼
            ┌───────────────────────────────┐
            │    CuSO₄ ACTIVATION STAGE    │
            │  Sphalerite surface priming  │
            └──────────────┬───────────────┘
                           │
                           ▼
            ┌───────────────────────────────┐
            │     Zn ROUGHER BANK          │
            │  Xanthate collector + Air    │
            └──────────────┬───────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
     [Zn ROUGHER CONCENTRATE]  [Zn ROUGHER TAILINGS]
     To Zn Scavenger / Cleaner  To Zn Scavenger
     Grade: OSA                 Grade: OSA
     P754: MP-08 | P6,P7        P754: MP-09 | P6,P7
              │
              ▼
            ┌───────────────────────────────┐
            │     Zn SCAVENGER BANK        │
            └──────────────┬───────────────┘
                           │
              ┌────────────┴─────────────────┐
              ▼                               ▼
     [Zn SCAVENGER CONCENTRATE]  [Zn TAILINGS — FINAL LOSS]
     Recycled to Rougher          To Pb circuit (Antamina)
     or Zn Regrind                or Final Tailings (Red Dog post-Pb)
                                  Grade: OSA + shift composite
                                  P754: MP-10 | P7 (KEY ZN LOSS)
              │
              ▼ (if Regrind installed)
            ┌───────────────────────────────┐
            │       Zn REGRIND MILL        │
            └──────────────┬───────────────┘
                           │
                           ▼
            ┌───────────────────────────────┐
            │     Zn CLEANER BANK(S)       │
            │  NaCN depressant (if Pb/Cu)  │
            └──────────────┬───────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
     [Zn FINAL CONCENTRATE]    [Zn CLEANER TAILS — RECYCLE]
     ★ CUSTODY TRANSFER
     ─────────────────────
     Mass:  C_zn t/hr
     Grade: c_zn% Zn, c_pb% Pb (spec: Pb < 1.5% typical)
            c_cu% Cu, c_fe% Fe, c_cd% Cd
     Moisture: m%
     P754: MP-11 | Principles 1,2,5,6,7,8 | CTP = YES
     ─────────────────────

     MASS BALANCE IDENTITY:
     F_zn × f_zn = C_zn × c_zn + T_zn × t_zn + Δinventory
     Recovery: R_zn = (C_zn × c_zn) / (F_zn × f_zn) × 100
```

---

### Mass Balance Node Map: Lead Flotation Circuit (Antamina and Red Dog)
[LEAD-SPECIFIC — where applicable]

```
     [Pb CIRCUIT FEED NODE]
     Zn Scavenger Tailings (Antamina) OR Mill Product at natural pH (Red Dog differential)
     Mass: F_pb t/hr | Grade: f_pb% Pb | P754: MP-12 | Principles 1,2

                     │
                     ▼
     ┌───────────────────────────────┐
     │     Pb ROUGHER BANK          │
     │  Pb-selective collector      │
     │  Low pH (7–8) for Red Dog    │
     └──────────────┬───────────────┘
                    │
       ┌────────────┴────────────┐
       ▼                         ▼
  [Pb ROUGHER CONC]       [Pb ROUGHER TAILS]
  To Pb Regrind/Cleaner    To Final Tailings
  Grade: OSA               P754: MP-13 | P7
  P754: MP-14 | P6,P7
       │
       ▼
     ┌───────────────────────────────┐
     │     Pb CLEANER BANK(S)       │
     │  NaCN depressant (Zn/Fe)     │
     └──────────────┬───────────────┘
                    │
     [Pb FINAL CONCENTRATE]
     ★ CUSTODY TRANSFER
     ───────────────────────
     Mass:  C_pb t/hr
     Grade: c_pb% Pb, c_zn% Zn, c_ag g/t Ag, c_au g/t Au
     Moisture: m%
     P754: MP-15 | Principles 1,2,5,6,7,8 | CTP = YES
```

---

## SIPOC Artifacts

### SIPOC 3.1 — Comminution

| Element | Content |
|---------|---------|
| **Suppliers** | Mine Operations (Pillar 2) — ROM ore tonnes by material type to crusher feed; Mine Planning (Pillar 1) — mill feed grade and tonnage targets (blend plan); Water management — process water supply; Grinding media supplier — steel balls; Primary crusher vendor/maintenance (out of scope) — crusher availability |
| **Inputs** | ROM ore (from haul truck tipping or ROM stockpile reclaim); process water; grinding balls (by size fraction per mill); lime (for pH pre-conditioning where added at mill); COS buffer inventory (stockpile level) |
| **Process** | Progressively reduce ROM ore from P80 150–350 mm to P80 75–150 µm through staged crushing and wet grinding, using belt weighers and density/flow measurement to track mass through the size reduction circuit. |
| **Outputs** | Cyclone overflow at target P80 (mill circuit product — to flotation); COS inventory (buffer); mill operating telemetry (power draw, bearing pressure, throughput, water addition — continuous to PI Historian); belt weigher mass records (crusher feed, discharge conveyor, COS reclaim); particle size analysis results (periodic) |
| **Customers** | Flotation (3.2) — mill circuit product is the flotation feed; Metallurgical Accounting (3.4) — feed mass flow and grade data for mass balance; Mine Planning (Pillar 1) — mill throughput actuals vs. plan |

---

### SIPOC 3.2 — Concentration (Flotation)

| Element | Content |
|---------|---------|
| **Suppliers** | Comminution (3.1) — cyclone overflow at target P80 (flotation feed); Reagent suppliers — collectors, frothers, depressants, CuSO₄, lime; Process water circuit — water from TSF reclaim and fresh water; On-stream analyzer vendor (maintenance) — OSA data availability |
| **Inputs** | Cyclone overflow slurry at target P80 and pH; collectors (xanthates, dithiophosphates); frothers (MIBC, DF250); depressants (NaCN, ZnSO₄, lime); CuSO₄ (Zn activation where applicable); air (cell aeration); process water |
| **Process** | Selectively separate valuable mineral species (chalcopyrite, sphalerite, galena) from gangue by froth flotation, using reagent chemistry to make target minerals hydrophobic. Operate Cu, Zn, and Pb flotation circuits as appropriate to site commodity mix. Generate separate concentrate streams per commodity. |
| **Outputs** | Cu final concentrate slurry (to Cu thickening); Zn final concentrate slurry (to Zn thickening — where applicable); Pb final concentrate slurry (to Pb thickening — where applicable); combined flotation tailings (to tailings thickening); OSA grade data (to PI Historian); shift composite samples (to LIMS); reagent consumption records |
| **Customers** | Dewatering & Product Handling (3.3) — concentrate slurry streams for thickening and filtration; Tailings Management (3.3.3) — combined tailings; Metallurgical Accounting (3.4) — concentrate grade and mass flow data for mass balance |

---

### SIPOC 3.3 — Dewatering & Product Handling

| Element | Content |
|---------|---------|
| **Suppliers** | Flotation (3.2) — concentrate slurry streams (Cu, Zn, Pb) and tailings slurry; Flocculant supplier — polymer flocculant; Compressed air supply — for pressure filters; TSF management — TSF cell availability for tailings deposition |
| **Inputs** | Flotation concentrate slurry (per commodity — dilute, 40–60% solids); combined flotation tailings slurry; polymer flocculant; compressed air (for pressure filters); wash water (where applicable) |
| **Process** | Remove water from concentrate slurry by thickening then filtration to produce filter cake at commercial moisture specification. Thicken and pump tailings to TSF with maximum water recovery to process circuit. |
| **Outputs** | Filter cake (per commodity — physical product at target moisture %; to concentrate shed); filtrate water (returned to process circuit); tailings deposited at TSF (physical); thickener overflow (process water recovered); moisture % verification records (per filter cycle — in LIMS); filter cake batch mass records; TSF deposition records |
| **Customers** | Logistics & Outbound (Pillar 4) — filter cake physical product delivered to concentrate shed; Metallurgical Accounting (3.4) — filter cake mass and moisture data for dry tonnes calculation; Environmental (out of scope as domain) — TSF deposition records, process water quality |

---

### SIPOC 3.4 — Metallurgical Accounting & Quality

| Element | Content |
|---------|---------|
| **Suppliers** | All process areas (3.1–3.3) — mass flow data (PI Historian), sample submissions; Auto-samplers (3.4.1) — physical shift composite samples; Logistics (Pillar 4) — outbound concentrate weights (weighbridge) and CoA (third-party assay) for reconciliation |
| **Inputs** | Shift mass flow data (belt weighers, flowmeters, density gauges — from PI Historian); shift composite assay results (LIMS); OSA grade data (PI Historian); moisture % results (LIMS); reagent consumption records; outbound weighbridge weights and CoA data; stockpile survey data |
| **Process** | Integrate all measurement point data into a closed mass balance per accounting period (shift, daily, monthly). Calculate metal produced, metal recovered, metal lost, and balance error. Flag discrepancies for investigation. Produce the auditable metal accounting record. |
| **Outputs** | Shift mass balance report; daily/weekly reconciliation report; monthly metal accounting report; QA/QC performance reports; inventory adjustment records; audit-ready documentation package |
| **Customers** | Corporate Finance — monthly metal production for revenue recognition; Mine Planning (Pillar 1) — metallurgical reconciliation data for mine model calibration; Logistics & Outbound (Pillar 4) — certified concentrate grade and mass for CoA and commercial invoice; Senior Management / Board — production performance reporting; Audit Committee (per P754 Principle 4) |

---

## Entity Catalog

### Master & Reference Entities

| Entity Name | Entity Type | Business Definition | Grain | Key Attributes | Lifecycle / State Transitions | Relationships | Standard Alignment |
|-------------|-------------|---------------------|-------|----------------|-------------------------------|---------------|--------------------|
| `process_node` | Master | A named, fixed point in the processing plant circuit — a unit operation (e.g., SAG mill, Cu rougher bank, Cu thickener) or a measurement point (e.g., crusher belt weigher, concentrate flowmeter). The canonical reference for all time-series telemetry and measurement data. | One row per named process unit or measurement point | `node_id`, `node_name`, `node_type` (unit_operation/measurement_point), `process_area`, `isa95_level`, `commodity` (Cu/Zn/Pb/All), `amira_p754_mp_id` (if measurement point), `custody_transfer_flag` | Active → Decommissioned (plant change) | GENERATES `process_telemetry`; ASSOCIATED WITH `amira_measurement_point`; LINKED TO `concentrate_production_record` | ISA-95 Level hierarchy (Area → Process Cell → Unit); AMIRA P754 measurement points |
| `amira_measurement_point` | Reference | A formally designated measurement point in the plant circuit conforming to AMIRA P754 requirements. Specifies the measurement type, method, instrument, frequency, and which P754 principles it satisfies. This is the governance reference for mass balance instrument qualification. | One row per P754-designated measurement point | `mp_id`, `mp_name`, `stream_description`, `measurement_type` (mass/grade/density/moisture/volume), `method`, `instrument_type`, `sampling_frequency`, `p754_principles`, `custody_transfer_point_flag`, `primary_or_secondary` (primary accounting vs. check measurement) | Active → Updated (instrument replacement or method change) | LINKED TO `process_node`; PROVIDES DATA TO `shift_mass_balance` | AMIRA P754 Principles 1–10 |
| `reagent_type` | Reference | A specific chemical reagent used in the plant (collector, frother, depressant, flocculant, lime, grinding media). Canonical reference for reagent consumption tracking and cost accounting. | One row per reagent product code | `reagent_id`, `reagent_name`, `reagent_class` (collector/frother/depressant/flocculant/pH_modifier/grinding_media), `supplier`, `typical_dosage_g_t`, `unit_cost_per_kg` | Static reference; updated on product substitution | CONSUMED IN `reagent_addition_record`; LINKED TO `process_node` (addition point) | ISA-95 Level 3 (inventory); AMIRA P754 Principle 1 |
| `concentrate_type` | Reference | A named saleable concentrate product (e.g., "Cu Concentrate — QB", "Zn Concentrate — Red Dog"). Defines the commodity, site, and commercial specification (grade, moisture, penalty elements). | One row per concentrate product definition | `conc_type_id`, `commodity`, `site_id`, `grade_spec_min`, `moisture_spec_max`, `penalty_elements`, `smelter_contract_ref` | Static reference; updated on contract renewal | CLASSIFIES `concentrate_production_record`; LINKED TO `process_node` (final cleaner and filter cake) | AMIRA P754 Principle 5 (commercial specification at custody transfer) |

---

### Transactional / Event Entities

| Entity Name | Entity Type | Business Definition | Grain | Key Attributes | Lifecycle / State Transitions | Relationships | Standard Alignment |
|-------------|-------------|---------------------|-------|----------------|-------------------------------|---------------|--------------------|
| `concentrate_production_record` | Transactional | A shift-level or batch-level record of concentrate produced by commodity, capturing mass (wet and dry tonnes), grade (by metal), moisture %, and the associated measurement basis. This is the central product entity of the Processing pillar — the data object from which commercial invoicing, metallurgical accounting, and mine-to-mill reconciliation are derived. | One row per shift per commodity per site | `prod_record_id`, `concentrate_type_id`, `shift_id`, `wet_tonnes_produced`, `moisture_pct`, `dry_tonnes_produced`, `grade_cu_pct`, `grade_zn_pct`, `grade_pb_pct`, `grade_ag_g_t`, `grade_au_g_t`, `mass_measurement_basis`, `grade_measurement_basis`, `balance_error_pct` | Preliminary (shift-end estimate) → Lab-confirmed (assay complete) → Certified (monthly) | BELONGS TO `concentrate_type`; CLOSES within `shift_mass_balance`; MEASURED AT `amira_measurement_point` (MP-05, MP-11, MP-15) | AMIRA P754 Principles 1, 5, 7, 8 |
| `shift_mass_balance` | Transactional | A formal closure of the plant mass balance for one shift period, integrating all mass flow measurements and grade analyses to confirm metal inputs equal metal outputs within an acceptable tolerance. The P754 shift-level accounting record. | One row per shift per site | `balance_id`, `shift_id`, `site_id`, `feed_dry_t`, `feed_grade_cu_pct`, `feed_grade_zn_pct`, `cu_produced_dry_t`, `zn_produced_dry_t`, `pb_produced_dry_t`, `cu_recovery_pct`, `zn_recovery_pct`, `pb_recovery_pct`, `cu_balance_error_pct`, `zn_balance_error_pct`, `balance_status` (open/closed/accepted/flagged) | Open (shift start) → In Progress → Closed (shift end calculation) → Accepted or Flagged | AGGREGATES `concentrate_production_record`; INTEGRATES `process_measurement_point` data; CONTAINS `qc_performance_record` | AMIRA P754 Principles 1–10 (synthesis) |
| `sample_submission` | Transactional | A physical sample submitted to the laboratory for analysis, registered in LIMS with its source stream, collection method, collection time, and chain of custody. The sample submission is the provenance record for every analytical result. | One row per submitted sample | `sample_id`, `lims_barcode`, `source_stream`, `sample_type` (auto-sampler composite/grab/duplicate/CRM/blank), `collection_timestamp_utc`, `collection_method`, `submitting_technician`, `lab_received_timestamp`, `lab_result_completed_timestamp` | Collected → Submitted → Received by Lab → In Preparation → Analysed → QC_Reviewed → Closed | LINKED TO `process_node` (source stream); PRODUCES `assay_result`; ASSOCIATED WITH `shift_mass_balance` | AMIRA P754 Principles 6, 7, 10 |
| `assay_result` | Transactional | A laboratory analytical result for a specific sample, reporting the grade of one or more analytes (metal content %) with associated QC metadata. | One row per sample per analytical method (or per analyte if system design requires) | `result_id`, `sample_id`, `analyte` (Cu%, Zn%, Pb%, Ag_g_t, Au_g_t, Fe%, S%, moisture_pct, etc.), `result_value`, `result_units`, `analytical_method`, `lab_instrument_id`, `analyst_id`, `crm_batch`, `qc_flag`, `result_timestamp_utc` | Provisional → QC_Reviewed → Validated → Released | LINKED TO `sample_submission`; CONSUMED BY `shift_mass_balance`; VALIDATED BY `qc_performance_record` | AMIRA P754 Principles 1, 5, 6, 7, 8, 10 |
| `reagent_addition_record` | Transactional | A shift-level record of reagent consumed per addition point per shift, derived from dosing pump flow meter integration or tank level change. Used for cost accounting and mass balance input verification. | One row per reagent per addition point per shift | `addition_id`, `reagent_type_id`, `process_node_id`, `shift_id`, `quantity_kg`, `dosage_g_t_calculated`, `measurement_method` (flow meter/tank level) | Shift end closure event | LINKED TO `reagent_type`; LINKED TO `process_node`; ASSOCIATED WITH `shift_mass_balance` | AMIRA P754 Principle 1 |
| `qc_performance_record` | Transactional | A QA/QC summary for a laboratory analytical batch, capturing CRM accuracy, duplicate precision, and blank contamination statistics. The record determines whether the batch meets AMIRA P754 accuracy requirements and whether associated assay results are accepted or require re-analysis. | One row per analytical batch | `qc_record_id`, `batch_id`, `lab_id`, `analytical_method`, `crm_accuracy_pct`, `duplicate_rpd_pct`, `blank_contamination_flag`, `batch_qc_status` (pass/fail), `re_assay_instruction` | Per analytical batch | VALIDATES `assay_result`; LINKED TO `shift_mass_balance` (batch acceptance) | AMIRA P754 Principles 8, 10 |

---

### Time-Series Entities

| Entity Name | Entity Type | Business Definition | Grain | Key Attributes | Relationships | Standard Alignment |
|-------------|-------------|---------------------|-------|----------------|---------------|--------------------|
| `mill_telemetry` | Time-Series | Continuous operating data from SAG and ball mills: power draw, bearing pressure, feed rate, water addition, speed (% critical), and mill charge proxy parameters. Logged at 1-minute intervals to PI Historian. Primary data source for mill throughput optimisation and energy efficiency analysis. | One row per minute per mill | `node_id`, `timestamp_utc`, `power_draw_kw`, `bearing_pressure_kpa`, `feed_rate_t_hr`, `water_addition_m3_hr`, `speed_pct_critical`, `ball_charge_proxy` | GENERATED BY `process_node` (mill unit operation); USED IN `shift_mass_balance` (throughput integration) | ISA-95 Level 2; AMIRA P754 Principle 2 |
| `flotation_cell_telemetry` | Time-Series | Continuous operating data per flotation cell bank: air flow rate (m³/min/cell), froth depth (mm), impeller speed (RPM), cell level (mm from overflow lip), and motor current (A). Logged at 1-minute intervals. Used for flotation circuit optimisation and performance monitoring. | One row per minute per flotation bank | `node_id`, `timestamp_utc`, `air_rate_m3_min_per_cell`, `froth_depth_mm`, `impeller_rpm`, `cell_level_mm`, `motor_current_a` | GENERATED BY `process_node` (flotation cell bank) | ISA-95 Level 2; AMIRA P754 Principles 1, 2 |
| `osa_grade_telemetry` | Time-Series | On-stream XRF analyzer grade measurements per process stream at 2–4 minute scan intervals. Provides near-real-time grade data for flotation process control. Secondary to laboratory assay for accounting — used for trend monitoring and control. | One row per stream per scan interval | `analyzer_id`, `stream_id`, `timestamp_utc`, `grade_cu_pct`, `grade_zn_pct`, `grade_pb_pct`, `grade_fe_pct`, `scan_validity_flag` | GENERATED BY on-stream XRF analyzer; ASSOCIATED WITH `process_node` (stream sampled) | ISA-95 Level 2; AMIRA P754 Principles 6, 7 |
| `process_measurement_telemetry` | Time-Series | Continuous readings from process instrumentation at P754-designated measurement points: belt weigher mass rates (t/hr), magnetic flowmeter volumetric rates (m³/hr), nuclear density gauge readings (t/m³), and inline pH sensor readings. The primary data source for mass balance integration. | One row per minute per instrument | `mp_id`, `instrument_id`, `timestamp_utc`, `measurement_value`, `measurement_units`, `instrument_status_flag` | GENERATED BY instrument at `amira_measurement_point`; USED IN `shift_mass_balance` | ISA-95 Level 1; AMIRA P754 Principles 1, 2, 7 |

---

## Interaction & Data Flow Map

### 3.1 Comminution

| Interaction Type | Description |
|-----------------|-------------|
| **Upstream data dependencies** | Mine Operations (Pillar 2) — ROM ore tonnes delivered (haul cycle records from FMS); mine plan (Pillar 1) — mill feed grade and throughput targets (blend plan); stockpile grade tracking (Pillar 2, 2.2.4.2) — expected mill feed head grade by material zone |
| **Downstream data consumers** | Flotation (3.2) — cyclone overflow (physical feed + P80 data); Metallurgical Accounting (3.4) — crusher feed belt weigher data (opening mass balance measurement), mill throughput telemetry |
| **Cross-domain interactions** | Maintenance (out of scope) — crusher and mill availability drives throughput capacity; Energy (out of scope) — mill power draw is the primary energy consumption variable in the plant |
| **System integration points** | FMS (Pillar 2) → DCS (crusher tip event from truck GPS); DCS → PI Historian (all mill telemetry); belt weighers → PI Historian; online PSA → DCS (P80 feedback to mill control); DCS → metallurgical accounting system (throughput data) |

### 3.2 Concentration (Flotation)

| Interaction Type | Description |
|-----------------|-------------|
| **Upstream data dependencies** | Comminution (3.1) — cyclone overflow at P80 target (feed quality); reagent inventory (3.2.1.1 — ERP); mine plan (Pillar 1) — head grade forecast for reagent plan |
| **Downstream data consumers** | Dewatering (3.3) — concentrate slurry streams and combined tailings; Metallurgical Accounting (3.4) — OSA grade data and shift composite samples for mass balance; Logistics (Pillar 4) — concentrate grade forecast for shipping schedule |
| **Cross-domain interactions** | Laboratory (LIMS) — shift composite samples submitted for assay; Maintenance (out of scope) — cell availability, OSA analyzer uptime; Environmental — tailings characterisation for TSF management |
| **System integration points** | DCS → PI Historian (flotation cell telemetry, reagent dosing rates, pH); on-stream XRF → PI Historian (OSA grade data); auto-samplers → LIMS (sample registration); metallurgist workstation → DCS (reagent setpoint changes) |

### 3.3 Dewatering & Product Handling

| Interaction Type | Description |
|-----------------|-------------|
| **Upstream data dependencies** | Flotation (3.2) — concentrate slurry streams and tailings; reagent supply (flocculant); compressed air supply |
| **Downstream data consumers** | Logistics & Outbound (Pillar 4) — filter cake physical delivery to concentrate shed; Metallurgical Accounting (3.4) — filter cake mass (wet tonnes), moisture % results; Environmental — TSF volume, water quality |
| **Cross-domain interactions** | Environmental (out of scope) — TSF freeboard, embankment stability, seepage monitoring; Water Management (out of scope) — reclaim water quality and volume |
| **System integration points** | DCS → PI Historian (thickener and filter telemetry); LIMS → metallurgical accounting system (moisture results); DCS/SCADA (tailings pump station) → PI Historian; TSF monitoring system → geotechnical database |

### 3.4 Metallurgical Accounting & Quality

| Interaction Type | Description |
|-----------------|-------------|
| **Upstream data dependencies** | All process areas (3.1–3.3) — all P754 measurement point data from PI Historian; LIMS — all assay results; Logistics (Pillar 4) — outbound weighbridge weights and CoA (third-party) for reconciliation against plant production |
| **Downstream data consumers** | Corporate Finance — monthly metal production for revenue recognition; Mine Planning (Pillar 1) — mill-to-mine reconciliation data for resource model calibration; Logistics (Pillar 4) — certified concentrate grade (CoA) and dry tonnes for commercial invoice; Audit Committee — P754-compliant accounting documentation |
| **Cross-domain interactions** | External laboratory (third-party umpire) — independent assay for commercial concentrate certification; Regulatory (out of scope as domain) — reporting of contained metal in production returns |
| **System integration points** | PI Historian → metallurgical accounting software (mass flow data); LIMS → metallurgical accounting software (assay data); metallurgical accounting software → ERP (production postings); ERP → finance (revenue recognition) |

---

## Process Flow Narratives (BPMN-Ready)

### 3.1 Comminution — Process Flow Narrative

**Pool**: Comminution | **Lanes**: Mine Interface / FMS, DCS / Auto-control, Control Room Operator, Metallurgist

**Start Event**: ROM ore available at crusher pocket (haul truck tip event or ROM stockpile reclaim active); plant in Run state.

1. **Receive ROM Ore at Crusher** (DCS + FMS interface) — tip event recorded; apron feeder belt weigher starts logging mass rate to PI Historian. **P754 MP-01 active — opening mass measurement**.
2. **Execute Primary Crushing** (DCS Auto-control) — crusher CSS maintained at setpoint; power draw and vibration monitored; tramp metal detection active.
3. **Classify Crusher Product at Discharge Conveyor** (DCS) — belt weigher on discharge conveyor logs secondary mass measurement (cross-check against MP-01). Product conveyed to COS.
   - *[COPPER NOTE: SABC circuit — proceed directly to SAG mill feed bin (3.1.3). ZINC NOTE: Red Dog — proceed to secondary/tertiary crushing circuit (3.1.2).]*
4. **Manage COS Level** (DCS Auto-control / Control Room Operator) — COS level sensor monitored; reclaim feeders controlled to maintain target SAG mill feed rate.
   - *[GATEWAY — COS level below minimum?]* → Yes: reduce SAG mill feed rate (DCS auto-throttle); alert to control room. No: continue.
5. **[CONDITIONAL — Secondary/Tertiary Crushing — Red Dog only]** — ore passes through secondary cone crusher → vibrating screen → tertiary cone crusher → screen undersize forward to ball mill feed.
6. **Operate SAG Mill** (DCS Auto-control) — mill speed, bearing pressure, water addition, and feed rate controlled by DCS; power draw optimised; MWD load estimate applied.
   - *[GATEWAY — SAG discharge screen generating excess pebbles?]* → Yes: pebble crusher activated (3.1.2.3 — Cu sites only). No: undersize direct to ball mill.
7. **Operate Ball Mill** (DCS Auto-control) — sump level controlled; cyclone feed pump speed varied to maintain sump.
8. **Classify via Hydrocyclone** (DCS Auto-control) — cyclone feed density and flow monitored; overflow reports to flotation feed sump; underflow recirculates.
   - *[GATEWAY — Cyclone overflow P80 off-target?]* → Yes: metallurgist adjusts cyclone apex, feed density, or mill throughput. No: continue.
9. **Add Grinding Media** (Plant Operator — scheduled) — balls added to SAG and/or ball mill per ball addition schedule.

**End Event**: Cyclone overflow at target P80 reporting continuously to flotation feed; all telemetry and mass measurement data streaming to PI Historian.

---

### 3.2 Concentration (Flotation) — Process Flow Narrative

**Pool**: Flotation | **Lanes**: DCS/Auto-control, Control Room Operator, Metallurgist, On-Stream Analyzer, Sampler

**Start Event**: Cyclone overflow feeding flotation feed sump; cells running; reagents dosed; target pH established.

**[NOTE — The following describes the full RSC Cu circuit as the primary narrative. Zn and Pb circuit flows are parallel pools operating after Cu tailings, flagged with commodity markers.]**

1. **Condition Feed at Target pH** (DCS + Metallurgist) — lime dosing pump controls pH to setpoint; pH telemetry logged continuously. OSA monitoring of feed grade begins.
2. **Dose Reagents to Rougher** (DCS Auto-control) — collector and frother dosing pumps active at setpoint rates; consumption logged at 1-min intervals.
3. **Operate Cu Rougher Bank** (DCS Auto-control + Metallurgist oversight) — air rate, froth depth, impeller speed per cell at setpoints; froth scrapers active; OSA scans Cu rougher concentrate and tail every 2–4 min.
4. **Auto-sample Rougher Concentrate and Rougher Tail** (Auto-sampler) — increments collected at 15–60 min interval; accumulated in shift composite cutter.
   - *[GATEWAY — OSA rougher tail Cu% above threshold?]* → Yes: metallurgist increases collector dosage or reduces air rate at scavenger; logs process change. No: continue.
5. **Operate Cu Scavenger Bank** (DCS Auto-control) — additional collector dosed at scavenger head; tail grade monitored by OSA.
   - *[GATEWAY — Cu scavenger tail Cu% above rejection limit?]* → Yes: metallurgist investigation (plant feed grade shift, reagent failure, OSA calibration); escalate. No: continue.
6. **Operate Cu Regrind Mill (if present)** (DCS Auto-control) — rougher/scavenger concentrate reground to target P80 before cleaning.
7. **Operate Cu Cleaner Bank(s)** (DCS Auto-control + Metallurgist) — depressant dosed; froth depth set for grade optimisation; OSA monitors final concentrate grade continuously.
   - *[GATEWAY — Cu final concentrate grade below smelter spec?]* → Yes: metallurgist increases cleaning stages or adjusts froth depth; logs change. No: continue.
8. **Collect Shift Composite Sample — Cu Final Concentrate** (Auto-sampler) — increments accumulated throughout shift; composite submitted to LIMS at shift end. **P754 MP-05 — primary grade measurement for accounting**.

**[PARALLEL — Zn Circuit (Antamina and Red Dog)]**

9. **Activate Sphalerite with CuSO₄** (DCS + Metallurgist) — Cu scavenger tailings conditioned with CuSO₄; dosing rate logged.
10. **Operate Zn Rougher → Scavenger → Cleaner** — mirrors Cu circuit RSC flow; OSA monitoring at rougher concentrate and scavenger tailings; shift composite collected at Zn final concentrate. **P754 MP-11 — primary Zn grade measurement**.

**[PARALLEL — Pb Circuit (Antamina and Red Dog, where applicable)]**

11. **Operate Pb Rougher → Cleaner** — shift composite at Pb final concentrate. **P754 MP-15 — primary Pb grade measurement**.

**End Event**: Shift end — all shift composite samples dispatched to LIMS; all OSA data archived to PI Historian; final concentrate slurries flowing to respective thickeners.

---

### 3.3 Dewatering & Product Handling — Process Flow Narrative

**Pool**: Dewatering & Product Handling | **Lanes**: DCS/Auto-control, Control Room Operator, Process Technician, Environmental Officer

**[PARALLEL — Separate dewatering trains per commodity; tailings runs concurrently]**

**Concentrate Dewatering Stream (repeated per commodity):**

**Start Event**: Flotation cleaner concentrate flowing to thickener feed pump.

1. **Feed Concentrate to Thickener** (DCS) — feed flowmeter and densitometer log mass rate (t/hr) continuously. **P754 MP measurement active**.
2. **Dose Flocculant** (DCS Auto-control) — polymer flocculant dosing pump at setpoint; consumption logged.
3. **Monitor Thickener Performance** (DCS + Control Room Operator) — underflow density setpoint; overflow clarity check.
   - *[GATEWAY — Underflow density below minimum?]* → Yes: reduce feed rate or increase flocculant; log response. No: continue.
4. **Pump Underflow to Filter Feed Tank** (DCS) — underflow pump speed controlled by level; density and flow logged.
5. **Operate Filter** (DCS Auto-control) — cycle sequence automated (feed, press, blow, discharge for pressure filters; or continuous rotation for disc filters); cycle parameters logged.
6. **Discharge Filter Cake** (Plant Operator + DCS) — cake discharged to conveyor; belt weigher logs wet tonnes per batch. **P754 MP — primary wet tonnes measurement**.
7. **Collect Moisture Sample** (Process Technician) — grab sample taken from conveyor at defined frequency; weighed wet, submitted to lab for oven dry (105°C); moisture % entered in LIMS.
   - *[GATEWAY — Moisture % exceeds specification?]* → Yes: metallurgist adjusts filter cycle time, wash water, or compressed air; investigate thickener underflow density. No: filter cake accepted.
8. **Transfer Filter Cake to Concentrate Shed** (Conveyor / FEL) — physical product moved to storage; production record created in metallurgical accounting system.

**Tailings Management Stream (continuous):**

1. **Thicken Tailings** (DCS Auto-control) — flocculant dosed; underflow density monitored; overflow returned to process water.
2. **Pump Tailings to TSF** (DCS/SCADA) — pump station operating; pipeline pressure and flow logged continuously; any pressure drop triggers alarm (potential pipeline failure).
3. **Monitor TSF** (Environmental Officer + Monitoring System) — freeboard, pond level, seepage, embankment monitoring continuous.
   - *[GATEWAY — TSF freeboard below minimum?]* → Yes: reduce tailings input rate; emergency water management response; notify environmental team. No: continue.
4. **Recover Process Water from TSF** (DCS/SCADA) — reclaim pump operates to return decant to process water circuit; flow logged.

**End Event**: Filter cake accumulating in concentrate shed (physical); tailings continuing to TSF; all telemetry archived to PI Historian.

---

### 3.4 Metallurgical Accounting & Quality — Process Flow Narrative

**Pool**: Metallurgical Accounting | **Lanes**: Auto-samplers / Instruments, Laboratory, Metallurgist, Chief Metallurgist, Systems

**Start Event**: Shift start — all auto-samplers active; PI Historian recording all P754 measurement points.

**[CONTINUOUS DURING SHIFT]**

1. **Collect Auto-Sampler Increments** (Auto-samplers) — increments collected at 15–60 min intervals across all designated streams; accumulated in shift composite cutters.
2. **Monitor OSA Data** (Metallurgist) — real-time grade trends reviewed; process adjustments made; OSA data archived to PI Historian continuously.
3. **Collect Grab/Composite Samples** (Process Technician) — as per shift sampling plan; submitted to LIMS.

**[AT SHIFT END]**

4. **Submit Shift Composite Samples to LIMS** (Process Technician) — shift composite samples registered in LIMS with source stream, collection interval, shift ID, and chain-of-custody record.
5. **Prepare Samples in Laboratory** (Lab Technician) — drying, pulverising, splitting; QC inserts (CRM, duplicate, blank) at defined rates.
6. **Analyse Samples** (Lab Analyst) — ICP/XRF analysis per assay method; results entered in LIMS.
7. **Review QA/QC** (Lab Analyst + Chief Metallurgist) — CRM recovery, duplicate RPD, blank contamination reviewed.
   - *[GATEWAY — QC batch accepted?]* → Yes: results released in LIMS. No: re-assay instruction issued; affected results flagged; batch held.
8. **Close Shift Mass Balance** (Metallurgist) — fetch mass flow data from PI Historian; fetch assay results from LIMS; calculate shift balance.
   - *[GATEWAY — Balance error within tolerance?]* → Yes: shift balance accepted and filed. No: investigation initiated (check instrument data, sample integrity, stockpile changes); escalate to Chief Metallurgist.
9. **Produce Daily Reconciliation** (Metallurgist) — aggregate shift balances; cross-check against independent measurements; report issued.

**[MONTHLY]**

10. **Close Monthly Metal Accounting Period** (Chief Metallurgist) — aggregate daily reconciliations; apply certification assay results; reconcile with outbound weighbridge and commercial CoA; produce formal monthly report; submit to Finance and Audit Committee.
11. **Conduct Stocktake** (Chief Metallurgist + Survey Team) — physical measurement of all in-process inventory; variance to book inventory calculated; adjustment entries made.

**End Event**: Monthly metal accounting report filed; P754-compliant documentation archived; Finance receives production figures for revenue recognition.

---

## Commodity Variations

| Process Area | Variation Type | Copper — Single Metal (QB, HVC, CdA) | Copper-Zinc Polymetallic (Antamina) | Zinc-Lead Differential (Red Dog) | Data Implication |
|--------------|---------------|--------------------------------------|--------------------------------------|----------------------------------|-----------------|
| **3.1.2 Crushing** | Circuit configuration | SABC circuit — no secondary/tertiary crushing stage; pebble crusher active in SAG circuit | SABC circuit — same as Cu-single | Three-stage crushing (primary jaw, secondary cone, tertiary cone) before ball mill; no SAG mill | `process_node` master must include node_type = "secondary_cone_crusher" for Red Dog; SAG mill node absent at Red Dog |
| **3.1.3 Grinding** | Mill type | SAG + ball mill (SABC); SAG is primary power consumer | SAG + ball mill | Ball mill only (three-stage crushing circuit eliminates SAG); grinding media consumption patterns differ | Mill telemetry entity must accommodate absence of SAG mill at Red Dog; `process_node` configuration is site-specific |
| **3.2.2 Cu Circuit** | Circuit scope | Full Cu RSC circuit; Mo by-product circuit possible at QB and HVC (separate Mo flotation after Cu cleaning) | Cu RSC circuit first; Cu tailings become Zn circuit feed | Not applicable — no Cu ore | Mo by-product recovery at QB/HVC requires additional `concentrate_production_record` entity for Mo concentrate |
| **3.2.3 Zn Circuit** | Circuit position and activation | Not applicable (Cu-only sites) | Sequential after Cu — Cu scavenger tailings feed Zn conditioning; sphalerite activation with CuSO₄ required | PRIMARY circuit — Zn rougher follows differential Pb flotation; different activation regime | At Red Dog, `process_node` sequence is: Pb rougher → Pb cleaner → Zn activation → Zn rougher → Zn cleaner; at Antamina, Pb comes last |
| **3.2.4 Pb Circuit** | Circuit position | Not applicable | Pb recovery from Zn scavenger tailings — Pb circuit is third in sequence | Pb floated FIRST (differential flotation at natural pH ~7–8 depresses sphalerite); Pb circuit precedes Zn circuit | Circuit sequence ordering in `process_node` master must reflect site-specific flow topology; Red Dog and Antamina have opposite Pb/Zn sequencing |
| **3.3.2 Filtration** | Product moisture spec | Cu concentrate: target moisture 8–12% (smelter contract dependent) | Cu: 8–12%; Zn: 8–10%; Pb: 8–10% | Zn: 8–9%; Pb: 8–10%; Arctic storage: moisture is critical — high moisture in Arctic storage can cause freezing and handling issues | `concentrate_type` reference entity must carry commodity-specific moisture specification; moisture QC gate must compare against the commodity-specific spec |
| **3.4 Metal Accounting** | Metals in scope | Cu (primary), Mo (by-product at QB/HVC), Ag (minor by-product) | Cu, Zn, Pb, Ag, Au | Zn (primary), Pb (major by-product), Ag, Cd (in Zn concentrate — subject to penalties) | `shift_mass_balance` entity must carry grade fields for all metals in scope at each site; Cd in Zn concentrate at Red Dog requires penalty element tracking |

---

## Standard Alignment Summary

| L2 Process Area | ISA-95 | AMIRA P754 | GMG TUM | BPMN 2.0 |
|----------------|--------|-----------|---------|---------|
| **3.1 Comminution** | Levels 0–3 | Principles 1, 2, 5, 7 (mass measurement at crusher feed and COS; cross-check at discharge conveyor) | Not primary (mine services equipment only at periphery) | Complete |
| **3.2 Concentration (Flotation)** | Levels 0–3 | Principles 1, 2, 5, 6, 7, 8, 10 (grade measurement — OSA and lab; custody transfer at final concentrate streams) | Not primary | Complete |
| **3.3 Dewatering & Product Handling** | Levels 0–3 | Principles 1, 5, 7, 8 (mass at thickener feed; moisture verification; filter cake dry tonnes — commercial custody) | Not primary | Complete |
| **3.4 Metallurgical Accounting & Quality** | Levels 2–4 | **ALL 10 Principles** (this process area IS the P754 implementation) | Not primary | Complete |

---

## Completeness Verification

### Quality Test Checklist

| Test | 3.1 Comminution | 3.2 Flotation | 3.3 Dewatering | 3.4 Met Accounting |
|------|----------------|---------------|---------------|-------------------|
| BEAM facilitator could run 2-day workshop? | Pass | Pass | Pass | Pass |
| Entity business definitions understandable to plant metallurgist? | Pass | Pass | Pass | Pass |
| All custody transfer points identified? | Pass (COS = internal mine-to-mill) | Pass (cleaner final concentrate per commodity) | Pass (filter cake to concentrate shed; TSF boundary) | Pass (monthly concentrate certification) |
| All ISA-95 levels represented? | Pass (L0–L3) | Pass (L0–L3) | Pass (L0–L3) | Pass (L2–L4) |
| BPMN modeler could convert narrative without clarification? | Pass | Pass | Pass | Pass |
| AMIRA P754 annotation on every measurement node? | Pass | Pass | Pass | Pass (synthesis) |
| Mass balance node maps produced per flotation circuit? | — | Pass (Cu, Zn, Pb circuits) | — | — |
| Commodity variations — structural divergence explicitly flagged? | Pass | Pass | Pass | Pass |

### Known Gaps and Forward Dependencies

| # | Gap | Resolution Path |
|---|-----|----------------|
| G1 | Molybdenum by-product circuit (QB and HVC) — not decomposed to L4 as Mo recovery is conditional and structurally minor. It mirrors the Cu cleaner RSC pattern. | Add Mo circuit decomposition as a conditional branch in a future revision once QB/HVC site data is available to confirm circuit configuration |
| G2 | On-stream XRF analyser availability (downtime) — OSA data is used for process control but lab assay is primary for P754 accounting. The data product must handle OSA data gaps gracefully (null vs. estimated) — this is a data quality rule for the Raw → Curated transition, not a process model gap | Flag for data product contract: OSA grade telemetry must carry data_quality_flag attribute |
| G3 | Metallurgical accounting software system (vendor and data model) is not specified. This is the primary integration dependency for the curated `shift_mass_balance` and `metallurgical_accounting_report` entities — they must be modelled in the curated layer to be independent of the accounting software's proprietary schema | BEAM workshop Pillar 3 session must include the metallurgical accountant as a key stakeholder to identify the source system |
| G4 | TSF geotechnical monitoring is referenced but not decomposed to L4 — it is on the boundary of the out-of-scope Environmental domain. Slope monitoring data generated at the TSF boundary is structurally similar to pit wall monitoring in Pillar 2 (Mine Services). | Confirm scope with programme team; if TSF monitoring is in scope, it should be added as a sub-process under 3.3.3 |
| G5 | Red Dog Arctic logistics creates unique inventory dynamics — concentrate must be stockpiled for months before the shipping season opens. The inventory management implications for metallurgical accounting (long inventory hold periods, moisture change during storage, sampling of aged concentrate) are not fully addressed in this process model. | Address in cross-reference file (00) and Pillar 4 where the Red Dog logistics distinction is primary |

---

*End of Pillar 3: Processing & Beneficiation. Produced per Open-Pit Mining Value Chain Process Model Development Specification v1.0.*


---

## Pillar 3 — Processing & Beneficiation: Cross-Pillar Dependencies (Pillars 5 & 6)

### Pillar 5 (Maintenance & Reliability) Dependencies

| Pillar 3 Entity / Activity | Dependency Direction | Pillar 5 Entity / Activity | Integration Point |
|---|---|---|---|
| `process_node` (SAG mill, ball mill, flotation cells, thickeners, filters) | Shared across Pillars 3 and 5 | `work_order`, `equipment_failure_record`, `equipment_criticality_record` | Processing plant fixed equipment (mills, cells, conveyors) must be registered in SAP PM as functional locations and equipment masters, the same as mobile equipment. Currently, many mining operations have a gap: mobile equipment is well-tracked in EAM, but processing plant equipment maintenance is managed informally or in a separate CMMS. The curated `process_node` entity in Pillar 3 and the equipment master in Pillar 5 EAM must be reconciled to a single record per physical asset. |
| 3.1.3.1 Operate SAG Mill | Pillar 3 generates Pillar 5 condition data | `condition_monitoring_telemetry` (SAG mill bearing temperature, vibration, power draw trending) | SAG mill bearing temperature (PI Historian — continuous) and vibration (if permanently instrumented) are condition monitoring inputs for predictive bearing replacement. Power draw trending over time (declining power at same throughput = ball charge depletion or liner wear) drives maintenance work orders for liner inspection/replacement and ball top-up. Pillar 5 condition monitoring must be configured to watch Pillar 3 PI Historian tags for mill health indicators. |
| 3.3.2.3 Verify Moisture Content | Pillar 3 generates AMIRA P754 record; Pillar 5 maintains the instrument | Weighbridge / LIMS instrument calibration (Pillar 5 scope) | Moisture measurement instruments (oven balances, infrared moisture analysers), LIMS equipment, and belt weighers used in Pillar 3 mass balance are measurement instruments requiring periodic calibration. Instrument calibration is a Pillar 5 maintenance task (statutory inspection category). Calibration certificates must be linked to AMIRA P754 Principle 8 (measurement accuracy targets) — the weighbridge and analytical instrument calibration records are P754 documentation requirements. |
| 3.4.3.1 Close Shift Mass Balance | AMIRA P754 — Pillar 5 instrument calibration governs data quality | `work_order` (statutory inspection — weighbridge calibration); calibration certificate records | The shift mass balance (P754 compliance document) is only as reliable as the measurement instruments that feed it. Belt weighers, density gauges, flowmeters, and analytical instruments must all have current calibration certificates. Instrument calibration work orders in Pillar 5 must reference the P754 measurement point ID (from the `amira_measurement_point` entity in Pillar 3) — this enables the metallurgical accountant to confirm that all measurement points were within calibration at the time of each mass balance closure. |

### Pillar 6 (Health & Safety) Dependencies

| Pillar 3 Entity / Activity | Dependency Direction | Pillar 6 Entity / Activity | Integration Point |
|---|---|---|---|
| 3.2.1.1 Manage Reagent Inventory and Preparation | Pillar 6 governs | `risk_register_record` (chemical hazards: xanthate, NaCN, lime, CuSO4); `exposure_monitoring_record` (airborne NaCN, lime dust) | Flotation reagents include potentially hazardous chemicals: sodium cyanide (NaCN — acute toxic, asphyxiation risk if reacts with acid), lime dust (respiratory hazard), MIBC frother (flammable), xanthates (flammable, spontaneous ignition risk). The Pillar 6 risk register must cover reagent handling. Exposure monitoring (6.4) must cover airborne NaCN and lime dust. Any reagent spill is an environmental and safety incident (Pillar 6) and a potential AMIRA P754 mass balance perturbation (Pillar 3). |
| 3.3.3.3 Deposit Tailings at TSF | Pillar 6 governs (TSF failure is a catastrophic safety event) | `risk_register_record` (TSF failure — dam breach); `incident_record` (if embankment anomaly detected) | TSF embankment failure is classified as a top-tier fatal hazard (ICMM Fatal Hazard Control). The TSF geotechnical monitoring data (freeboard, embankment deformation, seepage — from Pillar 3 SCADA and geotechnical instruments) must feed the Pillar 6 risk register review process. Anomalous TSF readings are potential near-miss events requiring Pillar 6 incident classification and response. |
| Processing plant confined space entry (thickeners, flotation cells, sumps) | Pillar 6 gates | `permit_to_work` (Confined Space Entry — mandatory for any entry into enclosed space with atmospheric hazard) | Every entry into a thickener, flotation cell, agitated tank, or sump is a confined space entry requiring a Pillar 6 PTW with atmospheric testing (oxygen content, toxic gas, flammable gas) before entry. These are the most safety-critical PTWs in the processing plant. |
| `osa_grade_telemetry` (on-stream XRF analyzer) | Pillar 6 indirect dependency | `exposure_monitoring_record` (X-ray radiation — maintenance of XRF analyzers) | On-stream XRF analyzers contain sealed radioactive sources. Maintenance of XRF analyzers requires radiation work permits (a specialist PTW type) and radiation monitoring for maintenance workers. Pillar 5 maintenance work orders for XRF analyzer maintenance must trigger Pillar 6 radiation work permits. |

---