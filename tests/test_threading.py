import pytest
import time
from pizdyuk.pzd_threading import Pizdyuk_Thread

@pytest.mark.parametrize("raise_error", [True, False])
def test_thread(mocker, raise_error):
    thread = Pizdyuk_Thread(runnable, raise_error)
    mock = mocker.Mock()

    thread.on_started.add_handler(mock.on_started)
    thread.on_finished.add_handler(mock.on_finished)
    thread.on_error.add_handler(mock.on_error)
    thread.on_success.add_handler(mock.on_success)

    thread.start()
    time.sleep(1)

    if raise_error:
        mock.on_error.assert_called_once()
    else:
        mock.on_error.assert_not_called()
        mock.on_success.assert_called_with("success")

    mock.on_started.assert_called_once()
    mock.on_finished.assert_called_once()

def runnable(raise_error):
    if raise_error:
        raise Exception("Mock Exception")

    return "success"