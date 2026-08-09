# Job Tracker API

A REST API for managing job applications built with FastAPI and PostgreSQL, featuring JWT authentication, database migrations, automated tests, and Docker support.

## Features

* User registration and login
* JWT authentication and password hashing
* User-specific job applications (CRUD operations)
* Search by company or position
* Filter by application status
* Pagination and sorting
* PostgreSQL database with Alembic migrations
* Pytest test suite with 100% core coverage
* Docker and Docker Compose setup
* Swagger / OpenAPI interactive documentation

## Tech Stack

* **Python 3.10**
* **FastAPI**
* **PostgreSQL 16**
* **SQLAlchemy & Alembic**
* **Pydantic**
* **JWT & bcrypt**
* **Pytest**
* **Docker / Docker Compose**

## Project Structure

```text
app/
├── core/         # Configuration, database, authentication, security
├── models/       # SQLAlchemy models
├── repositories/ # Database operations
├── routers/      # API endpoints
├── schemas/      # Request/response schemas
├── services/     # Application logic
└── main.py       # Application entry point

alembic/          # Database migrations
tests/            # Automated tests
Dockerfile
compose.yaml
requirements.txt