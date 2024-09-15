from evrim.client import Evrim
import pytest
import os


@pytest.fixture
def evrim_client():
    url = os.getenv("EVRIM_URL")
    username = os.getenv("EVRIM_USERNAME")
    password = os.getenv("EVRIM_PASSWORD")
    return Evrim(url=url, username=username, password=password)
