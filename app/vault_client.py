import os
import time
import requests

def _get_vault_addr():
    return os.environ.get("VAULT_ADDR", "http://vault:8200")

def _get_vault_token():
    return os.environ.get("VAULT_TOKEN", "")

def get_headers():
    return {"X-Vault-Token": _get_vault_token()}

def wait_for_vault(retries=30, delay=2):
    addr = _get_vault_addr()
    if not addr or not _get_vault_token():
        print("Vault not configured, skipping health check")
        return
    for _ in range(retries):
        try:
            resp = requests.get(f"{addr}/v1/sys/health", timeout=3)
            if resp.status_code in [200, 429, 472, 473, 501, 503]:
                return
        except requests.exceptions.RequestException:
            time.sleep(delay)
    raise ConnectionError("Vault is not available")

def write_postgres_secret():
    addr = _get_vault_addr()
    token = _get_vault_token()
    if not addr or not token:
        raise RuntimeError("Vault not configured")
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
    resp = requests.post(f"{addr}/v1/secret/data/postgres",
                         headers=get_headers(), json=payload, timeout=5)
    resp.raise_for_status()

def get_postgres_secret():
    addr = _get_vault_addr()
    token = _get_vault_token()
    # Если Vault не настроен, возвращаем переменные окружения напрямую
    if not addr or not token:
        print("Vault not configured, using environment variables")
        return {
            "POSTGRES_DB": os.environ.get("POSTGRES_DB", ""),
            "POSTGRES_USER": os.environ.get("POSTGRES_USER", ""),
            "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "POSTGRES_HOST": os.environ.get("POSTGRES_HOST", ""),
            "POSTGRES_PORT": os.environ.get("POSTGRES_PORT", "")
        }
    wait_for_vault()
    resp = requests.get(f"{addr}/v1/secret/data/postgres",
                        headers=get_headers(), timeout=5)
    resp.raise_for_status()
    return resp.json()["data"]["data"]