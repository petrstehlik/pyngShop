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
from api.models.models import ProductProperty, ProductPropertyException
from api.role import Role

product_property = Module('product_property', __name__, url_prefix='/product_property', no_version=True)

@auth.required(Role.admin)
def count_products_property():
	""" FIXME not used, remove """
	return db.product_property.count()

@auth.required(Role.admin)
def get_product_properties():
	res = ProductProperty.query.all()
	product_properties = []

	for product_property in res:
		tmp = product_property.to_dict()
		product_properties.append(tmp)

	return(json_util.dumps(product_properties))

@auth.required(Role.admin)
def add_product_property():
	r = request.get_json()
	try:
		product_property = ProductProperty.from_dict(r)
	except Exception as e:
		raise ProductException(str(e))

	try:
		db.db.session.add(product_property)
		res = db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise ProductException(str(e))

	inserted = Product.query.get_or_404(product_property.id)

	product_property = inserted.to_dict()

	return(json_util.dumps(product_property))

@auth.required(Role.admin)
def remove_product_property(product_property_id):
	"""
	Remove the product_property
	"""

	product_property = ProductProperty.query.get_or_404(product_property_id)

	try:
		db.db.session.delete(product_property)
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise ProductException(str(e))

	tmp = product_property.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def edit_product_property(product_property_id):

	product_property_dict = request.get_json()
	product_property = ProductProperty.query.get_or_404(product_property_id)

	# check for all fields to be updated
	if "name" in product_property_dict and product_property_dict["name"]!= "":
		product_property.name = product_property_dict["name"]

	if "prefix" in product_property_dict and product_property_dict["prefix"] != "":
		product_property.prefix = product_property_dict["prefix"]

	if "sufix" in product_property_dict and product_property_dict["sufix"] != "":
		product_property.sufix = product_property_dict["sufix"]

	# Update the product_property and return updated document
	try:
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise ProductException(str(e))

	tmp = product_property.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def get_product_property(product_property_id):
	product_property = ProductProperty.query.get_or_404(product_property_id)
	product_property = product_property.to_dict()
	return(json_util.dumps(product_property))

product_property.add_url_rule('', view_func=get_product_properties, methods=['GET'])
product_property.add_url_rule('', view_func=add_product_property, methods=['POST'])
product_property.add_url_rule('/<string:product_property_id>', view_func=get_product_property, methods=['GET'])
product_property.add_url_rule('/<string:product_property_id>', view_func=edit_product_property, methods=['PUT'])
product_property.add_url_rule('/<string:product_property_id>', view_func=remove_product_property, methods=['DELETE'])
