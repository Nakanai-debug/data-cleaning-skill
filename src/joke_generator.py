"""Fetch and display random jokes from JokeAPI."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from html import unescape
from typing import Any, Mapping

import requests


API_URL = "https://v2.jokeapi.dev/joke/Any"


class JokeAPIError(RuntimeError):
    """Raised when the joke API cannot return a valid joke."""


@dataclass(frozen=True)
class Joke:
    """A normalized joke returned by JokeAPI."""

    category: str
    text: str
    joke_id: int | None = None


def _parse_joke(payload: Mapping[str, Any]) -> Joke:
    if payload.get("error"):
        raise JokeAPIError(str(payload.get("message", "The joke API returned an error.")))

    category = str(payload.get("category", "Unknown"))
    joke_id = payload.get("id")
    if payload.get("type") == "twopart":
        setup = payload.get("setup")
        delivery = payload.get("delivery")
        if not setup or not delivery:
            raise JokeAPIError("The API returned an incomplete two-part joke.")
        text = f"{setup}\n{delivery}"
    else:
        text = payload.get("joke")
        if not text:
            raise JokeAPIError("The API returned an empty joke.")

    return Joke(category=category, text=unescape(str(text)), joke_id=joke_id)


def get_random_joke(
    *,
    timeout: float = 10.0,
    category: str = "Any",
    safe: bool = False,
    session: requests.Session | None = None,
) -> Joke:
    """Fetch one random joke, raising a useful error on failure."""
    params = {"type": "single,twopart"}
    if safe:
        params["safe-mode"] = ""
    client = session or requests
    try:
        response = client.get(f"https://v2.jokeapi.dev/joke/{category}", params=params, timeout=timeout)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise JokeAPIError(f"Unable to reach JokeAPI: {exc}") from exc
    except ValueError as exc:
        raise JokeAPIError("JokeAPI returned invalid JSON.") from exc
    return _parse_joke(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="Print a random joke from JokeAPI")
    parser.add_argument("--category", default="Any", help="JokeAPI category, for example Programming or Misc")
    parser.add_argument("--safe", action="store_true", help="Request safe-mode jokes")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()
    try:
        joke = get_random_joke(category=args.category, safe=args.safe, timeout=args.timeout)
    except JokeAPIError as exc:
        parser.error(str(exc))
    print(f"[{joke.category}]\n{joke.text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
