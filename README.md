# 🏦 BankingSys

**A full-stack banking application — FastAPI backend with a React + Vite frontend.**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com/)

---

## Overview

BankingSys is a full-stack banking application with a FastAPI backend and a React + Vite frontend. It supports user registration with email verification, JWT-authenticated sessions, deposits, withdrawals, peer-to-peer transfers, and a statistics dashboard with charts. The whole stack runs via Docker Compose with a single command.

---

## Features

### Backend
- **JWT authentication** with token versioning — changing your password immediately invalidates all active sessions
- **Account lockout** after 5 consecutive failed login attempts
- **Email verification** on signup; password reset flow via SMTP
- **Deposits, withdrawals, and transfers** with atomic balance updates and self-transfer prevention
- **Analytics endpoints** — lifetime summary (total sent, received, deposited, withdrawn) and month-by-month breakdowns
- **Audit log** for every sensitive action (login, transfers, password resets, email verification)
- **Rate limiting** on auth endpoints via SlowAPI
- **Admin role** with access to user management (create, list, delete)

### Frontend
- React 19 + Vite SPA with client-side routing via React Router
- **Protected routes** — unauthenticated users are redirected to login
- **Dashboard** showing live balance, recent transactions, and quick action buttons
- Dedicated pages for **Deposit**, **Withdrawal**, and **Transfer**
- **Statistics page** powered by Recharts — a money flow bar chart (sent vs. received vs. deposited vs. withdrawn) and a monthly activity line chart
- Sidebar navigation with logout
- Axios instance with a request interceptor that automatically attaches the Bearer token

---

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Backend    | Python 3.10+, FastAPI, SQLAlchemy 2 |
| Database   | MySQL 8.0                           |
| Auth       | JWT (python-jose), bcrypt           |
| Email      | FastAPI-Mail, SMTP                  |
| Frontend   | React 19, Vite, React Router 7      |
| Charts     | Recharts                            |
| HTTP       | Axios                               |
| Testing    | Pytest                              |
| Deployment | Docker, Docker Compose              |

---

## Project Structure

```
.
├── bankingsys.py          # App entry point, CORS middleware, router registration
├── models.py              # SQLAlchemy models: User, Transaction, Deposit, Withdrawal, AuditLog
├── schemas.py             # Pydantic request/response schemas
├── database.py            # Engine + session factory
├── email_config.py        # FastAPI-Mail SMTP config
├── utils.py               # Shared audit log helper
├── routers/
│   ├── auth.py            # Login, email verify, forgot/reset password
│   ├── users.py           # User CRUD (admin-gated), self-registration
│   ├── deposits.py        # Deposit funds + history
│   ├── withdrawals.py     # Withdraw funds + history
│   ├── transactions.py    # Peer-to-peer transfers + history
│   └── analytics.py      # /analytics/summary and /analytics/monthly
├── test_bankingsys.py     # 30+ pytest test cases
├── Dockerfile
├── docker-compose.yml
└── frontend/
    ├── src/
    │   ├── App.jsx                        # Route definitions
    │   ├── pages/
    │   │   ├── Login.jsx
    │   │   ├── Dashboard.jsx
    │   │   ├── Deposit.jsx
    │   │   ├── Withdrawal.jsx
    │   │   ├── Transfer.jsx
    │   │   └── Statistics.jsx
    │   ├── components/
    │   │   ├── Sidebar.jsx
    │   │   ├── BalanceCard.jsx
    │   │   ├── TransactionHistory.jsx
    │   │   ├── MoneyFlowCharts.jsx
    │   │   ├── MonthlyActivityChart.jsx
    │   │   ├── ActionButtons.jsx
    │   │   ├── TiltCard.jsx
    │   │   └── ProtectedRoute.jsx
    │   └── services/api.js               # Axios instance + auth interceptor
    ├── Dockerfile
    └── vite.config.js
```

---

## Getting Started

### With Docker (recommended)

```bash
cp .env.example .env.docker   # fill in your values
docker compose up --build
```

| Service  | URL                       |
|----------|---------------------------|
| API      | http://localhost:8001      |
| Frontend | http://localhost:5173      |
| API Docs | http://localhost:8001/docs |

The API container waits 20 seconds for MySQL to be ready before starting. MySQL data is persisted in a named Docker volume.

### Local Development

**Backend**
```bash
pip install -r requirements.txt
cp .env.example .env        # fill in your values
uvicorn bankingsys:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8001` (configured in `src/services/api.js`).

---

## Environment Variables

Copy `.env.example` to `.env` (local) or `.env.docker` (Docker) and fill in:

| Variable        | Description                          |
|-----------------|--------------------------------------|
| `DATABASE_URL`  | MySQL connection string              |
| `SECRET_KEY`    | JWT signing secret (keep this safe)  |
| `MAIL_USERNAME` | SMTP username                        |
| `MAIL_PASSWORD` | SMTP password                        |
| `MAIL_FROM`     | Sender email address                 |
| `MAIL_SERVER`   | SMTP host (e.g. `smtp.gmail.com`)    |
| `MAIL_PORT`     | SMTP port (e.g. `587`)               |

---

## API Overview

### Auth
| Method | Endpoint            | Auth | Description                      |
|--------|---------------------|------|----------------------------------|
| POST   | `/login`            | —    | Returns JWT access token         |
| GET    | `/verify-email`     | —    | Confirms email from token link   |
| POST   | `/forgotpassword/`  | —    | Sends password reset email       |
| POST   | `/resetpassword/`   | —    | Resets password with UUID token  |

### Users
| Method | Endpoint       | Auth  | Description             |
|--------|----------------|-------|-------------------------|
| GET    | `/users/`      | Admin | List all users          |
| POST   | `/users/`      | Admin | Create a user           |
| GET    | `/users/me`    | User  | Get own profile         |
| PATCH  | `/users/me`    | User  | Update own profile      |
| DELETE | `/users/{id}`  | Admin | Delete a user           |

### Banking
| Method | Endpoint          | Auth | Description                   |
|--------|-------------------|------|-------------------------------|
| POST   | `/deposits/`      | User | Deposit funds                 |
| GET    | `/deposits/`      | User | Deposit history               |
| POST   | `/withdrawals/`   | User | Withdraw funds                |
| GET    | `/withdrawals/`   | User | Withdrawal history            |
| POST   | `/transactions/`  | User | Transfer to another user      |
| GET    | `/transactions/`  | User | Full transaction history      |

### Analytics
| Method | Endpoint               | Auth | Description                          |
|--------|------------------------|------|--------------------------------------|
| GET    | `/analytics/summary`   | User | Lifetime totals (sent, received, etc)|
| GET    | `/analytics/monthly`   | User | Month-by-month sent/received data    |

Full interactive docs (Swagger UI) at **`/docs`**, ReDoc at **`/redoc`**.

---

## Authentication Flow

1. Register via `POST /users/` (admin) or the signup flow — a verification email is sent
2. Click the link in the email to hit `GET /verify-email?token=...`
3. Log in via `POST /login` with `username` + `password` (form-encoded) — receive a JWT
4. Pass the token as `Authorization: Bearer <token>` on all subsequent requests
5. Changing your password increments `token_version`, invalidating all existing tokens

---

## Testing

```bash
pytest test_bankingsys.py -v
```

The test suite covers: user registration and login, admin-only guards, deposit/withdrawal/transfer flows, balance validation, token invalidation after password change, account lockout, and edge cases like self-transfers and insufficient funds.

---

## Security

- Passwords hashed with **bcrypt**
- JWT `version` field means a stolen token is useless after a password change
- Accounts lock temporarily after **5 failed login attempts**
- Email must be **verified** before login is permitted
- Auth endpoints are **rate-limited** (SlowAPI)
- CORS restricted to `http://localhost:5173` by default — update for production