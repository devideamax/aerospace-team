---
description: Side-by-side comparison of launch vehicles — cost, payload, reusability
argument-hint: "<vehicle1> <vehicle2> [vehicle3...]"
---

# /vehicle-comparison

Compare launch vehicles from the shared database.

## Usage

```
/vehicle-comparison falcon9 starship new_glenn
/vehicle-comparison electron h3 ariane6
```

## What Happens

1. Reads `shared/data/vehicles.json` for current specs and costs
2. Builds comparison table: payload LEO/GTO, cost, cost/kg, reusability, flight rate
3. Ranks by cost-effectiveness for your payload class

## Available Vehicles

falcon9, falcon_heavy, starship, electron, neutron, ariane6, vulcan, new_glenn, sls, long_march_5, h3
