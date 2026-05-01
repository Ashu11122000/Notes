# Notes App Backend

---

## Overview

This project is a **production-ready RESTful backend** built using **FastAPI**.
It provides a secure and scalable system for managing personal notes with authentication, authorization, and clean architecture.

The application demonstrates real-world backend practices including:

* JWT authentication
* Role-based access control
* Database integration with PostgreSQL
* Docker containerization
* API documentation
* Unit testing

---

## Key Features

### Authentication & Authorization

* User registration and login
* JWT-based authentication
* Role-based access control (RBAC)

### Notes Management

* Create, read, update, delete notes (CRUD)
* Users can only access their own notes

### Dockerized Setup

* Fully containerized using Docker & Docker Compose
* Consistent environment across systems

### API Documentation

* Swagger UI → `/docs`
* ReDoc → `/redoc`

### Testing

* Pytest-based test suite
* Covers authentication & notes APIs

### Google OAuth (Optional)

* Login via Google account using Authlib

---

## Project Goal

To build a **clean, scalable, production-like backend system** using best practices:

* Separation of concerns
* Secure authentication
* Modular architecture
* Containerized deployment

---

## Tech Stack

| Category         | Technology        |
| ---------------- | ----------------- |
| Framework        | FastAPI           |
| Database         | PostgreSQL        |
| ORM              | SQLAlchemy        |
| Auth             | JWT (python-jose) |
| Hashing          | Passlib (bcrypt)  |
| Containerization | Docker            |
| Testing          | Pytest            |
| API Client       | Postman           |

---

## Architecture Overview

```
Client → API Routes → Dependencies → Services → Database → Response
```

---

## Project Structure

```
app/
├── main.py
│
├── core/
│   ├── config.py
│   ├── security.py
│
├── db/
│   ├── session.py
│   ├── base.py
│
├── models/
│   ├── user.py
│   ├── note.py
│
├── schemas/
│   ├── user.py
│   ├── note.py
│   ├── token.py
│
├── api/
│   ├── deps.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── note.py
│
├── services/
│   ├── user_service.py
│   ├── note_service.py
│
├── tests/
│   ├── test_auth.py
│   ├── test_notes.py
│
.env
requirements.txt
Dockerfile
docker-compose.yml
README.md
```

---

## Local Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run the App

```bash
uvicorn app.main:app --reload
```

---

### 4. Open API Docs

```
http://127.0.0.1:8000/docs
```

---

## Docker Setup

### Build & Run

```bash
docker compose up --build
```

### Run in background

```bash
docker compose up -d
```

### Stop containers

```bash
docker compose down
```

---

## Run Tests

```bash
pytest
```

---

## API Endpoints

### Auth

| Method | Endpoint         | Description      |
| ------ | ---------------- | ---------------- |
| POST   | `/auth/register` | Register user    |
| POST   | `/auth/login`    | Login user       |
| GET    | `/auth/me`       | Get current user |

---

### Notes

| Method | Endpoint      | Description   |
| ------ | ------------- | ------------- |
| POST   | `/notes`      | Create note   |
| GET    | `/notes`      | Get all notes |
| GET    | `/notes/{id}` | Get note      |
| PUT    | `/notes/{id}` | Update note   |
| DELETE | `/notes/{id}` | Delete note   |

---

## Authentication Flow

```
Client → Login → JWT Token
        ↓
Protected Route → Token Validation → User Access
```

* Passwords hashed using bcrypt
* JWT token contains user identity
* Token required for protected routes

---

## Notes Flow

```
Request → Route → Service → DB → Response
```

* Ownership enforced at service layer
* Users can only access their own notes

---

## Important Notes

* `owner_id` is used instead of `user_id` in database
* Pydantic V2 uses `ConfigDict` instead of `Config`
* Docker does NOT generate requirements (only installs)

---

## Pagination (Concept & Usage)

Pagination helps in efficiently handling large datasets by returning results in smaller chunks instead of loading everything at once.

### How it works?

```bash
GET /notes?page=1&limit=10
```

* `page` → Page number (starts from 1)
* `limit` → Number of records per page

### Internal Logic

```python
skip = (page - 1) * limit
```

* Page 1 → skip = 0
* Page 2 → skip = 10
* Page 3 → skip = 20

### Example Response

```json
[
  {
    "id": 1,
    "title": "My Note",
    "content": "Hello World",
    "owner_id": 1,
    "created_at": "2026-05-01T10:00:00",
    "updated_at": null
  }
]
```

### Benefits

* Improves performance
* Reduces server load
* Better user experience for large datasets

* Note: Pagination can be easily re-enabled in the API by adding `page` and `limit` query parameters in the `/notes` route.

---

## Testing

This project uses **Pytest** to ensure the correctness of core functionalities.

### Run Tests

```bash
pytest
```

---

### Test Coverage

#### Authentication Tests

* User registration (`/auth/register`)
* User login (`/auth/login`)
* JWT token generation and validation

#### Notes Tests

* Create note (`POST /notes`)
* Get notes (`GET /notes`)
* Authorization using Bearer token
* Ownership validation

---

### Testing Approach

* Uses `TestClient` from FastAPI
* Simulates real API requests
* Tests both success and failure cases
* Ensures authentication is required for protected routes

---

### Example Test Flow

```bash
Register → Login → Get Token → Access Protected Route
```

---

### Why Testing matters?

* Prevents regressions
* Ensures API reliability
* Validates authentication & authorization logic
* Helps maintain production-ready code quality

---

## Final Status

* All tests passing
* Fully functional authentication system
* Secure notes management
* Dockerized backend
* Clean architecture

---


## Postman Collection

This collection helps you test all API endpoints of the Notes Backend easily using Postman.

---

### Import Collection

1. Open **Postman**
2. Click **Import**
3. Select **Raw Text**
4. Paste the JSON below
5. Click **Import**

---

### Base URL

```bash
http://127.0.0.1:8000
```


---

### Collection JSON

```json
{
  "info": {
    "name": "Notes App Backend",
    "_postman_id": "12345-abcde-67890",
    "description": "Postman collection for Notes App",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://127.0.0.1:8000"
    },
    {
      "key": "token",
      "value": ""
    }
  ],
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Register User",
          "request": {
            "method": "POST",
            "header": [],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"test@example.com\",\n  \"password\": \"password123\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            },
            "url": "{{base_url}}/auth/register"
          }
        },
        {
          "name": "Login User",
          "request": {
            "method": "POST",
            "header": [],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"test@example.com\",\n  \"password\": \"password123\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            },
            "url": "{{base_url}}/auth/login"
          }
        },
        {
          "name": "Get Current User",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "url": "{{base_url}}/auth/me"
          }
        }
      ]
    },
    {
      "name": "Notes",
      "item": [
        {
          "name": "Create Note",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"title\": \"My Note\",\n  \"content\": \"Hello World\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            },
            "url": "{{base_url}}/notes"
          }
        },
        {
          "name": "Get All Notes",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "url": "{{base_url}}/notes"
          }
        },
        {
          "name": "Get Note By ID",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "url": "{{base_url}}/notes/1"
          }
        },
        {
          "name": "Update Note",
          "request": {
            "method": "PUT",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"title\": \"Updated Note\",\n  \"content\": \"Updated content\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            },
            "url": "{{base_url}}/notes/1"
          }
        },
        {
          "name": "Delete Note",
          "request": {
            "method": "DELETE",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "url": "{{base_url}}/notes/1"
          }
        }
      ]
    }
  ]
}
```
---