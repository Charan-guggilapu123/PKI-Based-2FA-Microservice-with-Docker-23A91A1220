#!/bin/sh
set -euo pipefail

# Start cron in background to process scheduled tasks
cron

# Run FastAPI app in foreground so container exits on failure
uvicorn app.main:app --host 0.0.0.0 --port 8080
