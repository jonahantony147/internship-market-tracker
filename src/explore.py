"""
Quick exploratory look at the raw listings.json feed before designing
the database schema. Run this yourself in Spyder to poke around further,
the point isn't the output, it's getting a feel for what the real data
looks like so the schema fits reality instead of guesswork.
"""
import json
from datetime import datetime, timezone

import pandas as pd
import requests

SOURCE_URL = (
    "https://raw.githubusercontent.com/SimplifyJobs/"
    "Summer2027-Internships/dev/.github/scripts/listings.json"
)


def fetch_listings() -> list[dict]:
    resp = requests.get(SOURCE_URL, timeout=30)
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    data = fetch_listings()
    df = pd.json_normalize(data)

    print("total entries:", len(df))
    print("\ncolumns:", list(df.columns))
    print("\nnulls per column:\n", df.isna().sum())
    print("\ncategory counts:\n", df["category"].value_counts())
    print("\nactive counts:\n", df["active"].value_counts())
    print("\nunique companies:", df["company_name"].nunique())
    print(
        "\ndate_posted range:",
        datetime.fromtimestamp(df["date_posted"].min(), tz=timezone.utc),
        "to",
        datetime.fromtimestamp(df["date_posted"].max(), tz=timezone.utc),
    )
    print("\nduplicate ids:", df["id"].duplicated().sum())


if __name__ == "__main__":
    main()
