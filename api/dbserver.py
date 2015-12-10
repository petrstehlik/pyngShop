#/bin/env python3

import simplejson as json
import sys
from flask import Flask, request, session
from flask.ext.cors import CORS
import pdb
from datetime import datetime
import hashlib
from slugify import slugify

from connector import *
from mail import *

app = Flask(__name__)
app.debug = True

CORS(app)

app.secret_key = 'pyngshop'


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route(CONFIG['version'] + '/categories', methods=['GET', 'DELETE', 'POST'])
def get_categories():
	if request.method == 'GET': 
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

	if request.method == 'DELETE':
		r = request.get_json()
		db = DB()

		query = "UPDATE `category` SET `hidden` = '1' WHERE `category`.`category_id` = \'" + str(r["category_id"]) + "\'"
		db.cursor.execute(query)
		db.db.commit()
		del db
		return("OK")

	if request.method == 'POST':
		db = DB()
		r = request.get_json()
		print(r)
		data = {
			'name' : r["name"],
			'description' : r["description"],
			'slug' : slugify(r["name"]),
			'parent' : r["parent"],
			'category_id' : r["category_id"]
		}
		query = "UPDATE `category` SET name = %(name)s, description = %(description)s, slug = %(slug)s, parent = %(parent)s WHERE category_id = %(category_id)s"

		db.cursor.execute(query, data)
		db.db.commit()
		del db
		return("OK")


@app.route(CONFIG['version'] + '/addcategory', methods=['POST'])
def add_cat():
	if request.method == 'POST':
		db = DB()
		cat = request.get_json()
		data = {
			'slug' : slugify(cat["name"]),
			'name' : cat["name"],
			'parent' : cat["parent"]
		}
		query = """INSERT INTO category (`name`, `slug`, `parent`) VALUES (%(name)s, %(slug)s, %(parent)s)"""
		res = db.cursor.execute(query, data)
		db.db.commit()

		#print(json.dumps(newcat))
		#print(cat)
		row = db.cursor.lastrowid
		del db
		return(str(row))


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
		cat = db.query("SELECT * FROM category WHERE category.slug = \"" + categories + "\"", False)

		final = {
			'category' : cat,
			'products' : res
		}

		del db
		return(json.dumps(final))

@app.route(CONFIG['version'] + '/product', methods=['POST', 'DELETE'])
def product():
	if request.method == 'POST':
		p = request.get_json()
		db = DB()
		query = """SELECT product.name, product.product_id, product.slug, product.description, product.price, product.image, product.in_stock, manufacturer.manufacturer_id, manufacturer.name as man_name FROM product LEFT JOIN product_supplier on product.product_id = product_supplier.product_id LEFT JOIN manufacturer ON product_supplier.manufacturer_id = product_supplier.manufacturer_id WHERE product.slug = \'""" + p + "\';"
		res = db.query(query, False)
		return(json.dumps(res))
	if request.method == 'DELETE':
		p = request.get_json()
		db = DB()

		query = "UPDATE `product` SET `hidden` = '1' WHERE `product`.`product_id` = \'" + str(p["product_id"]) + "\'"
		db.cursor.execute(query)
		db.db.commit()
		del db
		return("OK")

@app.route(CONFIG['version'] + '/addproduct', methods=['POST'])
def addproduct():
	if request.method == 'POST':
		db = DB()
		p = request.get_json()
		print(p)
		query = "INSERT INTO product (`name`, `slug`, `description`, `price`, `image`, `in_stock`) VALUES (%(name)s, %(slug)s, %(description)s, %(price)s, %(image)s, %(in_stock)s)"
		data = p["product"]
		data["slug"] = slugify(p["product"]["name"])
		db.cursor.execute(query, data)
		prod_id = db.cursor.lastrowid

		query = "INSERT INTO product_category VALUES (%(product_id)s, %(category_id)s)"
		data = {
			'product_id' : prod_id,
			'category_id' : p["category"]["category_id"]
		}
		db.cursor.execute(query, data)

		query = "INSERT INTO product_supplier VALUES (%(product_id)s, %(manufacturer_id)s)"
		data = {
			'product_id' : prod_id,
			'manufacturer_id' : p["supplier"]["manufacturer_id"]
		}
		db.cursor.execute(query, data)
		db.db.commit()
		del db
		return("OK")

@app.route(CONFIG['version'] + '/updateproduct', methods=['POST'])
def updateproduct():
	if request.method == 'POST':
		db = DB()
		r = request.get_json()
		print(json.dumps(r))
		query = "UPDATE product SET price = %(price)s, image = %(image)s, name = %(name)s, description = %(description)s, in_stock = %(in_stock)s, slug = %(slug)s WHERE product_id = %(product_id)s"
		data = {
			'price' :r["product"]["price"],
			'image' : r["product"]["image"],
			'name' : r["product"]["name"],
			'description' : r["product"]["description"],
			'in_stock' : r["product"]["in_stock"],
			'slug' : slugify(r["product"]["name"]),
			'product_id' : r["product"]["product_id"]
		}

		db.cursor.execute(query, data)

		if r["supplier"] != None:
			print("we should do the manufacturer")

		db.db.commit()
		del db
		return("OK")


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
		query = """SELECT * FROM  `review` LEFT JOIN customer ON review.customer_id = customer.customer_id WHERE review.product_id = \'""" + str(r_id) + "\'"
		res = db.query(query, False)
		del db
		return(json.dumps(res))

@app.route(CONFIG['version'] + '/newreview', methods=['POST'])
def newreview():
	if request.method == 'POST':
		db = DB()
		data = request.get_json()
		query = """INSERT INTO `review` (`product_id`, `customer_id`, `content`, `rating`, `timestamp`) 
		VALUES (%(product_id)s, %(customer_id)s, %(content)s, %(rating)s, %(timestamp)s);"""
		data["timestamp"] = datetime.now()
		print(data)
		res = db.cursor.execute(query, data)
		db.db.commit()
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

		print(data)

		if "customer_id" not in customer:
			query = """INSERT INTO `customer` (`first_name`, `last_name`, `email`, `address_1`, `telephone`, `city`, `postal_code`) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(address_1)s, %(telephone)s, %(city)s, %(postal_code)s); """
			print(data)
			customer_data = {
				'first_name'	: customer["first_name"],
				'last_name'		: customer["last_name"],
				'email'			: customer["email"],
				'address_1'		: customer["address_1"],
				'telephone'		: customer["telephone"],
				'city'			: customer["city"],
				'postal_code'	: customer["postal_code"]
			}
			res = db.cursor.execute(query, customer_data)
			db.db.commit()
			cust_id = db.cursor.lastrowid
		else:
			cust_id = customer["customer_id"]

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


		#sendmail(customer["email"], "Hello " + customer["first_name"])

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

@app.route(CONFIG['version'] + '/login', methods=['POST'])
def login():
	if request.method == 'POST':
		db = DB()

		role = {
			'admin' : False,
			'customer'	: False,
			'details'	: None,
			'session' 	: None
		}
		cred = request.get_json()

		h = hashlib.sha256(cred['password'].encode('utf-8'))
		print(h.hexdigest())
		query = "SELECT email FROM `users` WHERE email = \'" + cred['email'] + "\' AND password = \'" + str(h.hexdigest()) + "\';"
		res = db.query(query, False)
		
		if not res:
			query = "SELECT * from `customer` WHERE email = \'" + cred['email'] + "\' AND password = \'" + str(h.hexdigest()) + "\';"
			res = db.query(query, False)
			if res:
				role['customer'] = True
				role['details'] = res[0]
		else:
			role['admin'] = True
			session['pyngshop_user'] = cred['email']
			session['pyngshop_pwd'] = str(h.hexdigest())
			role['session'] = {
				'user' : session['pyngshop_user'],
				'password' : session['pyngshop_pwd'][-10:]
				}
		del db
		return(json.dumps(role))

@app.route(CONFIG['version'] + '/register', methods=['POST'])
def register():
	if request.method == 'POST':
		db = DB()
		req = request.get_json()
		#res = db.query()
		query = "INSERT INTO `customer` (email, password, first_name, last_name, city, address_1, postal_code, telephone) VALUES (%(email)s, %(password)s, %(first_name)s, %(last_name)s, %(city)s, %(address_1)s, %(postal_code)s, %(telephone)s)"
		tmphash = hashlib.sha256(req['password'].encode('utf-8'))
		req['password'] = str(tmphash.hexdigest())
		db.cursor.execute(query, req)
		db.db.commit()
		del db
		return(str(1))


@app.route(CONFIG['version'] + '/checklogin', methods=['POST'])
def checklogin():
	if request.method == 'POST':
		db = DB()
		cred = request.get_json()

		query = "SELECT email FROM `users` WHERE email = \'" + cred['user'] + "\' AND (SELECT RIGHT(password, 10)) = \'" + cred['password'] + "\';"
		res = db.query(query, False)

		if res:
			del db
			return (str(1));
		else:
			query = "SELECT email FROM `customer` WHERE email = \'" + cred['user'] + "\' AND (SELECT RIGHT(password, 10)) = \'" + cred['password'] + "\';"
			res = db.query(query, False)
			if res:
				del db
				return(str(1))
		del db
		return(str(0))

@app.route(CONFIG['version'] + '/orders', methods=['GET'])
def orders():
	if request.method == 'GET':
		db = DB()

		query = """SELECT * FROM customer_order
JOIN customer on customer_order.customer_id = customer.customer_id
"""
		res = db.query(query, False)
		del db
		return(json.dumps(res))

@app.route(CONFIG['version'] + '/orders/<order_id>', methods=['GET'])
def get_order(order_id):
	db = DB()
	order = {
		'customer' : None,
		'products' : None,
		'shipping' : None
	}
	query = """SELECT * FROM customer_order JOIN customer ON customer_order.customer_id = customer.customer_id WHERE customer_order.order_id = \'""" + order_id + "\';"
	res = db.query(query, False)
	order["customer"] = res[0]

	query = "SELECT * FROM `ordered_products` LEFT JOIN `product` ON ordered_products.product_id = product.product_id WHERE ordered_products.order_id = \'" + order_id + "\';"
	res = db.query(query, False)
	order["products"] = res

	query = "SELECT * FROM `shipping` WHERE shipping_id = \'" + str(order['customer']['shipping_id']) + "\'"
	res = db.query(query, False)
	order["shipping"] = res[0]

	return(json.dumps(order))

@app.route(CONFIG['version'] + '/warehouse', methods=['GET', 'POST', 'DELETE'])
def warehouse():
	# GET all products and its in stock values
	if request.method == 'GET':
		db = DB()
		res = {
			'products' : None,
			'man'		: None
		}
		query = """SELECT 
					product.name as pname, 
					product.product_id as pproduct_id, 
					product.slug as slug, 
					product.price as pprice, 
					product.in_stock as pin_stock,
					m.manufacturer_id,
					m.name,
					m.first_name,
					m.last_name,
					m.telephone,
					m.email
					FROM `product` LEFT JOIN product_supplier ON product.product_id = product_supplier.product_id LEFT JOIN manufacturer as m ON product_supplier.manufacturer_id = m.manufacturer_id """
		res['products'] = db.query(query, False)
		res['man'] = db.query("SELECT * FROM manufacturer", False)
		del db
		return(json.dumps(res))
	if request.method == 'POST':
		db = DB()
		query = """INSERT INTO `manufacturer` (`name`, `first_name`, `last_name`, `telephone`, `email`, `id_num`) VALUES (%(name)s, %(first_name)s, %(last_name)s, %(telephone)s, %(email)s, %(id_num)s)"""
		data = request.get_json()
		res = db.cursor.execute(query, data)
		db.db.commit()
		man_id = db.cursor.lastrowid
		del db
		return(str(man_id))

	if request.method == 'DELETE':
		db = DB()
		req = request.get_json()
		query = "DELETE FROM manufacturer WHERE manufacturer_id = %(manufacturer_id)s"
		db.cursor.execute(query, req)
		db.db.commit()
		del db
		return(str(1))

@app.route(CONFIG['version'] + '/admins', methods=['GET', 'POST', 'DELETE'])
def admins():
	db = DB()
	if request.method == 'GET':
		res = db.query("SELECT email FROM users", False)
		del db
		return(json.dumps(res))

	if request.method == 'POST':
		req = request.get_json()
		tmphash = hashlib.sha256(req['password'].encode('utf-8'))
		req['password'] = str(tmphash.hexdigest())
		query = "INSERT INTO `users` VALUES (%(email)s, %(password)s)"
		db.cursor.execute(query, req)
		db.db.commit()
		del db
		return(str(1))

	if request.method == 'DELETE':
		req = request.get_json()
		query = "DELETE FROM users WHERE email = %(email)s "
		db.cursor.execute(query, req)
		db.db.commit()
		del db
		return(str(1))

@app.route(CONFIG['version'] + '/updateorder', methods=['POST'])
def updateorder():
	if request.method == 'POST':
		db = DB()
		r = request.get_json()

		query = "UPDATE `customer_order` SET `status` = %(status)s WHERE `order_id` = %(order_id)s"
		db.cursor.execute(query, r)
		db.db.commit()
		del db
		return("OK")

@app.route(CONFIG['version'] + '/customerorders', methods=['POST'])
def custord():
	if request.method == 'POST':
		db = DB()
		r = request.get_json()
		print(r)
		query = "SELECT DISTINCT * FROM customer_order LEFT JOIN ordered_products ON customer_order.order_id = ordered_products.order_id LEFT JOIN product ON ordered_products.product_id = product.product_id WHERE customer_id = \'" + str(r) + "\' GROUP BY customer_order.order_id ORDER BY customer_order.order_id"

		res = db.query(query, False)
		del db
		return(json.dumps(res))



if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)

   # result = db.query("SELECT * FROM `settings`")
