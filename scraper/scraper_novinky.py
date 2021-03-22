from datetime import datetime
import json
import mechanicalsoup

from scraper.database.base_objects import Article
from scraper.database.db_utils import save_to_db

BASE_URL = "https://novinky.cz/stalo-se"


def retrieve_paragraphs(page) -> str:
    paragraphs = page.select('div[data-dot-data=\'{"component":"article-content"}\'] p')

    text = ""
    for paragraph in paragraphs:
        text += paragraph.text + "\n"
    return text


def retrieve_authors(page) -> []:
    authors_select = page.select('div[class="g_gz"] a[class="d_aZ"]')

    authors = []
    for link in authors_select:
        authors.append(link.text)

    return authors


def find_category(first_script_data) -> str:
    item_list_element = first_script_data["itemListElement"]
    for list_element in item_list_element:
        if list_element["position"] == 2:
            return list_element["name"]


def extract_article(browser: mechanicalsoup.StatefulBrowser, url: str) -> (Article, []):
    browser.open(url)
    page = browser.get_current_page()

    script_data = page.select('script[type="application/ld+json"]')
    first_script_data = json.loads(script_data[1].text)
    second_script_data = json.loads(script_data[0].text)

    header = second_script_data["headline"]
    description = second_script_data["description"]
    category = find_category(first_script_data)
    published_at = datetime.strptime(second_script_data["datePublished"], '%Y-%m-%dT%H:%M:%S.%fZ')
    modified_at = datetime.strptime(second_script_data["dateModified"], '%Y-%m-%dT%H:%M:%S.%fZ')
    authors = retrieve_authors(page)
    paragraphs = retrieve_paragraphs(page)

    article = Article(link=url, header=header, description=description, category=category, published_at=published_at,
                   modified_at=modified_at, paragraphs=paragraphs)
    return article, authors


if __name__ == '__main__':
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(BASE_URL)

    page = browser.get_current_page()

    # we will crawl these sites
    articles = []
    stalo_se_articles = page.select('div[data-dot="stalo_se"] a')
    for article in stalo_se_articles:
        # skip not article
        if 'lastItem' in article['href']:
            continue

        articles.append(extract_article(browser, article['href']))

    save_to_db(articles)









