#!/usr/bin/env bash
# Build and start the whole stack, then wait until the API reports healthy.
set -euo pipefail

cd "$(dirname "$0")/.."

docker compose up -d --build --wait

echo "ServiceWatch is up:"
docker compose ps
echo "API docs: http://localhost:8000/docs"
