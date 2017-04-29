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
from api.models.product import Product, ProductException
from api.role import Role

products = Module('products', __name__, url_prefix='/products', no_version=True)

def count_products():
	""" FIXME not used, remove """
	return db.products.count()

def get_products():
	res = Product.query.all()
	products = []

	for product in res:
		tmp = product.to_dict()
		products.append(tmp)

	return(json_util.dumps(products))

@auth.required(Role.admin)
def add_product():
	r = request.get_json()
	try:
		product = Product.from_dict(r)
	except Exception as e:
		raise ProductException(str(e))

	try:
		db.db.session.add(product)
		res = db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise ProductException(str(e))

	inserted = Product.query.get_or_404(product.id)

	product = inserted.to_dict()

	return(json_util.dumps(product))

@auth.required(Role.admin)
def remove_product(product_id):
	"""
	Remove the product
	"""

	product = Product.query.get_or_404(product_id)

	try:
		db.db.session.delete(product)
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise ProductException(str(e))

	tmp = product.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def edit_product(product_id):

	product_dict = request.get_json()
	product = Product.query.get_or_404(product_id)

	# check for all fields to be updated
	if "name" in product_dict and product_dict["name"]!= "":
		product.name = product_dict["name"]

	if "price" in product_dict and product_dict["price"] != "":
		product.price = product_dict["price"]

	if "slug" in product_dict and product_dict["slug"] != "":
		product.slug = product_dict["slug"]

	if "description" in product_dict and product_dict["description"] != "":
		product.description = product_dict["description"]

	if "image" in product_dict and product_dict["image"] != "":
		product.image = product_dict["image"]

	if "in_stock" in product_dict and product_dict["in_stock"] != "":
		product.in_stock = product_dict["in_stock"]

	if "hidden" in product_dict and product_dict["hidden"] != "":
		product.hidden = product_dict["hidden"]

	# Update the product and return updated document
	try:
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise ProductException(str(e))

	tmp = product.to_dict()

	return(json_util.dumps(tmp))

products.add_url_rule('', view_func=get_products, methods=['GET'])
products.add_url_rule('', view_func=add_product, methods=['POST'])
# products.add_url_rule('/<string:product_id>', view_func=get_product, methods=['GET'])
products.add_url_rule('/<string:product_id>', view_func=edit_product, methods=['PUT'])
products.add_url_rule('/<string:product_id>', view_func=remove_product, methods=['DELETE'])
