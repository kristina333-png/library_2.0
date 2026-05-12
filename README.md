# Library Service API

Бэкенд-сервис для управления библиотекой.


## Технологии

- Python 3.11
- FastAPI
- PostgreSQL 15
- SQLAlchemy 2.0 (async)
- Docker / Docker Compose
- Pydantic

## Структура проекта
'''
library_2.0/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── app/
├── init.py
├── main.py
├── config.py
├── database.py
├── exceptions.py
├── models/
│ ├── init.py
│ ├── author.py
│ ├── book.py
│ └── issue.py
├── schemas/
│ ├── init.py
│ ├── author.py
│ ├── book.py
│ └── issue.py
├── services/
│ ├── init.py
│ ├── authors.py
│ ├── books.py
│ └── issues.py
└── routers/
├── init.py
├── authors.py
├── books.py
└── issues.py'''

## Быстрый старт

### Запуск

```bash
docker compose up --build
