# Library Service API

Бэкенд-сервис для управления библиотекой. 

## Технологии

- Python 3.11
- FastAPI
- PostgreSQL 15
- SQLAlchemy 2.0 (async)
- Docker / Docker Compose
- Pydantic
- 
## Запуск и остановка

Запуск проекта

docker compose up --build

После запуска сервис будет доступен:

API: http://localhost:8000

Swagger документация: http://localhost:8000/docs

Остановка проекта

docker compose down

Остановка с удалением данных БД

docker compose down -v

## Структура проекта

```bash
library_2.0/
├── .dockerignore           # Игнорируемые файлы для Docker
├── .env.example            # Пример переменных окружения
├── .gitignore              # Игнорируемые файлы для Git
├── docker-compose.yml      # Docker оркестрация
├── Dockerfile              # Сборка образа
├── README.md               # Документация
├── requirements.txt        # Зависимости Python
└── app/
    ├── __init__.py
    ├── main.py             # Точка входа
    ├── config.py           # Конфигурация
    ├── database.py         # Подключение к БД
    ├── exceptions.py       # Обработчики ошибок
    ├── models/             # SQLAlchemy модели
    │   ├── __init__.py
    │   ├── author.py       # Модель автора
    │   ├── book.py         # Модель книги
    │   └── issue.py        # Модель выдачи
    ├── schemas/            # Pydantic схемы
    │   ├── __init__.py
    │   ├── author.py       # Схемы автора
    │   ├── book.py         # Схемы книги
    │   └── issue.py        # Схемы выдачи
    ├── services/           # Бизнес-логика
    │   ├── __init__.py
    │   ├── authors.py      # Логика авторов
    │   ├── books.py        # Логика книг
    │   └── issues.py       # Логика выдач
    └── routers/            # API эндпоинты
        ├── __init__.py
        ├── authors.py      # /authors/*
        ├── books.py        # /books/*
        └── issues.py       # /issues/*



