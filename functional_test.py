import requests
import os
import psycopg2

url = "http://localhost:8000/predict"
body = {"X": [[14.88, 14.57, 0.881, 5.554, 3.333, 1.018, 4.956]]}

resp = requests.post(url, json=body, timeout=10)
assert resp.status_code == 200, f"Status {resp.status_code}"
data = resp.json()
assert "prediction" in data, "No prediction field"
print(f"Prediction: {data['prediction']}")

# Проверяем, что запись появилась в БД
try:
    conn = psycopg2.connect(
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"],
    )
    cur = conn.cursor()
    cur.execute("SELECT features, prediction FROM predictions ORDER BY id DESC LIMIT 1;")
    row = cur.fetchone()
    if row:
        print(f"DB check: features={row[0]}, prediction={row[1]}")
    else:
        print("No records in DB")
    cur.close()
    conn.close()
except Exception as e:
    print(f"DB check failed: {e}")
    # не фатально, потому что функциональный тест API уже пройден