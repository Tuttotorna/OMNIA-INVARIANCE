import os
import json
import numpy as np
import matplotlib.pyplot as plt


os.makedirs("results", exist_ok=True)


with open("results/physics_invariance_profile.json", "r") as f:
    physics = json.load(f)

with open("results/logic_invariance_profile.json", "r") as f:
    logic = json.load(f)


physics_layers = list(physics.keys())
logic_layers = list(logic.keys())

physics_omega = [
    physics[layer]["Omega"]
    for layer in physics_layers
]

logic_omega = [
    logic[layer]["Omega"]
    for layer in logic_layers
]

physics_iri = [
    physics[layer]["IRI"]
    for layer in physics_layers
]

logic_iri = [
    logic[layer]["IRI"]
    for layer in logic_layers
]


cross_domain_summary = {
    "physics": {
        "layers": physics_layers,
        "Omega": physics_omega,
        "IRI": physics_iri,
        "mean_Omega": float(np.mean(physics_omega)),
        "mean_IRI": float(np.mean(physics_iri)),
    },
    "logic": {
        "layers": logic_layers,
        "Omega": logic_omega,
        "IRI": logic_iri,
        "mean_Omega": float(np.mean(logic_omega)),
        "mean_IRI": float(np.mean(logic_iri)),
    },
}


with open("results/cross_domain_comparison.json", "w") as f:
    json.dump(cross_domain_summary, f, indent=2)


fig = plt.figure(figsize=(14, 6))

ax1 = fig.add_subplot(1, 2, 1)

ax1.plot(
    range(len(physics_omega)),
    physics_omega,
    marker="o",
    linewidth=2,
    label="physics",
)

ax1.plot(
    range(len(logic_omega)),
    logic_omega,
    marker="o",
    linewidth=2,
    label="logic",
)

ax1.set_title("Residual Structural Coherence Across Domains")
ax1.set_xlabel("Representation layer index")
ax1.set_ylabel("Ω")
ax1.set_ylim(0, 1.05)
ax1.legend()
ax1.grid(True, alpha=0.3)


ax2 = fig.add_subplot(1, 2, 2)

ax2.plot(
    range(len(physics_iri)),
    physics_iri,
    marker="o",
    linewidth=2,
    label="physics",
)

ax2.plot(
    range(len(logic_iri)),
    logic_iri,
    marker="o",
    linewidth=2,
    label="logic",
)

ax2.set_title("Irreversibility Across Domains")
ax2.set_xlabel("Representation layer index")
ax2.set_ylabel("IRI")
ax2.legend()
ax2.grid(True, alpha=0.3)


fig.suptitle(
    "OMNIA-INVARIANCE — Cross-Domain Stability Comparison",
    fontsize=16,
)

plt.tight_layout()

plt.savefig(
    "results/cross_domain_comparison.png",
    dpi=300,
    bbox_inches="tight",
)

plt.show()


print("\nSaved:")
print("results/cross_domain_comparison.json")
print("results/cross_domain_comparison.png")