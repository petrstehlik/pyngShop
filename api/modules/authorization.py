from flask import request
from bson import json_util

from api import auth, db
from api.module import Module
from api.auth import AuthException
from api.models.user import SqlUser as User
from api.models.customer import Customer

au = Module('authorization', __name__, url_prefix='/authorization', no_version=True)

@au.route('/user', methods=['POST'])
def login_user():
	"""
	Authorize user using their username and password
	@return user's document from the DB including config
	"""
	user_data = request.get_json()

	if not user_data:
		raise AuthException("Missing user data")

	user = User(user_data['username'], password=user_data['password'])

	user = auth.login_user(user)

	session_id = auth.store_session(user, is_user=True)

	return(json_util.dumps({"session_id" : session_id, "user" : user.to_dict()}))

@au.route('/customer', methods=['POST'])
def login_customer():
	"""
	Authorize customer using their username and password
	@return customer's document from the DB including config
	"""
	customer_data = request.get_json()
	if not customer_data:
		raise AuthException("Missing customer data")
	customer = Customer(customer_data['username'], password=customer_data['password'])
	customer = auth.login_customer(customer)
	session_id = auth.store_session(customer, is_user=False)
	return(json_util.dumps({"session_id" : session_id, "customer" : customer.to_dict()}))

@au.route('', methods=['DELETE'])
@auth.required()
def logout():
	session_id = request.headers.get('Authorization', None)
	auth.delete(session_id)
	return(json_util.dumps({"success" : True}))


"""
Checks validity of session using only required() decorator
"""
@au.route('', methods=['GET'])
@auth.required()
def checkSession():
	return('')
