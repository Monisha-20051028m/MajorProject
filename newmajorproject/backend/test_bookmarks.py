import requests

payload = {
    'username': 'testuser123',
    'article': {
        'title': 'Test Bookmark from Script',
    }
}
try:
    res = requests.post('http://127.0.0.1:5000/api/bookmarks', json=payload)
    print("Response code:", res.status_code)
    print("Response text:", res.text)
except Exception as e:
    print("Error:", e)
