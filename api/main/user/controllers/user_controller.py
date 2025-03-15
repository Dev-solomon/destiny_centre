from flask import Flask, jsonify, request, make_response, url_for, redirect, render_template
from flask_bcrypt import Bcrypt
from main.user.models.user_model import User
from main.auth import encodeAccessToken, set_cookies
from flask import current_app as app 
from bson import ObjectId
import datetime
import os
from werkzeug.utils import secure_filename
from main.tools import upload_profile_image



bcrypt = Bcrypt(app)



# Import users from data - usually for test
def import_users():
    try:
        data = request.json
        User.collection.delete_many({})
        import_users = User.collection.insert_many(data['users'])
        return jsonify({'message': 'Users imported successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Login user
def login():
    try:
        data = request.form.to_dict()
        user = User.collection.find_one({'email': data['email']})
        
        if user and 'password' not in user:
            return render_template("user/login.html", messageError="No Password, Try Google Login") 
        
        if user and bcrypt.check_password_hash(user['password'], data['password']):
            token = encodeAccessToken(user['email'])
            return set_cookies(token, 'home')
        else:
             return render_template("user/login.html", messageError="Invalid Email or Password")
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    # User by ID
def get_user(id):
    try:
        user = User.collection.find_one({'_id': ObjectId(id)}) 
        if user:
           return user
        return None
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    # user by email
def get_user_by_email(email):
    try:
        user = User.collection.find_one({'email': email}) 
        if user:
           return user
        return None
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Update user profile
def update_profile():
    try:
        data = request.form.to_dict()
        files = request.files.get('image')
        
        # Exclude '_id' from the update operation
        update_data = {key: value for key, value in data.items() if key != '_method' and key != 'check_email'}
        
        # code for saving file uploaded in profile
        file_path = os.path.join('uploads/', secure_filename(files.filename))
        files.save(file_path)
        # upload file to cloudinary for storage there
        image_url = upload_profile_image(file_path)
        update_data['image'] = str(image_url)
        # Remove the file after successful upload
        os.remove(file_path)
        print(f"Local file removed: {file_path}")
       
        
        update_user = User.collection.update_one(
            {'email': data['check_email']},
            {'$set': update_data}
        )
        if update_user.modified_count > 0:
            return redirect(url_for('change_profile', message="Password Updated Successfully"))
        else:
            return redirect(url_for('change_profile', messageError="Something Went Wrong, Try Again!"))
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Change user password
def change_password():
    try:
        data = request.form.to_dict()
        user = User.collection.find_one({'email': data['email']})
        if "password" not in user:
            User.collection.update_one(
                {'email': data['email']},
                {'$set': {'password': bcrypt.generate_password_hash(data['newPassword']).decode('utf-8')}}
            )
            return redirect(url_for('change_password', message="Password Updated Successfully"))
        
        elif bcrypt.check_password_hash(user['password'], data['oldPassword']):
            User.collection.update_one(
                {'email': data['email']},
                {'$set': {'password': bcrypt.generate_password_hash(data['newPassword']).decode('utf-8')}}
            )
            return redirect(url_for('change_password', message="Password Updated Successfully"))
        else:
            return redirect(url_for('change_password', messageError="Invalid Old Password"))
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Delete user
def delete_user():
    try:
        data = request.form.to_dict()
        user = User.collection.delete_one({'_id': ObjectId(data['_id'])})
        if user.deleted_count > 0:  
            return  redirect(url_for('user.user_login', message="User Deleted Successfully"))
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Register a new user
def register_user():
    try:
        data = request.form.to_dict()
        data['createdAt'] = datetime.datetime.now().isoformat()   
        data['isAdmin'] = False
        user = User.collection.find_one({'email': data['email']})
        if (user):
           return render_template("user/signup.html", message="User Already Exists")
        else:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            data['password'] = hashed_password
            new_user = User.collection.insert_one(data).inserted_id
            created_user = User.collection.find_one({'email': data['email']})
            if(created_user):
                # token = encodeAccessToken(created_user['email'])
                # print(token)
                return render_template("user/login.html", message="User Created Successful, Login!")
            else:
                 return render_template("user/signup.html", messageError="Error Creating user, Try again!")
    except Exception as e:
        return jsonify({'message': str(e)}), 400

#  Logout a user  and delete cookies
def logout():
    resp = make_response(redirect(url_for('user.user_login'))) 
    resp.delete_cookie('token')
    return resp



