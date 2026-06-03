from tkinter.constants import CASCADE

from DateTime import DateTime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    Boolean,
    ForeignKey,
    DateTime
)
from datetime import datetime, UTC
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    UserID = Column(
        Integer,
        primary_key=True,
        index=True
    )
    UserName = Column(
        String(100),
        unique=True
    )
    UserPassword = Column(
        String(300)
    )
    UserBalance = Column(
        DECIMAL(10,2),
        default=0
    )
    UserEmail = Column(
        String(100),
        unique=True
    )
    is_Admin = Column(
        Boolean,
        default=False
    )
    token_version = Column(
        Integer,
        default=0
    )
    ResetToken = Column(
        String(255),
        nullable=True
    )
    FailedLoginAttempts = Column(
        Integer,
        default=0
    )
    LockedUntil = Column(
        DateTime,
        nullable=True
    )

class Transaction(Base):
    __tablename__ =  "transactions"

    TransactionID = Column(
        Integer,
        primary_key=True,
        index=True
    )
    SenderID = Column(
        Integer,
        ForeignKey(
            "users.UserID",
            ondelete="CASCADE"
        )
    )
    RecieverID = Column(
        Integer,
        ForeignKey(
            "users.UserID",
            ondelete="CASCADE"
        )
    )
    TransactionAmount = Column(
        DECIMAL(10, 2)
    )
    TransactionStatus = Column(
        String(50)
    )
    sender = relationship(
        "User",
        foreign_keys=[SenderID]
    )
    receiver = relationship(
        "User",
        foreign_keys=[RecieverID],

    )

class Deposit(Base):
    __tablename__ = "deposits"

    DepositID = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    UserID = Column(
        Integer,
        ForeignKey(
            "users.UserID",
            ondelete="CASCADE"
        )
    )
    Amount = Column(
        DECIMAL(
            10,2
        )
    )
    user = relationship("User")

class Withdrawal(Base):

    __tablename__ = "withdrawals"
    WithdrawalID = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    UserID = Column(
        Integer,
        ForeignKey(
            "users.UserID",
            ondelete="CASCADE"
        )
    )
    Amount = Column(
        DECIMAL(10,2)
    )
    user = relationship(
        "User"
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"

    LogID = Column(
        Integer,
        primary_key=True,
        index=True
    )

    UserID = Column(
        Integer,
        ForeignKey("users.UserID")
    )

    Action = Column(
        String(100)
    )
    Details = Column(
        String(500)
    )
    Created_At = Column(
        DateTime,
        default=lambda:datetime.now(UTC)
    )