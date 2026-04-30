import json
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def max_drop(values):
    if len(values) < 2:
        return 0.0

    drops = [
        values[i] - values[i + 1]
        for i in range(len(values) - 1)
    ]

    return max(drops)


def recovery_strength(values):
    if not values:
        return 0.0

    min_value = min(values)
    min_index = values.index(min_value)
    after_min = values[min_index:]

    return max(after_min) - min_value


def volatility(values):
    if len(values) < 2:
        return 0.0

    diffs = [
        abs(values[i + 1] - values[i])
        for i in range(len(values) - 1)
    ]

    return mean(diffs)


def growth_rate(values):
    if len(values) < 2:
        return 0.0

    return (values[-1] - values[0]) / (len(values) - 1)


def stability_span(values, threshold=0.75):
    return sum(1 for v in values if v >= threshold)


def compute_morphometrics(data):

    omega = data.get("omega_trajectory", [])
    iri = data.get("iri_trajectory", [])

    return {
        "domain": data.get("domain", "unknown"),
        "collapse_sharpness": round(max_drop(omega), 4),
        "recovery_strength": round(recovery_strength(omega), 4),
        "omega_volatility": round(volatility(omega), 4),
        "iri_growth_rate": round(growth_rate(iri), 4),
        "iri_volatility": round(volatility(iri), 4),
        "stability_span": stability_span(omega),
        "trajectory_length": len(omega)
    }


def main():

    print("\nOMNIA-INVARIANCE — Trajectory Morphometrics")
    print("=" * 80)

    profile_files = sorted(
        RESULTS_DIR.glob("*_invariance_profile.json")
    )

    if not profile_files:
        print("\nNo profiles found.")
        return

    rows = []

    for path in profile_files:
        data = load_json(path)
        rows.append(compute_morphometrics(data))

    headers = [
        "domain",
        "collapse_sharpness",
        "recovery_strength",
        "omega_volatility",
        "iri_growth_rate",
        "iri_volatility",
        "stability_span",
        "trajectory_length"
    ]

    print(" | ".join(headers))
    print("-" * 120)

    for row in rows:
        print(" | ".join(str(row[h]) for h in headers))

    print("\nDONE")


if __name__ == "__main__":
    main()