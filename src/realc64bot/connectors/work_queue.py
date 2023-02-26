import json
import logging
import pika
from realc64bot.config import Config

class WorkQueue:
    MESSAGES_QUEUE         = "messages"
    TOKENIZE_QUEUE         = "tokenize"
    RUN_AND_CAPTURE_QUEUE  = "runAndCapture"
    UPLOAD_VIDEO_QUEUE     = "upload"
    REPLY_QUEUE            = "reply"

    QUEUES = [ MESSAGES_QUEUE, TOKENIZE_QUEUE, RUN_AND_CAPTURE_QUEUE, UPLOAD_VIDEO_QUEUE, REPLY_QUEUE ]

    def __init__(self, host=None, username=None, password=None):
        #logging.getLogger("pika").setLevel(logging.DEBUG)
        print(f"WorkQueue: init")

        # Load configuration defaults, if needed
        config = Config().values()
        if host is None:
            host = config['rabbitmq']['host']
        if username is None:
            username = config['rabbitmq']['username']
        if password is None:
            password = config['rabbitmq']['password']

        # connect
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host = host, credentials = credentials))

        self.channel = self.connection.channel()
        
        print(f"WorkQueue: declaring queues")
        for queue in self.QUEUES:
            self.channel.queue_declare(queue=queue)

    def enqueue(self, message, queue):
        print(f"WorkQueue: enqueue: publishing {json.dumps(message)} to {queue}")

        self.channel.basic_publish(
            '',
            queue,
            json.dumps(message)
        )

    def close(self):
        self.connection.close()
