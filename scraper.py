
import logging
from decimal import Decimal, InvalidOperation

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-1.html"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def scrape_prices(url):
    """Fetch product names and prices from a practice product listing."""
    try:
        response = requests.get(
            url,
            timeout=20,
            headers={"User-Agent": "PriceWatch-Portfolio/1.0"},
        )
        response.raise_for_status()

    except requests.RequestException as error:
        logging.error("Could not fetch the page: %s", error)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.select("article.product_pod"):
        title_element = item.select_one("h3 a")
        price_element = item.select_one(".price_color")

        if title_element is None or price_element is None:
            logging.warning("Skipping a product with missing fields")
            continue

        name = title_element.get("title", "").strip()
        raw_price = price_element.get_text(strip=True)

        try:
            price = Decimal(raw_price.replace("£", "").strip())
        except InvalidOperation:
            logging.warning("Invalid price for product: %s", name)
            continue

        if not name or price < 0:
            logging.warning("Invalid product data; skipping")
            continue

        products.append({
            "name": name,
            "price": str(price),
            "currency": "GBP",
        })

    logging.info("Successfully extracted %d products", len(products))
    return products


if __name__ == "__main__":
    results = scrape_prices(BASE_URL)

    for product in results[:5]:
        print(product)

    print(f"\nProducts extracted: {len(results)}")