"""
Author: Frederik Muller, xmulle20@stud.fit.vutbr.cz
Date:   04/2017
"""

import bcrypt
from flask import request
from bson import json_util, ObjectId
import pymongo

from api import auth, db
from api.module import Module
from api.models.models import Shipping, ShippingException
from api.role import Role

shipping = Module('shippings', __name__, url_prefix='/shippings', no_version=True)

@auth.required(Role.admin)
def count_shippings():
	""" FIXME not used, remove """
	return db.shippings.count()

def get_shippings():
	res = Shipping.query.all()
	shippings = []

	for shipping in res:
		tmp = shipping.to_dict()
		shippings.append(tmp)

	return(json_util.dumps(shippings))

@auth.required(Role.admin)
def add_shipping():
	r = request.get_json()
	try:
		shipping = Shipping.from_dict(r)
	except Exception as e:
		print(e)
		raise ShippingException("Could not convert dictionary to Shipping")

	try:
		db.db.session.add(shipping)
		res = db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise ShippingException("Could not add shipping to database")

	inserted = Shipping.query.get_or_404(shipping.id)

	shipping = inserted.to_dict()

	return(json_util.dumps(shipping))

@auth.required(Role.admin)
def remove_shipping(shipping_id):
	"""
	Remove the shipping
	"""

	shipping = Shipping.query.get_or_404(shipping_id)

	try:
		db.db.session.delete(shipping)
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise ShippingException("Could not remove shipping")

	tmp = shipping.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def edit_shipping(shipping_id):

	shipping_dict = request.get_json()
	shipping = Shipping.query.get_or_404(shipping_id)

	# check for all fields to be updated
	if "name" in shipping_dict and shipping_dict["name"]!= "":
		shipping.name = shipping_dict["name"]

	if "price" in shipping_dict and shipping_dict["price"] != "":
		shipping.price = shipping_dict["price"]

	# Update the shipping and return updated document
	try:
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise ShippingException("Could not edit shipping")

	tmp = shipping.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def get_shipping(shipping_id):
	shipping = Shipping.query.get_or_404(shipping_id)
	shipping = shipping.to_dict()
	return(json_util.dumps(shipping))


shipping.add_url_rule('', view_func=get_shippings, methods=['GET'])
shipping.add_url_rule('', view_func=add_shipping, methods=['POST'])
shipping.add_url_rule('/<string:shipping_id>', view_func=get_shipping, methods=['GET'])
shipping.add_url_rule('/<string:shipping_id>', view_func=edit_shipping, methods=['PUT'])
shipping.add_url_rule('/<string:shipping_id>', view_func=remove_shipping, methods=['DELETE'])
