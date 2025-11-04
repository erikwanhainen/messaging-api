# Messages REST API

## Description

REST API for sending, retrieving and deleting messages. It uses a PostgreSQL database to store messages.

## Requirements

- Docker and Docker Compose
- Python 3.11 (for local development without Docker)

## Usage

### With Docker

Build and run the API and database
```bash
docker compose up --build
```

The API will be availble at 
```
http://localhost:8000
```

Notes:
- docker compose creates two containers:
    - `db`: postgres 15
    - `api`: the actual API
- Alembic migrations will run automatically before starting the API.


Stop and remove containers
```bash
# Stop and remove containers
docker compose down

# Stop and remove containers and DB volume
docker compose down -v
```

### Without Docker

#### 1. Set up DB

Start DB with docker compose
```bash
docker compose up db --build
```

Or if you run another DB, set correct env vars

```bash
export POSTGRES_USER=my_user
export POSTGRES_PASSWORD=my_pass
export POSTGRES_DB=my_db
export POSTGRES_HOST=my_host
export POSTGRES_PORT=my_port
```

#### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3 Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run Alembic migrations

```bash
alembic upgrade head
```


#### 5. Start the API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```


### Running tests

Requires DB and virtual environment

```bash
pytest
```


## API endpoints

See openapi documentation for full details

```
http://localhost:8000/docs
```

### Health
- `GET /health` Checks if the API and database are running.

### Messages
- `POST /messages/`Send a new message to a recipient.

- `GET /messages/` Retrieve all messages for a recipient. Pagination and sorting via query parameters:

- `GET /messages/unread/` Retrieve unread messages for a recipient. Pagination and sorting via query parameters:

- `PATCH /messages/mark-read` Mark messages as read by ids

- `DELETE /messages/{message_id}` Delete a single message by id

- `DELETE /messages/bulk` Delete multiple messages by ids



## Implementation 

### Tools used
- **FastAPI**: for building the REST API.
- **SQLModel**: ORM for database access and defining models.
- **Pydantic**: data validation and serialization.
- **Alembic**: database migrations.
- **Uvicorn** ASGI web server

### Design

#### Key design principles

- Stateless API design
    - Enables horizontal scaling
- Per request database sessions
    - Enables concurrent handling
- Idempotency

#### Code structure:
- `src/api/`: Handles HTTP requests and responses
- `src/services/`: Contains the business logic
- `src/repositories/`: Handles database operations


### Improvments

#### Redundancy and Scalability
- Scale API horizontally behind a load balancer
- Rate limit middleware
- DB connection pooling
- DB read replicas
- Cache layer
- Retry logic

#### Concurrency
- Currenlty synchronous endpoints with multiple workers. For higher concurrency, make endpoints async and use async database driver.
