import bcrypt
from functools import wraps
from flask import request
from datetime import datetime, timedelta

from .models.user import SqlUser as User
from .models.models import Customer
from .role import Role
from .session import SessionException
from .error import ApiException

class AuthException(ApiException):
	status_code = 404

class Auth(object):
	errors = {
		'0' : 'Username not found.',
		'1' : 'Username and password doesn\'t match.',
		'2' : 'Expired session.',
		'3' : 'Authorization header is missing.'
	}

	def __init__(self, db, session_manager, secret_key):
		self.db = db
		self.session_manager = session_manager
		self.secret_key = secret_key

	def check_password(self, password, hash):
		return bcrypt.checkpw(password.encode('utf8'), hash.encode('utf8'))

	def create_hash(self, password):
		return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(11))

	def auth_error(self, code):
		msg = {
			'code' : code,
			'description' : self.errors[str(code)]
		}
		res = json_util.dumps(msg)
		return msg

	def login_user(self, user):
		try:
			res = User.query.filter_by(username=user.username).first_or_404()
		except Exception as e:
			raise AuthException(str(e))

		#if not res:
		#	raise AuthException("User not found")

		if not self.check_password(user.password, res.password.decode('utf8')):
			raise AuthException("Password mismatch")

		# Remove password field from the user
		res.password = None

		return(res)

	def login_customer(self, customer):
		try:
			res = Customer.query.filter_by(username=customer.username).first_or_404()
		except Exception as e:
			raise AuthException(str(e))
		if not self.check_password(customer.password, res.password.decode('utf8')):
			raise AuthException("Password mismatch")
		# Remove password field
		res.password = None
		return (res)

	def store_session(self, user):
		session_id = self.session_manager.create(user)
		return session_id

	def lookup(self, session_id):
		try:
			session = self.session_manager.lookup(session_id)
			return session
		except SessionException:
			print("Couldn't find given session")
			raise

	def delete(self, session_id):
		try:
			self.session_manager.delete(session_id)
		except SessionException:
			print("Couldn't find given session")
			raise

	def required(self, role=Role.undefined):
		"""
		Decorator for required Authorization JWT token

		Usage: (auth is the initialized Auth object instance)
		@auth.required() -	Don't look for user's role.
							Only check if they have valid session.

		@auth.required(Role.[admin|user|customer|guest]) - check session validity and their role
		"""
		def auth_decorator(f):
			@wraps(f)
			def verify(*args, **kwargs):
				session_id = request.headers.get('Authorization', None)
				if not session_id:
					raise SessionException("Header field 'Authorization' not found.")

				try:
					session = self.lookup(session_id)
				except SessionException:
					raise SessionException("Session not found")

				if role != Role.undefined and role < session["user"].role:
					raise SessionException("Insufficient privileges.")

				return f(*args, **kwargs)
			return verify
		return auth_decorator
