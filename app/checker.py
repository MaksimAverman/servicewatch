import time

import httpx

TIMEOUT_SECONDS = 5.0


def check_url(url: str, transport: httpx.BaseTransport | None = None) -> dict:
    """Perform one HTTP check. Never raises: network errors count as "down"."""
    started = time.perf_counter()
    status_code = None
    error = None
    try:
        with httpx.Client(timeout=TIMEOUT_SECONDS, transport=transport) as client:
            response = client.get(url)
        status_code = response.status_code
    except httpx.HTTPError as exc:
        error = type(exc).__name__
    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    is_up = status_code is not None and status_code < 400
    return {
        "status_code": status_code,
        "response_time_ms": elapsed_ms,
        "is_up": is_up,
        "error": error,
    }
