---
description: Calculate launch cost for a payload to orbit — find cheapest vehicle or analyze specific one
argument-hint: "<payload_kg> [orbit] [--vehicle name]"
---

# /launch-cost

Quick cost analysis for getting payload to orbit.

## Usage

```
/launch-cost 5000 LEO
/launch-cost 3000 GTO --vehicle falcon9
/launch-cost 500 LEO
```

## What Happens

1. Runs `cost_estimator.py launch` with your parameters
2. If no vehicle specified → finds top 5 cheapest options
3. Shows cost per kg, utilization %, and total launch cost
4. Data source: `shared/data/vehicles.json` (refreshed every 90 days)
