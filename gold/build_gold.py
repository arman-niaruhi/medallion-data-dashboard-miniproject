"""Build gold-layer analytical tables from the cleaned silver dataset."""

from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
SILVER_FILE = ROOT_DIR / "data" / "silver" / "sales_clean.csv"
GOLD_DIR = ROOT_DIR / "data" / "gold"


def load_silver() -> pd.DataFrame:
    """Load the cleaned silver dataset used to build analytical outputs."""
    if not SILVER_FILE.exists():
        raise FileNotFoundError(f"Missing silver file: {SILVER_FILE}")
    df = pd.read_csv(SILVER_FILE)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    return df


def build_dim_customer(df: pd.DataFrame) -> pd.DataFrame:
    """Create the customer dimension from CRM-style customer attributes."""
    dim_customer = (
        df[["customer_id", "customer_name", "city", "country"]]
        .drop_duplicates()
        .sort_values("customer_id")
        .reset_index(drop=True)
    )
    dim_customer["customer_key"] = range(1, len(dim_customer) + 1)
    return dim_customer[["customer_key", "customer_id", "customer_name", "city", "country"]]


def build_dim_product(df: pd.DataFrame) -> pd.DataFrame:
    """Create the product dimension for analytical reporting."""
    dim_product = (
        df[["product_id", "product_name", "category"]]
        .drop_duplicates()
        .sort_values("product_id")
        .reset_index(drop=True)
    )
    dim_product["product_key"] = range(1, len(dim_product) + 1)
    return dim_product[["product_key", "product_id", "product_name", "category"]]


def build_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    """Create the date dimension used by the gold fact table."""
    dim_date = pd.DataFrame({
        "full_date": sorted(df["order_date"].dropna().drop_duplicates())
    }).reset_index(drop=True)

    dim_date["date_key"] = dim_date["full_date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["year"] = dim_date["full_date"].dt.year
    dim_date["quarter"] = dim_date["full_date"].dt.quarter
    dim_date["month"] = dim_date["full_date"].dt.month
    dim_date["month_name"] = dim_date["full_date"].dt.month_name()
    dim_date["day"] = dim_date["full_date"].dt.day
    dim_date["day_name"] = dim_date["full_date"].dt.day_name()
    dim_date["week_of_year"] = dim_date["full_date"].dt.isocalendar().week.astype(int)

    return dim_date[
        [
            "date_key",
            "full_date",
            "year",
            "quarter",
            "month",
            "month_name",
            "day",
            "day_name",
            "week_of_year",
        ]
    ]


def build_fact_sales(
    df: pd.DataFrame,
    dim_customer: pd.DataFrame,
    dim_product: pd.DataFrame,
) -> pd.DataFrame:
    """Create the fact table with sales measures and surrogate keys."""
    fact = df.copy()

    fact = fact.merge(
        dim_customer[["customer_id", "customer_key"]],
        on="customer_id",
        how="left",
    )

    fact = fact.merge(
        dim_product[["product_id", "product_key"]],
        on="product_id",
        how="left",
    )

    fact_sales = fact[
        [
            "order_id",
            "customer_key",
            "product_key",
            "date_key",
            "quantity",
            "unit_price",
            "amount",
        ]
    ].copy()

    fact_sales = fact_sales.rename(columns={"order_id": "sales_id"})
    fact_sales = fact_sales.sort_values("sales_id").reset_index(drop=True)
    return fact_sales


def save_gold(
    dim_customer: pd.DataFrame,
    dim_product: pd.DataFrame,
    dim_date: pd.DataFrame,
    fact_sales: pd.DataFrame,
) -> None:
    """Persist the gold analytical model to CSV files."""
    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    dim_customer.to_csv(GOLD_DIR / "dim_customer.csv", index=False)
    dim_product.to_csv(GOLD_DIR / "dim_product.csv", index=False)
    dim_date.to_csv(GOLD_DIR / "dim_date.csv", index=False)
    fact_sales.to_csv(GOLD_DIR / "fact_sales.csv", index=False)

    print(f"Gold files written in: {GOLD_DIR}")


if __name__ == "__main__":
    silver_df = load_silver()
    dim_customer = build_dim_customer(silver_df)
    dim_product = build_dim_product(silver_df)
    dim_date = build_dim_date(silver_df)
    fact_sales = build_fact_sales(silver_df, dim_customer, dim_product)
    save_gold(dim_customer, dim_product, dim_date, fact_sales)
