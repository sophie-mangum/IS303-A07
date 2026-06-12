"""
Book Market Analysis Pipeline

Inputs:
    BooksToScrape website pages

Processes:
    Scrape book data from multiple pages
    Store data in SQLite using Peewee ORM
    Query and analyze data with Pandas
    Create visualization with matplotlib

Outputs:
    Printed analysis
    books.db
    book_chart.png
"""

import requests
from bs4 import BeautifulSoup
from peewee import *
import pandas as pd
import matplotlib.pyplot as plt
import time

# -------------------------
# DATABASE SETUP
# -------------------------

db = SqliteDatabase("books.db")


class Book(Model):
    title = CharField(unique=True)
    price = FloatField()
    rating = IntegerField()

    class Meta:
        database = db


# -------------------------
# FETCH PAGE
# -------------------------

def fetch_page(url):
    """Fetch a webpage and return BeautifulSoup object."""

    response = requests.get(url)

    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")

    print(f"Failed to fetch {url}")
    return None


# -------------------------
# SCRAPE BOOKS
# -------------------------

def scrape_books():
    """Scrape book data from first 3 pages."""

    books = []

    for page in range(1, 4):

        url = f"https://books.toscrape.com/catalogue/page-{page}.html"

        soup = fetch_page(url)

        if soup is None:
            continue

        articles = soup.find_all("article", class_="product_pod")

        for article in articles:

            title = article.h3.a["title"]

            price_text = article.find("p", class_="price_color").text
            price = float(price_text.replace("£", "").replace("Â", ""))

            rating_text = article.find("p")["class"][1]

            rating_dict = {
                "One": 1,
                "Two": 2,
                "Three": 3,
                "Four": 4,
                "Five": 5
            }

            rating = rating_dict.get(rating_text, 0)

            books.append({
                "title": title,
                "price": price,
                "rating": rating
            })

        # Required rate limiting
        time.sleep(1)

    return books


# -------------------------
# STORE BOOKS
# -------------------------

def store_books(book_list):
    """Store books in SQLite database."""

    for book in book_list:

        exists = Book.select().where(
            Book.title == book["title"]
        ).exists()

        if not exists:

            Book.create(
                title=book["title"],
                price=book["price"],
                rating=book["rating"]
            )


# -------------------------
# ANALYZE DATA
# -------------------------

def analyze_books():
    """Analyze stored book data using Pandas."""

    records = []

    for book in Book.select():

        records.append({
            "title": book.title,
            "price": book.price,
            "rating": book.rating
        })

    df = pd.DataFrame(records)

    avg_price_by_rating = (
        df.groupby("rating")["price"]
        .mean()
        .round(2)
    )

    print("\n----- ANALYSIS RESULTS -----")

    print(f"Total books collected: {len(df)}")

    print(f"Average price: ${df['price'].mean():.2f}")

    print(f"Highest price: ${df['price'].max():.2f}")

    print(f"Lowest price: ${df['price'].min():.2f}")

    print("\nAverage Price by Rating:")
    print(avg_price_by_rating)

    return df, avg_price_by_rating


# -------------------------
# VISUALIZATION
# -------------------------

def visualize(avg_price_by_rating):
    """Create and save chart."""

    avg_price_by_rating.plot(kind="bar")

    plt.title("Average Book Price by Rating")
    plt.xlabel("Book Rating")
    plt.ylabel("Average Price (£)")

    plt.tight_layout()

    plt.savefig("book_chart.png")

    print("\nChart saved as book_chart.png")


# -------------------------
# MAIN
# -------------------------

def main():

    db.connect()

    db.create_tables([Book])

    books = scrape_books()

    store_books(books)

    df, avg_price_by_rating = analyze_books()

    visualize(avg_price_by_rating)

    db.close()


if __name__ == "__main__":
    main()