# OMNIA-INVARIANCE

<!-- TOTALITY_FIELD_ALIGNMENT_START -->
## Totality Field Alignment

This repository is not an independent fragment.

It is a local operational appearance of the same total field formalized in [LAW OF TOTALITY](https://github.com/Tuttotorna/LAW-OF-TOTALITY).

Public threshold release: [v0.1.2](https://github.com/Tuttotorna/LAW-OF-TOTALITY/releases/tag/v0.1.2)

DOI: [10.5281/zenodo.20700914](https://doi.org/10.5281/zenodo.20700914)

See: [TOTALITY-FIELD.md](TOTALITY-FIELD.md)
<!-- TOTALITY_FIELD_ALIGNMENT_END -->

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20368998.svg)](https://doi.org/10.5281/zenodo.20368998)

<!-- OMNIA_INVARIANCE_AUDITOR_TOP_START -->

# OMNIA-INVARIANCE



## Foundational Principle

OMNIA-INVARIANCE is an invariance-focused application of the L.O.N. Multi-Form Invariance Principle:

> No single form is sovereign.

In OMNIA-INVARIANCE, this becomes:

> No invariant claim is sovereign unless it survives independent transformations.

An invariant is not trusted because it appears stable once, under one representation, or inside one metric. It must preserve structural compatibility across independent transformations of form, scale, representation, context, and observation.

OMNIA-INVARIANCE exists to distinguish surface stability from structural invariance.

See:

- https://github.com/Tuttotorna/lon-mirror/tree/main/foundation

## Concrete entrypoint: OMNIA Invariance Auditor

This repository now has a direct operational tool:

    python -m omnia_invariance_auditor.cli --input examples/sample_invariance_cases.jsonl --out-dir report

It solves a concrete problem:

    given cases, transformations, and measured outputs,
    determine what remains invariant,
    what becomes fragile,
    and what breaks under transformation.

In short:

    cases + transformations -> invariant / fragile / broken report

## What problem does it solve?

A claim can appear stable in one representation and fail under equivalent or controlled transformations.

OMNIA-INVARIANCE turns this into a reproducible measurement problem.

It answers:

    Which cases remain structurally invariant?
    Which cases drift but remain recoverable?
    Which cases break under transformation?
    Which transformations cause the highest instability?
    What is the invariance rate of the dataset?
    Can CI fail when broken invariance appears?

The rest of this repository explains the invariance concept.

The auditor is the practical entrypoint.

## Install

Clone the repository:

    git clone https://github.com/Tuttotorna/OMNIA-INVARIANCE.git
    cd OMNIA-INVARIANCE

Install locally:

    pip install -e .

The auditor only uses the Python standard library.

## Run

Run the sample audit:

    python -m omnia_invariance_auditor.cli --input examples/sample_invariance_cases.jsonl --out-dir report

Run and fail if broken invariance is detected:

    python -m omnia_invariance_auditor.cli --input examples/sample_invariance_cases.jsonl --out-dir report --fail-on-broken

Run and fail if fragile or broken cases are detected:

    python -m omnia_invariance_auditor.cli --input examples/sample_invariance_cases.jsonl --out-dir report --fail-on-fragile

## Input format

The auditor accepts JSONL.

Required fields:

    case_id
    transform_id
    output

Optional fields:

    expected
    source
    note

Example:

    {"case_id":"c1","transform_id":"base","output":"A"}
    {"case_id":"c1","transform_id":"rewrite","output":"A"}
    {"case_id":"c1","transform_id":"order_swap","output":"B"}

Classification rule:

    invariant = all transformed outputs are structurally equivalent
    fragile   = outputs differ but remain partially compatible
    broken    = outputs differ beyond the configured compatibility threshold

## Output

The auditor writes:

    report.json
    report.csv
    report.html
    fragile_cases.jsonl
    broken_cases.jsonl
    certificate.json

Meaning:

    report.json
    Full structured invariance analysis.

    report.csv
    Spreadsheet-friendly case summary.

    report.html
    Human-readable audit report.

    fragile_cases.jsonl
    One JSON object per fragile case.

    broken_cases.jsonl
    One JSON object per broken case.

    certificate.json
    Reproducibility certificate with thresholds, counts, and boundary statement.

## CI gate

Fail when broken invariance appears:

    python -m omnia_invariance_auditor.cli --input examples/sample_invariance_cases.jsonl --out-dir report --fail-on-broken

Fail when fragile or broken invariance appears:

    python -m omnia_invariance_auditor.cli --input examples/sample_invariance_cases.jsonl --out-dir report --fail-on-fragile

Exit codes:

    0 = analysis completed without selected blocking condition
    2 = fragile invariance detected under --fail-on-fragile
    3 = broken invariance detected under --fail-on-broken or --fail-on-fragile
    4 = invalid input or measurement error

## What this is not

This is not a semantic truth engine.

It does not decide meaning.

It does not decide whether an answer is true.

It does not claim that transformations are semantically equivalent unless the dataset defines them as the test boundary.

It provides one concrete, reproducible operation:

    read transformed case outputs
    normalize structural form
    measure pairwise compatibility
    classify invariant / fragile / broken
    produce reports
    optionally fail CI

## Why the rest of the repository still matters

The rest of the repository documents the invariance concept:

    invariance under transformation
    observer-independent stability
    structural compatibility
    perturbation response
    fragile equivalence
    broken equivalence

The code above is the entrypoint.

The repository below is the derivation path.

<!-- OMNIA_INVARIANCE_AUDITOR_TOP_END -->

---

<!-- MB-X.01 LON RELEASE:START -->

## MB-X.01 / L.O.N. release state

Repository: Tuttotorna/OMNIA-INVARIANCE
Release tag: v2026.05.21
Release commit: 1e6f54c
Release DOI: 10.5281/zenodo.20322694

Boundary:

measurement != validation
validation != orchestration
orchestration != decision
decision != measurement

<!-- MB-X.01 LON RELEASE:END -->

# OMNIA-INVARIANCE

<!-- ZENODO DOI:START -->

## DOI

Zenodo DOI badge for this repository.

Repository: Tuttotorna/OMNIA-INVARIANCE
GitHub repository id: 1224811295
Release tag: v2026.05.21
Latest release DOI: 10.5281/zenodo.20322694

<!-- ZENODO DOI:END -->


## DOI

Release DOI: [10.5281/zenodo.20368998](https://doi.org/10.5281/zenodo.20368998)

GitHub release: [OMNIA-INVARIANCE v1.0.0 release](https://github.com/Tuttotorna/OMNIA-INVARIANCE/releases/tag/v1.0.0)

## Start here

From a clean environment:

    git clone [OMNIA-INVARIANCE.git](https://github.com/Tuttotorna/OMNIA-INVARIANCE.git)
    cd OMNIA-INVARIANCE
    python -m pip install -e .
    pytest

If example scripts are available, run the smallest demonstration after tests pass.

The goal is to see the invariance path:

    source structure
      -> controlled transformation
      -> invariance check
      -> stability / collapse
      -> external validation

---

## What OMNIA-INVARIANCE does

OMNIA-INVARIANCE checks what remains stable after controlled transformation.

It can help distinguish:

- stable structural residue;
- transformation-sensitive structure;
- collapse under perturbation;
- representation-bound artifacts;
- invariance candidates worth validating.

Public compression:

    RADAR detects.
    OMNIA measures.
    INVARIANCE checks what survives transformation.
    VALIDATION tests artifacts.

---

## What OMNIA-INVARIANCE does not do

OMNIA-INVARIANCE does not:

- infer semantic truth;
- decide correctness;
- replace OMNIA measurement;
- replace OMNIA-VALIDATION;
- prove final truth;
- prove physical truth;
- perform security scanning;
- perform cryptographic attacks;
- convert invariance into final decision.

The final decision remains external.

---

## Public mental model

    Surface similarity is cheap.
    Structural invariance is harder.
    OMNIA-INVARIANCE checks what survives controlled transformation.

Invariance is evidence of structural persistence.

It is not final truth.

---

## Invariance contract

Every serious OMNIA-INVARIANCE result should make clear:

| Component | Meaning |
|---|---|
| source structure | The object, output, trace, representation, or trajectory being transformed |
| transformation | The controlled change applied |
| invariance check | What structural property is checked after transformation |
| stable residue | What remains invariant |
| collapse signal | What fails to survive |
| result | stable, unstable, collapsed, candidate, or inconclusive |
| limitation | What the invariance result does not prove |
| external validation | How the result should be tested later |

---

## Result vocabulary

Recommended result vocabulary:

    stable
    unstable
    collapsed
    candidate
    inconclusive

Meaning:

- stable: measured structure persists under the declared transformation;
- unstable: measured structure changes significantly;
- collapsed: measured structure fails to survive the transformation;
- candidate: a possible invariant residue should be tested further;
- inconclusive: the check is insufficient or ambiguous.

---

## Recommended reading order

1. [docs/QUICKSTART_INVARIANCE.md](docs/QUICKSTART_INVARIANCE.md)
2. [docs/INVARIANCE_OVERVIEW.md](docs/INVARIANCE_OVERVIEW.md)
3. [docs/TRANSFORMATION_CONTRACT.md](docs/TRANSFORMATION_CONTRACT.md)
4. [docs/STABILITY_AND_COLLAPSE.md](docs/STABILITY_AND_COLLAPSE.md)
5. [docs/INVARIANCE_BOUNDARY.md](docs/INVARIANCE_BOUNDARY.md)
6. [docs/INVARIANCE_MANIFEST.json](docs/INVARIANCE_MANIFEST.json)

---

## Ecosystem entry point

For the full ecosystem map, start here:

[lon-mirror](https://github.com/Tuttotorna/lon-mirror)

For public validation artifacts, start here:

[OMNIA-VALIDATION](https://github.com/Tuttotorna/OMNIA-VALIDATION)

For core structural measurement, start here:

[OMNIA](https://github.com/Tuttotorna/OMNIA)

---


## Smoke-test required terms

    Decision remains external

## Related repositories

| Repository | Role |
|---|---|
| [lon-mirror](https://github.com/Tuttotorna/lon-mirror) | Canonical public entry point |
| [OMNIA-VALIDATION](https://github.com/Tuttotorna/OMNIA-VALIDATION) | Public validation showroom |
| [OMNIA](https://github.com/Tuttotorna/OMNIA) | Core structural measurement engine |
| [OMNIABASE](https://github.com/Tuttotorna/OMNIABASE) | Representation invariance foundation |
| [omnia-limit](https://github.com/Tuttotorna/omnia-limit) | Stop / continue boundary layer |
| [OMNIA-RADAR](https://github.com/Tuttotorna/OMNIA-RADAR) | Structural signal detection layer |
| [OMNIA-INVARIANCE](https://github.com/Tuttotorna/OMNIA-INVARIANCE) | Structural invariance layer |
| [OMNIA-CONSTANT](https://github.com/Tuttotorna/OMNIA-CONSTANT) | Structural constant candidate layer |
| [OMNIAMIND](https://github.com/Tuttotorna/OMNIAMIND) | Structural cognition orchestration layer |
| [OMNIA-THREE-BODY](https://github.com/Tuttotorna/OMNIA-THREE-BODY) | Dynamic divergence stress test |
| [OMNIA-SECURITY](https://github.com/Tuttotorna/OMNIA-SECURITY) | Bounded structural security diagnostics |
| [OMNIA-CRYPTO](https://github.com/Tuttotorna/OMNIA-CRYPTO) | Bounded structural crypto diagnostics |

---

## Boundary and smoke-test required terms

    Structural truth = invariance under transformation
    measurement != inference != decision
    not a truth oracle
    not a semantic judge

---

## License

MIT.

<!-- OMNIA_ECOSYSTEM_BOUNDARY_V1 -->

## Ecosystem Boundary

```text
measurement != inference != decision
```

This repository is part of the MB-X.01 / OMNIA ecosystem. Its outputs must be read as structural measurement, validation, detection, orchestration or adapter artifacts according to the repository role. They are not autonomous semantic truth claims and they do not make external decisions.

<!-- STRUCTURAL_OBSERVABILITY_ROLE_START -->
## Structural Observability role

This repository is one bounded measurement role inside **Structural Observability**.

Role:

~~~text
transformation-stability auditor
~~~

Boundary:

~~~text
Invariance is measured under declared transformations. It is not a universal truth claim.
~~~

Structural Observability foundation:

- lon-mirror: https://github.com/Tuttotorna/lon-mirror
- Foundation release: https://github.com/Tuttotorna/lon-mirror/releases/tag/v0.2.2
- DOI: https://doi.org/10.5281/zenodo.20379374

Role document:

- [Structural Observability Role](docs/STRUCTURAL_OBSERVABILITY_ROLE.md)
<!-- STRUCTURAL_OBSERVABILITY_ROLE_END -->

<!-- OMNIA_ZENODO_CITATION_BLOCK_START -->

## Citation and archival

This repository is prepared for GitHub-Zenodo archival.

Repository:
https://github.com/Tuttotorna/OMNIA-INVARIANCE

Latest GitHub release: v0.1.2 (https://github.com/Tuttotorna/OMNIA-INVARIANCE/releases/tag/v0.1.2)

Detected Zenodo DOI(s):
- https://doi.org/10.5281/zenodo.20368998
- https://doi.org/10.5281/zenodo.20322694
- https://doi.org/10.5281/zenodo.20379374

Metadata files used for archival/citation:

- .zenodo.json
- CITATION.cff

Zenodo note:

GitHub-Zenodo archiving works after the repository is enabled in Zenodo GitHub settings and a GitHub release is created.

<!-- OMNIA_ZENODO_CITATION_BLOCK_END -->
