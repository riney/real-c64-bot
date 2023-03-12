import asyncio, json, logging, sys, time, traceback
import aio_pika
from bs4 import BeautifulSoup, NavigableString
from mastodon import CallbackStreamListener, Mastodon
from realc64bot.config import Config
from realc64bot.connectors.work_queue import WorkQueue

mastodon = None
channel = None

logger = logging.getLogger('mastodon_source')
logging.basicConfig(level=logging.INFO)

def handle_notification(notification):
    logger.info("handle_notification: got an notification!")
    type = notification['type']
    if type == 'mention':
        id = notification['status']['id']
        content = notification['status']['content']
        toot = strip_toot(content)

        logger.info(f'mastodon_source: handle_notification: got status {id} with type "{type}" and toot "{toot}"')
        message = {
            "message_id": id,
            "message_source": "mastodon",
            "content": toot,
        }

        logger.info(f"handle_notification: enqueuing message {message}")
        loop.create_task(enqueue(message))

def strip_toot(content):
    soup = BeautifulSoup(content, 'lxml')
    navstrs = [x for x in soup.html.body.p.contents if isinstance(x, NavigableString)]

    return navstrs[0].strip() or ""

async def enqueue(message) -> None:
    logger.info("publishing message")
    await channel.default_exchange.publish(
        aio_pika.Message(body=bytes(json.dumps(message), encoding='utf8')),
        routing_key=WorkQueue.MESSAGES_QUEUE,
    )

async def main() -> None:
    config = Config().values()

    try:
        logger.info("connecting to work queue")
        connection = await aio_pika.connect_robust(f"amqp://{config['rabbitmq']['username']}:{config['rabbitmq']['password']}@{config['rabbitmq']['host']}")
        global channel
        channel = await connection.channel()
        await channel.declare_queue(WorkQueue.MESSAGES_QUEUE)        
        
        logger.info("connecting to mastodon")
        global mastodon
        mastodon = Mastodon(
            client_id=config['mastodon']['client_id'],
            access_token=config['mastodon']['access_token'])
       
        logger.info("setting version")
        v = mastodon.retrieve_mastodon_version()
        logger.info(f"got version #{v}")
        listener = CallbackStreamListener(notification_handler = handle_notification)

        logger.info("starting notification stream...")
        global stream
        stream = mastodon.stream_user(listener,
            run_async = True,
            reconnect_async = True,
        )

        global loop
        loop = asyncio.get_running_loop()

        logger.info("awaiting the future...")
        await asyncio.Future()
        
    except Exception:
        logger.info("exception")

        traceback.logger.info_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == "__main__":
    logger.info("in startup")
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.info("Shutdown requested... closing Mastodon stream")
        stream.close()
        logger.info("exiting")
