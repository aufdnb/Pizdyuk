import pytest
import datetime
from pizdyuk.market.portfolio import Portfolio, PortfolioMember
from pizdyuk.pzd_errors import PzdNotFoundError, PzdInvalidOperationError

def test_portfolio_update(mocker):
    member_1 = mocker.Mock()
    member_2 = mocker.Mock()

    portfolio_members = {
        "mock_symbol_1": member_1,
        "mock_symbol_2": member_2
    }

    portfolio = Portfolio("mock_user_id", portfolio_members)
    portfolio.update()

    member_1.update.assert_called_once()
    member_2.update.assert_called_once()
    assert portfolio.has_member("mock_symbol_1")
    assert portfolio.has_member("mock_symbol_2")

def test_portfolio_add_position(mocker):
    mock_create_member = mocker.patch("pizdyuk.market.portfolio.Portfolio._Portfolio__create_portfolio_member")
    member_1 = mocker.Mock()
    member_2 = mocker.Mock()

    portfolio_members = {
        "mock_symbol_1": member_1,
        "mock_symbol_2": member_2
    }

    portfolio = Portfolio("mock_user_id", portfolio_members)
    portfolio.add_position("mock_symbol_1", 100, datetime.datetime.now(), 1)
    portfolio.add_position("mock_symbol_2", 100, datetime.datetime.now(), 1)
    portfolio.add_position("mock_symbol_3", 100, datetime.datetime.now(), 1)

    member_1.add_position.assert_called_once()
    member_2.add_position.assert_called_once()
    mock_create_member.assert_called_once()
    mock_create_member.assert_called_with("mock_symbol_3")

def test_portfolio_remove_position(mocker):
    member_1 = mocker.Mock()
    member_2 = mocker.Mock()

    portfolio_members = {
        "mock_symbol_1": member_1,
        "mock_symbol_2": member_2
    }

    portfolio = Portfolio("mock_user_id", portfolio_members)
    portfolio.remove_position("mock_symbol_1", 100, datetime.datetime.now(), 1)
    portfolio.remove_position("mock_symbol_2", 100, datetime.datetime.now(), 1)

    member_1.remove_position.assert_called_once()
    member_2.remove_position.assert_called_once()

    with pytest.raises(Exception) as e:
        portfolio.remove_position("mock_symbol_3", 100, datetime.datetime.now(), 1)
        assert isinstance(e, PzdNotFoundError)

def test_portfolio_position_size(mocker):
    member_1 = mocker.Mock()
    member_1.position_size = 10

    portfolio_members = {
        "mock_symbol_1": member_1,
    }

    portfolio = Portfolio("mock_user_id", portfolio_members)
    
    assert portfolio.get_position_size("mock_symbol_1") == member_1.position_size
    assert portfolio.get_position_size("mock_symbol_2") == 0

def test_member_update(mocker, mock_stock):
    member = PortfolioMember(mock_stock, average_price=20, position_size=1)
    member.update()

    assert member.performance == 10
    assert member.performance_percentage == 100

def test_member_add_position(mocker, mock_stock):
    member = PortfolioMember(mock_stock)
    member.add_position(20, datetime.datetime.now(), 1)

    assert member.activity != ""
    assert "BUY" in member.activity
    assert member.position_size == 1
    assert member.total_value == 20

def test_remove_position(mocker, mock_stock):
    member_1 = PortfolioMember(mock_stock)

    member_1.add_position(20, datetime.datetime.now(), 1)
    member_1.remove_position(20, datetime.datetime.now(), 1)

    with pytest.raises(Exception) as e:
        member_1.remove_position(20, datetime.datetime.now(), 1)
        assert isinstance(e, PzdInvalidOperationError)

    assert member_1.position_size == 0
    assert member_1.average_price == 0

@pytest.fixture    
def mock_stock(mocker):
    mock_stock = mocker.patch("pizdyuk.market.stock.Stock")
    mock_stock.price = 10
    mock_stock.symbol = "mock_symbol"
    return mock_stock