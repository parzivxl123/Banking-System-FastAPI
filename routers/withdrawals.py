from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.orm import Session

from database import get_db
from models import Withdrawal, User
from schemas import WithdrawalPost, WithdrawalView

from routers.auth import get_current_user
import logging

from utils import create_audit_log

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)
router = APIRouter()
@router.get('/withdrawals/')
def displayWithdrawalsByUser(
        page: int = Query(1),
        page_size: int = Query(5),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    start = (page-1)*page_size
    withdrawal_query = db.query(Withdrawal).filter(Withdrawal.UserID==current_user.UserID).order_by(Withdrawal.WithdrawalID.desc())
    history = withdrawal_query.offset(start).limit(page_size).all()
    return {
        "page": page,
        "page_size": page_size,
        "total_withdrawals": withdrawal_query.count(),
        "withdrawals": history
    }

@router.post('/withdrawal/', response_model=WithdrawalView)
def makeWithdrawal(withdrawal : WithdrawalPost,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if withdrawal.Amount <=0 :
        raise  HTTPException(
            status_code=400,
            detail="Invalid Amount"
        )
    if current_user.UserBalance<withdrawal.Amount:
        logger.warning(
            f"Withdrawal failed: User='{current_user.UserName}' Amount={withdrawal.Amount} Reason='Insufficient Funds'"
        )
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds"
        )
    current_user.UserBalance -= withdrawal.Amount
    withdrawal1 = Withdrawal(
        UserID=current_user.UserID,
        Amount = withdrawal.Amount,

    )
    logger.info(
        f"Withdrawal successful: User='{current_user.UserName}' Amount={withdrawal.Amount}"
    )
    db.add(withdrawal1)
    db.commit()
    db.refresh(withdrawal1)

    create_audit_log(
        db,
        current_user.UserID,
        "WITHDRAWAL",
        f"Withdrew {withdrawal.Amount}"
    )
    print(withdrawal1.__dict__)
    return withdrawal1
