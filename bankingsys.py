from sqlalchemy.orm import Session
from database import get_db
from database import engine
from models import *
from schemas import *
from fastapi import FastAPI, HTTPException, Depends
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, UTC
app = FastAPI()
Base.metadata.create_all(
    bind = engine
)
pwd_context = CryptContext(
    schemes = ["bcrypt"],
    deprecated = "auto")
SECRET_KEY = "aa564rus1hma456nglunxyz448ia"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
def create_accestoken(data : dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(
        {"exp":expire}
    )

    encodedjwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encodedjwt

@app.post('/login')
def loginsys(
    form_data: OAuth2PasswordRequestForm= Depends(), db:Session= Depends(get_db)):
    userfound = db.query(User).filter(User.UserName==form_data.username).first()
    print(User)
    if userfound is None:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )
    if not pwd_context.verify(
        form_data.password,
        userfound.UserPassword
    ):
        raise HTTPException(
            status_code=401,
            detail="Wrong Password"
        )
    accesstoken = create_accestoken(
        {
            "sub": str(userfound.UserID),
            "version" : userfound.token_version
        }
    )
    return {
        "access_token": accesstoken,
        "token_type": "bearer"
    }

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid Token"
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        userid = int(
            payload.get("sub")
        )

        version = int(
            payload.get("version")
        )

    except JWTError:

        raise credentials_exception


    db.expire_all()

    user = db.query(
        User
    ).filter(
        User.UserID == userid
    ).first()


    if user.token_version != version:

        raise HTTPException(
            status_code=401,
            detail="Session Expired"
        )

    return user
@app.get('/deposits/')
def displayDepositsByUser(db:Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    history = db.query(Deposit).filter(Deposit.UserID==current_user.UserID).all()
    return history
@app.post(
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

@app.get('/withdrawal/', response_model=list[WithdrawalView])
def displayWithdrawalsByUser(db :Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    history = db.query(Withdrawal).filter(Withdrawal.UserID == current_user.UserID).all()
    return history

@app.post('/withdrawal/')
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


@app.get(
    '/users/',
    response_model=list[UserView]
)
def displayallusers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_Admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized"
        )
    users = db.query(
        User
    ).all()

    return users
@app.get('/users/{NumberOfUsers}')
def displaySelectUsers(NumberOfUsers: int,db : Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    if current_user.is_Admin:
        if 20>NumberOfUsers>0:
            return db.query(User).limit(NumberOfUsers).all()
        if NumberOfUsers>20:
            return "Limit Exceeded"
        else:
            return "Number of Users invalid"
    else:
        raise HTTPException(
            status_code=403,
            detail="Unauthorised"
        )

@app.post('/users/')
def CreateUser(user : UserCreate,db : Session = Depends(get_db), current_user = Depends(get_current_user)):

    if not current_user.is_Admin:
        raise HTTPException(
            status_code=403,
            detail="Unauthorised"
        )
    existing_user = db.query(
        User
    ).filter(
        User.UserName == user.UserName
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="UserName Already Exists"
        )
    new_user = User(
        UserName=user.UserName,
        UserEmail=user.UserEmail,
        UserPassword=pwd_context.hash(user.UserPassword),
        UserBalance = user.UserBalance
    )

    db.add(
        new_user
    )
    db.commit()
    db.refresh(
        new_user
    )
    return new_user

@app.put('/users/',response_model=UserView)
def updateuser(
    updated_user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    existing_user = db.query(
        User
    ).filter(
        User.UserName == updated_user.UserName,
        User.UserID != current_user.UserID
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username Already Exists"
        )

    current_user.UserName = updated_user.UserName
    current_user.UserEmail = updated_user.UserEmail
    current_user.UserPassword = pwd_context.hash(
        updated_user.UserPassword
    )

    current_user.token_version += 1

    db.commit()
    db.refresh(current_user)

    return current_user


@app.delete('/users/' , response_model=UserView)
def delete_user(userID : int,db : Session = Depends(get_db), current_user : User = Depends(get_current_user)):

    if not current_user.is_Admin :
        raise HTTPException(
            status_code=403,
            detail="Unauthorised"
        )
    user = db.query(User).filter(User.UserID==userID).first()
    if user is None:
        raise HTTPException(
            status_code=404,
        detail = "userNotFound"
        )
    if user.UserID == current_user.UserID:

        raise HTTPException(
            status_code=400,
            detail="Cannot delete yourself"
        )
    db.delete(user)
    db.commit()
    return user

@app.get('/transanctions/')
def ViewAllTransactions(db:Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    if current_user.is_Admin:
        return db.query(Transaction).all()
    else:
        raise HTTPException(
            status_code=403 ,
            detail="Unauthorised"
        )

@app.get('/transanctions/{NumberofTransactions}')
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
@app.post('/transactions/')
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

@app.get('/transactions/')
def TransactionbyUser(db : Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    history = db.query(Transaction).filter(
        (Transaction.SenderID==current_user.UserID)|(Transaction.RecieverID==current_user.UserID)
    ).all()

    return history