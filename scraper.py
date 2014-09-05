import itertools
import logging
import sys
import time

from terroroftinytown.client.scraper import Scraper
from terroroftinytown.client.tracker import TrackerClient, TrackerError


def main():
    logging.basicConfig(level=logging.INFO)

    tracker_host = sys.argv[1]
    client_version = sys.argv[2]
    username = sys.argv[3]
    bind_address = sys.argv[4]
    user_agent = sys.argv[5]

    tracker_client = TrackerClient(
        tracker_host,
        username,
        version=client_version,
        bind_address=bind_address,
        user_agent=user_agent,
    )

    print('Getting item from tracker.')
    item_info = try_with_tracker(tracker_client.get_item)

    todo_list = range(item_info['lower_sequence_num'],
                      item_info['upper_sequence_num'] + 1)

    scraper_client = Scraper(
        item_info['project'], todo_list
    )

    result = scraper_client.run()

    try_with_tracker(tracker_client.upload_item,
                     item_info['id'],
                     item_info['tamper_key'],
                     result)


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
