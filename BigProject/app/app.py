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
import random
from random import randrange

app = Flask(__name__)

# Users database:
users = []

# Define Pydantic model for user registration
class UserRegistration(BaseModel):
    id: Optional[int]
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
    record_id: Optional[int]
    title: str
    author: str
    label: str
    year: int  
    condition: str
    cost: int 
    year_of_purchase: int
    offers: Optional[List[str]] = []
    comments: Optional[List[str]] = []
    user_id: int
    
class RecordUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    label: Optional[str]
    year: Optional[int]
    condition: Optional[str]
    cost: Optional[int]
    year_of_purchase: Optional[int]
    offer: Optional[Offer]  # Change to type Offer
    comment: Optional[Comment]  # Change to type Comment
    user_id: int

# Define a list to store user data
users = [
    {
        "id": 123,
        "fname": "John",
        "lname": "Doe",
        "gender": "Male",
        "nationality": "US",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "password": "securepassword"
    },
    {
        "id": 456,
        "fname": "Jane",
        "lname": "Smith",
        "gender": "Female",
        "nationality": "UK",
        "email": "jane.smith@example.com",
        "username": "janesmith",
        "password": "anothersecurepassword"
    }
]

# Endpoint to provide basic information about the API
@app.route('/')
def index():
    return """
    <h1>Welcome to the Vinyl Collector API</h1>
    <p>Are you registered yet? </p>
    <ul>
        <li><a href="/registration_form">Register</a></li>
    <p>Otherwise: </p>
        <li><a href="/login">Login</a></li>
    </ul>
    """

# Endpoint for user registration
@app.route('/registration_form', methods=['POST'])
def register():
    data = request.json
    try:
        # Validate incoming JSON data using Pydantic model
        registration_data = UserRegistration(**data)
        print(registration_data.dict())
        
        # Generate a random user ID
        new_user_id = random.randrange(1, 10000000)
        
        # Create a dictionary representing the user
        new_user = {
            'id': new_user_id,
            'fname': registration_data.fname,
            'lname': registration_data.lname,
            'gender': registration_data.gender,
            'nationality': registration_data.nationality,
            'email': registration_data.email,
            'username': registration_data.username,
            'password': registration_data.password
        }
        
        # Add the new user to the users list
        users.append(new_user)

        return "User registered successfully"
    except Exception as e:
        return f"Validation error: {str(e)}", 400
    
    
# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Search for the user in the users list by username
    user = next((user for user in users if user['username'] == username), None)

    if user:
        # Check if the password matches
        if user['password'] == password:
            return jsonify({"message": "Login successful", "user_id": user['id']}), 200
        else:
            return jsonify({"error": "Incorrect password"}), 401
    else:
        return jsonify({"error": "User not found"}), 404
    
# Endpoint to browse users
@app.route('/users', methods=['GET'])
def browse():
    data = request.json
    return jsonify(users), 200
        
# Endpoint to search specific users by ID
@app.route('/users/id/<int:user_id>', methods=['GET'])
def search_by_id(user_id):
    # Logic to search for the user profile based on the user ID
    user_profile = next((user for user in users if user['id'] == user_id), None)
    
    if user_profile:
        return jsonify(user_profile), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Endpoint to search specific users by username
@app.route('/users/username/<username>', methods=['GET'])
def search_by_username(username):
    user_profile = next((user for user in users if user['username'] == username), None)
    
    if user_profile:
        return jsonify(user_profile), 200
    else:
        return jsonify({"error": "User not found"}), 404
        
# Endpoint to update a user profile
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user_profile = next((user for user in users if user['id'] == user_id), None)
    if user_profile:
        user_update_data = UserUpdate(**data)
        user_profile.update(user_update_data.dict())
        return jsonify({"message": "User profile updated successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404
    
# Endpoint to delete a user profile
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user['id'] != user_id]
    return jsonify({"message": "User deleted successfully"})

# Endpoint to create a new record
@app.route('/records/new', methods=['POST'])
def create_record():
    data = request.json
    try:
        # Validate incoming JSON data using Pydantic model
        registered_record = RecordForm(**data)
        print(registered_record.dict())
        
        # Generate a random record ID
        new_record_id = random.randint(1, 10000000)
        
        # Create a dictionary representing a record
        new_record = {
            'record_id': new_record_id,
            'title': registered_record.title,
            'author': registered_record.author,
            'label': registered_record.label,
            'year': registered_record.year,
            'condition': registered_record.condition,
            'cost': registered_record.cost,
            'year_of_purchase': registered_record.year_of_purchase,
            'offers': registered_record.offers,
            'comments': registered_record.comments,
            'user_id': registered_record.user_id  # Set user_id
        }
        
        # Add the new record to the records list
        records.append(new_record)
        return "Record registered successfully"
    except Exception as e:
        return f"Validation error: {str(e)}", 400
        
# Endpoint to browse records
@app.route('/records', methods=['GET'])
def browse_records():
    data = request.json
    return jsonify(records), 200
        
# Endpoint to search a record by title
@app.route('/records/<title>', methods=['GET'])
def record_search_by_title(title):
    record = next((record for record in records if record['title'] == title), None)
    if record:
        return jsonify({"message": f"Here are the results for {title}", "record": record}), 200
    else:
        return jsonify({"error": "Record not found"}), 404
        
# Endpoint to search a record by ID
@app.route('/records/<int:record_id>', methods=['GET'])
def record_search_by_id(record_id):
    record = next((record for record in records if record['record_id'] == record_id), None)
    if record:
        return jsonify({"message": f"Here are the results for {record_id}", "record": record}), 200
    else:
        return jsonify({"error": "Record not found"}), 404
        
# Endpoint to update a record's detail
@app.route('/records/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    data = request.json
    record = next((record for record in records if record['record_id'] == record_id), None)
    if record:
        # Update the record details
        record_update_data = RecordUpdate(**data)
        record.update(record_update_data.dict())
        
        # Update offer if provided in the request data
        if 'offer' in data:
            record['offer'] = data['offer']
        
        # Update comments if provided in the request data
        if 'comments' in data:
            record['comments'] = data['comments']
        
        return jsonify({"message": "Record updated successfully", "record": record}), 200
    else:
        return jsonify({"error": "Record not found"}), 404

# Endpoint to delete a vinyl record by ID
@app.route('/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    global records
    records = [record for record in records if record['record_id'] != record_id]
    return jsonify({"message": "Record deleted successfully"})
    
# Endpoint to create a new offer for a record
@app.route('/records/<int:record_id>/offers', methods=['POST'])
def create_offer(record_id):
    data = request.json
    try:
        # Validate incoming JSON data using Pydantic model
        offer_data = Offer(**data)
        
        # Find the record
        record = next((record for record in records if record['record_id'] == record_id), None)
        if record:
            # Update the offer field of the record
            record['offer'] = offer_data.offer
            
            return jsonify({"message": "Offer created successfully", "record": record}), 200
        else:
            return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        return f"Validation error: {str(e)}", 400

# Endpoint to add a comment to a record
@app.route('/records/<int:record_id>/comments', methods=['POST'])
def add_comment(record_id):
    data = request.json
    try:
        # Validate incoming JSON data using Pydantic model
        comment_data = Comment(**data)
        
        # Find the record
        record = next((record for record in records if record['record_id'] == record_id), None)
        if record:
            # Add the comment to the record
            if 'comments' in record:
                record['comments'].append(comment_data.comment)
            else:
                record['comments'] = [comment_data.comment]
            
            return jsonify({"message": "Comment added successfully", "record": record}), 200
        else:
            return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        return f"Validation error: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)

''''''''''
-- Create a table for users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(255) NOT NULL,
    lname VARCHAR(255) NOT NULL,
    gender VARCHAR(10),
    nationality VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create a table for records
CREATE TABLE records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    label VARCHAR(255),
    year INT,
    condition VARCHAR(50),
    cost INT,
    year_of_purchase INT,
    user_id INT, -- New field to store the user ID who posted the record
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create a table for offers
CREATE TABLE offers (
    offer_id INT AUTO_INCREMENT PRIMARY KEY,
    offer VARCHAR(255) NOT NULL,
    record_id INT,
    user_id INT,
    FOREIGN KEY (record_id) REFERENCES records(record_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create a table for comments
CREATE TABLE comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    comment VARCHAR(255) NOT NULL,
    record_id INT,
    user_id INT,
    FOREIGN KEY (record_id) REFERENCES records(record_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
'''''
