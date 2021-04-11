import threading

from scraper.scraper_novinky import run

if __name__ == '__main__':
    # TODO -> also create graphql thread
    scraper_thread = threading.Thread(target=run)
    scraper_thread.start()
