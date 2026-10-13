#!/usr/bin/env bash
# Dump the PostgreSQL database to a gzipped file in ./backups (or $1).
set -euo pipefail

cd "$(dirname "$0")/.."

BACKUP_DIR="${1:-backups}"
KEEP="${KEEP:-7}"   # how many latest backups to keep
STAMP="$(date +%Y%m%d-%H%M%S)"
FILE="${BACKUP_DIR}/servicewatch-${STAMP}.sql.gz"
TMP="${FILE}.tmp"

mkdir -p "$BACKUP_DIR"
# If anything below fails, never leave a partial file behind.
trap 'rm -f "$TMP"' EXIT

# Credentials come from the container's own environment, so nothing is hardcoded here.
# pipefail makes the script fail if pg_dump fails, even though gzip succeeds.
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists' \
  | gzip > "$TMP"

# Sanity check: a valid dump contains our schema (an empty gzip is ~20 bytes, not 0).
if ! gunzip -c "$TMP" | grep -q "CREATE TABLE public.targets"; then
  echo "Backup failed: dump does not contain expected tables" >&2
  exit 1
fi

mv "$TMP" "$FILE"

# Rotation: remove everything except the newest $KEEP backups.
ls -1t "$BACKUP_DIR"/servicewatch-*.sql.gz | tail -n +"$((KEEP + 1))" | xargs -r rm --

echo "Backup written: $FILE ($(du -h "$FILE" | cut -f1))"
