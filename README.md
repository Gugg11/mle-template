
```markdown
# ML CI/CD Pipeline (Seeds Dataset)

##  Описание проекта

Проект расширяет ЛР1, добавляя сохранение результатов предсказаний в PostgreSQL.
- Модель: Logistic Regression (точность 0.975)
- API: FastAPI
- База данных: PostgreSQL (контейнер)
- Безопасность: секреты передаются через переменные окружения, не хранятся в коде
- CI/CD: Jenkins
```
---

## Датасет

Использован датасет: Вариант 19
- **Seeds Dataset (UCI)**  
https://www.kaggle.com/datasets/jmcaro/wheat-seedsuci

Признаки:
 0   Area             
 1   Perimeter        
 2   Compactness     
 3   Kernel.Length    
 4   Kernel.Width     
 5   Asymmetry.Coeff  
 6   Kernel.Groove  
```
---

## Ссылки

- [Репозиторий GitHub](https://github.com/Gugg11/mle-template/tree/lab2-postgres)
- [DockerHub Image](https://hub.docker.com/r/gug1/mle-template) (тег **lab2**)
```
---

##  Модель

Использована модель:
- **Logistic Regression**
- **StandardScaler для предобработки**
- **Точность на тестовой выборке: 0.975**

Результаты:
- Accuracy: 0.975 (на тестовой выборке)
```
---
## Взаимодействие с базой данных

### Конфигурация подключения
- Тип БД: PostgreSQL
- Подключение через переменные окружения / config.ini
- Аутентификация: [через env-переменные]
```
---
### Схема данных
```sql
-- Пример таблицы для результатов модели
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    features FLOAT8[] NOT NULL,
    prediction INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
---
## Архитектура
docker-compose включает два сервиса:
- `db` (postgres:15) — база данных
- `web` (FastAPI) — модель и API

```
---
## Безопасность
Все пароли и логины вынесены в `.env` (не хранится в репозитории). Пример в `.env.example`.
В Jenkins секреты берутся из Credentials и записываются в `.env` на этапе сборки.

```
---
## Структура проекта

```text
mle-template/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── db.py
├── src/
│   ├── unit_tests/
│   │   ├── test_preprocess.py
│   │   └── test_training.py
│   ├── preprocess.py
│   ├── train.py
│   └── predict.py
├── data/
│   └── seeds.csv
├── experiments/
│   └── log_reg.sav
├── tests/
│   ├── test_0.json
│   └── test_1.json
├── CI/
│   └── Jenkinsfile
├── CD/
│   └── Jenkinsfile
├── Dockerfile
├── docker-compose.yml
├── functional_test.py
├── requirements.txt
├── config.ini
└── README.md
```
---
## API сервис

Реализован на **FastAPI** с автоматической документацией Swagger.

### Запуск:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
После запуска документация доступна по адресу:  
[http://localhost:8000/docs](http://localhost:8000/docs)

### Доступные методы:

#### `GET /` – проверка работы
Ответ: `{"message":"ML model API is running"}`

#### `GET /health` – здоровье сервиса
Ответ: `{"status":"ok"}`

#### `GET /model` – информация о модели
Ответ: `{"model":"LOG_REG","dataset":"Seeds","status":"ready","scaler_loaded":true}`

#### `POST /predict` – предсказание
Тело запроса (ровно 7 признаков, список списков):
```json
{
  "X": [
    [14.88, 14.57, 0.881, 5.554, 3.333, 1.018, 4.956]
  ]
}
```
Успешный ответ (класс предсказания в массиве):
```json
{
  "prediction": [1]
}
```

---

## Docker

### Сборка и запуск:

```bash
docker-compose build
docker-compose up -d
```

После запуска API доступен:

```
 http://localhost:8000/docs
```

---

## CI/CD (Jenkins)

Реализован pipeline:

### CI:

- клонирование репозитория
- генерация .env из креденшелов Jenkins
- сборка Docker-образа (docker-compose build)
- запуск контейнеров (docker-compose up -d)
- юнит-тесты + coverage (внутри контейнера)
- функциональное тестирование модели (src/predict.py)
- пуш образа с тегом lab2 в DockerHub

### CD:

- получение образа из DockerHub gug1/mle-template:lab2
- удаление старого контейнера
- запуск контейнера docker-compose up -d
- функциональный тест (functional_test.py) – проверяет ответ API и запись в БД
- остановка и удаление контейнера

---

## Тестирование

Реализованы unit-тесты:

```bash
coverage run src/unit_tests/test_preprocess.py
coverage run -a src/unit_tests/test_training.py
coverage report
```
Функциональный тест: functional_test.py выводит DB check: features=[...], prediction=1, подтверждая сохранение в БД
Покрытие:

* ~92%

---

## DockerHub

Образ доступен:

```
docker build -t gug1/mle-template:lab2 
```

---

## Запуск проекта локально

1. Создайте файл .env в корне проекта:
```bash
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
```
2. Поднимите сервисы:
```bash
docker-compose up -d --build
```
3. Откройте http://localhost:8000/docs и выполните запрос к /predict:

---

##  Вывод

В результате работы реализован полный цикл запуска ML-сервиса с базой данных: модель делает предсказание через API, а результат автоматически сохраняется в PostgreSQL.
