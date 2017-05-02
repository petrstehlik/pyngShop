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
from api.models.models import Order, OrderException, Shipping, Customer, Product, OrderedProduct, OrderedProductException
from api.role import Role

order = Module('orders', __name__, url_prefix='/orders', no_version=True)

@auth.required(Role.admin)
def count_orders():
	""" FIXME not used, remove """
	return db.orders.count()

@auth.required(Role.admin)
def get_orders():
	res = Order.query.all()
	orders = []

	for order in res:
		tmp = order.to_dict()
		tmp["customer"] = order.customer.to_dict()
		tmp["shipping"] = order.shipping.to_dict()
		products = []
		for ordered_product in order.ordered_products:
			products.append(ordered_product.product.to_dict())
		tmp["products"] = products
		orders.append(tmp)

	return(json_util.dumps(orders))

@auth.required()
def add_order():
	r = request.get_json()

	session_id = request.headers.get('Authorization', None)
	if not session_id:
		raise SessionException("Header field 'Authorization' not found.")
	try:
		session = auth.lookup(session_id)
	except SessionException:
		raise SessionException("Session not found")

	order = {}
	order["shipping"] = Shipping.query.get_or_404(r["shipping"]["id"])
	order["customer"] = Customer.query.get_or_404(session["user"].id)
	order["status"] = "Accepted"
	products = []
	shipping = order["shipping"].to_dict()
	order["full_price"] = shipping["price"]
	for ordered_product in r["ordered_products"]:
		product = Product.query.get_or_404(ordered_product["product"]["id"])
		products.append(product)
		product_dict = product.to_dict()
		order["full_price"] += (product_dict["price"] * ordered_product["quantity"])

	order["products"] = products

	try:
		order = Order.from_dict(order)
	except Exception as e:
		print(e)
		raise OrderException("Could not convert dictionary to Order")

	try:
		db.db.session.add(order)
		res = db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise OrderException("Could not add order to database")

	inserted_order = Order.query.get_or_404(order.id)

	# create ordered_product
	for ordered_product in r["ordered_products"]:
		product = Product.query.get_or_404(ordered_product["product"]["id"])
		order_product = {}
		order_product["product"] = product
		order_product["order"] = inserted_order
		order_product["quantity"] = ordered_product["quantity"]
		try:
			order_product = OrderedProduct.from_dict(order_product)
		except Exception as e:
			print(e)
			raise OrderedProductException("Could not convert dictionary to OrderedProduct")

		try:
			db.db.session.add(order_product)
			res = db.db.session.commit()
		except Exception as e:
			db.db.session.rollback()
			print(e)
			raise OrderedProductException("Could not add ordered product to database")

	inserted = Order.query.get_or_404(order.id)

	order = inserted.to_dict()

	return(json_util.dumps(order))

@auth.required(Role.admin)
def remove_order(order_id):
	"""
	Remove the order
	"""

	ordered_products = db.db.session.query(OrderedProduct).filter_by(order_id = order_id).all()
	for ordered_product in ordered_products:
		try:
			db.db.session.delete(ordered_product)
			db.db.session.commit()
		except Exception as e:
			db.db.session.rollback()
			print(e)
			raise OrderException("Could not remove ordered product")

	order = Order.query.get_or_404(order_id)

	try:
		db.db.session.delete(order)
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise OrderException("Could not remove order")

	tmp = order.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def edit_order(order_id):

	order_dict = request.get_json()
	order = Order.query.get_or_404(order_id)

	# check for all fields to be updated
	if "status" in order_dict and order_dict["status"] != "":
		order.status = order_dict["status"]

	if "shipping" in order_dict:
		if "id" in order_dict["shipping"]:
			old_shipping = order.shipping.to_dict()
			order.shipping = Shipping.query.get_or_404(order_dict["shipping"]["id"])
			new_shipping = order.shipping.to_dict()
			order.full_price = order.full_price - old_shipping["price"] + new_shipping["price"]

	# Update the order and return updated document
	try:
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise OrderException("Could not edit order")

	tmp = order.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def get_order(order_id):
	order = Order.query.get_or_404(order_id)
	tmp = order.to_dict()
	tmp["customer"] = order.customer.to_dict()
	tmp["shipping"] = order.shipping.to_dict()
	products = []
	for ordered_product in order.ordered_products:
		products.append(ordered_product.product.to_dict())
	tmp["products"] = products

	return(json_util.dumps(tmp))


order.add_url_rule('', view_func=get_orders, methods=['GET'])
order.add_url_rule('', view_func=add_order, methods=['POST'])
order.add_url_rule('/<string:order_id>', view_func=get_order, methods=['GET'])
order.add_url_rule('/<string:order_id>', view_func=edit_order, methods=['PUT'])
order.add_url_rule('/<string:order_id>', view_func=remove_order, methods=['DELETE'])
