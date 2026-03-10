from datetime import timedelta, timezone, datetime
from typing import Annotated
from dotenv import load_dotenv
import os

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import BaseModel

from app.db.db import SessionDep
from app.models.model import User

load_dotenv()


password_hash = PasswordHash.recommended()
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "SomeBigSecretijfjiafhihasihihihdasihdtAFSG")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp" : datetime.now(timezone.utc) + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)})
    encoded_jwt = jwt.encode(payload= to_encode, key= SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt



def get_user_from_token(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    user = session.get(User, username)
    if user is None:
        raise credentials_exception
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, session: SessionDep):
    user = session.get(User, username)
    if not user:
        verify_password(password, "adummypassword")
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
    


router = APIRouter(prefix= "/token")

@router.post("/")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")
        
