import re
import requests
import pandas
from bs4 import BeautifulSoup

base_url = "http://books.toscrape.com/"

# To get the html contents
r = requests.get(base_url)
c = r.content

# To parse the html
soup = BeautifulSoup(c,"html.parser")

# To extract the first and last page numbers
paging = soup.select('li[class="current"]')[0].text.strip().split(" ")[1:4:2]
start_page = int(paging[0])
last_page = int(paging[1])
web_content_list = []
n = 1 # To get the number of each appended book

for page_number in range(start_page, last_page + 1):
    
    # To form and scrap with pagination
    url = base_url + f'/catalogue/page-{page_number}.html'
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    
    # To extract all the articles present in the current page
    articles = soup.find_all("article",{"class":"product_pod"})