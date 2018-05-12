"""Contains functions for JWT authentication."""
from user import User


def authenticate(username, password):
    """Find user and check if password matches."""
    user = User.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    """Match user payload with entry in User 'database'."""
    user_id = payload['identity']
    return User.find_by_id(user_id)
