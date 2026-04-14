from pathlib import Path
import pandas as pd

BRONZE_FILE = Path("/data/bronze/sales_raw.csv")
SILVER_DIR = Path("/data/silver")
SILVER_FILE = SILVER_DIR / "sales_clean.csv"


def load_bronze() -> pd.DataFrame:
    if not BRONZE_FILE.exists():
        raise FileNotFoundError(f"Missing bronze file: {BRONZE_FILE}")
    return pd.read_csv(BRONZE_FILE)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    required_columns = [
        "order_id",
        "order_date",
        "customer_id",
        "customer_name",
        "city",
        "country",
        "product_id",
        "product_name",
        "category",
        "quantity",
        "unit_price",
    ]
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    text_cols = [
        "customer_id",
        "customer_name",
        "city",
        "country",
        "product_id",
        "product_name",
        "category",
    ]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["order_id"] = pd.to_numeric(df["order_id"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    df = df.dropna(subset=[
        "order_id",
        "order_date",
        "customer_id",
        "customer_name",
        "product_id",
        "product_name",
        "quantity",
        "unit_price",
    ])

    df = df[(df["quantity"] > 0) & (df["unit_price"] >= 0)]
    df = df.drop_duplicates()

    df["order_id"] = df["order_id"].astype(int)
    df["amount"] = df["quantity"] * df["unit_price"]
    df["date_key"] = df["order_date"].dt.strftime("%Y%m%d").astype(int)

    df = df.sort_values(["order_date", "order_id"]).reset_index(drop=True)
    return df


def save_silver(df: pd.DataFrame) -> None:
    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(SILVER_FILE, index=False)
    print(f"Silver file written: {SILVER_FILE} ({len(df)} rows)")


if __name__ == "__main__":
    bronze_df = load_bronze()
    silver_df = clean_data(bronze_df)
    save_silver(silver_df)