import pytest
from pizdyuk.pzd_events import Event, TypedEvent

def test_event(mocker):
    mock = mocker.Mock()
    event = Event()
    event.add_handler(mock.on_event)
    event.invoke()
    event.clear_handlers()
    event.invoke()

    mock.on_event.assert_called_once()

    with pytest.raises(ValueError):
        event.add_handler(10)
    
def test_typed_event(mocker):
    mock = mocker.Mock()
    event = TypedEvent(str)

    with pytest.raises(ValueError):
        TypedEvent("mock_value")

    with pytest.raises(ValueError):
        event.add_handler(10)

    event.add_handler(mock.on_event)
    event.invoke("mock_string")

    with pytest.raises(TypeError):
        event.invoke(10)

    mock.on_event.assert_called_once()
    mock.on_event.assert_called_with("mock_string")

