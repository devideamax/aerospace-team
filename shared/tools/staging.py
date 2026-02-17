"""Staging Optimizer — Shared tool for space-engineering pack.

Finds optimal delta-v split across stages to minimize GLOW.

Usage:
    python staging.py optimize --delta-v 9.4 --stages 2 --isp 282,348 --structural-fraction 0.06,0.08 --payload-kg 22800
    python staging.py optimize --delta-v 9.4 --stages 2 --engine merlin_1d,rl10c --payload-kg 5000
"""
import argparse
import json
import math
import sys
import os

G0 = 9.80665  # m/s²

SHARED_DATA = os.path.join(os.path.dirname(__file__), "..", "data")


def _load_engines():
    filepath = os.path.join(SHARED_DATA, "vehicles.json")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("engines", {})
    return {}


def _stage_mass(dv_kms, isp, sf, payload_kg):
    """Calculate stage masses given delta-v, Isp, structural fraction, payload."""
    dv = dv_kms * 1000
    mass_ratio = math.exp(dv / (isp * G0))

    # m_initial / m_final = mass_ratio
    # m_final = m_structure + m_payload_above
    # m_structure = sf * (m_structure + m_propellant)
    # => m_propellant = m_payload * (mass_ratio - 1) * (1 - sf) / (1 - mass_ratio * sf)
    denominator = 1 - mass_ratio * sf
    if denominator == 0 or denominator > 0:
        # For feasible cases, denominator should be negative (mass_ratio * sf < 1 is normal)
        pass
    propellant = payload_kg * (mass_ratio - 1) * (1 - sf) / (1 - mass_ratio * sf)
    if propellant < 0:
        return None  # Infeasible
    structure = sf * propellant / (1 - sf)
    wet = propellant + structure + payload_kg
    dry = structure + payload_kg
    return {
        "propellant_kg": propellant,
        "structure_kg": structure,
        "wet_kg": wet,
        "dry_kg": dry,
        "mass_ratio": mass_ratio,
    }


def _compute_glow(dv_split, isps, sfs, payload_kg):
    """Compute GLOW for a given delta-v split (top-down: last stage first)."""
    n = len(dv_split)
    payload_above = payload_kg
    stages = []
    for i in range(n - 1, -1, -1):  # From top stage down
        result = _stage_mass(dv_split[i], isps[i], sfs[i], payload_above)
        if result is None:
            return float("inf"), []
        stages.insert(0, result)
        payload_above = result["wet_kg"]
    glow = stages[0]["wet_kg"] if stages else float("inf")
    return glow, stages


def optimize_staging(total_dv_kms, n_stages, isps, sfs, payload_kg):
    """Find optimal delta-v split to minimize GLOW."""
    if len(isps) != n_stages or len(sfs) != n_stages:
        return {"error": f"Must provide {n_stages} Isp and structural-fraction values"}
    if payload_kg <= 0:
        return {"error": "Payload must be > 0 kg"}
    if total_dv_kms <= 0:
        return {"error": "Delta-v must be > 0 km/s"}

    # Check if all Isp equal — use analytical equal split
    all_equal_isp = all(abs(isp - isps[0]) < 0.1 for isp in isps)

    if all_equal_isp:
        # Equal split is optimal for equal Isp
        optimal_split = [total_dv_kms / n_stages] * n_stages
        method = "analytical (equal Isp)"
    else:
        # Numerical optimization with scipy
        try:
            from scipy.optimize import minimize
        except ImportError:
            # Fallback: proportional to ln(Isp) heuristic
            ln_sum = sum(math.log(isp) for isp in isps)
            optimal_split = [total_dv_kms * math.log(isp) / ln_sum for isp in isps]
            method = "heuristic (scipy not available)"
            glow_opt, stages_opt = _compute_glow(optimal_split, isps, sfs, payload_kg)
            return _build_result(optimal_split, isps, sfs, payload_kg, total_dv_kms,
                                 glow_opt, stages_opt, method)

        def objective(x):
            # x contains n-1 delta-v values; last is computed from constraint
            dv_split = list(x) + [total_dv_kms - sum(x)]
            if any(dv < 0.1 for dv in dv_split):
                return 1e15
            glow, _ = _compute_glow(dv_split, isps, sfs, payload_kg)
            return glow

        # Initial guess: proportional to Isp
        ln_sum = sum(math.log(isp) for isp in isps)
        x0 = [total_dv_kms * math.log(isps[i]) / ln_sum for i in range(n_stages - 1)]

        bounds = [(0.5, total_dv_kms - 0.5)] * (n_stages - 1)
        constraints = [{"type": "ineq", "fun": lambda x: total_dv_kms - sum(x) - 0.1}]

        result = minimize(objective, x0, method="SLSQP", bounds=bounds,
                          constraints=constraints, options={"maxiter": 500, "ftol": 1e-8})

        optimal_split = list(result.x) + [total_dv_kms - sum(result.x)]
        method = "numerical (SLSQP)"

    glow_opt, stages_opt = _compute_glow(optimal_split, isps, sfs, payload_kg)

    # Compare with equal split
    equal_split = [total_dv_kms / n_stages] * n_stages
    glow_equal, stages_equal = _compute_glow(equal_split, isps, sfs, payload_kg)
    mass_saved_pct = (glow_equal - glow_opt) / glow_equal * 100 if glow_equal > 0 else 0

    return _build_result(optimal_split, isps, sfs, payload_kg, total_dv_kms,
                         glow_opt, stages_opt, method, glow_equal, mass_saved_pct)


def _build_result(split, isps, sfs, payload_kg, total_dv, glow, stages, method,
                  glow_equal=None, mass_saved_pct=None):
    stage_details = []
    for i, (dv, isp, sf, st) in enumerate(zip(split, isps, sfs, stages)):
        stage_details.append({
            "stage": i + 1,
            "delta_v_kms": round(dv, 3),
            "isp_s": isp,
            "structural_fraction": sf,
            "propellant_kg": round(st["propellant_kg"], 1),
            "structure_kg": round(st["structure_kg"], 1),
            "wet_mass_kg": round(st["wet_kg"], 1),
            "dry_mass_kg": round(st["dry_kg"], 1),
        })

    result = {
        "total_delta_v_kms": total_dv,
        "payload_kg": payload_kg,
        "stages": stage_details,
        "glow_kg": round(glow, 1),
        "glow_tonnes": round(glow / 1000, 2),
        "payload_fraction": round(payload_kg / glow, 5) if glow > 0 else 0,
        "method": method,
    }
    if glow_equal is not None:
        result["comparison"] = {
            "equal_split_glow_kg": round(glow_equal, 1),
            "optimal_glow_kg": round(glow, 1),
            "mass_saved_pct": round(mass_saved_pct, 2),
        }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Staging Optimizer")
    sub = parser.add_subparsers(dest="command")

    p_o = sub.add_parser("optimize", help="Find optimal delta-v split across stages")
    p_o.add_argument("--delta-v", type=float, required=True, help="Total delta-v in km/s")
    p_o.add_argument("--stages", type=int, required=True, help="Number of stages")
    p_o.add_argument("--isp", type=str, default=None, help="Comma-separated Isp per stage (s)")
    p_o.add_argument("--structural-fraction", type=str, default=None,
                     help="Comma-separated structural fraction per stage")
    p_o.add_argument("--engine", type=str, default=None,
                     help="Comma-separated engine names from vehicles.json")
    p_o.add_argument("--payload-kg", type=float, required=True)

    args = parser.parse_args()
    if args.command == "optimize":
        n = args.stages

        if args.engine:
            # Load engines from vehicles.json
            engines_db = _load_engines()
            engine_names = [e.strip() for e in args.engine.split(",")]
            if len(engine_names) != n:
                print(json.dumps({"error": f"Provide {n} engine names, got {len(engine_names)}"}))
                sys.exit(1)
            isps = []
            for ename in engine_names:
                key = ename.lower().replace(" ", "_").replace("-", "_")
                if key not in engines_db:
                    print(json.dumps({"error": f"Unknown engine '{ename}'. Available: {list(engines_db.keys())}"}))
                    sys.exit(1)
                isps.append(engines_db[key].get("isp_vac_s", 300))

            # Amendment 2: default structural fraction 0.07 when using --engine
            if args.structural_fraction:
                sfs = [float(x) for x in args.structural_fraction.split(",")]
            else:
                sfs = [0.07] * n
        elif args.isp:
            isps = [float(x) for x in args.isp.split(",")]
            if args.structural_fraction:
                sfs = [float(x) for x in args.structural_fraction.split(",")]
            else:
                sfs = [0.07] * n
        else:
            print(json.dumps({"error": "Provide either --isp or --engine"}))
            sys.exit(1)

        result = optimize_staging(args.delta_v, n, isps, sfs, args.payload_kg)
        if "error" in result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            sys.exit(1)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        parser.print_help()
        sys.exit(0)
