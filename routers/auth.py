from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from jose import JWTError, jwt
from passlib.context import CryptContext

from datetime import datetime, timedelta, UTC

from database import get_db
from models import User
router = APIRouter()
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

@router.post('/login')
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