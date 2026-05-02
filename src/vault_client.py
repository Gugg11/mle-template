import os
import time
import requests


VAULT_ADDR = os.environ["VAULT_ADDR"]
VAULT_TOKEN = os.environ["VAULT_TOKEN"]

SECRET_PATH = "v1/secret/data/postgres"


def get_headers():
    return {
        "X-Vault-Token": VAULT_TOKEN
    }


def wait_for_vault(retries=30, delay=2):
    for _ in range(retries):
        try:
            response = requests.get(
                f"{VAULT_ADDR}/v1/sys/health",
                timeout=3
            )

            if response.status_code in [200, 429, 472, 473, 501, 503]:
                return True

        except requests.exceptions.RequestException:
            time.sleep(delay)

    raise ConnectionError("Vault is not available")


def write_postgres_secret():
    """
    Записывает параметры подключения в Vault.
    Берём ТОЛЬКО из env (Jenkins Credentials / .env)
    """
    wait_for_vault()

    payload = {
        "data": {
            "POSTGRES_DB": os.environ["POSTGRES_DB"],
            "POSTGRES_USER": os.environ["POSTGRES_USER"],
            "POSTGRES_PASSWORD": os.environ["POSTGRES_PASSWORD"],
            "POSTGRES_HOST": os.environ["POSTGRES_HOST"],
            "POSTGRES_PORT": os.environ["POSTGRES_PORT"]
        }
    }

    response = requests.post(
        f"{VAULT_ADDR}/{SECRET_PATH}",
        headers=get_headers(),
        json=payload,
        timeout=5
    )

    response.raise_for_status()


def get_postgres_secret():
    """
    Получает параметры подключения из Vault
    """
    wait_for_vault()

    response = requests.get(
        f"{VAULT_ADDR}/{SECRET_PATH}",
        headers=get_headers(),
        timeout=5
    )

    response.raise_for_status()

    return response.json()["data"]["data"]