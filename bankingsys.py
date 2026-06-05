import schemas
from database import engine, get_db
from models import *
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
limiter = Limiter(
    key_func=get_remote_address
)
from utils import create_audit_log
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)
from routers import (
    auth,
    users,
    deposits,
    withdrawals,
    transactions,
    analytics
)
Base.metadata.create_all(
    bind = engine
)
app.include_router(
    auth.router
)
app.include_router(
    users.router
)
app.include_router(
    deposits.router
)
app.include_router(
    withdrawals.router
)
app.include_router(
    transactions.router
)
app.include_router(
    analytics.router
)

