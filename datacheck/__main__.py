"""Run with: python -m datacheck examples/orders.csv"""

import argparse
import json
from pathlib import Path
import sys

from datacheck.analyzer import DataCheckError, analyze_csv


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect a UTF-8 CSV and produce a JSON quality report.")
    parser.add_argument("input", type=Path, help="CSV file with a header; UTF-8 BOM is supported")
    parser.add_argument("-o", "--output", type=Path, help="Write to a new JSON file (never overwrite)")
    args = parser.parse_args(argv)

    try:
        if args.output and args.output.resolve() == args.input.resolve():
            raise DataCheckError("Output must be different from the input file.")
        with args.input.open(encoding="utf-8-sig", newline="") as stream:
            report = analyze_csv(stream)
        payload = json.dumps(report, ensure_ascii=True, indent=2) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(payload)
        else:
            sys.stdout.write(payload)
    except (DataCheckError, OSError, UnicodeError) as exc:
        print(f"datacheck: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
