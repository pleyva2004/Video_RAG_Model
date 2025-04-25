from pymongo import MongoClient

# Connect
client = MongoClient("mongodb://video_rag:video_rag@localhost:27017/")
db = client["video_rag"]
collection = db["segments"]

def MongoInsert(segment_list):
    collection.insert_many(segment_list)

def MongoRetrieve():
    segments = collection.find()
    return segments

def MongoDeleteAll():
    collection.delete_many({})
