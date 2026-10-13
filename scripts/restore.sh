#!/usr/bin/env bash
# Restore the database from a backup file. This REPLACES current data.
# Usage: scripts/restore.sh backups/servicewatch-YYYYMMDD-HHMMSS.sql.gz
set -euo pipefail

cd "$(dirname "$0")/.."

FILE="${1:-}"
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Usage: $0 <backup.sql.gz>" >&2
  exit 1
fi

read -r -p "This will overwrite the current database with $FILE. Type 'yes' to continue: " ANSWER
if [ "$ANSWER" != "yes" ]; then
  echo "Aborted."
  exit 1
fi

# Stop the API so nothing writes while we restore.
docker compose stop api

gunzip -c "$FILE" \
  | docker compose exec -T db sh -c 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'

docker compose start api
echo "Restore complete."
