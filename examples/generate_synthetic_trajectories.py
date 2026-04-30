import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

random.seed(42)


# ============================================================
# IO
# ============================================================

def save_json(path, data):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ============================================================
# HELPERS
# ============================================================

def clamp(v, low=0.0, high=1.0):
    return max(low, min(high, round(v, 4)))


def noisy(values, scale=0.03):

    out = []

    for v in values:
        noise = random.uniform(-scale, scale)
        out.append(clamp(v + noise))

    return out


# ============================================================
# SYNTHETIC FAMILIES
# ============================================================

def rigid_collapse():

    omega = noisy([
        0.95,
        0.89,
        0.72,
        0.31,
        0.08
    ])

    iri = noisy([
        0.02,
        0.11,
        0.42,
        0.81,
        0.97
    ])

    return {
        "family": "rigid-collapse",
        "omega_trajectory": omega,
        "iri_trajectory": iri
    }


def smooth_degradation():

    omega = noisy([
        0.84,
        0.73,
        0.61,
        0.52,
        0.44
    ])

    iri = noisy([
        0.12,
        0.24,
        0.33,
        0.41,
        0.49
    ])

    return {
        "family": "smooth-degradation",
        "omega_trajectory": omega,
        "iri_trajectory": iri
    }


def recovery_dominant():

    omega = noisy([
        0.31,
        0.14,
        0.68,
        0.93,
        0.97
    ])

    iri = noisy([
        1.0,
        1.0,
        0.71,
        0.12,
        0.03
    ])

    return {
        "family": "recovery-dominant",
        "omega_trajectory": omega,
        "iri_trajectory": iri
    }


def hybrid():

    omega = noisy([
        0.91,
        0.77,
        0.48,
        0.63,
        0.41
    ])

    iri = noisy([
        0.05,
        0.19,
        0.57,
        0.44,
        0.66
    ])

    return {
        "family": "hybrid",
        "omega_trajectory": omega,
        "iri_trajectory": iri
    }


def oscillatory():

    omega = noisy([
        0.82,
        0.55,
        0.79,
        0.51,
        0.76
    ])

    iri = noisy([
        0.18,
        0.61,
        0.22,
        0.69,
        0.31
    ])

    return {
        "family": "oscillatory",
        "omega_trajectory": omega,
        "iri_trajectory": iri
    }


def chaotic():

    omega = noisy([
        0.91,
        0.33,
        0.74,
        0.21,
        0.67
    ])

    iri = noisy([
        0.11,
        1.0,
        0.38,
        1.0,
        0.52
    ])

    return {
        "family": "chaotic",
        "omega_trajectory": omega,
        "iri_trajectory": iri
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("\nOMNIA-INVARIANCE — Synthetic Trajectory Generator")
    print("=" * 80)

    generators = [
        rigid_collapse,
        smooth_degradation,
        recovery_dominant,
        hybrid,
        oscillatory,
        chaotic
    ]

    exported = []

    synthetic_dir = RESULTS_DIR / "synthetic"

    synthetic_dir.mkdir(exist_ok=True)

    for i, generator in enumerate(generators):

        data = generator()

        domain = f"synthetic_{i+1}"

        profile = {
            "domain": domain,
            "synthetic": True,
            "family": data["family"],
            "omega_trajectory":
                data["omega_trajectory"],
            "iri_trajectory":
                data["iri_trajectory"]
        }

        output_path = (
            synthetic_dir /
            f"{domain}_profile.json"
        )

        save_json(output_path, profile)

        exported.append(profile)

        print(f"\n{domain}")
        print("-" * 40)

        print(f"family: {profile['family']}")

        print("Ω:")
        print(profile["omega_trajectory"])

        print("IRI:")
        print(profile["iri_trajectory"])

    summary_path = (
        synthetic_dir /
        "synthetic_summary.json"
    )

    save_json(summary_path, exported)

    print("\n" + "=" * 80)
    print("SAVED FILES")
    print("=" * 80)

    for path in sorted(synthetic_dir.glob("*.json")):
        print(path.name)

    print("\nDONE")


if __name__ == "__main__":
    main()