import feedparser
import re
from urllib.parse import urlparse

CATEGORY_FEEDS = {
    'trending': [
        'https://feeds.bbci.co.uk/news/rss.xml',
        'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    ],
    'world': [
        'https://feeds.bbci.co.uk/news/world/rss.xml',
        'https://www.aljazeera.com/xml/rss/all.xml',
        'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    ],
    'war': [
        'https://feeds.bbci.co.uk/news/world/rss.xml',
        'https://www.aljazeera.com/xml/rss/all.xml',
        'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    ],
    'science': [
        'https://www.sciencedaily.com/rss/top/science.xml',
        'https://www.nasa.gov/rss/dyn/breaking_news.rss',
        'https://rss.nytimes.com/services/xml/rss/nyt/Science.xml',
        'https://www.theguardian.com/science/rss',
    ],
    'tech': [
        'https://feeds.feedburner.com/TechCrunch',
        'https://www.theverge.com/rss/index.xml',
        'https://feeds.arstechnica.com/arstechnica/index',
        'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml',
    ],
    'health': [
        'https://rss.nytimes.com/services/xml/rss/nyt/Health.xml',
        'https://www.theguardian.com/society/health/rss',
        'https://feeds.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC',
    ],
    'business': [
        'https://feeds.bbci.co.uk/news/business/rss.xml',
        'https://rss.nytimes.com/services/xml/rss/nyt/Business.xml',
    ],
    'sports': [
        'https://feeds.bbci.co.uk/sport/rss.xml',
        'https://www.espn.com/espn/rss/news',
    ],
}

WAR_KEYWORDS = [
    'war', 'conflict', 'attack', 'missile', 'military', 'troops', 'battle',
    'bombing', 'strike', 'invasion', 'ceasefire', 'ukraine', 'russia', 'gaza',
    'israel', 'hamas', 'hezbollah', 'nato', 'armed forces', 'airstrike',
    'casualties', 'hostage', 'siege', 'offensive', 'combat', 'frontline',
    'warship', 'drone strike', 'sanctions', 'weapons', 'killed in', 'dead in',
]

def _get_image(entry):
    try:
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            return entry.media_thumbnail[0].get('url', '')
        if hasattr(entry, 'media_content') and entry.media_content:
            for m in entry.media_content:
                if m.get('url', '').endswith(('.jpg', '.png', '.jpeg', '.webp')):
                    return m.get('url', '')
        if hasattr(entry, 'enclosures') and entry.enclosures:
            for enc in entry.enclosures:
                if 'image' in enc.get('type', ''):
                    return enc.get('href', '')
    except Exception:
        pass
    return ''

def _get_domain(url):
    try:
        d = urlparse(url).netloc
        return d.replace('www.', '').replace('feeds.', '').replace('rss.', '')
    except Exception:
        return 'News'

def _strip_html(text):
    return re.sub(r'<[^>]+>', '', text or '').strip()

def fetch_rss_by_category(category, max_items=20):
    """Fetch live RSS articles for a specific Inshorts-style category."""
    feeds = CATEGORY_FEEDS.get(category, CATEGORY_FEEDS['trending'])
    articles = []
    seen = set()

    for feed_url in feeds:
        try:
            print(f"  RSS [{category}] <- {feed_url}")
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:10]:
                title = _strip_html(entry.get('title', ''))
                description = _strip_html(
                    entry.get('summary', '') or entry.get('description', '')
                )

                if not title or len(title) < 5:
                    continue
                if not description or len(description) < 20:
                    description = title

                key = title.lower().strip()
                if key in seen:
                    continue

                # War category: only articles with conflict keywords
                if category == 'war':
                    combined = (title + ' ' + description).lower()
                    if not any(kw in combined for kw in WAR_KEYWORDS):
                        continue

                seen.add(key)
                articles.append({
                    'title': title,
                    'description': description[:600],
                    'type': 'news',
                    'source': _get_domain(feed_url),
                    'category': category,
                    'inshorts_category': category,
                    'url': entry.get('link', ''),
                    'published_at': entry.get('published', ''),
                    'image_url': _get_image(entry),
                    'feed_source': _get_domain(feed_url),
                })

                if len(articles) >= max_items:
                    break

        except Exception as e:
            print(f"  RSS error [{category}] {feed_url}: {e}")
            continue

        if len(articles) >= max_items:
            break

    print(f"  RSS [{category}]: {len(articles)} articles fetched")
    return articles


def fetch_rss():
    """Backward-compatible: fetch a mix of categories."""
    all_articles = []
    for cat in ['trending', 'world', 'science', 'tech', 'health', 'business']:
        all_articles.extend(fetch_rss_by_category(cat, max_items=4))
    return all_articles[:25]