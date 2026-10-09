import pandas as pd
from sqlalchemy import create_engine

# Read the raw CSV
df = pd.read_csv("raw_data/sample_company.csv")

print("Data loaded from CSV:")
print(df.head())
print(f"\nShape: {df.shape}")

# Connect to Postgres
engine = create_engine("postgresql+psycopg2://pipeline_user:pipeline_pass@localhost:5432/pipeline_db")

# Load into a raw table (replace if it already exists, for repeat testing)
df.to_sql("raw_financials", engine, if_exists="replace", index=False)

print("\nData loaded into Postgres table: raw_financials")