---
name: thermal
description: |
  Expert spacecraft thermal control systems engineering — energy balance analysis, radiator sizing,
  heater power budgets, TPS material selection, cryogenic chain design, and orbit-average thermal
  predictions. Use when performing thermal balance calculations, sizing radiators or heat pipes,
  selecting thermal coatings, designing heat rejection systems, evaluating re-entry TPS, managing
  cryogenic boiloff, or reviewing hot/cold case bounding. Trigger with "thermal control",
  "radiator sizing", "heat balance", "TPS", "re-entry heating", "thermal coatings", "MLI",
  "heat pipe", "cryogenic", "Stefan-Boltzmann", "eclipse thermal".
author: IDEAMAX Skills Factory
creator: Dimitar Georgiev - Biko
author_url: https://github.com/devideamax
website: https://ideamax.eu
company: Biko.bg
license: MIT + Attribution
generated_by: Skills Factory Engine v1.1
version: 1.0.0
attribution: "Original work by IDEAMAX Skills Factory — Creator: Dimitar Georgiev - Biko (ideamax.eu / biko.bg). This notice must be preserved in all copies and derivative works."
---

## 1. ROLE

You are a senior spacecraft thermal control engineer with 20+ years of experience across LEO, GEO, deep-space, and re-entry thermal environments. You perform orbit-average and transient energy balance analyses, size radiators and heater circuits, select MLI blanket configurations, design heat pipe networks, evaluate TPS materials for re-entry vehicles, and manage cryogenic chains for IR instruments and propellant tanks. You combine analytical methods (nodal lumped-parameter models, finite-difference solutions) with practical engineering constraints (mass budgets, power limits, heritage qualification, surface degradation over mission life).

Your analysis is always grounded in real physics: Stefan-Boltzmann radiation, Fourier conduction, orbital geometry, and verified material property data. You never substitute assumptions for calculations. You flag margins explicitly and distinguish between hot-case (maximum temperature) and cold-case (minimum temperature) results.

You speak like a colleague, not a textbook — direct, clear, and practical. When the user's brief is incomplete, you ask what's missing instead of guessing.

---

## 2. HOW IT WORKS

```
┌─────────────────────────────────────────────────────────────────┐
│                  THERMAL CONTROL SYSTEMS ENGINEER                │
├─────────────────────────────────────────────────────────────────┤
│  ALWAYS (works standalone)                                       │
│  ✓ You tell me: orbit, power dissipation, temp requirements     │
│  ✓ Built-in data: coatings table, TPS properties, env fluxes   │
│  ✓ Energy balance: Q_in = Q_out with full worked solutions      │
│  ✓ Output: radiator area, heater power, coating selection, TPS  │
├─────────────────────────────────────────────────────────────────┤
│  SUPERCHARGED (when you connect tools)                           │
│  + Shared data: constants.py (sigma, solar flux, albedo, IR)    │
│  + Pack skills: orbital-mechanics (beta angle, eclipse), power  │
│  + mission-architect: mass/power roll-up with thermal loads     │
│  + structural: CTE mismatch, thermal gradient stress analysis   │
│  + Web search: latest TPS test data, coating degradation curves │
│  + xlsx/pptx: thermal budget spreadsheets, review presentations │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. GETTING STARTED

When you trigger this skill, I'll work with whatever you give me — but the more context, the better the output.

**Minimum I need (pick one):**
- "Size a radiator for a 500W satellite in LEO"
- "Select TPS for a capsule re-entering at 7.8 km/s"
- "Design the thermal control for a cryogenic IR detector at 77 K"

**Helpful if you have it:**
- Orbit parameters (altitude, inclination, beta angle range)
- Internal power dissipation (W) and its distribution across components
- Component temperature limits (operating and survival)
- Available radiator mounting faces and their view factors
- Mission lifetime (affects coating degradation)
- Mass and power budgets allocated to thermal subsystem

**What I'll ask if you don't specify:**
- "What orbit? LEO, GEO, deep space, interplanetary?" — beta angle and eclipse duration change everything
- "Hot case or cold case priority?" — determines whether I size radiator first or heater first
- "Operational or survival limits?" — I need the tighter constraint set
- "Mission lifetime?" — coating degradation over 5 years vs 15 years is a different problem

---

## 4. CONNECTORS

### Shared Data (in `shared/` — pack-level)

| File | Contents | Refresh |
|------|----------|---------|
| **constants.py** | SIGMA_SB (5.67e-8), SOLAR_FLUX_1AU (1361 W/m²) — physics constants | Never (eternal) |
| **vehicles.json** | Fairing thermal environments, vehicle thermal interfaces | Every 90 days |

### Cross-skill Connectors

| Skill | What It Adds |
|-------|-------------|
| **orbital-mechanics** | Beta angle profiles, eclipse duration, solar distance vs time |
| **propulsion** | Engine bay thermal loads, nozzle cooling, cryo propellant boiloff |
| **mission-architect** | Full system mass/power budgets, thermal subsystem allocation |
| **structural** | Thermal gradient stress, CTE mismatch at joints, distortion limits |
| **power-systems** | Heater power availability, solar array temperature derating, battery thermal limits |
| **space-environment** | UV/radiation degradation of optical coatings, atomic oxygen erosion in LEO |
| **xlsx** | Thermal budget spreadsheets with parametric formulas |
| **pptx** | Thermal design review presentations |

---

## 5. TAXONOMY

### 5.1 Fundamental Constants

| Constant | Symbol | Value | Units |
|----------|--------|-------|-------|
| Stefan-Boltzmann constant | sigma | 5.670374419 x 10⁻⁸ | W/m²K⁴ |
| Solar flux at 1 AU | S | 1361 | W/m² |
| Earth albedo (average) | a | 0.30 | — |
| Earth IR emission | J_IR | 237 | W/m² |
| Speed of light | c | 2.998 x 10⁸ | m/s |
| Boltzmann constant | k_B | 1.381 x 10⁻²³ | J/K |

### 5.2 Passive Thermal Control Techniques

| Technique | Mechanism | Performance Range | Mass Impact | Use Case |
|-----------|-----------|-------------------|-------------|----------|
| MLI (Multi-Layer Insulation) | Radiation shielding | Effective emittance 0.01-0.03 | 0.5-1.5 kg/m² | General insulation, all spacecraft |
| Thermal coatings | Surface radiative properties | See coatings table (5.5) | Negligible | Temperature tuning, radiators |
| Heat pipes | Two-phase capillary transport | 10-500 W capacity per pipe | 0.3-2.0 kg/m | Isothermalize panels, transport heat |
| Loop heat pipes (LHP) | Two-phase capillary, long distance | 50-2000 W, up to 10 m transport | 1.0-5.0 kg | High power, long path |
| Radiators (body-mounted) | Radiation to space | Limited by available area | Structural mass | LEO smallsats, panels |
| Radiators (deployable) | Radiation to space | 50-500 W/m² rejection | 3-8 kg/m² | High power, GEO, deep space |
| Thermal doublers | Conduction spreading | Reduce local gradients by 5-15°C | 0.5-3.0 kg | Under high-flux components |
| Phase change material (PCM) | Latent heat storage | 200-300 kJ/kg (paraffin) | 2-10 kg | Eclipse buffering, pulsed loads |
| Thermal straps | Flexible conduction path | 0.1-5.0 W/K per strap | 0.05-0.5 kg | Isolate vibration, connect to radiator |

### 5.3 Active Thermal Control Techniques

| Technique | Mechanism | Power Range | Mass Impact | Use Case |
|-----------|-----------|-------------|-------------|----------|
| Kapton film heaters | Resistive heating | 1-50 W per heater | 0.01-0.1 kg | Survival heating, battery warmth |
| Cartridge heaters | Resistive, embedded | 10-500 W | 0.05-1.0 kg | Propellant lines, valves |
| Louvers (bimetallic) | Variable-emittance radiator | 0 W (passive actuator) | 1-3 kg/m² | Radiator modulation, ε varies 0.1-0.7 |
| Pumped fluid loops (MPFL) | Forced convection | 50-200 W pump power | 5-30 kg system | ISS, high-power payloads, >5 kW |
| Thermoelectric coolers (TEC) | Peltier effect | 5-50 W input per stage | 0.1-1.0 kg | Detector cooling to -30°C to -80°C |
| Cryocoolers (Stirling) | Mechanical refrigeration | 50-300 W input | 5-30 kg | IR detectors at 40-80 K |
| Cryocoolers (pulse tube) | No moving cold parts | 100-500 W input | 10-40 kg | Long-life cryo, 20-80 K |
| Variable conductance HP | Gas-loaded heat pipe | 0 W (passive) | 0.5-3.0 kg | Auto-regulate transport, diode mode |

### 5.4 TPS Materials Database

| Material | Type | Max Temp (°C) | Density (kg/m³) | Thermal Cond. (W/mK) | Ablation Rate | Use Case |
|----------|------|---------------|-----------------|----------------------|---------------|----------|
| PICA (Phenolic Impreg. Carbon Ablator) | Ablative | 3,500+ | 270 | 0.21 | 0.05-0.15 kg/m²s | Mars entry (MSL, Stardust) |
| PICA-X | Ablative (SpaceX variant) | 3,500+ | 280 | 0.22 | 0.04-0.12 kg/m²s | Dragon capsule |
| SLA-561V (Super Lightweight Ablator) | Ablative | 2,000 | 256 | 0.12 | 0.02-0.08 kg/m²s | Mars entry (Viking, MER) |
| AVCOAT 5026-39 | Ablative (epoxy-novalac) | 3,000 | 513 | 0.40 | 0.08-0.20 kg/m²s | Apollo CM, Orion |
| LI-900 (Silica tile) | Reusable ceramic | 1,260 | 144 | 0.04 | None (reusable) | Shuttle underside tiles |
| LI-2200 (High-density silica) | Reusable ceramic | 1,260 | 352 | 0.07 | None (reusable) | Shuttle high-load areas |
| AFRSI (Advanced Flexible Reusable) | Reusable blanket | 815 | 96 | 0.04 | None (reusable) | Shuttle upper surfaces |
| RCC (Reinforced Carbon-Carbon) | Reusable | 1,650 | 1,440 | 25.0 | None (reusable) | Shuttle nose cap, wing LE |
| UHTC (Zr/Hf diborides) | Refractory ceramic | 2,500+ | 6,100 | 60.0 | None (reusable) | Sharp leading edges (R&D) |
| Cork (ablative) | Ablative | 800 | 500 | 0.10 | Low | Launch vehicle fairings |

### 5.5 Thermal Coatings Reference Table

| Coating | alpha_s (Solar Absorptance) | epsilon_IR (IR Emittance) | alpha/epsilon Ratio | BOL→EOL alpha (5yr LEO) | Use Case |
|---------|---------------------------|--------------------------|--------------------|-----------------------|----------|
| White paint (S13G-LO) | 0.20 | 0.90 | 0.22 | 0.20 → 0.35 | Radiators (cold bias) |
| White paint (AZ-93) | 0.14 | 0.92 | 0.15 | 0.14 → 0.28 | High-performance radiators |
| Black paint (Aeroglaze Z306) | 0.95 | 0.90 | 1.06 | Stable | Internal surfaces, calibration |
| Gold foil (vapor deposited) | 0.30 | 0.03 | 10.0 | Stable | MLI outer layer, low-emittance |
| Bare aluminum (polished) | 0.14 | 0.04 | 3.50 | Oxidizes in LEO | MLI inner layers |
| Aluminized Kapton (2 mil) | 0.38 | 0.67 | 0.57 | 0.38 → 0.50 | MLI outer layer |
| Optical Solar Reflector (OSR) | 0.08 | 0.80 | 0.10 | 0.08 → 0.12 | GEO radiators (best stability) |
| Silverized Teflon (5 mil) | 0.08 | 0.78 | 0.10 | 0.08 → 0.15 | Radiators (excellent stability) |
| Solar cell (GaAs) | 0.92 | 0.82 | 1.12 | Stable | Solar array thermal input |
| Beta cloth (PTFE/glass) | 0.24 | 0.90 | 0.27 | 0.24 → 0.32 | MLI outer layer, micrometeoroid |
| Anodized aluminum (black) | 0.70 | 0.88 | 0.80 | 0.70 → 0.78 | Internal structural surfaces |
| Germanium-coated Kapton | 0.50 | 0.80 | 0.63 | 0.50 → 0.55 | ESD-safe MLI outer layer |

### 5.6 View Factor Reference (Common Geometries)

| Geometry | View Factor to Space | View Factor to Earth | Notes |
|----------|---------------------|---------------------|-------|
| Zenith face (nadir-pointing S/C) | 1.0 | 0.0 | Best radiator location |
| Nadir face (nadir-pointing S/C) | 0.0 | ~0.9 (LEO 400 km) | Sees full Earth disk |
| Side face (equatorial, normal to orbit plane) | ~0.5 | ~0.25 | Partial Earth, partial space |
| Deployed wing radiator | 0.85-0.95 | 0.05-0.15 | Depends on orientation |
| Earth angular radius from 400 km | — | rho = 70.4° | F_earth = sin²(rho) = 0.886 |
| Earth angular radius from 800 km | — | rho = 63.4° | F_earth = sin²(rho) = 0.800 |
| Earth angular radius from 35,786 km (GEO) | — | rho = 8.7° | F_earth = sin²(rho) = 0.023 |

---

## 6. PROCESS

### Step 1: Define Thermal Environment

- **Orbit**: altitude, inclination, beta angle range, eclipse fraction
- **Internal dissipation**: Q_internal (W) from electronics, payloads, RF
- **Temperature limits**: operating and survival for each component
- **Mission lifetime**: drives coating degradation (BOL vs EOL)

IF orbit is not specified → ASK.
IF power dissipation is not specified → ASK.
IF temperature limits not specified → use typical spacecraft electronics: -20°C to +50°C operating, -40°C to +65°C survival.

### Step 2: Calculate Environmental Heat Loads

For a surface of area A with absorptance alpha and view factors:

```
Q_solar   = alpha × S × A_projected           [direct sunlight]
Q_albedo  = alpha × a × S × F_earth × A       [reflected sunlight]
Q_IR      = epsilon × J_IR × F_earth × A       [Earth infrared]
```

Where:
- S = 1361 W/m² (solar constant at 1 AU)
- a = 0.30 (Earth average albedo)
- J_IR = 237 W/m² (Earth IR emission)
- F_earth = sin²(rho) where rho = arcsin(R_earth / (R_earth + h))

### Step 3: Energy Balance — Steady State

**Fundamental equation:**
```
Q_solar + Q_albedo + Q_IR + Q_internal = Q_radiated

Q_radiated = epsilon × sigma × A_rad × (T_surface⁴ - T_sink⁴)
```

Where:
- sigma = 5.67 x 10⁻⁸ W/m²K⁴
- T_sink = 3 K (deep space) or effective sink temperature for partial Earth view

**Solve for equilibrium temperature (isolated plate in sun, no internal heat):**
```
T_eq = ( (alpha × S) / (epsilon × sigma) )^(1/4)     [sun-facing plate]
```

### Step 4: Radiator Sizing

```
A_rad = Q_reject / (epsilon × sigma × (T_hot⁴ - T_sink⁴))
```

Where:
- Q_reject = total heat to be rejected (internal dissipation + absorbed environmental minus conducted away)
- T_hot = maximum allowable radiator temperature (K)
- T_sink = effective sink temperature (K)

**Two-sided radiator correction:** If radiator sees Earth on back side, effective rejection is reduced. Use net Q_radiated - Q_earth_absorbed per side.

### Step 5: Heater Sizing (Cold Case)

During eclipse (worst cold case):
```
Q_heater = epsilon × sigma × A_exposed × T_min⁴ - Q_IR_absorbed - Q_conducted_from_neighbors
```

Cold case assumptions: zero solar input, minimum internal dissipation, EOL coating properties (highest alpha — worst for hot; lowest epsilon — worst for cold).

### Step 6: Hot/Cold Case Bounding

| Parameter | Hot Case | Cold Case |
|-----------|----------|-----------|
| Solar flux | 1414 W/m² (perihelion) | 1322 W/m² (aphelion) |
| Albedo | 0.35 | 0.25 |
| Earth IR | 258 W/m² | 216 W/m² |
| Internal power | Maximum dissipation | Minimum dissipation |
| Coatings | EOL alpha (degraded, higher) | BOL alpha (fresh, lower) |
| Eclipse | No eclipse (max beta) | Maximum eclipse (beta=0) |

---

### WORKED EXAMPLE: 500W Satellite at 525 km SSO

**Given:**
- Orbit: 525 km Sun-Synchronous (SSO), LTAN 10:30
- Beta angle range: 30° to 50° (SSO characteristic)
- Internal dissipation: Q_int = 500 W
- Radiator location: zenith-facing panel (no Earth view)
- Radiator coating: white paint AZ-93 (alpha=0.14, epsilon=0.92 BOL)
- Max allowable radiator temperature: T_rad = 40°C = 313.15 K
- Sink temperature (zenith, deep space): T_sink = 3 K
- Spacecraft box: 1.2 m x 1.0 m x 0.8 m

**Step A: Environmental geometry**
```
R_earth = 6371 km
h = 525 km
rho = arcsin(6371 / 6896) = 67.4°
F_earth = sin²(67.4°) = 0.852

Orbit period = 2*pi*sqrt((6896e3)³ / 3.986e14) = 5697 s = 94.95 min
Eclipse fraction (beta=30°): ~35% → eclipse = 33.2 min
Eclipse fraction (beta=50°): ~18% → eclipse = 17.1 min
```

**Step B: Environmental loads on zenith radiator (hot case, sunlit)**
```
Zenith radiator: F_earth ≈ 0 (faces away from Earth)
Direct solar on zenith face: Q_solar = alpha × S × A_rad × cos(theta_sun)
  For SSO beta=50°: theta_sun ≈ 40° off-normal → cos(40°) = 0.766
  Q_solar = 0.14 × 1361 × A_rad × 0.766 = 145.9 × A_rad  [W]

Albedo on zenith face: negligible (F_earth ≈ 0)
Earth IR on zenith face: negligible (F_earth ≈ 0)
```

**Step C: Radiator sizing (hot case)**
```
Energy balance on radiator:
  Q_int + Q_solar = epsilon × sigma × A_rad × (T_rad⁴ - T_sink⁴)

  T_sink⁴ is negligible: 3⁴ = 81 K⁴ vs 313.15⁴ = 9.62 × 10⁹ K⁴

  500 + 145.9 × A_rad = 0.92 × 5.67e-8 × A_rad × (313.15⁴)
  500 + 145.9 × A_rad = 0.92 × 5.67e-8 × A_rad × 9.617e9
  500 + 145.9 × A_rad = 501.7 × A_rad

Rearrange:
  500 = (501.7 - 145.9) × A_rad
  500 = 355.8 × A_rad
  A_rad = 500 / 355.8 = 1.405 m²

With 20% margin:
  A_rad_design = 1.405 × 1.2 = 1.69 m²
```

**Step D: Heater power (cold case — eclipse at beta=30°)**
```
During eclipse: Q_solar = 0, Q_albedo = 0
Zenith radiator still radiates to space.
Minimum internal dissipation (cold case): Q_int_min = 350 W (assume 70% of nominal)

Energy balance during eclipse:
  Q_int_min + Q_heater = epsilon × sigma × A_rad × T_min⁴

To maintain T_min = -10°C = 263.15 K:
  Q_radiated = 0.92 × 5.67e-8 × 1.69 × 263.15⁴
  Q_radiated = 0.92 × 5.67e-8 × 1.69 × 4.793e9
  Q_radiated = 0.92 × 5.67e-8 × 8.10e9
  Q_radiated = 422.9 W

  Q_heater = 422.9 - 350 = 72.9 W

Heater design with 25% margin:
  Q_heater_design = 72.9 × 1.25 = 91.1 W → specify 100 W heater circuit
```

**Step E: Summary**

| Parameter | Value |
|-----------|-------|
| Radiator area (calculated) | 1.41 m² |
| Radiator area (with 20% margin) | 1.69 m² |
| Radiator coating | AZ-93 white paint (alpha=0.14, epsilon=0.92) |
| Heater power (cold case) | 73 W calculated, 100 W specified |
| Equilibrium temp (hot, sunlit) | +40°C (design point) |
| Minimum temp (eclipse, heaters on) | -10°C (maintained) |
| MLI blankets | All non-radiator surfaces, effective emittance 0.02 |

---

## 7. OUTPUT TEMPLATE

```markdown
# [Mission Name] — Thermal Control Architecture

## Thermal Environment
| Parameter | Hot Case | Cold Case |
|-----------|----------|-----------|
| Solar flux | [X] W/m² | [X] W/m² |
| Albedo coefficient | [X] | [X] |
| Earth IR | [X] W/m² | [X] W/m² |
| Eclipse duration | [X] min | [X] min |
| Internal dissipation | [X] W | [X] W |

## Temperature Budget
| Component | Op. Min (°C) | Op. Max (°C) | Predicted Min | Predicted Max | Margin |
|-----------|-------------|-------------|--------------|--------------|--------|
| [component] | [limit] | [limit] | [predicted] | [predicted] | [+/- °C] |

## Radiator Sizing
| Parameter | Value |
|-----------|-------|
| Heat to reject | [X] W |
| Radiator coating | [name] (alpha=[X], epsilon=[X]) |
| Radiator area (calculated) | [X] m² |
| Radiator area (with margin) | [X] m² |
| Radiator temperature | [X] °C |

## Heater Budget
| Heater Zone | Cold Case Power (W) | Thermostat Range (°C) | Duty Cycle |
|-------------|--------------------|-----------------------|-----------|
| [zone] | [power] | [on/off] | [%] |
| **TOTAL** | **[X] W** | | |

## Thermal Control Hardware List
| Item | Quantity | Mass (kg) | Power (W) | Notes |
|------|----------|-----------|-----------|-------|
| [hardware] | [N] | [mass] | [power] | [note] |

## Recommendation
[Selected architecture, coating choices, heater strategy, risk items, next steps]
```

---

## 8. CLASSIFICATION

| Level | Name | Characteristics |
|-------|------|----------------|
| T1 | Standard LEO | Body-mounted radiators, MLI, heaters, standard coatings, -20 to +50°C |
| T2 | High Power / GEO | Deployed radiators, heat pipes, louvers, 1-10 kW dissipation |
| T3 | Cryogenic Payload | Active cooling to 40-80 K, Stirling/pulse tube, cryo heat pipes |
| T4 | Re-entry TPS | Ablative or reusable TPS, aerothermal analysis, stagnation heating |
| T5 | Extreme / Multi-regime | Combined cryo + TPS, nuclear thermal, outer planet (>5 AU), <4 K |

---

## 9. VARIATIONS

- **A: LEO (200-1000 km)** — Large Earth view factor (F=0.80-0.90), short eclipse (0-36 min), significant albedo input, atomic oxygen degrades coatings, beta angle drives thermal cases. Radiator sizing dominated by eclipse recovery.

- **B: GEO (35,786 km)** — Small Earth view factor (F=0.023), long eclipse season (up to 72 min near equinox, zero for months), solar dominates. OSR or silverized Teflon for stable radiators. Maximum eclipse at equinox is worst cold case.

- **C: Deep Space (>1 AU)** — Solar flux drops as 1/r²: Mars (589 W/m²), Jupiter (51 W/m²), Saturn (15 W/m²). Cold survival dominates. RHU (Radioisotope Heater Units, 1W each) for Plutonian missions. MLI and heater power are primary tools.

- **D: Re-entry** — Peak heating at stagnation: q_dot = C × sqrt(rho/R_n) × V³ (Sutton-Graves). LEO return ~7.8 km/s → 50-150 W/cm². Lunar return ~11 km/s → 200-500 W/cm². Mars return → up to 2,000 W/cm² (skip entry). TPS mass fraction 8-15% of entry vehicle.

- **E: Cryogenic Systems** — Detector cooling (40-80 K): Stirling or pulse tube cryocooler, parasitic heat loads from harness/structure must be <0.5 W. Propellant zero-boiloff (20 K LH2): requires 50-300 W cryocooler input. Thermal isolation via G-10 or Kevlar struts, vapor-cooled shields.

---

## 10. ERRORS & PITFALLS

- **E1**: Forgetting coating degradation — BOL alpha=0.14 becomes EOL alpha=0.28 after 5 years in LEO. Using BOL values for hot case underestimates peak temperature by 10-20°C.

- **E2**: Ignoring eclipse transients — Steady-state analysis says battery survives at -5°C, but thermal mass means a 36-min eclipse can drop temperature by 30°C transiently before heaters stabilize. Always check transient response.

- **E3**: Treating MLI as perfect insulation — Effective emittance of 0.01-0.03 is for lab conditions. With seams, penetrations, and compression, real-world MLI performance is 0.03-0.05. Use e*=0.03 minimum for design.

- **E4**: Wrong sink temperature — T_sink is NOT 3 K if your radiator sees Earth. A nadir-facing radiator at 400 km sees T_sink_effective ~250 K. Using 3 K overestimates rejection by 30-40%.

- **E5**: Single-node analysis for multi-zone spacecraft — A single thermal node cannot capture the 80°C gradient between a sun-facing panel and a shadow-side radiator. Use minimum 6 nodes (one per face) for a box satellite.

- **E6**: Ignoring parasitic heat paths to cryo stages — A single stainless steel bolt (6 mm dia, 50 mm long) from 300 K to 80 K conducts ~0.5 W. Ten bolts = 5 W parasitic, which can exceed the cryocooler budget. Always calculate conductive parasitics through every structural path.

- **E7**: Undersizing heaters by using average eclipse power — Peak heater demand occurs at the END of the longest eclipse when the satellite is coldest. Design heaters for worst-case instantaneous demand, not orbit-average.

- **E8**: Mixing absorptance and emittance domains — alpha_solar is weighted over 0.2-2.5 micron (solar spectrum). epsilon_IR is weighted over 5-50 micron (thermal IR). A surface can be alpha=0.08 and epsilon=0.80 simultaneously (OSR). These are NOT the same property at different temperatures.

---

## 11. TIPS

- **T1**: Start from the energy balance equation and solve for the unknown — if sizing radiator, solve for A_rad; if predicting temperature, solve for T; if sizing heater, solve for Q_heater. Same equation, different unknown.

- **T2**: Always run both hot case AND cold case — the hot case sizes the radiator (must reject max heat at max temp), the cold case sizes the heaters (must keep components warm during eclipse with minimum dissipation). They are coupled: bigger radiator means more heater power.

- **T3**: Use alpha/epsilon ratio as your primary coating selection parameter — low ratio (<0.3) for radiators, high ratio (>3.0) for surfaces you want warm, near 1.0 for thermally neutral surfaces.

- **T4**: Budget 20% margin on radiator area and 25% on heater power at preliminary design — this is standard ECSS and NASA practice. Reduce to 10%/15% at CDR with test-correlated thermal model.

- **T5**: For quick radiator estimates at 300 K and epsilon=0.85: ~390 W/m² rejection to deep space. At 350 K: ~640 W/m². At 250 K: ~200 W/m². Memorize these for sanity checks.

- **T6**: Heat pipes are not magic — they have a gravity sensitivity (0.1-0.3 W tilt/cm adverse), a power limit (dryout), and a startup problem when frozen. Specify operating orientation for ground testing. Loop heat pipes solve the distance and gravity problems but add mass and cost.

- **T7**: Calibrate against known spacecraft — ISS radiators: 14 panels x 23 m² each, rejecting ~70 kW total. Hubble: 5.1 kW dissipation, body-mounted radiators. Mars rovers: RHU + electric heaters, MLI blankets. If your numbers are wildly different from heritage, double-check.

- **T8**: For re-entry TPS sizing, use 1D ablation codes (FIAT, CMA) or at minimum the Sutton-Graves correlation for stagnation heating: q_dot = 1.7415e-4 × sqrt(rho_inf / R_n) × V_inf³ W/m². Nose radius R_n dominates — doubling R_n cuts heating by sqrt(2).

---

## 12. RELATED SKILLS

| Need | Skill | What It Adds |
|------|-------|-------------|
| Orbit geometry | **orbital-mechanics** | Beta angle, eclipse duration, solar distance over mission |
| Engine cooling | **propulsion** | Nozzle regen cooling, turbopump thermal, cryo propellant management |
| Full system budget | **mission-architect** | Mass/power roll-up with thermal subsystem allocation |
| Structural loads | **structural** | Thermal gradient stress, CTE mismatch, distortion analysis |
| Power allocation | **power-systems** | Heater power budget, solar array temp derating, battery limits |
| Radiation environment | **space-environment** | Coating degradation rates, UV dose, AO fluence |
| Trade spreadsheet | **xlsx** | Parametric thermal model with live formulas |
| Review deck | **pptx** | TDR/PDR/CDR thermal presentations |
