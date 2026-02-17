"""Rocket Trajectory Calculator — Shared tool for space-engineering pack.

Usage:
    python trajectory.py hohmann Earth Mars
    python trajectory.py tsiolkovsky --isp 311 --mass-initial 549000 --mass-final 26000
    python trajectory.py delta-v-budget LEO --reusable
    python trajectory.py gravity-loss --twr 1.3 --burn-time 162
"""
import argparse
import math
import json
import sys

G0 = 9.80665  # m/s²

# Delta-v reference table (km/s) — verified from NASA/ESA sources
DELTA_V = {
    "LEO": 9.4,        # Surface → LEO (185 km), includes losses
    "LEO_orbital": 7.8, # Pure orbital velocity at 185 km
    "GTO": 2.44,        # LEO → GTO
    "GEO": 3.93,        # LEO → GEO (direct)
    "GTO_GEO": 1.5,     # GTO → GEO circularization
    "Moon_orbit": 4.04,  # LEO → Lunar orbit
    "Moon_surface": 6.0, # LEO → Lunar surface
    "Mars_transfer": 3.6,# LEO → Mars (Hohmann min)
    "Mars_orbit": 5.7,   # LEO → Mars orbit
    "Mars_surface": 8.0, # LEO → Mars surface
    "Jupiter": 6.3,      # LEO → Jupiter transfer
    "Solar_escape": 8.8, # LEO → Solar escape (C3=0)
}

# Planetary data for Hohmann transfers (semi-major axis in AU, mu in km³/s²)
PLANETS = {
    "Mercury": {"a_au": 0.387, "mu": 22032},
    "Venus":   {"a_au": 0.723, "mu": 324859},
    "Earth":   {"a_au": 1.000, "mu": 398600},
    "Mars":    {"a_au": 1.524, "mu": 42828},
    "Jupiter": {"a_au": 5.203, "mu": 126687000},
    "Saturn":  {"a_au": 9.537, "mu": 37931000},
    "Uranus":  {"a_au": 19.19, "mu": 5794000},
    "Neptune": {"a_au": 30.07, "mu": 6836500},
}

MOONS = {
    "Moon":   {"parent": "Earth",   "a_km": 384400,  "mu": 4902.8,  "approx_dv_capture_kms": 0.8},
    "Titan":  {"parent": "Saturn",  "a_km": 1221870, "mu": 8978.1,  "approx_dv_capture_kms": 1.5},
    "Europa": {"parent": "Jupiter", "a_km": 671100,  "mu": 3203.4,  "approx_dv_capture_kms": 1.8},
}

MU_SUN = 1.327e11  # km³/s², Sun's gravitational parameter
AU_KM = 1.496e8    # km per AU


def tsiolkovsky(isp, m_initial, m_final):
    """Tsiolkovsky rocket equation: delta-v = Isp * g0 * ln(m_i / m_f)"""
    if m_final <= 0 or m_initial <= 0 or m_final >= m_initial:
        return {"error": "Invalid masses: m_initial must be > m_final > 0"}
    mass_ratio = m_initial / m_final
    dv = isp * G0 * math.log(mass_ratio)
    return {
        "delta_v_ms": round(dv, 1),
        "delta_v_kms": round(dv / 1000, 3),
        "mass_ratio": round(mass_ratio, 3),
        "propellant_fraction": round(1 - 1/mass_ratio, 4),
        "isp_s": isp,
        "m_initial_kg": m_initial,
        "m_final_kg": m_final,
    }


def inverse_tsiolkovsky(isp, delta_v_kms, m_payload, structural_fraction=0.08):
    """Given delta-v and payload, find required propellant and stage masses."""
    if m_payload <= 0:
        return {"error": "Payload must be > 0 kg"}
    dv = delta_v_kms * 1000
    mass_ratio = math.exp(dv / (isp * G0))
    # Check feasibility against structural limit
    max_mass_ratio = 1 / structural_fraction
    if mass_ratio > max_mass_ratio:
        return {"error": f"Infeasible: required mass ratio {mass_ratio:.2f} exceeds structural limit {max_mass_ratio:.2f}"}
    # m_initial / m_final = mass_ratio
    # m_initial = m_structure + m_propellant + m_payload
    # m_final = m_structure + m_payload
    # m_structure = structural_fraction * (m_structure + m_propellant)
    # Let m_prop = P, m_struct = S = sf * (S + P) => S = sf*P / (1-sf)
    # m_final = S + m_payload = sf*P/(1-sf) + m_payload
    # m_initial = S + P + m_payload = P/(1-sf) + m_payload
    # mass_ratio = (P/(1-sf) + m_payload) / (sf*P/(1-sf) + m_payload)
    # Solve for P:
    sf = structural_fraction
    # mass_ratio * (sf*P/(1-sf) + m_payload) = P/(1-sf) + m_payload
    # mass_ratio*sf*P/(1-sf) + mass_ratio*m_payload = P/(1-sf) + m_payload
    # P/(1-sf) * (mass_ratio*sf - 1) = m_payload * (1 - mass_ratio)
    # P = m_payload * (1 - mass_ratio) * (1-sf) / (mass_ratio*sf - 1)
    denominator = mass_ratio * sf - 1
    if denominator == 0:
        return {"error": "Degenerate case: mass_ratio * structural_fraction = 1"}
    propellant = m_payload * (1 - mass_ratio) * (1 - sf) / denominator
    if propellant < 0:
        # Flip sign — the algebra works out negative when feasible
        propellant = abs(propellant)
    structure = sf * propellant / (1 - sf)
    m_initial = structure + propellant + m_payload
    m_final = structure + m_payload
    return {
        "propellant_kg": round(propellant, 1),
        "structure_kg": round(structure, 1),
        "stage_dry_kg": round(structure + m_payload, 1),
        "stage_wet_kg": round(m_initial, 1),
        "mass_ratio": round(m_initial / m_final, 3),
        "payload_fraction": round(m_payload / m_initial, 4),
        "structural_fraction": sf,
        "delta_v_kms": delta_v_kms,
        "isp_s": isp,
    }


def hohmann_transfer(planet_from, planet_to):
    """Calculate Hohmann transfer delta-v between two planets (or to a moon)."""
    planet_from = planet_from.title()
    planet_to = planet_to.title()
    if planet_from == planet_to:
        return {"error": "Same planet — no transfer needed"}

    # Check if destination is a moon
    moon_note = None
    actual_to = planet_to
    if planet_to in MOONS:
        moon = MOONS[planet_to]
        actual_to = moon["parent"]
        moon_note = (f"Final leg to {planet_to} requires patched-conic analysis. "
                     f"Approximate additional delta-v: {moon['approx_dv_capture_kms']} km/s for capture/descent.")
    if planet_from in MOONS:
        moon = MOONS[planet_from]
        planet_from = moon["parent"]

    if planet_from not in PLANETS or actual_to not in PLANETS:
        available = list(PLANETS.keys()) + list(MOONS.keys())
        return {"error": f"Unknown body. Available: {available}"}
    r1 = PLANETS[planet_from]["a_au"] * AU_KM
    r2 = PLANETS[actual_to]["a_au"] * AU_KM
    if r1 > r2:
        r1, r2 = r2, r1
    # Transfer orbit semi-major axis
    a_transfer = (r1 + r2) / 2
    # Velocities
    v_circular_1 = math.sqrt(MU_SUN / r1)
    v_circular_2 = math.sqrt(MU_SUN / r2)
    v_departure = math.sqrt(MU_SUN * (2/r1 - 1/a_transfer))
    v_arrival = math.sqrt(MU_SUN * (2/r2 - 1/a_transfer))
    dv1 = abs(v_departure - v_circular_1)  # already in km/s
    dv2 = abs(v_circular_2 - v_arrival)
    # Transfer time
    t_transfer = math.pi * math.sqrt(a_transfer**3 / MU_SUN)
    result = {
        "from": planet_from,
        "to": planet_to,
        "delta_v_departure_kms": round(dv1, 2),
        "delta_v_arrival_kms": round(dv2, 2),
        "delta_v_total_kms": round(dv1 + dv2, 2),
        "transfer_time_days": round(t_transfer / 86400, 1),
        "transfer_time_months": round(t_transfer / (86400 * 30.44), 1),
        "note": "Heliocentric delta-v only. Add planet escape/capture for full budget.",
    }
    if moon_note:
        result["moon_note"] = moon_note
    return result


def gravity_loss(twr, burn_time_s):
    """Estimate gravity losses based on initial TWR and burn time."""
    if twr <= 1.0:
        return {"error": "TWR must be > 1.0 for launch"}
    # Simplified model: gravity loss ≈ g0 * burn_time * (1/TWR) * correction_factor
    # More accurate: integrate over changing mass, but this gives good estimate
    avg_twr = twr * 1.4  # TWR increases as propellant burns (rough 1.4x avg)
    g_loss = G0 * burn_time_s * (1 / avg_twr) * 0.85  # 0.85 correction for gravity turn
    drag_loss = 150 + (twr - 1.3) * 50  # Higher TWR = more drag (faster in atmo)
    steering_loss = 100  # Typical
    return {
        "gravity_loss_ms": round(g_loss, 0),
        "gravity_loss_kms": round(g_loss / 1000, 2),
        "drag_loss_ms": round(drag_loss, 0),
        "steering_loss_ms": round(steering_loss, 0),
        "total_losses_ms": round(g_loss + drag_loss + steering_loss, 0),
        "total_losses_kms": round((g_loss + drag_loss + steering_loss) / 1000, 2),
        "input_twr": twr,
        "burn_time_s": burn_time_s,
    }


def delta_v_budget(destination, reusable=False, margin_pct=10):
    """Build a complete delta-v budget for a destination."""
    dest_upper = destination.upper()
    lookup = {
        "LEO": "LEO", "GTO": "GTO", "GEO": "GEO",
        "MOON": "Moon_orbit", "LUNAR": "Moon_orbit",
        "MOON_SURFACE": "Moon_surface", "LUNAR_SURFACE": "Moon_surface",
        "MARS": "Mars_transfer", "MARS_ORBIT": "Mars_orbit",
        "MARS_SURFACE": "Mars_surface", "JUPITER": "Jupiter",
        "ESCAPE": "Solar_escape",
    }
    key = lookup.get(dest_upper)
    if not key:
        return {"error": f"Unknown destination. Available: {list(lookup.keys())}"}
    base_dv = DELTA_V[key]
    budget = {
        "destination": destination,
        "orbital_dv_kms": base_dv,
    }
    if key == "LEO":
        budget["gravity_loss_kms"] = 1.2
        budget["drag_loss_kms"] = 0.4
        budget["steering_loss_kms"] = 0.1
    else:
        budget["from_LEO_dv_kms"] = base_dv
        budget["LEO_insertion_dv_kms"] = DELTA_V["LEO"]
    if reusable:
        budget["reuse_penalty_kms"] = 2.0
        budget["reuse_note"] = "Boostback 0.8 + entry 0.5 + landing 0.4 + margin 0.3"
    subtotal = base_dv + (2.0 if reusable else 0)
    margin = subtotal * margin_pct / 100
    budget["margin_pct"] = margin_pct
    budget["margin_kms"] = round(margin, 2)
    budget["total_dv_kms"] = round(subtotal + margin, 2)
    budget["reusable"] = reusable
    return budget


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rocket Trajectory Calculator")
    sub = parser.add_subparsers(dest="command")

    p_ts = sub.add_parser("tsiolkovsky", help="Tsiolkovsky rocket equation")
    p_ts.add_argument("--isp", type=float, required=True)
    p_ts.add_argument("--mass-initial", type=float, required=True)
    p_ts.add_argument("--mass-final", type=float, required=True)

    p_inv = sub.add_parser("inverse", help="Inverse Tsiolkovsky — find propellant needed")
    p_inv.add_argument("--isp", type=float, required=True)
    p_inv.add_argument("--delta-v", type=float, required=True, help="km/s")
    p_inv.add_argument("--payload", type=float, required=True, help="kg")
    p_inv.add_argument("--structural-fraction", type=float, default=0.08)

    p_h = sub.add_parser("hohmann", help="Hohmann transfer between planets")
    p_h.add_argument("planet_from")
    p_h.add_argument("planet_to")

    p_g = sub.add_parser("gravity-loss", help="Estimate gravity/drag losses")
    p_g.add_argument("--twr", type=float, required=True)
    p_g.add_argument("--burn-time", type=float, required=True)

    p_d = sub.add_parser("delta-v-budget", help="Full delta-v budget")
    p_d.add_argument("destination")
    p_d.add_argument("--reusable", action="store_true")
    p_d.add_argument("--margin", type=float, default=10)

    args = parser.parse_args()
    if args.command == "tsiolkovsky":
        result = tsiolkovsky(args.isp, args.mass_initial, args.mass_final)
    elif args.command == "inverse":
        result = inverse_tsiolkovsky(args.isp, args.delta_v, args.payload, args.structural_fraction)
        if "error" in result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            sys.exit(1)
    elif args.command == "hohmann":
        result = hohmann_transfer(args.planet_from, args.planet_to)
        if "error" in result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            sys.exit(1)
    elif args.command == "gravity-loss":
        result = gravity_loss(args.twr, args.burn_time)
    elif args.command == "delta-v-budget":
        result = delta_v_budget(args.destination, args.reusable, args.margin)
    else:
        parser.print_help()
        sys.exit(0)
    print(json.dumps(result, indent=2, ensure_ascii=False))
