import os
import pytest
import json
from typing import Any

BASE_URL = "https://kaiten.mysite.ru/api"
DATA_DIR = "tests/data"


def read_file(filename: str) -> str:
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        return f.read()


def read_json(filename: str) -> Any:
    return json.loads(read_file(filename))


@pytest.fixture
def external_requests(requests_mock) -> None:  # type: ignore
    requests_mock.get(
        BASE_URL + "/latest/users/current", json=read_json("current.body.json")
    )
    requests_mock.get(
        BASE_URL + "/latest/cards/1733551", json=read_json("card.body.json")
    )
    requests_mock.get(
        BASE_URL + "/latest/cards/1733552",
        json={},
        status_code=404,
    )
    requests_mock.post(
        BASE_URL + "/latest/cards/1733551/time-logs",
        json=read_json("timelog.body.json"),
    )
