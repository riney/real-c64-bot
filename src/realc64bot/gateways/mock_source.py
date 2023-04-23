import asyncio
import json
import logging 
import random
import sys
import aio_pika
from realc64bot.config import Config
from realc64bot.workers.queue_worker import QueueWorker

logger = logging.getLogger('mock_source')
logging.basicConfig(level=logging.INFO)

async def mock_notification(id, content, channel) -> None:
        message = {
            "message_id": id,
            "message_source": "mock",
            "content": content,
        }

        print(f"mock_source: mock_notification: enqueuing message {message}")

        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message, indent=2).encode()),
            routing_key=QueueWorker.MESSAGES_QUEUE,
        )

async def main() -> None:
    config = Config().values()
    random.seed()

    q_url = f"amqp://{config['rabbitmq']['username']}:{config['rabbitmq']['password']}@{config['rabbitmq']['host']}"
    logger.info(f'Connecting to {q_url}.')
    connection = await aio_pika.connect_robust(q_url)

    async with connection:
        channel = await connection.channel()

        await mock_notification(random.randint(1,100000), '10 PRINT "HELLO MOCK"', channel)

if __name__ == "__main__":
    print("mock_source: in startup")

    asyncio.run(main())
