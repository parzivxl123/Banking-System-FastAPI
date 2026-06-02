<div align="center">

# 🏦 Banking System API

**A production-ready banking backend built with FastAPI, SQLAlchemy, and JWT authentication.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=flat-square)](https://sqlalchemy.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://mysql.com/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC?style=flat-square&logo=pytest)](https://pytest.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com/)

A complete, modular banking solution with **user management**, **fund transfers**, **deposits**, **withdrawals**, and **comprehensive transaction history** — all secured with stateless JWT authentication, email notifications, and Docker support.

</div>

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Authentication Guide](#authentication-guide)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Email Configuration](#email-configuration)
- [Interactive Documentation](#interactive-documentation)
- [Roadmap](#roadmap)

---

## ✨ Features

| Category | Details |
|----------|---------|
| **🔐 Authentication** | <ul><li>Stateless JWT access tokens with configurable expiry</li><li>Token version invalidation system (force logout)</li><li>Protected routes via OAuth2 dependency injection</li><li>Password reset with email verification</li></ul> |
| **👤 User Management** | <ul><li>User registration and profile management</li><li>Bcrypt password hashing with salt</li><li>Real-time account balance tracking</li><li>Admin and regular user roles</li><li>User lookup by ID or username</li><li>Secure user deletion with cascade rules</li></ul> |
| **💸 Transactions** | <ul><li>Transfer funds between user accounts</li><li>Self-transfer prevention</li><li>Atomic balance updates</li><li>Admin transaction history viewing</li><li>User-specific transaction history</li></ul> |
| **🏧 Deposits & Withdrawals** | <ul><li>Deposit funds to account</li><li>Withdraw with balance validation</li><li>Separate history tracking for each operation</li><li>Amount validation and error handling</li></ul> |
| **📧 Email Integration** | <ul><li>SMTP-based password reset notifications</li><li>Configurable email settings via `.env`</li><li>Reset token generation and validation</li></ul> |
| **🐳 Docker Support** | <ul><li>Complete Docker and Docker Compose setup</li><li>MySQL container with persistent volumes</li><li>Multi-container orchestration</li></ul> |

---

## 🛠 Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | 0.136+ |
| **ORM** | [SQLAlchemy](https://sqlalchemy.org/) | 2.0.49 |
| **Validation** | [Pydantic](https://docs.pydantic.dev/) | 2.13.4 |
| **Authentication** | `python-jose` (JWT) + `passlib` (bcrypt) | 3.5.0 + 1.7.4 |
| **Email** | `fastapi-mail` | 1.6.4 |
| **Database** | MySQL | 8.0+ |
| **Database Driver** | PyMySQL | 1.2.0 |
| **Server** | Uvicorn (ASGI) | 0.47.0 |
| **Testing** | Pytest + HTTPX | pytest + httpx |
| **Language** | Python | 3.10+ |

---

## 📁 Project Structure

```
Banking-System-FastAPI/
│
├── 📄 bankingsys.py                    # Main FastAPI app entry point
├── 📄 database.py                      # SQLAlchemy setup & DB connection
├── 📄 models.py                        # ORM models (User, Transaction, Deposit, Withdrawal)
├── 📄 schemas.py                       # Pydantic schemas for validation
├── 📄 email_config.py                  # Email/SMTP configuration
│
├── 📁 routers/                         # Modular API route handlers
│   ├── __init__.py
│   ├── auth.py                         # Login, JWT tokens, password reset
│   ├── users.py                        # User CRUD operations
│   ├── transactions.py                 # Fund transfers & transaction history
│   ├── deposits.py                     # Deposit operations
│   └── withdrawals.py                  # Withdrawal operations
│
├── 🧪 test_bankingsys.py               # Comprehensive pytest test suite
│
├── 🐳 Dockerfile                       # Docker image configuration
├── 🐳 docker-compose.yml               # Multi-container orchestration
├── 📄 docker-comose.yml                # Alternative compose file
├── 📦 requirements.txt                 # Python dependencies
├── 📝 .gitignore                       # Git ignore rules
├── 📖 README.md                        # This file
└── .env.example                        # Environment variables template
```

---

## 🗂️ Router Architecture

The application uses a **modular router pattern** for clean separation of concerns:

### **routers/auth.py**
- `POST /login` — User authentication & token generation
- `POST /forgotpassword/` — Request password reset token
- `POST /resetpassword/` — Reset password with token

### **routers/users.py**
- `GET /users/` — List all users (admin only)
- `GET /users/{NumberOfUsers}` — Get limited user list (admin only)
- `POST /users/` — Create new user (admin only)
- `PUT /users/` — Update own profile
- `DELETE /users/` — Delete user by ID (admin only)

### **routers/transactions.py**
- `GET /transanctions/` — View all transactions (admin only)
- `GET /transanctions/{NumberofTransactions}` — View limited transactions (admin only)
- `POST /transactions/` — Transfer funds between users
- `GET /transactions/` — View user's transaction history

### **routers/deposits.py**
- `POST /deposit/` — Deposit funds to account
- `GET /deposits/` — View deposit history

### **routers/withdrawals.py**
- `POST /withdrawal/` — Withdraw funds from account
- `GET /withdrawal/` — View withdrawal history

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **MySQL Server** 8.0+ (local or remote)
- **pip** (Python package manager)
- **(Optional) Docker & Docker Compose**

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

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost/banking_system

# JWT
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256

# Email Configuration (for password reset)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
```

### 5. Create MySQL Database

```sql
CREATE DATABASE banking_system;
```

Or let SQLAlchemy auto-create it if you have permissions.

### 6. Run the Application

```bash
uvicorn bankingsys:app --reload
```

✅ **API Server:** `http://127.0.0.1:8000`  
📚 **Swagger Docs:** `http://127.0.0.1:8000/docs`  
📖 **ReDoc:** `http://127.0.0.1:8000/redoc`

---

## 🔌 API Reference

All protected endpoints require a valid JWT token in the `Authorization` header.

### 🔐 Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---------:|
| `POST` | `/login` | Get JWT access token | ❌ |
| `POST` | `/forgotpassword/` | Request password reset token | ❌ |
| `POST` | `/resetpassword/` | Reset password with token | ❌ |

### 👤 User Management Endpoints

| Method | Endpoint | Description | Auth | Admin Only |
|--------|----------|-------------|:----:|:----------:|
| `GET` | `/users/` | List all users | ✅ | ✅ |
| `GET` | `/users/{NumberOfUsers}` | Get limited user list | ✅ | ✅ |
| `POST` | `/users/` | Create new user | ✅ | ✅ |
| `PUT` | `/users/` | Update own profile | ✅ | ❌ |
| `DELETE` | `/users/` | Delete user (with userID param) | ✅ | ✅ |

### 💸 Transaction Endpoints

| Method | Endpoint | Description | Auth | Admin Only |
|--------|----------|-------------|:----:|:----------:|
| `POST` | `/transactions/` | Transfer funds to another user | ✅ | ❌ |
| `GET` | `/transactions/` | View user's transaction history | ✅ | ❌ |
| `GET` | `/transanctions/` | View all transactions | ✅ | ✅ |
| `GET` | `/transanctions/{NumberofTransactions}` | View limited transactions | ✅ | ✅ |

### 🏦 Deposit Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|:----:|
| `POST` | `/deposit/` | Deposit funds to account | ✅ |
| `GET` | `/deposits/` | View deposit history | ✅ |

### 💳 Withdrawal Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|:----:|
| `POST` | `/withdrawal/` | Withdraw funds from account | ✅ |
| `GET` | `/withdrawal/` | View withdrawal history | ✅ |

---

## 🔑 Authentication Guide

### Step 1: Login & Get Token

```bash
curl -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=John12345"
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
curl -X GET "http://127.0.0.1:8000/users/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Step 3: Transfer Funds

```bash
curl -X POST "http://127.0.0.1:8000/transactions/" \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "RecieverID": 5,
    "TransactionAmount": 250.00
  }'
```

### Step 4: Request Password Reset

```bash
curl -X POST "http://127.0.0.1:8000/forgotpassword/" \
  -H "Content-Type: application/json" \
  -d '{
    "UserEmail": "john@example.com"
  }'
```

### Step 5: Reset Password with Token

```bash
curl -X POST "http://127.0.0.1:8000/resetpassword/" \
  -H "Content-Type: application/json" \
  -d '{
    "Token": "reset-token-from-email",
    "NewPassword": "NewSecurePassword123"
  }'
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Request successful |
| `400 Bad Request` | Invalid data (negative amounts, self-transfer, etc.) |
| `401 Unauthorized` | Missing or invalid authentication token |
| `403 Forbidden` | Insufficient permissions (non-admin accessing admin routes) |
| `404 Not Found` | User or resource not found |
| `409 Conflict` | Duplicate username or email |
| `422 Unprocessable Entity` | Validation error |
| `500 Internal Server Error` | Database or server error |

---

## 🧪 Testing

The project includes a **comprehensive pytest test suite** covering all API endpoints.

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=.

# Run specific test file
pytest test_bankingsys.py

# Run specific test
pytest test_bankingsys.py::test_login
```

### Test Coverage

- ✅ User registration and authentication
- ✅ Login with valid/invalid credentials
- ✅ User not found scenarios
- ✅ Token validation and expiration
- ✅ Token invalidation after password change
- ✅ User profile updates
- ✅ Deposit operations (valid & invalid amounts)
- ✅ Withdrawal operations (sufficient & insufficient balance)
- ✅ Fund transfers (valid transfers, self-transfer prevention)
- ✅ Invalid receiver handling
- ✅ Transaction history retrieval
- ✅ Admin vs. regular user access control
- ✅ User deletion with permission checks
- ✅ Large amount transactions
- ✅ Missing/invalid field validation

---

## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
# Build and start containers
docker-compose up --build

# Access the API
# http://localhost:8001
```

### Docker Configuration

**docker-compose.yml** sets up:

- **MySQL 8.0 Container**
  - Database: `fastapi_banking`
  - Root Password: `bankingsys123`
  - Port: `3308:3306`
  - Persistent volume: `mysql_data`

- **FastAPI Application Container**
  - Uvicorn server running on port 8000 (mapped to 8001)
  - Auto-waits 20 seconds for DB to be ready
  - Uses `.env.docker` for configuration

### Running Containers Separately

```bash
# Build the image
docker build -t banking-system:latest .

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL=mysql+pymysql://root:bankingsys123@db/fastapi_banking \
  banking-system:latest
```

---

## 📧 Email Configuration

The application supports **SMTP-based email notifications** for password resets.

### Gmail Configuration Example

1. Enable 2-Factor Authentication on your Google Account
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. Add to `.env`:

```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-character-app-password
MAIL_FROM=your-email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
```

### Other SMTP Providers

```env
# Outlook
MAIL_SERVER=smtp.outlook.com
MAIL_PORT=587

# Yahoo Mail
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=465

# Custom SMTP Server
MAIL_SERVER=your-smtp-server.com
MAIL_PORT=587
```

---

## 📚 Interactive Documentation

FastAPI auto-generates interactive API documentation.

| Documentation | URL |
|---------------|-----|
| **Swagger UI** | `http://127.0.0.1:8000/docs` |
| **ReDoc** | `http://127.0.0.1:8000/redoc` |
| **OpenAPI Schema** | `http://127.0.0.1:8000/openapi.json` |

Test all endpoints directly from your browser with authentication support!

---

## 📁 Database Schema

### Users Table
```sql
CREATE TABLE users (
  UserID INT PRIMARY KEY AUTO_INCREMENT,
  UserName VARCHAR(100) UNIQUE NOT NULL,
  UserPassword VARCHAR(300) NOT NULL,
  UserEmail VARCHAR(100) UNIQUE NOT NULL,
  UserBalance DECIMAL(10,2) DEFAULT 0,
  is_Admin BOOLEAN DEFAULT FALSE,
  token_version INT DEFAULT 0,
  ResetToken VARCHAR(255) NULL
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
  TransactionID INT PRIMARY KEY AUTO_INCREMENT,
  SenderID INT NOT NULL,
  RecieverID INT NOT NULL,
  TransactionAmount DECIMAL(10,2) NOT NULL,
  TransactionStatus VARCHAR(50),
  FOREIGN KEY (SenderID) REFERENCES users(UserID) ON DELETE CASCADE,
  FOREIGN KEY (RecieverID) REFERENCES users(UserID) ON DELETE CASCADE
);
```

### Deposits Table
```sql
CREATE TABLE deposits (
  DepositID INT PRIMARY KEY AUTO_INCREMENT,
  UserID INT NOT NULL,
  Amount DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (UserID) REFERENCES users(UserID) ON DELETE CASCADE
);
```

### Withdrawals Table
```sql
CREATE TABLE withdrawals (
  WithdrawalID INT PRIMARY KEY AUTO_INCREMENT,
  UserID INT NOT NULL,
  Amount DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (UserID) REFERENCES users(UserID) ON DELETE CASCADE
);
```

---

## 🛡️ Security Features

- ✅ **Bcrypt Password Hashing** — Secure password storage with salt
- ✅ **JWT Authentication** — Stateless token-based auth
- ✅ **Token Versioning** — Force logout by incrementing token version
- ✅ **Role-Based Access Control** — Admin vs. regular user permissions
- ✅ **Input Validation** — Pydantic schemas for all inputs
- ✅ **Database Constraints** — Unique usernames and emails, cascade deletes
- ✅ **Self-Transfer Prevention** — Cannot transfer to own account
- ✅ **Balance Validation** — Prevent negative/insufficient balance operations
- ✅ **Reset Token Security** — UUID-based reset tokens for password recovery

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

**Parzival** — Built with FastAPI, SQLAlchemy, and Docker

---

## 📝 License

This project is open source and available for educational and commercial use.

---

<div align="center">
  <sub>If this project was helpful, please consider giving it a ⭐ on GitHub!</sub>
</div>