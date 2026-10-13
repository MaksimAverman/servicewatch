"""In-memory storage. Will be replaced by PostgreSQL; keep the interface small."""

_targets: list[dict] = []
_checks: list[dict] = []


def add_target(url: str) -> dict:
    target = {"id": len(_targets) + 1, "url": url}
    _targets.append(target)
    return target


def list_targets() -> list[dict]:
    return list(_targets)


def get_target(target_id: int) -> dict | None:
    return next((t for t in _targets if t["id"] == target_id), None)


def add_check(target_id: int, result: dict) -> dict:
    check = {"id": len(_checks) + 1, "target_id": target_id, **result}
    _checks.append(check)
    return check


def list_checks() -> list[dict]:
    return list(_checks)


def clear() -> None:
    _targets.clear()
    _checks.clear()
