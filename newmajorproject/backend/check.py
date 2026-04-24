from db import users_collection

users = list(users_collection.find({}, {'_id': 0}))
print(f"Total users found in MongoDB: {len(users)}")
for u in users:
    print(f"User: {u.get('username')}")
    print(f"Bookmarks: {len(u.get('bookmarks', []))}")
    if u.get('bookmarks'):
        print(f"Latest Bookmark: {u['bookmarks'][0].get('title')}")
    print("-" * 20)
