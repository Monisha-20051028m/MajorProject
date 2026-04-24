from pymongo import MongoClient

# 🔑 Replace with your actual MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://admin:laya123@cluster0.awr7pjx.mongodb.net/?appName=Cluster0"

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)

# 📦 Create / access database
db = client["productivity_app"]

# 📂 Create / access collection
collection = db["content"]