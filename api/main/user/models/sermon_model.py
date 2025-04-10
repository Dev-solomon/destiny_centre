from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection

# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]


class Sermon:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
    }

    def __init__(self, title: str, speaker: str, audio: str, message: str):
        self.title = title
        self.speaker = speaker
        self.audio = audio
        self.message = message

# Set the collection reference
Sermon.collection = db['sermons']  # Replace 'sermons' with your collection name
# Update validator for 'products' collection
db.command({
    'collMod': 'sermons',
    'validator': {'$jsonSchema': Sermon.schema}
})





