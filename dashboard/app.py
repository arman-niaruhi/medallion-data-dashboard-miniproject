from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Medallion Dashboard", layout="wide")

BASE = Path(__file__).resolve().parents[1] / "data" / "gold"

@st.cache_data
def load_data():
    fact_sales = pd.read_csv(BASE / "fact_sales.csv")
    dim_customer = pd.read_csv(BASE / "dim_customer.csv")
    dim_product = pd.read_csv(BASE / "dim_product.csv")
    dim_date = pd.read_csv(BASE / "dim_date.csv")
    return fact_sales, dim_customer, dim_product, dim_date

fact_sales, dim_customer, dim_product, dim_date = load_data()

df = (
    fact_sales
    .merge(dim_customer, on="customer_key", how="left")
    .merge(dim_product, on="product_key", how="left")
    .merge(dim_date, on="date_key", how="left")
)

st.title("Sales Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Revenue", f"{df['amount'].sum():,.2f}")
col2.metric("Orders", f"{df['sales_id'].nunique():,}")
col3.metric("Customers", f"{df['customer_id'].nunique():,}")

st.subheader("Revenue by Category")
rev_by_cat = df.groupby("category", as_index=False)["amount"].sum()
st.bar_chart(rev_by_cat.set_index("category"))

st.subheader("Revenue by Month")
rev_by_month = df.groupby(["year", "month_name"], as_index=False)["amount"].sum()
st.dataframe(rev_by_month, use_container_width=True)

st.subheader("Detailed Data")
st.dataframe(df, use_container_width=True)