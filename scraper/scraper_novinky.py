from datetime import datetime
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
import mechanicalsoup
from bs4 import BeautifulSoup
from tqdm import tqdm

from database.base_objects import Article, Comment
from scraper.db_utils import save_to_db

BASE_URL = "https://novinky.cz/stalo-se"


def extract_info_from_iframe(browser: webdriver, url: str) -> []:
    try:
        # open all other pages with comments
        button = browser.find_element_by_css_selector("button[data-dot='strankovani/nacist_dalsi']")
        while button:
            try:
                action = ActionChains(browser)
                action.move_to_element(button).click().perform()
            except (ElementClickInterceptedException, StaleElementReferenceException):
                pass
            sleep(0.5)
            button = browser.find_element_by_css_selector("button[data-dot='strankovani/nacist_dalsi']")
    except NoSuchElementException:
        pass

    try:
        # open threads of subcomments
        for button in browser.find_elements_by_css_selector("button[data-dot='nacist_nove_podkomentare']"):
            try:
                action = ActionChains(browser)
                action.move_to_element(button).click().perform()
            except (ElementClickInterceptedException, StaleElementReferenceException):
                pass
            sleep(0.3)
    except NoSuchElementException:
        pass

    # now we can use familiar beautiful soup
    soup = BeautifulSoup(browser.page_source, "html.parser")

    authors = soup.select("a[class='f_bO'] span")
    texts = soup.select("p[class='d_aJ']")
    reactions = soup.select("a[class='f_cQ']")

    comments = []
    progress_bar = tqdm(total=len(authors), desc="Comments", position=0)
    for i in range(len(authors)):
        author = authors[i].text
        text = texts[i].text

        # expect that reaction can miss in some comments
        reactions_count = 0
        if len(reactions) > i:
            reactions_count = reactions[i].text

        comments.append(Comment(author=author, text=text, reactions=reactions_count))
        progress_bar.update(1)

    return comments


def retrieve_comments(browser_, url: str) -> []:
    """
    This function needs selenium, because comments are generated by Javascript.
    :param url: URL to retrieve comments from
    :return: List of Comment objects
    """
    ChromeOptions = webdriver.ChromeOptions()
    ChromeOptions.add_argument('--headless')
    ChromeOptions.add_argument('--no-sandbox')
    ChromeOptions.add_argument('--disable-gpu')
    ChromeOptions.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options=ChromeOptions, executable_path='/snap/bin/chromium.chromedriver')
    #browser = webdriver.Chrome(options=ChromeOptions)
    browser.implicitly_wait(6)
    browser.get(url)

    # selenium browser will wait for up to 6 seconds for iframes to load
    _ = browser.find_element_by_tag_name("iframe")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    soup.select("iframe")
    for iframe in soup.select("iframe"):
        if "src" in iframe.attrs:
            if "diskuze.seznam.cz" in iframe["src"]:
                browser.get(iframe['src'])
                return extract_info_from_iframe(browser, iframe['src'])

    return []


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

    header = second_script_data["headline"].replace(u'\xa0', ' ')
    description = second_script_data["description"].replace(u'\xa0', ' ')
    category = find_category(first_script_data)
    published_at = datetime.strptime(second_script_data["datePublished"], '%Y-%m-%dT%H:%M:%S.%fZ')
    modified_at = datetime.strptime(second_script_data["dateModified"], '%Y-%m-%dT%H:%M:%S.%fZ')
    authors = retrieve_authors(page)
    paragraphs = retrieve_paragraphs(page)

    print(f"Currently working on article {header}")

    comments = retrieve_comments(browser, url.replace("clanek", "diskuze"))

    article = Article(link=url, header=header, description=description, category=category, published_at=published_at,
                   modified_at=modified_at, paragraphs=paragraphs)
    return article, authors, comments


def run():
    browser = mechanicalsoup.StatefulBrowser()

    while True:
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


if __name__ == '__main__':
    run()
