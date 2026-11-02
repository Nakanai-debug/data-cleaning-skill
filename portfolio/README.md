# Data Analyst Portfolio — TO PHUONG THUY

Three runnable **synthetic-data** projects for Data Analyst / Business Data Analyst interviews.

| Project | Main skill |
|---|---|
| [Hotel Revenue Analysis](hotel-revenue-analysis/) | Occupancy, ADR, RevPAR, data validation |
| [E-commerce Metrics](ecommerce-metrics/) | SQL, GMV, AOV, repeat purchase |
| [Python + Excel Automation](excel-automation/) | CSV validation, logging, Excel reporting |

## Run (Python 3.10+)
```bash
pip install -r portfolio/requirements.txt
python portfolio/hotel-revenue-analysis/analyze.py
python portfolio/ecommerce-metrics/analyze.py
python portfolio/excel-automation/pipeline.py
python -m unittest discover -s portfolio/excel-automation -p 'test_*.py'
```

Outputs appear under each project's `output/` directory. All sample records are **synthetic**. These demos do not represent verified client results, production deployments or historical business impact.

## Interview flow
Business question → KPI definition → sample data → SQL/Python → generated report → caveat → recommended next analysis.
