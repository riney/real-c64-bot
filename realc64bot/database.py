import datetime
import psycopg2

class Database:
    def __init__(self, host, database, username, password):
        self.conn = psycopg2.connect(f"host=%{host} dbname=%{database} user=%{username} password=%{password}")

    def is_tweet_completed(self, tweet_id):
        with self.conn.cursor() as c:
            c.execute("SELECT COUNT(*) FROM jobs WHERE tweet_id=%s", (tweet_id))
            results_count = c.fetchone()[]
            c.close()

            return results_count > 0

   def save_job(self, tweet_id, status):
       with self.conn.cursor() as c:
           c.execute(
               "INSERT INTO jobs (tweet_id, status, completed_at) VALUES (%s, %s, %s)",
                tweet_id, status, datetime.datetime.now()
            )
            c.close()
