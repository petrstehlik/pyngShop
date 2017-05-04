from api.error import ApiException
from api.role import Role

class UserException(ApiException):
	status_code = 401

class User(object):
	"""
	User data model representation.

	Username is the default identifier and is required.
	"""

	username = None
	user_id = None
	first_name = None
	last_name = None
	email = None
	password = None
	role = None
	settings = {}

	def __init__(self,
			username,
			user_id		= None,
			first_name	= None,
			last_name	= None,
			email		= None,
			password	= None,
			role		= None,
			settings	= None,
			):
		self.username = username
		self.user_id = user_id
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password = password
		self.role = self.parseRole(role)
		self.settings = settings

	def get(self, key, default):
		if key == "username":
			return self.username
		elif key == "user_id":
			return self.user_id
		elif key == "first_name":
			return self.first_name
		elif key == "last_name":
			return self.last_name
		elif key == "email":
			return self.email
		elif key == "password":
			return self.password
		elif key == "role":
			return self.role
		elif key == "settings":
			return self.settings

		return default

	@classmethod
	def parseRole(self, role):
		try:
			if role == None:
				return Role.undefined
			elif role == "admin":
				return Role.admin
			elif role == "user":
				return Role.user
			elif role == "guest":
				return Role.guest

			if int(role) == Role.undefined:
				return Role.undefined
			elif int(role) == Role.admin:
				return Role.admin
			elif int(role) == Role.user:
				return Role.user
			elif int(role) == Role.guest:
				return Role.guest

			return Role.undefined
		except Exception as e:
			print(e)
			raise UserException(str(e))


	def setRole(self, role):
		self.role = self.parseRole(role)

	def to_dict(self):
		"""
		Return the internal data in dictionary
		"""
		tmp = {
			'username' : self.username,
			'user_id' : self.user_id,
			'first_name' : self.first_name,
			'last_name' : self.last_name,
			'email' : self.email,
			'role' : int(self.role),
			'settings' : self.settings,
		}

		if self.password:
			tmp['password'] = self.password

		return tmp

	@classmethod
	def from_dict(self, user):
		"""
		Create new user from dictionary
		"""
		# First try MongoDB id field, otherwise use API defined field
		if str(user.get("_id", None)):
			user_id = str(user.get("_id", None))
		else:
			user_id = str(user.get("user_id", None))

		return(self(
			username	= user.get("username", None),
			user_id		= user_id,
			first_name	= user.get("first_name", None),
			last_name	= user.get("last_name", None),
			email		= user.get("email", None),
			password	= user.get("password", None),
			role		= User.parseRole(user.get("role", None)),
			settings	= user.get("settings", {})
			))

from api.dbConnector import dbConnector
conn = dbConnector()

db = conn.db

class SqlUser(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	first_name = db.Column(db.String(120), unique=False)
	last_name = db.Column(db.String(120), unique=False)
	password = db.Column(db.String(120), unique=False)
	role = db.Column(db.Integer, unique=False)
	settings = db.Column(db.String(10000), unique=False)

	def __init__(self,
			username,
			id			= None,
			first_name	= None,
			last_name	= None,
			email		= None,
			password	= None,
			role		= Role.guest,
			settings	= None,
			):
		self.username = username
		self.id = id
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password = password
		self.role = self.parseRole(role)
		self.settings = settings

	@classmethod
	def parseRole(self, role):
		try:
			if role == None:
				return Role.undefined
			elif role == "admin":
				return Role.admin
			elif role == "user":
				return Role.user
			elif role == "guest":
				return Role.guest

			if int(role) == Role.undefined:
				return Role.undefined
			elif int(role) == Role.admin:
				return Role.admin
			elif int(role) == Role.user:
				return Role.user
			elif int(role) == Role.guest:
				return Role.guest

			return Role.undefined
		except Exception as e:
			print(e)
			raise UserException(str(e))

	def setRole(self, role):
		self.role = self.parseRole(role)

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
			username	= user.get("username", None),
			id			= user.get("id", None),
			first_name	= user.get("first_name", None),
			last_name	= user.get("last_name", None),
			email		= user.get("email", None),
			password	= user.get("password", None),
			role		= User.parseRole(user.get("role", None)),
			settings	= str(user.get("settings", {}))
			))

	def __repr__(self):
		return '<User %r>' % self.username

