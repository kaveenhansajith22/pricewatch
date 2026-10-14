
import logging
import time
from decimal import Decimal, InvalidOperation

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-1.html"

MAX_RETRIES = 3
RETRY_DELAY = 2


def parse_price(raw_price):
    """Convert a price string into a Decimal value."""
    cleaned_price = "".join(
        character
        for character in raw_price
        if character.isdigit() or character == "."
    )

    try:
        return Decimal(cleaned_price)
    except InvalidOperation:
        logging.warning("Could not parse price: %s", raw_price)
        return None


def scrape_prices(url):
    """Scrape product names and prices, retrying temporary failures."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(
                url,
                timeout=20,
                headers={
                    "User-Agent": "PriceWatch-Portfolio/1.0"
                },
            )
            response.raise_for_status()
            break

        except requests.RequestException as error:
            logging.warning(
                "Request attempt %d/%d failed: %s",
                attempt,
                MAX_RETRIES,
                error,
            )

            if attempt == MAX_RETRIES:
                logging.error(
                    "All retry attempts failed. No products collected."
                )
                return []

            logging.info("Retrying in %d seconds...", RETRY_DELAY)
            time.sleep(RETRY_DELAY)

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.select("article.product_pod"):
        title_element = item.select_one("h3 a")
        price_element = item.select_one(".price_color")

        if title_element is None or price_element is None:
            continue

        name = title_element.get("title", "").strip()
        price = parse_price(price_element.get_text(strip=True))

        if not name or price is None:
            continue

        products.append({
            "name": name,
            "price": str(price),
            "currency": "GBP",
        })

    logging.info("Successfully extracted %d products", len(products))
    return products


if __name__ == "__main__":
    from database import create_database, save_prices

    create_database()
    products = scrape_prices(BASE_URL)

    if products:
        save_prices(products)

        for product in products[:5]:
            print(product)