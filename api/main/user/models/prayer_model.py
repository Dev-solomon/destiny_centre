from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection

# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]


class Prayer:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
    }

    def __init__(self, prayer: str, verse: str, image: str):
        self.prayer = prayer
        self.verse = verse
        self.image = image
        
# Set the collection reference
Prayer.collection = db['prayers']  # Replace 'prayers' with your collection name
# Update validator for 'products' collection
db.command({
    'collMod': 'prayers',
    'validator': {'$jsonSchema': Prayer.schema}
})





