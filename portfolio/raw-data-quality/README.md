# Raw Data Quality & Cleaning Pipeline

**Status:** Working prototype with synthetic examples; no production claims.

## Business problem
Raw commerce orders and hotel reservations often contain duplicates, inconsistent dates, missing prices, invalid values, and conflicting statuses. Reporting directly from such records can distort KPIs.

## Approach
- Preserve original CSV unchanged.
- Profile required fields and duplicate identifiers.
- Normalize supported date formats, brand labels, and booking statuses.
- Validate domain-specific business rules.
- Split records into **clean.csv** and **quarantine.csv**; keep original row numbers and explicit error codes.
- Generate **quality_report.json** with issue counts and input/output reconciliation.

## Reproduce (Python 3.10+, standard library only)
From the repository root:

```bash
python portfolio/raw-data-quality/clean.py --domain ecommerce --input portfolio/raw-data-quality/data/ecommerce_raw.csv --output portfolio/raw-data-quality/output/ecommerce
python portfolio/raw-data-quality/clean.py --domain hotel --input portfolio/raw-data-quality/data/hotel_raw.csv --output portfolio/raw-data-quality/output/hotel
python -m unittest discover -s portfolio/raw-data-quality -p 'test_*.py'
```

## Output
- `clean.csv`: validated records with normalized fields.
- `quarantine.csv`: original invalid records, source row, reason codes.
- `quality_report.json`: counts, error distribution, reconciliation.

## Data quality policy
- Duplicate IDs are **quarantined for review**, not silently dropped. Real order-item data may legitimately repeat order IDs.
- Negative prices and room rates are flagged, not converted to positive numbers.
- Missing prices are not invented.
- Invalid date order is flagged, not swapped.
- Date parsing accepts ISO and day-first slash format only.
- All input records must appear in exactly one output.

## Limitations
Synthetic fixtures; simple title-casing is not a full brand dictionary. No PII, no external data ingestion, no automatic duplicate resolution, no production benchmark. The hotel example treats one booking ID as one record. Additional source-specific rules would be needed for real PMS data.

## Interview demo
Show a raw record, the corresponding quarantine error code, the quality report, then explain why business rules prevent silent data corruption.
