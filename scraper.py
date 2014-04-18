import os.path
import sys

sys.path.append(
    os.path.join(os.path.dirname(__file__), 'terroroftinytown')
)

from terroroftinytown.client.tracker import TrackerClient
from terroroftinytown.client.scraper import Scraper


def main():
    tracker_host = sys.argv[1]
    client_version = sys.argv[2]
    username = sys.argv[3]
    bind_address = sys.argv[4]
    tracker_client = TrackerClient(tracker_host, client_version=client_version)
    item_info = tracker_client.get_item()
    scraper_client = Scraper(
        item_info['shortener_params'], item_info['todo_list']
    )
    scraper_client.run()


if __name__ == '__main__':
    main()
