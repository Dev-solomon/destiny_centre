from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from main.user.models.sermon_model import Sermon
from main.user.models.prayer_model import Prayer
from main.user.models.request_model import Request
from main.user.models.meeting_model import Meeting
from main.user.models.testimony_model import Testimony
from main.user.models.upcoming_model import Upcoming
from main.user.models.sunday_model import Sunday
from flask import current_app as app 
from bson import ObjectId
import datetime
import os
from pymongo import  DESCENDING
from werkzeug.utils import secure_filename
from main.tools import upload_sermon_image



def get_daily_prayer():
    try:
        dp = list(Prayer.collection.find({}).sort('_id', -1).limit(1))  # Sort in descending order and get the first document
        if dp:
            # print(dp)
            return dp[0]  # Return the first document if found
        return None
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
def get_upcoming_events():
    try:
        events = list(Upcoming.collection.find({}).sort('_id', -1).limit(1))  # Sort in descending order and get the first document
        if events:
            # print(events)
            return events[0]  # Return the first document if found
        return None
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
def home_video():
    try:
        vid = list(Sunday.collection.find({}).sort('_id', -1).limit(1))  # Sort in descending order and get the first document
        if vid:
            # print(vid)
            return vid[0]  # Return the first document if found
        return None
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    
def get_sermons(pageNum):
    try:
        pageSize = 9
        skip = (int(pageNum) - 1) * pageSize
        
         # Count the total number of matching products (for pagination calculation)
        total_count = Sermon.collection.count_documents({})
        
        # Calculate total pages
        total_pages = (total_count + pageSize - 1) // pageSize  # Equivalent to ceiling division
        
        sermons = list(Sermon.collection.find({}).sort('createdAt', DESCENDING).limit(pageSize).skip(skip))  # Sort in descending order and get the first document
        if sermons:
            # print(sermons)
            return [sermons, total_count]  # Return the documents if found
        return None
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    
def get_a_sermon(sermon_id):
    try:
        
        sermon = Sermon.collection.find_one({"_id": ObjectId(sermon_id)})  # Sort in descending order and get the first document
        if sermon:
            # print(sermon)
            return sermon  # Return the documents if found
        return None
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    
