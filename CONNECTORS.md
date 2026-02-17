# Connectors — Space Engineering Pack

## Shared Python Tools (all skills)

Python tools are in `shared/tools/` and available to all 12 skills. Run with:
```bash
python shared/tools/script_name.py subcommand --arg value
```

All tools output JSON for easy parsing.

### Tool Reference

| Tool | Subcommands | Purpose |
|------|-------------|---------|
| `trajectory.py` | `hohmann`, `tsiolkovsky`, `inverse`, `gravity-loss`, `delta-v-budget` | Trajectory analysis, delta-v calculations |
| `cost_estimator.py` | `engine`, `vehicle`, `launch`, `compare` | Cost estimation and vehicle comparison |
| `geometry.py` | `tank`, `fairing`, `vehicle-size` | Tank sizing, fairing checks, vehicle estimates |
| `plot.py` | `hohmann-plot`, `delta-v-waterfall`, `trade-matrix` | Visualizations (requires matplotlib) |
| `staging.py` | `optimize` | Staging optimization with SLSQP (requires scipy) |
| `timeline.py` | `plan`, `gantt` | Mission timeline generation and Gantt charts |

## Shared Data Layer

All skills can read from `shared/data/*.json`:
```python
# From any tool, access shared data:
SHARED_DATA = Path(__file__).resolve().parent.parent / "data"
vehicles = json.load(open(SHARED_DATA / "vehicles.json"))
```

## Data Freshness

Market data ages. Run the sync checker:
```bash
python shared/sync_data.py --check    # Check if data is stale
python shared/sync_data.py --force    # Force refresh via web search
```

Physics constants (`constants.py`) never expire.

## Cross-Skill Integration

Skills reference each other when relevant:
- Propulsion → calls orbital-mechanics for transfer delta-v
- Mission-architect → aggregates budgets from all subsystem skills
- Satellite-comms → uses orbital-mechanics for coverage geometry

## External Tool Integration

When available, these Claude Code skills enhance output:
| Skill | Enhancement |
|-------|------------|
| `xlsx` | Export budgets as Excel spreadsheets with formulas |
| `pptx` | Generate mission review presentations |
| `data` | Visualize trade study results |
| `pdf` | Create formal mission reports |
