
```markdown
# ML CI/CD Pipeline (Seeds Dataset)

##  Описание проекта

Проект реализует цикл разработки модели машинного обучения с использованием CI/CD подхода.

В рамках работы:
- выполнена подготовка данных (Seeds dataset, вариант 19)
- обучена ML модель (Logistic Regression (точность 0.975))
- реализованы тесты
- создан Docker образ
- реализован CI/CD pipeline в Jenkins
- реализован API сервис для взаимодействия с моделью
```
---
```
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
```
## Ссылки

- [Репозиторий GitHub](https://github.com/Gugg11/mle-template/tree/lab1-ci-cd)
- [DockerHub Image](https://hub.docker.com/r/gug1/mle-template) (тег lab1)
```
---
```
##  Модель

Использована модель:
- **Logistic Regression**
- **StandardScaler для предобработки**
- **Точность на тестовой выборке: 0.975**

Результаты:
- Accuracy: 0.975 (на тестовой выборке)
```
---

## Структура проекта

```text
mle-template/
├── app/
│   ├── __init__.py
│   └── main.py
├── src/
│   ├── unit_tests/
│   │   ├── test_preprocess.py
│   │   └── test_training.py
│   ├── preprocess.py
│   ├── train.py
│   ├── predict.py
│   └── app.py
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
  "prediction": [2]
}
```

---

## Docker

### Сборка и запуск:

```bash
docker-compose build
docker-compose up
```

После запуска API доступен:

```
http://localhost:8000
```

---

## CI/CD (Jenkins)

Реализован pipeline:

### CI:

- клонирование репозитория
- установка зависимостей
- предобработка данных (`src/preprocess.py`)
- обучение модели (`src/train.py`)
- юнит-тесты + coverage
- функциональное тестирование модели (`src/predict.py -m LOG_REG -t func`)
- сборка Docker-образа (`docker-compose build`)
- логин и пуш образа в DockerHub

### CD:

- получение образа из DockerHub
- удаление старого контейнера
- запуск контейнера с пробросом порта 8000
- функциональное тестирование API (POST /predict и проверка ответа)
- остановка и удаление контейнера

---

## Тестирование

Реализованы unit-тесты:

```bash
coverage run src/unit_tests/test_preprocess.py
coverage run -a src/unit_tests/test_training.py
coverage report
```

Покрытие:

* ~92%

---

## DockerHub

Образ доступен:

```
docker build -t gug1/mle-template:lab1 .
```

---

## Запуск проекта

1. Подготовка данных:
```bash
python src/preprocess.py
python src/train.py
python src/predict.py -m LOG_REG -t func
```
2. Обучение модели:
```bash
python src/train.py
```
3. Тестирование модели:
```bash
python src/predict.py -m LOG_REG -t smoke
python src/predict.py -m LOG_REG -t func  
```
4. Запуск API:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 
```

---

##  Вывод

В рамках проекта реализован полный цикл разработки ML модели.
