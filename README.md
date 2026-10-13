# ServiceWatch

Uptime monitoring system for websites and APIs: it checks URLs, measures response time, stores history and notifies about outages.

## Quick start (Docker)

```bash
./scripts/up.sh
```

This builds the image, starts PostgreSQL and the API, and waits until both are healthy.
Open http://localhost:8000/docs for the interactive API.

Optional: `cp .env.example .env` and change the values (compose reads `.env` automatically).

## Run for development (API outside Docker)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

docker compose up -d --wait db       # PostgreSQL on localhost:5434
uvicorn app.main:app --reload
```

The default `DATABASE_URL` matches the compose database. To use another one, export it
first (see `.env.example` for the format).

## Backup and restore

```bash
./scripts/backup.sh                              # writes backups/servicewatch-<timestamp>.sql.gz
./scripts/restore.sh backups/<file>.sql.gz       # asks for confirmation, replaces current data
```

`backup.sh` keeps the 7 newest backups (`KEEP=N` to change) and never leaves a partial file
if the dump fails.

## API

| Method | Path                  | Description           |
|--------|-----------------------|-----------------------|
| GET    | `/health`             | Liveness probe        |
| POST   | `/targets`            | Add a URL to monitor  |
| GET    | `/targets`            | List monitored URLs   |
| POST   | `/targets/{id}/check` | Run an HTTP check now |
| GET    | `/checks`             | Check history         |

## Configuration

| Variable                 | Default                  | Description                                  |
|--------------------------|--------------------------|----------------------------------------------|
| `DATABASE_URL`           | local compose PostgreSQL | SQLAlchemy connection URL                    |
| `CHECK_INTERVAL_SECONDS` | `60`                     | Pause between background check runs          |
| `SCHEDULER_ENABLED`      | `true`                   | Set to `false` to disable background checks  |

## Tests

```bash
pytest
```

Tests use in-memory SQLite, so Docker is not required.
