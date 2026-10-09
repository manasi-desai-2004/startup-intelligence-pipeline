import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://pipeline_user:pipeline_pass@localhost:5432/pipeline_db")

# Load raw data, sorted by month
df = pd.read_sql("SELECT * FROM raw_financials ORDER BY month", engine)

# --- KPI Calculations ---

# MRR Growth Rate (month-over-month %)
df["mrr_growth_rate"] = df["mrr"].pct_change() * 100

# Gross Margin %
df["gross_margin_pct"] = ((df["revenue"] - df["cogs"]) / df["revenue"]) * 100

# CAC (Customer Acquisition Cost)
df["cac"] = df["cac_spend"] / df["new_customers"]

# ARPA (Average Revenue Per Account, monthly)
df["arpa"] = df["mrr"] / df["total_customers"]

# CAC Payback Period (in months) = CAC / (ARPA * Gross Margin %)
df["cac_payback_months"] = df["cac"] / (df["arpa"] * (df["gross_margin_pct"] / 100))

# Logo Retention Rate (% of customers retained month-over-month)
# NOTE: this is a proxy for true dollar-based NRR, which needs per-customer
# expansion/contraction revenue data not present in this sample dataset.
df["prev_total_customers"] = df["total_customers"].shift(1)
df["logo_retention_pct"] = ((df["prev_total_customers"] - df["churned_customers"]) / df["prev_total_customers"]) * 100

# Net New ARR (Annual Recurring Revenue added this month, annualized)
df["net_new_arr"] = (df["mrr"] - df["mrr"].shift(1)) * 12

# Burn Multiple = Net Burn / Net New ARR
# Net Burn approximated as (CAC spend + COGS) - Revenue for that month
df["net_burn"] = (df["cac_spend"] + df["cogs"]) - df["revenue"]
df["burn_multiple"] = df["net_burn"] / df["net_new_arr"]

# Rule of 40 = MRR Growth Rate % + Gross Margin % (simplified proxy;
# true Rule of 40 uses profit margin, which needs full P&L data)
df["rule_of_40"] = df["mrr_growth_rate"] + df["gross_margin_pct"]

print(df[["month", "mrr_growth_rate", "gross_margin_pct", "cac",
          "cac_payback_months", "logo_retention_pct", "burn_multiple",
          "rule_of_40"]].round(2))

# Save computed KPIs to a new table
df.to_sql("kpi_metrics", engine, if_exists="replace", index=False)
print("\nKPIs saved to Postgres table: kpi_metrics")