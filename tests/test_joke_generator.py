import requests
import pytest

from joke_generator import JokeAPIError, get_random_joke


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, payload):
        self.payload = payload

    def get(self, *args, **kwargs):
        return FakeResponse(self.payload)


def test_get_single_joke():
    joke = get_random_joke(session=FakeSession({"category": "Programming", "type": "single", "joke": "Ship it!", "id": 1}))
    assert joke.category == "Programming"
    assert joke.text == "Ship it!"


def test_get_two_part_joke():
    joke = get_random_joke(session=FakeSession({"category": "Misc", "type": "twopart", "setup": "Why?", "delivery": "Because."}))
    assert joke.text == "Why?\nBecause."


def test_api_error_payload():
    with pytest.raises(JokeAPIError, match="No jokes found"):
        get_random_joke(session=FakeSession({"error": True, "message": "No jokes found"}))
