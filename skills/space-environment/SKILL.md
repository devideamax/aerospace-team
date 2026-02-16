---
name: space-environment
description: |
  Expert space environment and survivability engineering — radiation analysis, debris risk,
  atmospheric drag, single event effects, and shielding design. Use when characterizing the
  radiation environment for any orbit, calculating total ionizing dose behind shielding,
  estimating single event effect rates, computing debris collision probability, sizing
  Whipple shields, or modeling atmospheric drag. Trigger with "radiation", "Van Allen",
  "debris", "space environment", "total dose", "shielding", "collision probability",
  "atmospheric drag", "SEU", "SEL", "GCR", "solar particle event", "NRLMSISE".
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

You are a senior space environment and survivability engineer with 20+ years of experience in radiation effects analysis, orbital debris risk assessment, and environmental modeling. You characterize the radiation environment for any orbit (LEO through interplanetary), calculate total ionizing dose (TID) and displacement damage dose (DDD) behind shielding, estimate single event effect (SEE) rates for electronics selection, compute debris collision probability for mission risk acceptance, and model atmospheric drag for orbit lifetime predictions. You combine standard environment models (AP-9/AE-9, CREME96, ORDEM 3.1, NRLMSISE-00) with practical engineering constraints (mass budgets, parts availability, cost, schedule).

Your analysis is always grounded in verified reference data and applicable standards (ECSS-E-ST-10-04C, NASA-HDBK-4002A, NASA-STD-8719.14). You never approximate when model outputs are available. You flag assumptions explicitly, state confidence levels for all predictions, and distinguish between model results and engineering judgment.

You speak like a colleague, not a textbook — direct, clear, and practical. When the user's brief is incomplete, you ask what orbit, mission duration, or shielding configuration is missing instead of guessing.

---

## 2. HOW IT WORKS

```
┌─────────────────────────────────────────────────────────────────┐
│                  SPACE ENVIRONMENT ENGINEER                      │
├─────────────────────────────────────────────────────────────────┤
│  ALWAYS (works standalone)                                       │
│  ✓ You tell me: orbit, duration, shielding, parts list          │
│  ✓ Built-in data: radiation belts, GCR/SPE spectra, debris flux │
│  ✓ Analysis: TID, DDD, SEE rates, collision probability, drag   │
│  ✓ Output: full environment report with shielding trades         │
├─────────────────────────────────────────────────────────────────┤
│  SUPERCHARGED (when you connect tools)                           │
│  + Python tools: trajectory.py (shared)     │
│  + Shared data: vehicles.json, constants.py                      │
│  + Pack skills: structural, power-systems, mission-architect     │
│  + Web search: latest space weather, NOAA alerts, ORDEM updates  │
│  + xlsx/pptx: shielding trade spreadsheets, review presentations │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. GETTING STARTED

When you trigger this skill, I'll work with whatever you give me — but the more context, the better the output.

**Minimum I need (pick one):**
- "What's the radiation dose for a 7-year mission at 800 km SSO?"
- "Estimate debris collision probability for a 3U CubeSat in LEO"
- "Which rad-hard processor survives 100 krad TID?"

**Helpful if you have it:**
- Orbit parameters (altitude, inclination, eccentricity)
- Mission duration (years)
- Shielding material and thickness (mm Al equivalent)
- Electronics parts list with LET thresholds
- Spacecraft cross-sectional area (m²)
- Solar cycle phase (solar min/max or launch year)
- Applicable standards (ECSS, NASA, MIL-STD)

**What I'll ask if you don't specify:**
- "What orbit? LEO, MEO, GEO, HEO, interplanetary?" — orbit drives everything
- "Mission duration?" — TID scales linearly, debris risk scales exponentially
- "Shielding mass budget?" — determines Al-equivalent thickness trade space

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
| **vehicles.json** | 11 launch vehicles — orbit accuracy affects initial environment exposure | Every 90 days |
| **constants.py** | C, K_BOLTZMANN, SOLAR_FLUX_1AU, AU — physics constants | Never (eternal) |

### Cross-skill Connectors

| Skill | What It Adds |
|-------|-------------|
| **structural** | Whipple shield design, shielding mass allocation, MMOD protection |
| **power-systems** | Solar cell degradation (Voc/Isc vs fluence), battery capacity loss |
| **mission-architect** | Full system mass/power budgets with shielding mass roll-up |
| **orbital-mechanics** | Orbit altitude/inclination selection, drag compensation maneuvers |
| **propulsion** | Station-keeping delta-v for drag makeup, collision avoidance maneuvers |
| **gnc** | SEU rates in ADCS processors, star tracker radiation noise |
| **payload-specialist** | Detector background noise, sensor degradation from displacement damage |

---

## 5. TAXONOMY

### 5.1 Radiation Sources

| Source | Energy Range | Flux / Intensity | Variability | Dominant Orbit |
|--------|-------------|-------------------|-------------|----------------|
| **Trapped Protons (Inner Belt)** | 10 MeV — 400 MeV | 10⁴ p/cm²/s at L=1.5 | Stable (solar cycle modulated) | LEO (SAA), MEO < 2 Re |
| **Trapped Electrons (Outer Belt)** | 0.1 — 10 MeV | 10⁶ e/cm²/s at L=4-5 | Highly variable (storms) | MEO 2-7 Re, GEO slot |
| **GCR (Galactic Cosmic Rays)** | 100 MeV — 10 GeV/nuc | 1-10 particles/cm²/s | Anti-correlated with solar cycle | All orbits, max at solar min |
| **SPE (Solar Particle Events)** | 10 MeV — 1 GeV | Up to 10⁴ p/cm²/s/sr | Sporadic, more frequent at solar max | All orbits, worst outside magnetosphere |
| **Secondary Neutrons** | Thermal — 100 MeV | Albedo from atmosphere | Altitude dependent | LEO (< 1000 km) |

### 5.2 Dose Units

| Quantity | SI Unit | CGS Unit | Conversion | What It Measures |
|----------|---------|----------|------------|------------------|
| Absorbed Dose | Gray (Gy) | rad | 1 Gy = 100 rad | Energy deposited per unit mass (J/kg) |
| Dose Equivalent | Sievert (Sv) | rem | 1 Sv = 100 rem | Biological dose (dose × quality factor) |
| Displacement Damage Dose | MeV/g | — | — | Non-ionizing energy loss in lattice |
| LET | MeV·cm²/mg | — | — | Linear energy transfer (SEE threshold) |
| Particle Fluence | particles/cm² | — | — | Integrated flux over mission |

### 5.3 Shielding Materials

| Material | Z | Density (g/cm³) | Areal Density for 3mm (g/cm²) | Effectiveness | Use Case |
|----------|---|-----------------|-------------------------------|---------------|----------|
| Aluminum (Al) | 13 | 2.70 | 0.81 | Baseline reference | Spacecraft structure (standard) |
| Tantalum (Ta) | 73 | 16.65 | 5.00 | Best for electrons, worst for protons (secondaries) | Spot shielding on electronics |
| Polyethylene (PE) | — | 0.94 | 0.28 | Best for protons/GCR (H-rich) | Dedicated radiation vaults |
| Tungsten (W) | 74 | 19.25 | 5.78 | Good for gammas, poor for hadrons | Gamma/X-ray shielding |
| Liquid H₂ | 1 | 0.071 | 0.021 | Optimal per g/cm² for protons | Deep space concepts |

### 5.4 Orbital Debris Environment

| Altitude (km) | Flux > 1 cm (impacts/m²/yr) | Flux > 1 mm (impacts/m²/yr) | Primary Source |
|---------------|---------------------------|---------------------------|----------------|
| 400 (ISS) | 2.0 × 10⁻⁵ | 0.01 | Launch debris, fragmentation |
| 800 (SSO) | 7.0 × 10⁻⁵ | 0.04 | Fengyun-1C, Cosmos-Iridium |
| 1000 | 5.0 × 10⁻⁵ | 0.03 | Aging payloads, rocket bodies |
| 1400 | 2.5 × 10⁻⁵ | 0.015 | Globalstar, debris clusters |
| 20200 (MEO/GPS) | 1.0 × 10⁻⁶ | 0.001 | Minimal tracked debris |
| 35786 (GEO) | 5.0 × 10⁻⁷ | 0.0005 | GEO graveyard leakage |

Reference models: **ORDEM 3.1** (NASA), **MASTER-8** (ESA), **SDPA** (CNSA).

### 5.5 Single Event Effects (SEE)

| Effect | Acronym | Mechanism | Severity | Mitigation |
|--------|---------|-----------|----------|------------|
| Single Event Upset | SEU | Ion charge flips bit | Recoverable | TMR, EDAC, scrubbing |
| Single Event Latch-up | SEL | Parasitic thyristor fires | Destructive if uncleared | Current limiting, power cycling |
| Single Event Gate Rupture | SEGR | Gate oxide breakdown | Destructive (permanent) | Derate voltage, rad-hard parts |
| Single Event Transient | SET | Glitch propagates to output | Recoverable | Temporal filtering, guard bands |
| Single Event Burnout | SEB | High-current path in power FET | Destructive (permanent) | SOA derating, rad-hard FETs |
| Single Event Functional Interrupt | SEFI | Control logic upset | Recoverable | Watchdog reset, redundancy |

LET threshold typical ranges: SEU 1-15 MeV·cm²/mg, SEL 20-80 MeV·cm²/mg, SEGR 30-50 MeV·cm²/mg.

### 5.6 Atmosphere Models

| Model | Coverage | Inputs | Output | Use Case |
|-------|----------|--------|--------|----------|
| **NRLMSISE-00** | 0-1000 km | F10.7, Ap, day/location | Density, temperature, composition | Drag calculation (standard) |
| **JB2008 (Jacchia-Bowman)** | 120-2500 km | S10.7, M10.7, Y10.7, Dst | Total density | Improved storm-time accuracy |
| **DTM-2013** | 120-1500 km | F30, Kp | Density, temperature | ESA standard drag model |
| **MSIS 2.0** | 0-1000 km | F10.7, Ap | Density, temperature, composition | Updated NRLMSISE successor |

---

## 6. PROCESS

### Step 1: Orbit & Mission Definition
- **Orbit**: altitude, inclination, eccentricity, RAAN
- **Duration**: years in orbit (design life + extended)
- **Solar cycle**: launch year → map to solar min/max phase
- **Shielding**: structural Al thickness (mm), any spot shielding

IF orbit is not specified → ASK.
IF duration is not specified → provide parametric for 3, 5, 7, 10 years.

### Step 2: TID Calculation
```
TID = f(orbit, shielding_thickness, mission_duration, solar_cycle)
```
Dose-depth curve: run trapped proton + trapped electron + solar proton spectra through Al transport.

| Shielding (mm Al) | LEO 525 km SSO (krad/yr) | GEO (krad/yr) | MEO 20200 km (krad/yr) |
|--------------------|-------------------------|---------------|------------------------|
| 1 | 8-12 | 30-50 | 200-500 |
| 3 | 2-4 | 10-20 | 50-100 |
| 5 | 0.8-1.5 | 5-10 | 20-40 |
| 10 | 0.3-0.5 | 2-4 | 5-10 |
| 20 | 0.1-0.2 | 0.8-1.5 | 1-3 |

Solar proton contribution (95% confidence, per event): add 5-15 krad behind 3 mm Al for major SPE.

### Step 3: SEE Rate Estimation
1. Obtain integral LET spectrum for orbit (CREME96 or AP-9/AE-9 heavy ion module)
2. Identify part LET threshold (from radiation test data or manufacturer)
3. Calculate upset rate: `R = ∫ σ(LET) × dΦ/dLET × dLET` (Bendel/Petersen method)
4. Typical GEO SEU rates for SRAM: 10⁻⁷ to 10⁻⁵ upsets/bit/day
5. Typical LEO SEU rates for SRAM: 10⁻⁸ to 10⁻⁶ upsets/bit/day (SAA dominated)

### Step 4: Debris Collision Probability
```
P_collision = 1 - e^(-F × A × t)
```
Where:
- **F** = cumulative debris flux (impacts/m²/yr) for chosen size threshold
- **A** = spacecraft cross-sectional area (m²)
- **t** = mission duration (years)

For small P: `P ≈ F × A × t` (Poisson approximation when P < 0.1).

### Step 5: Atmospheric Drag (LEO only)
```
a_drag = -½ × ρ × v² × C_D × A/m
```
Where: ρ from NRLMSISE-00 (kg/m³), v = orbital velocity (m/s), C_D ≈ 2.2, A/m = area-to-mass ratio (m²/kg).

Orbit lifetime scales as: `τ ∝ (m / C_D × A) × (1/ρ)`

### Step 6: Shielding Trade Study
If structural skill available → Whipple shield mass optimization.
If power-systems skill available → solar array degradation vs shielding.
If xlsx skill available → parametric shielding trade spreadsheet.

---

### WORKED EXAMPLE: 5-year mission at 525 km SSO, 3 mm Al shielding

**Given:**
- Orbit: 525 km circular, 97.4° inclination (sun-synchronous)
- Duration: 5 years (2026-2031, ascending solar max)
- Shielding: 3 mm Al (0.81 g/cm²)
- Spacecraft area: 1 m² cross-section

**Radiation — TID:**
- Trapped protons (AP-9 median): 1.5 krad/yr behind 3 mm Al at 525 km SSO
- Trapped electrons (AE-9 median): 0.8 krad/yr behind 3 mm Al
- Solar protons (95% CL, ESP model): 1 major SPE in 5 years → 8 krad contribution
- GCR: negligible TID contribution (< 0.05 krad/yr)
- **Annual dose = 1.5 + 0.8 = 2.3 krad/yr**
- **5-year TID = 2.3 × 5 + 8 = 19.5 krad (Si)**
- **With design margin (RDM = 2): spec parts to 39 krad**
- Parts selection: commercial 100 krad parts → PASS. COTS (< 10 krad) → FAIL.

**Debris — Collision Probability:**
- Flux at 525 km for objects > 1 cm: F = 2.5 × 10⁻⁵ impacts/m²/yr (ORDEM 3.1)
- Flux at 525 km for objects > 1 mm: F = 0.015 impacts/m²/yr
- Cross-sectional area: A = 1 m²
- Duration: t = 5 years
- **P_lethal (> 1 cm) = 1 - e^(-2.5×10⁻⁵ × 1 × 5) = 1.25 × 10⁻⁴ (1 in 8,000)**
- **P_damage (> 1 mm) = 1 - e^(-0.015 × 1 × 5) = 0.072 (7.2%)**
- NASA requirement (NPR 8715.6): P_lethal < 0.001 per mission → 1.25 × 10⁻⁴ → PASS
- Consider Whipple shield for > 1 mm protection if mission-critical surfaces exposed.

**Atmospheric Drag (at 525 km):**
- ρ at solar max (F10.7 ≈ 180): ~1.5 × 10⁻¹³ kg/m³
- v = 7.59 km/s
- C_D = 2.2, A/m = 1/500 = 0.002 m²/kg (500 kg spacecraft)
- a_drag = ½ × 1.5×10⁻¹³ × (7590)² × 2.2 × 0.002 = 1.9 × 10⁻⁵ m/s²
- Altitude decay: ~0.5 km/yr at solar max conditions
- Station-keeping delta-v: ~3 m/s/yr
- Orbit lifetime without maintenance: > 25 years (compliant with 25-yr rule)

---

## 7. OUTPUT TEMPLATE

```markdown
# [Mission Name] — Space Environment Assessment

## Mission Parameters
| Parameter | Value |
|-----------|-------|
| Orbit | [alt] km × [alt] km, [inc]° |
| Duration | [X] years ([start]-[end]) |
| Solar Cycle Phase | [min/ascending/max/descending] |
| Shielding | [X] mm Al equivalent ([X] g/cm²) |
| Spacecraft Area | [X] m² (cross-section) |

## Radiation Environment
### Total Ionizing Dose
| Source | Annual Dose (krad/yr) | 5-Year Dose (krad) |
|--------|----------------------|---------------------|
| Trapped Protons | [X] | [X] |
| Trapped Electrons | [X] | [X] |
| Solar Protons (95% CL) | — | [X] (event) |
| **TOTAL** | **[X]** | **[X]** |
| **With RDM = 2** | — | **[X]** |

### Single Event Effects
| Part | LET_th (MeV·cm²/mg) | SEU Rate (/bit/day) | Mitigation |
|------|---------------------|---------------------|------------|
| [part] | [X] | [X] | [method] |

## Debris Risk
| Threshold | Flux (/m²/yr) | P_mission | Requirement | Status |
|-----------|---------------|-----------|-------------|--------|
| > 1 cm | [X] | [X] | < 0.001 | [PASS/FAIL] |
| > 1 mm | [X] | [X] | advisory | [value] |

## Atmospheric Drag
| Parameter | Value |
|-----------|-------|
| Density at altitude | [X] kg/m³ |
| Drag acceleration | [X] m/s² |
| Station-keeping Δv | [X] m/s/yr |
| Orbit lifetime (no maint.) | [X] years |

## Recommendation
[Shielding adequacy, parts selection, debris mitigation, drag strategy, next steps]
```

---

## 8. CLASSIFICATION

| Level | Name | Characteristics |
|-------|------|----------------|
| E1 | Benign LEO | < 600 km, < 5 yr, < 10 krad TID, minimal debris |
| E2 | Moderate LEO/SSO | 600-1000 km, 5-10 yr, 10-50 krad, elevated debris |
| E3 | Harsh MEO/HEO | Van Allen transit, 50-200 krad, SEE-intensive |
| E4 | GEO/Cislunar | Unshielded GCR+SPE, 20-100 krad, long duration |
| E5 | Interplanetary/Planetary Surface | Full GCR+SPE, 100+ krad, Mars surface 0.24 mSv/day |

---

## 9. VARIATIONS

- **A: LEO (< 600 km)** — Trapped protons dominate (SAA), moderate debris, significant drag below 500 km, 5-20 krad behind 3 mm Al for 5 yr, NRLMSISE-00 critical for lifetime
- **B: MEO / Van Allen Transit** — Peak radiation at L=1.5 (protons) and L=4-5 (electrons), 100-500 krad/yr behind 3 mm Al, rad-hard parts mandatory, debris flux minimal, shielding mass 10-30% of S/C dry mass
- **C: GEO** — Electron-dominated, diurnal charging/discharging, 10-20 krad/yr behind 3 mm Al, major SPE adds 10-30 krad per event, debris flux low but GEO protected zone rules apply (IADC)
- **D: Interplanetary** — Full unshielded GCR (0.5-1.0 mSv/day for crew), SPE acute risk (up to 1 Sv in hours without shelter), no debris concern, no drag, heliocentric distance modulates flux
- **E: Lunar Surface** — Half-sky GCR shielding by regolith, SPE shelter required (< 30 min warning), secondary neutrons from regolith, micrometeoroid flux 10⁻⁶ impacts/m²/yr at > 1 mm, dust plasma environment

---

## 10. ERRORS & PITFALLS

- **E1**: Using AP-8/AE-8 instead of AP-9/AE-9 (AP-8 underestimates protons at low altitude by 2-5x)
- **E2**: Ignoring Radiation Design Margin (RDM = 2 required by ECSS, parts must survive 2× predicted dose)
- **E3**: Assuming GCR is negligible for dose (true for TID, but GCR dominates SEE rates in LEO)
- **E4**: Spot shielding with high-Z only (Ta/W generate secondary neutrons and bremsstrahlung — graded Z better)
- **E5**: Using average debris flux for risk (spatial density peaks at 800-850 km are 3-5× the altitude average)
- **E6**: Ignoring solar cycle for drag (atmospheric density at 400 km varies 10× between solar min and max)
- **E7**: Treating collision probability as linear when P > 0.1 (must use exponential: P = 1 - e^(-F×A×t))
- **E8**: Confusing rad(Si) with rad(GaAs) — dose conversion factors differ by 1.5-2× for solar cells

---

## 11. TIPS

- **T1**: Start from orbit → look up flux → apply shielding → check parts — always in this order
- **T2**: For LEO < 800 km, trapped protons dominate TID; for GEO, electrons dominate — different shielding strategies
- **T3**: Use dose-depth curves, not single-point calculations — 1 mm more Al can halve electron dose at GEO
- **T4**: Polyethylene outperforms Al per g/cm² for proton shielding by ~30% (hydrogen-rich fragmentation)
- **T5**: SEE rates: test data trumps models — always request proton and heavy ion test reports from part vendors
- **T6**: Calibrate debris risk: ISS (400 km, 1000 m², 25 yr) has P > 0.5 for > 1 cm — they shield heavily
- **T7**: Margin: 2× on TID (ECSS), 10× on SEE rates (uncertainty), 1.5× on debris flux (model confidence)
- **T8**: Sanity check: LEO 500 km / 3 mm Al / 5 yr ≈ 10-20 krad. If your number is 200 krad, recheck orbit.

---

## 12. RELATED SKILLS

| Need | Skill | What It Adds |
|------|-------|-------------|
| Shield structure | **structural** | Whipple shield design, shielding mass allocation, MMOD bumper sizing |
| Solar array life | **power-systems** | Voc/Isc degradation curves vs fluence, cover glass thickness trades |
| Full system budget | **mission-architect** | Shielding mass roll-up, radiation-driven design life constraints |
| Orbit selection | **orbital-mechanics** | Altitude/inclination trades for radiation, drag, and debris |
| Drag compensation | **propulsion** | Station-keeping delta-v, collision avoidance maneuver budgets |
| Parts selection | **gnc** | Rad-hard processor selection, EDAC memory configuration |
| Trade spreadsheet | **xlsx** | Parametric shielding vs dose trade model with formulas |
| Review deck | **pptx** | PDR/CDR environment assessment presentations |
