import json, pprint, sys, time, traceback
from mastodon import CallbackStreamListener, Mastodon
from realc64bot.config import Config
from realc64bot.connectors.work_queue import WorkQueue

mastodon = None
work_queue = None

def handle_notification(notification):
    print("mastodon_listener: handle_notification: got an notification!")
    id = notification['id']
    content = notification['content']
    print("mastodon_listener: handle_notification: #{id} #{status}")
    message = {
        "message_id": id,
        "message_source": "mastodon",
        "content": content,
    }
    #work_queue.enqueue(message)

def handle_unknown(name, unknown_event):
    print(f"mastodon_listener: got an unknown event #{name}")

def handle_update(status):
    print(f"mastodon_listener: got an update #{status}")

def handle_local_update(status):
    print(f"mastodon_listener: got a local update #{status}")

def handle_conversation(conversation):
    print(f"mastodon_listener: got a conversation #{conversation}")

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
        mastodon = Mastodon(client_id = secret)
        print("mastodon_listener: setting version")
        v = mastodon.retrieve_mastodon_version()
        print(f"mastodon_listener: got version #{v}")
        listener = CallbackStreamListener(
            notification_handler = handle_notification,
            conversation_handler = handle_conversation,
            update_handler = handle_update,
            local_update_handler = handle_local_update,
            unknown_event_handler = handle_unknown)

        print("mastodon_listener: starting notification stream...")
        
        stream = mastodon.stream_user(listener,
            run_async = True,
            reconnect_async = True,
        )

        while True:
            time.sleep(1)
            print(f"Stream healthy? {mastodon.stream_healthy()}")

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
