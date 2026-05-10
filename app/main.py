from pathlib import Path
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

# Путь к папке, в которой лежит этот файл (app/)
BASE_DIR = Path(__file__).resolve().parent

# Поднимаемся на уровень корня проекта (mle-template/)
PROJECT_ROOT = BASE_DIR.parent

MODEL_PATH = PROJECT_ROOT / "experiments" / "log_reg.sav"
SCALER_PATH = PROJECT_ROOT / "experiments" / "scaler.sav"

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    print(f"Failed to load model: {e}")

try:
    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)
except Exception as e:
    scaler = None
    print(f"Scaler not loaded: {e}")


class InputData(BaseModel):
    X: List[List[float]] = Field()

app = FastAPI(
    title="Seeds Classification API",
    description="API для классификации сортов пшеницы по 7 признакам",
    version="1.0.0"
)


@app.get("/")
async def home():
    return {"message": "ML model API is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/model")
async def model_info():
    return {
        "model": "LOG_REG",
        "dataset": "Seeds",
        "status": "ready" if model is not None else "error",
        "scaler_loaded": scaler is not None
    }


@app.post("/predict")
async def predict(data: InputData):
    if model is None:
        raise HTTPException(status_code=500, detail="Модель не загружена")
    if scaler is None:
        raise HTTPException(status_code=500, detail="Скалер не загружен")

    X = pd.DataFrame(data.X)

    if X.shape[1] != 7:
        raise HTTPException(status_code=400, detail="Ожидается 7 признаков")

    X = scaler.transform(X)
    prediction = model.predict(X)
    return {"prediction": prediction.tolist()}