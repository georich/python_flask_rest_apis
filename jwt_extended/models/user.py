"""User model."""
from db import db


class UserModel(db.Model):
    """Holds users for crude database."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        """Init user."""
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        """Find user by username and return row information."""
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        """Find user by id and return row information."""
        return cls.query.filter_by(id=_id)

    def save_to_db(self):
        """Save the user to the db."""
        db.session.add(self)
        db.session.commit()
