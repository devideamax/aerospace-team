"""Mission Timeline Generator — Shared tool for space-engineering pack.

Usage:
    python timeline.py plan --launch-date 2027-03-15 --destination Mars --payload-kg 1000
    python timeline.py gantt --launch-date 2027-03-15 --destination Mars --output /tmp/timeline.png
"""
import argparse
import json
import math
import sys
import os
from datetime import datetime, timedelta

# Import Hohmann transfer times
sys.path.insert(0, os.path.dirname(__file__))
from trajectory import hohmann_transfer, PLANETS, MOONS

# Default operations duration (days)
OPS_DURATION = {
    "LEO": 5 * 365,      # 5 years
    "GTO": 5 * 365,
    "GEO": 5 * 365,
    "MOON": 1 * 365,     # 1 year
    "MARS": 1 * 365,     # 1 year
    "JUPITER": 2 * 365,  # 2 years
    "SATURN": 2 * 365,
    "URANUS": 2 * 365,
    "NEPTUNE": 2 * 365,
}

# Parking orbit duration before injection (days)
PARKING_ORBIT_DAYS = 0.1  # ~2.4 hours (typical 1-2 orbits)


def mission_plan(launch_date_str, destination, payload_kg=None):
    """Generate mission timeline with phases."""
    try:
        launch_date = datetime.strptime(launch_date_str, "%Y-%m-%d")
    except ValueError:
        return {"error": f"Invalid date format. Use YYYY-MM-DD (got '{launch_date_str}')"}

    dest_upper = destination.upper()
    phases = []
    current_date = launch_date

    # Phase 1: Launch
    launch_duration = timedelta(minutes=10)
    phases.append({
        "name": "Launch",
        "start": current_date.strftime("%Y-%m-%d"),
        "end": current_date.strftime("%Y-%m-%d"),
        "duration_days": 0,
        "notes": "Liftoff through MECO",
    })

    if dest_upper == "LEO":
        # LEO: no cruise, just launch + operations
        current_date += timedelta(days=1)
        ops_days = OPS_DURATION.get("LEO", 1825)
        phases.append({
            "name": "LEO Operations",
            "start": current_date.strftime("%Y-%m-%d"),
            "end": (current_date + timedelta(days=ops_days)).strftime("%Y-%m-%d"),
            "duration_days": ops_days,
            "notes": f"Payload: {payload_kg} kg" if payload_kg else "Nominal operations",
        })
    else:
        # Phase 2: Parking orbit
        park_end = current_date + timedelta(days=PARKING_ORBIT_DAYS)
        phases.append({
            "name": "Parking Orbit",
            "start": current_date.strftime("%Y-%m-%d"),
            "end": park_end.strftime("%Y-%m-%d"),
            "duration_days": round(PARKING_ORBIT_DAYS, 1),
            "notes": "LEO coast, systems checkout",
        })
        current_date = park_end

        # Phase 3: Transfer injection
        phases.append({
            "name": "Transfer Injection",
            "start": current_date.strftime("%Y-%m-%d"),
            "end": current_date.strftime("%Y-%m-%d"),
            "duration_days": 0,
            "notes": "Trans-injection burn",
        })

        # Phase 4: Cruise — use Hohmann transfer time
        dest_title = destination.title()
        transfer = hohmann_transfer("Earth", dest_title)
        if "error" in transfer:
            cruise_days = 180  # default fallback
        else:
            cruise_days = transfer.get("transfer_time_days", 180)

        cruise_end = current_date + timedelta(days=cruise_days)
        phases.append({
            "name": "Cruise",
            "start": current_date.strftime("%Y-%m-%d"),
            "end": cruise_end.strftime("%Y-%m-%d"),
            "duration_days": round(cruise_days, 1),
            "notes": f"Hohmann transfer to {dest_title}",
        })
        current_date = cruise_end

        # Phase 5: Arrival/Insertion
        phases.append({
            "name": "Arrival/Insertion",
            "start": current_date.strftime("%Y-%m-%d"),
            "end": current_date.strftime("%Y-%m-%d"),
            "duration_days": 0,
            "notes": f"Orbit insertion at {dest_title}",
        })

        # Phase 6: Operations
        ops_key = dest_upper
        if dest_title in MOONS:
            ops_key = MOONS[dest_title]["parent"].upper()
        ops_days = OPS_DURATION.get(ops_key, 365)
        ops_end = current_date + timedelta(days=ops_days)
        phases.append({
            "name": "Operations",
            "start": current_date.strftime("%Y-%m-%d"),
            "end": ops_end.strftime("%Y-%m-%d"),
            "duration_days": ops_days,
            "notes": f"Science/mission ops at {dest_title}",
        })

    total_days = (datetime.strptime(phases[-1]["end"], "%Y-%m-%d") - launch_date).days
    return {
        "mission": f"Earth -> {destination}",
        "launch_date": launch_date_str,
        "end_date": phases[-1]["end"],
        "total_duration_days": total_days,
        "total_duration_years": round(total_days / 365.25, 1),
        "payload_kg": payload_kg,
        "phases": phases,
    }


def gantt_chart(launch_date_str, destination, output_path, payload_kg=None):
    """Generate Gantt chart of mission timeline."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        return {"error": "matplotlib not installed. Run: pip install matplotlib"}

    plan = mission_plan(launch_date_str, destination, payload_kg)
    if "error" in plan:
        return plan

    phases = plan["phases"]
    fig, ax = plt.subplots(figsize=(14, 4 + len(phases) * 0.4))

    colors = ["#F44336", "#FF9800", "#FFC107", "#2196F3", "#4CAF50", "#9C27B0", "#795548"]
    y_positions = list(range(len(phases) - 1, -1, -1))

    for i, phase in enumerate(phases):
        start = datetime.strptime(phase["start"], "%Y-%m-%d")
        end = datetime.strptime(phase["end"], "%Y-%m-%d")
        duration = max((end - start).days, 1)  # At least 1 day for visibility
        color = colors[i % len(colors)]

        ax.barh(y_positions[i], duration, left=start, color=color,
                edgecolor="white", height=0.6, alpha=0.85)
        # Label
        label = f"{phase['name']} ({phase['duration_days']}d)"
        ax.text(start + timedelta(days=duration / 2), y_positions[i], label,
                ha="center", va="center", fontsize=8, fontweight="bold", color="white")

    ax.set_yticks(y_positions)
    ax.set_yticklabels([p["name"] for p in phases], fontsize=9)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate(rotation=30)

    ax.set_xlabel("Date", fontsize=11)
    ax.set_title(f"Mission Timeline: {plan['mission']} | Total: {plan['total_duration_years']} years",
                 fontsize=13, fontweight="bold")
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    return {"status": "ok", "output": output_path, "size_bytes": os.path.getsize(output_path)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mission Timeline Generator")
    sub = parser.add_subparsers(dest="command")

    p_p = sub.add_parser("plan", help="Generate mission timeline JSON")
    p_p.add_argument("--launch-date", required=True, help="YYYY-MM-DD")
    p_p.add_argument("--destination", required=True)
    p_p.add_argument("--payload-kg", type=float, default=None)

    p_g = sub.add_parser("gantt", help="Generate Gantt chart PNG")
    p_g.add_argument("--launch-date", required=True, help="YYYY-MM-DD")
    p_g.add_argument("--destination", required=True)
    p_g.add_argument("--payload-kg", type=float, default=None)
    p_g.add_argument("--output", default="/tmp/plot_output.png")

    args = parser.parse_args()
    if args.command == "plan":
        result = mission_plan(args.launch_date, args.destination, args.payload_kg)
    elif args.command == "gantt":
        result = gantt_chart(args.launch_date, args.destination, args.output, args.payload_kg)
    else:
        parser.print_help()
        sys.exit(0)
    print(json.dumps(result, indent=2, ensure_ascii=False))
