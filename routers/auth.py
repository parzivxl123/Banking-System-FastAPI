import uuid
from fastapi_mail import (
    FastMail,
    MessageSchema,
    MessageType
)

from email_config import conf
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from schemas import *
from jose import JWTError, jwt
from passlib.context import CryptContext

from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv
import os

load_dotenv()
from database import get_db
from models import User
import logging

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)
router = APIRouter()
pwd_context = CryptContext(
    schemes = ["bcrypt"],
    deprecated = "auto")
SECRET_KEY = os.getenv(
    "SECRET_KEY"
)
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

def create_refresh_token(
        data:dict
):
    to_encode = data.copy()
    expire = datetime.now(UTC)+timedelta(
        days = 7
   )

    to_encode.update(
        {
            "exp" : expire,
            "type" : "refresh"
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


@router.post('/login')
def loginsys(
    form_data: OAuth2PasswordRequestForm= Depends(), db:Session= Depends(get_db)):
    userfound = db.query(User).filter(User.UserName==form_data.username).first()

    if userfound is None:
        logger.warning(
            f"Login failed: user '{form_data.username}' not found"
        )

        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )
    if not pwd_context.verify(
        form_data.password,
        userfound.UserPassword
    ):
        logger.warning(
            f"Login failed: incorrect password for '{userfound.UserName}'"
        )
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

    logger.info(
        f"User '{userfound.UserName}' logged in successfully"
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

@router.post("/forgotpassword/")
async def forgotPassword(
        request:ForgotPassword,
        db : Session = Depends(get_db)
):
    user = db.query(User).filter(User.UserEmail==request.UserEmail).first()

    if not user :
        logger.warning(
            f"Password reset requested for unknown email '{request.UserEmail}'"
        )
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )
    logger.info(
        f"Password reset requested: Email='{user.UserEmail}'"
    )
    token = str(uuid.uuid4())

    user.ResetToken = token
    db.commit()
    message = MessageSchema(
        subject="Password Reset",
        recipients = [
            user.UserEmail
        ],
        body=f"""
Your Password reset token:
{token}
            """,
        subtype=MessageType.plain
    )
    fm = FastMail(conf)
    await fm.send_message(
        message

    )
    return {
        "Check Your Mail"
    }


@router.post("/resetpassword/")
def resetPassword(
        request:ResetPassword,
        db : Session = Depends(get_db)
):
    user = db.query(User).filter(User.ResetToken==request.Token).first()
    if not user :
        logger.warning(
            f"Password reset failed: Invalid token '{request.Token}'"
        )
        raise HTTPException(
            status_code=404,
            detail="User Not Found for given Token"
        )

    user.UserPassword = pwd_context.hash(request.NewPassword)
    user.ResetToken = None
    user.token_version+=1
    logger.info(
        f"Password reset successful: User='{user.UserName}'"
    )
    db.commit()
    return {
        "Password Updated"
    }