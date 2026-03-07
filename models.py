
from typing import Annotated
from datetime import datetime, time
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
import uuid


class VideoBase(SQLModel):
    headline: str
    source_url: str | None = None
    channel: str = Field(index = True)
    user: str = Field(index = True)
    team: str = Field(index = True)
    language: str = Field(index = True)
    uploaded_duration: time
    uploaded_at: datetime  = Field(default_factory=datetime.now)


class VideoUpdate(VideoBase):
    headline: str | None = None
    source_url: str | None = None
    channel: str | None = None
    user: str | None = None
    team: str | None = None
    language: str | None = None
    uploaded_duration: time | None = None
    uploaded_at: datetime  | None = None


class Video(VideoBase, table = True):
    video_id: str | None = Field(default_factory=lambda: str(uuid.uuid4()), primary_key = True)


    video_pub: list["Published_Video"] = Relationship(back_populates = "video")
    video_cre: list["Created_Video"] = Relationship(back_populates = "video")


class Created_Video_Base(SQLModel):
    
    output_type: str = Field(index = True)
    created_duration: time
    created_at: datetime = Field(default_factory = datetime.now)
    video_id: str

class Created_Video_Update(Created_Video_Base):
    
    output_type: str | None = None
    created_duration: time | None = None
    created_at: datetime | None = None
    video_id: str | None = None


class Created_Video(Created_Video_Base, table = True):
    creation_id: int | None = Field(default = None, primary_key = True)
    
    video_id: str = Field(foreign_key = "video.video_id")
    video: "Video" = Relationship(back_populates = "video_cre")


class Published_Video_Base(SQLModel):
    
    platform: str = Field(index = True)
    published_url: str | None = None
    is_published: bool = True
    published_duration: time
    published_at: datetime  = Field(default_factory=datetime.now)
    video_id: str


class Published_Video_Update(Published_Video_Base):
    
    platform: str | None = None
    published_url: str | None = None
    is_published: bool | None = None
    published_duration: time | None = None
    published_at: datetime | None = None
    video_id: str | None = None


class Published_Video(Published_Video_Base, table = True):
    publish_id: int |None = Field(default = None, primary_key = True)

    video_id: str = Field(foreign_key = "video.video_id")
    video: "Video" = Relationship(back_populates = "video_pub")

