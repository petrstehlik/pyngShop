"""
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
