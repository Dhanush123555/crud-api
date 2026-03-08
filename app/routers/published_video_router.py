from __future__ import annotations

from fastapi import APIRouter, Query, HTTPException
from typing import Annotated
from app.models.model import PublishedVideo
from app.schemas.published_video_schema import PublishedVideoUpdate, PublishedVideoCreate
from app.filters.published_video_filter import PublishedVideoFilter, PUBLISHED_VIDEO_FILTER_MAP
from app.db.db import SessionDep
from sqlmodel import select

router = APIRouter(prefix = "/publishedvideos", tags = ["Published Videos"])


@router.get("/")
def get_published_videos(
    session: SessionDep,
    filter_query: Annotated[PublishedVideoFilter, Query()]
) -> list[PublishedVideo]:
    
    query = select(PublishedVideo)  
    data = filter_query.model_dump(exclude_none = True)

    for key, value in data.items():
        if value and key in PUBLISHED_VIDEO_FILTER_MAP:
            if not isinstance(value, list):
                value = [value]
            column = PUBLISHED_VIDEO_FILTER_MAP[key]
            query = query.where(column.in_(value))

    videos = session.exec(query.limit(data["limit"])).all()
    return videos

@router.get("/{publish_id}")
def get_published_video(session: SessionDep, publish_id: int) -> PublishedVideo:
    video = session.get(PublishedVideo, publish_id)
    if not video:
        raise HTTPException(status_code = 404, detail = "Video not found")
    
    return video

@router.post("/")
def post_published_video(video: PublishedVideoCreate, session: SessionDep) -> PublishedVideo:
    db_video = PublishedVideo.model_validate(video)
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video

@router.patch("/{publish_id}")
def patch_published_video(publish_id: int, video: PublishedVideoUpdate, session: SessionDep) -> PublishedVideo:
    db_video = session.get(PublishedVideo, publish_id)
    if not db_video:
        raise HTTPException(status_code = 404, detail = "Video to update not found")
    
    video_data = video.model_dump(exclude_unset = True)
    db_video.sqlmodel_update(video_data)
    session.add(db_video)
    session.commit()
    session.refresh(db_video)
    return db_video

@router.delete("/{publish_id}")
def delete_published_video(publish_id: int, session: SessionDep) -> dict[str, bool]:
    video = session.get(PublishedVideo, publish_id)
    if not video:
        raise HTTPException(status_code = 404, detail = "Video to delete not found")

    session.delete(video)
    session.commit()
    return {"ok": True}