<div align="center">

# 🏦 Banking System API

**A production-ready banking backend built with FastAPI, SQLAlchemy, and JWT authentication.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=flat-square)](https://sqlalchemy.org/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://mysql.com/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-blue?style=flat-square&logo=pytest)](https://pytest.org/)

Supports **user management**, **fund transfers**, **deposits**, **withdrawals**, and **full transaction history** — all secured with stateless JWT auth and backed by a relational database.

</div>

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Authentication Guide](#authentication-guide)
- [Running Tests](#running-tests)
- [Interactive Docs](#interactive-docs)
- [Roadmap](#roadmap)

---

## Features

<table>
<tr>
<td width="50%">

**🔐 Authentication**
- Stateless JWT access tokens
- Token version invalidation (force logout)
- Protected routes via dependency injection

**👤 User Management**
- Register and update users
- Bcrypt password hashing
- Account balance tracking
- Lookup users by ID or username

</td>
<td width="50%">

**💸 Transactions**
- Transfer funds between accounts
- Self-transfer prevention
- Atomic balance updates
- Full transaction history

**🏧 Deposits & Withdrawals**
- Deposit funds to your account
- Withdraw with insufficient-balance checks
- Separate history for each operation

</td>
</tr>
</table>

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **ORM** | [SQLAlchemy](https://sqlalchemy.org/) |
| **Validation** | [Pydantic v2](https://docs.pydantic.dev/) |
| **Authentication** | `python-jose` (JWT) + `passlib` (bcrypt) |
| **Database** | MySQL (production) |
| **Server** | Uvicorn (ASGI) |
| **Testing** | Pytest + HTTPX |
| **Language** | Python 3.10+ |

---

## Project Structure

```
banking_system/
│
├── bankingsys.py          # App entry point — routes, startup
├── models.py              # SQLAlchemy ORM models
├── schemas.py             # Pydantic request/response schemas
├── database.py            # DB engine, session factory, Base
│
├── test_bankingsys.py     # Pytest test suite
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- MySQL server running locally (or remotely)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/banking-system-api.git
cd banking-system-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Open `database.py` and set your connection string:

```python
DATABASE_URL = "mysql+pymysql://root:yourpassword@localhost/banking_system"
```

> 💡 Make sure the `banking_system` database exists in MySQL before running. Create it with:
> ```sql
> CREATE DATABASE banking_system;
> ```

### 5. Start the server

SQLAlchemy creates all tables automatically on startup. Just run:

```bash
uvicorn bankingsys:app --reload
```

The API is now live at **`http://127.0.0.1:8000`**.  
Interactive docs are at **`http://127.0.0.1:8000/docs`**.

---

## API Reference

All protected endpoints require a valid JWT in the `Authorization` header.

### 🔐 Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|:----:|
| `POST` | `/login` | Get access token | ❌ |

### 👤 Users

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|:----:|
| `POST` | `/users` | Register a new user | ❌ |
| `GET` | `/users` | Get current user profile & balance | ✅ |
| `PUT` | `/users` | Update user details | ✅ |

### 💸 Transactions

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|:----:|
| `POST` | `/transactions` | Transfer funds to another user | ✅ |
| `GET` | `/transactions/history` | View all outgoing/incoming transfers | ✅ |

### 🏦 Deposits

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|:----:|
| `POST` | `/deposit` | Deposit funds into account | ✅ |
| `GET` | `/deposit/history` | View deposit history | ✅ |

### 💳 Withdrawals

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|:----:|
| `POST` | `/withdrawal` | Withdraw funds from account | ✅ |
| `GET` | `/withdrawal/history` | View withdrawal history | ✅ |

---

## Authentication Guide

### Step 1 — Login and receive a token

```http
POST /login
Content-Type: application/json
```

```json
{
    "username": "john",
    "password": "John12345"
}
```

**Response:**

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

### Step 2 — Authenticate all subsequent requests

```http
GET /users
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 3 — Make a transfer

```http
POST /transactions
Authorization: Bearer eyJ...
Content-Type: application/json
```

```json
{
    "recipient_username": "alice",
    "amount": 250.00
}
```

**Common error responses:**

| Status | Reason |
|--------|--------|
| `401 Unauthorized` | Missing or invalid token |
| `400 Bad Request` | Self-transfer attempted |
| `422 Unprocessable Entity` | Insufficient balance |
| `404 Not Found` | Recipient does not exist |

---

## Running Tests

```bash
# Run the full test suite
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest test_bankingsys.py

# Run a specific test function
pytest test_bankingsys.py::test_login_success
```

The test suite covers:

- ✅ User registration and profile updates
- ✅ Login and token issuance
- ✅ Token validation and rejection
- ✅ Fund transfers (success, self-transfer, insufficient balance)
- ✅ Deposit and withdrawal flows

---

## Interactive Docs

FastAPI generates live, interactive API documentation automatically — no extra setup needed.

| UI | URL |
|---|---|
| **Swagger UI** | `http://127.0.0.1:8000/docs` |
| **ReDoc** | `http://127.0.0.1:8000/redoc` |
| **OpenAPI JSON** | `http://127.0.0.1:8000/openapi.json` |

You can authenticate and test every endpoint directly from the browser.

---

## Roadmap

- [x] Password reset via email (SMTP)
- [x] Pagination for history endpoints
- [ ] Structured logging (JSON format)
- [x] Docker + `docker-compose` setup
- [ ] Rate limiting (per user, per endpoint)
- [ ] Alembic database migrations
- [ ] Refresh token support
- [ ] Deployment guide (Railway, Render, or VPS)

---

## Author

**Parzival** — built with FastAPI and SQLAlchemy.

---

<div align="center">
<sub>If this project helped you, consider giving it a ⭐ on GitHub.</sub>
</div>
