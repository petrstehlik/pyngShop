#/bin/env python3

import simplejson as json
import sys
from flask import Flask, request
from flask.ext.cors import CORS

from connector import *

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
	#db.query("""SELECT * FROM category WHERE category.category_id NOT IN (SELECT child FROM sub_category)""", json=False)
	#print(main_categories)
	
	# for item in main_categories:
	# 	s[str(item["category_id"])] = item
	# 	s[str(item["category_id"])]["sub"] = db.query("""SELECT DISTINCT t1.* FROM `category` t1, `sub_category` t2 WHERE t2.parent = """ + str(item["category_id"]) + """ AND t2.child = t1.category_id""", json=False)
	del db
	return json.dumps(s)

@app.route(CONFIG['version'] + '/products', methods=['POST'])
def get_products():
	if request.method == 'POST':
		tmp = request.get_json()
		db = DB()
		query = """SELECT * FROM product_category
	LEFT JOIN product ON product_category.product_id = product.product_id
	WHERE product_category.category_id = (SELECT category_id FROM category WHERE category.slug = \"""" + tmp["category"] + """\")"""
		print(query)
		products = db.query(query, False)
		#print(json.dumps(products, cls=DecimalEncoder))
			
		print(products)
		del db
		return(json.dumps(products))

if __name__ == '__main__':
    app.run(threaded=True)

   # result = db.query("SELECT * FROM `settings`")
