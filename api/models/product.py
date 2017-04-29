"""
Author: Frederik Muller, xmulle20@stud.fit.vutbr.cz
Date: 04/2017
"""

from api.error import ApiException
from api.dbConnector import dbConnector

conn = dbConnector()
db = conn.db

class ProductException(ApiException):
    status_code = 401

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer,
            db.Sequence("product_cid_seq", start=1, increment=1),
            primary_key=True)
    name = db.Column(db.String(255), unique=False)
    slug = db.Column(db.String(255), unique=False)
    description = db.Column(db.String(10000), unique=False)
    price = db.Column(db.Float, unique=False, default=0.00)
    image = db.Column(db.String(255), unique=False)
    in_stock = db.Column(db.Integer, unique=False, default=0)
    hidden = db.Column(db.Boolean, unique=False, default=True)

    def __init__(self,
            name,
            price,
            id = None,
            slug = None,
            description = None,
            image = None,
            in_stock = None,
            hidden = None,
            ):
        self.name = name
        self.id = id
        self.slug = slug
        self.description = description
        self.price = price
        self.image = image
        self.in_stock = in_stock
        self.hidden = hidden

    def to_dict(self):
        """
        Return the internal data in dictionary
        """
        tmp = {
            'name' : self.name,
            'id' : self.id,
            'slug' : self.slug,
            'description' : self.description,
            'price' : self.price,
            'image' : self.image,
            'in_stock' : self.in_stock,
            'hidden': self.hidden,
        }

        return tmp

    @classmethod
    def from_dict(self, product):
        """
        Create new product from dictionary
        """
        return(self(
            name = product.get("name", None),
            id = product.get("id", None),
            slug = product.get("slug", None),
            description = product.get("description", None),
            price = product.get("price", None),
            image = product.get("image", None),
            in_stock = product.get("in_stock", None),
            hidden = product.get("hidden", None),
            ))

    def __repr__(self):
        return '<Product %r>' % self.name
