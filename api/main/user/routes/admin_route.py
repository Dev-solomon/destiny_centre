from flask import Blueprint
from flask import current_app as app
from flask import Flask, request, jsonify, session, redirect
from main.auth import token_required, del_cookies
from main.user.controllers.admin_controller import *


admin_blueprint = Blueprint('admin',  __name__, "api/admin")


@admin_blueprint.route('/addsermon', methods=['POST'])
# @token_required
def add_sermon():
    if request.method == 'POST':
        return upload_sermon()
    else:
        return "New Sermon Uploading Failed"
    
    
@admin_blueprint.route('/pr', methods=['POST'])
@token_required
def prayer_request():
    if request.method == 'POST':
        return send_prayer_request()
    else:
        return "Sending Request For Prayers Failed"
    

@admin_blueprint.route('/meeting', methods=['POST'])
@token_required
def new_meeting():
    if request.method == 'POST':
        return schedule_meeting()
    else:
        return "Meeting Scheduling Failed"
    
    
@admin_blueprint.route('/testimony', methods=['POST'])
@token_required
def testimony():
    if request.method == 'POST':
        return share_testimony()
    else:
        return "Sharing Testimony Failed"
    
@admin_blueprint.route('/events', methods=['POST'])
# @token_required
def upcoming_events():
    if request.method == 'POST':
        return create_event()
    else:
        return "New Event Couldn't be Added"
    
    
@admin_blueprint.route('/daily_prayer', methods=['POST'])
# @token_required
def daily_prayer():
    if request.method == 'POST':
        return pray_daily()
    else:
        return "Daily Prayer Failed"
    
    
@admin_blueprint.route('/service', methods=['POST'])
# @token_required
def last_service():
    if request.method == 'POST':
        return service()
    else:
        return "Failed To Add Latest Sunday Video"
    
    
    
    

 





   






