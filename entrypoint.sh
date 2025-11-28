#!/bin/sh
set -e

echo "Applying migrations..."
alembic upgrade head || true

echo "Seeding data..."
python scripts/seed.py || true

echo "Starting API..."
exec gunicorn -b 0.0.0.0:8000 wsgi:app
