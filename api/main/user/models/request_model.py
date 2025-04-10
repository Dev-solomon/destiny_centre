from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection

# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]


class Request:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
    }

    def __init__(self, name: str, email: str, pr: str):
        self.name = name
        self.email = email
        self.pr = pr

# Set the collection reference
Request.collection = db['requests']  # Replace 'requests' with your collection name
# Update validator for 'products' collection
db.command({
    'collMod': 'requests',
    'validator': {'$jsonSchema': Request.schema}
})





