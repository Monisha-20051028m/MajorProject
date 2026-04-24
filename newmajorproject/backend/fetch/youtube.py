from googleapiclient.discovery import build

API_KEY = "AIzaSyDT1udI7gyLZ-FiF4pyQQ_ChwXVTg_uNd8"

def fetch_youtube():
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        # Educational search queries
        search_queries = [
            "educational science technology",
            "learn programming tutorial",
            "physics chemistry biology explained",
            "mathematics calculus algebra",
            "computer science algorithms",
            "artificial intelligence explained",
            "quantum physics mechanics",
            "machine learning tutorial",
            "data science statistics",
            "history civilization explained",
            "geography earth science",
            "astronomy space exploration",
            "economics finance explained",
            "psychology neuroscience",
            "medical science health",
            "environmental science climate"
        ]

        all_videos = []

        # Fetch from multiple queries to get diverse educational content
        for query in search_queries[:3]:  # Limit to 3 queries to avoid quota issues
            try:
                request = youtube.search().list(
                    part="snippet",
                    q=query,
                    type="video",
                    maxResults=5,
                    order="relevance",
                    safeSearch="strict",
                    videoDuration="medium",  # Prefer longer, more educational videos
                    relevanceLanguage="en"
                )

                response = request.execute()

                for item in response.get('items', []):
                    # Skip if video is too short (likely not educational)
                    duration = get_video_duration(youtube, item['id']['videoId'])
                    if duration and duration < 180:  # Skip videos shorter than 3 minutes
                        continue

                    video_data = {
                        "title": item['snippet']['title'],
                        "description": item['snippet']['description'],
                        "type": "video",
                        "source": "youtube",
                        "video_id": item['id']['videoId'],
                        "channel_title": item['snippet']['channelTitle'],
                        "published_at": item['snippet']['publishedAt'],
                        "thumbnail": item['snippet']['thumbnails'].get('medium', {}).get('url', ''),
                        "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                    }
                    all_videos.append(video_data)

            except Exception as e:
                print(f"Error fetching query '{query}': {e}")
                continue

        # Remove duplicates based on video ID
        unique_videos = []
        seen_ids = set()
        for video in all_videos:
            if video['video_id'] not in seen_ids:
                seen_ids.add(video['video_id'])
                unique_videos.append(video)

        print(f"Fetched {len(unique_videos)} educational videos from YouTube")
        return unique_videos[:20]  # Return top 20 videos

    except Exception as e:
        print(f"YouTube API error: {e}")
        # Return mock educational data if API fails
        return [
            {
                "title": "Introduction to Machine Learning - Full Course",
                "description": "Complete beginner's guide to machine learning algorithms, neural networks, and practical applications in Python",
                "type": "video",
                "source": "youtube",
                "category": "technology"
            },
            {
                "title": "Quantum Physics for Everyone",
                "description": "Understanding quantum mechanics, superposition, entanglement, and quantum computing basics",
                "type": "video",
                "source": "youtube",
                "category": "science"
            },
            {
                "title": "The History of Ancient Civilizations",
                "description": "Comprehensive exploration of ancient Egypt, Greece, Rome, and Mesopotamia",
                "type": "video",
                "source": "youtube",
                "category": "history"
            },
            {
                "title": "Climate Change Science Explained",
                "description": "Scientific evidence, causes, and solutions for global climate change",
                "type": "video",
                "source": "youtube",
                "category": "environment"
            }
        ]

def get_video_duration(youtube, video_id):
    """
    Get video duration in seconds
    """
    try:
        request = youtube.videos().list(
            part="contentDetails",
            id=video_id
        )
        response = request.execute()

        if response['items']:
            duration_str = response['items'][0]['contentDetails']['duration']
            # Parse ISO 8601 duration (PT4M13S = 4 minutes 13 seconds)
            import re
            match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
            if match:
                hours = int(match.group(1) or 0)
                minutes = int(match.group(2) or 0)
                seconds = int(match.group(3) or 0)
                return hours * 3600 + minutes * 60 + seconds
    except Exception as e:
        print(f"Error getting video duration: {e}")

    return None