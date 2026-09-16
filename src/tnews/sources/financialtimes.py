import datetime

import feedparser
import requests

from tnews.models import Article


def _fetch(session: requests.Session) -> object:
    response = session.get(
        "https://www.ft.com/news-feed",
        params={
            "format": "rss",
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.content


def _parse_response(data: object) -> list[Article]:
    if not isinstance(data, bytes):
        raise TypeError("Expected Financial Times response to be bytes")

    parsed_feed = feedparser.parse(data)
    return [_parse_article(item) for item in parsed_feed.get("entries", [])]


def _parse_article(data: object) -> Article:
    if not isinstance(data, dict):
        raise TypeError("Expected Financial Times article to be an object")

    headline = data.get("title")
    url = data.get("link")
    published_parsed = data.get("published_parsed")

    if not isinstance(headline, str):
        raise TypeError("Missing or invalid headline")

    if not isinstance(url, str):
        raise TypeError("Missing or invalid url")

    if not published_parsed:
        raise TypeError("Missing or invalid publication time")

    published_at = datetime.datetime(
        *published_parsed[:6],
        tzinfo=datetime.UTC,
    )

    return Article(
        title=headline,
        url=url,
        source="Financial Times",
        published_at=published_at,
    )


class FinancialTimesSource:
    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers.update(
            {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "en-US,en;q=0.9",
                "referer": "https://www.reddit.com/",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
            }
        )

    def fetch_articles(self) -> list[Article]:
        response = _fetch(self._session)
        articles = _parse_response(response)
        return articles
