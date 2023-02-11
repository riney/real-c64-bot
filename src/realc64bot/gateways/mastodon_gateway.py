import logging, sys, time, traceback
from bs4 import BeautifulSoup, NavigableString
from mastodon import CallbackStreamListener, Mastodon
from realc64bot.config import Config
from realc64bot.connectors.work_queue import WorkQueue

mastodon = None
q = None

def handle_notification(notification):
    print("mastodon_gateway: handle_notification: got an notification!")
    type = notification['type']
    if type == 'mention':
        id = notification['status']['id']
        content = notification['status']['content']
        toot = strip_toot(content)
        print(f'mastodon_gateway: handle_notification: got status {id} with type "{type}" and toot "{toot}"')
        message = {
            "message_id": id,
            "message_source": "mastodon",
            "content": toot,
        }

        print(f"mastodon_gateway: handle_notification: queue channel open? {q.channel.is_open}")
        print(f"mastodon_gateway: handle_notification: enqueuing message {message}")
        q.enqueue(message, WorkQueue.MESSAGES_QUEUE)

def strip_toot(content):
    soup = BeautifulSoup(content, 'lxml')
    navstrs = [x for x in soup.html.body.p.contents if isinstance(x, NavigableString)]

    return navstrs[0].strip() or ""

def main():
    config = Config().values()

    try:
        print("mastodon_gateway: connecting to work queue")
        global q
        q = WorkQueue(
            config['rabbitmq']['host'],
            config['rabbitmq']['username'],
            config['rabbitmq']['password'])

        print("mastodon_gateway: connecting to mastodon")
        secret = config['mastodon']['secrets']
        global mastodon
        mastodon = Mastodon(access_token = secret)
        
        print("mastodon_gateway: setting version")
        v = mastodon.retrieve_mastodon_version()
        print(f"mastodon_gateway: got version #{v}")
        listener = CallbackStreamListener(notification_handler = handle_notification)

        print("mastodon_gateway: starting notification stream...")
        stream = mastodon.stream_user(listener,
            run_async = True,
            reconnect_async = True,
        )

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("mastodon_gateway: Shutdown requested... closing Mastodon stream")
        stream.close()
        print("mastodon_gateway: Closing work queue")
        q.close()
        print("mastodon_gateway: exiting")
    except Exception:
        print("mastodon_gateway: exception")

        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == "__main__":
    print("mastodon_gateway: in startup")
    main()
