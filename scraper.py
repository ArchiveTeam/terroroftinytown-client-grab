import os.path
import sys
from terroroftinytown.client.tracker import TrackerClient
from terroroftinytown.client.scraper import Scraper

sys.path.append(
    os.path.join(os.path.dirname(__file__), 'terroroftinytown')
)


def main():
    tracker_host = sys.argv[1]
    client_version = sys.argv[2]
    tracker_client = TrackerClient(tracker_host, client_version=client_version)
    item_info = tracker_client.get_item()
    scraper_client = Scraper(
        item_info['shortener_params'], item_info['todo_list']
    )
    scraper_client.run()


if __name__ == '__main__':
    pass
