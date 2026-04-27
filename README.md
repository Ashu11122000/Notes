# Notes App Backend

---

## Overview

This project is a RESTful backend service built using FastAPI that provides a complete notes management system. It allows users to securely create, manage, and organize notes through wee-structured APIs.
The system is designed with a focus on clean architecture, scalability, and real-world backend practices, including authentication, database integration, containerization, and API documentation.

---

## Key Features

* **Authentication and Authorization**
- Secure user registration and login using JWT-based authentication
- Role-based access control for protected resources

* **Notes Management**
- Create, read, update, and delete notes
- Each user can manage their own data securely

* **Dockerized Setup**
- Full containerized application using Docker and Docker Compose
- Easy local setup and environment consistency

* **API Documentation**
- Auto-generated Swagger UI
- Clear API structure for testing and integration

* **Pagination Support**
- Efficient handling of large datasets using paginated APIs

* **Social Login (Google Auth)**
- Integration for seamless authentication using Google accounts

* **Unit Testing**
- Includes test cases to ensure reliability and correctness of core functionalities.

---

## Project Goal

The goal of this project is to demonstrate the ability to design and implement a production-ready backend system.

* **Clean and modular architecture:** Code is organized into clear, separate parts, where each part has one responsibility.
   - `models/` → database tables (SQLAlchemy)
   - `schemas/` → request/response validation (Pydantic)
   - `api/` → routes (endpoints)
   - `services/` → business logic
   - `db/` → database connection

* **Secure authentication mechanisms:** Only authorized users can access data, and their identity is verified securely.
I will implement:
   - Register/Login APIs
   - JWT tokens
   - Password hashing

* **Containerized deployment:**
Containerization = Packaging of app + all dependencies into one unit (container) so it runs anywhere.
*Without Docker*
- Works on own laptop
- Fails on another system
*With Docker*
- Same environment everywhere

---

## Tech Stack

* **Backend Framework:** `FastAPI`
* **Database:** `PostgreSQL`
* **ORM:** `SQLAlchemy`
* **Authentication:** `JWT`
* **Containerization:** `Docker`
* **Testing:** `Pytest`
* **API Testing:** `Postman`

---

## HLD Flow Architecture

```bash
User → API → Auth → Service → Repository → Database → Response
```

---

## Backend Setup using `uv`

This project uses **uv** (a fast Python package manager) to manage dependencies and virtual environments.

**1. Install `uv`**

```bash
pip install uv
```

---

**2. Create Virtual Environment**

```bash
uv venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

---

**3. Initialize Project**

```bash
uv init
```

---

**4. Install Core Dependencies**

```bash
uv add fastapi sqlalchemy psycopg2-binary python-dotenv pydantic passlib[bcrypt] python-jose[cryptography] alembic pytest httpx email-validator
```

---

**5. Install Optional Dependencies**
*Google OAuth*

```bash
uv add authlib
```

*Pagination Support*

```bash
uv add fastapi-pagination
```

**6. Export Dependencies**

```bash
uv pip freeze > requirements.txt
```

**Installed Packages Overview**

* **FastAPI** → Web framework
* **SQLAlchemy** → ORM for database
* **psycopg2-binary** → PostgreSQL driver
* **Pydantic** → Data validation
* **python-dotenv** → Environment variables
* **passlib[bcrypt]** → Password hashing
* **python-jose** → JWT authentication
* **Alembic** → Database migrations
* **Pytest** → Unit testing
* **httpx** → API testing
* **email-validator** → Email validation
* **Authlib** → Google OAuth
* **fastapi-pagination** → Pagination support 

---

## Project Folder Structure

```
app/
├── main.py                     # Entry point of FastAPI application
│
├── core/
│   ├── config.py              # Application settings & environment variables
│   ├── security.py            # JWT auth & password hashing logic
│
├── db/
│   ├── session.py             # Database engine & session creation
│   ├── base.py                # Base class for SQLAlchemy models
│
├── models/
│   ├── user.py                # User database model
│   ├── note.py                # Note database model
│
├── schemas/
│   ├── user.py                # User request/response schemas
│   ├── note.py                # Note request/response schemas
│   ├── token.py               # JWT token schema
│
├── api/
│   ├── deps.py                # Shared dependencies (DB, auth)
│   ├── routes/
│   │   ├── auth.py            # Authentication routes (login/register)
│   │   ├── notes.py           # Notes CRUD routes
│
├── services/
│   ├── user_service.py        # User-related business logic
│   ├── note_service.py        # Notes business logic (CRUD, pagination)
│
├── tests/
│   ├── test_auth.py           # Tests for authentication APIs
│   ├── test_notes.py          # Tests for notes APIs
│
.env                           # Environment variables
requirements.txt               # Project dependencies
Dockerfile                     # Docker configuration for backend
docker-compose.yml             # Multi-container setup (app + DB)
README.md                      # Project documentation
```

**Architecture Summary**

* **models/** → Database layer (SQLAlchemy)
* **schemas/** → Validation layer (Pydantic)
* **services/** → Business logic layer
* **api/** → Request handling (routes)
* **core/** → Config & security
* **db/** → Database connection

This structure ensures clean, modular, and scalable backend design.

---

## Docker Setup (PostgreSQL + PgAdmin4)

This section describes how to set up PostgreSQL and pgAdmin using Docker.

**1. Pull PostgreSQL Image**

```bash
docker pull postgres:15
```

---

**2. Run PostgreSQL Container**

```bash
docker run --name notes-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD='Ashu11122000@' -e POSTGRES_DB=postgres -p 5432:5432 -d postgres:15
```

Verify container is running:

```bash
docker ps
```

---

**3. Pull pgAdmin Image**

```bash
docker pull dpage/pgadmin4
```

---

**4. Run pgAdmin Container**

```bash
docker run --name pgadmin-container -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=ashu11vats@gmail.com -e PGADMIN_DEFAULT_PASSWORD=Ashu11122000 -d dpage/pgadmin4
```

**5. Access pgAdmin**

Open in browser:

```
http://localhost:5050
```

**6.Connect PostgreSQL in pgAdmin**

Inside pgAdmin → **Register Server**

*General Tab*
* Name: `Local PostgreSQL`

*Connection Tab*
* Host: `host.docker.internal`
* Port: `5432`
* Maintenance DB: `postgres`
* Username: `postgres`
* Password: `Ashu11122000@`

**Final Status**

* PostgreSQL container running 
* pgAdmin container running 
* Connection established 


---

## API Endpoints

* **Authentication**

- POST `/auth/register` → 201 Created  
- POST `/auth/login` → 200 OK  
- POST `/auth/google` → 200 OK  
- GET `/auth/me` → 200 OK  
 
* **User**

- GET `/users/profile` → 200 OK  
- PUT `/users/profile` → 200 OK  
- DELETE `/users/profile` → 204 No Content  

* **Notes**

- POST `/notes` → 201 Created  
- GET `/notes` → 200 OK  
- GET `/notes/{id}` → 200 OK  
- PUT `/notes/{id}` → 200 OK  
- DELETE `/notes/{id}` → 204 No Content  

* **Pagination**

- GET `/notes?page={page}&limit={limit}` → 200 OK  

---

## Authentication Flow
## Pagination explanation
## Tests