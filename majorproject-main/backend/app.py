import time
from flask import Flask, jsonify
from datetime import datetime

from db import collection
from fetch.youtube import fetch_youtube
from fetch.news import fetch_news
from fetch.rss import fetch_rss
from utils.filter import is_useful

app = Flask(__name__)

sessions = {}


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


# 🌐 ROUTE 1 — Fetch
@app.route('/fetch')
def fetch():
    fetch_and_store()
    return jsonify({"message": "Data fetched and stored successfully"})


# 🌐 ROUTE 2 — All Content
@app.route('/content')
def get_content():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)


# 🌐 ROUTE 3 — By Type
@app.route('/content/<content_type>')
def get_by_type(content_type):
    data = list(collection.find({"type": content_type}, {"_id": 0}))
    return jsonify(data)


# 🌐 ROUTE 4 — Latest
@app.route('/latest')
def get_latest():
    data = list(collection.find({}, {"_id": 0}).limit(20))
    return jsonify(data)


# 🌐 ROUTE 5 — Home
@app.route('/')
def home():
    return "Backend is running 🚀"


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