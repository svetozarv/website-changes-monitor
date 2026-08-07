from pydantic import BaseModel, ConfigDict, Field, HttpUrl, PositiveInt
from datetime import datetime

class TargetCreate(BaseModel):
    url: HttpUrl
    check_interval_seconds: PositiveInt = 60


class TargetResponse(TargetCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
    created_at: datetime
