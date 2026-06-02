from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.orm import Session

from database import get_db
from models import Withdrawal, User
from schemas import WithdrawalPost, WithdrawalView

from routers.auth import get_current_user
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

@router.post('/withdrawal/')
def makeWithdrawal(withdrawal : WithdrawalPost,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if withdrawal.Amount <=0 :
        raise  HTTPException(
            status_code=400,
            detail="Invalid Amount"
        )
    if current_user.UserBalance<withdrawal.Amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds"
        )
    current_user.UserBalance -= withdrawal.Amount
    withdrawal1 = Withdrawal(
        UserID=current_user.UserID,
        Amount = withdrawal.Amount,

    )
    db.add(withdrawal1)
    db.commit()
    db.refresh(withdrawal1)
    return withdrawal1
