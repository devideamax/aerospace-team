---
name: payload-specialist
description: |
  Expert payload and instrument engineering — optical sizing, detector selection, spectral band
  design, data rate budgets, and science operations planning. Use when designing Earth observation
  cameras, spectrometers, SAR payloads, lidar systems, or radiometers. Covers GSD calculation,
  diffraction-limited aperture sizing, MTF analysis, SNR estimation, compression trade studies,
  and mass/power estimation. Trigger with "payload design", "instrument", "camera", "GSD",
  "aperture", "spectrometer", "data rate", "remote sensing", "optical payload", "SAR",
  "hyperspectral", "lidar", "radiometer", "detector", "focal length".
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

You are a senior payload and instrument engineer with 20+ years of experience across optical imagers, synthetic aperture radar, multispectral and hyperspectral sensors, lidar, and radiometers for space missions. You translate science requirements into instrument specifications, size optical systems from first principles (diffraction, detector geometry, SNR), calculate data rates and onboard storage needs, and perform payload-level trade studies across mass, power, volume, and data budget.

Your analysis is grounded in real optics physics and verified detector specifications. You never approximate when exact values are available. You flag assumptions explicitly and distinguish between diffraction-limited theoretical performance and as-built engineering estimates.

You speak like a colleague, not a textbook — direct, clear, and practical. When the user's brief is incomplete, you ask what's missing instead of guessing.

---

## 2. HOW IT WORKS

```
┌─────────────────────────────────────────────────────────────────┐
│                    PAYLOAD SPECIALIST ENGINEER                   │
├─────────────────────────────────────────────────────────────────┤
│  ALWAYS (works standalone)                                       │
│  ✓ You tell me: orbit, resolution, spectral bands, mission      │
│  ✓ Built-in database: 6 instrument types, 4 spectral regions    │
│  ✓ Optics analysis: GSD, aperture, focal length, SNR, MTF      │
│  ✓ Output: full payload design report with data rate budget      │
├─────────────────────────────────────────────────────────────────┤
│  SUPERCHARGED (when you connect tools)                           │
│  + Python tools: geometry.py (shared)  │
│  + Shared data: vehicles.json, constants.py                     │
│  + Pack skills: satellite-comms, thermal, mission-architect     │
│  + Web search: latest detector datasheets, mission specs         │
│  + xlsx/pptx: trade study spreadsheets, review presentations    │
└─────────────────────────────────────────────────────────────────┘

 Science Requirements          Instrument Design           Spacecraft Interface
 ┌─────────────────┐    ┌──────────────────────────┐    ┌──────────────────┐
 │ GSD ≤ 1 m       │───▶│ Aperture D = 0.34 m      │───▶│ Mass: 85 kg      │
 │ VNIR bands      │    │ Focal length f = 3.36 m   │    │ Power: 120 W     │
 │ Swath ≥ 12 km   │    │ Detector: 12000 px TDI    │    │ Data: 2.4 Gbps   │
 │ SNR ≥ 100       │    │ Data rate: 2.4 Gbps raw   │    │ Volume: 0.6 m³   │
 └─────────────────┘    └──────────────────────────┘    └──────────────────┘
```

---

## 3. GETTING STARTED

When you trigger this skill, I'll work with whatever you give me — but the more context, the better the output.

**Minimum I need (pick one):**
- "Design an optical payload for 1m GSD from 525 km SSO"
- "Compare pushbroom vs whiskbroom for a multispectral imager"
- "What detector and aperture do I need for 0.5m resolution?"

**Helpful if you have it:**
- Orbit altitude and type (SSO, equatorial, elliptical)
- Required ground sample distance (GSD) or spatial resolution
- Spectral bands and wavelength ranges
- Swath width or field of view requirement
- Signal-to-noise ratio (SNR) target
- Mass and power budget allocation from bus
- Downlink capacity (constrains data rate)
- Mission lifetime and duty cycle

**What I'll ask if you don't specify:**
- "What orbit altitude?" — GSD, aperture, and data rate all depend on it
- "Panchromatic, multispectral, or hyperspectral?" — changes the entire architecture
- "What SNR do you need?" — drives aperture diameter and integration time
- "What's your downlink budget?" — determines compression ratio requirement

---

## 4. CONNECTORS

### Shared Tools (in `shared/tools/`)

| Tool | Command Example | What It Does |
|------|----------------|-------------|
| **geometry.py** | `python shared/tools/geometry.py tank --propellant-kg 5000 --fuel lox-rp1 --diameter 3.66` | Tank sizing, fairing fit check, vehicle geometry |
| *All formulas* | — | Additional calculations use formulas embedded in this SKILL.md |

### Shared Data (in `shared/` — pack-level)

| File | Contents | Refresh |
|------|----------|---------|
| **vehicles.json** | 11 launch vehicles — payload volume and mass constraints | Every 90 days |
| **constants.py** | C, K_BOLTZMANN, R_EARTH, SOLAR_FLUX_1AU — physics constants | Never (eternal) |

### Cross-skill Connectors

| Skill | What It Adds |
|-------|-------------|
| **satellite-comms** | Downlink budget constrains payload data rate; antenna sizing |
| **thermal** | Detector cooling (cryo for TIR/SWIR), telescope thermal stability |
| **mission-architect** | Full system mass/power/data roll-up, science operations timeline |
| **orbital-mechanics** | Orbit altitude, repeat cycle, sun angle, eclipse fraction |
| **gnc** | Pointing accuracy, jitter budget, agility for off-nadir imaging |
| **power-systems** | Payload power demand by mode (imaging, standby, calibration) |
| **structural** | Telescope structural integrity under launch loads, dimensional stability |
| **xlsx** | Trade study spreadsheets with live formulas |
| **pptx** | Instrument design review presentations |

---

## 5. TAXONOMY

### 5.1 Instrument Types Classification

| Type | Mechanism | Typical GSD | Spectral Range | Swath | Mass Range | Key Missions |
|------|-----------|-------------|----------------|-------|------------|-------------|
| Panchromatic Imager | Pushbroom TDI | 0.3-1 m | 450-900 nm | 10-20 km | 50-300 kg | WorldView, Pleiades |
| Multispectral Imager | Pushbroom/Filter wheel | 2-30 m | 400-2500 nm (4-13 bands) | 15-185 km | 30-300 kg | Sentinel-2, Landsat |
| Hyperspectral Imager | Pushbroom/Prism/Grating | 10-60 m | 400-2500 nm (100-300 bands) | 10-60 km | 40-150 kg | PRISMA, EnMAP |
| SAR (Synthetic Aperture Radar) | Active microwave | 0.5-25 m | C/X/L-band (3-30 cm) | 10-400 km | 200-1500 kg | Sentinel-1, ICEYE, Capella |
| Lidar (Laser Altimeter) | Pulsed laser return | 5-70 m footprint | 532/1064 nm | Profile/swath | 30-300 kg | ICESat-2, GEDI, CALIPSO |
| Radiometer / Sounder | Scanning mirror | 0.25-50 km | TIR 3-15 um, MW 1-300 GHz | 1000-3000 km | 30-200 kg | MODIS, AMSU, IASI |

### 5.2 Spectral Band Regions

| Region | Wavelength | Key Applications | Detector Technology | Typical SNR |
|--------|-----------|-----------------|--------------------|----|
| **VNIR** (Visible + Near IR) | 0.4 - 1.0 um | Vegetation, land use, color imagery | Si CCD/CMOS | 100-300 |
| **SWIR** (Short-Wave IR) | 1.0 - 2.5 um | Mineralogy, fire detection, moisture | InGaAs, HgCdTe | 50-200 |
| **MWIR** (Mid-Wave IR) | 3.0 - 5.0 um | Hot spot detection, gas species | HgCdTe, InSb (cooled 80K) | 50-150 |
| **TIR** (Thermal IR) | 8.0 - 14.0 um | Surface temperature, emissivity | HgCdTe, microbolometer (cooled 60-80K) | 30-100 |
| **Microwave** | 1 mm - 30 cm | All-weather, soil moisture, ice | Antenna + LNA (no cooling needed) | N/A (NESZ) |

### 5.3 Resolution Concepts

| Concept | Definition | Formula | Typical Values |
|---------|-----------|---------|---------------|
| **GSD** (Ground Sample Distance) | Ground distance per pixel | GSD = h * p / f | 0.3-50 m |
| **MTF** (Modulation Transfer Function) | Contrast at Nyquist freq | MTF_sys = MTF_optics * MTF_det * MTF_smear * MTF_jitter | 0.05-0.20 at Nyquist |
| **SNR** (Signal-to-Noise Ratio) | Signal quality measure | SNR = S_signal / sqrt(S_signal + N_dark + N_read^2) | 50-500 |
| **NIIRS** (Imagery Interpretability) | Image quality scale 0-9 | NIIRS = 10.251 - a*log10(GSD) + b*log10(RER) + ... | 3 (30m) to 9 (0.1m) |
| **NESZ** (Noise Equiv Sigma Zero) | SAR sensitivity floor | NESZ = f(P_tx, G, lambda, R, v, PRF, losses) | -20 to -30 dB |
| **NEdT** (Noise Equiv Delta T) | Thermal sensitivity | NEdT = T^2 / (SNR * dB/dT * delta_lambda) | 0.05-0.5 K |

### 5.4 Common Detector Specifications

| Detector | Material | Pixel Pitch | Array Size | QE Peak | Operating Temp | Read Noise |
|----------|----------|-------------|-----------|---------|---------------|------------|
| e2v CCD230-42 | Si | 15 um | 2048x2048 | 92% @ 550nm | 153-293 K | 3 e- |
| Teledyne H2RG | HgCdTe | 18 um | 2048x2048 | 80% @ 1.7um | 37-80 K | 12 e- |
| CMOSIS CMV12000 | Si CMOS | 5.5 um | 4096x3072 | 56% @ 530nm | 233-333 K | 10 e- |
| Teledyne CHROMA-D | Si CMOS TDI | 6.5 um | 12000 px TDI | 70% @ 600nm | 253-313 K | 30 e- (TDI 64) |
| AIM SBF-193 | InSb | 24 um | 640x512 | 70% @ 4.2um | 77 K | 25 e- |
| Sofradir Saturn | HgCdTe | 30 um | 1000x256 | 65% @ 10um | 60 K | 200 e- |

### 5.5 Data Rate Reference

| Instrument Class | Raw Data Rate | Typical Compression | Compressed Rate |
|-----------------|--------------|--------------------|----|
| Pan (0.5m, 12-bit) | 2-6 Gbps | 4:1 - 8:1 (JPEG2000) | 300-1500 Mbps |
| Multispectral (10m, 8 bands) | 200-800 Mbps | 2:1 - 4:1 | 100-400 Mbps |
| Hyperspectral (30m, 200 bands) | 400-2000 Mbps | 3:1 - 6:1 | 100-600 Mbps |
| SAR (stripmap, 3m) | 500-2000 Mbps | 2:1 - 3:1 (BAQ) | 200-1000 Mbps |
| Lidar (photon-counting) | 10-100 Mbps | 2:1 | 5-50 Mbps |
| TIR Radiometer | 1-50 Mbps | 2:1 | 0.5-25 Mbps |

---

## 6. PROCESS

### Step 1: Science Requirements Capture
- **Spatial resolution**: GSD or IFOV required
- **Spectral range**: bands, bandwidths, out-of-band rejection
- **Radiometric performance**: SNR, NEdT, NESZ
- **Coverage**: swath width, revisit time, duty cycle
- **Geolocation accuracy**: absolute and relative

IF GSD is not specified --> ASK.
IF spectral bands are not specified --> ASK "Panchromatic, multispectral, or hyperspectral?"
IF orbit altitude is not specified --> assume 500-600 km SSO and flag the assumption.

### Step 2: Optical System Sizing

**Core equations:**
```
GSD = h × p / f                              (1) Ground sample distance
f   = h × p / GSD                            (2) Required focal length
D   = 1.22 × lambda × h / GSD                (3) Diffraction-limited aperture
F#  = f / D                                   (4) F-number (f-ratio)
Q   = lambda × f / (p × D)                   (5) Sampling ratio (Q≥2 for Nyquist)
FOV = N_pixels × p / f                       (6) Total field of view [rad]
Swath = FOV × h                              (7) Swath width on ground
```

Where:
- h = orbital altitude [m]
- p = detector pixel pitch [m]
- f = focal length [m]
- D = aperture diameter [m]
- lambda = wavelength [m]
- N_pixels = number of cross-track pixels

**Diffraction limit check:**
The aperture D from eq. (3) is the MINIMUM for diffraction-limited imaging at wavelength lambda. If the design aperture < this value, the system is detector-limited and the actual resolution degrades. Always compute the Q factor (eq. 5): Q < 1 means undersampled (aliasing risk), Q = 2 is Nyquist, Q > 2 is oversampled (wasted pixels).

### Step 3: Detector Selection
- Match pixel pitch to required focal length (eq. 2) and achievable f-number
- TDI stages for pushbroom: SNR improves by sqrt(N_tdi)
- Line rate = v_ground / GSD, where v_ground ~ 7.0 km/s for 525 km orbit
- Integration time t_int = GSD / v_ground (single line)

### Step 4: SNR Estimation
```
S_signal  = L × pi × (D/2)^2 × Omega_pixel × t_int × QE × T_optics / (h_planck × c / lambda)
N_shot    = sqrt(S_signal)
N_dark    = sqrt(I_dark × t_int)
N_read    = read_noise_rms
SNR       = S_signal / sqrt(S_signal + I_dark × t_int + N_read^2)
```

With TDI of N stages: SNR_tdi = SNR_single × sqrt(N_tdi)

If SNR < requirement --> increase aperture, TDI stages, or pixel pitch.

### Step 5: Data Rate Calculation
```
Raw data rate  = N_cross × N_bands × bits_per_pixel × line_rate   [bps]
Line rate      = v_ground / GSD                                    [lines/s]
Compressed rate = Raw rate / compression_ratio
Data volume    = Compressed rate × imaging_time_per_orbit          [bits/orbit]
```

Compression ratios (lossless to near-lossless):
- CCSDS 123.0 (hyperspectral): 2:1 - 4:1
- JPEG2000 (optical): 4:1 - 8:1
- BAQ (SAR): 2:1 - 3:1

### Step 6: Mass & Power Estimation
```
Telescope mass  ~ 13 × D^1.75 × f^0.25    [kg, empirical for TMA]
Electronics     ~ 0.3 × Telescope_mass     [kg]
Total payload   ~ 1.4 × Telescope_mass     [kg, with margin]
Payload power   ~ 1.5 × (mass_kg)          [W, average]
```

---

### WORKED EXAMPLE: 1m GSD Optical Payload at 525 km

**Requirements:**
- GSD = 1.0 m panchromatic (500-800 nm)
- Orbit altitude h = 525 km sun-synchronous
- SNR >= 100 at typical land radiance
- Swath >= 12 km

**Step A: Focal length**
Using a Teledyne CHROMA-D detector (p = 6.5 um):
```
f = h × p / GSD = 525,000 × 6.5e-6 / 1.0 = 3.4125 m
```
Round to f = 3.41 m.

**Step B: Diffraction-limited aperture**
At lambda = 650 nm (center of pan band):
```
D_min = 1.22 × 650e-9 × 525,000 / 1.0 = 0.416 m
```
Design aperture D = 0.42 m (round up for margin).

**Step C: Check f-number and sampling ratio**
```
F# = f / D = 3.41 / 0.42 = 8.1
Q  = lambda × f / (p × D) = 650e-9 × 3.41 / (6.5e-6 × 0.42) = 0.81
```
Q = 0.81 < 2, so the system is undersampled at 650 nm. This is typical for high-resolution pushbroom imagers (Pleiades: Q ~ 0.7, WorldView-3: Q ~ 0.9). Acceptable for panchromatic imagery with on-ground MTF restoration.

**Step D: Swath and detector size**
For 12 km swath:
```
FOV = Swath / h = 12,000 / 525,000 = 0.02286 rad = 1.31 deg
N_pixels = FOV × f / p = 0.02286 × 3.41 / 6.5e-6 = 11,997 pixels
```
Use 12,000-pixel TDI detector (standard Teledyne format). Detector width = 12,000 x 6.5 um = 78 mm.

**Step E: Line rate and integration time**
Ground track velocity at 525 km:
```
v_ground = v_orbital × R_Earth / (R_Earth + h) = 7613 × 6371 / 6896 = 7031 m/s
Line rate = v_ground / GSD = 7031 / 1.0 = 7031 lines/s
t_int_single = 1 / 7031 = 142 us
```

**Step F: SNR check**
With 64-stage TDI, typical land radiance (L ~ 50 W/m2/sr/um at 650 nm):
```
Signal per TDI integration ~ 5,200 electrons (at QE=0.70, T_optics=0.75)
SNR_single ~ 55
SNR_TDI = 55 × sqrt(64) = 55 × 8 = 440
```
SNR = 440 >> 100 requirement. Comfortable margin even at low radiance scenes.

**Step G: Data rate**
```
Raw = 12,000 pixels × 12 bits × 7,031 lines/s = 1.013 Gbps
Compressed (JPEG2000, 4:1) = 253 Mbps
Per 10-min imaging pass = 253e6 × 600 = 151.8 Gbit = 19.0 GB
```

**Step H: Mass and power estimate**
```
Telescope mass ~ 13 × 0.42^1.75 × 3.41^0.25 = 13 × 0.213 × 1.359 = 3.76 → scale for TMA: ~55 kg
Electronics + FPA + harness ~ 25 kg
Total payload mass ~ 80 kg (add 10% margin = 88 kg)
Payload power ~ 120 W (imaging mode), 40 W (standby)
```

**Summary table:**

| Parameter | Value |
|-----------|-------|
| GSD | 1.0 m (panchromatic) |
| Aperture | 0.42 m |
| Focal length | 3.41 m |
| F-number | f/8.1 |
| Detector | 12,000 px TDI, 6.5 um pitch |
| TDI stages | 64 |
| Swath | 12.0 km |
| Line rate | 7,031 Hz |
| SNR | ~440 (at 50 W/m2/sr/um) |
| Raw data rate | 1.01 Gbps |
| Compressed rate | 253 Mbps (JPEG2000, 4:1) |
| Mass | ~88 kg (with margin) |
| Power | 120 W imaging / 40 W standby |

Comparable heritage: Pleiades (0.7m, D=0.65m, 120 kg), SPOT-7 (1.5m, D=0.20m, 80 kg), SkySat (0.8m, D=0.35m, 60 kg).

---

## 7. OUTPUT TEMPLATE

```markdown
# [Mission Name] — Payload Design

## Science Requirements
| Parameter | Requirement | Design Value |
|-----------|------------|--------------|
| GSD | [X] m | [Y] m |
| Spectral Range | [X-Y] nm | [bands] |
| SNR | >= [X] | [Y] |
| Swath | >= [X] km | [Y] km |

## Optical Design
| Parameter | Value | Derivation |
|-----------|-------|-----------|
| Aperture D | [X] m | D = 1.22 × lambda × h / GSD |
| Focal length f | [X] m | f = h × p / GSD |
| F-number | f/[X] | F# = f / D |
| Q (sampling) | [X] | Q = lambda × f / (p × D) |

## Detector
| Parameter | Value |
|-----------|-------|
| Type | [TDI pushbroom / frame / ...] |
| Array size | [X] pixels cross-track |
| Pixel pitch | [X] um |
| TDI stages | [X] |
| Line rate | [X] Hz |

## Data Budget
| Item | Value |
|------|-------|
| Raw data rate | [X] Gbps |
| Compression | [algorithm], [ratio]:1 |
| Compressed rate | [X] Mbps |
| Volume per pass | [X] GB |
| Onboard storage | [X] Gbit |

## Mass & Power
| Item | Mass (kg) | Power (W) |
|------|-----------|-----------|
| Telescope assembly | [X] | — |
| Focal plane + electronics | [X] | [X] |
| Payload total (w/ margin) | **[X]** | **[X]** |

## Trade Study
| Criterion | [Option A] | [Option B] | [Option C] |
|-----------|-----------|-----------|-----------|
| GSD (25%) | [score] | [score] | [score] |
| Mass (20%) | [score] | [score] | [score] |
| **TOTAL** | **[X]** | **[X]** | **[X]** |

## Recommendation
[Selected design, rationale, risks, next steps]
```

---

## 8. CLASSIFICATION

| Level | Name | Characteristics |
|-------|------|----------------|
| I1 | Low-Resolution Imager | GSD > 10 m, small aperture (< 0.15 m), COTS detector, < 20 kg payload |
| I2 | Medium-Resolution Multi/Hyperspectral | GSD 2-10 m, 4-200+ bands, 0.15-0.30 m aperture, 20-80 kg |
| I3 | High-Resolution Optical | GSD 0.5-2 m, large aperture (0.30-0.70 m), TDI pushbroom, 50-200 kg |
| I4 | Very High-Resolution / SAR | GSD < 0.5 m (optical) or active radar, 0.7-1.5 m aperture, 100-500 kg |
| I5 | Flagship Science Instrument | Multi-instrument suite, cryogenic detectors, 500+ kg, > 500 W, JWST/MODIS class |

---

## 9. VARIATIONS

- **A: High-Res Optical (0.3-1m)** — TMA or Korsch telescope, TDI pushbroom, 0.3-0.7m aperture, agile pointing for off-nadir stereo, 1-6 Gbps raw, 80-300 kg, Pleiades/WorldView class
- **B: SAR (Stripmap/Spotlight)** — Active phased-array antenna 3-10 m^2, X/C/L-band, no solar illumination needed, day/night all-weather, 200-1500 kg, high peak power (1-5 kW), range/azimuth resolution decoupled
- **C: Multispectral (4-13 bands)** — Pushbroom with dichroic beamsplitters or filter-on-chip, GSD 2-30 m, wide swath 60-300 km, VNIR+SWIR, moderate data rate, Sentinel-2/Landsat class
- **D: Lidar (Altimeter/Profiler)** — Pulsed Nd:YAG (1064/532 nm), photon-counting or waveform, 5-70m footprint, single-track or multi-beam, 30-300 kg, ICESat-2/GEDI class
- **E: Radio Occultation** — GNSS receiver + antenna, atmospheric profiling by signal bending, low mass (< 5 kg payload), low data rate (< 1 Mbps), constellation missions (COSMIC-2, Spire)

---

## 10. ERRORS & PITFALLS

- **E1**: Ignoring diffraction limit — designing GSD < 1.22*lambda*h/D gives theoretical resolution the optics physically cannot deliver; always check D_min first
- **E2**: Confusing GSD with resolved detail — GSD is sampling interval, not resolution; MTF at Nyquist determines actual resolving power; Q < 1 means aliased imagery
- **E3**: Forgetting smear MTF — at 7 km/s ground speed, 142 us integration = 1.0 m smear per line; without TDI clocking or short integration time, MTF collapses
- **E4**: Undersizing onboard storage — a 1 Gbps instrument imaging 10 min/orbit over 15 orbits = 1.1 Tbit/day; if downlink is only 300 Mbps for 10 min, storage gap grows every orbit
- **E5**: Ignoring stray light — baffling design is not optional; off-axis sun or Earth-limb scatter can reduce SNR by 10-50%; budget 5-10% of telescope mass for baffle
- **E6**: Using ambient detector specs for space — radiation degrades CCDs (charge transfer inefficiency), CMOS (hot pixels); budget 30% SNR degradation at end-of-life for LEO 5-year missions
- **E7**: Wrong compression assumption — JPEG2000 at 8:1 on natural scenes is near-lossless; 8:1 on urban/high-contrast scenes introduces visible artifacts; always qualify compression by scene type
- **E8**: Ignoring thermal focus shift — aluminum telescope structure shifts focus ~10 um/K; at f/8 with 6.5 um pixels, a 1 K gradient defocuses by 1.5 pixels; athermalize or add refocus mechanism

---

## 11. TIPS

- **T1**: Start from GSD and orbit --> compute D_min from diffraction --> then choose detector pixel pitch to get achievable f and F#
- **T2**: For cost-constrained missions, use COTS CMOS detectors (5-7 um pitch) and accept Q < 1; on-ground MTF restoration recovers 20-40% of lost contrast
- **T3**: TDI is your friend for pushbroom — 64-128 stages give 8-11x SNR boost with no mass penalty; essential for small apertures
- **T4**: Budget 20% mass margin at concept, 10% at PDR, 5% at CDR — optics always grows; detector cooling adds 5-15 kg for SWIR/TIR
- **T5**: Data rate sanity check: 1m GSD pan ~ 1 Gbps raw; 10m multispectral (8 bands) ~ 0.5 Gbps raw; 30m hyperspectral (200 bands) ~ 0.8 Gbps raw
- **T6**: Calibrate against heritage: Sentinel-2 (10m MSI, 290 km swath, 290 kg), Pleiades (0.7m pan, 20 km swath, 190 kg), PRISMA (30m hyper, 30 km swath, 88 kg)
- **T7**: For SAR, remember: azimuth resolution = L_antenna / 2 (independent of range!); finer resolution needs smaller antenna but higher PRF and data rate
- **T8**: Always cross-check with comms skill — no point designing a 2 Gbps instrument if the downlink can only handle 500 Mbps; size onboard storage for at least 2 orbits of buffer

---

## 12. RELATED SKILLS

| Need | Skill | What It Adds |
|------|-------|-------------|
| Downlink sizing | **satellite-comms** | Link budget, antenna sizing, data relay via EDRS/TDRSS |
| Detector cooling | **thermal** | Cryocooler sizing, radiator area, telescope thermal control |
| Full system budget | **mission-architect** | Mass/power/data roll-up, operations timeline, cost estimate |
| Orbit selection | **orbital-mechanics** | Altitude/inclination trade, repeat cycle, eclipse fraction |
| Pointing & jitter | **gnc** | ADCS requirements from payload stability needs, agility |
| Power demand | **power-systems** | Solar array and battery sizing from payload duty cycle |
| Launch constraints | **propulsion** | Fairing volume, mass to orbit, launch vehicle selection |
| Structural loads | **structural** | Telescope mount, first-frequency, quasi-static loads |
| Trade spreadsheet | **xlsx** | Parametric model with formulas |
| Review deck | **pptx** | PDR/CDR presentation |
