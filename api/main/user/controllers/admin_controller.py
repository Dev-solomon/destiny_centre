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
import datetime
import os
from werkzeug.utils import secure_filename
from main.tools import upload_sermon_image



def upload_sermon():
    try:
        data = request.get_json()
        files = request.files.get('image')
        
        # code for saving file uploaded in profile
        file_path = os.path.join('uploads/', secure_filename(files.filename))
        files.save(file_path)
        
        # upload file to cloudinary for storage there
        image_url = upload_sermon_image(file_path)
        if (image_url != False):
            # Remove the file after successful upload
            os.remove(file_path)
            print(f"Local file removed: {file_path}")
            
            data['image'] = image_url
            data['createdAt'] = datetime.datetime.now().isoformat()
            sermon = Sermon.collection.find_one({'title': data['title']})
            if (sermon):
                return "This Sermon Already Exists!"
            else:
                new_sermon = Sermon.collection.insert_one(data).inserted_id
                created_sermon = Sermon.collection.find_one({'title': data['title']})
                if(created_sermon):
                    return "Sermon Added Sucessfully"
                else:
                    return "Error Added New Sermon, Try again!"
        return "Error Added New Sermon, Try again!"
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    
def send_prayer_request():
    try:
        data = request.form.to_dict()
        data['prayed'] = False
        data['createdAt'] = datetime.datetime.now().isoformat()
       
        
       
        new_pr = Request.collection.insert_one(data).inserted_id
        created_pr = Request.collection.find_one({'pr': data['pr']})
        if(created_pr):
            return "Your Prayer Request Has Been Sent"
        else:
                return "Error In Sending Request, Try again!"
    except Exception as e:
        return jsonify({'message': str(e)}), 400


def schedule_meeting():
    try:
        data = request.form.to_dict()
        data['met'] = False
        data['createdAt'] = datetime.datetime.now().isoformat()
       
        
       
        new_meeting = Meeting.collection.insert_one(data)
        if(new_meeting.acknowledged):
            return "Your Meeting Has Been Scheduled"
        else:
                return "Error In Scheduling a New Meeting, Try again!"
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
def share_testimony():
    try:
        data = request.form.to_dict()
        data['createdAt'] = datetime.datetime.now().isoformat()
       
        
       
        new_testimony = Testimony.collection.insert_one(data)
        if(new_testimony.acknowledged):
            return "Thank You For Sharing God's Faithfulness To Others"
        else:
                return "Sharing Your Testimony Failed, Try again!"
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    
def create_event():
    try:
        data = request.get_json()
        data['createdAt'] = datetime.datetime.now().isoformat()
       
        
       
        created_event = Upcoming.collection.insert_one(data)
        if(created_event.acknowledged):
            return "You Have Added A New Event"
        else:
                return "Event Addition Failed, Try again!"
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    
    
def pray_daily():
    try:
        data = request.form.to_dict()
        files = request.files.get('image')
        
        # code for saving file uploaded in profile
        file_path = os.path.join('uploads/', secure_filename(files.filename))
        files.save(file_path)
        
        # upload file to cloudinary for storage there
        image_url = upload_sermon_image(file_path)
        if (image_url != False):
            # Remove the file after successful upload
            os.remove(file_path)
            print(f"Local file removed: {file_path}")
            
            data['image'] = image_url
            data['createdAt'] = datetime.datetime.now().isoformat()
            created_prayer = Prayer.collection.insert_one(data)
            if(created_prayer.acknowledged):
                return "Daily Prayer Has Uploaded Successfully"
            else:
                    return "Failed To Add Daily Prayers, Try again!"
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
def service():
    try:
        data = request.form.to_dict()
        data['createdAt'] = datetime.datetime.now().isoformat()
       
        
        last_sunday = Sunday.collection.insert_one(data)
        if(last_sunday.acknowledged):
            return "Last Sunday Video Inserted"
        else:
                return "Failed To Insert Last Sunday Service, Try again!"
    except Exception as e:
        return jsonify({'message': str(e)}), 400