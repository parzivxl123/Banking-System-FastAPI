from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db

from models import (
    User,
    Transaction
)

from schemas import (
    TransactionsPost,
    TransactionView
)

from routers.auth import get_current_user
router = APIRouter()

@router.get('/transanctions/')
def ViewAllTransactions(db:Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    if current_user.is_Admin:
        return db.query(Transaction).all()
    else:
        raise HTTPException(
            status_code=403 ,
            detail="Unauthorised"
        )

@router.get('/transanctions/{NumberofTransactions}')
def ViewTransactions(NumberofTransactions:int,db:Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    if current_user.is_Admin:
        if 20>=NumberofTransactions>0:
            return db.query(Transaction).limit(NumberofTransactions).all()
        if NumberofTransactions<0:
            return "Invalid Number Of Transactions"
        else:
            return "Transactions Number Limit Reached"
    else:
        raise HTTPException(
            status_code=403,
            detail="Unauthorised"
        )
@router.post('/transactions/')
def addTransactions(transaction : TransactionsPost,db : Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    Sender = current_user
    Receiver = db.query(User).filter(User.UserID==transaction.RecieverID).first()
    if Receiver is None:
        raise HTTPException(
            status_code=404,
            detail="Receiver not Found"
        )

    newtransaction = Transaction(
        TransactionAmount=transaction.TransactionAmount,
        TransactionStatus = "Done",
        RecieverID = Receiver.UserID,
        SenderID=Sender.UserID
    )
    if(Sender.UserBalance<transaction.TransactionAmount):
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )
    if(transaction.TransactionAmount<=0):
        raise HTTPException(
            status_code=400,
            detail="Invalid Amount"
        )
    if(Sender==Receiver):
        raise HTTPException(
            status_code = 400,
            detail= "Sender cannot same as receiver"
        )
    Sender.UserBalance -= (
        transaction.TransactionAmount
    )

    Receiver.UserBalance += (
        transaction.TransactionAmount
    )
    db.add(
        newtransaction
    )

    db.commit()

    db.refresh(
        newtransaction
    )
    return newtransaction

@router.get('/transactions/')
def TransactionbyUser(db : Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    history = db.query(Transaction).filter(
        (Transaction.SenderID==current_user.UserID)|(Transaction.RecieverID==current_user.UserID)
    ).all()

    return history