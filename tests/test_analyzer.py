import io
import unittest

from datacheck.analyzer import DataCheckError, analyze_csv


def inspect(text):
    return analyze_csv(io.StringIO(text, newline=""))


class AnalyzerTests(unittest.TestCase):
    def test_missing_and_duplicate_statistics(self):
        report = inspect("name,city\nAlice,Suzhou\nBob, \nAlice,Suzhou\n")
        self.assertEqual(report["row_count"], 3)
        self.assertEqual(report["column_count"], 2)
        self.assertEqual(report["missing_cell_count"], 1)
        self.assertEqual(report["duplicate_row_count"], 1)
        self.assertEqual(report["duplicate_record_examples"], [4])
        self.assertEqual(report["columns"][1], {
            "name": "city", "missing_count": 1, "missing_ratio": 0.3333,
        })

    def test_header_only_has_zero_ratios(self):
        report = inspect("name,city\n")
        self.assertEqual(report["row_count"], 0)
        self.assertEqual(report["columns"][0]["missing_ratio"], 0.0)

    def test_whitespace_normalization_and_zero_is_not_missing(self):
        report = inspect(" value \n 0 \n0\n \n")
        self.assertEqual(report["columns"][0]["name"], "value")
        self.assertEqual(report["missing_cell_count"], 1)
        self.assertEqual(report["duplicate_row_count"], 1)

    def test_quoted_commas_and_multiline_values(self):
        report = inspect('name,note\n"Alice,Bob","line1\nline2"\n')
        self.assertEqual(report["row_count"], 1)
        self.assertEqual(report["missing_cell_count"], 0)

    def test_blank_physical_lines_are_ignored(self):
        self.assertEqual(inspect("name\n\nAlice\n\n")["row_count"], 1)

    def test_literal_null_is_not_missing(self):
        self.assertEqual(inspect("value\nNULL\nNaN\n0\n")["missing_cell_count"], 0)

    def test_duplicate_examples_are_bounded_but_count_is_exact(self):
        report = inspect("name\n" + "Alice\n" * 10)
        self.assertEqual(report["duplicate_row_count"], 9)
        self.assertEqual(report["duplicate_record_examples"], [3, 4, 5, 6, 7])

    def test_invalid_headers(self):
        for text in ("", "\n", "a,\n", "a, a\n", " ,b\n"):
            with self.subTest(text=text), self.assertRaises(DataCheckError):
                inspect(text)

    def test_wrong_row_width_is_rejected(self):
        for text in ("a,b\n1\n", "a,b\n1,2,3\n"):
            with self.subTest(text=text), self.assertRaisesRegex(DataCheckError, "Record 2"):
                inspect(text)

    def test_unclosed_quote_is_rejected(self):
        with self.assertRaisesRegex(DataCheckError, "Invalid CSV"):
            inspect('name\n"Alice\n')


if __name__ == "__main__":
    unittest.main()
