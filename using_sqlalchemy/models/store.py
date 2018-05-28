"""Store model."""
from db import db


class StoreModel(db.Model):
    """docstring for StoreModel"""
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def json(self):
        """Return the JSON representation of an object."""
        return {
            "name": self.name,
            "items": [item.json() for item in self.items.all()],
        }

    @classmethod
    def find_by_name(cls, name):
        """Find store entry via name."""
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        """Save store entry."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete store entry."""
        db.session.delete(self)
        db.session.commit()
