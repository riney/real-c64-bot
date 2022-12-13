import json, pprint, sys, time, traceback
from bs4 import BeautifulSoup, NavigableString
from mastodon import CallbackStreamListener, Mastodon
from realc64bot.config import Config
from realc64bot.connectors.work_queue import WorkQueue

mastodon = None
work_queue = None

def handle_notification(notification):
    print("mastodon_listener: handle_notification: got an notification!")
    type = notification['type']
    print(f"type = {type}")
    if type == 'mention':
        id = notification['status']['id']
        content = notification['status']['content']
        toot = strip_toot(content)
        print(f'mastodon_listener: handle_notification: got status {id} with type "{type}" and toot "{toot}"')
        message = {
            "message_id": id,
            "message_source": "mastodon",
            "content": toot,
        }
        #work_queue.enqueue(message)

def strip_toot(content):
    soup = BeautifulSoup(content, 'lxml')
    navstrs = [x for x in soup.html.body.p.contents if isinstance(x, NavigableString)]

    return navstrs[0].strip() or ""

def main():
    config = Config().values()

    try:
        print("mastodon_listener: connecting to work queue")
        work_queue = WorkQueue(
            config['rabbitmq']['host'],
            config['rabbitmq']['username'],
            config['rabbitmq']['password'])

        print("mastodon_listener: connecting to mastodon")
        secret = config['mastodon']['secrets']
        mastodon = Mastodon(access_token = secret)
        print("mastodon_listener: setting version")
        v = mastodon.retrieve_mastodon_version()
        print(f"mastodon_listener: got version #{v}")
        listener = CallbackStreamListener(notification_handler = handle_notification)

        print("mastodon_listener: starting notification stream...")
        stream = mastodon.stream_user(listener,
            run_async = True,
            reconnect_async = True,
        )

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("mastodon_listener: Shutdown requested... closing Mastodon stream")
        stream.close()
        print("mastodon_listener: Closing work queue")
        work_queue.close()
        print("mastodon_listener: exiting")
    except Exception:
        print("mastodon_listener: exception")

        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == "__main__":
    print("mastodon_listener: in startup")
    main()
