# Second-Pass Online CI Repair Report

Repository: OMNIA-INVARIANCE

Timestamp UTC: 2026-05-21T18:58:19Z

Purpose:
Repair remaining red GitHub Actions after first ecosystem CI repair.

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
      "id": 26246602513,
      "name": "CI",
      "status": "completed",
      "conclusion": "failure",
      "html_url": "https://github.com/Tuttotorna/OMNIA-INVARIANCE/actions/runs/26246602513",
      "created_at": "2026-05-21T18:54:16Z",
      "updated_at": "2026-05-21T18:54:43Z",
      "head_sha": "73b89bcaf8163b267861c45ec4118b8a1880dc31"
    }
  ]
}

Failed online log samples before repair:
{
  "ok": true,
  "failed_runs": [
    {
      "id": 26246602513,
      "name": "CI",
      "status": "completed",
      "conclusion": "failure",
      "html_url": "https://github.com/Tuttotorna/OMNIA-INVARIANCE/actions/runs/26246602513",
      "created_at": "2026-05-21T18:54:16Z",
      "updated_at": "2026-05-21T18:54:43Z",
      "head_sha": "73b89bcaf8163b267861c45ec4118b8a1880dc31"
    }
  ],
  "samples": [
    {
      "run_id": 26246602513,
      "download_ok": true,
      "html_url": "https://github.com/Tuttotorna/OMNIA-INVARIANCE/actions/runs/26246602513",
      "samples": [
        {
          "file": "0_test _ python-3.12.txt",
          "lines": [
            "2026-05-21T18:54:24.1196247Z \u001b[36;1mpython -m pip install pytest numpy matplotlib jsonschema\u001b[0m",
            "2026-05-21T18:54:25.6787468Z Collecting pytest",
            "2026-05-21T18:54:25.7988394Z   Downloading pytest-9.0.3-py3-none-any.whl.metadata (7.6 kB)",
            "2026-05-21T18:54:26.4234191Z Collecting iniconfig>=1.0.1 (from pytest)",
            "2026-05-21T18:54:26.4753670Z Collecting packaging>=22 (from pytest)",
            "2026-05-21T18:54:26.5260186Z Collecting pluggy<2,>=1.5 (from pytest)",
            "2026-05-21T18:54:26.5826293Z Collecting pygments>=2.7.2 (from pytest)",
            "2026-05-21T18:54:28.0821865Z Downloading pytest-9.0.3-py3-none-any.whl (375 kB)",
            "2026-05-21T18:54:28.9398381Z Installing collected packages: typing-extensions, six, rpds-py, pyparsing, pygments, pluggy, pillow, packaging, numpy, kiwisolver, iniconfig, fonttools, cycler, attrs, referencing, python-dateutil, pytest, contourpy, matplotlib, jsonschema-specifications, jsonschema",
            "2026-05-21T18:54:35.3556891Z Successfully installed attrs-26.1.0 contourpy-1.3.3 cycler-0.12.1 fonttools-4.63.0 iniconfig-2.3.0 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 kiwisolver-1.5.0 matplotlib-3.10.9 numpy-2.4.6 packaging-26.2 pillow-12.2.0 pluggy-1.6.0 pygments-2.20.0 pyparsing-3.3.2 pytest-9.0.3 python-dateutil-2.9.0.post0 referencing-0.37.0 rpds-py-0.30.0 six-1.17.0 typing-extensions-4.15.0",
            "2026-05-21T18:54:38.0302959Z \u001b[36;1m  python -m pytest -q\u001b[0m",
            "2026-05-21T18:54:38.5491871Z ==================================== ERRORS ====================================",
            "2026-05-21T18:54:38.5492495Z _______________ ERROR collecting tests/test_backbone_adapter.py ________________",
            "2026-05-21T18:54:38.5493394Z ImportError while importing test module '/home/runner/work/OMNIA-INVARIANCE/OMNIA-INVARIANCE/tests/test_backbone_adapter.py'.",
            "2026-05-21T18:54:38.5494670Z Traceback:",
            "2026-05-21T18:54:38.5499333Z E   ModuleNotFoundError: No module named 'omnia'",
            "2026-05-21T18:54:38.5500186Z ERROR tests/test_backbone_adapter.py",
            "2026-05-21T18:54:38.5500596Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!",
            "2026-05-21T18:54:38.5501327Z 1 error in 0.14s",
            "2026-05-21T18:54:38.5729669Z ##[error]Process completed with exit code 2."
          ]
        },
        {
          "file": "1_test _ python-3.11.txt",
          "lines": [
            "2026-05-21T18:54:23.5192585Z \u001b[36;1mpython -m pip install pytest numpy matplotlib jsonschema\u001b[0m",
            "2026-05-21T18:54:28.3985427Z Collecting pytest",
            "2026-05-21T18:54:28.4900467Z   Downloading pytest-9.0.3-py3-none-any.whl.metadata (7.6 kB)",
            "2026-05-21T18:54:28.9959416Z Collecting iniconfig>=1.0.1 (from pytest)",
            "2026-05-21T18:54:29.0351116Z Collecting packaging>=22 (from pytest)",
            "2026-05-21T18:54:29.0720112Z Collecting pluggy<2,>=1.5 (from pytest)",
            "2026-05-21T18:54:29.1148923Z Collecting pygments>=2.7.2 (from pytest)",
            "2026-05-21T18:54:30.3014083Z Downloading pytest-9.0.3-py3-none-any.whl (375 kB)",
            "2026-05-21T18:54:30.9775265Z Installing collected packages: typing-extensions, six, rpds-py, pyparsing, pygments, pluggy, pillow, packaging, numpy, kiwisolver, iniconfig, fonttools, cycler, attrs, referencing, python-dateutil, pytest, contourpy, matplotlib, jsonschema-specifications, jsonschema",
            "2026-05-21T18:54:36.7819278Z Successfully installed attrs-26.1.0 contourpy-1.3.3 cycler-0.12.1 fonttools-4.63.0 iniconfig-2.3.0 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 kiwisolver-1.5.0 matplotlib-3.10.9 numpy-2.4.6 packaging-26.2 pillow-12.2.0 pluggy-1.6.0 pygments-2.20.0 pyparsing-3.3.2 pytest-9.0.3 python-dateutil-2.9.0.post0 referencing-0.37.0 rpds-py-0.30.0 six-1.17.0 typing-extensions-4.15.0",
            "2026-05-21T18:54:40.2417162Z \u001b[36;1m  python -m pytest -q\u001b[0m",
            "2026-05-21T18:54:40.8396566Z ==================================== ERRORS ====================================",
            "2026-05-21T18:54:40.8397243Z _______________ ERROR collecting tests/test_backbone_adapter.py ________________",
            "2026-05-21T18:54:40.8397973Z ImportError while importing test module '/home/runner/work/OMNIA-INVARIANCE/OMNIA-INVARIANCE/tests/test_backbone_adapter.py'.",
            "2026-05-21T18:54:40.8399498Z Traceback:",
            "2026-05-21T18:54:40.8404617Z E   ModuleNotFoundError: No module named 'omnia'",
            "2026-05-21T18:54:40.8405276Z ERROR tests/test_backbone_adapter.py",
            "2026-05-21T18:54:40.8405616Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!",
            "2026-05-21T18:54:40.8405937Z 1 error in 0.13s",
            "2026-05-21T18:54:40.8619407Z ##[error]Process completed with exit code 2."
          ]
        },
        {
          "file": "test _ python-3.11/4_Install tooling.txt",
          "lines": [
            "2026-05-21T18:54:23.5192568Z \u001b[36;1mpython -m pip install pytest numpy matplotlib jsonschema\u001b[0m",
            "2026-05-21T18:54:28.3985359Z Collecting pytest",
            "2026-05-21T18:54:28.4900421Z   Downloading pytest-9.0.3-py3-none-any.whl.metadata (7.6 kB)",
            "2026-05-21T18:54:28.9959381Z Collecting iniconfig>=1.0.1 (from pytest)",
            "2026-05-21T18:54:29.0351045Z Collecting packaging>=22 (from pytest)",
            "2026-05-21T18:54:29.0720087Z Collecting pluggy<2,>=1.5 (from pytest)",
            "2026-05-21T18:54:29.1148897Z Collecting pygments>=2.7.2 (from pytest)",
            "2026-05-21T18:54:30.3014059Z Downloading pytest-9.0.3-py3-none-any.whl (375 kB)",
            "2026-05-21T18:54:30.9775219Z Installing collected packages: typing-extensions, six, rpds-py, pyparsing, pygments, pluggy, pillow, packaging, numpy, kiwisolver, iniconfig, fonttools, cycler, attrs, referencing, python-dateutil, pytest, contourpy, matplotlib, jsonschema-specifications, jsonschema",
            "2026-05-21T18:54:36.7818912Z Successfully installed attrs-26.1.0 contourpy-1.3.3 cycler-0.12.1 fonttools-4.63.0 iniconfig-2.3.0 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 kiwisolver-1.5.0 matplotlib-3.10.9 numpy-2.4.6 packaging-26.2 pillow-12.2.0 pluggy-1.6.0 pygments-2.20.0 pyparsing-3.3.2 pytest-9.0.3 python-dateutil-2.9.0.post0 referencing-0.37.0 rpds-py-0.30.0 six-1.17.0 typing-extensions-4.15.0"
          ]
        },
        {
          "file": "test _ python-3.11/6_Run tests when tests exist.txt",
          "lines": [
            "2026-05-21T18:54:40.2417160Z \u001b[36;1m  python -m pytest -q\u001b[0m",
            "2026-05-21T18:54:40.8396555Z ==================================== ERRORS ====================================",
            "2026-05-21T18:54:40.8397240Z _______________ ERROR collecting tests/test_backbone_adapter.py ________________",
            "2026-05-21T18:54:40.8397968Z ImportError while importing test module '/home/runner/work/OMNIA-INVARIANCE/OMNIA-INVARIANCE/tests/test_backbone_adapter.py'.",
            "2026-05-21T18:54:40.8399494Z Traceback:",
            "2026-05-21T18:54:40.8404614Z E   ModuleNotFoundError: No module named 'omnia'",
            "2026-05-21T18:54:40.8405274Z ERROR tests/test_backbone_adapter.py",
            "2026-05-21T18:54:40.8405614Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!",
            "2026-05-21T18:54:40.8405935Z 1 error in 0.13s",
            "2026-05-21T18:54:40.8619388Z ##[error]Process completed with exit code 2."
          ]
        },
        {
          "file": "test _ python-3.12/4_Install tooling.txt",
          "lines": [
            "2026-05-21T18:54:24.1196242Z \u001b[36;1mpython -m pip install pytest numpy matplotlib jsonschema\u001b[0m",
            "2026-05-21T18:54:25.6787407Z Collecting pytest",
            "2026-05-21T18:54:25.7988328Z   Downloading pytest-9.0.3-py3-none-any.whl.metadata (7.6 kB)",
            "2026-05-21T18:54:26.4234136Z Collecting iniconfig>=1.0.1 (from pytest)",
            "2026-05-21T18:54:26.4753423Z Collecting packaging>=22 (from pytest)",
            "2026-05-21T18:54:26.5260135Z Collecting pluggy<2,>=1.5 (from pytest)",
            "2026-05-21T18:54:26.5826259Z Collecting pygments>=2.7.2 (from pytest)",
            "2026-05-21T18:54:28.0821838Z Downloading pytest-9.0.3-py3-none-any.whl (375 kB)",
            "2026-05-21T18:54:28.9398342Z Installing collected packages: typing-extensions, six, rpds-py, pyparsing, pygments, pluggy, pillow, packaging, numpy, kiwisolver, iniconfig, fonttools, cycler, attrs, referencing, python-dateutil, pytest, contourpy, matplotlib, jsonschema-specifications, jsonschema",
            "2026-05-21T18:54:35.3556594Z Successfully installed attrs-26.1.0 contourpy-1.3.3 cycler-0.12.1 fonttools-4.63.0 iniconfig-2.3.0 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 kiwisolver-1.5.0 matplotlib-3.10.9 numpy-2.4.6 packaging-26.2 pillow-12.2.0 pluggy-1.6.0 pygments-2.20.0 pyparsing-3.3.2 pytest-9.0.3 python-dateutil-2.9.0.post0 referencing-0.37.0 rpds-py-0.30.0 six-1.17.0 typing-extensions-4.15.0"
          ]
        },
        {
          "file": "test _ python-3.12/6_Run tests when tests exist.txt",
          "lines": [
            "2026-05-21T18:54:38.0302957Z \u001b[36;1m  python -m pytest -q\u001b[0m",
            "2026-05-21T18:54:38.5491858Z ==================================== ERRORS ====================================",
            "2026-05-21T18:54:38.5492493Z _______________ ERROR collecting tests/test_backbone_adapter.py ________________",
            "2026-05-21T18:54:38.5493391Z ImportError while importing test module '/home/runner/work/OMNIA-INVARIANCE/OMNIA-INVARIANCE/tests/test_backbone_adapter.py'.",
            "2026-05-21T18:54:38.5494665Z Traceback:",
            "2026-05-21T18:54:38.5499331Z E   ModuleNotFoundError: No module named 'omnia'",
            "2026-05-21T18:54:38.5500184Z ERROR tests/test_backbone_adapter.py",
            "2026-05-21T18:54:38.5500594Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!",
            "2026-05-21T18:54:38.5501322Z 1 error in 0.14s",
            "2026-05-21T18:54:38.5729645Z ##[error]Process completed with exit code 2."
          ]
        }
      ]
    }
  ]
}

Patch:
{
  "ci_changed": true,
  "legacy_non_dot_github_removed": [],
  "duplicate_test_workflows_removed": [],
  "python_version_policy": "3.12 only",
  "omnia_required_doi_command_present": null
}

Local tests:
{
  "status": "pass",
  "passed": 8,
  "failed": 0,
  "errors": 0,
  "returncode": 0,
  "summary": "8 passed in 2.54s"
}

Push:
null

After online check:
null
