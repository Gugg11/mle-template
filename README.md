
```markdown
# ML CI/CD Pipeline (Seeds Dataset)

##  Описание проекта

Проект расширяет ЛР3, добавляя асинхронную передачу результатов предсказаний в Apache Kafka.
- Модель: Logistic Regression (точность 0.975)
- API: FastAPI
- База данных: PostgreSQL (контейнер)
- Хранилище секретов: HashiCorp Vault
- Потоковая передача: Apache Kafka (Producer + Consumer)
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

- [Репозиторий GitHub](https://github.com/Gugg11/mle-template/tree/lab4-kafka)
- [DockerHub Image](https://hub.docker.com/r/gug1/mle-template) (тег **lab4**)
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

### Конфигурация подключения
- Тип БД: PostgreSQL
- Подключение через переменные окружения / config.ini
```
---
## Хранилище секретов (HashiCorp Vault)

Параметры подключения к PostgreSQL больше не передаются через `.env` напрямую.
Они хранятся в Vault и запрашиваются приложением динамически с использованием токена.

- `vault-init` — одноразовый контейнер, записывающий секреты в Vault при старте.
- `vault_client.py` — модуль для взаимодействия с Vault (запись/чтение секретов).
---

### Потоковая передача (Apache Kafka)
Каждое предсказание, полученное через API, публикуется в Kafka-топик predictions.
Отдельный сервис kafka-consumer непрерывно читает этот топик и выводит сообщения в лог.
Producer встроен в веб-сервис (app/kafka_producer.py).
Consumer запускается как самостоятельный контейнер (app/kafka_consumer.py).

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
docker-compose включает шесть сервисов:
- db (postgres:15) — база данных
- web (FastAPI) — модель и API
- vault (hashicorp/vault) — хранилище секретов
- vault-init — инициализация секретов (одноразовый)
- zookeeper (confluentinc/cp-zookeeper) — координатор для Kafka
- kafka (confluentinc/cp-kafka) — брокер сообщений
- kafka-consumer — сервис чтения сообщений из топика predictions

---
## Безопасность
Все пароли и логины вынесены из кода и не хранятся в переменных окружения веб-сервиса.
Секреты записываются в Vault на этапе инициализации, а веб-приложение получает их через HTTP API Vault.
В репозитории лежит только `.env.example`.
В Jenkins секреты берутся из Credentials и передаются в `.env` для `vault-init`. 

---
## Структура проекта

```text
mle-template/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├──  vault_client.py
│   ├── kafka_producer.py
│   ├── kafka_consumer.py
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

### Сборка и запуск

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
- генерация .env из креденшелов Jenkins (с VAULT_TOKEN)
- сборка Docker-образа
- запуск всех контейнеров (включая Kafka, Zookeeper, consumer, vault и vault-init)
- юнит-тесты + coverage (внутри контейнера)
- пуш образа с тегом lab3 в DockerHub

### CD:

- получение образа из DockerHub gug1/mle-template:lab4
- удаление старого контейнера
- запуск контейнера docker-compose up -d
- функциональный тест (functional_test.py) – проверяет ответ API и запись в БД
- остановка и удаление контейнера
- 
Примечание: В логах CD может появляться DB check failed: 'POSTGRES_DB'. Это не ошибка, а подтверждение того, что веб-сервис не использует переменные окружения для БД (секреты получаются из Vault).

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
docker build -t gug1/mle-template:lab3 
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
VAULT_TOKEN =
```
2. Поднимите сервисы:
```bash
docker-compose up -d --build
```
3. Откройте http://localhost:8000/docs и выполните запрос к /predict:
   
4.Проверьте, что сообщение попало в Kafka:

```bash
docker logs kafka-consumer 
```
---

##  Вывод

В результате работы реализован ML-сервис с безопасным хранением секретов и асинхронной передачей результатов: модель предсказывает через API, результат сохраняется в PostgreSQL, а информация о предсказании публикуется в Kafka для дальнейшей обработки.
