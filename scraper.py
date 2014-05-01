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
        version=client_version,
        bind_address=bind_address
    )

    print('Getting item from tracker.')
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
        except TrackerError as error:
            sleep_time = 60 * try_count
            print('Error communicating with tracker: {0}.'.format(error))
            print('Trying again in {0} seconds.'.format(sleep_time))
            time.sleep(sleep_time)

            if try_count > 10:
                raise


if __name__ == '__main__':
    main()
