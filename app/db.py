import os
from sqlmodel import create_engine, Session

POSTGRES_USER = os.getenv("POSTGRES_USER", "fastapi_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "fastapi_pass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "messages_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# TODO for scalability and redundancy
# - configure pooling
# - add read replicas and route read only queries
engine = create_engine(
    DATABASE_URL,
    echo=True,
)


def get_session():
    with Session(engine) as session:
        yield session
