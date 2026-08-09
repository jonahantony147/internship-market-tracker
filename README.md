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

## Findings (so far)

Postings skew heavily toward AI/ML/Data (~44%) and Software (~32%), with Hardware, Product, and Quant roles making up smaller shares. Posting duration and monthly timing trends are still thin since the tracker's only been collecting daily snapshots for a few days — those numbers will get more meaningful as more data builds up.

See `charts/` for the current breakdowns.
