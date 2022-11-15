CREATE TABLE jobs (
    id              SERIAL PRIMARY KEY,
    message_id      TEXT,
    message_source  TEXT,
    job_status      TEXT,
    completed_at    TIMESTAMP
);

CREATE INDEX ON jobs (message_id, message_source);
