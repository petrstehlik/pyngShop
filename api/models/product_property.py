"""
Author: Frederik Muller, xmulle20@stud.fit.vutbr.cz
Date: 04/2017
"""

from api.error import ApiException
from api.dbConnector import dbConnector

conn = dbConnector()
db = conn.db

class ProductPropertyException(ApiException):
    status_code = 401

class ProductProperty(db.Model):
    __tablename__ = "product_property"
    id = db.Column(db.Integer,
            db.Sequence("product_property_cid_seq", start=1, increment=1),
            primary_key=True)
    name = db.Column(db.String(255), unique=False)
    prefix = db.Column(db.String(255), unique=False)
    sufix = db.Column(db.String(10000), unique=False)

    def __init__(self,
            name,
            prefix = None,
            sufix = None,
            ):
        self.name = name
        self.id = id
        self.prefix = prefix
        self.sufix = sufix

    def to_dict(self):
        """
        Return the internal data in dictionary
        """
        tmp = {
            'name' : self.name,
            'id' : self.id,
            'prefix' : self.prefix,
            'sufix' : self.sufix,
        }

        return tmp

    @classmethod
    def from_dict(self, product_property):
        """
        Create new product_property from dictionary
        """
        return(self(
            name = product.get("name", None),
            prefix = product.get("prefix", None),
            sufix = product.get("sufix", None),
            ))

    def __repr__(self):
        return '<Product property %r>' % self.name
