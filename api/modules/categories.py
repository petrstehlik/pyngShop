"""
Author: Frederik Muller, xmulle20@stud.fit.vutbr.cz
Author: Matej Vido, xvidom00@stud.fit.vutbr.cz
Date:   04/2017
"""

import bcrypt
from flask import request
from bson import json_util, ObjectId
import pymongo
from slugify import slugify

from api import auth, db
from api.module import Module
from api.models.models import Category, CategoryException
from api.role import Role

category = Module('categories', __name__, url_prefix='/categories', no_version=True)

def get_categories():
	res = Category.query.all()
	categories = []
	for category in res:
		if category.parent == None:
			tmp = category.to_dict()
			tmp["children"] = category.children_dict()
			categories.append(tmp)
	return(json_util.dumps(categories))

@auth.required(Role.admin)
def add_category():
	r = request.get_json()
	r.pop("products", [])
	r.pop("children", [])
	parent_dict = r.pop("parent", None)
	parent = None
	if parent_dict != None:
		parent_id = parent_dict.get("id", None)
		if parent_id != None:
			parent = Category.query.get_or_404(parent_id)
	try:
		category = Category.from_dict(r)
	except Exception as e:
		print(e)
		raise CategoryException("Could not convert dictionary to Category")

	try:
		if parent != None:
			parent.children.append(category)
		category.slug = slugify(category.name, to_lower=True)
		db.db.session.add(category)
		res = db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise CategoryException("Could not add category to database")

	inserted = Category.query.get_or_404(category.id)

	category = inserted.to_dict()
	category["parent"] = inserted.parent_dict()

	return(json_util.dumps(category))

@auth.required(Role.admin)
def remove_category(category_id):
	"""
	Remove the category
	"""

	category = Category.query.get_or_404(category_id)

	try:
		db.db.session.delete(category)
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise CategoryException("Could not remove category from database")

	tmp = category.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def edit_category(category_id):

	category_dict = request.get_json()
	category = Category.query.get_or_404(category_id)

	# check for all fields to be updated
	if "name" in category_dict and category_dict["name"]!= "":
		category.name = category_dict["name"]
		category.slug = slugify(category.name, to_lower=True)

	if "description" in category_dict and category_dict["description"] != "":
		category.description = category_dict["description"]

	if "slug" in category_dict and category_dict["slug"] != "":
		category.slug = category_dict["slug"]

	if "hidden" in category_dict and category_dict["hidden"] != "":
		category.hidden = category_dict["hidden"]

	parent_dict = category_dict.get("parent", None)
	if parent_dict != None:
		parent_id = parent_dict.get("id", None)
		if parent_id != None:
			parent = Category.query.get(parent_id)
			if parent != None:
				category.parent = parent

	# Update the category and return updated document
	try:
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise CategoryException("Could not edit category")

	tmp = category.to_dict()
	tmp["parent"] = category.parent_dict()
	tmp["children"] = category.children_dict()

	return(json_util.dumps(tmp))

def get_category(category_id):
	category = Category.query.get_or_404(category_id)
	category_dict = category.to_dict()
	category_dict["products"] = category.products_dict()
	category_dict["parent"] = category.parent_dict()
	category_dict["children"] = category.children_with_products_dict()
	return(json_util.dumps(category_dict))

category.add_url_rule('', view_func=get_categories, methods=['GET'])
category.add_url_rule('', view_func=add_category, methods=['POST'])
category.add_url_rule('/<string:category_id>', view_func=get_category, methods=['GET'])
category.add_url_rule('/<string:category_id>', view_func=edit_category, methods=['PUT'])
category.add_url_rule('/<string:category_id>', view_func=remove_category, methods=['DELETE'])
