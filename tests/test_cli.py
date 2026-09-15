import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "datacheck", *map(str, args)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )


class CliTests(unittest.TestCase):
    def test_sample_report(self):
        result = run_cli("examples/orders.csv")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["row_count"], 5)
        self.assertEqual(report["missing_cell_count"], 3)
        self.assertEqual(report["duplicate_row_count"], 1)

    def test_missing_file_is_an_actionable_error(self):
        with tempfile.TemporaryDirectory() as folder:
            result = run_cli(Path(folder) / "missing.csv")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("datacheck:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_bom_chinese_and_output_file(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "input.csv"
            output = Path(folder) / "report.json"
            source.write_text("城市,人数\n苏州,0\n", encoding="utf-8-sig")
            result = run_cli(source, "--output", output)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["columns"][0]["name"], "城市")
            self.assertEqual(report["missing_cell_count"], 0)
            self.assertEqual(result.stdout, "")

    def test_input_file_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "input.csv"
            original = "name\nAlice\n"
            source.write_text(original, encoding="utf-8")
            result = run_cli(source, "-o", source)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(source.read_text(encoding="utf-8"), original)

    def test_existing_output_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "existing.json"
            output.write_text("keep me", encoding="utf-8")
            result = run_cli("examples/orders.csv", "-o", output)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(output.read_text(encoding="utf-8"), "keep me")

    def test_invalid_encoding_has_no_traceback(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "invalid.csv"
            source.write_bytes(b"name\n\xff\n")
            result = run_cli(source)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_invalid_csv_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "invalid.csv"
            output = Path(folder) / "report.json"
            source.write_text("a,b\n1\n", encoding="utf-8")
            result = run_cli(source, "-o", output)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
