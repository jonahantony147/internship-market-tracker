"""
Fetches the current internship listings and loads them into tracker.db.

Safe to run more than once, INSERT OR IGNORE means re-running this on data
we've already stored just skips the duplicates instead of erroring out.
The only thing that grows every run is one new row per posting in
`snapshots`, dated with today's date, that's what builds history over time.
"""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import requests

SOURCE_URL = (
    "https://raw.githubusercontent.com/SimplifyJobs/"
    "Summer2027-Internships/dev/.github/scripts/listings.json"
)

# Find data/tracker.db relative to this script's own location on disk,
# instead of relative to whatever folder happens to be "current" when it
# runs. That "current directory" changes depending on how you run it
# (Spyder, VS Code, a terminal), which is exactly what broke last time.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "tracker.db"


def fetch_listings() -> list[dict]:
    resp = requests.get(SOURCE_URL, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_or_create_company(cur, name: str, company_url: str) -> int:
    # try to insert; if the name already exists, this silently does nothing
    cur.execute(
        "INSERT OR IGNORE INTO companies (name, company_url) VALUES (?, ?)",
        (name, company_url),
    )
    # then look up the id either way, whether we just created it or it already existed
    cur.execute("SELECT company_id FROM companies WHERE name = ?", (name,))
    return cur.fetchone()[0]


def main() -> None:
    listings = fetch_listings()
    today = datetime.now(timezone.utc).date().isoformat()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for entry in listings:
        company_id = get_or_create_company(
            cur, entry["company_name"], entry.get("company_url", "")
        )

        date_posted = datetime.fromtimestamp(
            entry["date_posted"], tz=timezone.utc
        ).date().isoformat()
        term = entry["terms"][0] if entry["terms"] else None

        cur.execute(
            """
            INSERT OR IGNORE INTO postings
                (id, company_id, title, category, term, date_posted)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (entry["id"], company_id, entry["title"], entry["category"], term, date_posted),
        )

        for location in entry["locations"]:
            cur.execute(
                "INSERT OR IGNORE INTO posting_locations (posting_id, location) VALUES (?, ?)",
                (entry["id"], location),
            )

        cur.execute(
            """
            INSERT OR IGNORE INTO snapshots (posting_id, snapshot_date, is_active)
            VALUES (?, ?, ?)
            """,
            (entry["id"], today, int(entry["active"])),
        )

    conn.commit()

    # quick sanity check printed at the end
    for table in ["companies", "postings", "posting_locations", "snapshots"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"{table}: {cur.fetchone()[0]} rows")

    conn.close()


if __name__ == "__main__":
    main()
