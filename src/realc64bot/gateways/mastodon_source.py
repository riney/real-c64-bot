import asyncio, json, logging, sys, time, traceback
import aio_pika
from bs4 import BeautifulSoup, NavigableString
from mastodon import CallbackStreamListener, Mastodon
from realc64bot.config import Config
from realc64bot.connectors.work_queue import WorkQueue

mastodon = None
channel = None

def handle_notification(notification):
    print("mastodon_source: handle_notification: got an notification!")
    type = notification['type']
    if type == 'mention':
        id = notification['status']['id']
        content = notification['status']['content']
        toot = strip_toot(content)

        print(f'mastodon_source: handle_notification: got status {id} with type "{type}" and toot "{toot}"')
        message = {
            "message_id": id,
            "message_source": "mastodon",
            "content": toot,
        }

        print(f"mastodon_source: handle_notification: enqueuing message {message}")
        loop.create_task(enqueue(message))

def strip_toot(content):
    soup = BeautifulSoup(content, 'lxml')
    navstrs = [x for x in soup.html.body.p.contents if isinstance(x, NavigableString)]

    return navstrs[0].strip() or ""

async def enqueue(message) -> None:
    print("mastodon_source: publishing message")
    await channel.default_exchange.publish(
        aio_pika.Message(body=bytes(json.dumps(message), encoding='utf8')),
        routing_key=WorkQueue.MESSAGES_QUEUE,
    )

async def main() -> None:
    config = Config().values()

    try:
        print("mastodon_source: connecting to work queue")
        connection = await aio_pika.connect_robust(f"amqp://{config['rabbitmq']['username']}:{config['rabbitmq']['password']}@{config['rabbitmq']['host']}")
        global channel
        channel = await connection.channel()
        
        print("mastodon_source: connecting to mastodon")
        global mastodon
        mastodon = Mastodon(
            client_id=config['mastodon']['client_id'],
            access_token=config['mastodon']['access_token'])
       
        print("mastodon_source: setting version")
        v = mastodon.retrieve_mastodon_version()
        print(f"mastodon_source: got version #{v}")
        listener = CallbackStreamListener(notification_handler = handle_notification)

        print("mastodon_source: starting notification stream...")
        global stream
        stream = mastodon.stream_user(listener,
            run_async = True,
            reconnect_async = True,
        )

        global loop
        loop = asyncio.get_running_loop()

        print("mastodon_source: awaiting the future...")
        await asyncio.Future()
        
    except Exception:
        print("mastodon_source: exception")

        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == "__main__":
    print("mastodon_source: in startup")
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("mastodon_source: Shutdown requested... closing Mastodon stream")
        stream.close()
        print("mastodon_source: exiting")
