from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser() # put it here easier to use or update
    parser.add_argument('price',
       type=float,
       required=True,
       help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',
       type=int,
       required=True,
       help="Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message' : "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args() ##add just Item to parse from class Item

        item = ItemModel(name, **data) # same as  data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500 # Internal Server Eroor

        return item.json(), 201 ## http status code for created



    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data) # same as  data['price'], data['store_id'])
        else:
            item.ItemModel = data['price'], data['store_id']


        item.save_to_db()

        return item.json()



class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
       # we can do the same using lambda it is better when using different programming language in one app
       # better for team too
       # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
