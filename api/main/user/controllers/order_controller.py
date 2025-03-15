from flask import current_app as app, jsonify, request, make_response, redirect, url_for
from pymongo import MongoClient, DESCENDING
from bson import ObjectId, json_util
import datetime
import json
from main.user.models.order_model import Order
from main.user.models.product_model import Product
from main.stripe.stripe import *
from termcolor import colored


# Asynchronous utility for handling in loops
# def async_map(func, iterable):
#     return asyncio.gather(*(func(item) for item in iterable))

# Create order function
def create_order():
    try:
        data = request.form.to_dict()
          # form temporary data_form
          # Original string with single quotes
        json_string = data['orderItems']
        # Replace single quotes with double quotes to make it a valid JSON string
        json_string = json_string.replace("'", "\"")
        # Convert to Python list using json.loads()
        orderItems = json.loads(json_string)
        create_new_order = {
                        "user": ObjectId(data['user']),
                        "order_items": orderItems,
                        "payments": json.loads(data['payments']),
                        "total_price": float(data['total_price']),
                        "sub_total_price": float(data['sub_total_price']),
                        "tax_price": float(data['tax_price']),
                        "shipping_address": json.loads(data['shipping_address']),
                        "createdAt" : datetime.datetime.now().isoformat()
                    }
        result =  Order.collection.insert_one(create_new_order).inserted_id
        # print(result)
        print(f"New Order by User: {data['user']} at Time: {datetime.datetime.now().isoformat()}")
        return result
    except Exception as e: 
        print({'message': str(e)})
        return False

# Update order to paid function
def update_order_to_paid(customer_order, payment_data):
    try: 
        # Convert customer_order to ObjectId
        order = Order.collection.find_one({'_id': ObjectId(customer_order)})
        
        if order:
            order_status = {
                'completed': 'completed',
                'canceled': 'cancelled'
            }
            
            # Check for payment status and update accordingly
            payment_status = order_status['completed'] if payment_data.get('status') == "complete" else order_status['canceled']
            
            Order.collection.update_one(
                {'_id': ObjectId(customer_order)}, 
                {'$set':  {
                    "payments": {
                        "status": payment_status,
                        "method": "stripe",  # Fixed typo from 'methd' to 'method'
                        "payment_date": datetime.datetime.now()
                    },
                    "total_price": payment_data.get('amount_total', 0) / 100,  # Handle missing data
                    "sub_total_price": payment_data.get('amount_subtotal', 0) / 100,
                    "shipping_address": {
                        'fullName': payment_data['customer_details'].get('name'),
                        'email': payment_data['customer_details'].get('email'),
                        'address': f"Line1: {payment_data['shipping_details']['address'].get('line1')}, "
                                   f"Line2: {payment_data['shipping_details']['address'].get('line2')}, "
                                   f"Postal Code: {payment_data['shipping_details']['address'].get('postal_code')}, "
                                   f"State: {payment_data['shipping_details']['address'].get('state')}",
                        'location': f"{payment_data['shipping_details']['address'].get('city')}, "
                                    f"{payment_data['shipping_details']['address'].get('country')}",
                        'phoneNumber': payment_data['customer_details'].get('phone'),
                        'shippingMethod': "CJPacket Ordinary",
                        'shipping_cost': order['shipping_address'].get('shipping_cost', 0)  # Handle missing cost
                    }
                }})
            
            print(colored(" ---- A Paid Order Has been Updated ---- ", "yellow"))
            return '', 200
            
    except Exception as e:
        print(f"Error occurred: {e}")  # Log the error for debugging
        return jsonify({'message': str(e)}), 400


# Function to delete an order
def delete_order(order_id):
    try: 
        result = Order.collection.delete_one({'_id': ObjectId(order_id)})
        if result.deleted_count == 1:
            return redirect(url_for('user_dashboard', message="Order Deleted!"))
        else:
            return redirect(url_for('user_dashboard', message="Order Failed To Delete!"))
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Function to get user orders
from bson.objectid import ObjectId
from flask import jsonify
 
def get_user_orders(user_id):
    try:
        orders_cursor = Order.collection.find({'user': ObjectId(user_id)}).sort('createdAt', DESCENDING)
        
        orders_list = list(orders_cursor)  # Retrieve all orders from the cursor
        
        total_orders = len(orders_list)  # Calculate total number of orders
        
        orders_cursor.close()  # Close the cursor
        
        # Format the response as JSON
        # return jsonify({
        #     'orders': json_util.dumps(orders_list),
        #     'total_orders': total_orders
        # })
        return orders_list
    
    except Exception as e:
        return jsonify({'message': str(e)}), 400


# Function to get order by ID
def get_order_by_id(order_id):
    try:
        order = Order.collection.find_one({'_id': ObjectId(order_id)})
        # return jsonify(str(order)), 201
        return order
    except Exception as e:
        return jsonify({'message': str(e)}), 400


# Delete all orders
def delete_all_orders(user_id):
    try:
        # Convert user_id to ObjectId if needed
        user_id = ObjectId(user_id)

        # Delete orders where user matches
        result = Order.collection.delete_many({"user": user_id})

        # Check deletion result
        if result.deleted_count > 0:
            return { "message": "Orders Deleted!" }
        else:
            return { "message": "No orders found for this user" }
    
    except Exception as e:
        return { "error": str(e) }
    
    

def get_cart():
    # Get the cart from cookies
    cart = request.cookies.get('cart')
    
    if cart:
        # Deserialize the cart JSON string back to a dictionary
        cart = json.loads(cart)
    else:
        cart = []
    
    return cart



def delete_cart_cookie(order_id):
    """
    Deletes the 'cart' cookie from the browser.
    """
    response = make_response(redirect(url_for('checkout', order_id=order_id, message="Your Order Has Been Placed!")))  # Create a response object
    response.delete_cookie('cart', path='/', domain='127.0.0.1')  # Specify the cookie name and path
    return response