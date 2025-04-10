from flask import Flask, request, render_template, session, make_response, redirect, url_for
from flask_cors import CORS
from pymongo import MongoClient
import jwt
import os
from flask_caching import Cache





def create_app():

  # Flask Config
  app = Flask(__name__, static_url_path='/static', static_folder='../../web/static', template_folder='../../web/templates')
  app.config.from_pyfile("config/config.cfg")
  cors = CORS(app, resources={r"/*": { "origins": app.config["FRONTEND_DOMAIN"] }})
  # Assuming you've initialized your Flask app with Flask-Caching
  cache = Cache(config={'CACHE_TYPE': 'simple'})
  cache.init_app(app)
  


  # Misc Config
  os.environ["TZ"] = app.config["TIMEZONE"]

  # Database Config
  if app.config["ENVIRONMENT"] == "production":
    mongo = MongoClient(app.config["MONGO_URI"])
    # mongo = MongoClient(app.config["MONGO_DB"], app.config["MONGO_PORT"])
  else:
    mongo = "Hello App!"
    
      # Import Routes
  with app.app_context():
    # EXPORTS FUNCTIONS START
    from main.auth import token_required
    from main.user.controllers.get_controllers import get_daily_prayer, get_upcoming_events, home_video, get_sermons, get_a_sermon
    
    # EXPORTS FUNCTIONS END
    
    # blueprints for user routes
    from main.user.routes.user_route import user_blueprint
    from main.user.routes.admin_route import admin_blueprint

  # Register User Blueprints
    app.register_blueprint(user_blueprint, url_prefix="/api/user")
    app.register_blueprint(admin_blueprint, url_prefix="/api/admin")
  
  
  
  

  # Index Route
    @app.route("/")
    def home():
      dp = get_daily_prayer()
      ue = get_upcoming_events()
      vid = home_video()
      # Render the page home
      return render_template('index.html', dp=dp, ue=ue, vid=vid)
    
    # Index Route
    @app.route("/login")
    def login():
      # Render the page home
      return render_template('login.html')
    
    @app.route("/signup")
    @token_required
    def signup():
      # Render the page home
      return render_template('signup.html')
    
    # About us page
    @app.route("/about")
    def about():
      return render_template('about.html')
    
    # Sermons Page
    @app.route("/sermons")
    def sermons():
      page_num = request.args.get('page_num', default=1)
      sermons = get_sermons(page_num)    
      return render_template('sermons.html', sermons=sermons)
    
    # Add Sermons Page
    @app.route("/addsermon")
    @token_required
    def addsermon():
      return render_template('admin/add-sermon.html')
    
    # add events page
    @app.route("/addevent")
    @token_required
    def addevent():
      return render_template('admin/add-event.html')
    
    # add prayer page
    @app.route("/addprayer")
    @token_required
    def addprayer():
      return render_template('admin/add-prayer.html')
    
     # admn portal
    @app.route("/adminportal")
    @token_required
    def admin():
      return render_template('admin/admin.html')
    
    # add last service to homepage
    @app.route("/addservice")
    @token_required
    def past_service():
      return render_template('admin/add-service.html')
    
    @app.route("/sermon/<string:sid>")
    def sermon(sid):  # Include 'sid' as a parameter
      single_sermon = get_a_sermon(sid)
      print(single_sermon)
      return render_template('sermon.html', sermon=single_sermon)  # Pass 'sid' to the template
    
    @app.route("/prayers")
    def prayers():
      return render_template('prayers.html')
    
    
    @app.route('/clear_cache')
    def clear_cache():
      cache.clear()  # Clears the entire cache
      return "Cache cleared!" 
    
  
  
  return app