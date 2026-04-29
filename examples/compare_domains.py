import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"


DOMAIN_FILES = {
    "crypto": RESULTS_DIR / "crypto_invariance_profile.json",
    "summary": RESULTS_DIR / "cross_domain_summary.json",
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def print_domain_summary(name, data):
    summary = data.get("summary", {})

    print(f"\nDOMAIN: {name}")
    print("-" * 40)
    print(f"mean Ω  : {summary.get('mean_omega')}")
    print(f"mean IRI: {summary.get('mean_iri')}")
    print(f"collapse point: {data.get('collapse_point')}")

    omega = data.get("omega_trajectory")
    iri = data.get("iri_trajectory")

    if omega:
        print("Ω trajectory:")
        print(" -> ".join(str(x) for x in omega))

    if iri:
        print("IRI trajectory:")
        print(" -> ".join(str(x) for x in iri))


def print_cross_domain_summary(data):
    print("\nCROSS-DOMAIN SUMMARY")
    print("=" * 40)

    domains = data.get("domains", {})

    for name, values in domains.items():
        print(f"\n{name.upper()}")
        print("-" * 40)
        print(f"mean Ω  : {values.get('mean_omega')}")
        print(f"mean IRI: {values.get('mean_iri')}")

        notes = values.get("notes", [])
        if notes:
            print("notes:")
            for note in notes:
                print(f"- {note}")

    print("\nCANONICAL OBSERVATION")
    print("-" * 40)
    print(data.get("canonical_observation"))

    print("\nBOUNDARY")
    print("-" * 40)
    for item in data.get("boundary", []):
        print(f"- {item}")


def main():
    print("OMNIA-INVARIANCE — Cross-Domain Comparison")
    print("=" * 40)

    crypto_path = DOMAIN_FILES["crypto"]
    summary_path = DOMAIN_FILES["summary"]

    if crypto_path.exists():
        crypto = load_json(crypto_path)
        print_domain_summary("crypto", crypto)
    else:
        print(f"Missing file: {crypto_path}")

    if summary_path.exists():
        summary = load_json(summary_path)
        print_cross_domain_summary(summary)
    else:
        print(f"Missing file: {summary_path}")


if __name__ == "__main__":
    main()