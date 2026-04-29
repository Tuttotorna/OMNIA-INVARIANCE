# OMNIA-INVARIANCE


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19895803.svg)](https://doi.org/10.5281/zenodo.19895803)


Cross-domain structural stability measurement across representations, perturbations, and invariant layers.

This repository does **not** claim a universal law.

It investigates whether different systems share comparable patterns of local fragility and global stability under controlled perturbation.

---

## Core question

```text
what remains structurally stable
when representation changes
and perturbation increases?


---

Core idea

A system can collapse in one representation while remaining stable in another.

OMNIA-INVARIANCE studies this pattern across domains:

chaotic physics

symbolic logic

language perturbation

numerical structure

synthetic systems


The goal is not to explain meaning.

The goal is to measure structural persistence.


---

First result — physics invariance profile

Source: OMNIA-THREE-BODY



Observed physics profile:

cartesian coordinates
→ fragile

pairwise distances
→ more fragile

total energy
→ relatively stable

angular momentum
→ almost invariant

center of mass
→ almost invariant

Interpretation:

local trajectory representations collapse,
while global invariant representations remain structurally stable.


---

Second result — symbolic logic invariance profile



Observed logic profile:

token layer
→ relatively stable

relation layer
→ partially collapsed

inference layer
→ partially collapsed

Interpretation:

surface similarity
does not guarantee
logical-structural persistence


---

First cross-domain comparison



The comparison does not claim that physics and logic are the same system.

It compares the shape of structural stability profiles across representation layers.

Current observation:

different domains
can show different local/global stability distributions
under controlled perturbation


---

Physics profile data

{
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


---

Logic profile data

{
  "token_layer": {
    "Omega": 0.8571428571428571,
    "IRI": 0.1428571428571429
  },
  "relation_layer": {
    "Omega": 0.5,
    "IRI": 0.5
  },
  "inference_layer": {
    "Omega": 0.5,
    "IRI": 0.5
  }
}


---

Cross-domain summary data

{
  "physics": {
    "mean_Omega": 0.6446806798878102,
    "mean_IRI": 1.6426090748396894
  },
  "logic": {
    "mean_Omega": 0.6190476190476191,
    "mean_IRI": 0.38095238095238093
  }
}


---

Minimal model

system
↓
representation layers
↓
controlled perturbation
↓
structural measurement
↓
stability profile
↓
cross-domain comparison


---

Metrics

Initial metrics:

T_delta — structural divergence time

Omega — residual structural coherence

IRI — irreversibility / accumulated divergence

representation stability profile

invariant persistence score



---

Generated outputs

Running the current demos generates:

results/
├── physics_invariance_profile.json
├── physics_invariance_profile.png
├── logic_invariance_profile.json
├── logic_invariance_profile.png
├── cross_domain_comparison.json
└── cross_domain_comparison.png


---

Run

Install dependencies:

pip install -r requirements.txt

Run physics profile:

python examples/invariance_physics_demo.py

Run logic profile:

python examples/invariance_logic_demo.py

Run cross-domain comparison:

python examples/cross_domain_comparison.py


---

Documentation

Detailed notes:

docs/CROSS_DOMAIN_INVARIANCE.md


---

Boundary

This repository does not claim:

universal consciousness metric

universal instability law

proof of physical ontology

equivalence between unrelated domains

replacement for domain science

prediction of exact future states


It is a measurement framework.


---

Canonical claim

OMNIA-INVARIANCE measures whether structural stability
is preserved across representation layers and perturbation regimes.


---

Ecosystem

Part of the MB-X.01 / OMNIA ecosystem.

Related repositories:

OMNIA
OMNIABASE
OMNIA-THREE-BODY
OMNIA-LIMIT
OMNIA-RADAR

Core principle:

measurement != inference != decision


---

Author

Massimiliano Brighindi
Project: MB-X.01