import requests

API_KEY = "17d48751951c4fe387e3fc54c110daa4"

# Map Inshorts categories to NewsAPI categories
NEWSAPI_CAT_MAP = {
    'trending':  'general',
    'world':     'general',
    'war':       'general',
    'tech':      'technology',
    'science':   'science',
    'health':    'health',
    'business':  'business',
    'sports':    'sports',
}

def _build_article(item, inshorts_category):
    return {
        'title':             item.get('title', ''),
        'description':       item.get('description', ''),
        'type':              'news',
        'source':            item.get('source', {}).get('name', 'News'),
        'category':          inshorts_category,
        'inshorts_category': inshorts_category,
        'url':               item.get('url', ''),
        'published_at':      item.get('publishedAt', ''),
        'source_name':       item.get('source', {}).get('name', ''),
        'author':            item.get('author', ''),
        'image_url':         item.get('urlToImage', ''),
    }

def fetch_news_by_category(inshorts_category, max_items=10):
    """Fetch live NewsAPI articles for a specific Inshorts category."""
    newsapi_cat = NEWSAPI_CAT_MAP.get(inshorts_category, 'general')
    articles = []
    try:
        url = (
            f"https://newsapi.org/v2/top-headlines"
            f"?category={newsapi_cat}&language=en"
            f"&apiKey={API_KEY}&pageSize={max_items}"
        )
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get('status') != 'ok':
            print(f"  NewsAPI [{inshorts_category}]: {data.get('message')}")
            return []

        for item in data.get('articles', []):
            if not item.get('title') or not item.get('description'):
                continue
            if len(item.get('description', '')) < 30:
                continue
            articles.append(_build_article(item, inshorts_category))

        print(f"  NewsAPI [{inshorts_category}]: {len(articles)} articles")
    except Exception as e:
        print(f"  NewsAPI error [{inshorts_category}]: {e}")
    return articles


def fetch_news():
    """Backward-compatible: fetch from all main categories."""
    all_articles = []
    for cat in ['trending', 'tech', 'science', 'health', 'business', 'sports']:
        all_articles.extend(fetch_news_by_category(cat, max_items=5))
    return all_articles