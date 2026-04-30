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

    return values + [values[-1]] * (target_length - len(values))


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


def nearest_neighbor(domain, profiles):

    distances = []

    for other in profiles:

        if other == domain:
            continue

        d = trajectory_distance(
            profiles[domain],
            profiles[other]
        )

        distances.append((other, d))

    distances.sort(key=lambda x: x[1])

    return distances[0]


def build_clusters(profiles, threshold=1.5):

    assigned = set()
    clusters = []

    domains = list(profiles.keys())

    for domain in domains:

        if domain in assigned:
            continue

        cluster = [domain]
        assigned.add(domain)

        for other in domains:

            if other in assigned:
                continue

            d = trajectory_distance(
                profiles[domain],
                profiles[other]
            )

            if d <= threshold:
                cluster.append(other)
                assigned.add(other)

        clusters.append(cluster)

    return clusters


def main():

    print("\nOMNIA-INVARIANCE — Trajectory Clustering")
    print("=" * 80)

    profile_files = sorted(
        RESULTS_DIR.glob("*_invariance_profile.json")
    )

    profiles = {}

    for path in profile_files:
        data = load_json(path)
        domain = data.get("domain", path.stem)
        profiles[domain] = data

    print("\nNEAREST NEIGHBORS")
    print("=" * 80)

    for domain in profiles:

        neighbor, distance = nearest_neighbor(
            domain,
            profiles
        )

        print(f"\n{domain.upper()}")
        print("-" * 40)
        print(f"nearest neighbor: {neighbor}")
        print(f"distance: {round(distance, 4)}")

    print("\nCLUSTERS")
    print("=" * 80)

    clusters = build_clusters(
        profiles,
        threshold=1.5
    )

    for i, cluster in enumerate(clusters, start=1):

        print(f"\nCluster {i}")
        print("-" * 40)

        for item in cluster:
            print(item)

    print("\nINTERPRETATION")
    print("=" * 80)

    print("""
Clusters are currently generated using:

- pairwise trajectory distances
- simple threshold grouping

This is an initial unsupervised approximation of
trajectory-space organization.
""")

    print("DONE")


if __name__ == "__main__":
    main()