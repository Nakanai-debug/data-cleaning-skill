# E-commerce Metrics — synthetic SQL demo

**Question:** How do GMV, AOV, category contribution and repeat purchasing vary?

**Run:** From repo root: `python portfolio/ecommerce-metrics/analyze.py`.

**Files:** `data/orders.csv` is a small synthetic sample; `metrics.sql` contains three SQLite queries; `analyze.py` executes them and exports CSVs under `output/`.

**KPI definitions:** GMV = sum of completed order amounts for this demo; AOV = GMV / completed orders; repeat purchase = customers with 2+ completed orders / customers with 1+ completed orders. Repeat purchase is **not** cohort retention.

**Caveats:** One category per order, no refunds, discounts, traffic or marketing spend. CAC and conversion cannot be calculated with this input.

**Next:** Expand to PostgreSQL with order items, refunds, traffic and marketing costs.
