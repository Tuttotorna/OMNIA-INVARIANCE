import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_trajectory(values):
    return " -> ".join(str(x) for x in values)


def print_domain_profile(data):

    domain = data.get("domain", "unknown")
    summary = data.get("summary", {})

    print(f"\nDOMAIN: {domain.upper()}")
    print("-" * 40)

    print(f"mean Ω  : {summary.get('mean_omega')}")
    print(f"mean IRI: {summary.get('mean_iri')}")

    collapse = data.get("collapse_point")
    if collapse is not None:
        print(f"collapse point: {collapse}")

    omega = data.get("omega_trajectory")
    iri = data.get("iri_trajectory")

    if omega:
        print("\nΩ trajectory:")
        print(format_trajectory(omega))

    if iri:
        print("\nIRI trajectory:")
        print(format_trajectory(iri))

    interpretation = data.get("interpretation", {})
    behavior = interpretation.get("behavior")

    if behavior:
        print("\nbehavior:")
        print(f"- {behavior}")

    notes = interpretation.get("notes", [])

    if notes:
        print("\nnotes:")
        for note in notes:
            print(f"- {note}")


def print_cross_domain_summary(data):

    print("\n" + "=" * 60)
    print("CROSS-DOMAIN SUMMARY")
    print("=" * 60)

    domains = data.get("domains", {})

    for name, values in domains.items():

        print(f"\n{name.upper()}")
        print("-" * 40)

        print(f"mean Ω  : {values.get('mean_omega')}")
        print(f"mean IRI: {values.get('mean_iri')}")

        notes = values.get("notes", [])

        if notes:
            print("\nnotes:")
            for note in notes:
                print(f"- {note}")

    observation = data.get("canonical_observation")

    if observation:
        print("\nCANONICAL OBSERVATION")
        print("-" * 40)
        print(observation)

    boundary = data.get("boundary", [])

    if boundary:
        print("\nBOUNDARY")
        print("-" * 40)

        for item in boundary:
            print(f"- {item}")


def main():

    print("\nOMNIA-INVARIANCE — Automatic Cross-Domain Comparison")
    print("=" * 60)

    profile_files = sorted(
        RESULTS_DIR.glob("*_invariance_profile.json")
    )

    if not profile_files:
        print("\nNo invariance profiles found.")
        return

    print("\nDETECTED PROFILES")
    print("-" * 40)

    for path in profile_files:
        print(path.name)

    for path in profile_files:

        try:
            data = load_json(path)
            print_domain_profile(data)

        except Exception as e:
            print(f"\nERROR reading {path.name}")
            print(e)

    summary_path = RESULTS_DIR / "cross_domain_summary.json"

    if summary_path.exists():

        try:
            summary = load_json(summary_path)
            print_cross_domain_summary(summary)

        except Exception as e:
            print("\nERROR reading cross-domain summary")
            print(e)

    print("\nDONE")


if __name__ == "__main__":
    main()