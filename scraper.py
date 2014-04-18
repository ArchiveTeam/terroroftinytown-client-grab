import itertools
import sys
import time

from terroroftinytown.client.scraper import Scraper
from terroroftinytown.client.tracker import TrackerClient, TrackerError


def main():
    tracker_host = sys.argv[1]
    client_version = sys.argv[2]
    username = sys.argv[3]
    bind_address = sys.argv[4]

    tracker_client = TrackerClient(
        tracker_host,
        username,
        client_version=client_version,
        bind_address=bind_address
    )

    item_info = try_with_tracker(tracker_client.get_item)

    scraper_client = Scraper(
        item_info['shortener_params'], item_info['todo_list']
    )

    result = scraper_client.run()

    try_with_tracker(tracker_client.upload_item, result)


def try_with_tracker(func, *args, **kwargs):
    for try_count in itertools.count():
        try:
            return func(*args, **kwargs)
        except TrackerError:
            # TODO: logging
            time.sleep(60 * try_count)

            if try_count > 10:
                raise


if __name__ == '__main__':
    main()
