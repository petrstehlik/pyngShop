import bcrypt
from flask import request
from bson import json_util, ObjectId
import pymongo

from api import auth, db
from api.module import Module
from api.models.user import SqlUser as User, UserException
from api.role import Role

users = Module('users', __name__, url_prefix='/users', no_version=True)

def count_users():
	""" FIXME not used, remove """
	return db.users.count()

def lookup_user(user):
	""" FIXME not used, remove """
	user_id = user.get("user_id", None)

	query = {"$or" : [
		{"_id" : None if user_id == None else ObjectId(user_id)},
		{"username" : user.get("username", None)},
		{"email" : user.get("email", None)}
		]}

	cursor = db.users.find(query)

	return list(cursor)

def user_exists(user):
	""" FIXME not used, remove """
	return False if db.users.find({"$or" : [
		{"username" : user.get("username", None)},
		{"email" : user.get("email", None)}
		]}).count() == 0 else True

@auth.required(Role.admin)
def get_users():
	res = User.query.all()
	users = []

	for user in res:
		tmp = user.to_dict()
		tmp.pop("password", None)
		users.append(tmp)

	return(json_util.dumps(users))

@auth.required(Role.admin)
def get_user(user_id):
	user = User.query.get_or_404(user_id)
	user = user.to_dict()
	user.pop('password', None)
	return(json_util.dumps(user))

def unprotected_add_user(user_data):
	"""
	Create a user and add it to database

	Fields:
		* password
		* email
		* username
	"""
	try:
		user = User.from_dict(user_data)
	except Exception as e:
		raise UserException(str(e))

	if user.password == None:
		raise UserException("Missing password")

	user.password = auth.create_hash(user.password)

	try:
		db.db.session.add(user)
		res = db.db.session.commit()
		return user
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise UserException(str(e))

@auth.required(Role.admin)
def add_user():
	r = request.get_json()
	try:
		user = User.from_dict(r)
	except Exception as e:
		raise UserException(str(e))

	#if user_exists(user):
	#	raise UserException("User '" + user.username + "' already exists", status_code = 400)

	user = unprotected_add_user(user.to_dict())

	inserted = User.query.get_or_404(user.id)

	user = inserted.to_dict()
	user.pop("password", None)

	return(json_util.dumps(user))

@auth.required(Role.admin)
def remove_user(user_id):
	"""
	Remove the user
	"""

	user = User.query.get_or_404(user_id)

	try:
		db.db.session.delete(user)
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise UserException(str(e))

	user.password = None
	tmp = user.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def edit_user(user_id):
	"""
	TODO: differentiate between PUT and PATCH -> PATCH partial update
	"""
	user_dict = request.get_json()
	user = User.query.get_or_404(user_id)

	# If the user updates their profile check for all fields to be updated
	if "first_name" in user_dict and user_dict["first_name"]!= "":
		user.first_name = user_dict["first_name"]

	if "last_name" in user_dict and user_dict["last_name"] != "":
		user.last_name = user_dict["last_name"]

	if "email" in user_dict and user_dict["email"] != "":
		user.email = user_dict["email"]

	if "role" in user_dict and User.parseRole(user_dict["role"]) >= 0:
		user.role = User.parseRole(user_dict["role"])

	if "settings" in user_dict and user_dict["settings"] != {}:
		user.settings = user_dict["settings"]

	# In case of password change, verify that it is really them (revalidate their password)
	if "password" in user_dict and user_dict["password"] != "":
		if not auth.check_password(user_dict["password"], user.password.decode('utf8')):
			raise UserException("Password mismatch")

		try:
			user.password = auth.create_hash(user_dict["password_new"])
		except Exception as e:
			raise UserException(str(e))

	# Update the user and return updated document
	try:
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise UserException(str(e))

	# Remove password hash from the response
	user.password = None
	tmp = user.to_dict()

	return(json_util.dumps(tmp))

users.add_url_rule('', view_func=get_users, methods=['GET'])
users.add_url_rule('', view_func=add_user, methods=['POST'])
users.add_url_rule('/<string:user_id>', view_func=get_user, methods=['GET'])
users.add_url_rule('/<string:user_id>', view_func=edit_user, methods=['PUT'])
users.add_url_rule('/<string:user_id>', view_func=remove_user, methods=['DELETE'])
