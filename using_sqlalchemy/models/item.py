"""Item model."""
from db import db


class ItemModel(db.Model):
    """docstring for ItemModel."""

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name, price, store_id):
        """Init item."""
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        """Return a dictonary containing JSON representation of item."""
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        """Find User by name in database and return, if not return none."""
        # SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        """Save an item to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Update an item in the database."""
        db.session.delete(self)
        db.session.commit()
