from db import users_collection
username = 'testuser123'
users = list(users_collection.find({'username': username}))
user = users[0]
history = user.get('history', [])
article = {'title': 'test from app logic'}
history.insert(0, article)
history = history[:100]
print("Before update, history:", history)

result = users_collection.update_one(
    {'username': username},
    {'$set': {'history': history}}
)
print("Matched count:", result.matched_count)
print("Modified count:", result.modified_count)

user2 = users_collection.find_one({'username': username})
print('After from DB:', user2.get('history'))
