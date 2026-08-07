# Internship Market Tracker

A self-built data pipeline that tracks tech internship postings over time and analyzes hiring trends: which companies post the most, when roles tend to open, and how role categories shift over a season.

## Data source

Daily snapshots of [SimplifyJobs/Summer2027-Internships](https://github.com/SimplifyJobs/Summer2027-Internships), a community-maintained tracker of software engineering, data science, and related internship postings.

## Status

Work in progress. Built step by step as a portfolio project.

## Stack

- Python (requests, pandas) for ingestion
- SQLite for storage
- SQL for analysis (joins, window functions, aggregation)
- matplotlib for visualization
- GitHub Actions for daily scheduled scraping

## Project structure

```
internship-market-tracker/
  data/           # SQLite database lives here
  src/            # ingestion, schema, and analysis scripts
  notebooks/      # exploratory analysis
  .github/
    workflows/    # scheduled scraper
```
