import threading

from scraper.scraper_novinky import run as scraper_run
from graphql_backend.server import app

if __name__ == '__main__':
    # TODO -> also create graphql thread
    scraper_thread = threading.Thread(target=scraper_run)
    scraper_thread.start()
