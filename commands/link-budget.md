---
description: Satellite communications link budget — EIRP, G/T, C/N, margin calculation
argument-hint: "<orbit> <frequency_band> [data_rate]"
---

# /link-budget

Calculate satellite communication link budget.

## Usage

```
/link-budget LEO S-band 1Mbps
/link-budget GEO Ka-band 100Mbps
/link-budget "lunar orbit" X-band 10Mbps
```

## What Happens

1. **satellite-comms** skill calculates full link budget
2. EIRP, free space loss, atmospheric loss, G/T, C/N ratio
3. Link margin assessment (target: >3 dB for LEO, >6 dB for deep space)
4. Antenna sizing recommendation

> Requires **satellite-comms** skill.
