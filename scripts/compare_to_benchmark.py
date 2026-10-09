import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://pipeline_user:pipeline_pass@localhost:5432/pipeline_db")

kpi_df = pd.read_sql("SELECT * FROM kpi_metrics ORDER BY month", engine)
benchmark_df = pd.read_sql("SELECT * FROM benchmarks", engine)

# Use the most recent month's KPIs for comparison
latest = kpi_df.iloc[-1]

# Metrics where LOWER is better (flip comparison direction)
lower_is_better = {"cac_payback_months", "burn_multiple"}

results = []

for _, row in benchmark_df.iterrows():
    metric = row["metric"]
    company_value = latest[metric]
    p25, p50, p75 = row["p25"], row["p50"], row["p75"]

    if pd.isna(company_value):
        results.append({"metric": metric, "company_value": None, "position": "No data"})
        continue

    if metric in lower_is_better:
        if company_value <= p75:
            position = "Top quartile"
        elif company_value <= p50:
            position = "Above median"
        elif company_value <= p25:
            position = "Below median"
        else:
            position = "Bottom quartile"
    else:
        if company_value >= p75:
            position = "Top quartile"
        elif company_value >= p50:
            position = "Above median"
        elif company_value >= p25:
            position = "Below median"
        else:
            position = "Bottom quartile"

    results.append({
        "metric": metric,
        "company_value": round(company_value, 2),
        "p25": p25, "p50": p50, "p75": p75,
        "position": position
    })

comparison_df = pd.DataFrame(results)
print(comparison_df)

comparison_df.to_sql("benchmark_comparison", engine, if_exists="replace", index=False)
print("\nComparison saved to Postgres table: benchmark_comparison")