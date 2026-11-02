# Raw Data Quality & Cleaning Pipeline

**Verified prototype using synthetic data.** No customer data or production impact claims.

## Business problem
Raw order and booking exports may contain duplicate identifiers, inconsistent dates, missing prices, invalid values and conflicting statuses. These defects can corrupt reports if silently dropped or corrected.

## Pipeline
Raw CSV → schema checks → field standardization and business rules → clean / quarantine split → reconciliation and quality report. Original input remains unchanged.

## Reproduce (Python 3.10+, standard library only)
```bash
python portfolio/raw-data-quality/clean.py --domain ecommerce --input portfolio/raw-data-quality/data/ecommerce_raw.csv --output portfolio/raw-data-quality/output/ecommerce
python portfolio/raw-data-quality/clean.py --domain hotel --input portfolio/raw-data-quality/data/hotel_raw.csv --output portfolio/raw-data-quality/output/hotel
python -m unittest discover -s portfolio/raw-data-quality -p 'test_*.py'
```

## Verified results
| Domain | Input | Clean | Quarantine | Reconciled |
|---|---:|---:|---:|---|
| E-commerce | 5 | 2 | 3 | Yes |
| Hotel | 4 | 2 | 2 | Yes |

See [RESULTS.md](RESULTS.md) for before/after evidence and `output/` for generated CSV and JSON. All three unit tests passed in local execution on 2026-11-03.

## Quality policy
- Preserve raw files and source row numbers.
- Quarantine duplicate IDs for review; do not silently deduplicate.
- Flag negative or missing amounts rather than inventing values.
- Flag reversed hotel dates rather than swapping them.
- Output `clean.csv`, `quarantine.csv`, `quality_report.json`.
- Reconcile input count = clean count + quarantine count.

## Limitations
Fixtures are tiny and synthetic. Brand title-casing is not a verified brand master; ID uniqueness depends on source grain; booking statuses depend on source system. No real-world performance benchmark or automated correction audit trail yet.
