#/bin/env python3

import simplejson as json
import sys
from flask import Flask, request
from flask.ext.cors import CORS
import pdb
from datetime import datetime
import hashlib

from connector import *
from mail import *

app = Flask(__name__)
app.debug = True

CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route(CONFIG['version'] + '/categories')
def get_categories():
	db = DB()
	main = "SELECT * FROM category WHERE category.parent IS NULL"
	main_categories = db.query(main, False)

	#sub = "SELECT * FROM category WHERE category.parent = (SELECT category_id FROM category WHERE category.parent IS NULL)"

	#sub_cat = db.query(sub, False)
	s = dict()
	for item in main_categories:
		cat_id = str(item["category_id"])
		s[cat_id] = item
		s[cat_id]["sub"] = db.query("SELECT * FROM category WHERE category.parent = " + cat_id, False)
	del db
	return json.dumps(s)

@app.route(CONFIG['version'] + '/products', methods=['POST'])
def get_products():
	if request.method == 'POST':
		tmp = request.get_json()
		#categories = tmp["category"].split("/")
		categories = tmp["category"]
		db = DB()
		# get categories

		query = """SELECT * FROM category
		LEFT JOIN product_category ON category.category_id = product_category.category_id 
		LEFT JOIN product ON product_category.product_id = product.product_id
		WHERE category.slug = \"""" + categories + """\""""
		
		res = db.query(query, False)

		query = """SELECT * FROM category
LEFT JOIN product_category ON category.category_id = product_category.category_id
LEFT JOIN product ON product_category.product_id = product.product_id
WHERE category.parent = \'""" + str(res[0]["category_id"]) + "\'"
		subres = db.query(query, False)
		res += subres

		del db
		return(json.dumps(res))

@app.route(CONFIG['version'] + '/product', methods=['POST'])
def product():
	if request.method == 'POST':
		p = request.get_json()
		db = DB()
		query = """SELECT * FROM product WHERE product.slug = \'""" + p + "\';"
		res = db.query(query, False)
		return(json.dumps(res))

@app.route(CONFIG['version'] + '/checkpage', methods=['POST'])
def checkpage():
	if request.method == 'POST':
		pages = request.get_json()
		db = DB()
		# query = """SELECT * FROM product WHERE product.slug = """ + pages["product"]
		# res = db.query(query, True)
		return(str(1))

@app.route(CONFIG['version'] + '/shipping', methods=['GET'])
def shipping():
	if request.method == 'GET':
		db = DB()
		query = """SELECT * FROM  `shipping` ORDER BY `price` ASC"""
		res = db.query(query, False)
		del db
		return(json.dumps(res))

@app.route(CONFIG['version'] + '/reviews', methods=['POST'])
def reviews():
	if request.method == 'POST':
		db = DB()
		r_id = request.get_json()
		query = """SELECT * FROM  `review` WHERE review.product_id = \'""" + str(r_id) + "\'"
		res = db.query(query, False)
		del db
		return(json.dumps(res))

@app.route(CONFIG['version'] + '/order', methods=['POST'])
def order():
	if request.method == 'POST':
		db = DB()
		data = request.get_json();
		customer = data["customer"]
		shipping = data["shipping"]
		cart = data["cart"]

		query = """INSERT INTO `customer` (`first_name`, `last_name`, `email`, `address_1`, `telephone`, `city`) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(address_1)s, %(telephone)s, %(city)s); """
		customer_data = {
			'first_name'	: customer["name"],
			'last_name'		: customer["surname"],
			'email'			: customer["email"],
			'address_1'		: customer["address"],
			'telephone'		: customer["tel"],
			'city'			: customer["town"]
		}
		res = db.cursor.execute(query, customer_data)
		db.db.commit()
		cust_id = db.cursor.lastrowid

		# Get total price of the order
		total_price = 0
		for item in cart["items"]:
			total_price += item["price"] * item["quantity"]

		# Don't forget the shipping
		total_price += shipping["price"]

		query = """INSERT INTO `customer_order` (`customer_id`, `shipping_id`, `timestamp`, `status`, `full_price`) VALUES (%(customer_id)s, %(shipping_id)s, %(timestamp)s, %(status)s, %(full_price)s)"""
		order_data = {
			'customer_id' 	: int(cust_id),
			'shipping_id' 	: int(shipping["shipping_id"]),
			'timestamp'		: datetime.now(),
			'status'		: "waiting",
			'full_price'	: total_price
		}

		print(order_data)

		res_order = db.cursor.execute(query, order_data)
		db.db.commit()

		order_id = db.cursor.lastrowid

		ordered_products = list()
		for item in cart["items"]:
			ordered_products.append((item["product_id"], order_id, item["quantity"]))

		query = """INSERT INTO `ordered_products` (`product_id`, `order_id`, `quantity`) VALUES (%s, %s, %s)"""
		db.cursor.executemany(query, ordered_products)
		db.db.commit()

		sendmail(customer["email"], "Hello " + customer["name"])

		del db
		return(str(1))

@app.route(CONFIG['version'] + '/invoice', methods=['POST'])
def invoice():
	if request.method == 'POST':
		db = DB()
		req = request.get_json()
		result = {}
		query = "SELECT * FROM `customer` WHERE email = \'" + req["email"] + "\';"
		res = db.query(query, False)
		if not res:
			result = {
				'valid' : 'false'
			}
		else:
			query = "SELECT * FROM `customer_order` WHERE order_id = \'" + str(req["invoicenum"]) + "\' AND customer_id = \'" + str(res[0]["customer_id"]) + "\';"
			order = db.query(query, False)
			if not order:
				result = {
					'valid' : 'false'
				}
			else:
				query = "SELECT * FROM `ordered_products` LEFT JOIN `product` ON ordered_products.product_id = product.product_id WHERE ordered_products.order_id = \'" + str(req["invoicenum"]) + "\';"
				prod = db.query(query, False)
				print(order[0]["shipping_id"])
				query = "SELECT * FROM `shipping` WHERE shipping_id = \'" + str(order[0]["shipping_id"]) + "\'"
				shipping = db.query(query, False)
				result = {
					'valid' : 'true',
					'order' : order[0],
					'customer' : res[0],
					'products' : prod,
					'shipping' : shipping[0]
				}

		print(result)
		
		del db
		return(json.dumps(result))


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)

   # result = db.query("SELECT * FROM `settings`")
