from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name
    
    def toJSON(self):
        return {'store': {'name': self.name, 'items': [item.toJSON() for item in self.items.all()]}}
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_store(self):
        db.session.add(self)
        db.session.commit()

    def delete_store(self):
        db.session.delete(self)
        db.session.commit()