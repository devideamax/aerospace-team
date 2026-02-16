"""Tank Geometry Calculator — Shared tool for space-engineering pack.

Usage:
    python geometry.py tank --propellant-kg 400000 --fuel lox-rp1 --diameter 3.66
    python geometry.py fairing --payload-diameter 4.0 --payload-height 6.0
    python geometry.py vehicle-size --payload-kg 22800 --orbit LEO --propellant lox-rp1
"""
import argparse
import json
import math
import sys

# Propellant densities (kg/m³)
PROPELLANTS = {
    "lox": {"density": 1141, "name": "Liquid Oxygen"},
    "rp1": {"density": 820, "name": "RP-1 (Kerosene)"},
    "lh2": {"density": 71, "name": "Liquid Hydrogen"},
    "ch4": {"density": 422, "name": "Liquid Methane (LCH4)"},
    "n2o4": {"density": 1440, "name": "Nitrogen Tetroxide"},
    "udmh": {"density": 793, "name": "UDMH"},
    "xenon": {"density": 1640, "name": "Xenon (supercritical)"},
}

# Common bipropellant combinations with mixture ratios (oxidizer/fuel by mass)
COMBINATIONS = {
    "lox-rp1":  {"ox": "lox", "fuel": "rp1",  "mr": 2.27, "name": "LOX/RP-1 (Kerolox)"},
    "lox-ch4":  {"ox": "lox", "fuel": "ch4",  "mr": 3.6,  "name": "LOX/CH4 (Methalox)"},
    "lox-lh2":  {"ox": "lox", "fuel": "lh2",  "mr": 6.0,  "name": "LOX/LH2 (Hydrolox)"},
    "n2o4-udmh":{"ox": "n2o4","fuel": "udmh", "mr": 2.6,  "name": "N2O4/UDMH (Hypergolic)"},
}

WALL_DENSITY_ALUMINUM = 2700   # kg/m³
WALL_DENSITY_STEEL = 7800      # kg/m³
WALL_DENSITY_CFRP = 1600       # kg/m³


def tank_sizing(propellant_kg, fuel_type, diameter_m, wall_material="aluminum", wall_thickness_mm=3):
    """Calculate tank dimensions for given propellant mass and diameter."""
    combo = COMBINATIONS.get(fuel_type.lower())
    if not combo:
        return {"error": f"Unknown fuel type. Available: {list(COMBINATIONS.keys())}"}

    mr = combo["mr"]
    ox_mass = propellant_kg * mr / (1 + mr)
    fuel_mass = propellant_kg - ox_mass
    ox_density = PROPELLANTS[combo["ox"]]["density"]
    fuel_density = PROPELLANTS[combo["fuel"]]["density"]
    ox_volume = ox_mass / ox_density
    fuel_volume = fuel_mass / fuel_density
    total_volume = ox_volume + fuel_volume
    ullage_factor = 1.05  # 5% ullage
    total_volume_with_ullage = total_volume * ullage_factor

    radius = diameter_m / 2
    cross_section = math.pi * radius ** 2
    # Cylindrical tank with hemispherical domes
    dome_volume = (4/3) * math.pi * radius ** 3  # Two hemispheres = one sphere
    cylinder_volume_needed = total_volume_with_ullage - dome_volume
    if cylinder_volume_needed < 0:
        cylinder_length = 0
        total_length = diameter_m  # Just a sphere
    else:
        cylinder_length = cylinder_volume_needed / cross_section
        total_length = cylinder_length + diameter_m  # Add dome heights

    # Wall mass estimate
    wt = wall_thickness_mm / 1000
    materials = {"aluminum": WALL_DENSITY_ALUMINUM, "steel": WALL_DENSITY_STEEL, "cfrp": WALL_DENSITY_CFRP}
    wall_density = materials.get(wall_material, WALL_DENSITY_ALUMINUM)
    surface_area = 2 * math.pi * radius * cylinder_length + 4 * math.pi * radius ** 2
    wall_mass = surface_area * wt * wall_density
    # Insulation for cryo
    insulation_mass = surface_area * 2.0 if fuel_type in ["lox-lh2"] else surface_area * 0.5

    return {
        "propellant_type": combo["name"],
        "mixture_ratio": mr,
        "oxidizer_kg": round(ox_mass, 0),
        "fuel_kg": round(fuel_mass, 0),
        "oxidizer_volume_m3": round(ox_volume, 1),
        "fuel_volume_m3": round(fuel_volume, 1),
        "total_volume_m3": round(total_volume_with_ullage, 1),
        "tank_diameter_m": diameter_m,
        "cylinder_length_m": round(cylinder_length, 2),
        "total_tank_length_m": round(total_length, 2),
        "wall_material": wall_material,
        "wall_mass_kg": round(wall_mass, 0),
        "insulation_mass_kg": round(insulation_mass, 0),
        "total_tank_mass_kg": round(wall_mass + insulation_mass, 0),
        "tank_mass_fraction": round((wall_mass + insulation_mass) / propellant_kg, 4),
    }


def fairing_check(payload_diameter_m, payload_height_m):
    """Check payload against common fairing dimensions."""
    fairings = {
        "Falcon 9": {"diameter": 5.2, "height": 13.1, "usable_diameter": 4.6, "usable_height": 11.0},
        "Falcon Heavy": {"diameter": 5.2, "height": 13.1, "usable_diameter": 4.6, "usable_height": 11.0},
        "Ariane 6": {"diameter": 5.4, "height": 20.0, "usable_diameter": 4.57, "usable_height": 17.0},
        "Vulcan": {"diameter": 5.4, "height": 21.3, "usable_diameter": 4.57, "usable_height": 18.0},
        "Starship": {"diameter": 9.0, "height": 22.0, "usable_diameter": 8.0, "usable_height": 18.0},
        "New Glenn": {"diameter": 7.0, "height": 21.9, "usable_diameter": 6.0, "usable_height": 18.0},
        "SLS": {"diameter": 8.4, "height": 19.1, "usable_diameter": 7.5, "usable_height": 17.0},
    }
    results = []
    for name, f in fairings.items():
        fits = payload_diameter_m <= f["usable_diameter"] and payload_height_m <= f["usable_height"]
        margin_d = f["usable_diameter"] - payload_diameter_m
        margin_h = f["usable_height"] - payload_height_m
        results.append({
            "vehicle": name,
            "fits": fits,
            "diameter_margin_m": round(margin_d, 2),
            "height_margin_m": round(margin_h, 2),
            "fairing_diameter_m": f["usable_diameter"],
            "fairing_height_m": f["usable_height"],
        })
    return {
        "payload_diameter_m": payload_diameter_m,
        "payload_height_m": payload_height_m,
        "results": results,
    }


def vehicle_size_estimate(payload_kg, orbit="LEO", propellant="lox-rp1"):
    """Quick vehicle sizing estimate from payload requirements."""
    # Typical payload fractions
    fractions = {"LEO": 0.030, "GTO": 0.012, "GEO": 0.008, "Moon": 0.005, "Mars": 0.003}
    pf = fractions.get(orbit.upper(), 0.030)
    glow = payload_kg / pf
    combo = COMBINATIONS.get(propellant, COMBINATIONS["lox-rp1"])
    propellant_fraction = 0.88
    propellant_mass = glow * propellant_fraction
    structure_mass = glow - propellant_mass - payload_kg
    mr = combo["mr"]
    ox_mass = propellant_mass * mr / (1 + mr)
    fuel_mass = propellant_mass - ox_mass
    ox_vol = ox_mass / PROPELLANTS[combo["ox"]]["density"]
    fuel_vol = fuel_mass / PROPELLANTS[combo["fuel"]]["density"]
    total_vol = (ox_vol + fuel_vol) * 1.05
    # Estimate diameter from volume (assume L/D = 10)
    est_diameter = (4 * total_vol / (10 * math.pi)) ** (1/3) * 1.2
    return {
        "payload_kg": payload_kg,
        "orbit": orbit.upper(),
        "propellant": combo["name"],
        "estimated_glow_kg": round(glow, 0),
        "estimated_glow_tonnes": round(glow / 1000, 1),
        "propellant_mass_kg": round(propellant_mass, 0),
        "structure_mass_kg": round(structure_mass, 0),
        "total_volume_m3": round(total_vol, 1),
        "estimated_diameter_m": round(est_diameter, 1),
        "payload_fraction": pf,
        "note": "ROM estimate ±30%. Use full staging analysis for detailed design.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tank Geometry Calculator")
    sub = parser.add_subparsers(dest="command")

    p_t = sub.add_parser("tank", help="Tank sizing for propellant mass")
    p_t.add_argument("--propellant-kg", type=float, required=True)
    p_t.add_argument("--fuel", required=True, help="lox-rp1, lox-ch4, lox-lh2, n2o4-udmh")
    p_t.add_argument("--diameter", type=float, required=True, help="Tank diameter in meters")
    p_t.add_argument("--wall", default="aluminum", help="aluminum, steel, cfrp")

    p_f = sub.add_parser("fairing", help="Fairing compatibility check")
    p_f.add_argument("--payload-diameter", type=float, required=True)
    p_f.add_argument("--payload-height", type=float, required=True)

    p_s = sub.add_parser("vehicle-size", help="Quick vehicle sizing from payload")
    p_s.add_argument("--payload-kg", type=float, required=True)
    p_s.add_argument("--orbit", default="LEO")
    p_s.add_argument("--propellant", default="lox-rp1")

    args = parser.parse_args()
    if args.command == "tank":
        result = tank_sizing(args.propellant_kg, args.fuel, args.diameter, args.wall)
    elif args.command == "fairing":
        result = fairing_check(args.payload_diameter, args.payload_height)
    elif args.command == "vehicle-size":
        result = vehicle_size_estimate(args.payload_kg, args.orbit, args.propellant)
    else:
        parser.print_help()
        sys.exit(0)
    print(json.dumps(result, indent=2, ensure_ascii=False))
