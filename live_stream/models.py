from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy() # create an instance of a database connection
migrate = Migrate(db) # associate migration functions to it

# This ORM has the migration and the model together
class User(db.Model):
    # This is the migration part
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Boolean, server_default='f', nullable=True)
    posts = db.relationship('Post', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # This is regular old Python classes
    # Right here is where we "whitelist" what can be set when creating a user
    # any column omitted cannot be set by the user/app manually
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'posts': [post.to_dict() for post in Post.query.filter_by(user_id=self.id)],
            'created_at': self.created_at
        }

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, nullable=True, server_default='published')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, content):
        self.content = content

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'user_id': self.user_id
        }

    def __repr__(self):
        return f'<Post {self.id}>'