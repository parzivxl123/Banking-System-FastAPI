from database import engine
from models import *
from fastapi import FastAPI
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