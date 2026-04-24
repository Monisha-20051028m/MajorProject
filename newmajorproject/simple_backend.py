#!/usr/bin/env python3
"""
Enhanced Productivity App Backend - Uses real APIs with educational filtering
"""

from flask import Flask, jsonify, request
import time
import json
import os

# API fetchers are imported lazily inside load_content()
from utils.filter import filter_content_batch

# Try to import OpenAI for AI summaries
try:
    import openai
    OPENAI_AVAILABLE = True
    # Set your OpenAI API key here
    openai.api_key = os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here')
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI not available - summaries will be basic text extraction")

app = Flask(__name__)

# Allow cross-origin access from the frontend server
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# In-memory storage for content and user data
content_store = []
user_progress = {
    "articles_read": 0,
    "videos_watched": 0,
    "time_spent": 0,
    "level": 1,
    "xp": 0
}

# Timer sessions storage
active_sessions = {}

def load_content():
    """Load and filter educational content from APIs"""
    global content_store

    if not content_store:  # Only fetch if we don't have content
        print("🔄 Fetching fresh educational content from APIs...")

        try:
            # Import fetchers lazily to avoid startup failure when dependencies are missing
            from backend.fetch.youtube import fetch_youtube
            from backend.fetch.news import fetch_news
            from backend.fetch.rss import fetch_rss

            # Fetch from all sources
            youtube_data = fetch_youtube()
            news_data = fetch_news()
            rss_data = fetch_rss()

            # Combine all data
            all_content = youtube_data + news_data + rss_data

            # Filter for educational content only
            educational_content = filter_content_batch(all_content)

            # Store filtered content
            content_store = educational_content

            print(f"✅ Loaded {len(content_store)} educational items")

        except Exception as e:
            print(f"❌ Error loading content: {e}")
            # Fallback to mock data
            content_store = get_mock_educational_content()

    return content_store

def get_mock_educational_content():
    """Fallback mock data - only educational content"""
    return [
        {
            "title": "Introduction to Machine Learning Algorithms",
            "description": "Comprehensive guide to supervised and unsupervised learning techniques, including neural networks and deep learning fundamentals",
            "type": "video",
            "source": "youtube",
            "category": "technology"
        },
        {
            "title": "Quantum Mechanics: Wave Functions and Probability",
            "description": "Understanding the mathematical foundations of quantum physics, wave-particle duality, and quantum measurement theory",
            "type": "video",
            "source": "youtube",
            "category": "science"
        },
        {
            "title": "CRISPR Gene Editing Technology Breakthrough",
            "description": "Latest developments in genetic engineering, with potential applications in medicine, agriculture, and biotechnology research",
            "type": "news",
            "source": "newsapi",
            "category": "biology"
        },
        {
            "title": "Climate Change: Scientific Evidence and Solutions",
            "description": "Analysis of global warming data, greenhouse gas emissions, and renewable energy transition strategies for sustainability",
            "type": "blog",
            "source": "rss",
            "category": "environment"
        },
        {
            "title": "The Mathematics of Artificial Intelligence",
            "description": "Linear algebra, calculus, and probability theory essential for understanding modern AI algorithms and machine learning models",
            "type": "blog",
            "source": "rss",
            "category": "mathematics"
        },
        {
            "title": "Neuroscience: Brain Plasticity and Learning",
            "description": "How neural connections change with experience, memory formation, and cognitive development throughout life",
            "type": "video",
            "source": "youtube",
            "category": "psychology"
        },
        {
            "title": "The History of Ancient Civilizations",
            "description": "Exploring the rise and fall of ancient civilizations, from Mesopotamia to the Roman Empire, and their lasting impact on modern society",
            "type": "video",
            "source": "youtube",
            "category": "history"
        },
        {
            "title": "World War II: Key Events and Turning Points",
            "description": "Comprehensive analysis of the major events, battles, and political decisions that shaped the outcome of World War II",
            "type": "blog",
            "source": "rss",
            "category": "history"
        },
        {
            "title": "Latest Advances in Artificial Intelligence Research",
            "description": "Cutting-edge developments in AI, machine learning, and neural networks from top research institutions worldwide",
            "type": "news",
            "source": "newsapi",
            "category": "technology"
        },
        {
            "title": "Research Methods in Social Sciences",
            "description": "Comprehensive guide to qualitative and quantitative research methodologies used in social science studies",
            "type": "blog",
            "source": "rss",
            "category": "research"
        },
        {
            "title": "The Future of Machine Learning",
            "description": "Exploring upcoming trends and breakthroughs in machine learning technology and applications",
            "type": "video",
            "source": "youtube",
            "category": "technology"
        }
    ]

# Routes
@app.route('/')
def home():
    return jsonify({
        "message": "Educational Productivity App Backend",
        "status": "Running with real API data",
        "features": ["Educational content filtering", "YouTube API", "NewsAPI", "RSS feeds"]
    })

@app.route('/content')
def get_content():
    """Get all educational content"""
    content = load_content()
    return jsonify(content)

@app.route('/content/<content_type>')
def get_by_type(content_type):
    """Get content filtered by type (video, news, blog)"""
    content = load_content()
    filtered = [item for item in content if item.get("type") == content_type]
    return jsonify(filtered)

@app.route('/content/category/<category>')
def get_by_category(category):
    """Get content filtered by educational category"""
    content = load_content()
    filtered = [item for item in content if item.get("category") == category]
    return jsonify(filtered)

@app.route('/fetch')
def fetch():
    """Fetch fresh content from all APIs"""
    global content_store
    try:
        # Clear existing content to force refresh
        content_store = []

        # Load fresh content
        new_content = load_content()

        return jsonify({
            "message": "Fresh educational content fetched from APIs",
            "total_items": len(new_content),
            "sources": ["YouTube", "NewsAPI", "RSS feeds"],
            "filtered": "educational_only"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to fetch content, using fallback data"
        }), 500

@app.route('/search', methods=['POST'])
def semantic_search():
    """Category-aware search with fallback to keyword matching"""
    query = request.json.get('query', '').lower().strip()
    content = load_content()

    if not query:
        return jsonify({
            "query": query,
            "results": [],
            "total_found": 0,
            "message": "Empty search query"
        })

    # Import categories from filter module
    from utils.filter import PRODUCTIVE_CATEGORIES

    # Check if query matches a known category
    matching_category = None
    for category in PRODUCTIVE_CATEGORIES:
        if query == category.lower():
            matching_category = category
            break

    results = []

    if matching_category:
        # Category-based search: return content classified under this category
        for item in content:
            item_category = item.get('category', '').lower()
            if item_category == matching_category.lower():
                results.append(item)
        
        return jsonify({
            "query": query,
            "results": results[:10],  # Return top 10 results
            "total_found": len(results),
            "search_type": "category",
            "matched_category": matching_category
        })

    else:
        # Keyword-based search (improved - more flexible)
        query_words = [word for word in query.split() if word.strip()]
        for item in content:
            title = item.get('title', '').lower()
            description = item.get('description', '').lower()
            category = item.get('category', '').lower()
            full_text = f"{title} {description} {category}"

            # Check if any of the query words appear in the content
            # This is more flexible than requiring ALL words
            if any(word in full_text for word in query_words):
                results.append(item)

        return jsonify({
            "query": query,
            "results": results[:10],  # Return top 10 results
            "total_found": len(results),
            "search_type": "keyword",
            "message": f"Keyword search for: {query}"
        })

@app.route('/progress')
def get_progress():
    """Get user progress"""
    return jsonify(user_progress)

@app.route('/progress/update', methods=['POST'])
def update_progress():
    """Update user progress"""
    data = request.json
    global user_progress

    if 'xp' in data:
        user_progress['xp'] += data['xp']
        user_progress['level'] = (user_progress['xp'] // 100) + 1

    if 'articles_read' in data:
        user_progress['articles_read'] += data['articles_read']

    if 'videos_watched' in data:
        user_progress['videos_watched'] += data['videos_watched']

    if 'time_spent' in data:
        user_progress['time_spent'] += data['time_spent']

    return jsonify(user_progress)

@app.route('/start_timer/<int:minutes>')
def start_timer(minutes):
    """Start a focus timer session"""
    session_id = f"session_{int(time.time())}"
    end_time = time.time() + (minutes * 60)

    active_sessions[session_id] = {
        "start_time": time.time(),
        "end_time": end_time,
        "duration": minutes,
        "active": True
    }

    return jsonify({
        "session_id": session_id,
        "end_time": end_time,
        "message": f"{minutes}-minute focus session started"
    })

@app.route('/timer_status')
def timer_status():
    """Check timer status"""
    active_sessions_list = []
    current_time = time.time()

    for session_id, session_data in active_sessions.items():
        if session_data['active']:
            remaining = max(0, session_data['end_time'] - current_time)
            if remaining <= 0:
                session_data['active'] = False
                # Award XP for completing session
                user_progress['xp'] += 10
                user_progress['level'] = (user_progress['xp'] // 100) + 1

            active_sessions_list.append({
                "session_id": session_id,
                "remaining_seconds": remaining,
                "completed": remaining <= 0
            })

    return jsonify({
        "active_sessions": active_sessions_list,
        "user_progress": user_progress
    })

@app.route('/stats')
def get_stats():
    """Get application statistics"""
    content = load_content()
    stats = {
        "total_content": len(content),
        "content_by_type": {},
        "content_by_category": {},
        "user_progress": user_progress,
        "active_sessions": len([s for s in active_sessions.values() if s['active']])
    }

    # Count by type and category
    for item in content:
        item_type = item.get('type', 'unknown')
        item_category = item.get('category', 'general')

        stats['content_by_type'][item_type] = stats['content_by_type'].get(item_type, 0) + 1
        stats['content_by_category'][item_category] = stats['content_by_category'].get(item_category, 0) + 1

    return jsonify(stats)

@app.route('/summarize/<int:item_id>', methods=['GET'])
def summarize_content(item_id):
    """AI-powered content summarization"""
    try:
        content = load_content()

        if item_id < 0 or item_id >= len(content):
            return jsonify({"error": "Content item not found"}), 404

        item = content[item_id]
        title = item.get('title', 'No title')
        description = item.get('description', 'No description')

        # Combine title and description for summarization
        text_to_summarize = f"{title}. {description}"

        if OPENAI_AVAILABLE and openai.api_key != 'your_openai_api_key_here':
            try:
                # Use OpenAI GPT for intelligent summarization
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert at creating concise, educational summaries. Summarize the given content in 2-3 sentences, focusing on the key educational points."},
                        {"role": "user", "content": f"Please summarize this educational content:\n\n{text_to_summarize}"}
                    ],
                    max_tokens=150,
                    temperature=0.3
                )
                summary = response.choices[0].message.content.strip()
                summary_type = "ai"

            except Exception as e:
                print(f"OpenAI error: {e}")
                # Fallback to basic summary
                summary = f"{title[:100]}... {description[:200]}..."
                summary_type = "basic"
        else:
            # Basic text extraction fallback
            summary = f"{title[:100]}... {description[:200]}..."
            summary_type = "basic"

        return jsonify({
            "item_id": item_id,
            "title": title,
            "summary": summary,
            "summary_type": summary_type,
            "word_count": len(summary.split()),
            "content_type": item.get('type', 'unknown')
        })

    except Exception as e:
        return jsonify({
            "error": f"Failed to generate summary: {str(e)}",
            "item_id": item_id
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Educational Productivity App Backend...")
    print("📡 Server will run on http://127.0.0.1:5000")
    print("🎯 Features: Real API data, Educational filtering, Progress tracking")
    print("Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=5000)