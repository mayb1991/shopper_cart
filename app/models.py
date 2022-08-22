from secrets import token_hex
from app import db, login
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    phone = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    user_cart = db.relationship('Cart', backref='user_br', lazy=True)
    apitoken = db.Column(db.String, default=None, nullable=True)

    
    def __init__(self, first_name, last_name, username, phone, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.phone = phone
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'token': self.apitoken
        }


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    price = db.Column(db.String(150))
    category = db.Column(db.String(150))
    description = db.Column(db.String(300))
    image_url = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cart_items = db.relationship('Cart', backref='product_br', lazy=True)
    

    def __init__(self, name, price, category, description, image_url):
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.image_url = image_url


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id


