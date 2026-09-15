import requests


def main() -> None:
    session = requests.Session()
    session.headers.update(
        {
            "Referer": "https://www.bloomberg.com/latest",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
        }
    )
    response = session.get(
        "https://www.bloomberg.com/lineup-next/api/stories",
        params={
            "types": "ARTICLE,FEATURE,INTERACTIVE,LETTER,EXPLAINERS",
            "locale": "en",
            "pageNumber": 1,
            "limit": 25,
        },
    )
    response.raise_for_status()
    data = response.json()
    for article in data:
        print(f"{article['publishedAt']} - {article['headline']}")
