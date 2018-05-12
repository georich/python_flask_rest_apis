"""Flask app for simple store of items."""
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = '123abc'  # Only visible because learning
api = Api(app)

jwt = JWT(app, authenticate, identity)  # creates /auth

items = []


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
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        """POST /item route."""
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {
                'message': f"An item with name '{name}' already exists."
            }, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
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


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
