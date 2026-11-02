# Python + Excel Automation — synthetic data quality demo

**Question:** Can recurring CSV files be checked and converted into auditable Excel reports?

**Run from repository root:**
```bash
pip install -r portfolio/requirements.txt
python portfolio/excel-automation/pipeline.py
python portfolio/excel-automation/pipeline.py --input portfolio/excel-automation/data/sales_invalid.csv --output portfolio/excel-automation/output/invalid_demo.xlsx
python -m unittest discover -s portfolio/excel-automation -p 'test_*.py'
```

**Files:** `pipeline.py`, `test_pipeline.py`, synthetic valid and invalid CSV fixtures.

**Output:** `output/sales_report.xlsx` with Clean Data, Summary + chart and Validation Errors; `output/pipeline.log` logs invalid rows.

**Validation:** required columns, duplicate IDs, ISO date format, non-negative numeric revenue, empty keys.

**Interview:** Show valid output, invalid input, error sheet and explain how validation protects reporting. No real-world time savings claimed.
