# Student REST API

A simple Student CRUD REST API built using **Python**, **Flask**, and **SQLite** as part of the **One2N SRE Bootcamp**.

This project follows REST API best practices and demonstrates API versioning, logging, validation, error handling, database migrations, environment variable configuration, and automated testing.

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
- Unit Testing using Pytest

---

## Project Structure

```
student-rest-api/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   ├── health.py
│   ├── logger.py
│   └── error_handlers.py
│
├── migrations/
├── tests/
├── postman/
├── instance/
├── requirements.txt
├── .env
├── .env.example
├── run.py
├── README.md
└── Makefile
```

---

## Tech Stack

- Python 3.14
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- Pytest
- Postman

---

## Prerequisites

- Python 3.14+
- Git
- Virtual Environment

---

## Local Setup

Clone the repository

```bash
git clone <repository-url>
```

Navigate into the project

```bash
cd student-rest-api
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```powershell
.\venv\Scripts\Activate.ps1
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

Example:

```
DATABASE_URL=sqlite:///students.db
SECRET_KEY=your-secret-key
```

---

## Database Migration

Initialize database

```bash
flask db upgrade
```

---

## Run the Application

```bash
python run.py
```

Server runs on

```
http://127.0.0.1:5000
```

---

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

## Running Tests

Run all tests

```bash
python -m pytest -v
```

---

## Postman Collection

Import the Postman collection from the `postman/` folder.

---

## Future Improvements

- Docker Support
- CI/CD Pipeline
- Kubernetes Deployment
- Monitoring with Prometheus & Grafana
- Helm Charts
- ArgoCD Deployment

---

## Author

Developed as part of the One2N SRE Bootcamp.