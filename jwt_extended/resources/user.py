"""Class file for User to help with crude database."""
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token

from models.user import UserModel


class UserRegister(Resource):
    """docstring for UserRegister."""

    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )

    def post(self):
        """Create a user from POST /register."""
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    """docstring for User."""

    @classmethod
    def get(cls, user_id):
        """Get the user defined User by id."""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        """Delete the user defined User by id."""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted"}, 200


class UserLogin(Resource):
    """docstring for UserLogin."""

    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )

    @classmethod
    def post(cls):
        """Get data from parser, find user in db, check password,
        create access token, create refresh token, return them."""
        data = cls.parser.parse_args()

        user = UserModel.find_by_username(data["username"])

        if user and (user.password == data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return (
                {"access_token": access_token, "refresh_token": refresh_token},
                200,
            )

        return {"message": "Invalid credentials"}, 401
