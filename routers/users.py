from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import *


import logging

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
    logger.info(
        f"Admin '{current_user.UserName}' viewed all transactions"
    )
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

@router.get('/users/user')
def ViewYourself(db: Session = Depends(get_db), current_user : User = Depends(get_current_user),):
    user = User(
        UserName=current_user.UserName,
        UserEmail=current_user.UserEmail,
        UserID= current_user.UserID,
        UserPassword=current_user.UserPassword,
        UserBalance= current_user.UserBalance
    )
    return user