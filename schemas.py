from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class DepositPost(BaseModel):
    Amount : Decimal

class DepositView(BaseModel):
    UserID : int
    Amount : Decimal
    DepositID : int
    model_config = ConfigDict(
        from_attributes = True)

class WithdrawalPost(BaseModel):
    Amount : Decimal

class WithdrawalView(BaseModel):
    UserID : int
    Amount : Decimal
    WithdrawalID : int

    model_config = ConfigDict(
        from_attributes = True)

from pydantic import Field

class UserCreate(BaseModel):

    UserName: str = Field(
        min_length=1
    )

    UserPassword: str = Field(
        min_length=1
    )

    UserBalance: Decimal
    is_Admin: bool = False
    token_version: int = 0
    UserEmail: str

class UserUpdate(BaseModel):
    UserName: str = Field(
        min_length=1
    )

    UserPassword: str = Field(
        min_length=1
    )

    UserBalance: Decimal
    UserEmail: str


class UserView(BaseModel):
    UserID : int
    UserName : str
    UserBalance : Decimal
    UserEmail : str

    model_config = ConfigDict(
        from_attributes = True)

class TransactionsPost(BaseModel):
    TransactionAmount : Decimal
    RecieverID : int


class TransactionView(BaseModel):
    TransactionId: int
    TransactionAmount: Decimal
    RecieverID: int
    SenderID: int
    TransactionStatus : str

    model_config = ConfigDict(
        from_attributes = True)