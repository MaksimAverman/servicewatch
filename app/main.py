from fastapi import FastAPI

from app import storage
from app.schemas import Target, TargetCreate

app = FastAPI(title="ServiceWatch")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe: used by Docker/Kubernetes to know the app is up."""
    return {"status": "ok"}


@app.post("/targets", response_model=Target, status_code=201)
def create_target(payload: TargetCreate) -> dict:
    return storage.add_target(str(payload.url))


@app.get("/targets", response_model=list[Target])
def get_targets() -> list[dict]:
    return storage.list_targets()
