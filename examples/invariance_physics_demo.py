import os
import json
import numpy as np
import matplotlib.pyplot as plt


os.makedirs("results", exist_ok=True)


physics_results = {
    "cartesian_coordinates": {
        "T_delta": 1345,
        "Omega": 0.33353144232183113,
        "IRI": 1.9982180781477268
    },
    "pairwise_distances": {
        "T_delta": 827,
        "Omega": 0.14553109791625538,
        "IRI": 5.871383603354944
    },
    "total_energy": {
        "T_delta": -1,
        "Omega": 0.7443741914232316,
        "IRI": 0.3434103593624276
    },
    "angular_momentum": {
        "T_delta": -1,
        "Omega": 0.9999999999999933,
        "IRI": 6.7288397076481484e-15
    },
    "center_of_mass": {
        "T_delta": -1,
        "Omega": 0.9999666677777395,
        "IRI": 3.333333333474693e-05
    }
}


with open(
    "results/physics_invariance_profile.json",
    "w"
) as f:
    json.dump(
        physics_results,
        f,
        indent=2,
    )


names = list(physics_results.keys())

omega = [
    physics_results[n]["Omega"]
    for n in names
]

iri = [
    physics_results[n]["IRI"]
    for n in names
]


fig = plt.figure(figsize=(12, 5))

ax1 = fig.add_subplot(1, 2, 1)

ax1.bar(names, omega)

ax1.set_title("Residual Structural Coherence")
ax1.set_ylabel("Ω")
ax1.tick_params(axis="x", rotation=35)

ax2 = fig.add_subplot(1, 2, 2)

ax2.bar(names, iri)

ax2.set_title("Irreversibility")
ax2.set_ylabel("IRI")
ax2.tick_params(axis="x", rotation=35)

fig.suptitle(
    "OMNIA-INVARIANCE — Physics Stability Profile",
    fontsize=16,
)

plt.tight_layout()

plt.savefig(
    "results/physics_invariance_profile.png",
    dpi=300,
    bbox_inches="tight",
)

plt.show()


print("\nSaved:")
print("results/physics_invariance_profile.json")
print("results/physics_invariance_profile.png")