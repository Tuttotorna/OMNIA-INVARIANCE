import json
from pathlib import Path
from math import sqrt

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


# ============================================================
# HELPERS
# ============================================================

def euclidean_distance(a, b):

    return sqrt(
        sum((x - y) ** 2 for x, y in zip(a, b))
    )


def pad(values, target_length):

    if len(values) >= target_length:
        return values

    if not values:
        return [0.0] * target_length

    return values + [values[-1]] * (
        target_length - len(values)
    )


# ============================================================
# NORMALIZATION
# ============================================================

def minmax(values):

    if not values:
        return values

    vmin = min(values)
    vmax = max(values)

    if vmax == vmin:
        return [0.0 for _ in values]

    return [
        round((v - vmin) / (vmax - vmin), 4)
        for v in values
    ]


# ============================================================
# VECTOR BUILDING
# ============================================================

def build_vector(profile):

    omega = pad(
        profile.get("omega_trajectory", []),
        5
    )

    iri = pad(
        profile.get("iri_trajectory", []),
        5
    )

    omega_norm = minmax(omega)
    iri_norm = minmax(iri)

    return omega_norm + iri_norm


# ============================================================
# DISTANCE
# ============================================================

def distance(a, b):

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

    pcs = eigenvectors[:, :2]

    projection = X_centered @ pcs

    return projection.real


# ============================================================
# LOAD PROFILES
# ============================================================

def load_profiles():

    profiles = []

    for path in sorted(
        RESULTS_DIR.glob("*_invariance_profile.json")
    ):

        data = load_json(path)

        data["synthetic"] = False

        profiles.append(data)

    if SYNTHETIC_DIR.exists():

        for path in sorted(
            SYNTHETIC_DIR.glob("*_profile.json")
        ):

            data = load_json(path)

            data["synthetic"] = True

            profiles.append(data)

    return profiles


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\nOMNIA-INVARIANCE — "
        "Normalized Trajectory Space"
    )

    print("=" * 80)

    profiles = load_profiles()

    vectors = [
        build_vector(p)
        for p in profiles
    ]

    projection = pca_2d(vectors)

    print("\nNORMALIZED SPACE")
    print("=" * 80)

    exported = []

    for i, p in enumerate(profiles):

        domain = p["domain"]

        nearest = None
        nearest_distance = None

        for other in profiles:

            if other["domain"] == domain:
                continue

            d = distance(p, other)

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
                p.get("synthetic", False),

            "nearest_neighbor":
                nearest,

            "nearest_distance":
                round(nearest_distance, 4),

            "embedding_pc1":
                round(float(projection[i][0]), 4),

            "embedding_pc2":
                round(float(projection[i][1]), 4)
        }

        exported.append(item)

        print(f"\n{domain}")
        print("-" * 40)

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
        "normalized_trajectory_space.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(exported, f, indent=2)

    print("\n" + "=" * 80)
    print("OUTPUT")
    print("=" * 80)

    print(output_path)

    print("\nDONE")


if __name__ == "__main__":
    main()