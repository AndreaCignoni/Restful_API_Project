# VinyRecordCollectorAPI.py

# This Python program implements a RESTful API for vinyl record collectors. The API allows users to store, manage, receive offers and interact with other collectors.

# Users can register, log in, and perform CRUD (Create, Read, Update, Delete) operations on their records.

# The purpose of this API is to provide a centralized platform for all collectors can organize their inventory and share receive offers through its user-friendly interface and robust functionalities.

# This API is implemented using Flask, a lightweight and flexible web framework for Python providing the necessary tools and libraries to build web applications and APIs quickly and efficiently. 

# The API endpoints are designed following RESTful principles, with each endpoint corresponding to a specific resource and operation. 

# Author: Andrea Cignoni

import json
from flask import Flask, request, jsonify, make_response, render_template, abort
from flask_cors import CORS
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from configDB  import DATABASE_CONFIG
import time

app = Flask(__name__, template_folder='templates')

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
    offers: str
    comments: int
    username: str
    
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
    username: str


# Endpoint to provide basic information about the API
@app.route('/')
def index():
    return render_template ('welcomePage.html')
# Endpoint for user CREATION
@app.route('/registration_form', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
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
    else:
        return render_template('registrationForm.html')

# Endpoint for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
    else:
        return render_template('login.html')

    
# Endpoint to browse all users
@app.route('/users', methods=['GET'])
def browse():
    try:
        cursor.execute("""SELECT * FROM users""")
        users = cursor.fetchall()
        return render_template('users.html', users=users), 200
    except Exception as e:
        # If an error occurs during database query execution, return a 500 Internal Server Error response
        return f"An error occurred: {str(e)}", 500

# Route to search for user by ID
@app.route('/users/<int:id>/profile', methods=['GET'])
def search_id(id):
    try:
        # Execute SQL query to fetch user from database using parameterized query
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
            user = cursor.fetchone()

        # Check if user is found in the database
        if user:
            return render_template('userProfile.html', user=user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# Route to search for user by username
@app.route('/users/<username>/profile', methods=['GET'])
def search_username(username):
    try:
        # Execute SQL query to fetch user from database using parameterized query
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

        # Check if user is found in the database
        if user:
            return render_template('userProfile.html', user=user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Endpoint to update a user
@app.route('/users/<int:id>/profile/update', methods=['PUT'])
def update_user(id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
            user = cursor.fetchone()
            if not user:
                return jsonify({'error': 'User not found'}), 404

        fname = request.form.get('fname')
        lname = request.form.get('lname')
        gender = request.form.get('gender')
        nationality = request.form.get('nationality')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET fname = %s, lname = %s, gender = %s, nationality = %s, email = %s, username = %s, password = %s WHERE id = %s",
                (fname, lname, gender, nationality, email, username, password, id)
            )
            conn.commit()

        return render_template('userUpdate.html')

    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# Route to delete a user profile
@app.route('/users/<int:id>/profile/delete', methods=['GET', 'DELETE'])
def delete_user(id):
    try:
        if request.method == 'GET':
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
                user = cursor.fetchone()
                if user:
                    return render_template('userDelete.html', user=user), 200
                else:
                    return render_template('userDelete.html', error='User not found'), 404
        elif request.method == 'DELETE':
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (id,))
                conn.commit()

            if cursor.rowcount > 0:
                return jsonify({'message': 'User deleted successfully'}), 200
            else:
                return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500
    
# Endpoint to browse all records
@app.route('/records', methods=['GET'])
def browse_records():
    try:
        cursor.execute("""SELECT * FROM records""")
        records = cursor.fetchall()
        return render_template('allRecords.html', records=records)
    except Exception as e:
        # If an error occurs during database query execution, return a 500 Internal Server Error response
        return f"An error occurred: {str(e)}", 500

# Endpoint to create a new record
@app.route('/records/new', methods=['GET','POST'])
def create_record():
    if request.method == 'POST':
        try:
            # Get JSON data from the request
            registered_record = RecordForm(**request.json)

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
            # Handle database and validation errors
            return f"Registration error: {str(e)}", 400
    else:
        return render_template('newRecord.html')

# Endpoint to search records by title
@app.route('/records/<title>', methods=['GET'])
def search_record(title):
    # Execute SQL query to fetch records with the same title from the database
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM records WHERE title = %s", (title,))
        record = cursor.fetchone()  # Assuming there's only one record with the given title

    # Check if any record is found in the database
    if record:
        # If a record is found, render the recordProfile.html template with the record data
        return render_template('recordProfile.html', record=record)
    else:
        # If no record is found, return error message
        return jsonify({"error": "Record not found"}), 404
    
# Endpoint to search records by ID
@app.route('/records/<int:record_id>', methods=['GET'])
def search_recordID(record_id):
    # Execute SQL query to fetch the record with the given record_id from the database
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM records WHERE record_id = %s", (record_id,))
        record = cursor.fetchone()

    # Check if any record is found in the database
    if record:
        # If a record is found, render the recordProfile.html template with the record data
        return render_template('recordProfile.html', record=record)
    else:
        # If no record is found, return error message
        return jsonify({"error": "Record not found"}), 404
    
# Endpoint to update a record's details
@app.route('/records/<int:record_id>/update', methods=['PUT'])
def update_record(record_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM records WHERE record_id = %s", (record_id,))
            record = cursor.fetchone()
            if not record:
                return jsonify({'error': 'User not found'}), 404
            
        title = request.form.get('title')
        author = request.form.get('author')
        label = request.form.get('label')
        year = request.form.get('year')
        condition = request.form.get('condition')
        cost = request.form.get('cost')
        year_of_purchase = request.form.get('year_of_purchase')
        comments = request.form.get('comments')

        with conn.cursor() as cursor:
            cursor.execute("""
            UPDATE records
            SET title = %s, author = %s, label = %s, year = %s, condition = %s, cost = %s, year_of_purchase = %s, comments = %sa
            WHERE record_id = %s            
            """, (title, author, label, year, condition, cost, year_of_purchase, comments, record_id)
            )
            conn.commit()

        return render_template('recordUpdate.html')
    
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

# Endpoint to DELETE a registered record
@app.route('/records/<int:record_id>/delete', methods=['GET', 'DELETE'])
def delete_record(record_id):
    try:
        if request.method == 'GET':
            # Fetch user data and render userDelete.html template
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM records WHERE record_id = %s", (record_id,))
                record = cursor.fetchone()
                if record:
                    return render_template('recordDelete.html', record=record), 200
                else:
                    return render_template('recordDelete.html', error='Record not found'), 404
        elif request.method == 'DELETE':
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM records WHERE record_id = %s", (record_id,))
                conn.commit()
            if cursor.rowcount > 0:
                return jsonify({'message': 'Record deleted successfully'}), 200
            else:
                return jsonify({'error': 'Record not found'}), 404
    except Exception as e:
            return jsonify({'error': f"An error occurred: {str(e)}"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)