# Transformation Contract

This document defines the public shape expected from OMNIA-INVARIANCE transformation results.

The goal is clarity.

A reviewer should understand what was transformed, what remained stable, and what collapsed.

---

## Invariance unit

An invariance result should contain:

| Component | Required | Meaning |
|---|---:|---|
| case_id | yes | Stable identifier for the invariance case |
| source_ref | yes | Source structure being transformed |
| transformation | yes | Declared controlled transformation |
| invariance_target | yes | Property or structure expected to persist |
| stable_residue | preferred | What remains invariant |
| collapse_signal | preferred | What fails to survive |
| invariance_result | yes | stable, unstable, collapsed, candidate, or inconclusive |
| limitation | yes | What the result does not prove |
| external_validation | yes | How the artifact should be validated later |

---

## Minimal JSON shape

A minimal invariance artifact can use this shape:

    {{
      "case_id": "invariance-example-001",
      "source_ref": "path-or-description",
      "transformation": "declared controlled transformation",
      "invariance_target": "declared property or structure",
      "stable_residue": "declared residue or null",
      "collapse_signal": "declared collapse signal or null",
      "invariance_result": "stable | unstable | collapsed | candidate | inconclusive",
      "boundary": "measurement != inference != decision",
      "limitation": "What this invariance check does not prove",
      "external_validation": "Validate through OMNIA-VALIDATION or declared artifact checks"
    }}

---

## Result vocabulary

Use a small vocabulary:

    stable
    unstable
    collapsed
    candidate
    inconclusive

Meaning:

- stable: the declared structure persists under transformation;
- unstable: the declared structure changes significantly;
- collapsed: the declared structure fails to survive;
- candidate: possible invariant residue requires further testing;
- inconclusive: evidence is insufficient.

---

## No silent promotion

An invariance result must not silently become final truth.

A stable residue is not semantic certainty.

A collapse signal is not automatic falsehood.

A candidate invariant is not a decision.

