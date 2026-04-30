import json
from pathlib import Path
from math import sqrt


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def pad(values, target_length):
    if len(values) >= target_length:
        return values

    if not values:
        return [0.0] * target_length

    last = values[-1]

    return values + [last] * (target_length - len(values))


def euclidean_distance(a, b):
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def trajectory_distance(profile_a, profile_b):

    omega_a = profile_a.get("omega_trajectory", [])
    omega_b = profile_b.get("omega_trajectory", [])

    iri_a = profile_a.get("iri_trajectory", [])
    iri_b = profile_b.get("iri_trajectory", [])

    max_len_omega = max(len(omega_a), len(omega_b))
    max_len_iri = max(len(iri_a), len(iri_b))

    omega_a = pad(omega_a, max_len_omega)
    omega_b = pad(omega_b, max_len_omega)

    iri_a = pad(iri_a, max_len_iri)
    iri_b = pad(iri_b, max_len_iri)

    omega_distance = euclidean_distance(omega_a, omega_b)
    iri_distance = euclidean_distance(iri_a, iri_b)

    total_distance = omega_distance + iri_distance

    return round(total_distance, 4)


def main():

    print("\nOMNIA-INVARIANCE — Trajectory Distance Matrix")
    print("=" * 80)

    profile_files = sorted(
        RESULTS_DIR.glob("*_invariance_profile.json")
    )

    profiles = {}

    for path in profile_files:
        data = load_json(path)
        domain = data.get("domain", path.stem)
        profiles[domain] = data

    domains = sorted(profiles.keys())

    print("\nDISTANCE MATRIX")
    print("=" * 80)

    header = "domain".ljust(12)

    for d in domains:
        header += d.ljust(12)

    print(header)
    print("-" * (12 * (len(domains) + 1)))

    for d1 in domains:

        row = d1.ljust(12)

        for d2 in domains:

            distance = trajectory_distance(
                profiles[d1],
                profiles[d2]
            )

            row += str(distance).ljust(12)

        print(row)

    print("\nINTERPRETATION")
    print("=" * 80)

    print("""
Lower values indicate more similar trajectory behavior.

Distances currently combine:

- Ω trajectory distance
- IRI trajectory distance

using simple Euclidean comparison.

This is an initial geometric approximation of trajectory similarity.
""")

    print("DONE")


if __name__ == "__main__":
    main()