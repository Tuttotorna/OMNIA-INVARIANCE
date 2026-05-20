# OMNIA-INVARIANCE Backbone Compliance

## Role

OMNIA-INVARIANCE is a Producer/Adapter.

It may produce invariance-facing structural measurements.

It may adapt invariance-specific metrics into a BoundaryCertificate-compatible artifact.

It is not the boundary validator.

It is not the validation control plane.

It is not a decision engine.

## Canonical flow

OMNIA-INVARIANCE adapts into the existing backbone:

invariance measurement
  -> OMNIA-INVARIANCE adapter
  -> BoundaryCertificate-compatible artifact
  -> omnia-limit validate_certificate()
  -> OMNIA-VALIDATION process_boundary_step()
  -> ValidationEnvelope

## Public API

OMNIA-INVARIANCE exposes:

adapt_invariance_measurement_to_boundary_certificate(...)
run_invariance_backbone_flow(...)

## Contract rule

OMNIA-INVARIANCE does not redefine BoundaryCertificate.

OMNIA-INVARIANCE does not redefine ValidationEnvelope.

OMNIA-INVARIANCE does not bypass omnia-limit.

OMNIA-INVARIANCE does not bypass OMNIA-VALIDATION.

OMNIA-INVARIANCE adapts its own domain-specific measurements into the canonical backbone.

## Metric normalization

Current adapter mapping:

invariance_score
  -> ast_deformation_index = 1.0 - invariance_score

stability_score
  -> ast_deformation_index = 1.0 - stability_score

residual_variance
  -> ast_deformation_index = residual_variance

variance
  -> ast_deformation_index = variance

invariance_break
  -> ast_deformation_index = invariance_break

explicit ast_deformation_index
  -> preserved directly

## Boundary

measurement != validation
validation != orchestration
orchestration != decision
adapter != validator
adapter != control plane

OMNIA-INVARIANCE stays in the Producer/Adapter layer.
