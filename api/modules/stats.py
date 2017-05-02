"""
Author: Matej Vido, xvidom00@stud.fit.vutbr.cz
Author: Frederik Muller, xmulle20@stud.fit.vutbr.cz
Date:   04/2017
"""

from flask import request
from bson import json_util

from .. import auth, db
from ..module import Module
from ..models.models import Order, OrderedProduct, Product, Review
from ..role import Role
from ..session import SessionException
from sqlalchemy import and_
from sqlalchemy.sql import func, desc

stats = Module('stats', __name__, url_prefix='/stats', no_version=True)

def filter_criterion(ts, from_, to_):
	if from_ == None and to_ == None:
		return (True)
	elif from_ == None and to_ != None:
		return (ts <= to_)
	elif from_ != None and to_ == None:
		return (ts >= from_)
	elif from_ != None and to_ != None:
		return (and_(ts >= from_, ts <= to_))

@auth.required(Role.admin)
def get_orders():
	arg_from = request.args.get("from", None)
	arg_to = request.args.get("to", None)
	arg_products_count = request.args.get("products_count", None)

	orders = {}
	if arg_from != None:
		arg_from = int(arg_from)
		orders["from"] = arg_from
	if arg_to != None:
		arg_to = int(arg_to)
		orders["to"] = arg_to
	if arg_products_count != None:
		arg_products_count = int(arg_products_count)
		orders["products_count"] = arg_products_count

	orders["count"] = Order.query.filter(filter_criterion(Order.timestamp, arg_from, arg_to)).count()
	if orders["count"] == None:
		orders["count"] = 0

	orders["average"] = db.db.session.query(
			func.avg(Order.full_price).label('average')
			).filter(filter_criterion(Order.timestamp, arg_from, arg_to)).all()[0][0]
	if orders["average"] == None:
		orders["average"] = 0

	orders["sum"] = db.db.session.query(
			func.sum(Order.full_price).label('sum')
			).filter(filter_criterion(Order.timestamp, arg_from, arg_to)).all()[0][0]
	if orders["sum"] == None:
		orders["sum"] = 0

	sold_products = []
	if OrderedProduct.query.count() > 0:
		tmp = db.db.session.query(
				OrderedProduct.product_id, func.count(OrderedProduct.product_id).label('qty')
				).filter(and_(filter_criterion(Order.timestamp, arg_from, arg_to), OrderedProduct.order_id == Order.id)).\
						group_by(OrderedProduct.product_id).\
						order_by(desc('qty')).\
						limit(1 if arg_products_count == None else arg_products_count)
		for item in tmp:
			product_id = item[0]
			quantity = item[1]
			product = Product.query.get_or_404(product_id)
			sold_products.append({"product" : product.to_dict(), "quantity" : quantity})
	orders["sold_products"] = sold_products

	return(json_util.dumps(orders))

@auth.required(Role.admin)
def get_products():
	arg_from = request.args.get("from", None)
	arg_to = request.args.get("to", None)
	arg_products_count = request.args.get("products_count", None)

	products = {}
	if arg_from != None:
		arg_from = int(arg_from)
		products["from"] = arg_from
	if arg_to != None:
		arg_to = int(arg_to)
		products["to"] = arg_to
	if arg_products_count != None:
		arg_products_count = int(arg_products_count)
		products["products_count"] = arg_products_count

	products["count"] = Product.query.count()

	popular_products = []
	if Review.query.count() > 0:
		tmp = db.db.session.query(
				Review.product_id, func.avg(Review.rating).label('rating')
				).filter(filter_criterion(Review.timestamp, arg_from, arg_to)).\
						order_by(desc('rating')).limit(1 if arg_products_count == None else arg_products_count)
		for item in tmp:
			product_id = item[0]
			rating_avg = item[1]
			product = Product.query.get_or_404(product_id)
			popular_products.append({"product" : product.to_dict(), "rating" : rating_avg})
	products["popular_products"] = popular_products

	return(json_util.dumps(products))

stats.add_url_rule('/products', view_func=get_products, methods=['GET'])
stats.add_url_rule('/orders', view_func=get_orders, methods=['GET'])

