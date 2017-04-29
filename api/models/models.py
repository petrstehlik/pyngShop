"""
Author: Frederik Muller, xmulle20@stud.fit.vutbr.cz
Author: Matej Vido, xvidom00@stud.fit.vutbr.cz
Date: 04/2017
"""

from api.error import ApiException
from api.role import Role
from api.dbConnector import dbConnector

conn = dbConnector()
db = conn.db

class CustomerException(ApiException):
	status_code = 401

class Customer(db.Model):
	__tablename__ = "customers"
	id = db.Column(db.Integer,
			db.Sequence("customer_cid_seq", start=1001, increment=1),
			primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	first_name = db.Column(db.String(120), unique=False)
	last_name = db.Column(db.String(120), unique=False)
	password = db.Column(db.String(120), unique=False)
	role = db.Column(db.Integer, unique=False, default=Role.customer)
	settings = db.Column(db.String(10000), unique=False)
	address1 = db.Column(db.String(200), unique=False)
	address2 = db.Column(db.String(200), unique=False)
	phone = db.Column(db.String(20), unique=False)
	city = db.Column(db.String(200), unique=False)
	state = db.Column(db.String(200), unique=False)
	postal_code = db.Column(db.String(20), unique=False)
	orders = db.relationship("Order", backref="customer", lazy="dynamic")

	def __init__(self,
			username,
			id         = None,
			first_name = None,
			last_name  = None,
			email      = None,
			password   = None,
			settings   = None,
			address1   = None,
			address2   = None,
			phone      = None,
			city       = None,
			state      = None,
			postal_code= None,
			orders     = [],
			):
		self.username = username
		self.id = id
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password = password
		self.role = Role.customer
		self.settings = settings
		self.address1 = address1
		self.address2 = address2
		self.phone = phone
		self.city = city
		self.state = state
		self.postal_code = postal_code
		self.orders = orders

	def to_dict(self):
		"""
		Return the internal data in dictionary
		"""
		tmp = {
			'username' : self.username,
			'id' : self.id,
			'first_name' : self.first_name,
			'last_name' : self.last_name,
			'email' : self.email,
			'role' : int(self.role),
			'settings' : self.settings,
			'address1' : self.address1,
			'address2' : self.address2,
			'phone' : self.phone,
			'city' : self.city,
			'state' : self.state,
			'postal_code' : self.postal_code,
		}
		if self.password:
			tmp['password'] = self.password
		return tmp

	def orders_dict(self):
		olist = []
		for order in self.orders:
			olist.append(order.to_dict())
		return olist

	@classmethod
	def from_dict(self, user):
		"""
		Create new user from dictionary
		"""
		return(self(
			username    = user.get("username", None),
			id          = user.get("id", None),
			first_name  = user.get("first_name", None),
			last_name   = user.get("last_name", None),
			email       = user.get("email", None),
			password    = user.get("password", None),
			settings    = user.get("settings", {}),
			address1    = user.get("address1", None),
			address2    = user.get("address2", None),
			phone       = user.get("phone", None),
			city        = user.get("city", None),
			state       = user.get("state", None),
			postal_code = user.get("postal_code", None),
			orders      = user.get("orders", []),
			))

	def __repr__(self):
		return '<Customer %r>' % self.username

class ShippingException(ApiException):
	status_code = 401

class Shipping(db.Model):
	__tablename__ = "shipping"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), unique=False)
	price = db.Column(db.Integer, unique=False)
	orders = db.relationship("Order", backref="shipping", lazy="dynamic")

	def __init__(self, name, price, orders=[], id=None):
		self.id = id
		self.name = name
		self.price = price
		self.orders = orders

	def to_dict(self):
		tmp = {
			'id' : self.id,
			'name' : self.name,
			'price' : self.price,
			}
		return tmp

	def orders_dict(self):
		olist = []
		for order in self.orders:
			olist.append(order.to_dict())
		return olist

	@classmethod
	def from_dict(self, shipping):
		return self(
			id     =shipping.get('id', None),
			name   =shipping.get('name', None),
			price  =shipping.get('price', None),
			orders =shipping.get('orders', []),
			)

	def __repr__(self):
		return '<Shipping %r>' % self.id

class OrderException(ApiException):
	status_code = 401

class Order(db.Model):
	__tablename__ = "orders"
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.Date, unique=False)
	status = db.Column(db.String(200), unique=False)
	full_price = db.Column(db.Integer, unique=False)
	shipping_id = db.Column(db.Integer, db.ForeignKey("shipping.id"))
	customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))

	def __init__(self, timestamp, status, full_price, id=None, shipping=None, customer=None):
		self.id = id
		self.timestamp = timestamp
		self.status = status
		self.full_price = full_price
		self.shipping = shipping
		self.customer = customer

	def to_dict(self):
		tmp = {
			'id' : self.id,
			'timestamp' : self.timestamp,
			'status' : self.status,
			'full_price' : self.full_price,
			}
		return tmp

	def shipping_dict(self):
		return self.shipping.to_dict()

	def customer_dict(self):
		return self.customer.to_dict()

	@classmethod
	def from_dict(self, order):
		return self(
			id         = order.id,
			timestamp  = order.timestamp,
			status     = order.status,
			full_price = order.full_price,
			shipping   = order.shipping,
			customer   = order.customer,
			)

class ProductException(ApiException):
    status_code = 401

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer,
            db.Sequence("product_cid_seq", start=1, increment=1),
            primary_key=True)
    name = db.Column(db.String(255), unique=False)
    slug = db.Column(db.String(255), unique=False)
    description = db.Column(db.String(10000), unique=False)
    price = db.Column(db.Float, unique=False, default=0.00)
    image = db.Column(db.String(255), unique=False)
    in_stock = db.Column(db.Integer, unique=False, default=0)
    hidden = db.Column(db.Boolean, unique=False, default=True)

    def __init__(self,
            name,
            price,
            id = None,
            slug = None,
            description = None,
            image = None,
            in_stock = None,
            hidden = None,
            ):
        self.name = name
        self.id = id
        self.slug = slug
        self.description = description
        self.price = price
        self.image = image
        self.in_stock = in_stock
        self.hidden = hidden

    def to_dict(self):
        """
        Return the internal data in dictionary
        """
        tmp = {
            'name' : self.name,
            'id' : self.id,
            'slug' : self.slug,
            'description' : self.description,
            'price' : self.price,
            'image' : self.image,
            'in_stock' : self.in_stock,
            'hidden': self.hidden,
        }

        return tmp

    @classmethod
    def from_dict(self, product):
        """
        Create new product from dictionary
        """
        return(self(
            name = product.get("name", None),
            id = product.get("id", None),
            slug = product.get("slug", None),
            description = product.get("description", None),
            price = product.get("price", None),
            image = product.get("image", None),
            in_stock = product.get("in_stock", None),
            hidden = product.get("hidden", None),
            ))

    def __repr__(self):
        return '<Product %r>' % self.name

class ProductPropertyException(ApiException):
    status_code = 401

class ProductProperty(db.Model):
    __tablename__ = "product_properties"
    id = db.Column(db.Integer,
            db.Sequence("product_property_cid_seq", start=1, increment=1),
            primary_key=True)
    name = db.Column(db.String(255), unique=False)
    prefix = db.Column(db.String(255), unique=False)
    sufix = db.Column(db.String(10000), unique=False)

    def __init__(self,
            name,
            id = None,
            prefix = None,
            sufix = None,
            ):
        self.name = name
        self.id = id
        self.prefix = prefix
        self.sufix = sufix

    def to_dict(self):
        """
        Return the internal data in dictionary
        """
        tmp = {
            'name' : self.name,
            'id' : self.id,
            'prefix' : self.prefix,
            'sufix' : self.sufix,
        }

        return tmp

    @classmethod
    def from_dict(self, product_property):
        """
        Create new product_property from dictionary
        """
        return(self(
            name = product_property.get("name", None),
            prefix = product_property.get("prefix", None),
            sufix = product_property.get("sufix", None),
            ))

    def __repr__(self):
        return '<Product property %r>' % self.name

class ManufacturerException(ApiException):
    status_code = 401

class Manufacturer(db.Model):
    __tablename__ = "manufacturers"
    id = db.Column(db.Integer,
            db.Sequence("manufacturer_cid_seq", start=1, increment=1),
            primary_key=True)
    name = db.Column(db.String(255), unique=False)
    first_name = db.Column(db.String(255), unique=False)
    last_name = db.Column(db.String(255), unique=False)
    telephone = db.Column(db.String(20), unique=False)
    email = db.Column(db.String(255), unique=False)
    id_num = db.Column(db.String(20), unique=False)
    delivery_time = db.Column(db.String(20), unique=False)


    def __init__(self,
            name,
            id = None,
            first_name = None,
            last_name = None,
            telephone = None,
            email = None,
            id_num = None,
            delivery_time = None,
            ):
        self.name = name
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.telephone = telephone
        self.email = email
        self.id_num = id_num
        self.delivery_time = delivery_time

    def to_dict(self):
        """
        Return the internal data in dictionary
        """
        tmp = {
            'name' : self.name,
            'id' : self.id,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'telephone' : self.telephone,
            'email' : self.email,
            'id_num' : self.id_num,
            'delivery_time' : self.delivery_time,
        }

        return tmp

    @classmethod
    def from_dict(self, manufacturer):
        """
        Create new manufacturer from dictionary
        """
        return(self(
            name = manufacturer.get("name", None),
            first_name = manufacturer.get("first_name", None),
            last_name = manufacturer.get("last_name", None),
            telephone = manufacturer.get("telephone", None),
            email = manufacturer.get("email", None),
            id_num = manufacturer.get("id_num", None),
            delivery_time = manufacturer.get("delivery_time", None),
            ))

    def __repr__(self):
        return '<Manufacturer %r>' % self.name

class CategoryException(ApiException):
    status_code = 401

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer,
            db.Sequence("category_cid_seq", start=1, increment=1),
            primary_key=True)
    name = db.Column(db.String(255), unique=False)
    description = db.Column(db.String(10000), unique=False)
    slug = db.Column(db.String(255), unique=False)
    hidden = db.Column(db.Boolean, unique=False, default=True)

    def __init__(self,
            name,
            id = None,
            description = None,
            slug = None,
            hidden = None,
            ):
        self.name = name
        self.id = id
        self.description = description
        self.slug = slug
        self.hidden = hidden

    def to_dict(self):
        """
        Return the internal data in dictionary
        """
        tmp = {
            'name' : self.name,
            'id' : self.id,
            'description' : self.description,
            'slug' : self.slug,
            'hidden' : self.hidden,
        }

        return tmp

    @classmethod
    def from_dict(self, category):
        """
        Create new category from dictionary
        """
        return(self(
            name = category.get("name", None),
            description = category.get("description", None),
            slug = category.get("slug", None),
            hidden = category.get("hidden", None),
            ))

    def __repr__(self):
        return '<Category %r>' % self.name
