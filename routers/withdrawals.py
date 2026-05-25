from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db
from models import Withdrawal, User
from schemas import WithdrawalPost, WithdrawalView

from routers.auth import get_current_user
router = APIRouter()
@router.get('/withdrawal/', response_model=list[WithdrawalView])
def displayWithdrawalsByUser(db :Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    history = db.query(Withdrawal).filter(Withdrawal.UserID == current_user.UserID).all()
    return history

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
