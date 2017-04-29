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
			))

	def __repr__(self):
		return '<Customer %r>' % self.username

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
    __tablename__ = "product_property"
    id = db.Column(db.Integer,
            db.Sequence("product_property_cid_seq", start=1, increment=1),
            primary_key=True)
    name = db.Column(db.String(255), unique=False)
    prefix = db.Column(db.String(255), unique=False)
    sufix = db.Column(db.String(10000), unique=False)

    def __init__(self,
            name,
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
            name = product.get("name", None),
            prefix = product.get("prefix", None),
            sufix = product.get("sufix", None),
            ))

    def __repr__(self):
        return '<Product property %r>' % self.name

class ManufacturerException(ApiException):
    status_code = 401

class Manufacturer(db.Model):
    __tablename__ = "manufacturer"
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
            name = product.get("name", None),
            first_name = product.get("first_name", None),
            last_name = product.get("last_name", None),
            telephone = product.get("telephone", None),
            email = product.get("email", None),
            id_num = product.get("id_num", None),
            delivery_time = product.get("delivery_time", None),
            ))

    def __repr__(self):
        return '<Manufacturer %r>' % self.name
