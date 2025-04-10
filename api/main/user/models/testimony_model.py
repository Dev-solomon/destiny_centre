from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection

# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]


class Testimony:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
    }

    def __init__(self, name: str, email: str, testimony: str):
        self.name = name
        self.email = email
        self.testimony = testimony

# Set the collection reference
Testimony.collection = db['testimonies']  # Replace 'testimonies' with your collection name
# Update validator for 'products' collection
db.command({
    'collMod': 'testimonies',
    'validator': {'$jsonSchema': Testimony.schema}
})





