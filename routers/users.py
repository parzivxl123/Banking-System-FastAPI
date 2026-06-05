from fastapi import APIRouter, Depends, HTTPException
from fastapi_mail import MessageSchema, MessageType, FastMail
from sqlalchemy import false
from sqlalchemy.orm import Session
from database import get_db
from email_config import conf
from models import User
from schemas import *
import logging
import secrets
logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)

from routers.auth import (
    get_current_user,
    pwd_context
)
router = APIRouter()
@router.get(
    '/users/',
    response_model=list[UserView]
)
def displayallusers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_Admin:
        logger.warning(
            f"Unauthorized transaction access attempt by '{current_user.UserName}'"
        )
        raise HTTPException(
            status_code=403,
            detail="Unauthorized"
        )
    users = db.query(
        User
    ).all()

    return users

@router.post('/users/')
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
        UserBalance = user.UserBalance,
        IsVerified=True
    )
    db.add(
        new_user
    )
    db.commit()
    db.refresh(
        new_user
    )
    return new_user

@router.put('/users/',response_model=UserView)
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


@router.delete('/users/' , response_model=UserView)
def delete_user(userid : int,db : Session = Depends(get_db), current_user : User = Depends(get_current_user)):

    if not current_user.is_Admin :
        raise HTTPException(
            status_code=403,
            detail="Unauthorised"
        )
    user = db.query(User).filter(User.UserID==userid).first()
    if user is None:
        raise HTTPException(
            status_code=404,
        detail = "userNotFount"
        )
    if user.UserID == current_user.UserID:

        raise HTTPException(
            status_code=400,
            detail="Cannot delete yourself"
        )
    db.delete(user)
    db.commit()
    return user

@router.get('/users/user' , response_model=UserView)
def ViewYourself(current_user : User = Depends(get_current_user),):
    user = User(UserName=current_user.UserName,
                UserEmail=current_user.UserEmail,
                UserID=current_user.UserID,
                UserPassword=current_user.UserPassword,
                UserBalance=current_user.UserBalance)
    return user





@router.post('/users/register' , response_model=UserView)
async def NewRegister(user:UserRegister, db:Session = Depends(get_db)):
    verification_token = secrets.token_urlsafe(32)
    new_user = User(
        UserName=user.UserName,
        UserEmail=user.UserEmail,
        UserPassword=pwd_context.hash(user.UserPassword),
        IsVerified=False,
        VerificationToken=verification_token

    )
    existing_user = db.query(User).filter(User.UserName==user.UserName,
                                          User.UserEmail==user.UserEmail).first()
    if existing_user:
        raise HTTPException(
            status_code=401,
            detail="Username or email id already taken"
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    verification_link = (
        f"http://localhost:8001/verify-email"
        f"?token={verification_token}"
    )
    body = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0;padding:0;background:#f4f6f9;font-family:Arial,sans-serif;">

    <div style="
    max-width:600px;
    margin:40px auto;
    background:white;
    border-radius:12px;
    overflow:hidden;
    box-shadow:0 4px 12px rgba(0,0,0,0.1);
    ">

    <div style="
    background:#1f2937;
    padding:30px;
    text-align:center;
    ">

    <h1 style="color:white;margin:0;">
    Banking System
    </h1>

    <p style="color:#d1d5db;">
    Email Verification
    </p>

    </div>

    <div style="padding:40px;">

    <h2>
    Welcome!
    </h2>

    <p>
    Thank you for creating an account.
    Please verify your email address before logging in.
    </p>

    <div style="text-align:center;margin:30px 0;">

    <a
    href="{verification_link}"
    style="
    background:#2563eb;
    color:white;
    padding:14px 30px;
    text-decoration:none;
    border-radius:8px;
    font-weight:bold;
    display:inline-block;
    "
    >
    Verify Email
    </a>

    </div>

    <p>
    If the button does not work, copy the link below:
    </p>

    <p style="
    background:#f3f4f6;
    padding:12px;
    border-radius:6px;
    word-break:break-all;
    ">
    {verification_link}
    </p>

    <hr>

    <p style="font-size:13px;color:#6b7280;">
    If you did not create this account, you can safely ignore this email.
    </p>

    </div>

    </div>

    </body>
    </html>
    """
    message = MessageSchema(
        subject="Email Verification",
        recipients=[
            user.UserEmail
        ],
        body=body,
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(
        message)
    return new_user




@router.get('/users/verificationemail')
async def VerificationEmail(useremail:str, db:Session = Depends(get_db)):
    verification_token = secrets.token_urlsafe(32)
    user = db.query(User).filter(User.UserEmail==useremail).first()
    user.VerificationToken = verification_token
    db.commit()
    db.refresh(user)
    verification_link = (
        f"http://localhost:8001/verify-email"
        f"?token={verification_token}"
    )
    body = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0;padding:0;background:#f4f6f9;font-family:Arial,sans-serif;">

    <div style="
    max-width:600px;
    margin:40px auto;
    background:white;
    border-radius:12px;
    overflow:hidden;
    box-shadow:0 4px 12px rgba(0,0,0,0.1);
    ">

    <div style="
    background:#1f2937;
    padding:30px;
    text-align:center;
    ">

    <h1 style="color:white;margin:0;">
    Banking System
    </h1>

    <p style="color:#d1d5db;">
    Email Verification
    </p>

    </div>

    <div style="padding:40px;">

    <h2>
    Welcome!
    </h2>

    <p>
    Thank you for creating an account.
    Please verify your email address before logging in.
    </p>

    <div style="text-align:center;margin:30px 0;">

    <a
    href="{verification_link}"
    style="
    background:#2563eb;
    color:white;
    padding:14px 30px;
    text-decoration:none;
    border-radius:8px;
    font-weight:bold;
    display:inline-block;
    "
    >
    Verify Email
    </a>

    </div>

    <p>
    If the button does not work, copy the link below:
    </p>

    <p style="
    background:#f3f4f6;
    padding:12px;
    border-radius:6px;
    word-break:break-all;
    ">
    {verification_link}
    </p>

    <hr>

    <p style="font-size:13px;color:#6b7280;">
    If you did not create this account, you can safely ignore this email.
    </p>

    </div>

    </div>

    </body>
    </html>
    """
    message = MessageSchema(
        subject="Email Verification",
        recipients=[
            user.UserEmail
        ],
        body=body,
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(
        message)
    return "Check your mail"

