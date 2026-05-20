from omnia_invariance import (
    adapt_invariance_measurement_to_boundary_certificate,
    run_invariance_backbone_flow,
)
from omnia_limit import validate_certificate


def test_adapt_invariance_measurement_to_boundary_certificate_continue_flow():
    measurement = {
        "invariance_score": 0.88,
        "perturbation_step": 2,
        "gate_status": "CONTINUE",
        "transformation_family": "base_shift",
        "invariant_property": "digit_sum_mod",
    }

    raw_certificate = adapt_invariance_measurement_to_boundary_certificate(
        measurement,
        target_repository="OMNIA-INVARIANCE",
        certificate_id="invariance-continue-cert",
        timestamp="2026-05-20T20:00:00Z",
    )

    cert = validate_certificate(raw_certificate)

    assert cert.certificate_id == "invariance-continue-cert"
    assert cert.target_repository == "OMNIA-INVARIANCE"
    assert round(cert.ast_deformation_index, 2) == 0.12
    assert cert.perturbation_step == 2
    assert cert.should_continue is True
    assert cert.saturation_detected is False
    assert raw_certificate["metrics"]["invariance_score"] == 0.88
    assert raw_certificate["metrics"]["transformation_family"] == "base_shift"
    assert raw_certificate["metrics"]["invariant_property"] == "digit_sum_mod"


def test_run_invariance_backbone_flow_stop_flow():
    measurement = {
        "invariance_score": 0.97,
        "perturbation_step": 5,
        "gate_status": "STOP",
        "transformation_family": "observer_shift",
        "invariant_property": "structural_residual",
    }

    envelope = run_invariance_backbone_flow(
        measurement,
        target_repository="OMNIA-INVARIANCE",
        certificate_id="invariance-stop-cert",
        timestamp="2026-05-20T20:00:00Z",
    )

    assert envelope["validation_status"] == "GATE_CLOSED_SATURATION_REACHED"
    assert envelope["details"]["certificate_id"] == "invariance-stop-cert"
    assert envelope["details"]["target_repository"] == "OMNIA-INVARIANCE"
    assert envelope["details"]["saturation_detected"] is True
    assert round(envelope["details"]["ast_deformation_index"], 2) == 0.03
    assert envelope["details"]["perturbation_step"] == 5


def test_run_invariance_backbone_flow_explicit_deformation():
    measurement = {
        "ast_deformation_index": 0.42,
        "perturbation_step": 3,
        "should_continue": False,
        "saturation_detected": True,
        "reason": "Explicit invariance boundary reached",
        "invariance_score": 0.58,
    }

    envelope = run_invariance_backbone_flow(
        measurement,
        target_repository="OMNIA-INVARIANCE",
        certificate_id="invariance-explicit-cert",
        timestamp="2026-05-20T20:00:00Z",
    )

    assert envelope["validation_status"] == "GATE_CLOSED_SATURATION_REACHED"
    assert envelope["details"]["certificate_id"] == "invariance-explicit-cert"
    assert envelope["details"]["target_repository"] == "OMNIA-INVARIANCE"
    assert envelope["details"]["saturation_detected"] is True
    assert envelope["details"]["ast_deformation_index"] == 0.42
    assert envelope["details"]["perturbation_step"] == 3
