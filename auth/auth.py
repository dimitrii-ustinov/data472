from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure database URI
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "your-rds-endpoint")
DB_NAME = os.getenv("DB_NAME", "yourdbname")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Use hashing in real scenarios

    def __repr__(self):
        return '<User %r>' % self.username

@app.before_first_request
def create_tables():
    db.create_all()

# Register API
@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']  # In real applications, hash the password!
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# Login API
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'message': 'Bad username or password'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
