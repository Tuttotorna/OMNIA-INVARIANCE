# OMNIA-INVARIANCE Results Index

## Purpose

This file gives a public entrypoint into the result artifacts produced by OMNIA-INVARIANCE.

## Main result families

### Cross-domain comparison

Relevant files:

- `results/cross_domain_comparison.json`
- `results/cross_domain_summary.json`
- `results/cross_domain_omega.png`
- `results/cross_domain_iri.png`
- `results/cross_domain_comparison.png`

Purpose:

- compare structural trajectories across heterogeneous domains
- observe similarity and divergence under perturbation

### Domain profiles

Relevant files:

- `results/crypto_invariance_profile.json`
- `results/finance_invariance_profile.json`
- `results/llm_invariance_profile.json`
- `results/logic_invariance_profile.json`
- `results/physics_invariance_profile.json`

Purpose:

- record domain-level structural behavior
- compare invariance profiles

### Trajectory-space analysis

Relevant files:

- `results/integrated_trajectory_space.json`
- `results/normalized_trajectory_space.json`
- `results/trajectory_feature_table.json`
- `results/trajectory_embedding.png`
- `results/trajectory_space_map.png`

Purpose:

- map trajectory regions
- compare raw and normalized structure
- inspect topology and embedding behavior

### Run traces

Relevant files:

- `results/latest_colab_run.txt`
- `results/trajectory_classification_run.txt`
- `results/trajectory_clustering_run.txt`
- `results/trajectory_distance_matrix_run.txt`
- `results/trajectory_feature_export_run.txt`
- `results/trajectory_morphometrics_run.txt`

Purpose:

- preserve execution traces
- provide minimal reproducibility evidence

## Reading rule

```text
result artifact = structural evidence for a specific experiment
result artifact != universal proof
result artifact != semantic truth
```
