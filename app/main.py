from fastapi import FastAPI, HTTPException

from app import storage
from app.checker import check_url
from app.schemas import Check, Target, TargetCreate

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


@app.post("/targets/{target_id}/check", response_model=Check, status_code=201)
def run_check(target_id: int) -> dict:
    target = storage.get_target(target_id)
    if target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    return storage.add_check(target_id, check_url(target["url"]))


@app.get("/checks", response_model=list[Check])
def get_checks() -> list[dict]:
    return storage.list_checks()
