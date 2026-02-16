---
description: Plan orbital trajectory — Hohmann transfers, launch windows, delta-v requirements
argument-hint: "<from> <to>"
---

# /orbit-plan

Calculate orbital transfers and trajectory requirements.

## Usage

```
/orbit-plan Earth Mars
/orbit-plan LEO GEO
/orbit-plan Earth Jupiter
```

## What Happens

1. Runs `trajectory.py hohmann` for interplanetary transfers
2. Calculates departure/arrival delta-v and transfer time
3. Builds complete delta-v budget including losses
4. When **orbital-mechanics** skill is available → adds launch window analysis
