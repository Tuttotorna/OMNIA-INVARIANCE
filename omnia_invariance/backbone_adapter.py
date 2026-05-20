from __future__ import annotations

from typing import Any

from omnia import build_boundary_certificate
from omnia_limit import validate_certificate
from omnia_validation.enveloper import process_boundary_step


def _coerce_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _coerce_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _derive_ast_deformation_index(measurement: dict[str, Any]) -> float:
    """Normalize invariance-facing metrics into the backbone deformation field."""

    if "ast_deformation_index" in measurement:
        return _coerce_float(measurement["ast_deformation_index"])

    if "deformation_index" in measurement:
        return _coerce_float(measurement["deformation_index"])

    if "invariance_break" in measurement:
        return _coerce_float(measurement["invariance_break"])

    if "variance" in measurement:
        return _coerce_float(measurement["variance"])

    if "residual_variance" in measurement:
        return _coerce_float(measurement["residual_variance"])

    if "invariance_score" in measurement:
        score = _coerce_float(measurement["invariance_score"], default=1.0)
        return max(0.0, min(1.0, 1.0 - score))

    if "stability_score" in measurement:
        score = _coerce_float(measurement["stability_score"], default=1.0)
        return max(0.0, min(1.0, 1.0 - score))

    return _coerce_float(
        measurement.get("drift_score", measurement.get("delta_omega", measurement.get("delta", 0.0)))
    )


def _derive_boundary_state(measurement: dict[str, Any]) -> tuple[bool, bool, str]:
    """Derive explicit backbone boundary fields without owning validation policy."""

    should_continue = measurement.get("should_continue")
    saturation_detected = measurement.get("saturation_detected")

    gate = str(
        measurement.get(
            "gate",
            measurement.get("gate_status", measurement.get("status", "")),
        )
    ).upper()

    if should_continue is None:
        if gate in {"STOP", "NO_GO", "CLOSED", "GATE_CLOSED", "SATURATED"}:
            should_continue = False
        elif gate in {"GO", "CONTINUE", "OPEN", "GATE_OPEN"}:
            should_continue = True

    if saturation_detected is None:
        if gate in {"STOP", "NO_GO", "CLOSED", "GATE_CLOSED", "SATURATED"}:
            saturation_detected = True
        elif gate in {"GO", "CONTINUE", "OPEN", "GATE_OPEN"}:
            saturation_detected = False

    if should_continue is None and saturation_detected is None:
        invariance_score = measurement.get("invariance_score")
        if invariance_score is not None:
            score = _coerce_float(invariance_score, default=1.0)
            saturation_detected = score >= 0.95
            should_continue = not saturation_detected
        else:
            saturation_detected = False
            should_continue = True

    if should_continue is None:
        should_continue = not bool(saturation_detected)

    if saturation_detected is None:
        saturation_detected = not bool(should_continue)

    reason = measurement.get("reason")
    if reason is None:
        reason = (
            "Invariance saturation reached"
            if bool(saturation_detected)
            else "Invariance measurement still yields structural information"
        )

    return bool(should_continue), bool(saturation_detected), str(reason)


def _extract_extra_metrics(measurement: dict[str, Any]) -> dict[str, Any]:
    known_keys = {
        "ast_deformation_index",
        "deformation_index",
        "invariance_break",
        "variance",
        "residual_variance",
        "invariance_score",
        "stability_score",
        "drift_score",
        "delta_omega",
        "delta",
        "perturbation_step",
        "should_continue",
        "saturation_detected",
        "gate",
        "gate_status",
        "status",
        "reason",
    }

    return {
        key: value
        for key, value in measurement.items()
        if key not in known_keys and isinstance(value, (int, float, str, bool, type(None)))
    }


def adapt_invariance_measurement_to_boundary_certificate(
    measurement: dict[str, Any],
    *,
    target_repository: str = "OMNIA-INVARIANCE",
    certificate_id: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Adapt invariance measurements into the canonical BoundaryCertificate shape.

    OMNIA-INVARIANCE is a Producer/Adapter.

    It may normalize invariance-specific metrics into the backbone artifact.

    It does not define the BoundaryCertificate contract.
    It does not define the ValidationEnvelope contract.
    It does not validate the schema directly.
    It does not decide semantic truth.
    """

    ast_deformation_index = _derive_ast_deformation_index(measurement)
    perturbation_step = _coerce_int(measurement.get("perturbation_step", 0))
    should_continue, saturation_detected, reason = _derive_boundary_state(measurement)
    extra_metrics = _extract_extra_metrics(measurement)

    if "invariance_score" in measurement:
        extra_metrics["invariance_score"] = _coerce_float(measurement["invariance_score"])

    if "stability_score" in measurement:
        extra_metrics["stability_score"] = _coerce_float(measurement["stability_score"])

    return build_boundary_certificate(
        target_repository=target_repository,
        ast_deformation_index=ast_deformation_index,
        perturbation_step=perturbation_step,
        should_continue=should_continue,
        saturation_detected=saturation_detected,
        reason=reason,
        certificate_id=certificate_id,
        timestamp=timestamp,
        extra_metrics=extra_metrics,
    )


def run_invariance_backbone_flow(
    measurement: dict[str, Any],
    *,
    target_repository: str = "OMNIA-INVARIANCE",
    certificate_id: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Run an invariance measurement through the canonical OMNIA backbone.

    Flow:

    invariance measurement
      -> OMNIA-INVARIANCE adapter
      -> BoundaryCertificate-compatible artifact
      -> omnia-limit validate_certificate()
      -> OMNIA-VALIDATION process_boundary_step()
      -> ValidationEnvelope

    OMNIA-INVARIANCE only adapts/produces.
    """

    raw_certificate = adapt_invariance_measurement_to_boundary_certificate(
        measurement,
        target_repository=target_repository,
        certificate_id=certificate_id,
        timestamp=timestamp,
    )

    validate_certificate(raw_certificate)

    return process_boundary_step(raw_certificate)
