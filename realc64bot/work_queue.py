import json
import pika

class WorkQueue:
    QUEUE_NAME = "incoming_messages"

    def __init__(self, host, username, password):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit.local'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=WorkQueue.QUEUE_NAME)

    def enqueue(self, message):
        self.channel.basic_publish(
            exchange = '',
            routing_key = WorkQueue.QUEUE_NAME,
            body = json.dumps(message),
            properties = pika.BasicProperties(
                delivery_mode = 2
            )
        )

    def close(self):
        self.connection.close()
