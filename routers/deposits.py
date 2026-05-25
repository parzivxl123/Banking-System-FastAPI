from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db
from models import Deposit, User
from schemas import DepositPost, DepositView

from routers.auth import get_current_user
router = APIRouter()
@router.get('/deposits/')
def displayDepositsByUser(db:Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    history = db.query(Deposit).filter(Deposit.UserID==current_user.UserID).all()
    return history
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
    db.add(
        newdeposit
    )
    db.commit()
    db.refresh(
        newdeposit
    )
    return newdeposit
