import json
from pathlib import Path
from math import sqrt

import matplotlib.pyplot as plt


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

    return omega_distance + iri_distance


def main():

    print("\nOMNIA-INVARIANCE — Trajectory Space Map")
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

    if len(domains) < 2:
        print("\nNeed at least two domains.")
        return

    reference = domains[0]

    x_positions = []
    y_positions = []
    labels = []

    for domain in domains:

        profile = profiles[domain]
        ref_profile = profiles[reference]

        distance_to_reference = trajectory_distance(
            profile,
            ref_profile
        )

        omega = profile.get("omega_trajectory", [])

        mean_omega = (
            sum(omega) / len(omega)
            if omega else 0.0
        )

        x_positions.append(distance_to_reference)
        y_positions.append(mean_omega)
        labels.append(domain)

    plt.figure(figsize=(10, 6))

    plt.scatter(x_positions, y_positions)

    for x, y, label in zip(x_positions, y_positions, labels):
        plt.text(x, y, label.upper(), fontsize=10)

    plt.xlabel(f"Distance from {reference.upper()}")
    plt.ylabel("Mean Ω")
    plt.title("OMNIA-INVARIANCE Trajectory Space")

    plt.grid(True)

    output_path = RESULTS_DIR / "trajectory_space_map.png"

    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

    print(f"\nSaved: {output_path}")
    print("\nDONE")


if __name__ == "__main__":
    main()