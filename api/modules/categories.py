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
from api.models.models import Category, CategoryException
from api.role import Role

category = Module('categories', __name__, url_prefix='/categories', no_version=True)

@auth.required(Role.admin)
def count_categories():
	""" FIXME not used, remove """
	return db.category.count()

def get_categories():
	res = Category.query.all()
	categories = []

	for category in res:
		tmp = category.to_dict()
		categories.append(tmp)

	return(json_util.dumps(categories))

@auth.required(Role.admin)
def add_category():
	r = request.get_json()
	try:
		category = Category.from_dict(r)
	except Exception as e:
		raise CategoryException(str(e))

	try:
		db.db.session.add(category)
		res = db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise CategoryException(str(e))

	inserted = Category.query.get_or_404(category.id)

	category = inserted.to_dict()

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
		raise CategoryException(str(e))

	## MISSING
	## if category has children, direct descendants will lose the parent

	tmp = category.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def edit_category(category_id):

	category_dict = request.get_json()
	category = Category.query.get_or_404(category_id)

	# check for all fields to be updated
	if "name" in category_dict and category_dict["name"]!= "":
		category.name = category_dict["name"]

	if "description" in category_dict and category_dict["description"] != "":
		category.description = category_dict["description"]

	if "slug" in category_dict and category_dict["slug"] != "":
		category.slug = category_dict["slug"]

	if "hidden" in category_dict and category_dict["hidden"] != "":
		category.hidden = category_dict["hidden"]

	# Update the category and return updated document
	try:
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise CategoryException(str(e))

	tmp = category.to_dict()

	return(json_util.dumps(tmp))

def get_category(category_id):
	category = Category.query.get_or_404(category_id)
	category = category.to_dict()

	## MISSING
	## get all its products

	return(json_util.dumps(category))

category.add_url_rule('', view_func=get_categories, methods=['GET'])
category.add_url_rule('', view_func=add_category, methods=['POST'])
category.add_url_rule('/<string:category_id>', view_func=get_category, methods=['GET'])
category.add_url_rule('/<string:category_id>', view_func=edit_category, methods=['PUT'])
category.add_url_rule('/<string:category_id>', view_func=remove_category, methods=['DELETE'])
