import asyncio
import json
import logging
from realc64bot.workers.queue_worker import QueueWorker

logger = logging.getLogger('message_worker')
logging.basicConfig(level=logging.INFO)

async def handle(message, output_queue) -> None:
    logger.info('Parsing inbound json')
    parsed_message = json.loads(message.body)
    logger.info(f"Handler handling message {parsed_message['content']}")

async def main() -> None:
    logger.info('Starting up.')
    worker = QueueWorker(
        queue_name=QueueWorker.MESSAGES_QUEUE,
        handler=handle,
        output_queue_name=QueueWorker.RUN_AND_CAPTURE_QUEUE
    )

    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
