from db import users_collection
users = list(users_collection.find({}, {'_id': 0}))
print(f'Total users: {len(users)}')
for u in users:
    print(f"User: {u.get('username')}")
    print(f"History len: {len(u.get('history', []))}")
