
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "pricewatch.db"


def create_database():
    """Create the database and price history table if needed."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                price TEXT NOT NULL,
                currency TEXT NOT NULL,
                collected_at TEXT NOT NULL
            )
        """)

    print("Database and price history table are ready.")


def save_prices(products):
    """Save scraped products with their collection timestamps."""
    if not products:
        print("No products to save.")
        return

    collected_at = datetime.now(timezone.utc).isoformat()

    rows = [
        (
            product["name"],
            product["price"],
            product["currency"],
            collected_at,
        )
        for product in products
    ]

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.executemany("""
            INSERT INTO price_history (
                product_name,
                price,
                currency,
                collected_at
            )
            VALUES (?, ?, ?, ?)
        """, rows)

    print(f"Saved {len(rows)} price records to the database.")


def get_price_history():
    """Return all saved price records."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row

        records = connection.execute("""
            SELECT
                id,
                product_name,
                price,
                currency,
                collected_at
            FROM price_history
            ORDER BY id DESC
        """).fetchall()

    return [dict(record) for record in records]


if __name__ == "__main__":
    create_database()