# Backbone CI Repair Report

Repository: OMNIA-INVARIANCE

Timestamp UTC: 2026-05-21T19:05:35Z

Purpose:
Repair remaining red GitHub Actions caused by missing online backbone package installation.

No release was created.
No tag was created.
Only CI workflow files and this repair report were changed.

Boundary:
measurement != inference != decision

Before:
{
  "green": false,
  "status": "failed",
  "reason": "At least one Actions run for current HEAD failed.",
  "runs": [
    {
      "id": 26246976923,
      "name": "CI",
      "status": "completed",
      "conclusion": "failure",
      "html_url": "https://github.com/Tuttotorna/OMNIA-INVARIANCE/actions/runs/26246976923",
      "created_at": "2026-05-21T19:01:33Z",
      "updated_at": "2026-05-21T19:01:57Z",
      "head_sha": "6459abfd0908e12e96bd6a06442e6da2d46bc449"
    }
  ]
}

Patch:
{
  "ci_changed": true,
  "legacy_non_dot_github_removed": [],
  "duplicate_test_workflows_removed": [],
  "python_version_policy": "3.12 only",
  "backbone_installs": {
    "OMNIA": true,
    "omnia-limit": true,
    "OMNIA-INVARIANCE": true
  },
  "required_omnia_doi_command_present": null
}

Local tests:
{
  "status": "pass",
  "passed": 8,
  "failed": 0,
  "errors": 0,
  "returncode": 0,
  "summary": "8 passed in 1.36s"
}

Push:
null

After online check:
null

After failed logs:
null
