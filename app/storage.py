"""Data access layer. Endpoints talk to these functions, not to SQL directly."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Check, Target


def add_target(db: Session, url: str) -> Target:
    target = Target(url=url)
    db.add(target)
    db.commit()
    return target


def list_targets(db: Session) -> list[Target]:
    return list(db.scalars(select(Target).order_by(Target.id)))


def get_target(db: Session, target_id: int) -> Target | None:
    return db.get(Target, target_id)


def add_check(db: Session, target_id: int, result: dict) -> Check:
    check = Check(target_id=target_id, **result)
    db.add(check)
    db.commit()
    return check


def list_checks(db: Session) -> list[Check]:
    return list(db.scalars(select(Check).order_by(Check.id)))
