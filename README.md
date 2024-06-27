# Django Customer and Order Service API Documentation

## Introduction

This API provides services for managing customers and orders. It is built using Django and includes the following features:
- Authentication using OpenID Connect
- Data storage with PostgreSQL
- Containerization with Docker
- SMS notifications using Africa's Talking SMS API

The Services is hosted  at http://102.133.146.44/schema/swagger-ui

## Prerequisites

Before you start, ensure you have the following installed:
- Docker


## Getting Started

### Cloning the Repository

```bash
git clone https://github.com/Okemwag/SavannahAssessment.git
cd  SavannahAssessment

```

### Docker Setup

Build and run the Docker containers:

```bash
docker compose up -d --build
```

This command will:
- Build the Docker images for the Django application and PostgreSQL database.
- Run the containers.

### Database Migrations

Run the following command to apply the database migrations:

```bash
docker compose exec backend python manage.py migrate
```

### Creating a Superuser

Create a superuser to access the Django admin interface:

```bash
docker compose exec backend python manage.py createsuperuser
```

### Running Tests  Using Coverage

To run the tests with coverage, use the following command:



```bash

docker compose exec backend python manage.py test

```

This command will execute  tests and collect coverage data.