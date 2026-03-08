from app.models.model import CreatedVideo
from pydantic import BaseModel, Field

CREATED_VIDEO_FILTER_MAP = {
    "output_types" : CreatedVideo.output_type
}

class CreatedVideoFilter(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(10, le = 50)
    output_types: list[str] | None = None