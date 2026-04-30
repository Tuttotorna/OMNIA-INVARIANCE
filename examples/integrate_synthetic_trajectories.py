import json
from pathlib import Path
from math import sqrt
from statistics import mean

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = ROOT / "results"
SYNTHETIC_DIR = RESULTS_DIR / "synthetic"


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
# HELPERS
# ============================================================

def clamp(v, low=0.0, high=1.0):
    return max(low, min(high, v))


def pad(values, target_length):

    if len(values) >= target_length:
        return values

    if not values:
        return [0.0] * target_length

    return values + [values[-1]] * (
        target_length - len(values)
    )


def euclidean_distance(a, b):

    return sqrt(
        sum((x - y) ** 2 for x, y in zip(a, b))
    )


# ============================================================
# FEATURE VECTOR
# ============================================================

def build_vector(profile, target_length=5):

    omega = profile.get("omega_trajectory", [])
    iri = profile.get("iri_trajectory", [])

    omega = pad(omega, target_length)
    iri = pad(iri, target_length)

    return omega + iri


# ============================================================
# DISTANCE
# ============================================================

def profile_distance(a, b):

    va = build_vector(a)
    vb = build_vector(b)

    return euclidean_distance(va, vb)


# ============================================================
# PCA
# ============================================================

def pca_2d(matrix):

    X = np.array(matrix)

    X_centered = X - X.mean(axis=0)

    covariance = np.cov(X_centered.T)

    eigenvalues, eigenvectors = np.linalg.eig(
        covariance
    )

    idx = np.argsort(eigenvalues)[::-1]

    eigenvectors = eigenvectors[:, idx]

    principal_components = eigenvectors[:, :2]

    projection = X_centered @ principal_components

    return projection.real


# ============================================================
# CLASSIFICATION
# ============================================================

def classify(profile):

    omega = profile.get("omega_trajectory", [])
    iri = profile.get("iri_trajectory", [])

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

    return "hybrid"


# ============================================================
# LOAD REAL DOMAINS
# ============================================================

def load_real_profiles():

    profiles = []

    for path in sorted(
        RESULTS_DIR.glob("*_invariance_profile.json")
    ):

        data = load_json(path)

        data["synthetic"] = False

        profiles.append(data)

    return profiles


# ============================================================
# LOAD SYNTHETICS
# ============================================================

def load_synthetic_profiles():

    profiles = []

    if not SYNTHETIC_DIR.exists():
        return profiles

    for path in sorted(
        SYNTHETIC_DIR.glob("*_profile.json")
    ):

        data = load_json(path)

        profiles.append(data)

    return profiles


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\nOMNIA-INVARIANCE — Synthetic Integration"
    )

    print("=" * 80)

    real_profiles = load_real_profiles()

    synthetic_profiles = load_synthetic_profiles()

    all_profiles = (
        real_profiles +
        synthetic_profiles
    )

    print("\nREAL DOMAINS")
    print("-" * 40)

    for p in real_profiles:
        print(p["domain"])

    print("\nSYNTHETIC DOMAINS")
    print("-" * 40)

    for p in synthetic_profiles:
        print(
            f"{p['domain']} "
            f"({p.get('family', 'unknown')})"
        )

    vectors = []

    for p in all_profiles:
        vectors.append(build_vector(p))

    projection = pca_2d(vectors)

    integrated = []

    print("\n" + "=" * 80)
    print("INTEGRATED SPACE")
    print("=" * 80)

    for i, profile in enumerate(all_profiles):

        domain = profile["domain"]

        nearest = None
        nearest_distance = None

        for other in all_profiles:

            if other["domain"] == domain:
                continue

            d = profile_distance(profile, other)

            if (
                nearest_distance is None
                or d < nearest_distance
            ):
                nearest_distance = d
                nearest = other["domain"]

        item = {

            "domain":
                domain,

            "synthetic":
                profile.get("synthetic", False),

            "family":
                profile.get("family", "real"),

            "trajectory_class":
                classify(profile),

            "embedding_pc1":
                round(float(projection[i][0]), 4),

            "embedding_pc2":
                round(float(projection[i][1]), 4),

            "nearest_neighbor":
                nearest,

            "nearest_distance":
                round(nearest_distance, 4)
        }

        integrated.append(item)

        print(f"\n{domain}")
        print("-" * 40)

        print(
            f"class: "
            f"{item['trajectory_class']}"
        )

        print(
            f"nearest: "
            f"{item['nearest_neighbor']}"
        )

        print(
            f"distance: "
            f"{item['nearest_distance']}"
        )

        print(
            f"PC1: "
            f"{item['embedding_pc1']}"
        )

        print(
            f"PC2: "
            f"{item['embedding_pc2']}"
        )

    output_path = (
        RESULTS_DIR /
        "integrated_trajectory_space.json"
    )

    save_json(output_path, integrated)

    print("\n" + "=" * 80)
    print("OUTPUT")
    print("=" * 80)

    print(output_path)

    print("\nDONE")


if __name__ == "__main__":
    main()