#!/usr/bin/env python3
"""Bloom Beauty Suites — pricing & financial calculator.

Pure standard library. Models two sides of the business:
  * lash studio  — per-service margin, revenue/hour vs a target, monthly P&L,
                   break-even sets.
  * suite rental — rent roll, occupancy, expenses, net, break-even occupancy.

Estimates for planning only — NOT tax/accounting advice. Benchmarks are general
industry references, not guarantees.

Usage:
    python3 bloom_calc.py --input model.json
    python3 bloom_calc.py --demo            # runs on the real Bloom seed numbers
    python3 bloom_calc.py --input model.json --json-only
"""
import argparse
import json
import math
import sys


def _round2(x):
    return round(x + 0.0, 2)


def analyze_lash(lash):
    target_hr = float(lash.get("targetHourlyRate", 0) or 0)
    overhead = float(lash.get("monthlyOverhead", 0) or 0)
    services = []
    rev = cogs = hours = sets = 0.0
    for s in lash.get("services", []):
        price = float(s["price"])
        dur_h = float(s.get("durationMin", 0)) / 60.0
        materials = float(s.get("materialsCost", 0) or 0)
        count = float(s.get("monthlyCount", 0) or 0)
        gm = price - materials
        row = {
            "name": s["name"],
            "price": price,
            "duration_h": _round2(dur_h),
            "materials_cost": _round2(materials),
            "gross_margin": _round2(gm),
            "gross_margin_pct": _round2(gm / price) if price else None,
            "revenue_per_hour": _round2(price / dur_h) if dur_h else None,
            "margin_per_hour": _round2(gm / dur_h) if dur_h else None,
            "meets_target_hourly": (price / dur_h >= target_hr) if (dur_h and target_hr) else None,
            "monthly_count": count,
            "monthly_revenue": _round2(price * count),
        }
        services.append(row)
        rev += price * count
        cogs += materials * count
        hours += dur_h * count
        sets += count

    gross_profit = rev - cogs
    net = gross_profit - overhead
    avg_gm_per_set = (gross_profit / sets) if sets else 0.0
    breakeven_sets = math.ceil(overhead / avg_gm_per_set) if avg_gm_per_set > 0 and overhead > 0 else 0
    return {
        "target_hourly_rate": target_hr,
        "services": services,
        "monthly": {
            "revenue": _round2(rev),
            "cogs": _round2(cogs),
            "gross_profit": _round2(gross_profit),
            "overhead": _round2(overhead),
            "net": _round2(net),
            "net_margin_pct": _round2(net / rev) if rev else None,
            "total_sets": sets,
            "total_chair_hours": _round2(hours),
            "blended_revenue_per_hour": _round2(rev / hours) if hours else None,
            "avg_gross_margin_per_set": _round2(avg_gm_per_set),
            "break_even_sets_for_overhead": breakeven_sets,
        },
    }


def analyze_suites(suites):
    units = suites.get("units", [])
    total = len(units)
    occupied = [u for u in units if u.get("occupied")]
    rent_actual = sum(float(u["rent"]) for u in occupied)
    rent_potential = sum(float(u["rent"]) for u in units)
    expenses_map = suites.get("monthlyExpenses", {})
    total_expenses = sum(float(v) for v in expenses_map.values())
    avg_rent = (rent_potential / total) if total else 0.0
    net = rent_actual - total_expenses
    breakeven_units = math.ceil(total_expenses / avg_rent) if avg_rent > 0 else 0
    return {
        "total_suites": total,
        "occupied_suites": len(occupied),
        "vacant_suites": total - len(occupied),
        "occupancy_pct": _round2(len(occupied) / total) if total else None,
        "rent_roll_actual": _round2(rent_actual),
        "rent_roll_potential": _round2(rent_potential),
        "vacancy_value_monthly": _round2(rent_potential - rent_actual),
        "total_monthly_expenses": _round2(total_expenses),
        "net": _round2(net),
        "net_margin_pct": _round2(net / rent_actual) if rent_actual else None,
        "avg_rent": _round2(avg_rent),
        "break_even_occupancy_units": breakeven_units,
        "break_even_occupancy_pct": _round2(breakeven_units / total) if total else None,
        "revenue_per_occupied_suite": _round2(rent_actual / len(occupied)) if occupied else None,
    }


def analyze(data):
    out = {"business": data.get("business", "Bloom Beauty Suites & Lash Bar")}
    if "lash" in data:
        out["lash"] = analyze_lash(data["lash"])
    if "suites" in data:
        out["suites"] = analyze_suites(data["suites"])
    if "lash" in out and "suites" in out:
        out["combined_monthly_net"] = _round2(
            out["lash"]["monthly"]["net"] + out["suites"]["net"]
        )
    return out


def demo_data():
    """The real Bloom seed numbers (see bloom-*/src/seed.js)."""
    units = []
    for i in range(1, 13):
        rent = 550 if i <= 4 else (650 if i <= 8 else 750)
        # Seed occupancy: suites 4, 8, 12 are vacant.
        occupied = i not in (4, 8, 12)
        units.append({"name": f"Suite {i}", "rent": rent, "occupied": occupied})
    return {
        "business": "Bloom Beauty Suites & Lash Bar (demo — seed numbers)",
        "lash": {
            "targetHourlyRate": 80,
            "monthlyOverhead": 350,
            "services": [
                {"name": "Classic Full Set", "price": 165, "durationMin": 120, "materialsCost": 10, "monthlyCount": 8},
                {"name": "Volume Full Set", "price": 225, "durationMin": 150, "materialsCost": 18, "monthlyCount": 6},
                {"name": "Classic Fill (2wk)", "price": 75, "durationMin": 60, "materialsCost": 5, "monthlyCount": 30},
                {"name": "Volume Fill (2wk)", "price": 110, "durationMin": 90, "materialsCost": 8, "monthlyCount": 20},
                {"name": "Lash Lift & Tint", "price": 85, "durationMin": 60, "materialsCost": 7, "monthlyCount": 6},
            ],
        },
        "suites": {
            "units": units,
            "monthlyExpenses": {
                "mortgage": 4200, "utilities": 680, "insurance": 240,
                "cleaning": 320, "internet": 140, "other": 200,
            },
        },
    }


def _pct(x):
    return f"{x * 100:.1f}%" if x is not None else "n/a"


def render(result):
    L = []
    L.append(f"Bloom Pricing & Financials — {result['business']}")
    L.append("=" * 64)
    if "lash" in result:
        lash = result["lash"]
        L.append("\nLASH — service economics (target $%.0f/hr)" % lash["target_hourly_rate"])
        L.append(f"{'Service':<22}{'Price':>7}{'Mat':>6}{'GM$':>7}{'GM%':>6}{'$/hr':>7}{'Tgt?':>6}")
        for s in lash["services"]:
            tgt = "" if s["meets_target_hourly"] is None else ("ok" if s["meets_target_hourly"] else "LOW")
            L.append(f"{s['name']:<22}{s['price']:>7.0f}{s['materials_cost']:>6.0f}"
                     f"{s['gross_margin']:>7.0f}{_pct(s['gross_margin_pct']):>6}"
                     f"{s['revenue_per_hour']:>7.0f}{tgt:>6}")
        m = lash["monthly"]
        L.append(f"\nLash monthly P&L: revenue ${m['revenue']:.0f}  COGS ${m['cogs']:.0f}  "
                 f"gross ${m['gross_profit']:.0f}  overhead ${m['overhead']:.0f}  "
                 f"NET ${m['net']:.0f} ({_pct(m['net_margin_pct'])})")
        L.append(f"  Chair hours {m['total_chair_hours']:.0f}/mo  blended ${m['blended_revenue_per_hour']:.0f}/hr  "
                 f"break-even {m['break_even_sets_for_overhead']} sets cover overhead")
    if "suites" in result:
        s = result["suites"]
        L.append("\nSUITES — rental economics")
        L.append(f"  Occupancy: {s['occupied_suites']}/{s['total_suites']} ({_pct(s['occupancy_pct'])})  "
                 f"| break-even at {s['break_even_occupancy_units']}/{s['total_suites']} "
                 f"({_pct(s['break_even_occupancy_pct'])})")
        L.append(f"  Rent roll: ${s['rent_roll_actual']:.0f} actual / ${s['rent_roll_potential']:.0f} potential  "
                 f"| vacancy costing ${s['vacancy_value_monthly']:.0f}/mo")
        L.append(f"  Expenses ${s['total_monthly_expenses']:.0f}  →  NET ${s['net']:.0f} "
                 f"({_pct(s['net_margin_pct'])})  | ${s['revenue_per_occupied_suite']:.0f}/occupied suite")
    if "combined_monthly_net" in result:
        L.append(f"\nCOMBINED monthly net (lash + suites): ${result['combined_monthly_net']:.0f}")
    L.append("\nEstimates for planning only — not tax/accounting advice. "
             "Benchmarks are general references, not guarantees.")
    return "\n".join(L)


def main(argv=None):
    p = argparse.ArgumentParser(description="Bloom pricing & financial calculator.")
    p.add_argument("--input", help="Path to input JSON (default: stdin).")
    p.add_argument("--demo", action="store_true", help="Run on the real Bloom seed numbers.")
    p.add_argument("--json-only", action="store_true", help="Emit only JSON.")
    args = p.parse_args(argv)

    if args.demo:
        data = demo_data()
    else:
        raw = open(args.input).read() if args.input else sys.stdin.read()
        data = json.loads(raw)
    result = analyze(data)

    if args.json_only:
        print(json.dumps(result, indent=2))
    else:
        print(render(result))
        print()
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
