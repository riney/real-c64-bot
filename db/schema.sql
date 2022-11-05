DROP TABLE jobs;

CREATE TABLE jobs (
    id              SERIAL PRIMARY KEY,
    tweet_id        TEXT,
    job_status      TEXT,
    completed_at    TIMESTAMP
);

CREATE INDEX ON jobs (tweet_id);
