"""Auditable raw CSV cleaning: preserve raw, quarantine invalid rows, report quality."""
import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

SCHEMAS = {
    "ecommerce": ("order_id", "brand", "price", "date"),
    "hotel": ("booking_id", "check_in", "check_out", "room_rate", "status"),
}
STATUSES = {"confirmed", "checked_in", "checked_out", "cancelled"}

def parse_date(value):
    value = value.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    return None

def positive_number(value):
    try:
        number = Decimal(value.strip())
        return number if number.is_finite() and number >= 0 else None
    except (InvalidOperation, AttributeError):
        return None

def clean_csv(source, output_dir, domain):
    if domain not in SCHEMAS:
        raise ValueError("Unsupported domain")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(source, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no header")
        required = SCHEMAS[domain]
        missing = [c for c in required if c not in reader.fieldnames]
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(missing))
        rows = list(reader)
        columns = list(reader.fieldnames)
    counts = Counter((r["order_id"] if domain == "ecommerce" else r["booking_id"]).strip() for r in rows)
    valid, quarantine, issues = [], [], Counter()
    for row_number, original in enumerate(rows, start=2):
        row = dict(original)
        errors = []
        key = (row["order_id"] if domain == "ecommerce" else row["booking_id"]).strip()
        if not key:
            errors.append("MISSING_ID")
        elif counts[key] > 1:
            errors.append("DUPLICATE_ID_REVIEW")
        if domain == "ecommerce":
            row["brand"] = row["brand"].strip().title()
            date = parse_date(row["date"])
            if date is None:
                errors.append("INVALID_DATE")
            else:
                row["date"] = date.isoformat()
            amount = positive_number(row["price"])
            if amount is None:
                errors.append("INVALID_PRICE")
            else:
                row["price"] = str(amount)
            if not row["brand"]:
                errors.append("MISSING_BRAND")
        else:
            start, end = parse_date(row["check_in"]), parse_date(row["check_out"])
            if not start or not end:
                errors.append("INVALID_DATE")
            elif end <= start:
                errors.append("INVALID_STAY_DATES")
            else:
                row["check_in"], row["check_out"] = start.isoformat(), end.isoformat()
            rate = positive_number(row["room_rate"])
            if rate is None:
                errors.append("INVALID_ROOM_RATE")
            else:
                row["room_rate"] = str(rate)
            row["status"] = row["status"].strip().lower()
            if row["status"] not in STATUSES:
                errors.append("INVALID_STATUS")
        if errors:
            issues.update(errors)
            quarantine.append({**original, "source_row": row_number, "error_codes": "|".join(errors)})
        else:
            valid.append({**row, "source_row": row_number})
    def write(name, records, fields):
        with open(output_dir / name, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(records)
    write("clean.csv", valid, columns + ["source_row"])
    write("quarantine.csv", quarantine, columns + ["source_row", "error_codes"])
    report = {
        "domain": domain, "input_rows": len(rows), "clean_rows": len(valid),
        "quarantine_rows": len(quarantine), "issue_counts": dict(sorted(issues.items())),
        "reconciliation_passed": len(rows) == len(valid) + len(quarantine),
        "note": "All source records preserved in clean or quarantine; duplicate IDs require domain review.",
    }
    (output_dir / "quality_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--domain", choices=SCHEMAS, required=True)
    args = parser.parse_args()
    print(json.dumps(clean_csv(args.input, args.output, args.domain), indent=2))
