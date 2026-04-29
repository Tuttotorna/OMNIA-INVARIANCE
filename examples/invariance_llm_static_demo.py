import os
import json
import numpy as np
import matplotlib.pyplot as plt


os.makedirs("results", exist_ok=True)


reference = {
    "tokens": [
        "John",
        "has",
        "3",
        "apples",
        "he",
        "buys",
        "2",
        "more",
        "total",
        "5"
    ],

    "reasoning_steps": [
        "initial_apples=3",
        "purchased=2",
        "3+2=5"
    ],

    "final_answer": [
        "5"
    ]
}


perturbed = {
    "tokens": [
        "John",
        "has",
        "3",
        "apples",
        "he",
        "buys",
        "2",
        "additional",
        "total",
        "6"
    ],

    "reasoning_steps": [
        "initial_apples=3",
        "purchased=2",
        "3+2=6"
    ],

    "final_answer": [
        "6"
    ]
}


def jaccard_similarity(a, b):
    a = set(a)
    b = set(b)

    if not a and not b:
        return 1.0

    return len(a.intersection(b)) / len(a.union(b))


def omega(similarity):
    return float(similarity)


def iri(similarity):
    return float(1.0 - similarity)


token_similarity = jaccard_similarity(
    reference["tokens"],
    perturbed["tokens"]
)

reasoning_similarity = jaccard_similarity(
    reference["reasoning_steps"],
    perturbed["reasoning_steps"]
)

answer_similarity = jaccard_similarity(
    reference["final_answer"],
    perturbed["final_answer"]
)


results = {
    "token_layer": {
        "Omega": omega(token_similarity),
        "IRI": iri(token_similarity)
    },

    "reasoning_layer": {
        "Omega": omega(reasoning_similarity),
        "IRI": iri(reasoning_similarity)
    },

    "answer_layer": {
        "Omega": omega(answer_similarity),
        "IRI": iri(answer_similarity)
    }
}


with open("results/llm_invariance_profile.json", "w") as f:
    json.dump(results, f, indent=2)


layers = list(results.keys())

omega_values = [
    results[layer]["Omega"]
    for layer in layers
]

iri_values = [
    results[layer]["IRI"]
    for layer in layers
]


fig = plt.figure(figsize=(10, 5))

ax1 = fig.add_subplot(1, 2, 1)

ax1.bar(layers, omega_values)

ax1.set_title("Residual Structural Coherence")
ax1.set_ylabel("Ω")
ax1.set_ylim(0, 1.05)

ax2 = fig.add_subplot(1, 2, 2)

ax2.bar(layers, iri_values)

ax2.set_title("Irreversibility")
ax2.set_ylabel("IRI")

fig.suptitle(
    "OMNIA-INVARIANCE — LLM Stability Profile",
    fontsize=16
)

plt.tight_layout()

plt.savefig(
    "results/llm_invariance_profile.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\nSaved:")
print("results/llm_invariance_profile.json")
print("results/llm_invariance_profile.png")