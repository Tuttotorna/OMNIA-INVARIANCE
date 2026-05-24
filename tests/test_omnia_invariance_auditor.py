import json
import subprocess
import sys

from omnia_invariance_auditor.core import (
    Observation,
    analyze_observations,
    char_similarity,
    jaccard_similarity,
    normalize_output,
    read_jsonl,
    structural_similarity,
)


def test_normalize_output():
    assert normalize_output("  Approved!! ") == "approved"
    assert normalize_output("A   B") == "a b"


def test_similarity_identical():
    assert structural_similarity("approved", "approved") == 1.0


def test_similarity_partial():
    score = structural_similarity("refund approved within 5 business days", "refund approved in five business days")
    assert 0.6 < score < 1.0


def test_similarity_opposite_lower():
    score = structural_similarity("access denied", "account unlocked")
    assert score < 0.6


def test_analyze_observations_counts():
    observations = [
        Observation("a", "base", "approved", "", "", ""),
        Observation("a", "rewrite", "approved", "", "", ""),
        Observation("b", "base", "refund approved within 5 business days", "", "", ""),
        Observation("b", "rewrite", "refund approved in five business days", "", "", ""),
        Observation("b", "swap", "refund approved within 5 days", "", "", ""),
        Observation("c", "base", "access denied", "", "", ""),
        Observation("c", "rewrite", "account unlocked", "", "", ""),
    ]

    result = analyze_observations(observations)
    assert result["summary"]["total_cases"] == 3
    assert result["summary"]["invariant_cases"] == 1
    assert result["summary"]["fragile_cases"] >= 1
    assert result["summary"]["broken_cases"] >= 1
    assert "certificate" in result


def test_read_jsonl(tmp_path):
    p = tmp_path / "cases.jsonl"
    p.write_text(
        '{"case_id":"x","transform_id":"base","output":"A"}\n'
        '{"case_id":"x","transform_id":"rewrite","output":"A"}\n',
        encoding="utf-8",
    )

    rows = read_jsonl(str(p))
    assert len(rows) == 2
    assert rows[0].case_id == "x"


def test_duplicate_transform_rejected(tmp_path):
    p = tmp_path / "cases.jsonl"
    p.write_text(
        '{"case_id":"x","transform_id":"base","output":"A"}\n'
        '{"case_id":"x","transform_id":"base","output":"B"}\n',
        encoding="utf-8",
    )

    try:
        read_jsonl(str(p))
        assert False, "expected duplicate error"
    except ValueError as e:
        assert "Duplicate" in str(e)


def test_cli_writes_reports(tmp_path):
    input_path = tmp_path / "cases.jsonl"
    out_dir = tmp_path / "report"

    input_path.write_text(
        '{"case_id":"a","transform_id":"base","output":"approved"}\n'
        '{"case_id":"a","transform_id":"rewrite","output":"approved"}\n'
        '{"case_id":"b","transform_id":"base","output":"access denied"}\n'
        '{"case_id":"b","transform_id":"rewrite","output":"account unlocked"}\n',
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "omnia_invariance_auditor.cli",
            "--input",
            str(input_path),
            "--out-dir",
            str(out_dir),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0
    assert (out_dir / "report.json").exists()
    assert (out_dir / "report.csv").exists()
    assert (out_dir / "report.html").exists()
    assert (out_dir / "fragile_cases.jsonl").exists()
    assert (out_dir / "broken_cases.jsonl").exists()
    assert (out_dir / "certificate.json").exists()


def test_cli_fail_on_broken(tmp_path):
    input_path = tmp_path / "cases.jsonl"
    out_dir = tmp_path / "report"

    input_path.write_text(
        '{"case_id":"b","transform_id":"base","output":"access denied"}\n'
        '{"case_id":"b","transform_id":"rewrite","output":"account unlocked"}\n',
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "omnia_invariance_auditor.cli",
            "--input",
            str(input_path),
            "--out-dir",
            str(out_dir),
            "--fail-on-broken",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 3


def test_cli_stable_only_passes_gate(tmp_path):
    input_path = tmp_path / "cases.jsonl"
    out_dir = tmp_path / "report"

    input_path.write_text(
        '{"case_id":"a","transform_id":"base","output":"pass"}\n'
        '{"case_id":"a","transform_id":"rewrite","output":"pass"}\n',
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "omnia_invariance_auditor.cli",
            "--input",
            str(input_path),
            "--out-dir",
            str(out_dir),
            "--fail-on-fragile",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0
