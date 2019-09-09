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


def main():
    pass


if __name__ == '__main__':
    fmt = "%(asctime)s: %(message)s"
    log.basicConfig(format=fmt, level=log.INFO, datefmt="%H:%M:%S")
    main()
