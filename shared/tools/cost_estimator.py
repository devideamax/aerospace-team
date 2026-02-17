"""Rocket Cost Estimator — Shared tool for space-engineering pack.
Based on TRANSCOST parametric model and industry cost data.

Usage:
    python cost_estimator.py engine --thrust-kn 2000 --cycle staged --heritage new
    python cost_estimator.py vehicle --glow-tonnes 550 --stages 2 --reusable --flights-per-year 15
    python cost_estimator.py launch --payload-kg 22800 --orbit LEO --vehicle falcon9
    python cost_estimator.py compare --vehicles falcon9 electron starship
"""
import argparse
import json
import math
import sys
from pathlib import Path

# Shared data: ../data/vehicles.json (sibling directory)
SHARED_DATA = Path(__file__).resolve().parent.parent / "data"
# Fallback: local data/ if shared not found
LOCAL_DATA = Path(__file__).parent / "data"


def _find_data_file(filename):
    shared = SHARED_DATA / filename
    if shared.exists():
        return shared
    local = LOCAL_DATA / filename
    if local.exists():
        return local
    return None


def _load_vehicles():
    filepath = _find_data_file("vehicles.json")
    if filepath:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        meta = data.get("_meta", {})
        vehicles = {}
        for key, v in data.get("vehicles", {}).items():
            vehicles[key] = {
                "name": v.get("name", key),
                "launch_cost_m": v.get("launch_cost_m", 0),
                "payload_leo_kg": v.get("payload_leo_kg", 0),
                "payload_gto_kg": v.get("payload_gto_kg", 0),
                "reusable": v.get("reusable", False),
                "flights_per_year": v.get("flights_2025", v.get("flights_per_year", 1)),
                "cost_per_kg_leo": round(v["launch_cost_m"] * 1e6 / v["payload_leo_kg"], 0) if v.get("payload_leo_kg", 0) > 0 else 0,
            }
        return vehicles, meta.get("last_updated", "unknown")
    return {
        "falcon9": {"name": "Falcon 9", "launch_cost_m": 67, "payload_leo_kg": 22800, "payload_gto_kg": 8300, "reusable": True, "flights_per_year": 90, "cost_per_kg_leo": 2940},
    }, "fallback"


VEHICLES, _DATA_DATE = _load_vehicles()

ENGINE_DEV_BASE = {
    "pressure_fed": 0.5e9,
    "gas_generator": 1.2e9,
    "expander": 1.5e9,
    "staged": 2.5e9,
    "full_flow": 4.0e9,
}
HERITAGE_FACTOR = {"new": 1.0, "derivative": 0.4, "upgrade": 0.2}
THRUST_SCALE_EXP = 0.55


def engine_cost(thrust_kn, cycle, heritage="new"):
    cycle_key = cycle.lower().replace("-", "_").replace(" ", "_")
    if cycle_key not in ENGINE_DEV_BASE:
        return {"error": f"Unknown cycle. Available: {list(ENGINE_DEV_BASE.keys())}"}
    h = HERITAGE_FACTOR.get(heritage.lower(), 1.0)
    base = ENGINE_DEV_BASE[cycle_key]
    thrust_factor = (thrust_kn / 1000) ** THRUST_SCALE_EXP
    dev_cost = base * thrust_factor * h
    unit_cost_first = dev_cost * 0.005
    unit_cost_100th = unit_cost_first * 0.35
    return {
        "development_cost_usd": round(dev_cost),
        "development_cost_b": round(dev_cost / 1e9, 2),
        "unit_cost_first_m": round(unit_cost_first / 1e6, 1),
        "unit_cost_100th_m": round(unit_cost_100th / 1e6, 1),
        "thrust_kn": thrust_kn,
        "cycle": cycle,
        "heritage": heritage,
        "note": "TRANSCOST parametric estimate, +/-50% accuracy",
    }


def vehicle_cost(glow_tonnes, stages, reusable=False, flights_per_year=10):
    prod_base = glow_tonnes ** 0.65 * 2e6
    prod_cost = prod_base * stages * 0.8
    if reusable:
        prod_cost *= 1.3
        refurb_per_flight = prod_cost * 0.05
        amortized_vehicle = prod_cost / 20
        ops_per_flight = 2e6 + glow_tonnes * 500
        cost_per_flight = amortized_vehicle + refurb_per_flight + ops_per_flight
    else:
        cost_per_flight = prod_cost + 2e6 + glow_tonnes * 500
    annual_cost = cost_per_flight * flights_per_year
    return {
        "vehicle_production_m": round(prod_cost / 1e6, 1),
        "cost_per_flight_m": round(cost_per_flight / 1e6, 1),
        "annual_cost_m": round(annual_cost / 1e6, 1),
        "reusable": reusable,
        "flights_per_year": flights_per_year,
        "glow_tonnes": glow_tonnes,
        "stages": stages,
        "note": "Parametric estimate, +/-30% accuracy",
    }


KNOWN_ORBITS = ["LEO", "GTO", "GEO"]


def launch_cost(payload_kg, orbit="LEO", vehicle=None):
    if payload_kg <= 0:
        return {"error": f"Payload must be > 0 kg (got {payload_kg})"}
    if orbit.upper() not in KNOWN_ORBITS:
        return {"error": f"Unknown orbit '{orbit}'. Available: {KNOWN_ORBITS}"}
    if vehicle:
        v = VEHICLES.get(vehicle.lower().replace(" ", "_").replace("-", "_"))
        if not v:
            return {"error": f"Unknown vehicle. Available: {list(VEHICLES.keys())}"}
        key = "payload_leo_kg" if orbit.upper() == "LEO" else "payload_gto_kg"
        max_payload = v[key]
        if payload_kg > max_payload:
            return {"error": f"Payload {payload_kg}kg exceeds {v['name']} capacity of {max_payload}kg to {orbit}"}
        cost_per_kg = v["launch_cost_m"] * 1e6 / payload_kg
        return {
            "vehicle": v["name"],
            "launch_cost_m": v["launch_cost_m"],
            "payload_kg": payload_kg,
            "orbit": orbit.upper(),
            "cost_per_kg": round(cost_per_kg, 0),
            "utilization_pct": round(payload_kg / max_payload * 100, 1),
        }
    results = []
    for key, v in VEHICLES.items():
        cap = v["payload_leo_kg"] if orbit.upper() == "LEO" else v.get("payload_gto_kg", 0)
        if cap >= payload_kg and cap > 0:
            cpk = v["launch_cost_m"] * 1e6 / payload_kg
            results.append({
                "vehicle": v["name"],
                "launch_cost_m": v["launch_cost_m"],
                "cost_per_kg": round(cpk, 0),
                "utilization_pct": round(payload_kg / cap * 100, 1),
            })
    results.sort(key=lambda x: x["cost_per_kg"])
    return {
        "payload_kg": payload_kg,
        "orbit": orbit.upper(),
        "options": results[:5],
        "cheapest": results[0]["vehicle"] if results else "No vehicle found",
    }


def compare_vehicles(vehicle_names):
    rows = []
    for name in vehicle_names:
        key = name.lower().replace(" ", "_").replace("-", "_")
        v = VEHICLES.get(key)
        if v:
            rows.append(v)
        else:
            rows.append({"name": name, "error": "Not found"})
    return {"comparison": rows, "available_vehicles": list(VEHICLES.keys())}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rocket Cost Estimator")
    sub = parser.add_subparsers(dest="command")

    p_e = sub.add_parser("engine")
    p_e.add_argument("--thrust-kn", type=float, required=True)
    p_e.add_argument("--cycle", required=True)
    p_e.add_argument("--heritage", default="new")

    p_v = sub.add_parser("vehicle")
    p_v.add_argument("--glow-tonnes", type=float, required=True)
    p_v.add_argument("--stages", type=int, required=True)
    p_v.add_argument("--reusable", action="store_true")
    p_v.add_argument("--flights-per-year", type=int, default=10)

    p_l = sub.add_parser("launch")
    p_l.add_argument("--payload-kg", type=float, required=True)
    p_l.add_argument("--orbit", default="LEO")
    p_l.add_argument("--vehicle", default=None)

    p_c = sub.add_parser("compare")
    p_c.add_argument("--vehicles", nargs="+", required=True)

    args = parser.parse_args()
    if args.command == "engine":
        result = engine_cost(args.thrust_kn, args.cycle, args.heritage)
    elif args.command == "vehicle":
        result = vehicle_cost(args.glow_tonnes, args.stages, args.reusable, args.flights_per_year)
    elif args.command == "launch":
        result = launch_cost(args.payload_kg, args.orbit, args.vehicle)
        if "error" in result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            sys.exit(1)
    elif args.command == "compare":
        result = compare_vehicles(args.vehicles)
    else:
        parser.print_help()
        sys.exit(0)
    print(json.dumps(result, indent=2, ensure_ascii=False))
