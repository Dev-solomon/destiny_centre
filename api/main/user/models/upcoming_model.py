from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection

# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]


class Upcoming:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
    }

    def __init__(self, title: str, location: str, date: str, time: str):
        self.title = title
        self.location = location
        self.date = date
        self.time = time

# Set the collection reference
Upcoming.collection = db['upcomings']  # Replace 'upcomings' with your collection name
# Update validator for 'products' collection
db.command({
    'collMod': 'upcomings',
    'validator': {'$jsonSchema': Upcoming.schema}
})





