from pymongo import MongoClient

# 🔑 Replace with your actual MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://monisha:monisha123@cluster0.4pdbqpn.mongodb.net/?appName=Cluster0"

try:
    # Connect to MongoDB Atlas
    client = MongoClient(MONGO_URI)
    # Test the connection
    client.admin.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    print("Using mock database (data will not persist)")
    # Create a mock client that doesn't actually connect
    client = None

# 📦 Create / access database
if client:
    db = client["productivity_app"]
    collection = db["content"]
    users_collection = db["users"]
else:
    # Mock collections for development
    class MockCollection:
        def __init__(self):
            self.data = []

        def find(self, query=None, projection=None):
            return self.data

        def update_one(self, query, update, upsert=False):
            # Mock update - doesn't actually persist
            pass

        def insert_one(self, doc):
            self.data.append(doc)

    collection = MockCollection()
    users_collection = MockCollection()