# DevOps Intern Take-Home Assignment [Branch]

This project is an end-to-end DevOps implementation for Branch’s Loan API. It's converting a laptop-only microloan service into a production-grade, containerized application with multi-environment Docker setups, secure HTTPS ingress, PostgreSQL persistence, automated CI/CD pipelines, and full operational visibility.

---

# A simple architecture diagram showing how the components connect
<img width="1007" height="548" alt="Screenshot from 2025-11-28 22-09-42" src="https://github.com/user-attachments/assets/2b088703-960e-44b9-912a-ff49ced9327a" />

---

<<<<<<< Updated upstream
=======
# A simple architecture diagram showing how the components connect
<img width="1007" height="548" alt="Screenshot from 2025-11-28 22-09-42" src="https://github.com/user-attachments/assets/2b088703-960e-44b9-912a-ff49ced9327a" />

---

>>>>>>> Stashed changes
# 1. Run the application locally (step-by-step instructions)

## Prerequisites
- Docker & Docker Compose
- `OpenSSL / mkcert` installed (for HTTPS)
- Domain mapped in `/etc/hosts`
```
127.0.0.1  branchloans.com
```
- Clone the Repositry **[Private Repositry]**
```
git clone https://Shikhrshukla:<GITHUB_TOKEN>@github.com/Shikhrshukla/branch-sample-app.git
cd branch-sample-app
```

## Step 1 - Generate local HTTPS certificates (mkcert)

Inside `nginx/ssl/`:

```
<<<<<<< Updated upstream
cd nginx
mkdir ssl
cd ssl
=======
cd nginx/ssl
>>>>>>> Stashed changes
mkcert branchloans.com
mv branchloans.com.pem branchloans.crt
mv branchloans.com-key.pem branchloans.key
cd ../..
```

## Step 2 - Start services

Development:

```
docker compose build --no-cache api
docker compose up -d
```
>Retry this cmd if any container fails

Stop containers:

```
docker compose down -v
```

## Step 3 - Test your API


### Test this on your Browser

`https://branchloans.com/api/loans` and `https://branchloans.com/health`

```
curl -k https://branchloans.com/health
curl -k https://branchloans.com/api/loans
```
<<<<<<< Updated upstream
> Retry this cmd in some time.
> This is secure but, it will show that the CA is not valid / Unknown issuer

<img width="1312" height="604" alt="image" src="https://github.com/user-attachments/assets/4fe5106c-6759-4f05-9491-c1fe2c5819a1" />
<img width="826" height="342" alt="image" src="https://github.com/user-attachments/assets/a478780d-7bd3-4f15-9382-a3022c4a14df" />
=======
and,
```
curl -k https://branchloans.com/api/loans
```
>>>>>>> Stashed changes

---

# 2. Switch between different environments (dev/staging/production)

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
ENV_FILE=.env.dev docker compose build --no-cache api
ENV_FILE=.env.dev docker compose up -d
```
#### Test (this will show the env details)
``` 
docker compose exec api env
```

### Staging
```
ENV_FILE=.env.staging docker compose build --no-cache api
ENV_FILE=.env.staging docker compose up -d
```
#### Test (this will show the env details)
``` 
docker compose exec api env
```

### Production
```
ENV_FILE=.env.prod docker compose build --no-cache api
ENV_FILE=.env.prod docker compose up -d
```
#### Test (this will show the env details)
``` 
docker compose exec api env
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

## Diagram
<img width="2816" height="1536" alt="Gemini_Generated_Image_m0awpym0awpym0aw" src="https://github.com/user-attachments/assets/cadff97d-22f7-4cdf-ab8a-3ce7c4c2a3ed" />

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

# 8. Design Decisions:

## Document why you chose certain approaches
- Chose `Docker + Compose` to ensure identical environments across dev, staging, and production.
- Used `Nginx for HTTPS` termination because it is lightweight and easy to configure.
- Added entrypoint scripts to automate migrations and seeding to remove manual steps.
- Implemented multi-environment `.env` files to separate credentials, logging, and resource usage.
- Used GitHub Actions because it integrates natively with GitHub and supports Docker workflows well.

## Trade-offs
- `Docker Compose` not as powerful as `Kubernetes` for autoscaling, Compose is simpler and faster for an internship task.
- Running migrations automatically on container start is convenient but not ideal for large production databases.
- Using `mkcert or OpenSSL for SSL` is good for local development but not for real certificates in production.

## What I Would Improve With More Time
- Add `Prometheus + Grafana` for metrics.
- Add proper secrets management using `Vault`.
- Move to Kubernetes (Helm/Terraform) for autoscaling and robust resource enforcement.
- Automated DB backups, restore tests, and retention policies.

---

# 9. Troubleshooting

## Common Issues
- **500 error on /api/loans:** Migrations or seed did not run → fix entrypoint or check DB connection.
- **Nginx showing bad gateway:** API container not healthy → check docker compose logs api.
- **Certificate errors:** mkcert not installed or wrong domain in /etc/hosts.
- **DB connection errors:** Wrong password in .env or Postgres container not fully healthy.
- **Compose warning:** version is obsolete, so remove the top-level version: "3.9" line from docker-compose.yml.

## How to Check if Everything Is Running Correctly
- **Check container status:** docker ps
- **View API logs:** docker compose logs api
- **Verify DB is healthy:** docker compose exec db pg_isready
- **Test health endpoint:** `curl -k https://branchloans.com/health` and `curl -k https://branchloans.com/api/loans`

---

# 10. License
This project is for assessment and demonstration purposes only.
