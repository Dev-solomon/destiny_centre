from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection

# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]


class Sunday:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
    }

    def __init__(self, service: str):
        self.service = service

# Set the collection reference
Sunday.collection = db['sundays']  # Replace 'sundays' with your collection name
# Update validator for 'products' collection
db.command({
    'collMod': 'sundays',
    'validator': {'$jsonSchema': Sunday.schema}
})





