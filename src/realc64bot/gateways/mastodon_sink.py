import asyncio,logging, sys, time, traceback
from aio_pika import connect, Message
from bs4 import BeautifulSoup, NavigableString
from mastodon import CallbackStreamListener, Mastodon
from realc64bot.config import Config
from realc64bot.connectors.work_queue import WorkQueue

mastodon = None
q = None 

def handle_message(message):
    print("mastodon_sink: handle_message: got a message!")

async def main() -> None:
    config = Config().values()

    try:
        #print("mastodon_sink: connecting to mastodon")
        secret = config['mastodon']['secrets']
        global mastodon
        #mastodon = Mastodon(access_token = secret)        
        #print("mastodon_sink: setting version")
        #v = mastodon.retrieve_mastodon_version()
        #print(f"mastodon_sink: got version #{v}")
 
        q_url = f"amqp://{config['rabbitmq']['username']}:{config['rabbitmq']['password']}@{config['rabbitmq']['host']}"
        print(f"mastodon_sink: connecting to work queue at {q_url}")
        connection = await connect(q_url)
        
        async with connection:
            channel = await connection.channel()
            
            global q
            q = await channel.declare_queue(WorkQueue.REPLY_QUEUE)

            await q.consume(handle_message, no_ack=True)

            print("mastodon_sink: awaiting the future...")
            await asyncio.Future()
        
    except asyncio.exceptions.CancelledError:
        print("mastodon_sink: shutdown requested")
        print(f"At this point, channel is {channel}")
    except Exception:
        print("mastodon_sink: exception")

        traceback.print_exc(file=sys.stdout)

    print("mastodon_sink: exiting")
    sys.exit(0)

if __name__ == "__main__":
    print("mastodon_sink: in startup")
    asyncio.run(main())

