from fastapi import APIRouter, Depends, HTTPException, Query

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
import logging

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get('/transanctions/')
def ViewAllTransactions(
        page: int = Query(1),
        page_size: int = Query(10),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_Admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorised"
        )

    start = (page - 1) * page_size

    transaction_query = db.query(
        Transaction
    ).order_by(
        Transaction.TransactionID.desc()
    )

    history = transaction_query.offset(
        start
    ).limit(
        page_size
    ).all()

    return {
        "page": page,
        "page_size": page_size,
        "total_transactions": transaction_query.count(),
        "transactions": history
    }
@router.post('/transactions/')
def addTransactions(transaction : TransactionsPost,db : Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    Sender = current_user
    Receiver = db.query(User).filter(User.UserID==transaction.RecieverID).first()
    if Receiver is None:
        logger.warning(
            f"Transfer failed: Sender='{current_user.UserID}' ReceiverID={transaction.RecieverID} Reason='Receiver Not Found'"
        )
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
        logger.warning(
            f"Transfer failed: Sender='{Sender.UserName}' Amount={transaction.TransactionAmount} Reason='Insufficient Funds'"
        )
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
    logger.info(
        f"Transfer successful: Sender='{Sender.UserName}' Receiver='{Receiver.UserName}' Amount={transaction.TransactionAmount}"
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
def TransactionbyUser(
        page: int = Query(1),
        page_size: int = Query(5),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    start = (page - 1) * page_size

    transaction_query = db.query(
        Transaction
    ).filter(
        (Transaction.SenderID == current_user.UserID)
        |
        (Transaction.RecieverID == current_user.UserID)
    ).order_by(
        Transaction.TransactionID.desc()
    )

    history = transaction_query.offset(
        start
    ).limit(
        page_size
    ).all()

    return {
        "page": page,
        "page_size": page_size,
        "total_transactions": transaction_query.count(),
        "transactions": history
    }