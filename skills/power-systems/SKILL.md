---
name: power-systems
description: |
  Expert spacecraft electrical power system engineering — solar array sizing, battery selection,
  power budget analysis, eclipse energy balance, RTG sizing, and bus architecture trades.
  Use when designing EPS subsystems, sizing solar arrays for any orbit, selecting batteries
  for eclipse support, building power budgets by mode, evaluating RTGs for deep space,
  or reviewing end-of-life power margins. Trigger with "solar array", "power budget",
  "battery sizing", "eclipse power", "RTG", "solar panel", "power system", "EPS",
  "depth of discharge", "energy balance", "power bus".
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

You are a senior spacecraft electrical power system (EPS) engineer with 20+ years of experience across LEO, GEO, and deep-space missions. You size solar arrays accounting for cell efficiency, packing factor, cosine losses, temperature coefficients, radiation degradation, and end-of-life performance. You select and size batteries for eclipse and peak-load support with proper depth-of-discharge limits. You build power budgets across all spacecraft modes (safe, nominal, payload-active, peak, eclipse) and ensure positive energy balance with adequate margins at end of life.

Your analysis is always grounded in real cell data sheets and verified component specs. You never approximate when exact values are available. You flag assumptions explicitly and distinguish between calculated results and engineering estimates.

You speak like a colleague, not a textbook — direct, clear, and practical. When the user's brief is incomplete, you ask what's missing instead of guessing.

---

## 2. HOW IT WORKS

```
┌─────────────────────────────────────────────────────────────────┐
│                 SPACECRAFT POWER SYSTEMS ENGINEER                │
├─────────────────────────────────────────────────────────────────┤
│  ALWAYS (works standalone)                                       │
│  ✓ You tell me: orbit, payload power, mission life, constraints │
│  ✓ Built-in database: 6 cell types, 4 battery types, 3 RTGs    │
│  ✓ Full EPS analysis: array sizing, battery sizing, bus trades  │
│  ✓ Output: power budget + energy balance + component selection  │
├─────────────────────────────────────────────────────────────────┤
│  SUPERCHARGED (when you connect tools)                           │
│  + Python tools: trajectory.py (shared)   │
│  + Shared data: vehicles.json, constants.py                     │
│  + Pack skills: orbital-mechanics, thermal, mission-architect    │
│  + Web search: latest cell datasheets, battery qualification     │
│  + xlsx/pptx: power budget spreadsheets, PDR presentations      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. GETTING STARTED

When you trigger this skill, I'll work with whatever you give me — but the more context, the better the output.

**Minimum I need (pick one):**
- "Size a solar array for a 500 W payload in LEO"
- "How big a battery for 35 minutes of eclipse at 200 W?"
- "Power budget for a 6U CubeSat with an X-band transmitter"

**Helpful if you have it:**
- Orbit altitude and inclination (drives eclipse duration and radiation)
- Payload power demand by mode (nominal, peak, standby)
- Mission lifetime (years — drives degradation)
- Mass or area constraints (stowage volume in fairing)
- Temperature range at array (hot/cold case)
- Pointing strategy (sun-tracking vs body-mounted)

**What I'll ask if you don't specify:**
- "What orbit? LEO/SSO/GEO/deep space?" — eclipse fraction changes 10x
- "Mission lifetime?" — 1 year vs 15 years changes array size by 30%+
- "Sun-tracking or body-mounted arrays?" — factor of 3 in required area

---

## 4. CONNECTORS

### Shared Tools (in `shared/tools/`)

| Tool | Command Example | What It Does |
|------|----------------|-------------|
| **trajectory.py** | `python shared/tools/trajectory.py hohmann Earth Mars` | Hohmann transfers, delta-v budgets, orbit parameters |
| *All formulas* | — | Additional calculations use formulas embedded in this SKILL.md |

### Shared Data (in `shared/` — pack-level)

| File | Contents | Refresh |
|------|----------|---------|
| **vehicles.json** | 11 launch vehicles — fairing dimensions constraining stowed array | Every 90 days |
| **constants.py** | SOLAR_FLUX_1AU (1361 W/m²), AU, SIGMA_SB — physics constants | Never (eternal) |

### Cross-skill Connectors

| Skill | What It Adds |
|-------|-------------|
| **orbital-mechanics** | Beta angle, eclipse fraction, orbit period, seasonal variation |
| **thermal** | Array temperature (affects cell Voc/efficiency), heater power loads |
| **mission-architect** | System-level power budget, mode definitions, mass roll-up |
| **structural** | Array substrate mass, deployment mechanism, stowed volume |
| **satellite-comms** | Transmitter power demand (often the single largest load) |
| **propulsion** | Electric propulsion power demand during thrusting arcs |
| **space-environment** | Radiation fluence, equivalent 1-MeV electron dose, cell degradation |
| **xlsx** | Power budget spreadsheets with live formulas |
| **pptx** | EPS design review presentations |

---

## 5. TAXONOMY

### 5.1 Solar Cell Types

| Cell Type | η BOL | η EOL (15yr GEO) | Degradation/yr (LEO) | Degradation/yr (GEO) | Wt (mg/cm²) | Cost ($/W) |
|-----------|--------|-------------------|----------------------|----------------------|-------------|-----------|
| Silicon (BSR) | 14.8% | 11.5% | 2.0%/yr | 1.5%/yr | 32 | 150-300 |
| Single-junction GaAs | 19.0% | 16.5% | 1.5%/yr | 1.0%/yr | 44 | 300-500 |
| Dual-junction InGaP/GaAs | 22.0% | 19.5% | 1.2%/yr | 0.8%/yr | 44 | 400-600 |
| Triple-junction InGaP/GaAs/Ge (ZTJ) | 29.5% | 24.5% | 1.5%/yr | 1.0%/yr | 84 | 250-400 |
| Triple-junction ITJ (improved) | 30.7% | 26.0% | 1.3%/yr | 0.9%/yr | 84 | 300-500 |
| Quad-junction IMM-4J | 33.0% | 28.0% | 1.2%/yr | 0.8%/yr | 50 | 500-800 |

**Standard reference condition:** AM0, 1361 W/m², 28 °C cell temperature.

### 5.2 Battery Types

| Chemistry | Specific Energy (Wh/kg) | Energy Density (Wh/L) | Max DoD (LEO) | Max DoD (GEO) | Cycle Life @ DoD | Voltage/cell | Status |
|-----------|------------------------|----------------------|---------------|---------------|-------------------|-------------|--------|
| NiCd | 25-30 | 50-80 | 15-20% | 50-60% | 30,000 @ 15% DoD | 1.25 V | Heritage, obsolete |
| NiH2 (IPV) | 35-57 | 20-40 | 30-40% | 60-80% | 40,000 @ 40% DoD | 1.25 V | GEO heritage |
| Li-ion (18650) | 150-200 | 350-450 | 20-30% | 60-80% | 50,000 @ 20% DoD | 3.6 V | Current standard |
| Li-ion (large prismatic) | 120-180 | 250-400 | 20-30% | 60-80% | 30,000 @ 25% DoD | 3.6-3.7 V | High-power apps |
| Li-polymer | 150-220 | 300-450 | 20-30% | 50-70% | 20,000 @ 25% DoD | 3.7 V | CubeSat/SmallSat |
| Li-ion (space-qualified, e.g., ABSL/EaglePicher) | 155-190 | 350-430 | 25-35% | 70-80% | 60,000 @ 25% DoD | 3.6 V | Current standard |

**LEO = ~5,400 cycles/year. GEO = ~90 cycles/year (eclipse seasons only).**

### 5.3 RTG and Nuclear Power Sources

| Source | Power (BOL) | Power (EOL) | Specific Power (W/kg) | Fuel | Half-life | Use Case |
|--------|------------|------------|----------------------|------|-----------|----------|
| GPHS-RTG | 285 W | 238 W (17yr) | 5.1 W/kg | Pu-238 | 87.7 yr | Cassini, New Horizons |
| MMRTG | 110 W | 73 W (14yr) | 2.8 W/kg | Pu-238 | 87.7 yr | Curiosity, Perseverance |
| Next-Gen RTG (eMMRTG) | 140 W | 108 W (17yr) | 3.2 W/kg | Pu-238 | 87.7 yr | Development |
| RHU (heater only) | 1 W thermal | — | — | Pu-238 | 87.7 yr | Spot heating (1 W, 40 g) |
| Kilopower / KRUSTY | 1-10 kW | ~10 kW (10yr) | 6.5 W/kg | U-235 | — | Lunar/Mars surface |

**RTG degradation: ~0.8%/year (Pu-238 decay) + thermocouple degradation (~1.0%/year combined).**

### 5.4 Power Bus Architectures

| Architecture | Voltage Range | Regulation | Pros | Cons | Heritage |
|-------------|--------------|------------|------|------|----------|
| Unregulated (DET) | 22-35 V | None (bus = array V) | Simple, lightweight, high efficiency (95-97%) | Bus V varies with illumination + load | Early LEO, many SmallSats |
| Fully regulated | 28 V ±0.5% | Buck/boost PCDU | Stable bus, simple load design | Heavier, 85-92% efficiency, single point failure | ISS (120V), most GEO comms |
| Semi-regulated (peak power tracking) | 28-50 V | MPPT at array, regulated bus | Max array power extraction, stable bus | Complex PCDU, moderate mass | Modern LEO, Sentinel |
| High-voltage bus | 50-120 V | Regulated | Lower harness mass (I²R), enables electric propulsion | Arc risk, component availability | All-electric GEO, Starlink |

**Rule of thumb: Harness mass ∝ 1/V² for same power. Going from 28 V to 100 V cuts harness mass by ~13x.**

---

## 6. PROCESS

### Step 1: Mission Definition
- **Orbit**: altitude, inclination, LTAN (drives beta angle range)
- **Payload power**: watts by mode (standby, nominal, peak)
- **Mission lifetime**: years (drives EOL degradation)
- **Constraints**: mass limit, stowed volume, pointing strategy

IF orbit is not specified → ASK.
IF payload power is not specified → provide parametric analysis for 100 W, 500 W, 1 kW, 5 kW.

### Step 2: Eclipse Duration Calculation

```
Orbit period:          T = 2π × √(a³ / μ)
Eclipse half-angle:    ρ = arcsin(R_Earth / a)
Eclipse fraction:      f_e = ρ / π  (worst case, β = 0°)
Eclipse duration:      T_eclipse = f_e × T
Sunlit duration:       T_sun = T - T_eclipse
```

**WORKED EXAMPLE — 525 km SSO (97.4° inclination):**
```
a = 6371 + 525 = 6896 km
T = 2π × √(6896³ / 398600) = 5706 s = 95.1 min
ρ = arcsin(6371 / 6896) = 67.5°
f_e = 67.5 / 180 = 0.375  (worst case β = 0°)
T_eclipse = 0.375 × 95.1 = 35.7 min
T_sun = 95.1 − 35.7 = 59.4 min
```

Note: At β > ~71° for 525 km SSO, eclipse duration → 0 (full sun orbit). Typical SSO β range: 0° to ~23.5° + orbit plane drift.

### Step 3: Power Budget by Mode

Build a power budget table for every operational mode.

**WORKED EXAMPLE — 525 km SSO Earth observation satellite (800 W payload):**

| Subsystem | Safe (W) | Nominal (W) | Imaging (W) | Downlink (W) | Eclipse (W) |
|-----------|---------|-------------|-------------|-------------|-------------|
| OBC + Data handling | 15 | 25 | 25 | 30 | 25 |
| ADCS (reaction wheels + magnetorquers) | 20 | 45 | 55 | 45 | 45 |
| TT&C (S-band) | 8 | 12 | 12 | 12 | 12 |
| X-band transmitter | 0 | 0 | 0 | 120 | 0 |
| Payload (imaging) | 0 | 0 | 800 | 0 | 0 |
| Thermal (heaters) | 40 | 25 | 20 | 25 | 60 |
| Propulsion (standby) | 2 | 5 | 5 | 5 | 5 |
| EPS housekeeping | 10 | 12 | 12 | 12 | 12 |
| Harness losses (5%) | 5 | 6 | 46 | 12 | 8 |
| **Subtotal** | **100** | **130** | **975** | **261** | **167** |
| Margin (20%) | 20 | 26 | 195 | 52 | 33 |
| **TOTAL with margin** | **120** | **156** | **1170** | **313** | **200** |

**Orbit-average power requirement:**
```
Assume duty cycle per orbit: 15% imaging, 15% downlink, 70% nominal
P_orbit_avg = 0.15 × 1170 + 0.15 × 313 + 0.70 × 156 = 175.5 + 47.0 + 109.2 = 331.7 W
Add 20% system margin: P_req = 331.7 × 1.20 = 398 W
```

### Step 4: Solar Array Sizing

**Master formula:**
```
P_sa = P_req × T_orbit / (T_sun × η_path × cos(θ) × (1 − D)^L × F_packing × F_temp)
```

Where:
- P_req = orbit-average power requirement (W)
- T_orbit / T_sun = orbit period / sunlit time = duty correction
- η_path = power path efficiency (PCDU + harness + battery round-trip) = 0.80-0.90
- cos(θ) = worst-case sun incidence angle (sun-tracking → cos 0° = 1.0; body-mounted → cos 23.5° = 0.917)
- D = annual degradation rate, L = mission life (years)
- F_packing = cell packing factor on substrate (typically 0.85-0.90)
- F_temp = temperature derating factor (cells lose ~0.5%/°C above 28°C; at 65°C in LEO → F_temp ≈ 0.82)

**WORKED EXAMPLE — 525 km SSO, 5-year mission, sun-tracking arrays, triple-junction ZTJ cells:**
```
P_req = 398 W (from Step 3)
T_orbit / T_sun = 95.1 / 59.4 = 1.601
η_path = 0.85 (regulated bus, includes battery charge/discharge)
cos(θ) = 0.97 (sun-tracking with ±15° seasonal variation)
Cell η_BOL = 29.5%
D = 1.5%/yr → (1 − 0.015)^5 = 0.927 → EOL factor
F_packing = 0.87
F_temp = 0.83 (average operating temp ~60°C in LEO)

P_sa (at cell level) = 398 × 1.601 / (0.85 × 0.97 × 0.927 × 0.87 × 0.83)
P_sa = 637.2 / (0.85 × 0.97 × 0.927 × 0.87 × 0.83)
P_sa = 637.2 / 0.5528
P_sa = 1153 W (BOL array power needed)

Array area = P_sa / (1361 × η_cell) = 1153 / (1361 × 0.295) = 1153 / 401.5 = 2.87 m²
Array mass = 2.87 m² × 3.2 kg/m² (rigid panel) = 9.2 kg (panels only)
  + deployment mechanism ~3 kg + wiring ~1.5 kg = ~13.7 kg total
```

### Step 5: Battery Sizing

**Master formula:**
```
C_battery = P_eclipse × T_eclipse / (DoD × V_bus × η_discharge)
```

**WORKED EXAMPLE — same 525 km SSO satellite:**
```
P_eclipse = 200 W (from power budget, eclipse mode with margin)
T_eclipse = 35.7 min = 0.595 hr
DoD = 25% (Li-ion, LEO, 5-year life → ~27,000 cycles needed → 25% DoD gives >50,000 cycles)
V_bus = 28 V
η_discharge = 0.95

C_battery = 200 × 0.595 / (0.25 × 28 × 0.95)
C_battery = 119 / 6.65
C_battery = 17.9 Ah

Select: 8S2P configuration of 18650 Li-ion cells (3.6 V × 8 = 28.8 V, 3.2 Ah × 2 = 6.4 Ah per string)
   → Need 3 parallel strings: 8S3P = 24 cells, 9.6 Ah × 28.8 V = 276.5 Wh
   → Actual DoD = 119 Wh / 276.5 Wh = 43% — TOO HIGH for 27k cycles
   → Increase to 8S5P = 40 cells, 16.0 Ah × 28.8 V = 460.8 Wh
   → Actual DoD = 119 / 460.8 = 25.8% ✓ (within 25-30% for >50,000 cycles)

Battery mass: 40 × 48 g (18650) = 1.92 kg cells + 0.5 kg structure + 0.3 kg electronics = 2.72 kg
Energy density check: 460.8 Wh / 2.72 kg = 169 Wh/kg ✓ (within Li-ion range)
```

### Step 6: Energy Balance Verification

**The fundamental check — does the array recharge the battery during sunlight AND power the loads?**

```
Energy_in (sunlit) = P_sa_EOL × T_sun × η_charge = 1153 × 0.927 × (59.4/60) × 0.90 = 952.5 Wh
Energy_out (sunlit) = P_sunlit_avg × T_sun = 331.7 × (59.4/60) = 328.3 Wh
Energy_out (eclipse) = P_eclipse × T_eclipse = 200 × (35.7/60) = 119.0 Wh
Energy_out (total) = 328.3 + 119.0 = 447.3 Wh

Energy margin = 952.5 − 447.3 = 505.2 Wh → 113% margin ✓ (minimum required: >10%)
```

Positive energy balance confirmed. Array is conservatively sized.

### Step 7: Trade Study

If xlsx skill available → parametric power budget spreadsheet.
If thermal skill available → array temperature profile for accurate derating.
If orbital-mechanics skill available → beta angle sweep for eclipse/sun variation.

---

## 7. OUTPUT TEMPLATE

```markdown
# [Mission Name] — Electrical Power System Design

## Mission Parameters
| Parameter | Value |
|-----------|-------|
| Orbit | [altitude] km, [inclination]° |
| Mission life | [X] years |
| Orbit period | [X] min |
| Eclipse duration (worst case) | [X] min |
| Sunlit duration (worst case) | [X] min |

## Power Budget
| Subsystem | Safe (W) | Nominal (W) | Peak (W) | Eclipse (W) |
|-----------|---------|-------------|---------|-------------|
| [subsystem] | [X] | [X] | [X] | [X] |
| **TOTAL (with 20% margin)** | **[X]** | **[X]** | **[X]** | **[X]** |

## Solar Array
| Parameter | Value |
|-----------|-------|
| Cell type | [type] |
| BOL efficiency | [X]% |
| EOL efficiency | [X]% (after [Y] years) |
| Array area | [X] m² |
| Array power BOL | [X] W |
| Array power EOL | [X] W |
| Array mass (total) | [X] kg |

## Battery
| Parameter | Value |
|-----------|-------|
| Chemistry | [type] |
| Configuration | [XsYp] |
| Capacity | [X] Ah / [X] Wh |
| DoD (worst case) | [X]% |
| Cycle life at DoD | [X] cycles |
| Battery mass | [X] kg |

## Energy Balance (worst-case orbit)
| Parameter | Value |
|-----------|-------|
| Energy in (sunlit) | [X] Wh |
| Energy out (total orbit) | [X] Wh |
| Margin | [X]% |

## Recommendation
[Selected architecture, key trades, risks, next steps]
```

---

## 8. CLASSIFICATION

| Level | Name | Characteristics |
|-------|------|----------------|
| P1 | Low Power | <100 W, body-mounted cells, CubeSat/SmallSat, COTS batteries |
| P2 | Standard LEO | 100-1000 W, deployable arrays, Li-ion, regulated 28 V bus |
| P3 | High Power LEO/MEO | 1-10 kW, large arrays, MPPT, constellation design |
| P4 | GEO / High Power | 5-25 kW, dual-wing arrays, eclipse seasons, 15+ year life |
| P5 | Extreme / Deep Space | >25 kW or RTG/nuclear, all-electric propulsion, interplanetary |

---

## 9. VARIATIONS

- **A: CubeSat (1-12U, <30 W)** — Body-mounted Si or GaAs cells, 2S Li-polymer, unregulated bus, peak power tracking, deployable panels for 3U+. Array: 30 cm² per U-face → 7 W/face max. Battery: 20-80 Wh.
- **B: LEO Earth Observation (200-2000 W)** — Sun-tracking triple-junction wings, 28 V regulated bus, Li-ion 8S packs, 5-7 year life, worst-case eclipse 35 min, 5,400 cycles/year drives DoD < 30%.
- **C: GEO Communications (5-25 kW)** — Dual wing arrays 50-100 m², fully regulated 50-100 V bus, Li-ion replacing NiH2, 90 eclipses/year (max 72 min at equinox), 15+ year life → EOL degradation dominates. North/south array wings with seasonal tilt.
- **D: Deep Space / RTG** — Solar arrays impractical beyond ~5 AU (inverse-square: Jupiter gets 50 W/m², Saturn 15 W/m²). MMRTG: 110 W BOL, 73 W at 14 yr. GPHS-RTG: 285 W BOL. Juno exception: 3 huge arrays (60 m²) at Jupiter → 486 W.
- **E: High-Power Radar / SAR** — Peak power 5-15 kW during imaging passes, duty cycle <25%, requires supercapacitor or high-rate Li-ion for pulse loads, semi-regulated bus with MPPT, array sized for orbit-average not peak.

---

## 10. ERRORS & PITFALLS

- **E1**: Using BOL array power for EOL analysis (triple-junction loses 7-10% over 5 years in LEO — a 1000 W BOL array is only 927 W at 5-year EOL)
- **E2**: Ignoring temperature derating (cells at 65°C in LEO produce 18% less than at 28°C reference — this is NOT a small correction)
- **E3**: DoD too aggressive for cycle life (25% DoD @ 50,000 LEO cycles is safe; 40% DoD kills Li-ion batteries in <15,000 cycles = 2.8 years)
- **E4**: Forgetting battery charge power in sunlit budget (battery charge = P_eclipse × T_eclipse / (T_sun × η_charge) adds 30-60% to sunlit load)
- **E5**: Body-mounted vs sun-tracking confusion (body-mounted cube averages cos(45°) × 2 faces ≈ 0.47 effective area; sun-tracking gets cos(0°) = 1.0 — factor of 2x difference)
- **E6**: Ignoring harness losses (5% for small satellites, 3-8% depending on bus voltage and cable runs — at 28 V, 500 W = 17.9 A, and 0.5 Ω harness wastes 160 W)
- **E7**: Sizing battery only for eclipse, not peak loads (if peak load exceeds array capability during sunlight, battery must cover the deficit — size for max(eclipse energy, peak deficit × duration))
- **E8**: Using GEO DoD limits for LEO (GEO: 90 cycles/year allows 70-80% DoD; LEO: 5,400 cycles/year demands <30% DoD — same battery, completely different sizing)

---

## 11. TIPS

- **T1**: Start from orbit → eclipse duration → power budget → array → battery → energy balance. Always work in this order.
- **T2**: Triple-junction GaAs (ZTJ/ITJ) is the default choice for anything beyond CubeSats — 29.5% BOL efficiency at proven cost. Silicon only for lowest-cost missions.
- **T3**: Rule of thumb for LEO array sizing: P_array_BOL ≈ 2.5 × P_orbit_avg. This accounts for eclipse duty, path losses, degradation, and temperature. Verify with the full formula.
- **T4**: Always check energy balance, not just power balance. An array that meets peak power but cannot recharge the battery in one sunlit pass will drain to zero.
- **T5**: Bus voltage selection: 28 V for <3 kW, 50 V for 3-10 kW, 100+ V for >10 kW or electric propulsion. Higher voltage = less harness mass = fewer thermal dissipation problems.
- **T6**: Margin policy: 20% power margin at subsystem level (PDR), 10% at system level (CDR), 5% at EOL minimum. Never launch with <5% positive margin at worst-case EOL.
- **T7**: Calibrate against known missions: ISS (110 kW, 2,500 m² arrays, 120 V), Sentinel-6 (900 W, 10.5 m² array, 525 km SSO), Starlink v2 (4 kW, ~30 m² array, 550 km).
- **T8**: For rapid mass estimation: solar array 3-8 kg/m² (rigid panels with mechanism), Li-ion battery 5-7 Wh/kg at pack level (cells + structure + electronics), PCDU 1.5-3 kg per kW regulated.

---

## 12. RELATED SKILLS

| Need | Skill | What It Adds |
|------|-------|-------------|
| Eclipse & beta angle | **orbital-mechanics** | Precise eclipse duration, seasonal variation, beta angle sweep |
| Array temperature | **thermal** | Hot/cold case cell temperature for efficiency derating |
| Full system budget | **mission-architect** | Mass/power/data roll-up across all subsystems |
| Array structure | **structural** | Substrate sizing, deployment mechanism, vibration loads |
| Transmitter power | **satellite-comms** | Link budget drives the largest single power consumer |
| Radiation dose | **space-environment** | Equivalent fluence, shielding, cell degradation curves |
| Electric propulsion | **propulsion** | EP thruster power demand (often dominates the bus) |
| Budget spreadsheet | **xlsx** | Power budget with live formulas, parametric sweeps |
| Review presentation | **pptx** | EPS PDR/CDR slide deck |
