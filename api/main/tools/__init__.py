from flask import current_app as app
from pytz import timezone, UTC
from datetime import timedelta
import datetime
import random
import uuid
import cloudinary
import os
import cloudinary.api   
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

def nowDatetimeUserTimezone(user_timezone):
	tzone = timezone(user_timezone)
	return datetime.datetime.now(tzone)

def nowDatetimeUTC():
	tzone = UTC
	now = datetime.datetime.now(tzone)
	return now

def JsonResp(data, status):
	from flask import Response
	from bson import json_util
	import json
	return Response(json.dumps(data, default=json_util.default), mimetype="application/json", status=status)

def randID():
	randId = uuid.uuid4().hex
	return randId

def randString(length):
	randString = ""
	for _ in range(length):
		randString += random.choice("AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890")

	return randString

def randStringCaps(length):
	randString = ""
	for _ in range(length):
		randString += random.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789")

	return randString

def randStringNumbersOnly(length):
	randString = ""
	for _ in range(length):
		randString += random.choice("23456789")

	return randString

def validEmail(email):
	import re

	if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
		return True
	else:
		return False

cloudinary.config(
       cloud_name="dns8ckviy",
       api_key=os.getenv('cloudinary_api_key'),
       api_secret=os.getenv('cloudinary_api_secret')
)

# this is for sermon upload image through api
def upload_sermon_image(file_path):
# Example usage
# uploaded_image_url = upload_image("path/to/your/image.jpg")

# Upload from a remote URL
# response = cloudinary.uploader.upload("https://example.com/image.jpg")

# Upload with options (e.g., specifying a folder or tags)
# response = cloudinary.uploader.upload("path/to/image.jpg", folder="my_images", tags=["sample", "test"])
    try: 
        # Upload the image to Cloudinary
        response = cloudinary.uploader.upload(file_path, folder="destiny_centre/images")
        
        # Get the URL of the uploaded image
        url = response.get("secure_url")
        # print(f"Image uploaded successfully: {url}")
        return url
    except Exception as e:
        print("Error on uploading file.")
        return False

# this is for a sermon audio upload through api 
def upload_single_sermon(file_path):
    try:
        # Upload the image to Cloudinary
        response = cloudinary.uploader.upload(file_path, folder="destiny_centre/audios")
        
        # Get the URL of the uploaded image
        url = response.get("url")
        print(f"Sermon Audio successfully: {url}")
        return url
    except Exception as e:
        print("Error on uploading file.")
        return False
	
 

