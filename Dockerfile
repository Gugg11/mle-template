FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# Обучение и тесты на этапе сборки
RUN python src/preprocess.py && \
    python src/train.py && \
    coverage run src/unit_tests/test_preprocess.py && \
    coverage run -a src/unit_tests/test_training.py && \
    coverage report -m

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]