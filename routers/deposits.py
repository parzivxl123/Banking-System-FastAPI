from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.orm import Session

from database import get_db
from models import Deposit, User
from schemas import DepositPost, DepositView

from routers.auth import get_current_user
import logging

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)
router = APIRouter()
@router.get('/deposits/')
def displayDepositsByUser(
        page: int = Query(1),
        page_size: int = Query(5),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    start = (page-1)*page_size
    deposit_query = db.query(Deposit).filter(Deposit.UserID==current_user.UserID).order_by(Deposit.DepositID.desc())
    history = deposit_query.offset(start).limit(page_size).all()
    return {
        "page": page,
        "page_size": page_size,
        "total_deposits": deposit_query.count(),
        "deposits": history
    }
@router.post(
    '/deposit/',
    response_model=DepositView
)
def makeDeposit(
    deposit: DepositPost,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):
    if deposit.Amount <= 0:
        logger.warning(
            f"Invalid deposit attempt: User='{current_user.UserName}' Amount={Deposit.Amount}"
        )
        raise HTTPException(
            status_code=400,
            detail="Invalid Amount"
        )
    current_user.UserBalance += (
        deposit.Amount
    )
    newdeposit = Deposit(
        UserID=current_user.UserID,
        Amount=deposit.Amount
    )
    logger.info(
        f"Deposit successful: User='{current_user.UserName}' Amount={deposit.Amount}"
    )
    db.add(
        newdeposit
    )
    db.commit()
    db.refresh(
        newdeposit
    )
    return newdeposit
