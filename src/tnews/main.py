from tnews.sources.bloomberg import BloombergSource


def main() -> None:

    articles = BloombergSource().fetch_articles()
    for article in articles:
        print(f"{article.published_at}\t{article.title}")


if __name__ == "__main__":
    main()
