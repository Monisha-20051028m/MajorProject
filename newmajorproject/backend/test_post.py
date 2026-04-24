import requests
import json

payload = {
    'username': 'testuser123',
    'article': {
        'title': 'Test Article from Script',
        'category': 'science',
        'source': 'test'
    }
}
try:
    res = requests.post('http://127.0.0.1:5000/api/history', json=payload)
    print("Response code:", res.status_code)
    print("Response text:", res.text)
except Exception as e:
    print("Error:", e)
