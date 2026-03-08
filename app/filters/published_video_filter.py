from app.models.model import PublishedVideo
from pydantic import BaseModel, Field

PUBLISHED_VIDEO_FILTER_MAP = {
    "platforms" : PublishedVideo.platform
}

class PublishedVideoFilter(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(10, le = 50)
    platorms: list[str] | None = None