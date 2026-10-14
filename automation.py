
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

from database import create_database, save_prices
from scraper import BASE_URL, scrape_prices
from export_report import export_price_report

PROJECT_DIR = Path(__file__).parent
LOG_DIR = PROJECT_DIR / "logs"
LOG_FILE = LOG_DIR / "pricewatch.log"

LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)


def run_pricewatch():
    """Run the complete PriceWatch collection workflow."""
    start_time = datetime.now(timezone.utc)
    logging.info("PriceWatch automation started.")

    try:
        create_database()

        products = scrape_prices(BASE_URL)

        if not products:
            logging.error(
                "No products were collected. The CSV report was not updated."
            )
            return False

        save_prices(products)
        export_price_report()

        elapsed = datetime.now(timezone.utc) - start_time
        logging.info(
            "PriceWatch finished successfully. "
            "Collected %d products in %.2f seconds.",
            len(products),
            elapsed.total_seconds(),
        )
        return True

    except Exception:
        logging.exception("PriceWatch automation failed.")
        return False


if __name__ == "__main__":
    success = run_pricewatch()
    sys.exit(0 if success else 1)