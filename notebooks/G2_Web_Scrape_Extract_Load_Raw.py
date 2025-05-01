import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}
base_url = "https://books.toscrape.com/catalogue/page-{}.html"

for page in range(1, 51):  # Loop through all 50 pages
    url = base_url.format(page)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        availability = book.find("p", class_="instock availability").text.strip()
        rating = book.p["class"][-1]  # "One", "Two", "Three", etc.

        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Availability: {availability}")
        print(f"Rating: {rating}")
        print("-" * 40)
        
