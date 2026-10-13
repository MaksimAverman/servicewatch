from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import storage
from app.checker import check_url
from app.db import Base, engine, get_db
from app.schemas import Check, Target, TargetCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup. A migration tool (Alembic) can replace this later.
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="ServiceWatch", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe: used by Docker/Kubernetes to know the app is up."""
    return {"status": "ok"}


@app.post("/targets", response_model=Target, status_code=201)
def create_target(payload: TargetCreate, db: Session = Depends(get_db)):
    return storage.add_target(db, str(payload.url))


@app.get("/targets", response_model=list[Target])
def get_targets(db: Session = Depends(get_db)):
    return storage.list_targets(db)


@app.post("/targets/{target_id}/check", response_model=Check, status_code=201)
def run_check(target_id: int, db: Session = Depends(get_db)):
    target = storage.get_target(db, target_id)
    if target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    return storage.add_check(db, target_id, check_url(target.url))


@app.get("/checks", response_model=list[Check])
def get_checks(db: Session = Depends(get_db)):
    return storage.list_checks(db)
