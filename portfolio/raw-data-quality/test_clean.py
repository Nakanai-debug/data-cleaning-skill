import csv
import json
import tempfile
import unittest
from pathlib import Path
from clean import clean_csv

ROOT = Path(__file__).parent

class DataQualityTests(unittest.TestCase):
    def test_ecommerce_reconciliation_and_issues(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = clean_csv(ROOT / "data/ecommerce_raw.csv", tmp, "ecommerce")
            self.assertEqual(result["input_rows"], 5)
            self.assertEqual(result["clean_rows"], 2)
            self.assertEqual(result["quarantine_rows"], 3)
            self.assertTrue(result["reconciliation_passed"])
            self.assertEqual(result["issue_counts"]["DUPLICATE_ID_REVIEW"], 2)
            with open(Path(tmp) / "clean.csv", newline="") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(rows[0]["brand"], "Apple")
    def test_hotel_dates_and_rate(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = clean_csv(ROOT / "data/hotel_raw.csv", tmp, "hotel")
            self.assertEqual(result["clean_rows"], 2)
            self.assertEqual(result["quarantine_rows"], 2)
            self.assertIn("INVALID_STAY_DATES", result["issue_counts"])
    def test_missing_schema_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "bad.csv"
            src.write_text("order_id,price\n1,20\n")
            with self.assertRaisesRegex(ValueError, "Missing required columns"):
                clean_csv(src, Path(tmp) / "out", "ecommerce")

if __name__ == "__main__":
    unittest.main()
