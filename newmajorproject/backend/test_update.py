from db import users_collection
user = users_collection.find_one({'username': 'testuser123'})
print('Before:', user.get('history'))
users_collection.update_one({'username': 'testuser123'}, {'$set': {'history': [{'title': 'test'}]}})
user2 = users_collection.find_one({'username': 'testuser123'})
print('After:', user2.get('history'))
