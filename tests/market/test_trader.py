import pizdyuk
from pizdyuk.market.trader import get_trader

def test_handle_order(mocker):
    mocker.patch("pizdyuk.market.trader.stock_manager")
    mocker.patch("pizdyuk.market.trader.user_manager")
    valid_data = {
        "user_id": "mock_user_id",
        "symbol": "mock_symbol",
        "num_shares": 10
    }
    invalid_data = {
        "user_id": "mock_user_id",
        "num_shares": 10
    }
    trader = get_trader()

    status_code, response = trader.handle_order("buy", **valid_data)
    assert status_code == 200
    assert response == {}

    status_code, response = trader.handle_order("buy", **invalid_data)
    assert status_code == 400
    assert response["error"]