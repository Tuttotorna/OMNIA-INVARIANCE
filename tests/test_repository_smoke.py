
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_public_entrypoints_exist():
    required = [
        "README.md",
        "LICENSE",
        "CITATION.cff",
        "requirements.txt",
        "docs/INVARIANCE_SCOPE.md",
        "docs/RESULTS_INDEX.md",
        "docs/REPOSITORY_STATUS.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel

def test_core_directories_exist():
    for rel in ["docs", "examples", "results"]:
        assert (ROOT / rel).exists(), rel

def test_key_examples_exist():
    required = [
        "examples/compare_domains.py",
        "examples/classify_trajectories.py",
        "examples/invariance_logic_demo.py",
        "examples/invariance_physics_demo.py",
        "examples/invariance_llm_static_demo.py",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel

def test_key_results_exist():
    required = [
        "results/cross_domain_comparison.json",
        "results/cross_domain_summary.json",
        "results/crypto_invariance_profile.json",
        "results/llm_invariance_profile.json",
        "results/logic_invariance_profile.json",
        "results/physics_invariance_profile.json",
        "results/normalized_trajectory_space.json",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel

def test_readme_boundary_terms():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Structural truth = invariance under transformation" in text
    assert "measurement != inference != decision" in text
    assert "not a truth oracle" in text
    assert "Decision remains external" in text
