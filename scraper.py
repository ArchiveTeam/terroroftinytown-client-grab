import random
import itertools
import logging
import sys
import time
import traceback

from terroroftinytown.client.scraper import Scraper
from terroroftinytown.client.tracker import TrackerClient, TrackerError


def main():
    logging.basicConfig(level=logging.INFO)

    tracker_host = sys.argv[1]
    client_version = sys.argv[2]
    username = sys.argv[3]
    bind_address = sys.argv[4]
    user_agent = sys.argv[5]
    scheme = sys.argv[6]

    tracker_client = TrackerClient(
        tracker_host,
        username,
        version=client_version,
        bind_address=bind_address,
        user_agent=user_agent,
        scheme=scheme,
    )

    print('Getting item from tracker.')
    sys.stdout.flush()

    item_info = try_with_tracker(tracker_client.get_item)

    todo_list = range(item_info['lower_sequence_num'],
                      item_info['upper_sequence_num'] + 1)

    scraper_client = Scraper(
        item_info['project'], todo_list
    )

    try:
        result = scraper_client.run()
    except Exception:
        try_with_tracker(tracker_client.report_error,
                         item_info['id'],
                         item_info['tamper_key'],
                         str(traceback.format_exc())
                         )
        raise

    try_with_tracker(tracker_client.upload_item,
                     item_info['id'],
                     item_info['tamper_key'],
                     result)


def try_with_tracker(func, *args, **kwargs):
    for try_count in itertools.count(1):
        try:
            return func(*args, **kwargs)
        except TrackerError as error:
            sleep_time = 10 * try_count
            sleep_time += random.randint(0, 90)

            print('Error communicating with tracker: {0}.'.format(error))
            print('Trying again in {0} seconds.'.format(sleep_time))
            sys.stdout.flush()

            time.sleep(sleep_time)

            if try_count > 5:
                raise


if __name__ == '__main__':
    main()
