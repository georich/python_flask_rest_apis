"""Set up of resources for app."""
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.item import ItemModel


class Item(Resource):
    """Resource for item endpoints."""

    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="This field cannot be left blank!",
    )

    parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help="Every item needs a store id.",
    )

    @jwt_required
    def get(self, name):
        """GET /item route."""
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        """POST /item route."""
        if ItemModel.find_by_name(name):
            return (
                {"message": f"An item with name '{name}' already exists."},
                400,
            )

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except Exception as e:
            return {"message": "An error occured inserting the item."}, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        """DELETE /item route."""
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": "Admin privilege required"}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted"}
        return {"message": "Item not found"}, 404

    def put(self, name):
        """PUT /item route."""
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    """Resource for items endpoint."""

    def get(self):
        """GET /items route."""
        return {"items": [item.json() for item in ItemModel.find_all()]}
