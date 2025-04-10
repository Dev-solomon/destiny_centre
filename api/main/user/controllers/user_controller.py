from flask import Flask, jsonify, request, make_response, url_for, redirect, render_template
from flask_bcrypt import Bcrypt
from main.user.models.user_model import User
from main.auth import encodeAccessToken, set_cookies
from flask import current_app as app 
from bson import ObjectId
import datetime



bcrypt = Bcrypt(app)



# Login user
def login():
    try:
        data = request.form.to_dict()
        user = User.collection.find_one({'email': data['email']})
        
        if user and 'password' not in user:
            return "Something Went Wrong" 
        
        if user and bcrypt.check_password_hash(user['password'], data['password']):
            token = encodeAccessToken(user['email'])
            return set_cookies(token, 'admin')
        else:
             return "Invalid Credentials, Try Again!"
    except Exception as e:
        # return jsonify({'message': str(e)})
        return "Contact Tech Support For Help"
    



# Register a new user
def register_user():
    try:
        data = request.form.to_dict()
        data['createdAt'] = datetime.datetime.now().isoformat()  
        user = User.collection.find_one({'email': data['email']})
        if (user):
           return "This Admin Already Exists!"
        else:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            data['password'] = hashed_password
            new_user = User.collection.insert_one(data).inserted_id
            created_user = User.collection.find_one({'email': data['email']})
            if(created_user):
                return "User Created Sucessfully."
            else:
                 return "Error Creating user, Try again!"
    except Exception as e:
        return jsonify({'message': str(e)}), 400

#  Logout a user  and delete cookies
def logout():
    resp = make_response(redirect(url_for('user.user_login'))) 
    resp.delete_cookie('token')
    return resp



