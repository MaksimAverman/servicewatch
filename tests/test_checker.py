import httpx

from app.checker import check_url


def test_up_on_200():
    transport = httpx.MockTransport(lambda request: httpx.Response(200))
    result = check_url("https://example.com", transport=transport)
    assert result["is_up"] is True
    assert result["status_code"] == 200
    assert result["error"] is None


def test_down_on_500():
    transport = httpx.MockTransport(lambda request: httpx.Response(500))
    result = check_url("https://example.com", transport=transport)
    assert result["is_up"] is False
    assert result["status_code"] == 500


def test_down_on_network_error():
    def handler(request):
        raise httpx.ConnectError("boom")

    result = check_url("https://example.com", transport=httpx.MockTransport(handler))
    assert result["is_up"] is False
    assert result["status_code"] is None
    assert result["error"] == "ConnectError"
