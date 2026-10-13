from pydantic import BaseModel, HttpUrl


class TargetCreate(BaseModel):
    url: HttpUrl


class Target(BaseModel):
    id: int
    url: str


class Check(BaseModel):
    id: int
    target_id: int
    status_code: int | None
    response_time_ms: float
    is_up: bool
    error: str | None
