from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.orm import Session

from database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from sqlalchemy import func, extract
from models import User, Transaction, Deposit, Withdrawal

router = APIRouter(
    tags=["Analytics"]
)
from models import *

from schemas import *

from routers.auth import get_current_user
import logging

from utils import create_audit_log

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)


@router.get('/analytics/summary')
def AnalyticsSummary(db : Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    money_sent = (
        db.query(
            func.coalesce(
                func.sum(
                    Transaction.TransactionAmount
                ),
                0
            )
        )
        .filter(
            Transaction.SenderID == current_user.UserID
        )
        .scalar()
    )
    money_received = (
        db.query(
            func.coalesce(
                func.sum(
                    Transaction.TransactionAmount
                ),
                0
            )
        )
        .filter(
            Transaction.RecieverID == current_user.UserID
        )
        .scalar()
    )
    total_deposit = (
        db.query(
            func.coalesce(
                func.sum(
                    Deposit.Amount
                ),
                0
            )
        )
        .filter(
            Deposit.UserID == current_user.UserID
        )
        .scalar()
    )
    total_withdrawal = (
        db.query(
            func.coalesce(
                func.sum(
                    Withdrawal.Amount
                ),
                0
            )
        )
        .filter(
            Withdrawal.UserID == current_user.UserID
        )
        .scalar()
    )

    total_transaction = (
        db.query(
            Transaction
        )
        .filter(
            (Transaction.SenderID == current_user.UserID)
            |
            (Transaction.RecieverID == current_user.UserID)
        )
        .count()
    )
    total_deposits = (
        db.query(
            Deposit
        )
        .filter(
            Deposit.UserID==current_user.UserID
        )
        .count()
    )
    total_withdrawals = (
        db.query(
            Withdrawal
        )
        .filter(
            Withdrawal.UserID == current_user.UserID
        )
        .count()
    )
    return {
        "balance": current_user.UserBalance,
        "money_sent": money_sent,
        "money_received": money_received,
        "total_deposit": total_deposit,
        "total_withdrawal": total_withdrawal,
        "total_transactions": total_transaction,
        "total_deposits": total_deposits,
        "total_withdrawals": total_withdrawals,
    }

@router.get('/analytics/monthly')
def Monthlyanalytics(db : Session = Depends(get_db), current_user :User = Depends(get_current_user)):
    sent_query = (
        db.query(
            extract(
                "month",
                Transaction.TransactionDate
            ).label("month"),

            func.sum(
                Transaction.TransactionAmount
            ).label("total")
        )
        .filter(
            Transaction.SenderID ==
            current_user.UserID
        )
        .group_by("month")
        .all()
    )
    received_query = (
        db.query(
            extract(
                "month",
                Transaction.TransactionDate
            ).label("month"),

            func.sum(
                Transaction.TransactionAmount
            ).label("total")
        )
        .filter(
            Transaction.RecieverID ==
            current_user.UserID
        )
        .group_by("month")
        .all()
    )
    month_names = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }
    data = {}

    for i in range(1, 13):
        data[i] = {
            "month": month_names[i],
            "sent": 0,
            "received": 0
        }
    for month, total in sent_query:
        data[int(month)]["sent"] = float(total)
    for month, total in received_query:
        data[int(month)]["received"] = float(total)
    return list(data.values())