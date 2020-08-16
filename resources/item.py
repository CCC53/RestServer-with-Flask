from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field is required")
    parser.add_argument('store_id', type=int, required=True, help="This field is required")

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if item:
                return item.toJSON()
            return {'message': 'Item not found'}, 404
        except:
            return {'message': 'Internal Server Error'}

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with {name} already exists'}, 400
        body = Item.parser.parse_args()
        item = ItemModel(name, **body)
        try:
            item.save_item()
        except:
            return {'message': 'Internal Server Error'}, 500
        return item.toJSON()
    
    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_item()
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        body = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        item_updated = ItemModel(name, **body)
        if item is None:
            item = item.save_item()
        else:
            item.price = body['price']
        item.save_item()
        return item.toJSON()

class Items(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.toJSON() for item in ItemModel.query.all()]}