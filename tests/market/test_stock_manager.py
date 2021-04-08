import pytest
import datetime
import pizdyuk.market.stock_manager as stocks
from pizdyuk.pzd_utils import datetime_to_str

def test_update(mocker, mock_stock_manager):
    mock_stock_manager.update()
    mock_stock = mock_stock_manager.get_stock("mock_symbol")
    mock_stock.update.assert_called_once()

@pytest.mark.parametrize("mock_request", [{"symbol": "mock_symbol"}, {"symbol": "s"}, {"s": "s"}])
def test_handle_request(mocker, mock_stock_manager, mock_request):
    status_code, response = mock_stock_manager.handle_request(**mock_request)

    if mock_request.get("symbol", None) == "mock_symbol":
        assert status_code == 200
        assert response["symbol"] == "mock_symbol"
        assert response["current_time"] == datetime_to_str(datetime.datetime(2021, 4, 7, 10, 44, 0))
        assert response["price"] == 10
    elif mock_request.get("symbol", None) == "s":
        assert status_code == 404
        assert response["error"]
    else:
        assert status_code == 400
        assert response["error"]

@pytest.fixture
def mock_stock_manager(mocker):
    mocker.patch("pizdyuk.market.stock_manager.StockManager._StockManager__load")
    mock_stock = mocker.Mock()
    mock_stock.symbol = "mock_symbol"
    mock_stock.price = 10
    mock_stock.current_time = datetime.datetime(2021, 4, 7, 10, 44, 0)
    stock_manager = stocks.get_manager()
    stock_manager._StockManager__stocks = {"mock_symbol": mock_stock}

    return stock_manager