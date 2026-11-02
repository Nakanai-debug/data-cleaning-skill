# Data Analyst Portfolio — Interview Projects

**[View three runnable synthetic-data portfolio demos](portfolio/README.md)**: Hotel Revenue Analysis, E-commerce SQL Metrics, and Python + Excel Automation.

These are educational demonstrations using synthetic records, not company data or verified production impact.

---

## Other experiments in this repository

### Random joke generator

The project now includes a small command-line random joke generator backed by [JokeAPI](https://v2.jokeapi.dev/).

## Run it

After installation:

```bash
pip install -r requirements.txt
pip install -e .
joke
joke --safe
joke --category Programming
```

The generator supports both JokeAPI response formats:

- `single`: prints one joke line.
- `twopart`: prints setup and delivery on separate lines.

The API request uses a timeout and converts network, HTTP, malformed JSON, and API errors into a readable `JokeAPIError`.

## Data-cleaning pipeline

The original data-cleaning commands remain available:

```bash
data-clean --input data/raw/input.csv --output data/processed/cleaned.csv --report reports/quality.json --config configs/default.yaml
```
