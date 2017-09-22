from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))




    # this say that we have a relationship with itemmodel it goes to item Model
    #  and it check the store id in the item which means one item is related to a store
    # therefore there could be more than one item related to the same store
    # there could be one or two or ect items related to one store
    # therfore this items is a list of items in one store
    items = db.relationship('ItemModel', lazy ='dynamic')

    def __init__(self, name):
        self.name = name



    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        # cls instead of ItemModel because it is a class inside or for ItemModel
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name =name, first returns LIMIT 1


    # this function save directly to db both insert and update in the same function alchemy is easier
    # without using sqlite3 using instead SQLAlchemy
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
