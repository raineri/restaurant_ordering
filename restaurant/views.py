from restaurant import app
from flask import render_template, session, request, redirect, url_for
from models import *
import models
from database import db_session
import hashlib, time, twilio, urllib, jinja2
import cPickle as pickle

ALPHABET = "178264539MNBVCXZLKJHGFDSAPOIUYTREWQ"

def base62_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def base62_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num


import stripe

stripe_keys = {
    'secret_key': 'sk_test_3rwH56vRXZCdnInCVZGhnkCH',
    'publishable_key': 'pk_test_ZxvMLqMOGMVOaWsKl2dnotQ2'
}

stripe.api_key = stripe_keys['secret_key']


class ShoppingCart:
	items = []
	
	def __init__(self):
		self.items
	
	def clear_all(self):
		for item in range(0, len(self.items)):
			self.items.pop(0)
	
	def add_item(self, item):
		self.items.append(item)
		
	def total_price(self):
		total = 0
		for item in self.items:
			total += item.price
		return total
		
	def price_dollars(self):
		total = 0
		for item in self.items:
			total += item.price
		return total/100.0
		
	def num_of_items(self):
		return len(self.items)
		
	def has_items(self):
		if len(self.items) > 0:
			return True
			
	def remove(self, item_id):
		for item in self.items:
			if item.id == item_id:
				self.items.remove(item)
		
class CartItem:
	id = None
	dish = None
	price = None
	def __init__(self, dish_id):
		m = hashlib.md5()
		m.update(str(time.time()))
		self.id = m.hexdigest()
		self.dish = Dish.query.filter_by(dish_id=dish_id).first()
		self.price = self.dish.price
		# self.dish.dish_id, self.dish.name, self.dish.price
		
	def price_dollars(self):
		return self.price/100.0
		
@app.route('/admin/')
def admin():	
	return render_template('admin_login.html')
	
@app.route('/admin/login', methods=['POST', 'GET'])
def admin_login():
	login_success = False
	is_post = False
	error = False
	session['shop_id'] = 1
	if request.method == 'POST':
		is_post = True
		user = User.query.filter_by(email=request.form['username']).first()
		if user != None:
			if request.form['password'] == user.password:
				login_success = True
				session['admin_user'] = user
				return redirect(url_for('admin_dashboard', shop_id=session['shop_id']))
		error = True
	return render_template('admin_login.html', login_success=login_success, is_post=is_post, error=error, shop_id=session['shop_id'])

"""@app.route('/logout', methods=['POST', 'GET'])
def logout():
	session['user'] = None
	return redirect(url_for('shop_index', shop_id=session['shop_id']))
"""
@app.route('/admin/dashboard')
def admin_dashboard():	
	return render_template('admin_dashboard.html')
	
@app.route('/admin/billing')
def admin_billing():	
	return "admin"
	
@app.route('/admin/setting')
def admin_setting():	
	return "admin"
		
@app.route('/shop/index/<shop_id>')
def shop_index(shop_id):	
	session['shop_id'] = shop_id
	shop = Shop.query.filter_by(shop_id=shop_id).first()
	session['shop'] = pickle.dumps(shop)
	return render_template('shop_index.html', shop=shop, shop_id=shop_id)
	
@app.route('/shop/menu/<shop_id>')
def view_menu(shop_id):
	categories = Category.query.filter_by(shop_id=shop_id)
	return render_template('view_menu.html', categories=categories, Dish=Dish, shop_id=shop_id)

@app.route('/shop/<shop_id>/dish/<dish_id>')
def view_dish(shop_id, dish_id):
	dish = Dish.query.filter_by(dish_id=dish_id).first()
	return render_template('view_dish.html', dish=dish, Category=Category, shop_id=shop_id)
	
@app.route('/shop/<shop_id>/category/<category_id>')
def view_category(shop_id, category_id):
	category_name = Category.query.filter_by(category_id=category_id).first().name
	dishes = Dish.query.filter_by(category_id=category_id)
	return render_template('view_category.html', dishes=dishes, category_name=category_name, shop_id=shop_id)

@app.route('/signup', methods=['POST','GET'])
def signup():
	commit_success = False
	if request.method == 'POST':
		if request.form['email'] == "" or request.form['password'] == "" or request.form['first_name'] == "" or request.form['last_name'] == "":
			commit_success = False
			error = True
			return render_template('signup.html', commit_success=commit_success, error=error)
	
		u = User(request.form['email'], request.form['password'], request.form['first_name'], request.form['last_name'], 
				request.form['phone_number'], request.form['address1'], request.form['address2'])
		db_session.add(u)
		db_session.commit()
		commit_success = True
	return render_template('signup.html', commit_success=commit_success)
	
@app.route('/login', methods=['POST', 'GET'])
def login():
	login_success = False
	is_post = False
	error = False
	if request.method == 'POST':
		is_post = True
		user = User.query.filter_by(email=request.form['username']).first()
		if user != None:
			if request.form['password'] == user.password:
				login_success = True
				session['user'] = user
				return redirect(url_for('shop_index', shop_id=session['shop_id']))
		error = True
	return render_template('login.html', login_success=login_success, is_post=is_post, error=error, shop_id=session['shop_id'])
	
@app.route('/logout', methods=['POST', 'GET'])
def logout():
	session['user'] = None
	return redirect(url_for('shop_index', shop_id=session['shop_id']))
	
	
@app.route('/cart/view/<shop_id>', methods=['POST', 'GET'])
def view_shopping_cart(shop_id):
	session['shop_id'] = shop_id
	return render_template('view_cart.html')
	
@app.route('/shop/about/<shop_id>', methods=['POST', 'GET'])
def view_about(shop_id):
	return render_template('view_about.html', shop_id=shop_id)
	
@app.route('/user/preferences', methods=['POST', 'GET'])
def user_preferences():
	return render_template('user_preferences.html')
	
@app.route('/cart/remove/<item_id>', methods=['POST', 'GET'])
def remove_cart_item(item_id):
	if not session.get('shopping_cart', None) == None:
		pickle.loads(session['shopping_cart']).remove(item_id)
	return redirect(url_for('view_shopping_cart', shop_id=session['shop_id']))
	
	
@app.route('/cart/step/2', methods=['POST', 'GET'])
def cart_second_step():
	try:
		return render_template('cart_step_2.html')
	except jinja2.exceptions.UndefinedError:
		return redirect(url_for('login'))
		return "test"
	
@app.route('/cart/step/3', methods=['POST', 'GET'])
def cart_third_step():

	return render_template('cart_step_3.html', key=stripe_keys['publishable_key'])
	
@app.route('/order/index', methods=['POST', 'GET'])
def view_order_index():
	return render_template('view_order_index.html', models=models, Order=Order, base62_encode=base62_encode, int=int)
	
@app.route('/order/view/<order_id>', methods=['POST', 'GET'])
def view_order(order_id):
	return render_template('view_order.html', Order=Order, base62_encode=base62_encode, int=int)
	
@app.route('/active_order/view/<order_id>', methods=['POST', 'GET'])
def active_order(order_id):
	order_id = str(base62_decode(order_id))[:-6]
	order = Order.query.filter_by(order_id=order_id).first()
	shop = Shop.query.filter_by(shop_id=order.shop_id).first()
	amount = 0
	charge = False
	
	if request.method == 'POST':
		amount = request.forms['amount']
		charge = True
		
	return render_template('view_active_order.html', amount=amount, charge=charge, order=order, shop=shop)
	
@app.route('/charge', methods=['POST'])
def charge_card():
	amount = session['shopping_cart'].total_price()
	
	o = Order(user_id=session['user'].user_id, total_cost=amount, shop_id=session['shop'].shop_id, date=int(time.time()))
	db_session.add(o)
	db_session.commit()
	
	session['order_id'] = base62_encode(int('%s%s' % (o.order_id, '000000')))
	
	stripe.Charge.create(
	        amount=amount,
	        currency='usd',
	        card=request.form['stripeToken'],
	        description='Order #%s' % session['order_id']
	    )
	
	# Download the library from twilio.com/docs/libraries
	from twilio.rest import TwilioRestClient
	# Get these credentials from http://twilio.com/user/account
	account_sid = "XXX"
	auth_token = "YYY"
	client = TwilioRestClient(account_sid, auth_token)
	call = client.calls.create(to="+13479618623",  # Any phone number
	                           from_="+13475146625", # Must be a valid Twilio number
	                           url="http://twimlets.com/echo?Twiml=%3CResponse%3E%3CSay%20voice%3D%22woman%22" \
							       "%3EYou%20have%20a%20new%20order%20on%20Roku.%20The%20total%20is%20%2418.%20" \
								   "Customer%20has%20ordered%203%20items.%3C%2FSay%3E%3C%2FResponse%3E&")
	
	session['shopping_cart'].clear_all()
	
	return render_template('charge.html', amount=int(amount)/100.0)
	
@app.route('/cart/add', methods=['POST', 'GET'])
def add_to_cart():
	pickle.loads(session['shopping_cart']).add_item(CartItem(int(request.form['dish_id'])))
	return redirect(url_for('view_shopping_cart', shop_id=request.form['shop_id']))
	
@app.route('/cart/add/<dish_id>', methods=['GET'])
def add_to_cart_link(dish_id):
	pickle.loads(session['shopping_cart']).add_item(CartItem(int(dish_id)))  
	return redirect(url_for('view_shopping_cart', shop_id=pickle.loads(session['shop']).shop_id))
