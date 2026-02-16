"""Data Sync — Refreshes market data (prices, vehicle specs, new vehicles).
Physics constants are NOT here — they don't change.

Usage:
    python sync_data.py                  # Check if update needed
    python sync_data.py --force          # Force refresh regardless of age
    python sync_data.py --check          # Only check age, don't sync
    python sync_data.py --stamp          # Update timestamp after manual edit

How it works:
    1. Reads data/*.json metadata (last_updated, update_interval_days)
    2. If data is older than interval → prints search queries for Claude
    3. Claude runs web searches, updates JSON, then runs --stamp
    4. Old version backed up to data/vehicles_YYYY-MM-DD.json
"""
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_FILES = {
    "vehicles": {"file": "vehicles.json", "interval_days": 90},
    "engines": {"file": "vehicles.json", "interval_days": 90, "section": "engines"},
}


def load_json(filename):
    filepath = DATA_DIR / filename
    if not filepath.exists():
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def check_freshness():
    results = {}
    for name, cfg in DATA_FILES.items():
        data = load_json(cfg["file"])
        if not data:
            results[name] = {"status": "MISSING", "file": cfg["file"]}
            continue
        meta = data.get("_meta", {})
        last_updated = meta.get("last_updated", "2020-01-01")
        interval = cfg.get("interval_days", meta.get("update_interval_days", 90))
        last_date = datetime.strptime(last_updated, "%Y-%m-%d")
        age_days = (datetime.now() - last_date).days
        stale = age_days > interval
        section = cfg.get("section")
        count = len(data.get(section or name, data.get("vehicles", {})))
        results[name] = {
            "file": cfg["file"],
            "last_updated": last_updated,
            "age_days": age_days,
            "interval_days": interval,
            "stale": stale,
            "count": count,
            "action": "UPDATE RECOMMENDED" if stale else "Fresh",
        }
    return results


def backup_file(filename):
    filepath = DATA_DIR / filename
    if filepath.exists():
        data = load_json(filename)
        date_str = data.get("_meta", {}).get("last_updated", "unknown")
        backup_name = f"{filepath.stem}_{date_str}{filepath.suffix}"
        backup_path = DATA_DIR / backup_name
        if not backup_path.exists():
            shutil.copy2(filepath, backup_path)
            return str(backup_path)
    return None


def stamp_file(filename):
    filepath = DATA_DIR / filename
    data = load_json(filename)
    if data and "_meta" in data:
        data["_meta"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return data["_meta"]["last_updated"]
    return None


def generate_search_queries():
    data = load_json("vehicles.json")
    if not data:
        return []
    queries = []
    for key, v in data.get("vehicles", {}).items():
        name = v.get("name", key)
        queries.append({
            "vehicle": key,
            "query": f"{name} launch cost 2026 payload capacity",
            "fields": ["launch_cost_m", "payload_leo_kg", "payload_gto_kg", "flights_2025", "status"],
        })
    queries.append({
        "vehicle": "_new",
        "query": "new orbital launch vehicles 2025 2026 first flight",
        "fields": ["Add any new vehicles not in database"],
    })
    return queries


if __name__ == "__main__":
    force = "--force" in sys.argv
    check_only = "--check" in sys.argv
    stamp = "--stamp" in sys.argv

    if stamp:
        for cfg in DATA_FILES.values():
            backup = backup_file(cfg["file"])
            new_date = stamp_file(cfg["file"])
            print(json.dumps({"file": cfg["file"], "backup": backup, "new_timestamp": new_date}, indent=2))
        sys.exit(0)

    freshness = check_freshness()
    print(json.dumps(freshness, indent=2))

    if check_only:
        sys.exit(0)

    any_stale = any(v.get("stale") for v in freshness.values())
    if any_stale or force:
        print("\n--- DATA IS STALE. Refresh needed. ---")
        queries = generate_search_queries()
        for q in queries:
            print(f"\n  Vehicle: {q['vehicle']}")
            print(f"  Search:  {q['query']}")
            print(f"  Update:  {', '.join(q['fields'])}")
        print(f"\nAfter updating data files, run: python sync_data.py --stamp")
    else:
        print("\nAll data is fresh. No update needed.")
