import pytest
import datetime
from pizdyuk.market.stock import Stock

def test_stock(mocker):
    date = datetime.datetime(2021, 4, 7, 10, 58, 00)
    stock_data = [(date, 200)]
    stock = Stock("mock_symbol", stock_data)

    stock.update()

    assert stock.symbol == "mock_symbol"
    assert stock.price == 200
    assert stock.current_time == date