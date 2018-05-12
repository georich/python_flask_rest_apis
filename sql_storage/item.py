"""Set up of resources for app."""
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    """Resource for item endpoints."""

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank!")

    @classmethod
    def find_by_name(cls, name):
        """Find User by name in database and return, if not return none."""
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @jwt_required()
    def get(self, name):
        """GET /item route."""
        item = Item.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    def post(self, name):
        """POST /item route."""
        if Item.find_by_name(name):
            return {
                'message': f"An item with name '{name}' already exists."
            }, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

        return item, 201

    def delete(self, name):
        """DELETE /item route."""
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        """PUT /item route."""
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    """Resource for items endpoint."""

    def get(self):
        """GET /items route."""
        return {'items': items}
