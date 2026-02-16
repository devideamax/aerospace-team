---
description: Full mission architecture — from requirements to vehicle selection, delta-v budget, staging, and cost estimate
argument-hint: "<destination> <payload_kg>"
---

# /mission-design

Run a complete mission design workflow using the space-engineering pack.

## Usage

```
/mission-design Mars 5000
/mission-design LEO 22800 --reusable
/mission-design "lunar surface" 2000
```

## What Happens

1. **propulsion** skill builds delta-v budget and selects engines
2. **cost_estimator.py** calculates launch cost options
3. **geometry.py** sizes tanks and checks fairing fit
4. Output: full Mission Architecture Report

## Optional Enhancements

- Add `--reusable` for reusable booster analysis
- Add `--compare` to see 3+ vehicle options side by side
- If `xlsx` skill is loaded → generates trade study spreadsheet
- If `pptx` skill is loaded → generates review presentation
