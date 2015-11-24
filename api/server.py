#/bin/env python3

import json
import sys
from flask import Flask

from connector import *

app = Flask(__name__)
app.debug = True

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

db = DB()

@app.route(CONFIG['version'] + '/categories')
def get_categories():
	main_categories = db.query("""SELECT * FROM category WHERE category.category_id NOT IN (SELECT child FROM sub_category)""", json=False)
	#sub_categories = db.query("""SELECT * FROM `category` WHERE `parent` IS NOT NULL""", json=False)

	#test = db.query("""select * from `category` as item
#inner join category c on c.parent = item.category_id """, json=False)

	s = dict()

	#print(json.dumps(test))
	
	for item in main_categories:
		s[str(item["category_id"])] = item
		s[str(item["category_id"])]["sub"] = db.query("""SELECT DISTINCT t1.* FROM `category` t1, `sub_category` t2 WHERE t2.parent = """ + str(item["category_id"]) + """ AND t2.child = t1.category_id""", json=False)


	# for idx,item in enumerate(sub_categories):
	# 	parent = str(item["parent"])
	# 	print(parent)
	# 	if parent in s:
	# 		s[parent]["sub"][idx] = item
	# 		#s[item["parent"]]["sub"] = item

	# print(json.dumps(s, indent=4))

		#if item["parent"] != NULL
	return json.dumps(s)

if __name__ == '__main__':
    app.run(threaded=True)

    result = db.query("SELECT * FROM `settings`")
