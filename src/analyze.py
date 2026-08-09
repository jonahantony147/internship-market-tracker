"""Charts internship posting trends from tracker.db."""
import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "tracker.db"
CHARTS_DIR = PROJECT_ROOT / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

query = """
    SELECT c.name, COUNT(*) AS posting_count
    FROM postings p
    JOIN companies c ON p.company_id = c.company_id
    GROUP BY c.name
    ORDER BY posting_count DESC
    LIMIT 10
"""
top_companies = pd.read_sql_query(query, conn)
print(top_companies)

plt.figure(figsize=(10, 6))
plt.barh(top_companies["name"], top_companies["posting_count"])
plt.xlabel("Number of Postings")
plt.title("Top 10 Companies by Internship Postings")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(CHARTS_DIR / "top_companies.png")
plt.show()

category_query = """
    SELECT
        CASE
            WHEN category IN ('Software', 'Software Engineering') THEN 'Software'
            WHEN category IN ('AI/ML/Data', 'Data Science, AI & Machine Learning') THEN 'AI/ML/Data'
            ELSE category
        END AS clean_category,
        COUNT(*) AS posting_count
    FROM postings
    GROUP BY clean_category
    ORDER BY posting_count DESC
"""

categories = pd.read_sql_query(category_query, conn)
threshold = 0.02  # anything under 2% of total gets grouped
categories["share"] = categories["posting_count"] / categories["posting_count"].sum()
main = categories[categories["share"] >= threshold]
other_total = categories[categories["share"] < threshold]["posting_count"].sum()

if other_total > 0:
    other_row = pd.DataFrame([{"clean_category": "Other", "posting_count": other_total}])
    categories = pd.concat([main, other_row], ignore_index=True)

plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(categories["posting_count"], autopct="%1.1f%%")
plt.legend(wedges, categories["clean_category"], title="Category", loc="center left", bbox_to_anchor=(1, 0.5))
plt.title("Internship Postings by Category")
plt.tight_layout()
plt.savefig(CHARTS_DIR / "category_breakdown.png")
plt.show()

timing_query = """
    SELECT
        strftime('%m', date_posted) AS month,
        COUNT(*) AS posting_count
    FROM postings
    GROUP BY month
    ORDER BY month
"""
timing = pd.read_sql_query(timing_query, conn)

plt.figure(figsize=(10, 6))
plt.bar(timing["month"], timing["posting_count"])
plt.xlabel("Month")
plt.ylabel("Number of Postings")
plt.title("Internship Postings by Month")
plt.tight_layout()
plt.savefig(CHARTS_DIR / "postings_by_month.png")
plt.show()
