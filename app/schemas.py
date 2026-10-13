from pydantic import BaseModel, HttpUrl


class TargetCreate(BaseModel):
    url: HttpUrl


class Target(BaseModel):
    id: int
    url: str
