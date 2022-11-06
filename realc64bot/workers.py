from c64 import tokenize
from database import Database
from ultimate64 import run_program, upload_program

def execute_message(message):
    id = message['id']
    db = Database()
    print(f"Executing message: {message['text']}")
    filename = f"#{message['id']}.prg"
    tokenize(message['text'], filename)
    upload_program(filename)
    run_program()
    
    db.save_job(id, "done")

def reply():
    return
