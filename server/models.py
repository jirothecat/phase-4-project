from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

# Models go here!

class BubbleTea(db.Model, SerializerMixin):
    __tablename__ = "bubble_tea"

    id = db.Column(db.Integer, primary_key=True)
    franchise = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    topping = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    
