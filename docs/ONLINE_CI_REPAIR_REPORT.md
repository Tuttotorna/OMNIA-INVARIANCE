# Online CI Repair Report

Repository: OMNIA-INVARIANCE

Timestamp UTC: 2026-05-21T18:51:09Z

Purpose:
Repair red GitHub Actions for current HEAD.

No release was created.
No tag was created.
Only CI workflow files were changed.

Boundary:
measurement != inference != decision

Before:
{
  "green": false,
  "status": "failed",
  "reason": "At least one Actions run for current HEAD failed.",
  "runs": [
    {
      "id": 26240288755,
      "name": "CI",
      "status": "completed",
      "conclusion": "failure",
      "html_url": "https://github.com/Tuttotorna/OMNIA-INVARIANCE/actions/runs/26240288755",
      "created_at": "2026-05-21T16:52:01Z",
      "updated_at": "2026-05-21T16:52:43Z",
      "head_sha": "6c6262584245ac827fa25a0ed1f17ab96999556e"
    }
  ]
}

Patch:
{
  "ci_changed": true,
  "legacy_non_dot_github_removed": [],
  "duplicate_test_workflows_removed": []
}

Local tests:
{
  "status": "pass",
  "passed": 8,
  "failed": 0,
  "errors": 0,
  "returncode": 0,
  "summary": "8 passed in 1.55s"
}

Push:
null

After online check:
null
