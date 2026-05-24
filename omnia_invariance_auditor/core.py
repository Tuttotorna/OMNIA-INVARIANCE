import csv
import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Observation:
    case_id: str
    transform_id: str
    output: str
    expected: str
    source: str
    note: str


@dataclass(frozen=True)
class CaseAnalysis:
    case_id: str
    transforms: int
    unique_outputs: int
    status: str
    invariance_score: float
    compatibility_score: float
    max_distance: float
    reference_output: str
    outputs: Dict[str, str]
    notes: List[str]


def normalize_output(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9\.\-\+\s]", "", text)
    return text.strip()


def tokenize(value: str) -> List[str]:
    normalized = normalize_output(value)
    if not normalized:
        return []
    return normalized.split()


def jaccard_similarity(a: str, b: str) -> float:
    ta = set(tokenize(a))
    tb = set(tokenize(b))

    if not ta and not tb:
        return 1.0

    if not ta or not tb:
        return 0.0

    return len(ta & tb) / len(ta | tb)


def char_similarity(a: str, b: str) -> float:
    na = normalize_output(a)
    nb = normalize_output(b)

    if na == nb:
        return 1.0

    if not na or not nb:
        return 0.0

    m = len(na)
    n = len(nb)

    previous = list(range(n + 1))

    for i in range(1, m + 1):
        current = [i] + [0] * n
        for j in range(1, n + 1):
            cost = 0 if na[i - 1] == nb[j - 1] else 1
            current[j] = min(
                previous[j] + 1,
                current[j - 1] + 1,
                previous[j - 1] + cost,
            )
        previous = current

    distance = previous[n]
    scale = max(m, n)

    return max(0.0, 1.0 - (distance / scale))


def structural_similarity(a: str, b: str) -> float:
    if normalize_output(a) == normalize_output(b):
        return 1.0

    return round((0.65 * char_similarity(a, b)) + (0.35 * jaccard_similarity(a, b)), 12)


def read_jsonl(path: str) -> List[Observation]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)

    observations = []

    with p.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            raw = line.strip()
            if not raw:
                continue

            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as e:
                raise ValueError("Invalid JSONL at line " + str(line_no) + ": " + str(e))

            for field in ["case_id", "transform_id", "output"]:
                if field not in obj:
                    raise ValueError("Missing required field '" + field + "' at line " + str(line_no))

            observations.append(
                Observation(
                    case_id=str(obj["case_id"]),
                    transform_id=str(obj["transform_id"]),
                    output=str(obj["output"]),
                    expected=str(obj.get("expected", "")),
                    source=str(obj.get("source", "")),
                    note=str(obj.get("note", "")),
                )
            )

    if not observations:
        raise ValueError("No observations found in " + path)

    seen = set()
    for obs in observations:
        key = (obs.case_id, obs.transform_id)
        if key in seen:
            raise ValueError("Duplicate case_id + transform_id: " + obs.case_id + " / " + obs.transform_id)
        seen.add(key)

    return observations


def group_observations(observations: List[Observation]) -> Dict[str, List[Observation]]:
    grouped = defaultdict(list)
    for obs in observations:
        grouped[obs.case_id].append(obs)
    return dict(grouped)


def analyze_case(
    case_id: str,
    observations: List[Observation],
    fragile_threshold: float = 0.85,
    broken_threshold: float = 0.60,
) -> CaseAnalysis:
    ordered = sorted(observations, key=lambda x: x.transform_id)
    outputs = {obs.transform_id: obs.output for obs in ordered}
    normalized_outputs = [normalize_output(obs.output) for obs in ordered]
    unique_outputs = len(set(normalized_outputs))

    reference_output = ordered[0].output

    if len(ordered) == 1:
        compatibility_score = 1.0
        max_distance = 0.0
    else:
        sims = []
        for i in range(len(ordered)):
            for j in range(i + 1, len(ordered)):
                sims.append(structural_similarity(ordered[i].output, ordered[j].output))

        compatibility_score = round(sum(sims) / len(sims), 12) if sims else 1.0
        max_distance = round(1.0 - min(sims), 12) if sims else 0.0

    if unique_outputs == 1:
        status = "invariant"
        invariance_score = 1.0
    elif compatibility_score >= fragile_threshold:
        status = "fragile"
        invariance_score = compatibility_score
    elif compatibility_score < broken_threshold:
        status = "broken"
        invariance_score = compatibility_score
    else:
        status = "fragile"
        invariance_score = compatibility_score

    notes = [obs.note for obs in ordered if obs.note]

    return CaseAnalysis(
        case_id=case_id,
        transforms=len(ordered),
        unique_outputs=unique_outputs,
        status=status,
        invariance_score=round(invariance_score, 12),
        compatibility_score=round(compatibility_score, 12),
        max_distance=max_distance,
        reference_output=reference_output,
        outputs=outputs,
        notes=notes,
    )


def analyze_observations(
    observations: List[Observation],
    fragile_threshold: float = 0.85,
    broken_threshold: float = 0.60,
) -> Dict[str, Any]:
    grouped = group_observations(observations)

    cases = [
        analyze_case(
            case_id=case_id,
            observations=items,
            fragile_threshold=fragile_threshold,
            broken_threshold=broken_threshold,
        )
        for case_id, items in sorted(grouped.items())
    ]

    rows = [asdict(c) for c in cases]

    invariant_cases = [r for r in rows if r["status"] == "invariant"]
    fragile_cases = [r for r in rows if r["status"] == "fragile"]
    broken_cases = [r for r in rows if r["status"] == "broken"]

    total_cases = len(rows)
    total_observations = len(observations)

    transformation_counter = Counter()
    transform_break_counter = Counter()

    for obs in observations:
        transformation_counter[obs.transform_id] += 1

    broken_case_ids = {r["case_id"] for r in broken_cases}
    fragile_case_ids = {r["case_id"] for r in fragile_cases}

    for obs in observations:
        if obs.case_id in broken_case_ids:
            transform_break_counter[obs.transform_id] += 1

    invariance_rate = len(invariant_cases) / total_cases if total_cases else 0.0
    fragile_rate = len(fragile_cases) / total_cases if total_cases else 0.0
    broken_rate = len(broken_cases) / total_cases if total_cases else 0.0

    mean_invariance_score = (
        sum(r["invariance_score"] for r in rows) / total_cases if total_cases else 0.0
    )

    worst_case = min(rows, key=lambda r: r["invariance_score"]) if rows else None

    summary = {
        "total_cases": total_cases,
        "total_observations": total_observations,
        "invariant_cases": len(invariant_cases),
        "fragile_cases": len(fragile_cases),
        "broken_cases": len(broken_cases),
        "invariance_rate": round(invariance_rate, 12),
        "fragile_rate": round(fragile_rate, 12),
        "broken_rate": round(broken_rate, 12),
        "mean_invariance_score": round(mean_invariance_score, 12),
        "worst_case_id": worst_case["case_id"] if worst_case else None,
        "worst_case_score": worst_case["invariance_score"] if worst_case else None,
        "problem_solved": "Measures whether case outputs remain structurally invariant under transformations.",
    }

    certificate = {
        "audit_type": "omnia_invariance_audit",
        "summary": summary,
        "thresholds": {
            "fragile_threshold": fragile_threshold,
            "broken_threshold": broken_threshold,
        },
        "boundary": "measurement only; invariance is structural compatibility under supplied transformations, not a semantic truth claim",
        "measurement_language": [
            "normalization",
            "pairwise_structural_similarity",
            "compatibility_score",
            "invariance_score",
            "max_distance",
            "invariant_fragile_broken",
        ],
    }

    return {
        "summary": summary,
        "thresholds": {
            "fragile_threshold": fragile_threshold,
            "broken_threshold": broken_threshold,
        },
        "certificate": certificate,
        "cases": rows,
        "transforms": {
            "observed_counts": dict(sorted(transformation_counter.items())),
            "broken_case_counts": dict(sorted(transform_break_counter.items())),
        },
    }


def write_json(path: str, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv_report(path: str, result: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "case_id",
        "status",
        "transforms",
        "unique_outputs",
        "invariance_score",
        "compatibility_score",
        "max_distance",
        "reference_output",
        "notes",
    ]

    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        for row in result["cases"]:
            out = dict(row)
            out["notes"] = " | ".join(row.get("notes", []))
            writer.writerow({k: out.get(k, "") for k in fields})


def html_escape(x: Any) -> str:
    return (
        str(x)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def write_html_report(path: str, result: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    summary = result["summary"]

    rows = []
    for r in result["cases"]:
        if r["status"] == "invariant":
            continue

        rows.append(
            "<tr>"
            + "<td>" + html_escape(r["case_id"]) + "</td>"
            + "<td>" + html_escape(r["status"]) + "</td>"
            + "<td>" + html_escape(r["transforms"]) + "</td>"
            + "<td>" + html_escape(r["unique_outputs"]) + "</td>"
            + "<td>" + html_escape(r["invariance_score"]) + "</td>"
            + "<td>" + html_escape(r["compatibility_score"]) + "</td>"
            + "<td>" + html_escape(r["max_distance"]) + "</td>"
            + "<td><pre>" + html_escape(json.dumps(r["outputs"], indent=2, ensure_ascii=False)) + "</pre></td>"
            + "</tr>"
        )

    html = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>OMNIA Invariance Report</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 32px;
      line-height: 1.45;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
    }}
    th, td {{
      border: 1px solid #ddd;
      padding: 8px;
      vertical-align: top;
    }}
    th {{
      background: #f2f2f2;
    }}
    pre {{
      white-space: pre-wrap;
      margin: 0;
    }}
    .box {{
      background: #f8f8f8;
      padding: 16px;
      margin-bottom: 24px;
      border: 1px solid #eee;
    }}
  </style>
</head>
<body>
  <h1>OMNIA Invariance Report</h1>

  <div class="box">
    <p><b>Total cases:</b> {total_cases}</p>
    <p><b>Total observations:</b> {total_observations}</p>
    <p><b>Invariant cases:</b> {invariant_cases}</p>
    <p><b>Fragile cases:</b> {fragile_cases}</p>
    <p><b>Broken cases:</b> {broken_cases}</p>
    <p><b>Invariance rate:</b> {invariance_rate}</p>
    <p><b>Mean invariance score:</b> {mean_invariance_score}</p>
    <p><b>Worst case:</b> {worst_case_id}</p>
  </div>

  <h2>Fragile / Broken Cases</h2>

  <table>
    <tr>
      <th>Case</th>
      <th>Status</th>
      <th>Transforms</th>
      <th>Unique outputs</th>
      <th>Invariance score</th>
      <th>Compatibility score</th>
      <th>Max distance</th>
      <th>Outputs</th>
    </tr>
    {rows}
  </table>

  <h2>Boundary</h2>
  <p>Invariance is measured as structural compatibility under supplied transformations. This is not a semantic truth claim.</p>
</body>
</html>
""".format(
        total_cases=summary["total_cases"],
        total_observations=summary["total_observations"],
        invariant_cases=summary["invariant_cases"],
        fragile_cases=summary["fragile_cases"],
        broken_cases=summary["broken_cases"],
        invariance_rate=summary["invariance_rate"],
        mean_invariance_score=summary["mean_invariance_score"],
        worst_case_id=summary["worst_case_id"],
        rows="".join(rows),
    )

    p.write_text(html, encoding="utf-8")


def write_case_jsonl(path: str, result: Dict[str, Any], status: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    with p.open("w", encoding="utf-8") as f:
        for r in result["cases"]:
            if r["status"] == status:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")


def write_all_reports(out_dir: str, result: Dict[str, Any]) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    write_json(str(out / "report.json"), result)
    write_csv_report(str(out / "report.csv"), result)
    write_html_report(str(out / "report.html"), result)
    write_case_jsonl(str(out / "fragile_cases.jsonl"), result, "fragile")
    write_case_jsonl(str(out / "broken_cases.jsonl"), result, "broken")
    write_json(str(out / "certificate.json"), result["certificate"])
