from app import main


def fake_check(url):
    return {"status_code": 200, "response_time_ms": 12.5, "is_up": True, "error": None}


def test_run_check_stores_result(client, monkeypatch):
    monkeypatch.setattr(main, "check_url", fake_check)
    client.post("/targets", json={"url": "https://example.com"})

    response = client.post("/targets/1/check")
    assert response.status_code == 201
    assert response.json()["target_id"] == 1
    assert response.json()["is_up"] is True

    history = client.get("/checks").json()
    assert len(history) == 1


def test_check_unknown_target_returns_404(client):
    response = client.post("/targets/999/check")
    assert response.status_code == 404
