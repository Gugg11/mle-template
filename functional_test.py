import sys
import requests

url = "http://localhost:8000/predict"
body = {"X": [[14.88, 14.57, 0.881, 5.554, 3.333, 1.018, 4.956]]}

try:
    resp = requests.post(url, json=body, timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        pred = data.get("prediction")
        if pred is not None:
            print(f"TEST PASSED, prediction: {pred}")
            sys.exit(0)
        else:
            print("No prediction field in response")
            sys.exit(1)
    else:
        print(f"Unexpected status code: {resp.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"Functional test failed: {e}")
    sys.exit(1)