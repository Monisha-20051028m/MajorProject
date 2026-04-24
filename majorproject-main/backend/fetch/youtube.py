from googleapiclient.discovery import build

API_KEY = "AIzaSyAf0JkRknDkd2TtltOH-ThOpwxSualcvd4"   # <-- put your key here

def fetch_youtube():
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    request = youtube.search().list(
        part="snippet",
        q="science OR technology OR education",
        type="video",
        maxResults=10
    )

    response = request.execute()

    data = []

    for item in response.get('items', []):
        data.append({
            "title": item['snippet']['title'],
            "description": item['snippet']['description'],
            "type": "video",
            "source": "youtube"
        })

    return data