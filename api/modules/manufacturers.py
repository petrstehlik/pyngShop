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
from api.models.models import Manufacturer, ManufacturerException
from api.role import Role

manufacturer = Module('manufacturers', __name__, url_prefix='/manufacturers', no_version=True)

@auth.required(Role.admin)
def count_manufacturers():
	""" FIXME not used, remove """
	return db.manufacturer.count()

@auth.required(Role.admin)
def get_manufacturers():
	res = Manufacturer.query.all()
	manufacturers = []

	for manufacturer in res:
		tmp = manufacturer.to_dict()
		manufacturers.append(tmp)

	return(json_util.dumps(manufacturers))

@auth.required(Role.admin)
def add_manufacturer():
	r = request.get_json()
	try:
		manufacturer = Manufacturer.from_dict(r)
	except Exception as e:
		raise ManufacturerException(str(e))

	try:
		db.db.session.add(manufacturer)
		res = db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		print(e)
		raise ManufacturerException(str(e))

	inserted = Manufacturer.query.get_or_404(manufacturer.id)

	manufacturer = inserted.to_dict()

	return(json_util.dumps(manufacturer))

@auth.required(Role.admin)
def remove_manufacturer(manufacturer_id):
	"""
	Remove the manufacturer
	"""

	manufacturer = Manufacturer.query.get_or_404(manufacturer_id)

	try:
		db.db.session.delete(manufacturer)
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise ManufacturerException(str(e))

	tmp = manufacturer.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def edit_manufacturer(manufacturer_id):

	manufacturer_dict = request.get_json()
	manufacturer = Manufacturer.query.get_or_404(manufacturer_id)

	# check for all fields to be updated
	if "name" in manufacturer_dict and manufacturer_dict["name"]!= "":
		manufacturer.name = manufacturer_dict["name"]

	if "first_name" in manufacturer_dict and manufacturer_dict["first_name"] != "":
		manufacturer.first_name = manufacturer_dict["first_name"]

	if "last_name" in manufacturer_dict and manufacturer_dict["last_name"] != "":
		manufacturer.last_name = manufacturer_dict["last_name"]

	if "telephone" in manufacturer_dict and manufacturer_dict["telephone"] != "":
		manufacturer.telephone = manufacturer_dict["telephone"]

	if "email" in manufacturer_dict and manufacturer_dict["email"] != "":
		manufacturer.email = manufacturer_dict["email"]

	if "id_num" in manufacturer_dict and manufacturer_dict["id_num"] != "":
		manufacturer.id_num = manufacturer_dict["id_num"]

	if "delivery_time" in manufacturer_dict and manufacturer_dict["delivery_time"] != "":
		manufacturer.delivery_time = manufacturer_dict["delivery_time"]

	# Update the manufacturer and return updated document
	try:
		db.db.session.commit()
	except Exception as e:
		db.db.session.rollback()
		raise ManufacturerException(str(e))

	tmp = manufacturer.to_dict()

	return(json_util.dumps(tmp))

@auth.required(Role.admin)
def get_manufacturer(manufacturer_id):
	manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
	manufacturer = manufacturer.to_dict()
	return(json_util.dumps(manufacturer))

manufacturer.add_url_rule('', view_func=get_manufacturers, methods=['GET'])
manufacturer.add_url_rule('', view_func=add_manufacturer, methods=['POST'])
manufacturer.add_url_rule('/<string:manufacturer_id>', view_func=get_manufacturer, methods=['GET'])
manufacturer.add_url_rule('/<string:manufacturer_id>', view_func=edit_manufacturer, methods=['PUT'])
manufacturer.add_url_rule('/<string:manufacturer_id>', view_func=remove_manufacturer, methods=['DELETE'])
