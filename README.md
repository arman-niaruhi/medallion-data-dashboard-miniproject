# Medallion Data Dashboard Mini Project

This project builds a small medallion-style data pipeline and serves the curated gold-layer data through a Streamlit dashboard.

The repository includes:
- `bronze/`: raw data generation
- `silver/`: cleaned and standardized transformations
- `gold/`: dimensional/star-style analytical outputs
- `dashboard/`: Streamlit app for exploring the gold data
- `.github/workflows/update-medallion.yml`: CI/CD workflow for rebuilding datasets and validating the app

## Project Structure

```text
.
├── bronze/
│   └── generate_bronze.py
├── silver/
│   └── build_silver.py
├── gold/
│   └── build_gold.py
├── dashboard/
│   ├── app.py
│   └── requirements.txt
├── data/
├── compose.yml
└── README.md
```

## Dashboard

The Streamlit app reads from `data/gold/` and exposes the dashboard through top navigation tabs:

Online dashboard:
- https://medallion-data-pipeline.streamlit.app/

- `Overview`: high-level KPIs
- `Commercial`: metric breakdown chart and top products
- `Trends`: monthly trend analysis
- `Insights`: geography and category views
- `Details`: filtered transaction-level table

Filters remain in the sidebar and apply across all tabs:
- year
- category
- country
- chart variable
- comparison dimension
- trend variable
- top results count

## Data Layers

- `CRM data`: customer master and transactional sales data, including customer IDs, customer names, city, country, order dates, product details, quantity, and unit price.
- `Bronze input data`: raw synthetic sales and CRM-style records generated from source fields such as customer, location, product, order date, quantity, and unit price.
- `Silver cleaned data`: standardized and cleaned sales dataset with trimmed text fields, corrected data types, removed duplicates, handled missing values, and calculated transaction amount.
- `Gold analytical data`: business-ready dimensional model with `fact_sales`, `dim_customer`, `dim_product`, and `dim_date` tables for reporting and dashboard analysis.

## Run Locally

### 1. Install dashboard dependencies

```bash
pip install -r dashboard/requirements.txt
```

### 2. Build the medallion layers

Run the pipeline scripts in order:

```bash
python bronze/generate_bronze.py
python silver/build_silver.py
python gold/build_gold.py
```

### 3. Start the dashboard

```bash
streamlit run dashboard/app.py
```

## Docker Compose

If you want to run the pipeline services with Docker, use:

```bash
docker compose -f compose.yml up --build
```

## CI/CD

The GitHub Actions workflow at `.github/workflows/update-medallion.yml`:

- installs Python dependencies from `dashboard/requirements.txt`
- rebuilds the bronze, silver, and gold datasets
- validates expected CSV outputs
- smoke-tests the Streamlit app import
- commits refreshed `data/` artifacts back to `main` when they change

For hosted Streamlit deployments:
- deploy from this same repository
- point the platform to the `main` branch
- use `dashboard/app.py` as the entrypoint

## Notes

- Python cache files such as `*.pyc` and `__pycache__/` are ignored via `.gitignore`
- the dashboard expects the gold CSV outputs to exist before startup
