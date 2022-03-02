# promo_api

# Переменные окружения

```dotenv
# обязательные
APP_ID=promo_api
ENVIRONMENT=local/stage/prod
SECRET_TOKEN=SOME-SECRET-TOKEN
RSA_PUBLIC_KEY=SOME-RSA-PUBLIC-KEY   # в base64
RSA_PRIVATE_KEY=SOME-RSA-PRIVATE-KEY # в base64

# опциональные
DEBUG=0/1
AUTH_TOKEN_ACCESS_TTL=86400     # длительность Access Token (количество секунд)
AUTH_TOKEN_REFRESH_TTL=2592000   # длительность Refresh Token (количество секунд)
```

## Инициализация проекта

```bash
pip install -r config/requirements.txt -r config/requirements.test.txt
pip install -e .
```

## Локальный запуск проекта

### API
```bash
python src/entrypoints/api.py
```
или
```bash
uvicorn src.entrypoints.api:app --port 8000
```

## Создание тестовых данных

```bash
python util/faker.py
# > faker.sql
```

## Локальный запуск тестов

```bash
make test             # запуск всех тестов (unit, functional)
make functional-test  # только функциональных тестов
```

## Миграции
Используется Alembic https://alembic.sqlalchemy.org/en/latest/

### Запуск миграций в БД
```bash
alembic upgrade head
```

### Создать миграцию
```bash
alembic revision -m "short-migration-description"
```

### Откатить последнюю миграцию
```bash
alembic downgrade -1
```

## Структура кода

