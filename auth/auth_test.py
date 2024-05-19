from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
#import logging


app = Flask(__name__)

# Configure database URI
DB_USER = os.getenv("DB_USER", "ucstudent")
DB_PASSWORD = os.getenv("DB_PASSWORD", "DATA472JARRDmads")
DB_HOST = os.getenv("DB_HOST", "data472-rna104-jarrd-db.cyi9p9kw8doa.ap-southeast-2.rds.amazonaws.com")
DB_NAME = os.getenv("DB_NAME", "jarrd_db")
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

@app.before_request
def create_tables():
    # The following line will remove this handler, making it
    # only run on the first request
    app.before_request_funcs[None].remove(create_tables)

    db.create_all()

#Register API
@app.route('/register', methods=['POST'])
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


#______________This is working registration code____________________________________________________
from flask import Flask, request
from werkzeug.security import generate_password_hash
import mysql.connector

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/register", methods=["POST"])
def register():
    # Get data from POST request
    name = request.form.get('name')
    login = request.form.get('login')
    email = request.form.get('email')
    password = request.form.get('password')

    if not login or not email or not password:
        return "Missing information", 400

    # Hash the password for security
    hashed_password = generate_password_hash(password)

    # Save to a file
    with open("users.txt", "a") as file:
        file.write(f"{login},{email},{hashed_password}\n")

    try:
        # Configure database connection
        db_connection = mysql.connector.connect(
            host="data472-rna104-jarrd-db.cyi9p9kw8doa.ap-southeast-2.rds.amazonaws.com",
            user="ucstudent",
            password="DATA472JARRDmads",
            database="jarrd_db"
            )

        # Create cursor
        cursor = db_connection.cursor()

        # Insert user data into the database
        sql = "INSERT INTO users (name, login, pass, email) VALUES (%s, %s, %s, %s)"
        val = (name, login, hashed_password, email)
        cursor.execute(sql, val)
        db_connection.commit()

        # Close cursor and database connection
        cursor.close()
        db_connection.close()

        return "User registered successfully!"

    except mysql.connector.Error as err:
        return f"Error: {err}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


#______________________This is integration of the login_________________
from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'DATA472-JARRD-ifiretracker'  # Change this to a random secret key

@app.route("/register", methods=["POST"])
def register():
    # Get data from POST request
    name = request.form.get('name')
    login = request.form.get('login')
    email = request.form.get('email')
    password = request.form.get('password')

    if not login or not email or not password:
        return "Missing information", 400

    # Hash the password for security
    hashed_password = generate_password_hash(password)

    # Save to a file
    with open("users.txt", "a") as file:
        file.write(f"{login},{email},{hashed_password}\n")

    try:
        # Configure database connection
        db_connection = mysql.connector.connect(
            host="data472-rna104-jarrd-db.cyi9p9kw8doa.ap-southeast-2.rds.amazonaws.com",
            user="ucstudent",
            password="DATA472JARRDmads",
            database="jarrd_db"
        )

        # Create cursor
        cursor = db_connection.cursor()

        # Insert user data into the database
        sql = "INSERT INTO users (name, login, pass, email) VALUES (%s, %s, %s, %s)"
        val = (name, login, hashed_password, email)
        cursor.execute(sql, val)
        db_connection.commit()

        # Close cursor and database connection
        cursor.close()
        db_connection.close()

        return "User registered successfully!"

    except mysql.connector.Error as err:
        return f"Error: {err}", 500

@app.route("/login", methods=["POST"])
def login():
    # Get data from POST request
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return "Missing login or password", 400

    try:
        # Configure database connection
        db_connection = mysql.connector.connect(
            host="data472-rna104-jarrd-db.cyi9p9kw8doa.ap-southeast-2.rds.amazonaws.com",
            user="ucstudent",
            password="DATA472JARRDmads",
            database="jarrd_db"
        )

        # Create cursor
        cursor = db_connection.cursor()

        # Query user data from the database
        sql = "SELECT login, pass FROM users WHERE login = %s"
        cursor.execute(sql, (login,))
        user = cursor.fetchone()

        # Close cursor and database connection
        cursor.close()
        db_connection.close()

        if user and check_password_hash(user[1], password):
            # Set session
            session['user'] = login
            return "Login successful!"
        else:
            return "Invalid login or password", 401

    except mysql.connector.Error as err:
        return f"Error: {err}", 500

@app.route("/logout")
def logout():
    session.pop('user', None)
    return "Logged out successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)