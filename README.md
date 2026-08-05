# Student REST API

A Student CRUD REST API built using **Python**, **Flask**, **SQLAlchemy**, and **PostgreSQL**, containerized using **Docker** and orchestrated using **Docker Compose** as part of the **One2N SRE Bootcamp**.

The project demonstrates REST API development, database migrations, containerization, Docker Compose, Gunicorn, Makefile automation, logging, testing, and environment variable configuration.
---

## Features

- Create Student
- Get All Students
- Get Student by ID
- Update Student
- Delete Student
- API Versioning (`/api/v1`)
- Health Check Endpoint
- Logging
- Input Validation
- Error Handling
- Database Migrations using Flask-Migrate
- PostgreSQL Database
- Docker Multi-stage Build
- Docker Compose
- Gunicorn Production Server
- Makefile Automation
- Unit Testing using Pytest
---

## Project Structure

```
student-rest-api/
│
├── app/
├── migrations/
├── tests/
├── instance/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── run.py
├── README.md
├── .env
└── .env.example
```

---

## Tech Stack

- Python 3.13
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- PostgreSQL
- Alembic
- Gunicorn
- Docker
- Docker Compose
- GNU Make
- Pytest

---

## Prerequisites

- Docker
- Docker Compose
- GNU Make
- Git

---


## Docker Setup

Build the Docker image

```bash
make build
```

Start the complete development environment

```bash
make up
```

This command automatically:

1. Starts PostgreSQL
2. Waits for PostgreSQL to become ready
3. Builds the REST API image
4. Runs database migrations
5. Starts the API

Check running containers

```bash
make ps
```

View logs

```bash
make logs
```

Stop all services

```bash
make down
```

Clean containers, images and volumes

```bash
make clean
----------
## Database Migration

Database migrations are automatically executed when running:

```bash
make up
```

To execute manually:

```bash
docker compose exec api flask db upgrade
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /healthcheck | Health Check |
| POST | /api/v1/students | Create Student |
| GET | /api/v1/students | Get All Students |
| GET | /api/v1/students/{id} | Get Student |
| PUT | /api/v1/students/{id} | Update Student |
| DELETE | /api/v1/students/{id} | Delete Student |

---

## Run the Application

```bash
make up
```

API

```
http://localhost:5000
```

Health Check

```
http://localhost:5000/healthcheck
```
## Running Tests

Run all tests

```bash
## Running Tests

Using local Python:

```bash
python -m pytest -v
```

Or inside Docker:

```bash
docker compose exec api pytest -v

```

---

## Environment Variables

The application uses the following environment variables:

```text
DATABASE_URL=postgresql+psycopg2://student:student123@db:5432/studentdb
PORT=5000
DEBUG=False
SECRET_KEY=your-secret-key
```
------------

## Postman Collection

Import the Postman collection from the `postman/` folder.

---

## Future Improvements

- GitHub Actions CI/CD Pipeline
- Kubernetes Deployment
- Prometheus Monitoring
- Grafana Dashboards
- Helm Charts
- ArgoCD Deployment
- Terraform Infrastructure Automation

## Make Targets

| Command | Description |
|----------|-------------|
| `make build` | Build Docker image |
| `make up` | Start PostgreSQL, run migrations and start API |
| `make ps` | Show running containers |
| `make logs` | View application logs |
| `make down` | Stop all containers |
| `make clean` | Remove containers, volumes and images |

---

## Author

**Sanket Chikhale**

Developed as part of the One2N SRE Bootcamp to demonstrate REST API development, containerization, database migrations, Docker Compose orchestration, and DevOps automation.
