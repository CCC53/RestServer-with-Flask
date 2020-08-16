from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.toJSON()
            return {'1123': 123}
        return {'message': 'Store not found'}, 404
    
    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'A store with this name already exists'}, 400
        store = StoreModel(name)
        store.save_store()
        return store.toJSON()
    
    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if not store:
            return {'message': 'Store not found'}, 404
        else:
            store.delete_store()
            return {'message': 'Store Deleted'}

class Stores(Resource):
    @jwt_required()
    def get(self):
        return {'stores': [store.toJSON() for store in StoreModel.query.all()]}