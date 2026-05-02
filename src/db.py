import psycopg2
from vault_client import get_postgres_secret, write_postgres_secret


def get_connection():
    # получаем секреты из Vault
    secret = get_postgres_secret()

    return psycopg2.connect(
        dbname=secret["POSTGRES_DB"],
        user=secret["POSTGRES_USER"],
        password=secret["POSTGRES_PASSWORD"],
        host=secret["POSTGRES_HOST"],
        port=secret["POSTGRES_PORT"],
    )


def init_db():
    # сначала записываем секреты в Vault (один раз)
    write_postgres_secret()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            area FLOAT,
            perimeter FLOAT,
            compactness FLOAT,
            kernel_length FLOAT,
            kernel_width FLOAT,
            asymmetry_coeff FLOAT,
            kernel_groove FLOAT,
            prediction INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def save_prediction(features, prediction):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO predictions (
            area,
            perimeter,
            compactness,
            kernel_length,
            kernel_width,
            asymmetry_coeff,
            kernel_groove,
            prediction
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """,
        (
            float(features["Area"]),
            float(features["Perimeter"]),
            float(features["Compactness"]),
            float(features["Kernel.Length"]),
            float(features["Kernel.Width"]),
            float(features["Asymmetry.Coeff"]),
            float(features["Kernel.Groove"]),
            int(prediction),
        )
    )

    conn.commit()
    cur.close()
    conn.close()