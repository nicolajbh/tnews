from tnews.sources.financialtimes import FinancialTimesSource


def main() -> None:

    # articles = BloombergSource().fetch_articles()
    articles = FinancialTimesSource().fetch_articles()
    for article in articles:
        print(f"{article.published_at}\t{article.title}")


if __name__ == "__main__":
    main()
