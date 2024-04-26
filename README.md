# VinyRecordCollectorAPI

## Introduction

This repository contains a Python program that implements a RESTful API for vinyl record collectors. The API allows users to store, manage, receive offers, and interact with other collectors.

Users can register, log in, and perform CRUD (Create, Read, Update, Delete) operations on their records.

The purpose of this API is to provide a centralized platform for all collectors to organize their inventory and share/receive offers through its user-friendly interface and robust functionalities.

This API is implemented using Flask, a lightweight and flexible web framework for Python providing the necessary tools and libraries to build web applications and APIs quickly and efficiently. The API endpoints are designed following RESTful principles, with each endpoint corresponding to a specific resource and operation.

## Repository Structure

The repository structure is as follows:

+ app/: Contains the main files for the API.
- main.py: Contains the implementation of the API endpoints.
- init.py: Initializes the Flask application.

+ templates/: Contains HTML templates with embedded JavaScript for rendering API responses and handling user interactions.
- welcomePage.html
- registrationForm.html
- login.html
- users.html
- userUpdate.html
- userDelete.html
- allRecords.html
- recordProfile.html
- recordUpdate.html
- recordDelete.html

ajaxcalls.js

## Getting Started

To run the API locally, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone <repository-url>

2. Navigate to the project directory:

    cd VinyRecordCollectorAPI

3. Install the required dependencies:

    pip install -r requirements.txt

4. Run the Flask application:

    python app/main.py

5. Access the API endpoints using a web browser or API testing tool.

## API Endpoints

The API provides the following endpoints:

- `GET /`: Endpoint to provide basic information about the API.
- `GET /registration_form`: Endpoint for user registration.
- `POST /registration_form`: Endpoint to handle user registration form submission.
- `GET /login`: Endpoint for user login.
- `POST /login`: Endpoint to handle user login form submission.
- `GET /users`: Endpoint to browse all users.
- `GET /users/<int:id>/profile`: Route to search for a user by ID.
- `GET /users/<username>/profile`: Route to search for a user by username.
- `GET /users/<int:id>/profile/update`: Endpoint to view and update a user's profile.
- `PUT /users/<int:id>/profile/update`: Endpoint to update a user's profile.
- `GET /users/<int:id>/profile/delete`: Endpoint to view and delete a user's profile.
- `DELETE /users/<int:id>/profile/delete`: Endpoint to delete a user's profile.
- `GET /records`: Endpoint to browse all records.
- `GET /records/new`: Endpoint to view the record creation form.
- `POST /records/new`: Endpoint to create a new record.
- `GET /records/<title>`: Endpoint to search records by title.
- `GET /records/<int:id>/update`: Endpoint to view and update a record's details.
- `PUT /records/<int:id>/update`: Endpoint to update a record's details.
- `DELETE /records/<title>/delete`: Endpoint to delete a record by title.

This API is authored by Andrea Cignoni.