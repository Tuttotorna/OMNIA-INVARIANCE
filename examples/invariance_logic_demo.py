import os
import json
import numpy as np
import matplotlib.pyplot as plt


os.makedirs("results", exist_ok=True)


original = {
    "tokens": ["A", "implies", "B", "B", "implies", "C", "therefore", "A", "implies", "C"],
    "relations": [
        ("A", "B"),
        ("B", "C"),
        ("A", "C")
    ],
    "inference_chain": ["A->B", "B->C", "A->C"]
}


perturbed = {
    "tokens": ["A", "implies", "B", "B", "implies", "D", "therefore", "A", "implies", "C"],
    "relations": [
        ("A", "B"),
        ("B", "D"),
        ("A", "C")
    ],
    "inference_chain": ["A->B", "B->D", "A->C"]
}


def jaccard_similarity(a, b):
    a = set(a)
    b = set(b)

    if not a and not b:
        return 1.0

    return len(a.intersection(b)) / len(a.union(b))


def omega_from_similarity(similarity):
    return float(similarity)


def iri_from_similarity(similarity):
    return float(1.0 - similarity)


def relation_to_string(rel):
    return f"{rel[0]}->{rel[1]}"


token_similarity = jaccard_similarity(
    original["tokens"],
    perturbed["tokens"],
)

relation_similarity = jaccard_similarity(
    [relation_to_string(r) for r in original["relations"]],
    [relation_to_string(r) for r in perturbed["relations"]],
)

inference_similarity = jaccard_similarity(
    original["inference_chain"],
    perturbed["inference_chain"],
)


logic_results = {
    "token_layer": {
        "Omega": omega_from_similarity(token_similarity),
        "IRI": iri_from_similarity(token_similarity),
    },
    "relation_layer": {
        "Omega": omega_from_similarity(relation_similarity),
        "IRI": iri_from_similarity(relation_similarity),
    },
    "inference_layer": {
        "Omega": omega_from_similarity(inference_similarity),
        "IRI": iri_from_similarity(inference_similarity),
    },
}


with open("results/logic_invariance_profile.json", "w") as f:
    json.dump(logic_results, f, indent=2)


names = list(logic_results.keys())

omega = [
    logic_results[n]["Omega"]
    for n in names
]

iri = [
    logic_results[n]["IRI"]
    for n in names
]


fig = plt.figure(figsize=(10, 5))

ax1 = fig.add_subplot(1, 2, 1)

ax1.bar(names, omega)

ax1.set_title("Residual Structural Coherence")
ax1.set_ylabel("Ω")
ax1.tick_params(axis="x", rotation=25)

ax2 = fig.add_subplot(1, 2, 2)

ax2.bar(names, iri)

ax2.set_title("Irreversibility")
ax2.set_ylabel("IRI")
ax2.tick_params(axis="x", rotation=25)

fig.suptitle(
    "OMNIA-INVARIANCE — Logic Stability Profile",
    fontsize=16,
)

plt.tight_layout()

plt.savefig(
    "results/logic_invariance_profile.png",
    dpi=300,
    bbox_inches="tight",
)

plt.show()


print("\nSaved:")
print("results/logic_invariance_profile.json")
print("results/logic_invariance_profile.png")