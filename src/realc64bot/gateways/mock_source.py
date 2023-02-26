import logging, random, sys, traceback
from realc64bot.config import Config
from realc64bot.connectors.work_queue import WorkQueue

q = None

def mock_notification(id, content):
        message = {
            "message_id": id,
            "message_source": "mock",
            "content": content,
        }

        print(f"mock_source: mock_notification: queue channel open? {q.channel.is_open}")
        print(f"mock_source: mock_notification: enqueuing message {message}")

        q.enqueue(message, WorkQueue.MESSAGES_QUEUE)

def main():
    config = Config().values()

    random.seed()

    try:
        print("mock_source: connecting to work queue")
        global q
        q = WorkQueue()
        
        id = str(random.randint(0, 100000))

        mock_notification(id, '10 PRINT "HELLO MOCK"')        
    except Exception:
        print("mock_source: exception")

        traceback.print_exc(file=sys.stdout)

    print("mock_source: Closing work queue")
    q.close()
    
    print("mock_source: exiting")    
    sys.exit(0)

if __name__ == "__main__":
    print("mock_source: in startup")
    main()
