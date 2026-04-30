import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


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


def main():

    print("\nOMNIA-INVARIANCE — Trajectory Embedding")
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

        vector = build_feature_vector(data)

        profiles[domain] = vector

        vectors.append(vector)
        labels.append(domain)

    projection = pca_2d(vectors)

    plt.figure(figsize=(8, 6))

    x = projection[:, 0]
    y = projection[:, 1]

    plt.scatter(x, y)

    for xi, yi, label in zip(x, y, labels):
        plt.text(xi, yi, label.upper(), fontsize=10)

    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")

    plt.title("OMNIA-INVARIANCE Trajectory Embedding")

    plt.grid(True)

    output_path = RESULTS_DIR / "trajectory_embedding.png"

    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

    print("\nEMBEDDING COORDINATES")
    print("=" * 80)

    for label, xi, yi in zip(labels, x, y):

        print(f"\n{label.upper()}")
        print("-" * 40)
        print(f"PC1: {round(float(xi), 4)}")
        print(f"PC2: {round(float(yi), 4)}")

    print(f"\nSaved: {output_path}")

    print("\nDONE")


if __name__ == "__main__":
    main()