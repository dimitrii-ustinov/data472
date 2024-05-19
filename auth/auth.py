from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'DATA472-JARRD-ifiretracker'

@app.route("/")
def hello_world():
    return "Test"

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
