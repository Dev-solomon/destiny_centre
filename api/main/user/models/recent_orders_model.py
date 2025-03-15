from flask import current_app as app
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime

# Assuming you have a MongoDB connection URI
client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]

class RecentOrder:
    collection: Collection
    
    schema = {
        'bsonType': 'object',
        'required': ['order_id','order_num','status'],
        'properties': {
            'order_id': {
                'bsonType': 'string'
            },
            'order_num': {
                'bsonType': 'string'
            },
            'status': {
                'bsonType': 'string',
            }
            # Define other properties here
        }
    }
    
    def __init__(self, order_id: str, order_num: str, status: str):
        self.order_id = order_id
        self.order_num = order_num
        self.status = status
        self.created_at = datetime.datetime.utcnow() # Assuming you want to add a timestamp



# Set the collection reference
RecentOrder.collection = db['recent_orders']
# Update validator for 'products' collection
db.command({
    'collMod': 'recent_orders',
    'validator': {'$jsonSchema': RecentOrder.schema}
})



