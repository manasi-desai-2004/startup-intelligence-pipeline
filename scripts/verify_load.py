import psycopg2

conn = psycopg2.connect(
    host="localhost", port=5432,
    dbname="pipeline_db", user="pipeline_user", password="pipeline_pass"
)
cur = conn.cursor()
cur.execute("SELECT * FROM raw_financials;")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.close()