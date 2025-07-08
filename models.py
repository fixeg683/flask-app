from datetime import datetime, timedelta
from enum import Enum
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

class CategoryType(Enum):
    MOVIE = "movie"
    SOFTWARE = "software"
    GAME = "game"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_confirmed = db.Column(db.Boolean, default=False)
    confirmation_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self):
        self.confirmation_token = secrets.token_urlsafe(32)
        return self.confirmation_token

    def generate_reset_token(self):
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=24)
        return self.reset_token

    def is_reset_token_valid(self):
        if self.reset_token_expiry and self.reset_token_expiry > datetime.utcnow():
            return True
        return False

    def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.Enum(CategoryType), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    platform = db.Column(db.String(100), nullable=True)  # For games and software
    director = db.Column(db.String(100), nullable=True)  # For movies
    developer = db.Column(db.String(100), nullable=True)  # For games and software
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'category': self.category.value,
            'image_url': self.image_url,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'rating': self.rating,
            'genre': self.genre,
            'platform': self.platform,
            'director': self.director,
            'developer': self.developer
        }

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product', backref='cart_items')
    
    def __repr__(self):
        return f'<CartItem {self.product.title} x{self.quantity}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    session_id = db.Column(db.String(255), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    paypal_order_id = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Order {self.order_number}>'

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    order = db.relationship('Order', backref='items')
    product = db.relationship('Product', backref='order_items')
    
    def __repr__(self):
        return f'<OrderItem {self.product.title} x{self.quantity}>'
