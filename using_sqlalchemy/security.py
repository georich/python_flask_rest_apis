"""Contains functions for JWT authentication."""
from models.user import UserModel


def authenticate(username, password):
    """Find user and check if password matches."""
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    """Match user payload with entry in User 'database'."""
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
