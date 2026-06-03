<div align="center">

# 🏦 Banking System API

**A production-ready, enterprise-grade banking backend built with FastAPI, SQLAlchemy, and JWT authentication.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=flat-square)](https://sqlalchemy.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://mysql.com/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC?style=flat-square&logo=pytest)](https://pytest.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com/)

A complete, modular banking solution with **user management**, **fund transfers**, **deposits**, **withdrawals**, **audit logging**, and **comprehensive transaction history** — all secured with stateless JWT authentication, email notifications, and production-ready Docker support.

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Router Architecture](#-router-architecture)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [API Reference](#-api-reference)
- [Authentication Guide](#-authentication-guide)
- [Testing](#-testing)
- [Docker Deployment](#-docker-deployment)
- [Email Configuration](#-email-configuration)
- [Database Schema](#-database-schema)
- [Security Features](#-security-features)
- [Interactive Documentation](#-interactive-documentation)
- [Roadmap](#-roadmap)

---

## ✨ Features

### 🔐 Authentication & Security
- Stateless JWT access tokens with configurable expiry (3000 minutes)
- Token version invalidation system (force logout on password change)
- Protected routes via OAuth2 dependency injection
- Password reset with email verification via SMTP
- Bcrypt password hashing with automatic salt generation

### 👤 User Management
- User registration with validation
- Secure profile updates
- Admin and regular user role-based access control
- User lookup by ID or username
- Secure user deletion with cascade delete rules
- Real-time account balance tracking

### 💸 Fund Transfers
- Transfer funds between user accounts
- Self-transfer prevention
- Atomic balance updates (transaction-safe)
- Receiver validation
- Amount validation (no negative amounts)
- Insufficient balance checks

### 🏧 Deposits & Withdrawals
- Deposit funds to account with validation
- Withdraw funds with balance verification
- Separate history tracking for each operation
- Amount validation and error handling

### 📧 Email Integration
- SMTP-based password reset notifications
- Configurable email settings via `.env`
- UUID-based reset tokens for security
- HTML and plain text email support

### 📊 Audit Logging
- Comprehensive audit trail for sensitive operations
- Track user actions with timestamps
- User ID, action type, and detailed information
- Useful for compliance and debugging

### 🐳 Docker Support
- Complete Docker and Docker Compose setup
- MySQL 8.0 container with persistent volumes
- Multi-container orchestration
- Ready for production deployment

### 🧪 Comprehensive Testing
- 30+ test cases covering all endpoints
- Admin and regular user access control testing
- Balance and validation testing
- Token invalidation and session testing
- Edge case handling

---

## 🛠 Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | 0.136.1 |
| **ORM** | [SQLAlchemy](https://sqlalchemy.org/) | 2.0.49 |
| **Validation** | [Pydantic](https://docs.pydantic.dev/) | 2.13.4 |
| **Authentication** | `python-jose` (JWT) | 3.5.0 |
| **Password Hashing** | `passlib` (bcrypt) | 1.7.4 |
| **Email** | `fastapi-mail` | 1.6.4 |
| **Database** | MySQL | 8.0+ |
| **Database Driver** | PyMySQL | 1.2.0 |
| **Server** | Uvicorn (ASGI) | 0.47.0 |
| **Testing** | Pytest + HTTPX | Latest |
| **Language** | Python | 3.10+ |

---

## 📁 Project Structure

```
Banking-System-FastAPI/
│
├── 📄 bankingsys.py                    # Main FastAPI app entry point
├── 📄 database.py                      # SQLAlchemy setup & DB connection
├── 📄 models.py                        # ORM models (User, Transaction, Deposit, Withdrawal, AuditLog)
├── 📄 schemas.py                       # Pydantic schemas for validation
├── 📄 email_config.py                  # Email/SMTP configuration
├── 📄 utils.py                         # Utility functions (audit logging)
│
├── 📁 routers/                         # Modular API route handlers
│   ├── __init__.py
│   ├── auth.py                         # Login, JWT tokens, password reset
│   ├── users.py                        # User CRUD operations
│   ├── transactions.py                 # Fund transfers & transaction history
│   ├── deposits.py                     # Deposit operations
│   └── withdrawals.py                  # Withdrawal operations
│
├── 🧪 test_bankingsys.py               # Comprehensive pytest test suite (30+ tests)
│
├── 🐳 Dockerfile                       # Docker image configuration
├── 🐳 docker-compose.yml               # Multi-container orchestration
├── 📦 requirements.txt                 # Python dependencies
├── 📝 .gitignore                       # Git ignore rules
├── 📖 README.md                        # This file
└── .env.example                        # Environment variables template
```

---

## 🗂️ Router Architecture

The application uses a **modular router pattern** for clean, maintainable code separation:

### **routers/auth.py** 🔐
Handles all authentication and password management:
- `POST /login` — Authenticate user & get JWT token
- `POST /forgotpassword/` — Request password reset token (sends email)
- `POST /resetpassword/` — Reset password with token (invalidates old tokens)

**Key Features:**
- Token version tracking for session management
- Email-based password recovery
- Automatic token invalidation on password change

### **routers/users.py** 👤
Manages user accounts and admin operations:
- `GET /users/` — List all users (admin only)
- `GET /users/{NumberOfUsers}` — Get limited user list (admin only, max 20)
- `POST /users/` — Create new user (admin only)
- `PUT /users/` — Update own profile
- `DELETE /users/` — Delete user by ID (admin only)

**Key Features:**
- Admin-only endpoints for user management
- Duplicate username/email prevention
- Self-deletion prevention
- Token version increment on profile update

### **routers/transactions.py** 💸
Handles fund transfers between users:
- `POST /transactions/` — Transfer funds to another user
- `GET /transactions/` — View user's transaction history (both sent & received)
- `GET /transanctions/` — View all transactions (admin only)
- `GET /transanctions/{NumberofTransactions}` — View limited transactions (admin only, max 20)

**Key Features:**
- Self-transfer prevention
- Insufficient balance detection
- Atomic database transactions
- Receiver validation
- Transaction status tracking

### **routers/deposits.py** 🏦
Manages deposit operations:
- `POST /deposit/` — Deposit funds to account
- `GET /deposits/` — View deposit history

**Key Features:**
- Amount validation (no negative deposits)
- Automatic balance updates
- Deposit history tracking with timestamps

### **routers/withdrawals.py** 💳
Manages withdrawal operations:
- `POST /withdrawal/` — Withdraw funds from account
- `GET /withdrawal/` — View withdrawal history

**Key Features:**
- Amount validation (no negative withdrawals)
- Insufficient balance prevention
- Withdrawal history with timestamps

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **MySQL Server** 8.0+ (local or remote)
- **pip** (Python package manager)
- **(Optional) Docker & Docker Compose**

### Step 1: Clone the Repository

```bash
git clone https://github.com/parzivxl123/Banking-System-FastAPI.git
cd Banking-System-FastAPI
```

### Step 2: Create & Activate Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows
.venv\Scripts\activate

# Activate on macOS / Linux
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost/banking_system

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production-use-openssl-rand-hex
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=3000

# Email Configuration (for password reset)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_FROM=your-email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
```

### Step 5: Create MySQL Database

```sql
CREATE DATABASE banking_system;
```

Or SQLAlchemy will attempt to auto-create it (requires proper permissions).

### Step 6: Run the Application

```bash
uvicorn bankingsys:app --reload
```

✅ **API Server:** `http://127.0.0.1:8000`  
📚 **Swagger Docs:** `http://127.0.0.1:8000/docs`  
📖 **ReDoc:** `http://127.0.0.1:8000/redoc`  
🔌 **OpenAPI JSON:** `http://127.0.0.1:8000/openapi.json`

---

## 🌍 Environment Variables

### Database Configuration
```env
DATABASE_URL=mysql+pymysql://[username]:[password]@[host]:[port]/[database]
```

**Example:**
```env
DATABASE_URL=mysql+pymysql://root:MySecurePass123@localhost:3306/banking_system
```

### JWT Authentication
```env
SECRET_KEY=your-secret-key-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=3000
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Email Configuration (SMTP)

**Gmail:**
```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=app-password-from-google-account
MAIL_FROM=your-email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
```

**Outlook/Microsoft:**
```env
MAIL_SERVER=smtp.outlook.com
MAIL_PORT=587
```

**Yahoo Mail:**
```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=465
```

---

## 🔌 API Reference

All protected endpoints require a valid JWT token in the `Authorization` header.

### Authentication Endpoints 🔐

| Method | Endpoint | Description | Protected | Admin Only |
|--------|----------|-------------|:---------:|:----------:|
| `POST` | `/login` | Get JWT access token | ❌ | ❌ |
| `POST` | `/forgotpassword/` | Request password reset token | ❌ | ❌ |
| `POST` | `/resetpassword/` | Reset password with token | ❌ | ❌ |

### User Management Endpoints 👤

| Method | Endpoint | Description | Protected | Admin Only |
|--------|----------|-------------|:---------:|:----------:|
| `GET` | `/users/` | List all users | ✅ | ✅ |
| `GET` | `/users/{NumberOfUsers}` | Get limited user list (max 20) | ✅ | ✅ |
| `POST` | `/users/` | Create new user | ✅ | ✅ |
| `PUT` | `/users/` | Update own profile | ✅ | ❌ |
| `DELETE` | `/users/` | Delete user (by userID param) | ✅ | ✅ |

### Transaction Endpoints 💸

| Method | Endpoint | Description | Protected | Admin Only |
|--------|----------|-------------|:---------:|:----------:|
| `POST` | `/transactions/` | Transfer funds to another user | ✅ | ❌ |
| `GET` | `/transactions/` | View user's transaction history | ✅ | ❌ |
| `GET` | `/transanctions/` | View all transactions | ✅ | ✅ |
| `GET` | `/transanctions/{NumberofTransactions}` | View limited transactions (max 20) | ✅ | ✅ |

### Deposit Endpoints 🏦

| Method | Endpoint | Description | Protected | Admin Only |
|--------|----------|-------------|:---------:|:----------:|
| `POST` | `/deposit/` | Deposit funds to account | ✅ | ❌ |
| `GET` | `/deposits/` | View deposit history | ✅ | ❌ |

### Withdrawal Endpoints 💳

| Method | Endpoint | Description | Protected | Admin Only |
|--------|----------|-------------|:---------:|:----------:|
| `POST` | `/withdrawal/` | Withdraw funds from account | ✅ | ❌ |
| `GET` | `/withdrawal/` | View withdrawal history | ✅ | ❌ |

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
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidmVyc2lvbiI6MCwiZXhwIjoxNjc4OTAxMjM0fQ...",
  "token_type": "bearer"
}
```

### Step 2: Use Token for Protected Requests

```bash
curl -X GET "http://127.0.0.1:8000/users/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Step 3: Transfer Funds Between Users

```bash
curl -X POST "http://127.0.0.1:8000/transactions/" \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "RecieverID": 5,
    "TransactionAmount": 250.00
  }'
```

**Response:**
```json
{
  "TransactionId": 1,
  "TransactionAmount": "250.00",
  "RecieverID": 5,
  "SenderID": 1,
  "TransactionStatus": "Done"
}
```

### Step 4: Request Password Reset

```bash
curl -X POST "http://127.0.0.1:8000/forgotpassword/" \
  -H "Content-Type: application/json" \
  -d '{
    "UserEmail": "john@example.com"
  }'
```

User will receive an email with reset token.

### Step 5: Reset Password with Token

```bash
curl -X POST "http://127.0.0.1:8000/resetpassword/" \
  -H "Content-Type: application/json" \
  -d '{
    "Token": "abc12345-uuid-token-from-email",
    "NewPassword": "NewSecurePassword123"
  }'
```

**Response:**
```json
{
  "Password Updated"
}
```

### Error Responses

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Request successful |
| `400 Bad Request` | Invalid data (negative amounts, self-transfer, insufficient balance) |
| `401 Unauthorized` | Missing or invalid authentication token |
| `403 Forbidden` | Insufficient permissions (non-admin accessing admin routes) |
| `404 Not Found` | User or resource not found |
| `409 Conflict` | Duplicate username or email |
| `422 Unprocessable Entity` | Validation error (missing required fields) |
| `500 Internal Server Error` | Database or server error |

---

## 🧪 Testing

The project includes a **comprehensive pytest test suite** with 30+ test cases.

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest test_bankingsys.py

# Run specific test
pytest test_bankingsys.py::test_login
```

### Test Coverage

**Authentication Tests:**
- ✅ Successful login with valid credentials
- ✅ Wrong password handling
- ✅ User not found scenarios
- ✅ Token validation and expiration
- ✅ Token invalidation after password change

**User Management Tests:**
- ✅ User registration (creation)
- ✅ User profile updates
- ✅ Duplicate username prevention
- ✅ Admin-only access control
- ✅ User deletion with validation
- ✅ Self-deletion prevention
- ✅ Empty username validation

**Transaction Tests:**
- ✅ Valid fund transfers
- ✅ Self-transfer prevention
- ✅ Insufficient balance detection
- ✅ Invalid receiver handling
- ✅ Negative amount prevention
- ✅ Transaction history retrieval
- ✅ Admin transaction viewing

**Deposit/Withdrawal Tests:**
- ✅ Valid deposits
- ✅ Negative deposit prevention
- ✅ Valid withdrawals
- ✅ Insufficient balance on withdrawal
- ✅ Negative withdrawal prevention
- ✅ Deposit history retrieval
- ✅ Withdrawal history retrieval
- ✅ Large amount handling
- ✅ Missing field validation

**Access Control Tests:**
- ✅ Non-admin user access denial
- ✅ Non-admin creation prevention
- ✅ Protected route authentication
- ✅ Token requirement validation

---

## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
# Build and start all containers
docker-compose up --build

# Access the API
# http://localhost:8001
# Swagger UI: http://localhost:8001/docs
```

### Docker Configuration Details

**docker-compose.yml** provides:

**MySQL 8.0 Service:**
- Database: `fastapi_banking`
- Root Password: `bankingsys123`
- Port: `3308` (mapped from 3306)
- Persistent volume: `mysql_data:/var/lib/mysql`
- Auto-restart on failure

**FastAPI Application Service:**
- Uvicorn server on port 8000 (mapped to 8001)
- Auto-waits 20 seconds for database startup
- Uses `.env.docker` for configuration
- Depends on database service

### Using Docker Compose with Custom Environment

```bash
# Create .env.docker file
echo "DATABASE_URL=mysql+pymysql://root:bankingsys123@db:3306/fastapi_banking" > .env.docker
echo "SECRET_KEY=your-secret-key-here" >> .env.docker

# Start services
docker-compose up --build
```

### Running Individual Containers

```bash
# Build the image
docker build -t banking-system:latest .

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL=mysql+pymysql://root:bankingsys123@db/fastapi_banking \
  -e SECRET_KEY=your-secret-key \
  banking-system:latest
```

---

## 📧 Email Configuration

### Gmail Setup (Recommended)

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

**Outlook/Microsoft 365:**
```env
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
MAIL_FROM=your-email@outlook.com
MAIL_SERVER=smtp.outlook.com
MAIL_PORT=587
```

**Yahoo Mail:**
```env
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-password
MAIL_FROM=your-email@yahoo.com
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=465
```

**Custom SMTP Server:**
```env
MAIL_USERNAME=your-username
MAIL_PASSWORD=your-password
MAIL_FROM=noreply@yourdomain.com
MAIL_SERVER=mail.yourdomain.com
MAIL_PORT=587
```

---

## 📊 Database Schema

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
  ResetToken VARCHAR(255) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (SenderID) REFERENCES users(UserID) ON DELETE CASCADE,
  FOREIGN KEY (RecieverID) REFERENCES users(UserID) ON DELETE CASCADE,
  INDEX idx_sender (SenderID),
  INDEX idx_receiver (RecieverID)
);
```

### Deposits Table
```sql
CREATE TABLE deposits (
  DepositID INT PRIMARY KEY AUTO_INCREMENT,
  UserID INT NOT NULL,
  Amount DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (UserID) REFERENCES users(UserID) ON DELETE CASCADE,
  INDEX idx_user (UserID)
);
```

### Withdrawals Table
```sql
CREATE TABLE withdrawals (
  WithdrawalID INT PRIMARY KEY AUTO_INCREMENT,
  UserID INT NOT NULL,
  Amount DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (UserID) REFERENCES users(UserID) ON DELETE CASCADE,
  INDEX idx_user (UserID)
);
```

### Audit Logs Table (for compliance & tracking)
```sql
CREATE TABLE audit_logs (
  LogID INT PRIMARY KEY AUTO_INCREMENT,
  UserID INT NOT NULL,
  Action VARCHAR(100) NOT NULL,
  Details TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (UserID) REFERENCES users(UserID) ON DELETE CASCADE,
  INDEX idx_user (UserID),
  INDEX idx_action (Action)
);
```

---

## 🛡️ Security Features

- ✅ **Bcrypt Password Hashing** — Secure password storage with automatic salt generation
- ✅ **JWT Authentication** — Stateless token-based authentication
- ✅ **Token Versioning** — Force logout by incrementing token version on password change
- ✅ **Role-Based Access Control (RBAC)** — Admin vs. regular user permissions
- ✅ **Input Validation** — Pydantic schemas validate all inputs
- ✅ **Database Constraints** — Unique usernames/emails, cascade deletes
- ✅ **Self-Transfer Prevention** — Cannot transfer to own account
- ✅ **Balance Validation** — Prevent negative/insufficient balance operations
- ✅ **Reset Token Security** — UUID-based reset tokens for password recovery
- ✅ **Email Verification** — Password resets sent via verified email
- ✅ **Audit Logging** — Track sensitive operations for compliance
- ✅ **CORS Protection** — Configurable cross-origin resource sharing
- ✅ **SQL Injection Prevention** — SQLAlchemy ORM parameterized queries

---

## 📚 Interactive Documentation

FastAPI auto-generates beautiful, interactive API documentation — no setup needed!

| Documentation | URL | Feature |
|---------------|-----|---------|
| **Swagger UI** | `http://127.0.0.1:8000/docs` | Try all endpoints in browser |
| **ReDoc** | `http://127.0.0.1:8000/redoc` | Clean, readable API docs |
| **OpenAPI Schema** | `http://127.0.0.1:8000/openapi.json` | Machine-readable API spec |

**Test endpoints directly from Swagger UI:**
1. Click on an endpoint to expand it
2. Click "Try it out"
3. Fill in parameters (auto-populated from schema)
4. Click "Execute"
5. View response with status code and body

---

## 🗺 Roadmap

- [x] Password reset via email (SMTP)
- [x] Docker + `docker-compose` setup
- [x] Modular router architecture
- [x] Audit logging system
- [ ] Pagination for history endpoints
- [ ] Structured logging (JSON format)
- [ ] Rate limiting (per user, per endpoint)
- [ ] Alembic database migrations
- [ ] Refresh token support
- [ ] Two-factor authentication (2FA)
- [ ] Transaction notifications via email
- [ ] Dashboard/analytics endpoints
- [ ] API rate limiting and throttling
- [ ] Deployment guides (Railway, Render, VPS)

---

## �� Performance Optimizations

- Connection pooling for database efficiency
- Indexed database columns for fast queries
- Async/await patterns for non-blocking operations
- Efficient JWT validation with caching
- Pagination support for large datasets (in roadmap)

---

## 📝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available for educational and commercial use.

---

## 👤 Author

**Parzival** — Built with FastAPI, SQLAlchemy, and modern web technologies

---

<div align="center">
  <sub>If this project was helpful, please consider giving it a ⭐ on GitHub!</sub>
  
  Made with ❤️ by Parzival
</div>