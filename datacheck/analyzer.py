"""CSV inspection independent of the command-line interface."""

import csv
from typing import Iterator, TextIO


class DataCheckError(ValueError):
    """The input cannot be interpreted with our CSV contract."""


def analyze_csv(stream: TextIO) -> dict:
    """Inspect comma-separated CSV; record numbers include the header as 1.

    Whitespace is stripped for headers, missing values and duplicate checks.
    Empty records from blank physical lines are ignored. Memory grows with the
    number of distinct records because duplicate detection is exact.
    """
    reader = csv.reader(stream, strict=True)
    try:
        return _analyze(reader)
    except csv.Error as exc:
        raise DataCheckError(f"Invalid CSV near physical line {reader.line_num}: {exc}") from exc


def _analyze(reader: Iterator[list[str]]) -> dict:
    try:
        columns = [value.strip() for value in next(reader)]
    except StopIteration as exc:
        raise DataCheckError("CSV is empty; a header is required.") from exc

    if not columns or any(not name for name in columns):
        raise DataCheckError("Every column needs a non-empty header.")
    if len(set(columns)) != len(columns):
        raise DataCheckError("Column headers must be unique after stripping whitespace.")

    missing = [0] * len(columns)
    seen: set[tuple[str, ...]] = set()
    duplicate_examples: list[int] = []
    duplicate_count = 0
    row_count = 0

    for raw_row in reader:
        if not raw_row:
            continue
        record_number = row_count + 2
        if len(raw_row) != len(columns):
            raise DataCheckError(
                f"Record {record_number}: expected {len(columns)} fields, got {len(raw_row)}."
            )
        row = tuple(value.strip() for value in raw_row)
        row_count += 1
        for index, value in enumerate(row):
            if value == "":
                missing[index] += 1
        if row in seen:
            duplicate_count += 1
            if len(duplicate_examples) < 5:
                duplicate_examples.append(record_number)
        else:
            seen.add(row)

    return {
        "schema_version": 1,
        "row_count": row_count,
        "column_count": len(columns),
        "missing_cell_count": sum(missing),
        "duplicate_row_count": duplicate_count,
        "duplicate_record_examples": duplicate_examples,
        "columns": [
            {
                "name": name,
                "missing_count": count,
                "missing_ratio": round(count / row_count, 4) if row_count else 0.0,
            }
            for name, count in zip(columns, missing)
        ],
    }
