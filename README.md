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
  notebooks/  # exploration
  .github/workflows/
```
