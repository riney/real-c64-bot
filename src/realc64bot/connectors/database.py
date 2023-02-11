import datetime
import psycopg2

class Database:
    def __init__(self, host, database, username, password):
        self.conn = psycopg2.connect(f"host=%{host} dbname=%{database} user=%{username} password=%{password}")

    def is_message_completed(self, message_id, message_source):
        with self.conn.cursor() as c:
            c.execute("SELECT COUNT(*) FROM jobs WHERE message_id=%s AND message_source=%s", (message_id, message_source))
            results_count = c.fetchone()[0]
            c.close()

            return results_count > 0

    def save_job(self, message_id, message_source, status):
        with self.conn.cursor() as c:
            c.execute(
                "INSERT INTO jobs (message_id, message_source, status, completed_at) VALUES (%s, %s, %s, %s)",
                message_id, message_source, status, datetime.datetime.now()
            )
            c.close()
