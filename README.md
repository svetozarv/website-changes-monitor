Stack: FastAPI, PostgreSQL, Celery Beat


`
# Start a local PostgreSQL container for development
docker run --name uptime_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=uptime_monitor \
  -p 5432:5432 \
  -d postgres:15-alpine
`