import mechanicalsoup

BASE_URL = "https://novinky.cz/stalo-se"


if __name__ == '__main__':
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(BASE_URL   )

    page = browser.get_current_page()

    stalo_se_articles = page.select('div[data-dot="stalo_se"] a')
    for article in stalo_se_articles:
        print(article['href'])



