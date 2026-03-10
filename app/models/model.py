from app.schemas.video_schema import VideoBase, SQLModel
from app.schemas.created_video_schema import CreatedVideoBase
from app.schemas.published_video_schema import PublishedVideoBase
from sqlmodel import Field, Relationship
import uuid


class Video(VideoBase, table = True):
    video_id: str | None = Field(default_factory=lambda: str(uuid.uuid4()), primary_key = True)


    video_pub: list["PublishedVideo"] = Relationship(back_populates = "video")
    video_cre: list["CreatedVideo"] = Relationship(back_populates = "video")


class CreatedVideo(CreatedVideoBase, table = True):
    creation_id: int | None = Field(default = None, primary_key = True)
    
    video_id: str = Field(foreign_key = "video.video_id")
    video: "Video" = Relationship(back_populates = "video_cre")


class PublishedVideo(PublishedVideoBase, table = True):
    publish_id: int |None = Field(default = None, primary_key = True)

    video_id: str = Field(foreign_key = "video.video_id")
    video: "Video" = Relationship(back_populates = "video_pub")

class User(SQLModel, table = True):
    username: str = Field(primary_key=True)
    hashed_password: str