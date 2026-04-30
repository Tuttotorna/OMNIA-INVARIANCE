import json
from pathlib import Path
from statistics import mean
from math import sqrt

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"


# ============================================================
# IO
# ============================================================

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ============================================================
# UTILITIES
# ============================================================

def pad(values, target_length):

    if len(values) >= target_length:
        return values

    if not values:
        return [0.0] * target_length

    return values + [values[-1]] * (target_length - len(values))


def euclidean_distance(a, b):
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


# ============================================================
# DISTANCE
# ============================================================

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


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_profile(data):

    omega = data.get("omega_trajectory", [])
    iri = data.get("iri_trajectory", [])

    if not omega or not iri:
        return "unknown"

    start_omega = omega[0]
    end_omega = omega[-1]

    max_omega = max(omega)
    min_omega = min(omega)

    start_iri = iri[0]
    end_iri = iri[-1]

    if (
        min_omega < start_omega
        and end_omega >= max_omega * 0.95
        and end_omega > start_omega
    ):
        return "recovery-dominant"

    if (
        start_omega >= 0.8
        and end_omega <= start_omega * 0.35
        and end_iri > start_iri
    ):
        return "rigid-collapse"

    if (
        end_omega < start_omega
        and end_omega >= start_omega * 0.5
    ):
        return "smooth-degradation"

    return "unknown"


# ============================================================
# MORPHOMETRICS
# ============================================================

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


# ============================================================
# EMBEDDING
# ============================================================

def build_feature_vector(profile, target_length=5):

    omega = profile.get("omega_trajectory", [])
    iri = profile.get("iri_trajectory", [])

    omega = pad(omega, target_length)
    iri = pad(iri, target_length)

    return omega + iri


def pca_2d(matrix):

    X = np.array(matrix)

    X_centered = X - X.mean(axis=0)

    covariance = np.cov(X_centered.T)

    eigenvalues, eigenvectors = np.linalg.eig(covariance)

    idx = np.argsort(eigenvalues)[::-1]

    eigenvectors = eigenvectors[:, idx]

    principal_components = eigenvectors[:, :2]

    projection = X_centered @ principal_components

    return projection.real


# ============================================================
# MAIN
# ============================================================

def main():

    print("\nOMNIA-INVARIANCE — Export Trajectory Features")
    print("=" * 80)

    profile_files = sorted(
        RESULTS_DIR.glob("*_invariance_profile.json")
    )

    profiles = {}
    vectors = []
    labels = []

    for path in profile_files:

        data = load_json(path)

        domain = data.get("domain", path.stem)

        profiles[domain] = data

        vectors.append(build_feature_vector(data))
        labels.append(domain)

    projection = pca_2d(vectors)

    exported = []

    for i, domain in enumerate(labels):

        profile = profiles[domain]

        omega = profile.get("omega_trajectory", [])
        iri = profile.get("iri_trajectory", [])

        nearest_neighbor = None
        nearest_distance = None

        for other in labels:

            if other == domain:
                continue

            d = trajectory_distance(
                profile,
                profiles[other]
            )

            if nearest_distance is None or d < nearest_distance:
                nearest_distance = d
                nearest_neighbor = other

        exported.append({
            "domain": domain,

            "trajectory_class":
                classify_profile(profile),

            "mean_omega":
                round(mean(omega), 4),

            "mean_iri":
                round(mean(iri), 4),

            "collapse_sharpness":
                round(max_drop(omega), 4),

            "recovery_strength":
                round(recovery_strength(omega), 4),

            "omega_volatility":
                round(volatility(omega), 4),

            "iri_growth_rate":
                round(growth_rate(iri), 4),

            "iri_volatility":
                round(volatility(iri), 4),

            "stability_span":
                stability_span(omega),

            "trajectory_length":
                len(omega),

            "embedding_pc1":
                round(float(projection[i][0]), 4),

            "embedding_pc2":
                round(float(projection[i][1]), 4),

            "nearest_neighbor":
                nearest_neighbor,

            "nearest_distance":
                round(nearest_distance, 4)
        })

    output_path = RESULTS_DIR / "trajectory_feature_table.json"

    save_json(output_path, exported)

    print(f"\nSaved: {output_path}")

    print("\nEXPORTED DOMAINS")
    print("=" * 80)

    for item in exported:

        print(f"\n{item['domain'].upper()}")
        print("-" * 40)

        print(f"class: {item['trajectory_class']}")
        print(f"nearest: {item['nearest_neighbor']}")
        print(f"distance: {item['nearest_distance']}")

    print("\nDONE")


if __name__ == "__main__":
    main()