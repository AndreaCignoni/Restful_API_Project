# VinyRecordCollectorAPI.py

# This Python program implements a RESTful API for vinyl record collectors. The API allows users to store, manage, 
# and interact with details about their vinyl records.

# Users can register, log in, and perform CRUD (Create, Read, Update, Delete) operations on their records. Additionally, they can interact with other users, search for records, and view comments.

# The purpose of this API is to provide a centralized platform for vinyl collectors to organize and share information about their collections by offering a user-friendly interface 
# and robust functionality, the API aims to streamline the process of cataloging records, facilitating interactions between collectors.

# This API is implemented using Flask, a lightweight and flexible web framework for Python providing the necessary tools and libraries to build web applications and APIs quickly and efficiently. 

# The API endpoints are designed following RESTful principles, with each endpoint corresponding to a specific resource and operation. 

# Author: Andrea Cignoni


from flask import Flask, request, jsonify, make_response
import sqlite3
import json

app = Flask(__name__)

# Recorddatabase connection
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('records.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn

# Endpoint to provide basic information about the API
def index():
    return """
    <h1>Welcome to the Vinyl Collector API</h1>
    <p>Are you registered yet?</p>
    <ul>
        <li><a href="/register">Register</a></li>
        <li><a href="/login">Login</a></li>
    </ul>
    """

# Endpoint for registration
@app.route('/register')
def register():
    return "Registration Page"

# Endpoint for login
@app.route('/login')
def login():
    return "Login Page"

# Endpoint for user registration
@app.route('/register', methods=['POST'])
def register():
    # Extract registration data from the request JSON
    data = request.json
    fname = data.get('fname')
    lname = data.get('lname')
    gender = data.get('gender')
    nationality = data.get('nationality')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    # Check if all required fields are provided
    if not (fname and lname and gender and nationality and email and username and password):
        return jsonify({'error': 'All fields are required for registration'}), 400  # Bad request

    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the username is already taken
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        return jsonify({'error': 'Username is already taken'}), 409  # Conflict

    # Insert the new user into the database
    cursor.execute("""
        INSERT INTO users (fname, lname, gender, nationality, email, username, password_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (fname, lname, gender, nationality, email, username, password))

    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({'message': 'User registered successfully'}), 201  # Created

# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    # Extract login data from the request JSON
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Query the database to verify the username and password
    cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password))
    user = cursor.fetchone()

    conn.close()

    # Check if the user exists and the password is correct
    if user:
        return jsonify({'message': 'Login successful'}), 200  # OK
    else:
        return jsonify({'error': 'Invalid username or password'}), 401  # Unauthorized


# Endpoint to create a new record
def create_record():
    conn = db_connection()
    cursor = conn.cursor()

    # Extract data from the request body
    data = request.json
    title = data.get('title')
    author = data.get('author')
    label = data.get('label')
    year = data.get('year')
    condition = data.get('condition')
    cost = data.get('cost')
    year_of_purchase = data.get('year_of_purchase')
    user_id = data.get('user_id')  # Assuming user_id is provided in the request

    # Insert the new record into the database
    cursor.execute("""
        INSERT INTO records (user_id, title, author, label, year, condition, cost, year_of_purchase)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, title, author, label, year, condition, cost, year_of_purchase))

    conn.commit()

    # Get the ID of the newly inserted record
    new_record_id = cursor.lastrowid

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Return the ID of the newly created record as JSON response
    return jsonify({'record_id': new_record_id}), 201  # Return status code 201 (Created)

# Endpoint to get a specific vinyl record by ID
@app.route('/records/<int:record_id>', methods=['GET'])
def get_record(record_id):
    conn = db_connection()
    cursor = conn.cursor()
# Execute SQL query to select the record by ID
    cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,))
    record = cursor.fetchone()  # Fetch one record
    
    if record:
        # Convert the record to a dictionary for JSON response
        record_dict = {
            'id': record[0],
            'user_id': record[1],
            'title': record[2],
            'author': record[3],
            'label': record[4],
            'year': record[5],
            'condition': record[6],
            'cost': record[7],
            'year_of_purchase': record[8],
            'created_at': record[9]
        }
        return jsonify(record_dict), 200  # Return record as JSON response with status code 200
    else:
        return jsonify({'error': 'Record not found'}), 404  # Return error message with status code 404 if record not found

# Make sure to close the connection after the request is processed
    cursor.close()
    conn.close()

# Endpoint to update a specific vinyl record by ID
@app.route('/records/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    conn = db_connection()
    cursor = conn.cursor()

    # Extract updated data from the request body
    updated_data = request.json
    title = updated_data.get('title')
    author = updated_data.get('author')
    label = updated_data.get('label')
    year = updated_data.get('year')
    condition = updated_data.get('condition')
    cost = updated_data.get('cost')
    year_of_purchase = updated_data.get('year_of_purchase')
    user_id = updated_data.get('user_id')  # Assuming user_id can be updated

    # Update the record in the database
    cursor.execute("""
        UPDATE records
        SET title = ?, author = ?, label = ?, year = ?, condition = ?, cost = ?, year_of_purchase = ?, user_id = ?
        WHERE id = ?
    """, (title, author, label, year, condition, cost, year_of_purchase, user_id, record_id))

    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Return success message as JSON response
    return jsonify({'message': 'Record updated successfully'}), 200  # Return status code 200 (OK)

# Endpoint to delete a vinyl record by ID
@app.route('/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    conn = db_connection()
    cursor = conn.cursor()

    # Check if the record exists
    cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,))
    existing_record = cursor.fetchone()

    if existing_record:
        # Delete the record from the database
        cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return success message as JSON response
        return jsonify({'message': 'Record deleted successfully'}), 200  # Return status code 200 (OK)
    else:
        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return error message as JSON response
        return jsonify({'error': 'Record not found'}), 404  # Return status code 404 (Not Found)

if __name__ == '__main__':
    app.run(debug=True)