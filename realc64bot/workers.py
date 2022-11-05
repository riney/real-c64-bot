from c64 import tokenize
from database import Database
from ultimate64 import run_program, upload_program

def execute_tweet(tweet):
    tweet_id = tweet['id']
    db = Database()
    print(f"Executing tweet: {tweet['text']}")
    filename = f"#{tweet['id']}.prg"
    tokenize(tweet['text'], filename)
    upload_program(filename)
    run_program()
    
    db.save_job(tweet_id, "done")

def reply():
    return
