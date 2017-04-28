"""
Author: Matej Vido, xvidom00@stud.fit.vutbr.cz
Date:   04/2017
"""

from flask import request
from bson import json_util

from .. import auth, db
from ..module import Module
from ..models.customer import Customer, CustomerException
from ..role import Role

customers = Module('customers', __name__, url_prefix='/customers', no_version=True)

@auth.required(Role.admin)
def get_customers():
	res = Customer.query.all()
	customers = []

	for customer in res:
		tmp = customer.to_dict()
		tmp.pop("password", None)
		customers.append(tmp)

	return(json_util.dumps(customers))

@auth.required(Role.admin)
def get_customer(customer_id):
	customer = Customer.query.get_or_404(customer_id)
	customer = customer.to_dict()
	customer.pop('password', None)
	return(json_util.dumps(customer))

def unprotected_add_customer(customer_data):
	"""
	Create a customer and add it to database
	"""
	try:
		customer = Customer.from_dict(customer_data)
	except Exception as e:
		raise CustomerException(str(e))

	if customer.password == None:
		raise CustomerException("Missing password")

	customer.password = auth.create_hash(customer.password)

	try:
		db.db.session.add(customer)
		res = db.db.session.commit()
		return customer
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise CustomerException(str(e))

def add_customer():
	r = request.get_json()
	try:
		customer = Customer.from_dict(r)
	except Exception as e:
		raise CustomerException(str(e))

	#if customer_exists(customer):
	#	raise CustomerException("Customer '" + customer.username + "' already exists", status_code = 400)

	customer = unprotected_add_customer(customer.to_dict())

	inserted = Customer.query.get_or_404(customer.id)

	customer = inserted.to_dict()
	customer.pop("password", None)

	return(json_util.dumps(customer))

@auth.required(Role.admin)
def remove_customer(customer_id):
	"""
	Remove the customer
	"""

	customer = Customer.query.get_or_404(customer_id)

	try:
		db.db.session.delete(customer)
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise CustomerException(str(e))

	customer.password = None
	tmp = customer.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def edit_customer(customer_id):
	"""
	TODO: differentiate between PUT and PATCH -> PATCH partial update
	"""
	customer_dict = request.get_json()
	customer = Customer.query.get_or_404(customer_id)

	# If the customer updates their profile check for all fields to be updated
	if "first_name" in customer_dict and customer_dict["first_name"]!= "":
		customer.first_name = customer_dict["first_name"]

	if "last_name" in customer_dict and customer_dict["last_name"] != "":
		customer.last_name = customer_dict["last_name"]

	if "email" in customer_dict and customer_dict["email"] != "":
		customer.email = customer_dict["email"]

	if "settings" in customer_dict and customer_dict["settings"] != {}:
		customer.settings = customer_dict["settings"]

	# In case of password change, verify that it is really them (revalidate their password)
	if "password" in customer_dict and customer_dict["password"] != "":
		if not auth.check_password(customer_dict["password"], customer.password.decode('utf8')):
			raise CustomerException("Password mismatch")

		try:
			customer.password = auth.create_hash(customer_dict["password_new"])
		except Exception as e:
			raise CustomerException(str(e))

	if "address1" in customer_dict and customer_dict["address1"] != "":
		customer.address1 = customer_dict["address1"]
	if "address2" in customer_dict and customer_dict["address2"] != "":
		customer.address2 = customer_dict["address2"]
	if "phone" in customer_dict and customer_dict["phone"] != "":
		customer.phone = customer_dict["phone"]
	if "city" in customer_dict and customer_dict["city"] != "":
		customer.city = customer_dict["city"]
	if "state" in customer_dict and customer_dict["state"] != "":
		customer.state = customer_dict["state"]

	# Update the customer and return updated document
	try:
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise CustomerException(str(e))

	# Remove password hash from the response
	customer.password = None
	tmp = customer.to_dict()

	return(json_util.dumps(tmp))

customers.add_url_rule('', view_func=get_customers, methods=['GET'])
customers.add_url_rule('', view_func=add_customer, methods=['POST'])
customers.add_url_rule('/<string:customer_id>', view_func=get_customer, methods=['GET'])
customers.add_url_rule('/<string:customer_id>', view_func=edit_customer, methods=['PUT'])
customers.add_url_rule('/<string:customer_id>', view_func=remove_customer, methods=['DELETE'])
