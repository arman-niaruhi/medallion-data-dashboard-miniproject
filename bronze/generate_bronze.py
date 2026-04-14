from pathlib import Path
import random
import pandas as pd

OUTPUT_DIR = Path("/data/bronze")
OUTPUT_FILE = OUTPUT_DIR / "sales_raw.csv"


def generate_synthetic_raw_csv(num_rows: int = 200, seed: int = 42) -> None:
    random.seed(seed)

    customers = [
        {"customer_id": "C001", "customer_name": "Alice", "city": "Berlin", "country": "Germany"},
        {"customer_id": "C002", "customer_name": "Bob", "city": "Paris", "country": "France"},
        {"customer_id": "C003", "customer_name": "Charlie", "city": "Madrid", "country": "Spain"},
        {"customer_id": "C004", "customer_name": "Diana", "city": "Rome", "country": "Italy"},
        {"customer_id": "C005", "customer_name": "Ethan", "city": "Amsterdam", "country": "Netherlands"},
    ]

    products = [
        {"product_id": "P001", "product_name": "Laptop", "category": "Electronics", "unit_price": 1200.0},
        {"product_id": "P002", "product_name": "Mouse", "category": "Accessories", "unit_price": 25.0},
        {"product_id": "P003", "product_name": "Keyboard", "category": "Accessories", "unit_price": 75.0},
        {"product_id": "P004", "product_name": "Monitor", "category": "Electronics", "unit_price": 300.0},
        {"product_id": "P005", "product_name": "Dock", "category": "Peripherals", "unit_price": 150.0},
    ]

    dates = pd.date_range("2026-01-01", "2026-03-31", freq="D")

    rows = []
    for i in range(1, num_rows + 1):
        customer = random.choice(customers)
        product = random.choice(products)
        order_date = random.choice(dates)
        quantity = random.randint(1, 5)

        rows.append({
            "order_id": 1000 + i,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "customer_id": customer["customer_id"],
            "customer_name": customer["customer_name"] + (" " if random.random() < 0.2 else ""),
            "city": customer["city"] + ("  " if random.random() < 0.15 else ""),
            "country": customer["country"],
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"] + (" " if random.random() < 0.1 else ""),
            "quantity": quantity,
            "unit_price": product["unit_price"],
        })

    df = pd.DataFrame(rows)

    if not df.empty:
        df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Bronze file written: {OUTPUT_FILE} ({len(df)} rows)")


if __name__ == "__main__":
    generate_synthetic_raw_csv()