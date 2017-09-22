from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # this is to match the store id in order to retrieve it from database
    # it know that
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id= store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

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
