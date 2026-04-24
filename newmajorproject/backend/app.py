import time
from flask import Flask, jsonify, request
from datetime import datetime
import openai
import os
from werkzeug.security import generate_password_hash, check_password_hash

from db import collection, users_collection
from fetch.youtube import fetch_youtube
from fetch.news import fetch_news, fetch_news_by_category
from fetch.rss import fetch_rss, fetch_rss_by_category
from utils.filter import is_useful
from utils.credibility import enrich_with_credibility

app = Flask(__name__)

# Add CORS headers manually
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# OpenAI API key (replace with your key)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Check if OpenAI is available
OPENAI_AVAILABLE = bool(openai.api_key)

sessions = {}

# Initialize user profile
user_profile = {
    "articles_read": 0,
    "videos_watched": 0,
    "time_spent": 0,
    "level": 1,
    "xp": 0
}


def fetch_and_store():
    all_data = []

    youtube_data = fetch_youtube()
    news_data = fetch_news()
    rss_data = fetch_rss()

    print("YouTube:", len(youtube_data))
    print("News:", len(news_data))
    print("RSS:", len(rss_data))

    all_data.extend(youtube_data)
    all_data.extend(news_data)
    all_data.extend(rss_data)

    print("Total fetched:", len(all_data))

    for item in all_data:
        print("Checking item:", item.get("title"))

        if is_useful(item):
            print("Storing:", item.get("title"))

            collection.update_one(
                {"title": item["title"]},
                {"$set": item},
                upsert=True
            )

    # If no data was stored, add some mock data
    if hasattr(collection, 'data') and len(collection.data) == 0:
        mock_data = [
            {
                "title": "The Future of Artificial Intelligence",
                "description": "Exploring how AI will shape our world in the coming decades",
                "type": "video",
                "source": "youtube"
            },
            {
                "title": "Quantum Computing Breakthrough",
                "description": "Scientists achieve major milestone in quantum technology",
                "type": "news",
                "source": "newsapi"
            },
            {
                "title": "Climate Science Research Update",
                "description": "Latest findings on global climate patterns and solutions",
                "type": "blog",
                "source": "rss"
            }
        ]
        for item in mock_data:
            if is_useful(item):
                collection.insert_one(item)


def fetch_real_time():
    """Fetch fresh content without storing it"""
    try:
        all_data = []

        youtube_data = fetch_youtube()
        news_data = fetch_news()
        rss_data = fetch_rss()

        print("Real-time YouTube:", len(youtube_data))
        print("Real-time News:", len(news_data))
        print("Real-time RSS:", len(rss_data))

        all_data.extend(youtube_data)
        all_data.extend(news_data)
        all_data.extend(rss_data)

        # Filter useful content
        useful_data = [item for item in all_data if is_useful(item)]

        print("Total real-time useful content:", len(useful_data))
        return useful_data
    except Exception as e:
        print(f"Error in fetch_real_time: {e}")
        # Return mock data if everything fails
        return [
            {
                "title": "Real-time Content Unavailable",
                "description": "Unable to fetch real-time content at this time. Please try again later.",
                "type": "error",
                "source": "system"
            }
        ]


# 🌐 ROUTE 1 — Fetch
@app.route('/fetch')
def fetch():
    fetch_and_store()
    return jsonify({"message": "Data fetched and stored successfully"})


# 🌐 ROUTE 2 — Test Endpoint
@app.route('/test')
def test():
    return jsonify({"status": "Backend is running", "message": "Hello from the backend!"})


# 🌐 ROUTE 3 — All Content
@app.route('/content')
def get_content():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)


# 🌐 ROUTE 4 — Real-time Content
@app.route('/realtime')
def get_real_time_content():
    try:
        data = fetch_real_time()
        return jsonify(data)
    except Exception as e:
        print(f"Error in real-time endpoint: {e}")
        # Return mock data if there's an error
        mock_data = [
            {
                "title": "Sample Real-time Article",
                "description": "This is a sample article fetched in real-time",
                "type": "news",
                "source": "realtime",
                "url": "#"
            }
        ]
        return jsonify(mock_data)


# 🌐 ROUTE 5 — By Type
@app.route('/content/<content_type>')
def get_by_type(content_type):
    data = list(collection.find({"type": content_type}, {"_id": 0}))
    return jsonify(data)


# 🌐 ROUTE 5b — Latest
@app.route('/latest')
def get_latest():
    data = list(collection.find({}, {"_id": 0}).limit(20))
    return jsonify(data)


# 📰 ROUTE — Inshorts Categories List
@app.route('/categories')
def get_categories():
    INSHORTS_CATEGORIES = [
        {'id': 'all',      'label': 'All',      'icon': 'fa-globe'},
        {'id': 'trending', 'label': 'Trending',  'icon': 'fa-fire'},
        {'id': 'world',    'label': 'World',     'icon': 'fa-earth-americas'},
        {'id': 'war',      'label': 'War',       'icon': 'fa-burst'},
        {'id': 'science',  'label': 'Science',   'icon': 'fa-flask'},
        {'id': 'tech',     'label': 'Tech',      'icon': 'fa-microchip'},
        {'id': 'health',   'label': 'Health',    'icon': 'fa-heart-pulse'},
        {'id': 'business', 'label': 'Business',  'icon': 'fa-briefcase'},
        {'id': 'sports',   'label': 'Sports',    'icon': 'fa-trophy'},
    ]
    return jsonify(INSHORTS_CATEGORIES)


# 📰 ROUTE — Inshorts Live Content by Category
@app.route('/content/inshorts/<category>')
def get_inshorts_content(category):
    """Fetch real-time content for a given Inshorts category."""
    try:
        print(f"\nFetching Inshorts category: [{category}]")
        articles = []

        if category == 'all':
            # Mix of all categories
            for cat in ['trending', 'world', 'science', 'tech', 'health', 'business', 'sports']:
                articles.extend(fetch_rss_by_category(cat, max_items=5))
            articles.extend(fetch_news_by_category('trending', max_items=5))
        elif category == 'war':
            # War only comes from RSS (world feeds filtered by keywords)
            articles = fetch_rss_by_category('war', max_items=25)
        else:
            # RSS is primary, NewsAPI is secondary
            rss_data = fetch_rss_by_category(category, max_items=15)
            news_data = fetch_news_by_category(category, max_items=8)
            seen = {a['title'].lower().strip() for a in rss_data}
            for item in news_data:
                if item['title'].lower().strip() not in seen:
                    rss_data.append(item)
                    seen.add(item['title'].lower().strip())
            articles = rss_data

        # Enrich all articles with credibility scores
        enriched_articles = [enrich_with_credibility(a) for a in articles]

        print(f"  Total for [{category}]: {len(enriched_articles)} items")
        return jsonify(enriched_articles)

    except Exception as e:
        print(f"Inshorts route error [{category}]: {e}")
        return jsonify({'error': str(e), 'items': []}), 500


# 🔒 ROUTE — Auth: Sign Up
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
        
    if users_collection.find({'username': username}):
        # MockCollection returns a list, PyMongo returns a cursor. 
        # Check if any element has matching username if it's mock, else count.
        existing = [u for u in users_collection.find() if u.get('username') == username] if type(users_collection).__name__ == 'MockCollection' else list(users_collection.find({'username': username}))
        if existing:
            return jsonify({'error': 'Username already exists'}), 400

    hashed_pw = generate_password_hash(password)
    new_user = {
        'username': username,
        'password': hashed_pw,
        'bookmarks': [],
        'history': []
    }
    users_collection.insert_one(new_user)
    return jsonify({'message': 'User created successfully', 'username': username}), 201


# 🔒 ROUTE — Auth: Login
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    users = [u for u in users_collection.find() if u.get('username') == username] if type(users_collection).__name__ == 'MockCollection' else list(users_collection.find({'username': username}))
    if not users:
        return jsonify({'error': 'Invalid username or password'}), 401
        
    user = users[0]
    if check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful', 'username': username}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


# 📚 ROUTE — Bookmarks
@app.route('/api/bookmarks', methods=['GET', 'POST'])
def bookmarks():
    username = request.args.get('username') or (request.json and request.json.get('username'))
    if not username:
        return jsonify({'error': 'Username required'}), 400

    users = [u for u in users_collection.find() if u.get('username') == username] if type(users_collection).__name__ == 'MockCollection' else list(users_collection.find({'username': username}))
    if not users:
        return jsonify({'error': 'User not found'}), 404
    user = users[0]

    if request.method == 'GET':
        return jsonify(user.get('bookmarks', []))

    if request.method == 'POST':
        article = request.json.get('article')
        if not article:
            return jsonify({'error': 'Article data required'}), 400
            
        bookmarks = user.get('bookmarks', [])
        # Prevent duplicates based on title
        if not any(b.get('title') == article.get('title') for b in bookmarks):
            bookmarks.insert(0, article)  # Add to top
            
            if type(users_collection).__name__ == 'MockCollection':
                user['bookmarks'] = bookmarks
            else:
                users_collection.update_one(
                    {'username': username},
                    {'$set': {'bookmarks': bookmarks}}
                )
        return jsonify({'message': 'Article bookmarked successfully', 'bookmarks': bookmarks}), 200

# 🕒 ROUTE — History Tracking
@app.route('/api/history', methods=['POST'])
def track_history():
    data = request.json
    username = data.get('username')
    article = data.get('article')
    
    if not username or not article:
        return jsonify({'error': 'Username and article required'}), 400
        
    users = [u for u in users_collection.find() if u.get('username') == username] if type(users_collection).__name__ == 'MockCollection' else list(users_collection.find({'username': username}))
    if not users:
        return jsonify({'error': 'User not found'}), 404
        
    user = users[0]
    history = user.get('history', [])
    
    # Add to beginning of history, but limit to 100 items to save space
    history.insert(0, article)
    history = history[:100]
    
    if type(users_collection).__name__ == 'MockCollection':
        user['history'] = history
    else:
        users_collection.update_one(
            {'username': username},
            {'$set': {'history': history}}
        )
    return jsonify({'message': 'History updated'}), 200

# 👤 ROUTE — User Profile Stats
@app.route('/api/profile/<username>', methods=['GET'])
def get_profile(username):
    users = [u for u in users_collection.find() if u.get('username') == username] if type(users_collection).__name__ == 'MockCollection' else list(users_collection.find({'username': username}))
    if not users:
        return jsonify({'error': 'User not found'}), 404
        
    user = users[0]
    history = user.get('history', [])
    
    # Calculate stats
    total_read = len(history)
    
    # Most viewed category
    cat_counts = {}
    for article in history:
        cat = article.get('category', article.get('inshorts_category', 'general')).lower()
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        
    most_viewed_category = 'None'
    if cat_counts:
        most_viewed_category = max(cat_counts, key=cat_counts.get).title()
        
    return jsonify({
        'username': username,
        'total_read': total_read,
        'most_viewed_category': most_viewed_category,
        'history': history[:20]  # Return recent 20 for UI
    }), 200



@app.route('/progress')
def get_progress():
    return jsonify(user_profile)

# 🌐 ROUTE 7 — Mark Content as Read
@app.route('/read/<int:item_id>', methods=['POST'])
def mark_as_read(item_id):
    global user_profile

    # Get content type
    data = list(collection.find({}, {"_id": 0}))
    if item_id >= len(data):
        return jsonify({"error": "Item not found"})

    item = data[item_id]
    content_type = item.get("type", "unknown")

    # Update user progress
    if content_type == "video":
        user_profile["videos_watched"] += 1
        user_profile["xp"] += 10
    elif content_type in ["news", "blog"]:
        user_profile["articles_read"] += 1
        user_profile["xp"] += 5

    # Level up logic
    xp_needed = user_profile["level"] * 100
    if user_profile["xp"] >= xp_needed:
        user_profile["level"] += 1

    # Save to DB
    users_collection.update_one(
        {"user_id": "default_user"},
        {"$set": user_profile},
        upsert=True
    )

    return jsonify({"message": "Progress updated", "profile": user_profile})


# 🌐 ROUTE 10 — Semantic Search
@app.route('/search', methods=['POST'])
def semantic_search():
    query = request.json.get('query', '')
    if not query:
        return jsonify({"error": "No query provided"})

    if not OPENAI_AVAILABLE:
        return jsonify({"error": "OpenAI API not configured"})

    # Use GPT to understand the intent and find relevant content
    prompt = f"Based on the user's query: '{query}', suggest relevant topics from: science, technology, education, research, history, news, politics. Return only the most relevant topic."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        topic = response.choices[0].message.content.strip()

        # Find content related to the topic
        data = list(collection.find({"$or": [
            {"title": {"$regex": topic, "$options": "i"}},
            {"description": {"$regex": topic, "$options": "i"}}
        ]}, {"_id": 0}).limit(10))

        return jsonify({"topic": topic, "results": data})
    except Exception as e:
        return jsonify({"error": str(e)})


# 🌐 ROUTE 11 — Summarize Content
@app.route('/summarize/<int:item_id>', methods=['GET'])
def summarize_content(item_id):
    # For simplicity, using index as id
    data = list(collection.find({}, {"_id": 0}))
    if item_id >= len(data):
        return jsonify({"error": "Item not found"})

    item = data[item_id]
    text = item.get("title", "") + " " + item.get("description", "")

    if not OPENAI_AVAILABLE:
        return jsonify({"error": "OpenAI API not configured"})

    try:
        prompt = f"Summarize this content in 100 words: {text}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        summary = response.choices[0].message.content.strip()

        return jsonify({"summary": summary, "original": item})
    except Exception as e:
        return jsonify({"error": str(e)})


# 🌐 ROUTE 12 — Summarize Real-time Content
@app.route('/summarize_realtime', methods=['POST'])
def summarize_real_time_content():
    item = request.json
    if not item:
        return jsonify({"error": "No content provided"})

    text = item.get("title", "") + " " + item.get("description", "")

    if not OPENAI_AVAILABLE:
        return jsonify({"error": "OpenAI API not configured"})

    try:
        prompt = f"Summarize this content in 100 words: {text}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        summary = response.choices[0].message.content.strip()

        return jsonify({"summary": summary, "original": item})
    except Exception as e:
        return jsonify({"error": str(e)})


# ⏱️ TIMER ROUTE 1
@app.route("/start_timer/<int:minutes>")
def start_timer(minutes):
    start_time = time.time()
    end_time = start_time + minutes * 60

    sessions["user"] = {
        "start": start_time,
        "end": end_time
    }

    return jsonify({
        "message": f"Timer started for {minutes} minutes"
    })


# ⏱️ TIMER ROUTE 2
@app.route("/timer_status")
def timer_status():
    session = sessions.get("user")

    if not session:
        return jsonify({"status": "no active timer"})

    remaining = int(session["end"] - time.time())

    if remaining <= 0:
        return jsonify({"status": "ended", "remaining": 0})

    return jsonify({
        "status": "running",
        "remaining": remaining
    })


# ▶️ RUN SERVER (ALWAYS LAST)
if __name__ == '__main__':
    app.run(debug=True)