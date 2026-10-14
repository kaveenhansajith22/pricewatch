
from database import get_price_history


def compare_prices():
    """Compare the latest two recorded prices for each product."""
    records = get_price_history()

    if not records:
        print("No price records found. Run scraper.py first.")
        return

    # Group records by product name.
    products = {}

    for record in records:
        name = record["product_name"]
        products.setdefault(name, []).append(record)

    print("\nPRICEWATCH - PRICE COMPARISON")
    print("=" * 75)

    for name, history in sorted(products.items()):
        # Records are returned newest first by get_price_history().
        latest = history[0]
        previous = history[1] if len(history) > 1 else None

        if previous is None:
            print(f"\nProduct: {name}")
            print(f"Latest price: {latest['currency']} {latest['price']}")
            print("Previous price: Not available")
            print("Change: Not enough history")
            continue

        latest_price = float(latest["price"])
        previous_price = float(previous["price"])
        change = latest_price - previous_price

        if change > 0:
            status = "PRICE INCREASED"
        elif change < 0:
            status = "PRICE DECREASED"
        else:
            status = "NO CHANGE"

        print(f"\nProduct: {name}")
        print(f"Previous price: {previous['currency']} {previous_price:.2f}")
        print(f"Latest price:   {latest['currency']} {latest_price:.2f}")
        print(f"Price change:   {change:+.2f}")
        print(f"Status:         {status}")

    print("\n" + "=" * 75)


if __name__ == "__main__":
    compare_prices()