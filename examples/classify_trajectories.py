import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


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

    # --------------------------------------------------------
    # Recovery-dominant
    # --------------------------------------------------------

    if (
        min_omega < start_omega
        and end_omega >= max_omega * 0.95
        and end_omega > start_omega
    ):
        return "recovery-dominant"

    # --------------------------------------------------------
    # Rigid-collapse
    # --------------------------------------------------------

    if (
        start_omega >= 0.8
        and end_omega <= start_omega * 0.35
        and end_iri > start_iri
    ):
        return "rigid-collapse"

    # --------------------------------------------------------
    # Smooth-degradation
    # --------------------------------------------------------

    if (
        end_omega < start_omega
        and end_omega >= start_omega * 0.5
    ):
        return "smooth-degradation"

    return "unknown"


def main():

    print("\nOMNIA-INVARIANCE — Trajectory Classification")
    print("=" * 60)

    profile_files = sorted(
        RESULTS_DIR.glob("*_invariance_profile.json")
    )

    if not profile_files:
        print("\nNo profiles found.")
        return

    results = {}

    for path in profile_files:

        try:
            data = load_json(path)

            domain = data.get("domain", path.stem)

            trajectory_class = classify_profile(data)

            results[domain] = trajectory_class

            print(f"\n{domain.upper()}")
            print("-" * 40)
            print(f"classification: {trajectory_class}")

        except Exception as e:
            print(f"\nERROR reading {path.name}")
            print(e)

    print("\nSUMMARY")
    print("=" * 60)

    for domain, cls in results.items():
        print(f"{domain:<12} -> {cls}")

    print("\nDONE")


if __name__ == "__main__":
    main()