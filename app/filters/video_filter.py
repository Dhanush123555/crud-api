from app.models.model import Video
from pydantic import BaseModel, Field

VIDEO_FILTER_MAP = {
    "users" : Video.user,
    "channels" : Video.channel,
    "input_types" : Video.input_type,
    "teams" : Video.team,
    "languages" : Video.language
}

class VideoFilter(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(10, le = 50)
    channels: list[str] | None = None
    users: list[str] | None = None
    teams: list[str] | None = None
    languages: list[str] | None = None
    input_types: list[str] | None = None