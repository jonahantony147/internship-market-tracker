# Internship Market Tracker

Tracks tech internship postings over time and pulls out hiring trends: top posting companies, when roles open up, how categories shift by season.

## Data source

Daily snapshots of [SimplifyJobs/Summer2027-Internships](https://github.com/SimplifyJobs/Summer2027-Internships).

## Stack

- Python (requests, pandas) for ingestion
- SQLite for storage
- SQL for analysis
- matplotlib for charts
- GitHub Actions for daily scraping

## Structure

```
internship-market-tracker/
  data/       # tracker.db
  src/        # ingestion, schema, analysis
  charts/     # generated chart images
  .github/workflows/
```

## Setup

```bash
git clone https://github.com/jonahantony147/internship-market-tracker.git
cd internship-market-tracker
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

`data/tracker.db` is committed to the repo, so it comes pre-populated with whatever the daily scrape has collected so far. To start from a fresh, empty database instead:

```bash
rm data/tracker.db
sqlite3 data/tracker.db < src/schema.sql
```

Then pull the latest listings and generate charts:

```bash
python src/ingest.py     # fetches current listings, safe to re-run
python src/analyze.py    # writes PNGs to charts/
```

A GitHub Actions workflow (`.github/workflows/scrape.yml`) runs `ingest.py` daily and commits the updated database automatically, so a local `ingest.py` run is only needed for testing or catching up between snapshots.

## Findings (so far)

Postings skew heavily toward AI/ML/Data (~44%) and Software (~32%), with Hardware, Product, and Quant roles making up smaller shares. Posting duration and monthly timing trends are still thin since the tracker's only been collecting daily snapshots for a few days — those numbers will get more meaningful as more data builds up.

See `charts/` for the current breakdowns.
