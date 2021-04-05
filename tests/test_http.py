import pytest
import requests
from pizdyuk.pzd_http import PizdyukServer, PizdyukRequestHandler

url = "http://localhost:8080"

def test_server(mocker):
    server = start_and_get_server()

    assert server.is_running
    assert server.server_address == "localhost"
    assert server.port == 8080

    server.close()

    assert not server.is_running

@pytest.mark.parametrize("action", ["get_stock", "get_user", None])
def test_get_request(mocker, action):
    mock_user = mocker.patch("pizdyuk.pzd_http.users")
    mock_stocks = mocker.patch("pizdyuk.pzd_http.stocks")
    server = start_and_get_server()

    assert server.is_running

    try:
        response = requests.get(url, {
            "action": action
        }, timeout=1)
    except:
        server.close()

    if action == "get_stock":
        mock_stocks.handler_request.assert_called_once()
    elif action == "get_user":
        mock_user.handle_get_request.assert_called_once()
    elif not action:
        assert response.status_code == 400
        print(dict(response))
        assert False

    server.close()


def test_post_request(mocker):
    pass

def start_and_get_server():
    server_address = "localhost"
    server = PizdyukServer(server_address, PizdyukRequestHandler)
    server.start()
    return server