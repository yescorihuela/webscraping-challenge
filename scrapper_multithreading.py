# STL
import re
import logging as log
import os
import time
import concurrent.futures

# third-party libs
import requests
import pandas
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/"

BOOK_DATA_QUEUE = []
PAGES_URL_QUEUE = []
ARTICLES_PER_PAGE_QUEUE = []


def get_site_first_and_last_page():
    request_to_base_url = requests.get(BASE_URL)
    content_base_url = request_to_base_url.content
    page_soup = BeautifulSoup(content_base_url, "html.parser")

    paging = page_soup.select('li[class="current"]')[0].text.strip().split(" ")[1:4:2]
    start_page, last_page = int(paging[0]), int(paging[1])
    return start_page, last_page


# Linear urls construction
def get_pages_url(start_page, last_page):
    for page_number in range(start_page, last_page + 1):
        page_url = "".join([BASE_URL, f'/catalogue/page-{page_number}.html'])
        log.info("Page %d added", page_number)
        PAGES_URL_QUEUE.append((page_url, page_number))


# Get all articles from one page
def get_page_content(page_tuple):
    page_url, page_number = page_tuple
    page_request = requests.get(page_url)
    page_content = page_request.content
    page_soup = BeautifulSoup(page_content, "html.parser")
    articles_list = page_soup.find_all("article", {"class": "product_pod"})
    log.info("Scrapping content from page %d", page_number)
    ARTICLES_PER_PAGE_QUEUE.append(articles_list)


# Call threads executor
def get_detail_article_content(articles_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(process_article_content, articles_list)


# Processing the detail from each book
def process_article_content(article_list):
    book_link = article_list.find('div', {'class': 'image_container'}).select("a")[0].attrs['href']

    book_url = "".join([BASE_URL, f'/catalogue/{book_link}'])

    book_request = requests.get(book_url)
    book_content = book_request.content

    book_soup = BeautifulSoup(book_content, "html.parser")

    title = book_soup.select("div.col-sm-6.product_main h1")[0].text.strip()
    price = book_soup.select("div.col-sm-6.product_main p.price_color")[0].text.strip()
    price = re.sub("(€|£)", "", price)  # Clean price from currency symbols

    stock = book_soup.select("div.col-sm-6.product_main p.instock.availability")[0].text.strip()
    stock = re.sub("([\(\)a-zA-Z\s])", "", stock)
    category = book_soup.find("ul", {'class': 'breadcrumb'}).find_all("li")[2].text.strip()
    cover = BASE_URL + "/".join(book_soup.select("div.item.active img")[0].attrs['src'].split("/")[2:])
    table_th = book_soup.find("table", {'class': 'table table-striped'}).find_all("th")
    table_td = book_soup.find("table", {'class': 'table table-striped'}).find_all("td")

    book_data = {'title': title, 'price': price, 'stock': stock, 'category': category, 'cover': cover}

    for header, content in zip(table_th, table_td):
        clean_key = re.sub("([\s\.\(\)])", "_", header.text.strip().lower())
        book_data[clean_key] = re.sub("(€|£)", "", content.text.strip())

    BOOK_DATA_QUEUE.append(book_data)
    log.info("Book %s added...", title[:40])


def get_csv_file_output():
    df = pandas.DataFrame(BOOK_DATA_QUEUE)
    csv_file_output_name = 'scrapper_books.csv'
    filepath = "/".join([os.getcwd(), csv_file_output_name])

    try:
        df.to_csv(filepath)
        log.info("CSV File generated with filepath '%s'", filepath)
        del df
    except IOError as e: # If there's any problem writing the csv file
        raise e


def main():
    # We need measure the time which the scrapper takes
    start_time = time.time()
    log.info("Starting scrapping... ")
    start_page, last_page = get_site_first_and_last_page()

    # Fulls queue with built urls in O(n) process
    get_pages_url(start_page, last_page)

    # Processes all the page' content and stores each articles list in other queue
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(get_page_content, PAGES_URL_QUEUE)

    # Processes the articles list and article details
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(get_detail_article_content, ARTICLES_PER_PAGE_QUEUE)

    get_csv_file_output()
    total_duration = time.time() - start_time
    log.info("Total processing time: %d seconds", total_duration)


if __name__ == '__main__':
    fmt = "%(asctime)s: %(message)s"
    log.basicConfig(format=fmt, level=log.INFO, datefmt="%H:%M:%S")
    main()
