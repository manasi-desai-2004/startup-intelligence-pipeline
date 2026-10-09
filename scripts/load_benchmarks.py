import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://pipeline_user:pipeline_pass@localhost:5432/pipeline_db")

# Benchmark reference data for early-stage (Seed/Series A) SaaS companies
# Sourced conceptually from publicly available reports (e.g. OpenView SaaS Benchmarks)
# Values represent percentile bands: p25 = bottom quartile, p50 = median, p75 = top quartile
benchmark_data = {
    "metric": [
        "mrr_growth_rate", "gross_margin_pct", "cac_payback_months",
        "logo_retention_pct", "burn_multiple", "rule_of_40"
    ],
    "p25": [3.0, 65.0, 18.0, 85.0, 3.0, 25.0],
    "p50": [7.0, 75.0, 12.0, 92.0, 1.5, 40.0],
    "p75": [12.0, 82.0, 7.0, 97.0, 0.8, 55.0],
}

df_benchmark = pd.DataFrame(benchmark_data)
print(df_benchmark)

df_benchmark.to_sql("benchmarks", engine, if_exists="replace", index=False)
print("\nBenchmark table saved to Postgres: benchmarks")