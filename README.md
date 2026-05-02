
```markdown
# ML CI/CD Pipeline (Seeds Dataset)

##  Описание проекта

Проект реализует цикл разработки модели машинного обучения с использованием CI/CD подхода.

В рамках работы:
- выполнена подготовка данных
- обучена ML модель (Logistic Regression)
- реализованы тесты
- настроена система управления данными (DVC)
- создан Docker образ
- реализован CI/CD pipeline в Jenkins
- реализован API сервис для взаимодействия с моделью

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

---

## Ссылки

- [Репозиторий GitHub](https://github.com/Gugg11/mle-template)
- [DockerHub Image](https://hub.docker.com/r/gug1/mle-template)


##  Модель

Использована модель:
- **Logistic Regression**

Результаты:
- Accuracy: 0.975 (на тестовой выборке)


## Структура проекта

```text
mle-template/
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
├── requirements.txt
├── config.ini
└── README.md
```

## API сервис

Реализован на Flask.

### Запуск:
```bash
python src/app.py


### Доступные методы:

#### Проверка работы

```bash
GET / 
```

Ответ:

```json
{
  "message": "ML model API is running"
}
```

---

#### Информация о модели

```bash
GET /model
```

---

#### Предсказание

```bash
POST /predict
```

Пример запроса:

```json
{
  "X": [
        {
            "Area": 15.26,
            "Perimeter": 14.84,
            "Compactness": 0.8710,
            "Kernel.Length": 5.763,
            "Kernel.Width": 3.312,
            "Asymmetry.Coeff": 2.221,
            "Kernel.Groove": 5.220
        }
  ]
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

* clone репозитория
* сборка Docker image
* запуск контейнера
* обучение модели
* запуск тестов
* подсчёт coverage
* push в DockerHub

### CD:

* запуск контейнера с моделью
* развёртывание API сервиса

---

## Тестирование

Реализованы unit-тесты:

```bash
coverage run src/unit_tests/test_preprocess.py
coverage run -a src/unit_tests/test_training.py
coverage report
```

Покрытие:

* ~76%

---

## DockerHub

Образ доступен:

```
gug1/mle-template:latest
```

---

##  DVC

Используется для управления данными и артефактами модели.

---

## Запуск проекта

```bash
python src/preprocess.py
python src/train.py
python src/predict.py -m LOG_REG -t func
```

---

##  Вывод

В рамках проекта реализован полный цикл разработки ML модели.
