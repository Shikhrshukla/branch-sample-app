# Loan API – Containerized Microloans Service

A production-ready, containerized Flask microloans API using PostgreSQL, Docker, multi‑environment Compose setups, and a full CI/CD pipeline (GitHub Actions).

---

# 1. Run the Application Locally (Step‑by‑Step)

## Prerequisites
- Docker & Docker Compose
- mkcert installed (for HTTPS)
- Domain mapped in `/etc/hosts`

```
127.0.0.1  branchloans.com
```

## Step 1 — Generate local HTTPS certificates (mkcert)

Inside `nginx/ssl/`:

```
mkcert branchloans.com
mv branchloans.com.pem branchloans.crt
mv branchloans.com-key.pem branchloans.key
```

## Step 2 — Start services

Development:

```
docker compose --env-file .env.dev up -d --build
```

Staging:

```
docker compose --env-file .env.staging up -d --build
```

Production:

```
docker compose --env-file .env.prod up -d --build
```

## Step 3 — Test your API

```
curl -k https://branchloans.com/health
```

---

# 2. Switching Between Environments

The application supports:
- **Development** (`.env.dev`)
- **Staging** (`.env.staging`)
- **Production** (`.env.prod`)

Each environment overrides:
- Database credentials
- Log levels 
- Persistence settings 
- Resource configs 

## Commands

### Development
```
docker compose --env-file .env.dev up -d --build
```

### Staging
```
docker compose --env-file .env.staging up -d --build
```

### Production
```
docker compose --env-file .env.prod up -d --build
```

Stop containers:

```
docker compose down
```

---

# 3. Environment Variables (Explained)

| Variable | Description |
|---------|-------------|
| `POSTGRES_USER` | PostgreSQL username |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `POSTGRES_DB` | Database name |
| `DATABASE_URL` | SQLAlchemy DB URI |
| `API_PORT` | Flask/Gunicorn port |
| `API_LOG_LEVEL` | App log level (DEBUG/INFO/WARNING) |
| `PERSIST_DB` | Whether DB should be persistent between restarts |
| `POSTGRES_IMAGE` | PostgreSQL version used |
| `PYTHONPATH` | Ensures `app/` is importable |

---

# 4. CI/CD Pipeline (GitHub Actions)

The pipeline is split into four jobs:

## **1. tests**
- Installs dependencies
- Runs pytest unit tests
- Ensures the app loads and routes exist

## **2. build**
- Builds Docker image using Buildx
- Tags image with `${{ github.sha }}`
- Saves image as artifact

## **3. scan**
- Loads the built Docker image
- Scans image using **Trivy** for vulnerabilities
- Does **not** fail the pipeline on severity (configurable)

## **4. push**
- Runs **only** on `main` branch
- Logs in to Docker Hub
- Pushes image with:
 - `:latest`
 - `:${{ github.sha }}`

---

# 5. Project Structure

```
dummy-branch-app/
│
├── app/         # Flask app
├── alembic/       # DB migrations
├── scripts/       # Seeder
├── nginx/        # HTTPS reverse proxy
├── tests/        # Pytest suite
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── .env.*        # Environment configs
└── README.md
```

---

# 6. Local Testing

Run tests:

```
pytest -q
```

---

# 7. Deployment Notes
- Production uses persistent volumes for PostgreSQL
- App is served over HTTPS through NGINX reverse proxy
- Gunicorn runs behind NGINX for performance & stability
- Multi-environment Compose ensures consistent deployments

---

# 8. License
This project is for assessment and demonstration purposes only.
