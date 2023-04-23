import json
import logging
import aio_pika
from realc64bot.config import Config

logger = logging.getLogger('queue_worker')
logging.basicConfig(level=logging.INFO)

class QueueWorker:
    MESSAGES_QUEUE         = "messages"
    TOKENIZE_QUEUE         = "tokenize"
    RUN_AND_CAPTURE_QUEUE  = "runAndCapture"
    UPLOAD_VIDEO_QUEUE     = "upload"
    REPLY_QUEUE            = "reply"

    QUEUES = [ MESSAGES_QUEUE, TOKENIZE_QUEUE, RUN_AND_CAPTURE_QUEUE, UPLOAD_VIDEO_QUEUE, REPLY_QUEUE ]

    def __init__(self, queue_name, handler, output_queue_name=None):
        logger.info(f"QueueWorker: init")

        self.queue_name = queue_name
        self.output_queue_name = output_queue_name
        self.handler = handler
        self.config = Config().values()

    async def run(self):
        q_url = f"amqp://{self.config['rabbitmq']['username']}:{self.config['rabbitmq']['password']}@{self.config['rabbitmq']['host']}"
        logger.info(f'Connecting to {q_url}.')
        connection = await aio_pika.connect_robust(q_url)

        async with connection:
            # Creating channel
            logger.info(f"QueueWorker: init")

            channel = await connection.channel()

            # Will take no more than 10 messages in advance
            await channel.set_qos(prefetch_count=10)

            # Declaring queues
            logger.info(f"Creating input queue {self.queue_name}")
            input_queue = await channel.declare_queue(self.queue_name, auto_delete=True)
            output_queue = None
            if self.output_queue_name:
                logger.info(f"Creating output queue {self.output_queue_name}")
                output_queue = await channel.declare_queue(self.output_queue_name, auto_delete=True)

            async with input_queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        logger.info(f"Invoking handler.")
                        await self.handler(message, output_queue)
