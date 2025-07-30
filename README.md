# Recruitment Management System

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python\&style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker\&style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql\&style=flat-square)

This project is a **Python-based recruitment management system** to:

* Manage job vacancies.
* Update and track vacancy status.
* Simulate costs of ongoing vacancies.

---

## Project Structure

* **adapters/** – External services & integrations
* **application/** – Business logic (use cases)
* **domain/** – Core entities and domain models
* **infra/** – Infrastructure (Docker, DB config)
* **migrations/models/** – Database migrations & models
* **tests/** – Unit and integration tests
* **web/** – API and web interface

---

## Requirements

* [Docker](https://www.docker.com/get-started) and Docker Compose
* (Optional) [Make](https://www.gnu.org/software/make/)
* Python 3.12 environment (recommended via Poetry)
* PostgreSQL 15+

---

## Environment Variables

Create a `.env` file at project root with:

```env
APP_MODE=development

POSTGRES_PASSWORD=localpassword
POSTGRES_USER=localuser
POSTGRES_DB=recruitment-database
POSTGRES_HOST=recruitment-management-database
POSTGRES_PORT=5432

POSTGRES_URL=postgresql://localuser:localpassword@recruitment-management-database:5432/recruitment-database
```

---

## Setup and Run

### Install dependencies with Poetry

```bash
poetry install
```

Activate virtual environment (Linux/macOS):

```bash
source .venv/bin/activate
```

### Run API locally

```bash
poetry run python entrypoint.py
```

---

### Using Docker Compose

Start all services (Postgres + API):

```bash
docker compose -f infra/docker/compose.yaml up -d
```

Stop services:

```bash
docker compose -f infra/docker/compose.yaml down
```

---

### Using Makefile (recommended)

Start services:

```bash
make services-up
```

Stop services:

```bash
make services-down
```

Run API in dev mode (auto-reload):

```bash
make dev
```

Run tests (will start services, wait for readiness, run tests, then stop services):

```bash
make test
```

---

## PostgreSQL Information

This project uses **PostgreSQL 15** as the primary database.

### Accessing the database with Docker:

```bash
docker exec -it recruitment-management-database psql -U localuser -d recruitment-database
```

### Default database settings (from `.env`):

* **Host:** `recruitment-management-database` (use `localhost` if running locally without Docker)
* **Port:** `5432`
* **Database:** `recruitment-database`
* **User:** `localuser`
* **Password:** `localpassword`

---

## ORM and Migrations

This project uses:

* **[Tortoise ORM](https://tortoise.github.io/)** – Async Python ORM for database models and queries.
* **[Aerich](https://tortoise.github.io/aerich.html)** – Migration tool integrated with Tortoise ORM.

### Common Aerich commands:

Initialize Aerich (only once, after setting `TORTOISE_ORM`):

```bash
poetry run aerich init -t infra.database.pgdatabase.TORTOISE_ORM
```

Create a new migration:

```bash
poetry run aerich migrate --name <migration_name>
```

Apply migrations:

```bash
poetry run aerich upgrade
```

Rollback last migration:

```bash
poetry run aerich downgrade
```

---

## API Documentation

Access interactive OpenAPI docs at:

```
http://localhost:8000/docs
```

---

## API Documentation Preview

![Swagger UI preview](docs/swagger.png)

---

## CI/CD Pipelines and GitHub Workflows

This project includes GitHub Actions workflows for automated testing on pull requests.
The workflows:

* Start a PostgreSQL service container
* Run database migrations using **Aerich**
* Launch the FastAPI app in the background
* Wait for services to be ready
* Run pytest integration and unit tests

![Workflow preview](docs/workflow.png)

You can find the workflow files in `.github/workflows/` folder.

