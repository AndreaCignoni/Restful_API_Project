# VinyRecordCollectorAPI.py

# This Python program implements a RESTful API for vinyl record collectors. The API allows users to store, manage, receive offers and interact with other collectors.

# Users can register, log in, and perform CRUD (Create, Read, Update, Delete) operations on their records.

# The purpose of this API is to provide a centralized platform for all collectors can organize their inventory and share receive offers through its user-friendly interface and robust functionalities.

# This API is implemented using Flask, a lightweight and flexible web framework for Python providing the necessary tools and libraries to build web applications and APIs quickly and efficiently. 

# The API endpoints are designed following RESTful principles, with each endpoint corresponding to a specific resource and operation. 

# Author: Andrea Cignoni
import json
from flask import Flask, request, jsonify, make_response
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from configDB import DATABASE_CONFIG
import time

app = Flask(__name__)

# Postgre VynilRecordCollectorAPI database connection
while True:
    try:
        # Establish the database connection using the configuration
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connect to database failed!")
        print("Error: ", error)
        time.sleep(2)


# Users database:
users = []

# Define Pydantic model for user registration
class UserRegistration(BaseModel):
    fname: str
    lname: str
    gender: str
    nationality: str
    email: str
    username: str
    password: str
    
# Define Pydantic model for updating user profile
class UserUpdate(BaseModel):
    fname: Optional[str]
    lname: Optional[str]
    gender: Optional[str]
    nationality: Optional[str]
    email: Optional[str]
    username: Optional[str]
    password: Optional[str]
    
# Records database:
records = []

class Offer(BaseModel):
    offer: str

class Comment(BaseModel):
    comment: str

class RecordForm(BaseModel):
    title: str
    author: str
    label: str
    year: int  
    condition: str
    cost: int 
    year_of_purchase: int
    offers: Optional[List[int]] = []
    comments: Optional[List[str]] = []
    username: str # This should match a username in the users table
    
class RecordUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    label: Optional[str]
    year: Optional[int]
    condition: Optional[str]
    cost: Optional[int]
    year_of_purchase: Optional[int]
    offers: Optional[int]  
    comment: Optional[Comment]
    username: str # This should match a username in the users table


# Endpoint to provide basic information about the API
@app.route('/')
def index():
    return """
    <h1>Welcome to the Vinyl Record Collector API!</h1>
    <p>Database Connection: Successful</p>
    <h2>API Endpoints:</h2>
    <ul>
        <li>/users : Manage user registration and profile updates</li>
        <li>/records : Manage records, including adding, updating, and retrieving records</li>
        <li>/offers : Manage offers for records</li>
        <li>/comments : Manage comments on records</li>
    </ul>
    <p>Are you registered yet? </p>
    <ul>
        <li><a href="/registration_form">Register</a></li> <!-- Link to the registration form -->
    <p>Otherwise: </p>
        <li><a href="/login">Login</a></li> <!-- Link to the login page -->
    </ul>
    """
# Endpoint for user CREATION
@app.route('/registration_form', methods=['POST'])
def register():
    try:
        # Validate incoming JSON data using Pydantic model
        registration_data = UserRegistration(**request.json)

        # Execute SQL query to insert user data into the database
        cursor.execute("""
            INSERT INTO users (fname, lname, gender, nationality, email, username, password) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            registration_data.fname,
            registration_data.lname,
            registration_data.gender,
            registration_data.nationality,
            registration_data.email,
            registration_data.username,
            registration_data.password
        ))
        
        # Commit the transaction
        conn.commit()

        return "User registered successfully"
    except Exception as e:
        # Handle database and validation errors
        return f"Registration error: {str(e)}", 400

# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        # Execute SQL query to retrieve user with the provided username
        cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            user_id, hashed_password = user['id'], user['password']
            # Verify password
            if hashed_password == password:
                return jsonify({"message": "Login successful", "user_id": user_id}), 200
            else:
                return jsonify({"error": "Incorrect password"}), 401
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        # Handle database errors
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    
# Endpoint to browse all users
@app.route('/users', methods=['GET'])
def browse():
    try:
        cursor.execute("""SELECT * FROM users""")
        users = cursor.fetchall()
        return jsonify(users), 200
    except Exception as e:
        # If an error occurs during database query execution, return a 500 Internal Server Error response
        return f"An error occurred: {str(e)}", 500
    
# Route to search for user by ID
@app.route('/users/<int:id>', methods=['GET'])
def search_id(id):
    # Execute SQL query to fetch user from database
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()

    # Check if user is found in the database
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404
    
# Route to search for user by username
@app.route('/users/<username>', methods=['GET'])
def search_username(username):
    # Execute SQL query to fetch user from database
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

    # Check if user is found in the database
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

# To UPDATE a user's details
@app.route('/users/<username>', methods=['PUT'])
def update_user(username):
    try:
        data = request.json
        cursor.execute("""
        UPDATE users
        SET fname = %s, lname = %s, gender = %s, nationality = %s, email = %s, username = %s, password = %s
        WHERE username = %s
        """, (
            data.get('fname'),
            data.get('lname'),
            data.get('gender'),
            data.get('nationality'),
            data.get('email'),
            data.get('username'),
            data.get('password'),
            username
        ))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "User profile updated successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

#Route to DELETE a user profile   
@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    try:
        # Attempt to delete the user
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE username = %s", (username,))
            if cursor.rowcount > 0:
                return jsonify({"message": "User deleted successfully"}), 200
            else:
                return jsonify({"error": "User not found"}), 404
    except psycopg2.errors.ForeignKeyViolation as e:
        # Handle foreign key violation error
        return jsonify({"error": "User cannot be deleted until all listings are deleted"}), 409
    
# Endpoint to browse all records
@app.route('/records', methods=['GET'])
def browse_records():
    try:
        cursor.execute("""SELECT * FROM records""")
        users = cursor.fetchall()
        return jsonify(users), 200
    except Exception as e:
        # If an error occurs during database query execution, return a 500 Internal Server Error response
        return f"An error occurred: {str(e)}", 500

# Endpoint to create a new record
@app.route('/records/new', methods=['POST'])
def create_record():
    try:
        # Get JSON data from the request
        data = request.json
        # Validate incoming JSON data using Pydantic model
        registered_record = RecordForm(**data)

        # Execute SQL query to insert user data into the database
        cursor.execute("""
            INSERT INTO records (title, author, label, year, condition, cost, year_of_purchase, offers, comments, username) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            registered_record.title,
            registered_record.author,
            registered_record.label,
            registered_record.year,
            registered_record.condition,
            registered_record.cost,
            registered_record.year_of_purchase,
            registered_record.offers,
            registered_record.comments,
            registered_record.username
        ))

        # Commit the transaction
        conn.commit()

        return "Record registered successfully"
    except Exception as e:
        # Rollback the transaction in case of an error
        conn.rollback()
        return f"Validation error: {str(e)}", 400

# Endpoint to search records by title
@app.route('/records/<title>', methods=['GET'])
def search_record(title):
    # Execute SQL query to fetch records with the same title from database
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM records WHERE title = %s", (title,))
        records = cursor.fetchall()

    # Check if any records are found in the database
    if records:
        # If records are found, return them as JSON response
        return jsonify(records), 200
    else:
        # If no records are found, return error message
        return jsonify({"error": "Record not found"}), 404
    
# Endpoint to search records by ID
@app.route('/records/<int:record_id>', methods=['GET'])
def search_recordID(record_id):
    # Execute SQL query to fetch records with the same title from database
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM records WHERE record_id = %s", (record_id,))
        records = cursor.fetchall()

    # Check if any records are found in the database
    if records:
        # If records are found, return them as JSON response
        return jsonify(records), 200
    else:
        # If no records are found, return error message
        return jsonify({"error": "Record not found"}), 404
    
# Endpoint to update a record's detail
@app.route('/records/<title>', methods=['PUT'])
def update_record(title):
    try:
        data = request.json
        cursor.execute("""
        UPDATE records
        SET title = %s, author = %s, label = %s, year = %s, condition = %s, cost = %s, year_of_purchase = %s, comments =%s
        WHERE title = %s
        """, (
            data.get('title'),
            data.get('author'),
            data.get('label'),
            data.get('year'),
            data.get('condition'),
            data.get('cost'),
            data.get('year_of_purchase'),
            data.get('comments'),
            title
        ))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Record form updated successfully"}), 200
        else:
            return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Endpoint to DELETE a uregistered record
@app.route('/records/<title>', methods=['DELETE'])
def delete_record(title):
    try:
        # Attempt to delete a record
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM records WHERE title = %s", (title,))
            if cursor.rowcount > 0:
                return jsonify({"message": "Record deleted successfully"}), 200
            else:
                return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)