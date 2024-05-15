from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
#import logging


app = Flask(__name__)

# Configure database URI
DB_USER = os.getenv("DB_USER", "ucstudent")
DB_PASSWORD = os.getenv("DB_PASSWORD", "DATA472JARRDmads")
DB_HOST = os.getenv("DB_HOST", "data472-rna104-jarrd-db.cyi9p9kw8doa.ap-southeast-2.rds.amazonaws.com")
DB_NAME = os.getenv("DB_NAME", " data472-rna104-jarrd-db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)   #Hash it later
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.before_first_request
def create_tables():
    db.create_all()

#Register API
@app.route('/register', methods=['POST', 'GET'])
def register():
    name = request.json['name']
    login = request.json['login']
    password = request.json['password']  # In real applications, hash the password!
    email = request.json['email']
    
    if User.query.filter_by(login=login).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(name=name, login=login, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# Login API
@app.route('/login', methods=['POST'])
def login():
    login = request.json['login']
    password = request.json['password']
    user = User.query.filter_by(login=login).first()
    if user and user.password == password:
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'message': 'Bad login or password'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
