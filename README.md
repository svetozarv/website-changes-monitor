Stack:
- FastAPI, Uvicorn, Pydantic
- PostgreSQL, SQLAlchemy, Alembic,
- Redis, Celery,
- Docker, Docker Compose


```
# Start a local PostgreSQL container for development
docker run --name uptime_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=website-changes-monitor \
  -p 5432:5432 \
  -d postgres:15-alpine
```
```
docker run --name uptime_redis \
  -p 6379:6379 \
  -d redis:7-alpine
```


`alembic revision --autogenerate -m "initial_tables"`

`alembic upgrade head`
