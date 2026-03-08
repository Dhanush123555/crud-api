from datetime import datetime, time
from sqlmodel import Field, SQLModel


class VideoBase(SQLModel):
    headline: str
    source_url: str | None = None
    channel: str = Field(index = True)
    user: str = Field(index = True)
    team: str = Field(index = True)
    input_type: str = Field(index = True)
    language: str = Field(index = True)
    uploaded_duration: time
    uploaded_at: datetime  = Field(default_factory=datetime.now)


class VideoUpdate(VideoBase):
    headline: str | None = None
    source_url: str | None = None
    channel: str | None = None
    user: str | None = None
    team: str | None = None
    input_type: str | None = None
    language: str | None = None
    uploaded_duration: time | None = None
    uploaded_at: datetime  | None = None

class VideoCreate(VideoBase):
    pass

class VideoRead(VideoBase):
    pass