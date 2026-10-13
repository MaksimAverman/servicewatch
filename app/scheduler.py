import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor

from app import storage
from app.checker import check_url
from app.db import SessionLocal

logger = logging.getLogger("servicewatch.scheduler")

CHECK_INTERVAL_SECONDS = float(os.getenv("CHECK_INTERVAL_SECONDS", "60"))
MAX_WORKERS = 10


def run_all_checks(session_factory=SessionLocal) -> int:
    """Check every target once and store the results. Returns the number of checks."""
    with session_factory() as db:
        targets = [(t.id, t.url) for t in storage.list_targets(db)]

    # Network I/O is slow: check targets in parallel so one slow site doesn't delay the rest.
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        results = list(pool.map(lambda t: (t[0], check_url(t[1])), targets))

    with session_factory() as db:
        for target_id, result in results:
            storage.add_check(db, target_id, result)
    return len(results)


async def scheduler_loop(interval: float = CHECK_INTERVAL_SECONDS) -> None:
    while True:
        try:
            count = await asyncio.to_thread(run_all_checks)
            logger.info("Background run finished: %d checks", count)
        except Exception:
            # A failure (e.g. DB down) must not kill the loop; retry on the next tick.
            logger.exception("Background run failed")
        await asyncio.sleep(interval)
