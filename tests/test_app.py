import pytest
import json

from tw_kaiten.app import app
from tests.const import (
    TIMEWARRIOR_STDIN,
    TIMEWARRIOR_MULTIPLE_TAGS_STDIN,
    TIMEWARRIOR_MULTIPLE_TYPES_STDIN,
    TIMEWARRIOR_NOT_FOUND_STDIN,
)


@pytest.mark.usefixtures("external_requests")
def test_app_success(requests_mock) -> None:  # type: ignore
    app(TIMEWARRIOR_STDIN)

    history = requests_mock.request_history
    assert history[0].headers["Authorization"] == "Bearer MYKAITEN_TOKEN"
    task1_data = json.loads(history[4].text)
    assert task1_data == {
        "role_id": 1,
        "time_spent": 22,
        "for_date": "2024-07-15",
        "comment": "DEV: sometext",
    }
    task2_data = json.loads(history[5].text)
    assert task2_data == {
        "role_id": 1,
        "time_spent": 107,
        "for_date": "2024-07-15",
        "comment": "sometext",
    }
    task3_data = json.loads(history[6].text)
    assert task3_data == {
        "role_id": 1,
        "time_spent": 47,
        "for_date": "2024-07-15",
        "comment": "-",
    }


@pytest.mark.usefixtures("external_requests")
def test_app_wrong_params() -> None:
    with pytest.raises(AttributeError):
        app(TIMEWARRIOR_MULTIPLE_TAGS_STDIN)

    with pytest.raises(AttributeError):
        app(TIMEWARRIOR_MULTIPLE_TYPES_STDIN)

    with pytest.raises(SystemExit):
        app(TIMEWARRIOR_NOT_FOUND_STDIN)
