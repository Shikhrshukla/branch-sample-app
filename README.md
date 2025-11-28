# DevOps Intern Take-Home Assignment

This project is an end-to-end DevOps implementation for Branch’s Loan API. It's converting a laptop-only microloan service into a production-grade, containerized application with multi-environment Docker setups, secure HTTPS ingress, PostgreSQL persistence, automated CI/CD pipelines, and full operational visibility.

> I'll Provide you the `GITHUB_TOKEN`, kindly mail on `shikhar31690.4@gmail.com` 

---

# Architecture Diagram
<img width="2816" height="1536" alt="Gemini_Generated_Image_uzd6fquzd6fquzd6" src="https://github.com/user-attachments/assets/10baecaa-ba71-4156-a132-854b2ca40ebf" />

# 1. Run the Application Locally (Step‑by‑Step)

## Prerequisites
- Docker & Docker Compose
- mkcert installed (for HTTPS)
- Domain mapped in `/etc/hosts`
```
127.0.0.1  branchloans.com
```
- Clone the Repositry
```
git clone https://Shikhrshukla:<GITHUB_TOKEN>@github.com/Shikhrshukla/branch-sample-app.git
cd branch-sample-app
```

## Step 1 - Generate local HTTPS certificates (mkcert)

Inside `nginx/ssl/`:

```
mkcert branchloans.com
mv branchloans.com.pem branchloans.crt
mv branchloans.com-key.pem branchloans.key
```

## Step 2 - Start services

Development:

```
docker compose up -d --build
```

## Step 3 - Test your API

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
- **Database credentials:**
  - Different database usernames & passwords _(devuser, stageuser, produser)_ to isolate environments safely.
- **Log levels:**
  - `Development` → `DEBUG`
  - `Staging` → `INFO`
  - `Production` → `WARNING` _(with optional JSON structured logging)_
- **Persistence settings**
  - `Development` → `PERSIST_DB=false` _(stateless; fast iteration)_
  - `Staging & Production` → `PERSIST_DB=true` _(data survives restarts)_
- **Resource configs (Memory limits are environment-specific):**
  - `Development` → lightweight resources _(256m)_
  - `Staging` → moderate limits _(512m)_
  - `Production` → higher limits _(1g)_ for stable performance

## Commands

### Development
```
ENV_FILE=.env.dev docker compose up -d
```

### Staging
```
ENV_FILE=.env.staging docker compose up -d
```

### Production
```
ENV_FILE=.env.prod docker compose up -d
```

### Stop containers:

```
docker compose down -v
```

---

# 3. Environment Variables (Explained)

| Variable          | Description |
|------------------|-------------|
| `POSTGRES_USER`      | PostgreSQL username for the environment (dev/staging/prod). |
| `POSTGRES_PASSWORD`  | PostgreSQL password, unique per environment for security. |
| `POSTGRES_DB`        | Name of the PostgreSQL database (`microloans`). |
| `DATABASE_URL`       | SQLAlchemy-compatible PostgreSQL connection URI. |
| `POSTGRES_IMAGE`     | PostgreSQL Docker image version (e.g., `postgres:15`). |
| `API_PORT`           | Port where the Flask/Gunicorn API listens (default: `8000`). |
| `API_LOG_LEVEL`      | API log level (`DEBUG`, `INFO`, `WARNING`). |
| `API_LOG_FORMAT`     | Logging format (e.g., `json` for structured logs in production). |
| `PERSIST_DB`         | Whether database data persists across container restarts (`true`/`false`). |
| `PYTHONPATH`         | Ensures `/app` is added to Python module search path. |
| `DB_MEM_LIMIT`       | Memory limit for PostgreSQL container (dev=256m, staging=512m, prod=1g). |
| `API_MEM_LIMIT`      | Memory limit for API container (dev=256m, staging=512m, prod=1g). |
| `ENV_FILE`           | Points to `.env.dev`, `.env.staging`, or `.env.prod` for environment-specific config. |


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
├── nginx/ssl     # TLS Certs
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

# 7. Docker Image Testing (Locallly) 

- Create Network
```
docker network create branch-net
```
- Run postgreSQL DB
```
docker run -d   --name db   --network branch-net   -e POSTGRES_USER=postgres   -e POSTGRES_PASSWORD=postgres   -e POSTGRES_DB=microloans   -p 5433:5432   postgres:15
```
- Run Application with database connection
```
docker run -d   --name branch_api   --network branch-net   -p 8000:8000   -e DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/microloans   shikhrshukla/branch-loans:latest
```
- Verify the Running Containers
```
docker ps
```

>Verify it on Browser `localhost:8000/health` and `localhost:8000/api/loans`
---

# 7. Deployment Notes
- Production uses persistent volumes for PostgreSQL
- App is served over HTTPS through NGINX reverse proxy
- Gunicorn runs behind NGINX for performance & stability
- Multi-environment Compose ensures consistent deployments

---

# 8. License
This project is for assessment and demonstration purposes only.
