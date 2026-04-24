import requests

API_KEY = "8ea9f7ecb0e24d3e8e7de01ad39a23a6"

def fetch_news():
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    articles = []

    for item in data.get('articles', []):
        articles.append({
            "title": item.get('title', ''),
            "description": item.get('description', ''),
            "type": "news",
            "source": "newsapi"
        })

    return articles