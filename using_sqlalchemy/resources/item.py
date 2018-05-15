"""Set up of resources for app."""
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    """Resource for item endpoints."""

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        """GET /item route."""
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        """POST /item route."""
        if ItemModel.find_by_name(name):
            return {
                'message': f"An item with name '{name}' already exists."
            }, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {'message': 'An error occured inserting the item.'}, 500

        return item.json(), 201

    def delete(self, name):
        """DELETE /item route."""
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self, name):
        """PUT /item route."""
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            updated_item.insert()
        else:
            updated_item.update()
        return updated_item.json()


class ItemList(Resource):
    """Resource for items endpoint."""

    def get(self):
        """GET /items route."""
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append({
                'name': row[0],
                'price': row[1]
            })

        connection.close()

        return {'items': items}
