from datetime import datetime, time
from sqlmodel import Field, SQLModel

class PublishedVideoBase(SQLModel):
    
    platform: str = Field(index = True)
    published_url: str | None = None
    is_published: bool = True
    published_duration: time
    published_at: datetime  = Field(default_factory=datetime.now)
    video_id: str


class PublishedVideoUpdate(PublishedVideoBase):
    
    platform: str | None = None
    published_url: str | None = None
    is_published: bool | None = None
    published_duration: time | None = None
    published_at: datetime | None = None
    video_id: str | None = None

class PublishedVideoCreate(PublishedVideoBase):
    pass