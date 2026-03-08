from __future__ import annotations

from fastapi import APIRouter, Query, HTTPException
from typing import Annotated
from app.filters.video_filter import VIDEO_FILTER_MAP, VideoFilter
from app.models.model import Video
from app.schemas.video_schema import VideoCreate, VideoUpdate
from app.db.db import SessionDep
from sqlmodel import select

router = APIRouter(prefix = "/videos", tags = ["Videos"])

@router.get("/")
def get_uploaded_videos(
    session: SessionDep,
    filter_query: Annotated[VideoFilter, Query()]
) -> list[Video]:
    
    query = select(Video)  
    data = filter_query.model_dump(exclude_none = True)

    for key, value in data.items():
        if value and key in VIDEO_FILTER_MAP:
            if not isinstance(value, list):
                value = [value]
            column = VIDEO_FILTER_MAP[key]
            query = query.where(column.in_(value))

    videos = session.exec(query.limit(data["limit"])).all()
    return videos


@router.get("/{video_id}")
def get_uploaded_video(session: SessionDep, video_id: str) -> Video:
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code = 404, detail = "Video not found")
    
    return video

@router.post("/")
def post_video(video: VideoCreate, session: SessionDep) -> Video:
    db_video = Video.model_validate(video)
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video

@router.patch("/{video_id}")
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

@router.delete("/{video_id}")
def delete_video(video_id: str, session: SessionDep) -> dict[str, bool]:
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code = 404, detail = "Video to delete not found")

    session.delete(video)
    session.commit()
    return {"ok": True}