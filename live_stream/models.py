from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy() # create an instance of a database connection
migrate = Migrate(db) # associate migration functions to it

# This ORM has the migration and the model together


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, nullable=True)
    users = db.relationship('User', backref='rooms', lazy=True) 
    # users needs to be an object of users not just one user
    properties = db.relationship('Property', backref='rooms', lazy=True)

    def __init__(self, active, users):
        self.active = active
        self.users = users

    def to_dict(self):
        return {
            'id': self.id,
            'active': self.active,
            'users': self.users,
            'users': [user.to_dict() for user in self.users],
            'properties': [prop.to_dict() for prop in self.properties]
        }

    def __repr__(self):
        return f'<Room {self.id}>'
class User(db.Model):
    # This is the migration part
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    host = db.Column(db.Boolean, server_default='f', nullable=True)
    balance = db.Column(db.Integer, server_default='1500', nullable=False)
    # posts = db.relationship('Post', backref='user', lazy=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=True) #lazy true lets the db know when to access the related object, in this case only room will be accessed when it is accessed
    # properties = db.relationship('Property', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # This is regular old Python classes
    # Right here is where we "whitelist" what can be set when creating a user
    # any column omitted cannot be set by the user/app manually
    def __init__(self, username, email, password, fullname):
        self.username = username
        self.email = email
        self.password = password
        self.fullname = fullname

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'fullname' : self.fullname, 
            'room_id' : [room.to_dict() for room in self.rooms],
            'properties': [prop.to_dict() for prop in self.properties],
            'created_at': self.created_at
        }

    def __repr__(self):
        return '<User %r>' % self.username


class Property(db.Model): 
    __tablename__= 'properties'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False, unique=True)
    hotel = db.Column(db.Boolean, nullable=True)
    hotel_price = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __init__(self, price, name, hotel, hotel_price):
        self.price = price
        self.name = name
        self.hotel = hotel 
        self.hotel_price = hotel_price

    def to_dict(self):
        property_dict = {
            'id': self.id,
            'price': self.price,
            'name': self.name, 
            'hotel': self.hotel, 
            'hotel_price': self.hotel_price,  
            'user_id': [user.to_dict() for user in self.users]
        } 
        if self.rooms is not None:
            property_dict['room_id'] = [room.to_dict() for room in self.rooms]
        else:
            property_dict['room_id'] = []

        return property_dict
    
    def __repr__(self): 
        return f'<Property {self.id}>'


# class Post(db.Model):
#     __tablename__ = 'posts'
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text, nullable=False)
#     status = db.Column(db.String, nullable=True, server_default='published')
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

#     def __init__(self, content):
#         self.content = content

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'content': self.content,
#             'created_at': self.created_at,
#             'updated_at': self.updated_at,
#             'room_id':seld.room_id,
#             'user_id': self.user_id
#         }

#     def __repr__(self):
#         return f'<Post {self.id}>'