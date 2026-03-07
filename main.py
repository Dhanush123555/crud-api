from __future__ import annotations

from typing import Annotated
from datetime import datetime, time
import os
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select, create_engine

from models import SQLModel, VideoUpdate, Video, VideoBase, Created_Video_Base, Created_Video, Created_Video_Update, Published_Video_Base, Published_Video, Published_Video_Update



load_dotenv()

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_url, echo= True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# -------------------All routes that involve uploaded videos--------------------------------------------

@app.get("/videos/")
def get_uploaded_videos(
    session: SessionDep,
    limit: Annotated[int, Query(le = 50)] = 10
) -> list[Video]:
    
    videos = session.exec(select(Video).limit(limit)).all()
    return videos


@app.get("/videos/{video_id}")
def get_uploaded_video(session: SessionDep, video_id: str) -> Video:
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code = 404, detail = "Video not found")
    
    return video

@app.post("/videos/")
def post_video(video: VideoBase, session: SessionDep) -> Video:
    db_video = Video.model_validate(video)
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video

@app.patch("/videos/{video_id}")
def patch_video(video_id: str, video: VideoUpdate, session: SessionDep) -> Video:
    db_video = session.get(Video, video_id)
    if not db_video:
        raise HTTPException(status_code = 404, detail = "Video to update not found")
    
    video_data = video.model_dump(exclude_unset = True)
    db_video.sqlmodel_update(video_data)
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video

@app.delete("/videos/{video_id}")
def delete_video(video_id: str, session: SessionDep) -> dict[str, bool]:
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code = 404, detail = "Video to delete not found")

    session.delete(video)
    session.commit()
    return {"ok": True}

#---------------------------All routes that involve created videos------------------------------

@app.get("/createdvideos/")
def get_created_videos(
    session: SessionDep,
    limit: Annotated[int, Query(le = 50)] = 10
) -> list[Created_Video]:
    
    videos = session.exec(select(Created_Video).limit(limit)).all()
    return videos

@app.get("/createdvideos/{creation_id}")
def get_created_video(session: SessionDep, creation_id: int) -> Created_Video:
    video = session.get(Created_Video, creation_id)
    if not video:
        raise HTTPException(status_code = 404, detail = "Video not found")
    
    return video

@app.post("/createdvideos/")
def post_created_video(video: Created_Video_Base, session: SessionDep) -> Created_Video:
    db_video = Created_Video.model_validate(video)
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video

@app.patch("/createdvideos/{creation_id}")
def patch_created_video(creation_id: int, video: Created_Video_Update, session: SessionDep) -> Created_Video:
    db_video = session.get(Created_Video, creation_id)
    if not db_video:
        raise HTTPException(status_code = 404, detail = "Video to update not found")
    
    video_data = video.model_dump(exclude_unset = True)
    db_video.sqlmodel_update(video_data)
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video

@app.delete("/createdvideos/{creation_id}")
def delete_created_video(creation_id: int, session: SessionDep) -> dict[str, bool]:
    video = session.get(Created_Video, creation_id)
    if not video:
        raise HTTPException(status_code = 404, detail = "Video to delete not found")

    session.delete(video)
    session.commit()
    return {"ok": True}

#-----------------------All routes that involve published videos----------------------------

@app.get("/publishedvideos/")
def get_published_videos(
    session: SessionDep,
    limit: Annotated[int, Query(le = 50)] = 10
) -> list[Published_Video]:
    
    videos = session.exec(select(Published_Video).limit(limit)).all()
    return videos

@app.get("/publishedvideos/{publish_id}")
def get_published_video(session: SessionDep, publish_id: int) -> Published_Video:
    video = session.get(Published_Video, publish_id)
    if not video:
        raise HTTPException(status_code = 404, detail = "Video not found")
    
    return video

@app.post("/publishedvideos/")
def post_published_video(video: Published_Video_Base, session: SessionDep) -> Published_Video:
    db_video = Published_Video.model_validate(video)
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video

@app.patch("/publishedvideos/{publish_id}")
def patch_published_video(publish_id: int, video: Published_Video_Update, session: SessionDep) -> Published_Video:
    db_video = session.get(Published_Video, publish_id)
    if not db_video:
        raise HTTPException(status_code = 404, detail = "Video to update not found")
    
    video_data = video.model_dump(exclude_unset = True)
    db_video.sqlmodel_update(video_data)
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video

@app.delete("/publishedvideos/{publish_id}")
def delete_published_video(publish_id: int, session: SessionDep) -> dict[str, bool]:
    video = session.get(Published_Video, publish_id)
    if not video:
        raise HTTPException(status_code = 404, detail = "Video to delete not found")

    session.delete(video)
    session.commit()
    return {"ok": True}