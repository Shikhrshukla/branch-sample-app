#!/bin/bash
set -e

# Run migrations
alembic upgrade head || true

# Seed data (idempotent — won't duplicate)
python scripts/seed.py || true

# Start the actual API server
gunicorn -b 0.0.0.0:8000 wsgi:app

