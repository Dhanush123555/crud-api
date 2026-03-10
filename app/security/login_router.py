from fastapi import APIRouter, Form, HTTPException, Response
from pydantic import BaseModel
from typing import Annotated
from app.db.db import SessionDep
from app.models.model import User
from pwdlib import PasswordHash


router = APIRouter(prefix = "/signup")


class FormData(BaseModel):
    username: str
    password: str
    confirm_password: str

password_hash = PasswordHash.recommended()


@router.post("/", tags = ["Signup"])
def signup_user(data: Annotated[FormData, Form()], session: SessionDep):
    user = session.get(User, data.username)
    if user:
        raise HTTPException(status_code= 400, detail= "Username already exists. Please try another.")
    if data.password != data.confirm_password:
        raise HTTPException(status_code= 400, detail= "Please type the same password twice.")
    hashed_password = password_hash.hash(data.password)
    user = User(username= data.username, hashed_password= hashed_password)
    session.add(user)
    session.commit()
    return Response(status_code= 201, content= "User created succesfully")