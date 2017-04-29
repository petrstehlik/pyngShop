"""
Author: Frederik Muller, xmulle20@stud.fit.vutbr.cz
Date: 04/2017
"""

from api.error import ApiException
from api.dbConnector import dbConnector

conn = dbConnector()
db = conn.db

class ManufacturerException(ApiException):
    status_code = 401

class Manufacturer(db.Model):
    __tablename__ = "manufacturer"
    id = db.Column(db.Integer,
            db.Sequence("manufacturer_cid_seq", start=1, increment=1),
            primary_key=True)
    name = db.Column(db.String(255), unique=False)
    first_name = db.Column(db.String(255), unique=False)
    last_name = db.Column(db.String(255), unique=False)
    telephone = db.Column(db.String(20), unique=False)
    email = db.Column(db.String(255), unique=False)
    id_num = db.Column(db.String(20), unique=False)
    delivery_time = db.Column(db.String(20), unique=False)


    def __init__(self,
            name,
            first_name = None,
            last_name = None,
            telephone = None,
            email = None,
            id_num = None,
            delivery_time = None,
            ):
        self.name = name
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.telephone = telephone
        self.email = email
        self.id_num = id_num
        self.delivery_time = delivery_time

    def to_dict(self):
        """
        Return the internal data in dictionary
        """
        tmp = {
            'name' : self.name,
            'id' : self.id,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'telephone' : self.telephone,
            'email' : self.email,
            'id_num' : self.id_num,
            'delivery_time' : self.delivery_time,
        }

        return tmp

    @classmethod
    def from_dict(self, manufacturer):
        """
        Create new manufacturer from dictionary
        """
        return(self(
            name = product.get("name", None),
            first_name = product.get("first_name", None),
            last_name = product.get("last_name", None),
            telephone = product.get("telephone", None),
            email = product.get("email", None),
            id_num = product.get("id_num", None),
            delivery_time = product.get("delivery_time", None),
            ))

    def __repr__(self):
        return '<Manufacturer %r>' % self.name
