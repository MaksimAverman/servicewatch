"""In-memory storage. Will be replaced by PostgreSQL; keep the interface small."""

_targets: list[dict] = []


def add_target(url: str) -> dict:
    target = {"id": len(_targets) + 1, "url": url}
    _targets.append(target)
    return target


def list_targets() -> list[dict]:
    return list(_targets)


def clear() -> None:
    _targets.clear()
