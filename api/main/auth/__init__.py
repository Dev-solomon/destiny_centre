from flask import current_app as app, make_response, redirect, url_for, render_template
from flask import request
from functools import wraps
import jwt
import datetime
from bson import ObjectId
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from main.user.models.user_model import User
from flask import make_response
import datetime

print(datetime.datetime.utcnow() + datetime.timedelta(hours=1))

client = MongoClient(app.config["MONGO_URI"])
db = client[app.config["MONGO_DBNAME"]]
bcrypt = Bcrypt(app)



# Auth Decorator
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		access_token = request.cookies.get('token')
  
		if not access_token:
			return render_template('login.html')

		if access_token:
			try:
				data = jwt.decode(access_token, app.config['SECRET_KEY'], algorithms=["HS256"])
				current_user = User.collection.find_one({'email': data['email']})
				if not current_user:
					raise Exception("User not found")
			except Exception as e:
				return make_response(redirect(url_for('login'))) 

		kwargs['current_user'] = current_user  # Pass current_user to the wrapped function
		return f(*args, **kwargs)	

	return decorated



def set_cookies(token, redirect_url):
  resp = make_response(redirect(url_for(redirect_url))) 
  resp.set_cookie('token', str(token))
  return resp

def del_cookies():
    resp = make_response(redirect(url_for('login', message="Please Login For Access"))) 
    resp.delete_cookie('token')
    return resp

def encodeAccessToken(email):
	expiration_date = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
	accessToken = jwt.encode({
		"email": email,
		"exp": expiration_date,  # The token will expire in 15 minutes
	}, app.config["SECRET_KEY"], algorithm="HS256")

	return accessToken
