import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def discover_profiles():
    return sorted(
        RESULTS_DIR.glob("*_invariance_profile.json")
    )


def plot_metric(metric_name, output_name, title):

    profiles = discover_profiles()

    plt.figure(figsize=(10, 6))

    for path in profiles:

        data = load_json(path)

        domain = data.get("domain", path.stem)

        values = data.get(metric_name)

        if not values:
            continue

        x = list(range(len(values)))

        plt.plot(
            x,
            values,
            marker="o",
            label=domain.upper()
        )

    plt.title(title)
    plt.xlabel("Perturbation Step")
    plt.ylabel(metric_name)
    plt.grid(True)
    plt.legend()

    output_path = RESULTS_DIR / output_name

    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output_path}")


def main():

    print("\nOMNIA-INVARIANCE — Cross-Domain Trajectory Plots")
    print("=" * 60)

    plot_metric(
        metric_name="omega_trajectory",
        output_name="cross_domain_omega.png",
        title="Cross-Domain Ω Trajectories"
    )

    plot_metric(
        metric_name="iri_trajectory",
        output_name="cross_domain_iri.png",
        title="Cross-Domain IRI Trajectories"
    )

    print("\nDONE")


if __name__ == "__main__":
    main()