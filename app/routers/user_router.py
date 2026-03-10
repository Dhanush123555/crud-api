from fastapi import APIRouter, Depends
from typing import Annotated
from app.db.db import SessionDep
from app.models.model import User, Video
from app.security.utils import get_user_from_token
from sqlmodel import select


router = APIRouter(prefix= "/user", tags = ["User"])

@router.get("/")
def get_uploaded_videos(
    session: SessionDep,
    user: Annotated[User, Depends(get_user_from_token)],
    limit: int = 10
) -> list[Video]:
    
    query = select(Video)  
    videos = session.exec(query.where(Video.user == user.username).limit(limit)).all()
    return videos