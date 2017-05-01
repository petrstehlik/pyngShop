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
from api.models.models import Product, ProductException, Review, ReviewException, Customer, ProductProperty, TypeProperty, TypePropertyException, Category, CategoryException
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
	if "name" in product_dict and product_dict["name"] != "":
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

def get_product(product_id):
	product = Product.query.get_or_404(product_id)
	product = product.to_dict()

	return(json_util.dumps(product))

@auth.required()
def add_review(product_id):
	session_id = request.headers.get('Authorization', None)
	if not session_id:
		raise SessionException("Header field 'Authorization' not found.")
	try:
		session = auth.lookup(session_id)
	except SessionException:
		raise SessionException("Session not found")

	r = request.get_json()
	r["product"] = Product.query.get_or_404(product_id)
	r["customer"] = Customer.query.get_or_404(session["user"].id)

	try:
		review = Review.from_dict(r)
	except Exception as e:
		raise ReviewException(str(e))

	try:
		db.db.session.add(review)
		res = db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise ReviewException(str(e))

	inserted = db.db.session.query(Review).\
		filter_by(product_id = product_id, customer_id = session["user"].id).first()

	review = inserted.to_dict()

	return(json_util.dumps(review))

def get_reviews(product_id):
	reviews_with_customers = []
	reviews = db.db.session.query(Review).filter_by(product_id = product_id).all()
	for review in reviews:
		customer = review.customer.to_dict()
		review = review.to_dict()
		review_customer = {"customer" : {"username" : customer["username"], 
						 "first_name" : customer["first_name"],
						  "last_name" : customer["last_name"]}}
		review.update(review_customer)
		reviews_with_customers.append(review)

	return(json_util.dumps(reviews_with_customers))

def get_properties(product_id):
	product_properties = []
	type_properties = db.db.session.query(TypeProperty).filter_by(product_id = product_id).all()
	for type_property in type_properties:
		product_property = type_property.product_property.to_dict()
		type_property = type_property.to_dict()
		type_property.update(product_property)
		product_properties.append(type_property)

	return(json_util.dumps(product_properties))

@auth.required(Role.admin)
@auth.required()
def add_property(product_id, property_id):
	r = request.get_json()
	r["product"] = Product.query.get_or_404(product_id)
	r["product_property"] = ProductProperty.query.get_or_404(property_id)

	try:
		review = TypeProperty.from_dict(r)
	except Exception as e:
		raise TypePropertyException(str(e))

	try:
		db.db.session.add(review)
		res = db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise TypePropertyException(str(e))

	inserted = db.db.session.query(TypeProperty).\
		filter_by(product_id = product_id, product_property_id = property_id).first()

	property = inserted.to_dict()

	return(json_util.dumps(property))

@auth.required(Role.admin)
def edit_property(product_id, property_id):
	property_dict = request.get_json()

	property = db.db.session.query(TypeProperty).\
		filter_by(product_id = product_id, product_property_id = property_id).first()

	# check for all fields to be updated
	if "value" in property_dict and property_dict["value"] != "":
		property.value = property_dict["value"]

	# Update the property and return updated document
	try:
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise TypePropertyException(str(e))

	inserted = db.db.session.query(TypeProperty).\
		filter_by(product_id = product_id, product_property_id = property_id).first()

	tmp = inserted.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def remove_property(product_id, property_id):
	"""
	Remove the property
	"""

	property = db.db.session.query(TypeProperty).\
		filter_by(product_id = product_id, product_property_id = property_id).first()
	try:
		db.db.session.delete(property)
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise TypePropertyException(str(e))

	tmp = property.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def add_category(product_id, category_id):
	product = Product.query.get_or_404(product_id)
	category = Category.query.get_or_404(category_id)

	category.products.append(product)

	try:
		res = db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise CategoryException(str(e))

	product = Product.query.get_or_404(product_id)
	category = Category.query.get_or_404(category_id)

	if product in category.products:
		return(json_util.dumps(product.to_dict()))

	raise CategoryException("Not found", status_code=404)

def get_categories(product_id):
	product = Product.query.get_or_404(product_id)
	categories = []

	for category in product.categories:
		categories.append(category.to_dict())

	return(json_util.dumps(categories))

@auth.required(Role.admin)
def remove_category(product_id, category_id):
	product = Product.query.get_or_404(product_id)
	category = Category.query.get_or_404(category_id)

	if category in product.categories:
		product.categories.remove(category)
	else:
		raise CategoryException("There is not such a category", status_code=404)

	try:
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise CategoryException(str(e))

	product = Product.query.get_or_404(product_id)

	if category in product.categories:
		raise CategoryException("Failed to delete", status_code=404)

	tmp = category.to_dict()

	return(json_util.dumps(tmp))

products.add_url_rule('', view_func=get_products, methods=['GET'])
products.add_url_rule('', view_func=add_product, methods=['POST'])
products.add_url_rule('/<string:product_id>', view_func=get_product, methods=['GET'])
products.add_url_rule('/<string:product_id>', view_func=edit_product, methods=['PUT'])
products.add_url_rule('/<string:product_id>', view_func=remove_product, methods=['DELETE'])
products.add_url_rule('/<string:product_id>/reviews', view_func=add_review, methods=['POST'])
products.add_url_rule('/<string:product_id>/reviews', view_func=get_reviews, methods=['GET'])
products.add_url_rule('/<string:product_id>/properties', view_func=get_properties, methods=['GET'])
products.add_url_rule('/<string:product_id>/properties/<string:property_id>', view_func=add_property, methods=['POST'])
products.add_url_rule('/<string:product_id>/properties/<string:property_id>', view_func=edit_property, methods=['PUT'])
products.add_url_rule('/<string:product_id>/properties/<string:property_id>', view_func=remove_property, methods=['DELETE'])
products.add_url_rule('/<string:product_id>/categories/<string:category_id>', view_func=add_category, methods=['POST'])
products.add_url_rule('/<string:product_id>/categories', view_func=get_categories, methods=['GET'])
products.add_url_rule('/<string:product_id>/categories/<string:category_id>', view_func=remove_category, methods=['DELETE'])
