from pydantic import BaseModel, ConfigDict, HttpUrl


class TargetCreate(BaseModel):
    url: HttpUrl


class Target(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str


class Check(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    target_id: int
    status_code: int | None
    response_time_ms: float
    is_up: bool
    error: str | None
