import json, pprint, sys, time, traceback
from mastodon import CallbackStreamListener, Mastodon
from work_queue import WorkQueue

HASHTAG = "realc64bot"

mastodon = None
work_queue = None

def handle_update(status):
    print("mastodon_listener: got an update!")
    id = status['id']
    content = status['content']
    print("mastodon_listener: #{id} #{status}")
    message = {
        "message_id": id,
        "message_source": "mastodon",
        "content": content,
    }
    work_queue.enqueue(message)

def handle_unknown(name, unknown_event):
    print(f"mastodon_listener: got an unknown event #{name}")

def main():
    try:
        print("mastodon_listener: connecting to work queue")
        work_queue = WorkQueue('rabbit.local', 'user', 'pass')
        print("mastodon_listener: connecting to mastodon")
        mastodon = Mastodon(client_id = 'mastodon_test.secret')
        print("mastodon_listener: setting version")
        v = mastodon.retrieve_mastodon_version()
        print(f"mastodon_listener: got version #{v}")
        listener = CallbackStreamListener(
            update_handler = handle_update,
            unknown_event_handler = handle_unknown)
        print("mastodon_listener: starting hashtag stream...")
        
        stream = mastodon.stream_hashtag(HASHTAG,
            listener,
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
