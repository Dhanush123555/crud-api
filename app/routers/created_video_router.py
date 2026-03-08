from __future__ import annotations

from fastapi import APIRouter, Query, HTTPException
from typing import Annotated
from app.models.model import CreatedVideo
from app.schemas.created_video_schema import CreatedVideoUpdate, CreatedVideoCreate
from app.filters.created_video_filter import CREATED_VIDEO_FILTER_MAP, CreatedVideoFilter
from app.db.db import SessionDep
from sqlmodel import select

router = APIRouter(prefix = "/createdvideos", tags = ["Created Videos"])


@router.get("/")
def get_created_videos(
    session: SessionDep,
    filter_query: Annotated[CreatedVideoFilter, Query()]
) -> list[CreatedVideo]:
    
    query = select(CreatedVideo)  
    data = filter_query.model_dump(exclude_none = True)

    for key, value in data.items():
        if value and key in CREATED_VIDEO_FILTER_MAP:
            if not isinstance(value, list):
                value = [value]
            column = CREATED_VIDEO_FILTER_MAP[key]
            query = query.where(column.in_(value))

    videos = session.exec(query.limit(data["limit"])).all()
    return videos

@router.get("/{creation_id}")
def get_created_video(session: SessionDep, creation_id: int) -> CreatedVideo:
    video = session.get(CreatedVideo, creation_id)
    if not video:
        raise HTTPException(status_code = 404, detail = "Video not found")
    
    return video

@router.post("/")
def post_created_video(video: CreatedVideoCreate, session: SessionDep) -> CreatedVideo:
    db_video = CreatedVideo.model_validate(video)
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video

@router.patch("/{creation_id}")
def patch_created_video(creation_id: int, video: CreatedVideoUpdate, session: SessionDep) -> CreatedVideo:
    db_video = session.get(CreatedVideo, creation_id)
    if not db_video:
        raise HTTPException(status_code = 404, detail = "Video to update not found")
    
    video_data = video.model_dump(exclude_unset = True)
    db_video.sqlmodel_update(video_data)
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video

@router.delete("/{creation_id}")
def delete_created_video(creation_id: int, session: SessionDep) -> dict[str, bool]:
    video = session.get(CreatedVideo, creation_id)
    if not video:
        raise HTTPException(status_code = 404, detail = "Video to delete not found")

    session.delete(video)
    session.commit()
    return {"ok": True}