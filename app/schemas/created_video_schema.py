from datetime import datetime, time
from sqlmodel import Field, SQLModel

class CreatedVideoBase(SQLModel):
    
    output_type: str = Field(index = True)
    created_duration: time
    created_at: datetime = Field(default_factory = datetime.now)
    video_id: str

class CreatedVideoUpdate(CreatedVideoBase):
    
    output_type: str | None = None
    created_duration: time | None = None
    created_at: datetime | None = None
    video_id: str | None = None

class CreatedVideoCreate(CreatedVideoBase):
    pass
