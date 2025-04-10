from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection

# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]


class User:
    collection: Collection
    
    # Define schema validation rules
    schema = {
        'bsonType': 'object',
        'required': ['email','password'],
        'properties': {
            'email': {
                'bsonType': 'string'
            },
            'password': {
                'bsonType': 'string'
            }
            # Define other properties here
        }
    }

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

# Set the collection reference
User.collection = db['users']  # Replace 'users' with your collection name
# Update validator for 'products' collection
db.command({
    'collMod': 'users',
    'validator': {'$jsonSchema': User.schema}
})





