# Hotel Revenue Analysis — synthetic data demo

**Question:** Which months show stronger hotel demand and revenue productivity?

**Metrics:** Occupancy = sold room nights / available room nights; ADR = room revenue / sold room nights; RevPAR = room revenue / available room nights.

**Run:** From repo root: `python portfolio/hotel-revenue-analysis/analyze.py`.

**Files:** `data/hotel_monthly.csv` contains synthetic monthly data. `analyze.py` validates sold room nights against capacity and writes `output/monthly_kpis.csv`.

**Interview:** Explain whether RevPAR changes are caused by occupancy or room rate. Do not present sample seasonality as a real business finding.

**Next:** Add channel, cancellation and room-type data and build a dashboard.
