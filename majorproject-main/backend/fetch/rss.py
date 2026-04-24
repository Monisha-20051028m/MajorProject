import feedparser

def fetch_rss():
    feed = feedparser.parse("http://feeds.bbci.co.uk/news/science_and_environment/rss.xml")

    data = []

    for entry in feed.entries[:10]:
        data.append({
            "title": entry.get("title"),
            "description": entry.get("summary"),
            "type": "blog",
            "source": "rss"
        })

    return data