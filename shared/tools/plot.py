"""Visualization Tool — Shared tool for space-engineering pack.

Usage:
    python plot.py hohmann-plot Earth Mars --output /tmp/transfer.png
    python plot.py delta-v-waterfall LEO Mars --reusable --output /tmp/budget.png
    python plot.py trade-matrix --vehicles falcon9 starship ariane6 --output /tmp/trade.png
"""
import argparse
import json
import math
import sys
import os

# Import from sibling modules
sys.path.insert(0, os.path.dirname(__file__))
from trajectory import PLANETS, MOONS, MU_SUN, AU_KM, hohmann_transfer, delta_v_budget

# Lazy import matplotlib to fail gracefully
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ImportError:
    print(json.dumps({"error": "matplotlib not installed. Run: pip install matplotlib"}))
    sys.exit(1)

SHARED_DATA = os.path.join(os.path.dirname(__file__), "..", "data")


def _load_vehicles():
    filepath = os.path.join(SHARED_DATA, "vehicles.json")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"vehicles": {}, "engines": {}}


def hohmann_plot(planet_from, planet_to, output_path):
    """Top-down view of Hohmann transfer orbit."""
    planet_from = planet_from.title()
    planet_to = planet_to.title()

    # Resolve moons to parent
    actual_from = MOONS[planet_from]["parent"] if planet_from in MOONS else planet_from
    actual_to = MOONS[planet_to]["parent"] if planet_to in MOONS else planet_to

    if actual_from not in PLANETS or actual_to not in PLANETS:
        available = list(PLANETS.keys()) + list(MOONS.keys())
        print(json.dumps({"error": f"Unknown body. Available: {available}"}))
        sys.exit(1)

    r1_au = PLANETS[actual_from]["a_au"]
    r2_au = PLANETS[actual_to]["a_au"]
    if r1_au > r2_au:
        r1_au, r2_au = r2_au, r1_au
        actual_from, actual_to = actual_to, actual_from

    # Get delta-v data
    transfer = hohmann_transfer(planet_from, planet_to)

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.set_aspect("equal")
    ax.set_facecolor("white")

    # Sun at center
    ax.plot(0, 0, "o", color="#FFD700", markersize=18, zorder=5)
    ax.annotate("Sun", (0, 0), textcoords="offset points", xytext=(12, -5),
                fontsize=10, fontweight="bold", color="#B8860B")

    # Departure orbit (blue circle)
    theta = [i * 2 * math.pi / 360 for i in range(361)]
    x1 = [r1_au * math.cos(t) for t in theta]
    y1 = [r1_au * math.sin(t) for t in theta]
    ax.plot(x1, y1, "-", color="#2196F3", linewidth=1.5, label=f"{actual_from} orbit")
    ax.plot(r1_au, 0, "o", color="#2196F3", markersize=10, zorder=5)
    ax.annotate(actual_from, (r1_au, 0), textcoords="offset points", xytext=(8, 8),
                fontsize=9, color="#2196F3", fontweight="bold")

    # Arrival orbit (red circle)
    x2 = [r2_au * math.cos(t) for t in theta]
    y2 = [r2_au * math.sin(t) for t in theta]
    ax.plot(x2, y2, "-", color="#F44336", linewidth=1.5, label=f"{actual_to} orbit")
    ax.plot(-r2_au, 0, "o", color="#F44336", markersize=10, zorder=5)
    ax.annotate(actual_to, (-r2_au, 0), textcoords="offset points", xytext=(-15, 10),
                fontsize=9, color="#F44336", fontweight="bold")

    # Transfer ellipse (dashed green) — half ellipse from departure to arrival
    a_transfer = (r1_au + r2_au) / 2
    b_transfer = math.sqrt(r1_au * r2_au)  # semi-minor axis of transfer ellipse
    t_half = [i * math.pi / 180 for i in range(181)]
    # Ellipse centered at focus (Sun), parametric with focus at origin
    # x = a*cos(t) - c, y = b*sin(t), where c = a - r1 (periapsis at r1)
    c = a_transfer - r1_au
    xt = [a_transfer * math.cos(t) - c for t in t_half]
    yt = [b_transfer * math.sin(t) for t in t_half]
    ax.plot(xt, yt, "--", color="#4CAF50", linewidth=2.5, label="Transfer orbit", zorder=3)

    # Delta-v annotations
    dv_dep = transfer.get("delta_v_departure_kms", 0)
    dv_arr = transfer.get("delta_v_arrival_kms", 0)
    dv_tot = transfer.get("delta_v_total_kms", 0)
    t_days = transfer.get("transfer_time_days", 0)

    info_text = (f"Hohmann Transfer: {planet_from} → {planet_to}\n"
                 f"Δv departure: {dv_dep} km/s\n"
                 f"Δv arrival: {dv_arr} km/s\n"
                 f"Δv total: {dv_tot} km/s\n"
                 f"Transfer time: {t_days:.0f} days ({t_days/365.25:.1f} years)")
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=9,
            verticalalignment="top", fontfamily="monospace",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#E8F5E9", alpha=0.9))

    ax.set_xlabel("Distance (AU)", fontsize=11)
    ax.set_ylabel("Distance (AU)", fontsize=11)
    ax.set_title(f"Hohmann Transfer: {planet_from} → {planet_to}", fontsize=13, fontweight="bold")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return {"status": "ok", "output": output_path, "size_bytes": os.path.getsize(output_path)}


def delta_v_waterfall(destination, reusable=False, output_path="/tmp/plot_output.png"):
    """Horizontal stacked bar: delta-v budget breakdown."""
    budget = delta_v_budget(destination, reusable)
    if "error" in budget:
        print(json.dumps(budget))
        sys.exit(1)

    segments = []
    colors = []
    labels = []

    if "gravity_loss_kms" in budget:
        # LEO destination — show loss breakdown
        orbital = budget.get("orbital_dv_kms", 0) - 1.7  # subtract losses from total
        segments.append(orbital)
        colors.append("#2196F3")
        labels.append(f"Orbital vel: {orbital:.1f}")

        segments.append(budget["gravity_loss_kms"])
        colors.append("#FF9800")
        labels.append(f"Gravity loss: {budget['gravity_loss_kms']}")

        segments.append(budget["drag_loss_kms"])
        colors.append("#9C27B0")
        labels.append(f"Drag loss: {budget['drag_loss_kms']}")

        segments.append(budget["steering_loss_kms"])
        colors.append("#795548")
        labels.append(f"Steering: {budget['steering_loss_kms']}")
    else:
        segments.append(9.4)  # LEO insertion
        colors.append("#2196F3")
        labels.append("LEO insertion: 9.4")

        transfer_dv = budget.get("from_LEO_dv_kms", 0)
        if transfer_dv > 0:
            segments.append(transfer_dv)
            colors.append("#4CAF50")
            labels.append(f"Transfer: {transfer_dv}")

    if reusable and budget.get("reuse_penalty_kms", 0) > 0:
        segments.append(budget["reuse_penalty_kms"])
        colors.append("#F44336")
        labels.append(f"Reuse penalty: {budget['reuse_penalty_kms']}")

    segments.append(budget.get("margin_kms", 0))
    colors.append("#9E9E9E")
    labels.append(f"Margin ({budget.get('margin_pct', 10)}%): {budget.get('margin_kms', 0)}")

    fig, ax = plt.subplots(figsize=(12, 3))
    left = 0
    for seg, color, label in zip(segments, colors, labels):
        bar = ax.barh(0, seg, left=left, color=color, edgecolor="white", height=0.5)
        # Label inside bar if wide enough
        cx = left + seg / 2
        ax.text(cx, 0, f"{seg:.1f}", ha="center", va="center", fontsize=9,
                fontweight="bold", color="white" if seg > 0.5 else "black")
        left += seg

    ax.set_xlim(0, left * 1.05)
    ax.set_yticks([])
    ax.set_xlabel("Delta-v (km/s)", fontsize=11)
    reuse_tag = " [Reusable]" if reusable else ""
    ax.set_title(f"Delta-v Budget: Surface → {destination}{reuse_tag} | Total: {budget.get('total_dv_kms', 0)} km/s",
                 fontsize=12, fontweight="bold")

    # Legend
    patches = [mpatches.Patch(color=c, label=l) for c, l in zip(colors, labels)]
    ax.legend(handles=patches, loc="upper right", fontsize=8, ncol=2)
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return {"status": "ok", "output": output_path, "size_bytes": os.path.getsize(output_path)}


def trade_matrix(vehicle_names, output_path="/tmp/plot_output.png"):
    """Grouped bar chart comparing vehicles on cost, payload, cost/kg."""
    data = _load_vehicles()
    vehicles = data.get("vehicles", {})

    found = []
    for name in vehicle_names:
        key = name.lower().replace(" ", "_").replace("-", "_")
        if key in vehicles:
            v = vehicles[key]
            found.append({
                "key": key,
                "name": v.get("name", key),
                "cost_m": v.get("launch_cost_m", 0),
                "payload_leo_kg": v.get("payload_leo_kg", 0),
                "cost_per_kg": round(v["launch_cost_m"] * 1e6 / v["payload_leo_kg"], 0) if v.get("payload_leo_kg", 0) > 0 else 0,
            })
        else:
            found.append({"key": key, "name": name, "cost_m": 0, "payload_leo_kg": 0, "cost_per_kg": 0})

    if not found:
        print(json.dumps({"error": "No vehicles found", "available": list(vehicles.keys())}))
        sys.exit(1)

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    names = [v["name"] for v in found]
    x = range(len(names))

    # Cost ($M)
    costs = [v["cost_m"] for v in found]
    axes[0].bar(x, costs, color="#2196F3", edgecolor="white")
    axes[0].set_ylabel("Launch Cost ($M)")
    axes[0].set_title("Launch Cost", fontweight="bold")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(names, rotation=30, ha="right", fontsize=8)
    for i, c in enumerate(costs):
        axes[0].text(i, c + max(costs) * 0.02, f"${c}M", ha="center", fontsize=8)

    # Payload (kg)
    payloads = [v["payload_leo_kg"] for v in found]
    axes[1].bar(x, payloads, color="#4CAF50", edgecolor="white")
    axes[1].set_ylabel("Payload to LEO (kg)")
    axes[1].set_title("Payload Capacity", fontweight="bold")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(names, rotation=30, ha="right", fontsize=8)
    for i, p in enumerate(payloads):
        axes[1].text(i, p + max(payloads) * 0.02, f"{p:,.0f}", ha="center", fontsize=8)

    # Cost per kg ($/kg)
    cpk = [v["cost_per_kg"] for v in found]
    axes[2].bar(x, cpk, color="#FF9800", edgecolor="white")
    axes[2].set_ylabel("Cost per kg ($/kg)")
    axes[2].set_title("Cost Efficiency", fontweight="bold")
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(names, rotation=30, ha="right", fontsize=8)
    for i, c in enumerate(cpk):
        axes[2].text(i, c + max(cpk) * 0.02, f"${c:,.0f}", ha="center", fontsize=8)

    fig.suptitle("Launch Vehicle Trade Matrix", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return {"status": "ok", "output": output_path, "size_bytes": os.path.getsize(output_path)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Space Engineering Visualization Tool")
    sub = parser.add_subparsers(dest="command")

    p_h = sub.add_parser("hohmann-plot", help="Hohmann transfer orbit visualization")
    p_h.add_argument("planet_from")
    p_h.add_argument("planet_to")
    p_h.add_argument("--output", default="/tmp/plot_output.png")

    p_d = sub.add_parser("delta-v-waterfall", help="Delta-v budget waterfall chart")
    p_d.add_argument("args", nargs="+", help="Destination (e.g. Mars) or from-to (e.g. LEO Mars)")
    p_d.add_argument("--reusable", action="store_true")
    p_d.add_argument("--output", default="/tmp/plot_output.png")

    p_t = sub.add_parser("trade-matrix", help="Vehicle comparison trade matrix")
    p_t.add_argument("--vehicles", nargs="+", required=True)
    p_t.add_argument("--output", default="/tmp/plot_output.png")

    args = parser.parse_args()
    if args.command == "hohmann-plot":
        result = hohmann_plot(args.planet_from, args.planet_to, args.output)
    elif args.command == "delta-v-waterfall":
        dest = args.args[-1]  # Last arg is destination (e.g. "Mars" from "LEO Mars")
        result = delta_v_waterfall(dest, args.reusable, args.output)
    elif args.command == "trade-matrix":
        result = trade_matrix(args.vehicles, args.output)
    else:
        parser.print_help()
        sys.exit(0)
    print(json.dumps(result, indent=2, ensure_ascii=False))
