# Verified demo results (synthetic fixtures)

Executed locally on 2026-11-03 with Python standard library. All 3 unit tests passed.

| Dataset | Input rows | Clean | Quarantine | Reconciled |
|---|---:|---:|---:|---|
| E-commerce | 5 | 2 | 3 | Yes |
| Hotel | 4 | 2 | 2 | Yes |

## Before / After examples

| Source row | Before | After / action |
|---|---|---|
| E-commerce 2 | ` Apple ` | `Apple` (clean) |
| E-commerce 6 | `samsung`, `04/10/2026` | `Samsung`, `2026-10-04` (clean) |
| E-commerce 3–4 | duplicated `A002`, negative price | Quarantine: `DUPLICATE_ID_REVIEW`, `INVALID_PRICE` |
| E-commerce 5 | missing price | Quarantine: `INVALID_PRICE` |
| Hotel 4 | `01/10/2026`, `CHECKED_OUT` | `2026-10-01`, `checked_out` (clean) |
| Hotel 3 | check-out before check-in | Quarantine: `INVALID_STAY_DATES` |
| Hotel 5 | negative rate and unknown status | Quarantine: `INVALID_ROOM_RATE`, `INVALID_STATUS` |

**Caution:** Issue counts count rule violations, not unique records. A record may have multiple issues. Synthetic demonstration only.
