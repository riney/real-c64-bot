
CREATE TABLE jobs (
    id              SERIAL PRIMARY KEY,
    message_source  TEXT,
    message_id      TEXT,
    job_status      TEXT,
    completed_at    TIMESTAMP
);

CREATE INDEX ON jobs (message_source, message_id);
