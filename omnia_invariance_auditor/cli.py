import argparse
import sys
from pathlib import Path

from .core import analyze_observations, read_jsonl, write_all_reports


def main():
    parser = argparse.ArgumentParser(
        prog="omnia-invariance-audit",
        description="Audit structural invariance under supplied transformations.",
    )

    parser.add_argument("--input", required=True, help="JSONL file with case/transform/output observations.")
    parser.add_argument("--out-dir", default="omnia_invariance_report", help="Output directory.")
    parser.add_argument("--fragile-threshold", type=float, default=0.85, help="Compatibility score threshold for fragile classification.")
    parser.add_argument("--broken-threshold", type=float, default=0.60, help="Compatibility score threshold below which a case is broken.")
    parser.add_argument("--fail-on-fragile", action="store_true", help="Exit with code 2 if fragile cases are detected, or 3 if broken cases are detected.")
    parser.add_argument("--fail-on-broken", action="store_true", help="Exit with code 3 if broken cases are detected.")

    args = parser.parse_args()

    try:
        observations = read_jsonl(args.input)
        result = analyze_observations(
            observations=observations,
            fragile_threshold=args.fragile_threshold,
            broken_threshold=args.broken_threshold,
        )
        write_all_reports(args.out_dir, result)
    except Exception as e:
        print("ERROR:", str(e))
        sys.exit(4)

    s = result["summary"]

    print("")
    print("OMNIA INVARIANCE AUDIT")
    print("======================")
    print(f"input:                 {args.input}")
    print(f"total_cases:           {s['total_cases']}")
    print(f"total_observations:    {s['total_observations']}")
    print(f"invariant_cases:       {s['invariant_cases']}")
    print(f"fragile_cases:         {s['fragile_cases']}")
    print(f"broken_cases:          {s['broken_cases']}")
    print(f"invariance_rate:       {s['invariance_rate']:.6f}")
    print(f"fragile_rate:          {s['fragile_rate']:.6f}")
    print(f"broken_rate:           {s['broken_rate']:.6f}")
    print(f"mean_invariance_score: {s['mean_invariance_score']:.6f}")
    print(f"worst_case_id:         {s['worst_case_id']}")
    print("")
    print(f"WROTE: {Path(args.out_dir) / 'report.json'}")
    print(f"WROTE: {Path(args.out_dir) / 'report.csv'}")
    print(f"WROTE: {Path(args.out_dir) / 'report.html'}")
    print(f"WROTE: {Path(args.out_dir) / 'fragile_cases.jsonl'}")
    print(f"WROTE: {Path(args.out_dir) / 'broken_cases.jsonl'}")
    print(f"WROTE: {Path(args.out_dir) / 'certificate.json'}")
    print("")

    if args.fail_on_broken and s["broken_cases"] > 0:
        sys.exit(3)

    if args.fail_on_fragile:
        if s["broken_cases"] > 0:
            sys.exit(3)
        if s["fragile_cases"] > 0:
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
