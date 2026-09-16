from datetime import datetime

import requests

from tnews.models import Article


def _fetch(session: requests.Session) -> object:
    response = session.get(
        "https://www.bloomberg.com/lineup-next/api/stories",
        params={
            "types": "ARTICLE,FEATURE,INTERACTIVE,LETTER,EXPLAINERS",
            "locale": "en",
            "pageNumber": 1,
            "limit": 25,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def _parse_response(data: object) -> list[Article]:
    if not isinstance(data, list):
        raise TypeError("Expected Bloomberg response to be a list")

    return [_parse_article(item) for item in data]


def _parse_article(data: object) -> Article:
    if not isinstance(data, dict):
        raise TypeError("Expected Bloomberg article to be an object")

    headline = data.get("headline")
    url = data.get("url")
    published_at = data.get("publishedAt")

    if not isinstance(headline, str):
        raise TypeError("Missing or invalid headline")

    if not isinstance(url, str):
        raise TypeError("Missing or invalid url")

    if not isinstance(published_at, str):
        raise TypeError("Missing or invalid publication time")

    return Article(
        title=headline,
        url=url,
        source="Bloomberg",
        published_at=datetime.fromisoformat(published_at),
    )


class BloombergSource:
    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Referer": "https://www.bloomberg.com/latest",
                "Accept-Language": "en-US,en;q=0.9",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
            }
        )

    def fetch_articles(self) -> list[Article]:
        response = _fetch(self._session)
        articles = _parse_response(response)
        return articles
