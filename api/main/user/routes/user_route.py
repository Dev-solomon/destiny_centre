from flask import Blueprint
import requests
from flask import current_app as app
from flask import Flask, request, jsonify, session, redirect
from main.auth import token_required, del_cookies
from main.user.controllers.user_controller import *
from main.user.models.user_model import User
import json
import datetime


user_blueprint = Blueprint('user',  __name__, "api/user")


@user_blueprint.route('/registration', methods=['POST','GET'])
def registration():
    if request.method == 'POST':
        return register_user()
    else:
        return "Unable to Register Admin!"

@user_blueprint.route('/login', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        return login()
    else:
        return "Unable to Login Admin!"

    
@user_blueprint.route('/logout', methods=['POST'])
@token_required
def user_logout(current_user):
    return logout()





   






