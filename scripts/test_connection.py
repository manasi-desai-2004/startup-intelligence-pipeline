import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="pipeline_db",
    user="pipeline_user",
    password="pipeline_pass"
)
print("Connected successfully")
conn.close()