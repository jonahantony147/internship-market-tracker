-- internship tracker schema
-- run once to set up the database

CREATE TABLE companies (
    company_id  INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    company_url TEXT
);

CREATE TABLE postings (
    id          TEXT PRIMARY KEY,
    company_id  INTEGER NOT NULL REFERENCES companies(company_id),
    title       TEXT NOT NULL,
    category    TEXT,
    term        TEXT,
    date_posted TEXT
);

CREATE TABLE posting_locations (
    posting_id TEXT NOT NULL REFERENCES postings(id),
    location   TEXT NOT NULL,
    PRIMARY KEY (posting_id, location)
);

CREATE TABLE snapshots (
    snapshot_id   INTEGER PRIMARY KEY,
    posting_id    TEXT NOT NULL REFERENCES postings(id),
    snapshot_date TEXT NOT NULL,
    is_active     INTEGER NOT NULL,
    UNIQUE (posting_id, snapshot_date)
);
