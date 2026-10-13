# ServiceWatch

Uptime monitoring system for websites and APIs: it checks URLs, measures response time, stores history and notifies about outages.

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

docker compose up -d --wait          # PostgreSQL on localhost:5433
uvicorn app.main:app --reload
```

The default `DATABASE_URL` matches the compose database. To use another one, export it
first (see `.env.example` for the format).

Open http://localhost:8000/docs for the interactive API.

## API

| Method | Path                  | Description           |
|--------|-----------------------|-----------------------|
| GET    | `/health`             | Liveness probe        |
| POST   | `/targets`            | Add a URL to monitor  |
| GET    | `/targets`            | List monitored URLs   |
| POST   | `/targets/{id}/check` | Run an HTTP check now |
| GET    | `/checks`             | Check history         |

## Tests

```bash
pytest
```

Tests use in-memory SQLite, so Docker is not required.
