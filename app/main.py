from fastapi import FastAPI

app = FastAPI(title="ServiceWatch")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe: used by Docker/Kubernetes to know the app is up."""
    return {"status": "ok"}
