from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection

# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]


class Meeting:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
    }

    def __init__(self, meeting_type: str, name: str, email: str, phone: str, date_schdeule: str, time: str):
        self.meeting_type = meeting_type
        self.name = name
        self.email= email
        self.phone = phone
        self.date_schedule = date_schdeule
        self.time = time

# Set the collection reference
Meeting.collection = db['meetings']  # Replace 'meetings' with your collection name
# Update validator for 'products' collection 
db.command({
    'collMod': 'meetings',
    'validator': {'$jsonSchema': Meeting.schema}
})





