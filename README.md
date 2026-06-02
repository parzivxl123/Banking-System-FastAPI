<div align="center">

# 🏦 Banking System API

**A production-ready banking backend built with FastAPI, SQLAlchemy, and JWT authentication.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=flat-square)](https://sqlalchemy.org/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://mysql.com/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-blue?style=flat-square&logo=pytest)](https://pytest.org/)

A complete banking solution featuring **user management**, **fund transfers**, **deposits**, **withdrawals**, and **comprehensive transaction history** — all secured with stateless JWT authentication and backed by a robust relational database.

</div>

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Authentication Guide](#authentication-guide)
- [Running Tests](#running-tests)
- [Interactive Documentation](#interactive-documentation)
- [Roadmap](#roadmap)

---

## ✨ Features

| Category | Details |
|----------|---------|
| **🔐 Authentication** | <ul><li>Stateless JWT access tokens</li><li>Token version invalidation (force logout)</li><li>Protected routes via dependency injection</li></ul> |
| **👤 User Management** | <ul><li>User registration and updates</li><li>Bcrypt password hashing</li><li>Real-time account balance tracking</li><li>User lookup by ID or username</li></ul> |
| **💸 Transactions** | <ul><li>Transfer funds between accounts</li><li>Self-transfer prevention</li><li>Atomic balance updates</li><li>Complete transaction history</li></ul> |
| **🏧 Deposits & Withdrawals** | <ul><li>Deposit funds to account</li><li>Withdraw with balance validation</li><li>Separate history for each operation</li></ul> |

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) — Modern, fast web framework |
| **ORM** | [SQLAlchemy](https://sqlalchemy.org/) — Flexible database abstraction |
| **Validation** | [Pydantic v2](https://docs.pydantic.dev/) — Data validation & serialization |
| **Authentication** | `python-jose` (JWT) + `passlib` (bcrypt) — Secure token & password management |
| **Database** | MySQL — Production-grade relational database |
| **Server** | Uvicorn (ASGI) — High-performance async server |
| **Testing** | Pytest + HTTPX — Comprehensive test suite |
| **Language** | Python 3.10+ |

---

## 📁 Project Structure

```
banking-system-fastapi/
│
├── bankingsys.py               # Main application entry point
├── models.py                   # SQLAlchemy ORM models
├── schemas.py                  # Pydantic request/response schemas
├── database.py                 # Database configuration & session management
│
├── test_bankingsys.py          # Complete test suite
│
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **MySQL Server** (local or remote)
- **pip** (Python package manager)

### 1. Clone the Repository

```bash
git clone https://github.com/parzivxl123/Banking-System-FastAPI.git
cd Banking-System-FastAPI
```

### 2. Create & Activate Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows
.venv\Scripts\activate

# Activate on macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database Connection

Edit `database.py` and update your MySQL connection string:

```python
DATABASE_URL = "mysql+pymysql://root:yourpassword@localhost/banking_system"
```

**Create the database:**

```sql
CREATE DATABASE banking_system;
```

### 5. Run the Application

SQLAlchemy automatically creates all required tables on startup.

```bash
uvicorn bankingsys:app --reload
```

✅ **Server is running at:** `http://127.0.0.1:8000`  
📚 **Interactive docs:** `http://127.0.0.1:8000/docs`

---

## 🔌 API Reference

All protected endpoints require a valid JWT token in the `Authorization` header.

### 🔐 Authentication

| Method | Endpoint | Description | Protected |
|--------|----------|-------------|:---------:|
| `POST` | `/login` | Get JWT access token | ❌ |

### 👤 Users

| Method | Endpoint | Description | Protected |
|--------|----------|-------------|:---------:|
| `POST` | `/users` | Register a new user | ❌ |
| `GET` | `/users` | Get current user profile & balance | ✅ |
| `PUT` | `/users` | Update user information | ✅ |

### 💸 Transactions

| Method | Endpoint | Description | Protected |
|--------|----------|-------------|:---------:|
| `POST` | `/transactions` | Transfer funds to another user | ✅ |
| `GET` | `/transactions/history` | View all transfers (sent & received) | ✅ |

### 🏦 Deposits

| Method | Endpoint | Description | Protected |
|--------|----------|-------------|:---------:|
| `POST` | `/deposit` | Deposit funds into account | ✅ |
| `GET` | `/deposit/history` | View deposit history | ✅ |

### 💳 Withdrawals

| Method | Endpoint | Description | Protected |
|--------|----------|-------------|:---------:|
| `POST` | `/withdrawal` | Withdraw funds from account | ✅ |
| `GET` | `/withdrawal/history` | View withdrawal history | ✅ |

---

## 🔑 Authentication Guide

### Step 1: Login & Get Token

```bash
curl -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "John12345"
  }'
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Step 2: Use Token for Protected Requests

```bash
curl -X GET "http://127.0.0.1:8000/users" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Step 3: Transfer Funds

```bash
curl -X POST "http://127.0.0.1:8000/transactions" \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_username": "alice",
    "amount": 250.00
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| `401 Unauthorized` | Missing or invalid authentication token |
| `400 Bad Request` | Invalid request data (e.g., self-transfer) |
| `404 Not Found` | User or resource not found |
| `422 Unprocessable Entity` | Insufficient balance or validation error |
| `500 Internal Server Error` | Database or server error |

---

## ✅ Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_bankingsys.py

# Run specific test
pytest test_bankingsys.py::test_login_success
```

**Test Coverage Includes:**

- ✅ User registration and profile management
- ✅ Login and token generation
- ✅ Token validation and expiration
- ✅ Fund transfers with validation
- ✅ Deposit and withdrawal operations
- ✅ Transaction history retrieval

---

## 📚 Interactive Documentation

FastAPI auto-generates beautiful, interactive API documentation.

| Documentation | URL |
|---------------|-----|
| **Swagger UI** | `http://127.0.0.1:8000/docs` |
| **ReDoc** | `http://127.0.0.1:8000/redoc` |
| **OpenAPI Schema** | `http://127.0.0.1:8000/openapi.json` |

Test all endpoints directly from your browser with built-in authentication!

---

## 🗺 Roadmap

- [x] Password reset via email (SMTP)
- [ ] Pagination for history endpoints
- [ ] Structured logging (JSON format)
- [x] Docker + `docker-compose` setup
- [ ] Rate limiting (per user, per endpoint)
- [ ] Alembic database migrations
- [ ] Refresh token support
- [ ] Deployment guide (Railway, Render, or VPS)

---

## 👤 Author

**Parzival** — Built with FastAPI and SQLAlchemy  

---

<div align="center">
  <sub>If this project was helpful, please consider giving it a ⭐ on GitHub!</sub>
</div>