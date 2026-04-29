# Canonical Trajectory Format

## Purpose

This document defines the canonical trajectory structure used inside OMNIA-INVARIANCE.

The goal is to make cross-domain structural profiles directly comparable.

---

# Canonical Structure

Each domain trajectory should contain:

```json
{
  "domain": "...",

  "omega_trajectory": [],

  "iri_trajectory": [],

  "collapse_point": 0,

  "summary": {
    "mean_omega": 0.0,
    "mean_iri": 0.0
  }
}
```

---

# Required Fields

| Field | Meaning |
|---|---|
| domain | domain name |
| omega_trajectory | coherence evolution |
| iri_trajectory | irreversibility evolution |
| collapse_point | perturbation step where collapse becomes dominant |
| mean_omega | average coherence |
| mean_iri | average irreversibility |

---

# Ω Trajectory

The Ω trajectory measures structural coherence under progressive perturbation.

Example:

```text
0.91 -> 0.82 -> 0.67 -> 0.41 -> 0.18
```

High Ω indicates stronger structural persistence.

Low Ω indicates degradation or collapse.

---

# IRI Trajectory

The IRI trajectory measures irreversible structural loss.

Example:

```text
0.02 -> 0.11 -> 0.39 -> 0.72 -> 0.94
```

High IRI indicates increasing non-recoverable degradation.

---

# Collapse Point

The collapse point identifies the perturbation region where structural degradation becomes dominant.

This does not necessarily imply total destruction.

It marks the transition into unstable structural behavior.

---

# Cross-Domain Comparison

All domains inside OMNIA-INVARIANCE should follow this format.

This allows direct comparison between:

- physics
- logic
- crypto
- symbolic systems
- dynamical systems
- future domains

The comparison operates on trajectories, not semantics.

---

# Important Boundary

Trajectory similarity does not imply semantic equivalence.

OMNIA-INVARIANCE compares structural behavior under perturbation.

Not ontology.

Not meaning.

Not domain identity.

---

# Summary

The canonical trajectory format exists to standardize structural stability profiles across domains.

Its purpose is to make cross-domain invariance comparison reproducible and measurable.