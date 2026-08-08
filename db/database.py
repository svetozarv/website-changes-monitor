import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")  # db name

# Connection string for a local Docker PostgreSQL instance
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@postgres:{POSTGRES_PORT}/{POSTGRES_DB}"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session for FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
