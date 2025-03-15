from flask import Flask, request, render_template, session, make_response, redirect, url_for
from flask_cors import CORS
from pymongo import MongoClient
import jwt
import os
from flask_caching import Cache
import datetime
from dateutil.relativedelta import relativedelta




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
    mongo = MongoClient(app.config["MONGO_URI"])
    
      # Import Routes
  with app.app_context():
    # EXPORTS FUNCTIONS START
    from main.auth import token_required
    from main.user.controllers.user_controller import get_user_by_email
    from main.tools import JsonResp
    from main.user.models.user_model import User
    from main.user.controllers.order_controller import get_user_orders, create_order, get_order_by_id
    from main.user.controllers.product_controller import (
    get_product_by_id, 
    get_popular_tags, 
    get_popular_variants, 
    get_search_products, 
    get_user_reviews,
    get_all_reviews, 
    get_other_products, 
    get_related_products )
    from main.user.models.user_model import User
    from main.user.controllers.order_controller import get_cart
    
    # EXPORTS FUNCTIONS END
    
    # blueprints for user routes
    from main.user.routes.user_route import user_blueprint
    from main.user.routes.product_route import product_blueprint
    from main.user.routes.category_route import category_blueprint
    from main.user.routes.order_route import order_blueprint
    # blueprints for seller below
    from main.seller.routes.seller_route import seller_blueprint

  # Register User Blueprints
  app.register_blueprint(user_blueprint, url_prefix="/api/user")
  app.register_blueprint(product_blueprint, url_prefix="/api/products")
  app.register_blueprint(category_blueprint, url_prefix="/api/categories")
  app.register_blueprint(order_blueprint, url_prefix="/api/orders")
  # Register Seller Blueprints
  app.register_blueprint(seller_blueprint, url_prefix="/api/sellers")
  
  
  
  

  # Index Route
  @app.route("/")
  def home():
    one_month_ago = datetime.datetime.now() - relativedelta(months=1)
    
    message_error = request.args.get('messageError')
    message = request.args.get('message')
    token = request.cookies.get('token')
    cart = get_cart()
    # get all products reviews
    reviews = get_all_reviews()
    
    # for all products
    page_num = request.args.get('page_num', default=1)
    product_name = request.args.get('product_name', default=None)
    product_tag = request.args.get('product_tag', default=None)
    min_price = request.args.get('min', default=1)
    max_price = request.args.get('max', default=99999999)
    products = get_search_products(product_name, product_tag, min_price, max_price, page_num)[0]
    if not token:  # Token doesn't exist
        return render_template('user/index.html')
    else:
        try:
            # Decode the token and fetch the user
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.collection.find_one({'email': data['email']})
            if not current_user:
                raise Exception("User not found")
        except Exception as e:
            return make_response(redirect(url_for('user.user_login'))) 

        # Render the page with the current user's details
        return render_template('user/index.html', user=current_user, cart=cart, messageError=message_error, message=message, all_reviews=reviews, products=products, one_month_ago=one_month_ago)
    
    
  # dashboard normal user/ Buyer
  @app.route("/dashboard")  
  @token_required
  def user_dashboard(current_user):
    message_error = request.args.get('messageError')
    message = request.args.get('message')
    cart = get_cart()
    user_orders = get_user_orders(current_user['_id'])
    return render_template('user/dashboard.html', cart=cart, user=current_user, orders=user_orders,  messageError=message_error, message=message)
  
   
  # orders page for user
  @app.route("/orders")
  @token_required
  def orders(current_user):
    cart = get_cart()
    user_orders = get_user_orders(current_user['_id'])
    return render_template('user/orders.html', user=current_user, cart=cart, orders=user_orders)
  
  
  # checkout page
  @app.route("/checkout")
  @token_required
  def checkout(current_user): 
    cart = get_cart()
    order_id = request.args.get('order_id')
    message_error = request.args.get('messageError')
    message = request.args.get('message')
    user_orders = get_order_by_id(order_id)
    return render_template('user/checkout.html', user=current_user, cart=cart, orders=user_orders,  messageError=message_error, message=message)
  
  
  # product single detail page
  @app.route("/product_detail/<string:product_id>", methods=['GET', 'POST'])
  @token_required
  def product_detail(current_user, product_id): 
    try:
      # get the cart information
      cart = get_cart()
      # the page number on the product for the reviews
      page_num = request.args.get('page_num', default=1)
      # message args for the return messages
      message_error = request.args.get('messageError')
      message = request.args.get('message')
      # product id to get a single product info
      product = get_product_by_id(product_id)
      # get other products that are related and not-related
      relatedProducts = get_related_products(product_id)
      otherProducts = get_other_products(product_id)
      # get the user reviews and it's pages
      userReviews = get_user_reviews(product_id, page_num)[0]
      all_reviews = get_all_reviews()
      userReviews_pages = get_user_reviews(product_id, page_num)[1]
      
      # calculate the ratings for current single product
      ratings = [int(rating['rating']) for rating in userReviews]
      total_rating = sum(ratings)
      review_count = len(ratings)
      averagerating = (total_rating / review_count) if review_count > 0 else 0
      
      
      
      
          
      
      return render_template('user/product.html', cart=cart, 
                             user=current_user, 
                             reviews=userReviews, 
                             all_reviews=all_reviews,
                             reviews_pages=userReviews_pages, 
                             rating=averagerating,
                             product=product, 
                             relatedProducts=relatedProducts, 
                             otherProducts=otherProducts,  
                             messageError=message_error, 
                             message=message )
    except Exception as e:
      app.logger.error(f"Error occurred: {e}")  # Log the error message
      return {"message": "Internal server error"}, 500
      
      
      
  # shop page for good list
  @app.route("/catalog", methods=['POST', 'GET'])
  def catalog():
      cart = get_cart() # products in cart
      tags = get_popular_tags() # popular tags list
      variants = get_popular_variants() # popular variants list
      
      # get all reviews
      reviews = get_all_reviews()
      
      
      # display products in catalog with filter
      page_num = request.args.get('page_num', default=1)
      product_name = request.args.get('product_name', default=None)
      product_tag = request.args.get('product_tag', default=None)
      min_price = request.args.get('min', default=1)
      max_price = request.args.get('max', default=99999999)
      searched_products = get_search_products(product_name, product_tag, min_price, max_price, page_num)[0]
      searched_pages = get_search_products(product_name, product_tag, min_price, max_price, page_num)[1]
      
      
      return render_template('user/shop.html', cart=cart, 
                             show_login="no", 
                             tags=tags, 
                             all_reviews=reviews,
                             variants=variants, 
                             searched_products=searched_products, 
                             searched_pages=searched_pages )
    
    
  
  
  # create a new user account
  @app.route("/signup", methods=['POST', 'GET'])
  def signup():
    return render_template('user/signup.html', show_cart="no")
  
  
  # login page
  @app.route("/login")
  def login():
    return render_template('user/login.html', show_cart="no")
  
  # update password
  @app.route("/update-password", methods=['POST', 'GET'])
  @token_required
  def change_password(current_user):
    message_error = request.args.get('messageError')
    message = request.args.get('message')
    cart = get_cart()
    return render_template('user/change_password.html', user=current_user, cart=cart, messageError=message_error, message=message)
   
  # update user profile
  @app.route("/update-profile", methods=['POST', 'GET'])
  @token_required
  def change_profile(current_user):
    message_error = request.args.get('messageError')
    message = request.args.get('message')
    cart = get_cart()
    return render_template('user/update_profile.html', user=current_user, cart=cart, messageError=message_error, message=message, delete_="yes")
  
# URL for payments
  @app.route("/paymentSuccess")
  def payment_success():
   return render_template('user/paysuccess.html')
  
  
  @app.route("/paymentFailed")
  def payment_failed():
    return render_template('user/payfailed.html')
  
  
  @app.route('/clear_cache')
  def clear_cache():
    cache.clear()  # Clears the entire cache
    return 'Cache cleared!' 
  
  
  
  return app