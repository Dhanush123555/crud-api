from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routers.video_router import router as video_router
from app.routers.created_video_router import router as created_video_router
from app.routers.published_video_router import router as published_video_router
from app.security.login_router import router as login_router
from app.security.utils import router as token_router
from app.routers.user_router import router as user_router
from app.db.db import create_db_and_tables



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan = lifespan)


# -------------------All routes that involve uploaded videos--------------------------------------------

app.include_router(video_router)

#---------------------------All routes that involve created videos------------------------------

app.include_router(created_video_router)

#-----------------------All routes that involve published videos----------------------------

app.include_router(published_video_router)

#-----------------------All routes for the user route----------------------------------------

app.include_router(user_router)

#------------------------All routes for token routing-------------------------------

app.include_router(token_router)

#-----------------------All routes for login route-----------------------------

app.include_router(login_router)