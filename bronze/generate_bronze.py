from pathlib import Path
import random
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "data" / "bronze"
OUTPUT_FILE = OUTPUT_DIR / "sales_raw.csv"


def generate_synthetic_raw_csv(num_rows: int = 100, seed: int = 42) -> None:
    random.seed(seed)

    # 🔹 Expanded customers
    cities = [
        ("Berlin", "Germany"), ("Paris", "France"), ("Madrid", "Spain"),
        ("Rome", "Italy"), ("Amsterdam", "Netherlands"),
        ("Vienna", "Austria"), ("Brussels", "Belgium"),
        ("Zurich", "Switzerland"), ("Prague", "Czech Republic"),
        ("Lisbon", "Portugal")
    ]

    customers = []
    for i in range(1, 21):
        city, country = random.choice(cities)
        customers.append({
            "customer_id": f"C{i:03}",
            "customer_name": f"Customer_{i}",
            "city": city,
            "country": country
        })

    # 🔹 Expanded products
    products = [
        {"product_id": "P001", "product_name": "Laptop", "category": "Electronics", "unit_price": 1200},
        {"product_id": "P002", "product_name": "Mouse", "category": "Accessories", "unit_price": 25},
        {"product_id": "P003", "product_name": "Keyboard", "category": "Accessories", "unit_price": 75},
        {"product_id": "P004", "product_name": "Monitor", "category": "Electronics", "unit_price": 300},
        {"product_id": "P005", "product_name": "Dock", "category": "Peripherals", "unit_price": 150},
        {"product_id": "P006", "product_name": "Tablet", "category": "Electronics", "unit_price": 600},
        {"product_id": "P007", "product_name": "Phone", "category": "Electronics", "unit_price": 900},
        {"product_id": "P008", "product_name": "Headphones", "category": "Audio", "unit_price": 120},
        {"product_id": "P009", "product_name": "Speaker", "category": "Audio", "unit_price": 200},
        {"product_id": "P010", "product_name": "Webcam", "category": "Accessories", "unit_price": 80},
        {"product_id": "P011", "product_name": "Charger", "category": "Accessories", "unit_price": 40},
        {"product_id": "P012", "product_name": "SSD", "category": "Storage", "unit_price": 150},
        {"product_id": "P013", "product_name": "HDD", "category": "Storage", "unit_price": 100},
        {"product_id": "P014", "product_name": "Router", "category": "Networking", "unit_price": 130},
        {"product_id": "P015", "product_name": "Switch", "category": "Networking", "unit_price": 90},
    ]

    # 🔹 Longer date range
    dates = pd.date_range("2025-01-01", "2026-03-31", freq="D")

    rows = []

    for i in range(1, num_rows + 1):
        customer = random.choice(customers)

        # skew: some products appear more often
        product = random.choices(products, weights=[10, 20, 15, 8, 5, 7, 6, 10, 4, 6, 12, 8, 5, 3, 3])[0]

        order_date = random.choice(dates)

        quantity = max(1, int(random.gauss(2, 1)))  # more realistic distribution

        # random discount
        discount = random.choice([0, 0, 0, 0.1, 0.2])
        unit_price = product["unit_price"] * (1 - discount)

        row = {
            "order_id": 100000 + i,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "customer_id": customer["customer_id"],
            "customer_name": customer["customer_name"] + (" " if random.random() < 0.1 else ""),
            "city": customer["city"] + ("  " if random.random() < 0.1 else ""),
            "country": customer["country"],
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"] + (" " if random.random() < 0.05 else ""),
            "quantity": quantity,
            "unit_price": round(unit_price, 2),
        }

        # 🔹 introduce missing values (realistic noise)
        if random.random() < 0.02:
            row["customer_name"] = None

        rows.append(row)

    df = pd.DataFrame(rows)

    # 🔹 duplicates
    if not df.empty:
        df = pd.concat([df, df.sample(frac=0.01)], ignore_index=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Bronze file written: {OUTPUT_FILE} ({len(df)} rows)")


if __name__ == "__main__":
    generate_synthetic_raw_csv(100)
