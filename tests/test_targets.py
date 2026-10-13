def test_list_is_empty_initially(client):
    response = client.get("/targets")
    assert response.status_code == 200
    assert response.json() == []


def test_create_target(client):
    response = client.post("/targets", json={"url": "https://example.com"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "url": "https://example.com/"}


def test_created_target_is_listed(client):
    client.post("/targets", json={"url": "https://example.com"})
    response = client.get("/targets")
    assert len(response.json()) == 1


def test_invalid_url_is_rejected(client):
    response = client.post("/targets", json={"url": "not-a-url"})
    assert response.status_code == 422
