from sqlalchemy import Table, Column, Integer, String, Float, Text
from database import Base
import time

class User(Base):
	__tablename__ = 'users'
	user_id = Column(Integer, primary_key=True)
	email = Column(String(60), unique=True)
	password = Column(String(25))
	first_name = Column(String(60))
	last_name = Column(String(60))
	phone_number = Column(String(40))
	address1 = Column(String(60))
	address2 = Column(String(60))
	
	def __init__(self, email=None, password=None, first_name=None, last_name=None, phone_number=None, address1=None, address2=None):
		self.email = email
		self.password = password
		self.first_name = first_name
		self.last_name = last_name
		self.phone_number = phone_number
		self.address1 = address1
		self.address2 = address2

	def __repr__(self):
		return '<User %r>' % (self.email)

class Shop(Base):
	__tablename__ = 'shops'
	shop_id = Column(Integer, primary_key=True)
	domain = Column(String(40))
	title = Column(String(40))
	description = Column(String(60))
	shipping_cost = Column(Float)
	order_tax = Column(Float)

	def __init__(self, domain=None, title=None, description=None, shipping_cost=None, order_tax=None):
		self.domain = domain
		self.title = title
		self.description = description
		self.shipping_cost = shipping_cost
		self.order_tax = order_tax

	def __repr__(self):
		return '<Shop %s>' % (self.domain)

class Category(Base):
	__tablename__ = 'dish_category'
	category_id = Column(Integer, primary_key=True)
	shop_id = Column(Integer)
	name = Column(String(40))

	def __init__(self, shop_id=None, name=None):
		self.shop_id = shop_id
		self.name = name

	def __repr__(self):
		return '<Category %s>' % (self.name)

class Dish(Base):
	__tablename__ = 'dishes'
	dish_id = Column(Integer, primary_key=True)
	category_id = Column(Integer)
	name = Column(String(40))
	description = Column(String(160))
	price = Column(Integer)
	dish_picture = Column(String(60))
	
	def __init__(self, name=None, description=None, price=None, category_id=None, dish_picture=None):
		self.description = description
		self.name = name
		self.price = price
		self.category_id = category_id
		self.dish_picture = dish_picture

	def __repr__(self):
		return '<Dish %s>' % (self.name)
		
	def price_dollars(self):
		return self.price/100.0
		
class DishReview(Base):
	__tablename__ = 'dish_reviews'
	review_id = Column(Integer, primary_key=True)
	dish_id = Column(Integer)
	date = Column(String(40))
	user_id = Column(Integer)
	rating = Column(Integer)
	comment = Column(Text)

	def __init__(self, dish_id=None, date=None, user_id=None, rating=None, comment=None):
		self.dish_id = dish_id
		self.date = date
		self.user_id = user_id
		self.rating = rating
		self.comment = comment

	def __repr__(self):
		return '<DishReview %s>' % (self.review_id)
		
class Order(Base):
	__tablename__ = 'orders'
	order_id = Column(Integer, primary_key=True)
	total_cost = Column(Integer)
	shop_id = Column(Integer)
	special_instructions = Column(String(160))
	shipping_cost = Column(Float)
	order_tax = Column(Float)
	user_id = Column(Integer)
	date = Column(Integer)

	def __init__(self, total_cost=None, shop_id=None, user_id=None, date=None, special_instructions=None, shipping_cost=None, order_tax=None):
		self.total_cost = total_cost
		self.shop_id = shop_id
		self.special_instructions = special_instructions
		self.shipping_cost = shipping_cost
		self.order_tax = order_tax
		self.user_id = user_id
		self.date = date
		

	def __repr__(self):
		return '<Order %s>' % (self.order_id)
		
	def get_date(self):
		return time.ctime(self.date)

class OrderItem(Base):
	__tablename__ = 'order_items'
	item_id = Column(Integer, primary_key=True)
	order_id = Column(Integer)
	dish_id = Column(Integer)
	price = Column(Integer)

	def __init__(self, order_id=None, dish_id=None, price=None):
		self.shop_id = shop_id
		self.name = name

	
	def price_dollars(self):
		return self.price/100.0


"""
shops = Table('shops', metadata,
    Column('shop_id', Integer, primary_key=True),
	Column('domain', String(40)),
	Column('title', String(40)),
    Column('description', String(60)),
    Column('shipping_cost', Float),
	Column('order_tax', Float)
)

dish_category = Table('dish_category', metadata,
    Column('category_id', Integer, primary_key=True),
	Column('shop_id', Integer),
	Column('name', String(40))
)

dishes = Table('dishes', metadata,
    Column('dish_id', Integer, primary_key=True),
	Column('category_id', Integer),
	Column('name', String(40)),
	Column('description', String(160)),
	Column('price', Float),
	Column('dish_picture', String(60))
)

dish_reviews = Table('dish_reviews', metadata,
    Column('review_id', Integer, primary_key=True),
	Column('dish_id', Integer),
	Column('user_id', Integer),
	Column('rating', Integer),
	Column('comment', Text),
)


users = Table('users', metadata,
    Column('user_id', Integer, primary_key=True),
	Column('first_name', String(60)),
	Column('last_name', String(60)),
	Column('phone_number', String(40)),
	Column('address1', String(60)),
	Column('address2', String(60)),
	Column('email', String(60)),
	Column('password', String(25))
)

orders = Table('orders', metadata,
    Column('order_id', Integer, primary_key=True),
	Column('total_cost', Float),
	Column('shop_id', Integer),
    Column('special_instructions', String(160)),
    Column('shipping_cost', Float),
	Column('order_tax', Float)
)

order_items = Table('order_items', metadata,
    Column('item_id', Integer, primary_key=True),
	Column('order_id', Integer),
	Column('dish_id', Integer)
)
"""