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

    # Check one by one
    for article in articles:

        book_link = article.find('div', {'class': 'image_container'}).select("a")[0].attrs['href']

        book_url = base_url + f'/catalogue/{book_link}'

        book_request = requests.get(book_url)
        book_content = book_request.content

        book_soup = BeautifulSoup(book_content, "html.parser")

        title = book_soup.select("div.col-sm-6.product_main h1")[0].text.strip() 
        price = book_soup.select("div.col-sm-6.product_main p.price_color")[0].text.strip()
        price = re.sub("(€|£)", "", price) # Clean price from currency symbols

        stock = book_soup.select("div.col-sm-6.product_main p.instock.availability")[0].text.strip()
        stock = re.sub("([\(\)a-zA-Z\s])", "", stock)
        category = book_soup.find("ul", {'class': 'breadcrumb'}).find_all("li")[2].text.strip()
        cover = base_url + "/".join(book_soup.select("div.item.active img")[0].attrs['src'].split("/")[2:])
        table_th = book_soup.find("table", {'class': 'table table-striped'}).find_all("th")
        table_td = book_soup.find("table", {'class': 'table table-striped'}).find_all("td")
                 
        book_data = {}
        book_data['title'] = title
        book_data['price'] = price
        book_data['stock'] = stock
        book_data['category'] = category
        book_data['cover'] = cover
        book_data['title'] = title

        # To check table data
        for header, content in zip(table_th, table_td):
            clean_key = re.sub("([\s\.\(\)])","_", header.text.strip().lower())
            book_data[clean_key] = re.sub("(€|£)", "", content.text.strip())

        web_content_list.append(book_data)
        print(f"Book {n} added...")
        n += 1

df = pandas.DataFrame(web_content_list)
df.to_csv("scrapper_books.csv")


# These functions are for modularize and clean this solution

def get_site_paging():
  pass

def page_content():

  pass

def get_book_details():
  pass