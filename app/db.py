import psycopg2
from app.vault_client import get_postgres_secret 

def get_connection():
    secrets = get_postgres_secret()
    return psycopg2.connect(
        dbname=secrets["POSTGRES_DB"],
        user=secrets["POSTGRES_USER"],
        password=secrets["POSTGRES_PASSWORD"],
        host=secrets["POSTGRES_HOST"],
        port=secrets["POSTGRES_PORT"],
    )


def init_db():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id SERIAL PRIMARY KEY,
                    features FLOAT8[] NOT NULL,
                    prediction INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        conn.commit()
    finally:
        conn.close()


def save_prediction(features: list, prediction: int):
    """Принимает список из 7 чисел и предсказанный класс."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO predictions (features, prediction) VALUES (%s, %s)",
                (features, prediction)
            )
        conn.commit()
    finally:
        conn.close()