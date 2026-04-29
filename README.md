# OMNIA-INVARIANCE

OMNIA-INVARIANCE is an executable cross-domain framework for comparing structural stability and collapse trajectories under controlled perturbation.

It does not claim that different domains are semantically equivalent.

It does not prove a universal law.

It provides a shared metrological frame for measuring how different systems preserve, lose, recover, or collapse structural coherence when transformed.

---

## Core Claim

Different domains can be compared through shared structural stability trajectories.

The central question is:

```text
How does structure behave under controlled transformation?
```

OMNIA-INVARIANCE measures that behavior using standardized profiles.

---

## What this repository does

This repository compares structural trajectories across domains such as:

- physics
- logic
- LLM behavior
- crypto-like structures

Each domain is represented through a canonical invariance profile containing:

- Ω trajectory
- IRI trajectory
- collapse point
- mean Ω
- mean IRI
- structural interpretation

The goal is not semantic comparison.

The goal is structural comparison.

---

## What this repository is not

OMNIA-INVARIANCE is not:

- a semantic oracle
- a proof of universal structure
- a final theory of reality
- a replacement for domain science
- a claim that all systems are the same
- a claim that Ω is already a universal constant

It measures structural behavior under perturbation.

Interpretation remains separate from measurement.

---

## Canonical Metrics

| Metric | Meaning |
|---|---|
| Ω | structural coherence |
| IRI | irreversibility / non-recoverable structural loss |
| ΔΩ | variation in coherence |
| Collapse Point | perturbation step where collapse becomes dominant |
| Stability Profile | full structural trajectory under transformation |

These metrics are treated as structural signals.

They are not treated as final truth.

---

## Current Standardized Domains

The current multi-domain run includes:

| Domain | mean Ω | mean IRI | Preliminary trajectory class |
|---|---:|---:|---|
| Crypto | 0.598 | 0.436 | rigid-collapse |
| LLM | 0.602 | 0.408 | rigid-collapse |
| Logic | 0.619 | 0.393 | smooth-degradation |
| Physics | 0.644 | 1.650 | recovery-dominant |

The main observation is:

```text
mean Ω values are relatively close across domains,
while IRI behavior differs strongly.
```

This suggests that:

```text
coherence persistence != irreversibility behavior
```

This is the most important current result.

---

## Current Trajectories

### Crypto

```text
Ω:
0.91 -> 0.82 -> 0.67 -> 0.41 -> 0.18

IRI:
0.02 -> 0.11 -> 0.39 -> 0.72 -> 0.94
```

Preliminary interpretation:

```text
high initial rigidity followed by rapid collapse after perturbation accumulation
```

---

### LLM

```text
Ω:
0.92 -> 0.81 -> 0.63 -> 0.44 -> 0.21

IRI:
0.04 -> 0.12 -> 0.31 -> 0.66 -> 0.91
```

Preliminary interpretation:

```text
high apparent coherence with progressive instability under perturbation accumulation
```

---

### Logic

```text
Ω:
0.83 -> 0.50 -> 0.50

IRI:
0.18 -> 0.50 -> 0.50
```

Preliminary interpretation:

```text
moderate coherence persistence under symbolic degradation
```

---

### Physics

```text
Ω:
0.33 -> 0.15 -> 0.74 -> 1.00 -> 1.00

IRI:
2.00 -> 5.90 -> 0.35 -> 0.00 -> 0.00
```

Preliminary interpretation:

```text
initial instability followed by strong recovery and global structural persistence
```

---

## Preliminary Trajectory Classes

OMNIA-INVARIANCE currently identifies three experimental trajectory classes.

These are not universal categories.

They are observed structural response patterns.

---

### 1. Rigid-Collapse

Observed in:

- crypto
- LLM

Typical behavior:

```text
high initial coherence
slow early degradation
threshold-sensitive collapse
rapid irreversibility growth
```

---

### 2. Smooth-Degradation

Observed in:

- logic

Typical behavior:

```text
moderate coherence persistence
gradual degradation
limited collapse acceleration
stable irreversibility growth
```

---

### 3. Recovery-Dominant

Observed in:

- physics

Typical behavior:

```text
early instability
strong recovery
global structural persistence
irreversibility normalization
```

---

## Generated Visual Outputs

The repository includes generated cross-domain plots:

```text
results/cross_domain_omega.png
results/cross_domain_iri.png
```

These plots show:

- Ω trajectories across domains
- IRI trajectories across domains
- visible differences between collapse, degradation, and recovery profiles

---

## Repository Structure

```text
OMNIA-INVARIANCE/
│
├── docs/
│   ├── CANONICAL_TRAJECTORY_FORMAT.md
│   ├── CROSS_DOMAIN_METROLOGY_FRAME.md
│   ├── CRYPTO_DOMAIN_OBSERVATIONS.md
│   ├── MULTI_DOMAIN_RUN_INTERPRETATION.md
│   └── TRAJECTORY_CLASSES.md
│
├── domains/
│   └── crypto/
│       └── README.md
│
├── examples/
│   ├── compare_domains.py
│   ├── plot_cross_domain_trajectories.py
│   ├── invariance_physics_demo.py
│   ├── invariance_logic_demo.py
│   └── invariance_llm_static_demo.py
│
├── results/
│   ├── crypto_invariance_profile.json
│   ├── llm_invariance_profile.json
│   ├── logic_invariance_profile.json
│   ├── physics_invariance_profile.json
│   ├── cross_domain_summary.json
│   ├── cross_domain_omega.png
│   ├── cross_domain_iri.png
│   └── latest_colab_run.txt
│
├── README.md
├── requirements.txt
└── LICENSE
```

---

## Run the Cross-Domain Comparison

From the repository root:

```bash
python examples/compare_domains.py
```

This automatically discovers all files matching:

```text
*_invariance_profile.json
```

inside:

```text
results/
```

and prints the standardized cross-domain comparison.

---

## Generate the Cross-Domain Plots

```bash
python examples/plot_cross_domain_trajectories.py
```

This generates:

```text
results/cross_domain_omega.png
results/cross_domain_iri.png
```

---

## Canonical Profile Format

Each standardized domain profile follows this structure:

```json
{
  "domain": "domain_name",
  "experiment": "experiment_name",
  "description": "description",

  "omega_trajectory": [],
  "iri_trajectory": [],

  "collapse_point": 0,

  "summary": {
    "mean_omega": 0.0,
    "mean_iri": 0.0
  },

  "interpretation": {
    "behavior": "short structural interpretation",
    "notes": []
  }
}
```

This format makes new domains directly comparable.

---

## Current Supported Workflow

```text
1. Add or generate a domain invariance profile
2. Save it as results/<domain>_invariance_profile.json
3. Run examples/compare_domains.py
4. Generate plots with examples/plot_cross_domain_trajectories.py
5. Interpret trajectory behavior using docs/TRAJECTORY_CLASSES.md
```

---

## Important Boundary

The current results are preliminary.

They support this claim:

```text
Different domains can be represented and compared
through shared structural stability trajectories.
```

They do not yet prove:

```text
a universal structural law
```

Further validation requires:

- larger datasets
- more domains
- repeated perturbation families
- normalized IRI scaling
- statistical trajectory comparison
- independent replication

---

## Relationship to OMNIA

OMNIA is the structural measurement engine.

OMNIA-INVARIANCE focuses on one specific use:

```text
measuring structural behavior under transformation
```

In simple terms:

```text
OMNIA measures.
OMNIA-INVARIANCE compares trajectories.
```

---

## Current Research Direction

The next logical direction is trajectory classification automation.

Future work may include:

- automatic trajectory class detection
- trajectory distance metrics
- domain clustering
- collapse threshold comparison
- normalized IRI scaling
- larger cross-domain benchmark sets

The long-term goal is not to create another domain-specific metric.

The goal is to build a structural comparison layer that can operate across domains.

---

## Summary

OMNIA-INVARIANCE is an executable framework for cross-domain structural trajectory comparison.

Its current strongest conclusion is methodological:

```text
shared structural trajectory comparison is possible
```

The current data show:

```text
mean Ω values are relatively close across domains,
while IRI behavior separates domains more strongly.
```

This makes OMNIA-INVARIANCE a framework for studying:

- structural persistence
- collapse dynamics
- recovery behavior
- irreversibility
- cross-domain stability profiles

under controlled transformation.

