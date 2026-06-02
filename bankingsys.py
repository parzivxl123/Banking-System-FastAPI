import schemas
from database import engine, get_db
from models import *
from fastapi import FastAPI
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
app = FastAPI()
from routers import (
    auth,
    users,
    deposits,
    withdrawals,
    transactions
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

