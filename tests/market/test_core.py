import pytest
import pizdyuk.pzd_errors as errors
from pizdyuk.market.core import MarketObjectBase, Action

def test_market_object_base():
    object_base = MarketObjectBase()

    with pytest.raises(Exception) as e:
        object_base.update()
        assert isinstance(e, errors.PzdNotImplementedError)

    with pytest.raises(Exception) as e:
        object_base.get_object_info()
        assert isinstance(e, errors.PzdNotImplementedError)

def test_action(mocker):
    mock = mocker.Mock()
    action = Action(mock.function, "mock_value")
    action.execute()

    mock.function.assert_called_once()
    mock.function.assert_called_with("mock_value")