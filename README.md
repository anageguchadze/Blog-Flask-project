# Blog-Flask-project

A simple Flask-based blog application that allows users to register, log in, and manage blog posts. This project also integrates Swagger API documentation for easy testing and exploration of the blog API endpoints.

Features
User Authentication: Register and log in with password hashing for security.
Blog Management: CRUD (Create, Read, Update, Delete) operations for blog posts.
API Integration: RESTful API for blog operations, with Swagger UI documentation for easy exploration.
SQLite Database: Stores users and blog posts in a local SQLite database.
Technologies Used
Flask: Web framework for building the app.
Flask-RESTX: For creating the API and generating Swagger UI documentation.
SQLAlchemy: ORM for interacting with the SQLite database.
Werkzeug: For secure password hashing.
SQLite: A lightweight, local database for storing user data and blog posts.

Installation
Step 1: Clone the Repository
Clone the project repository to your local machine:
git clone https://github.com/anageguchadze/Blog-Flask-project.git
cd Blog-Flask-project

Step 2: Set Up a Virtual Environment
To create a virtual environment for the project:
python -m venv venv

Activate the virtual environment:

On Windows:
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate

Step 3: Install Dependencies
Install the required Python libraries:
pip install -r requirements.txt

Step 4: Set Up the Database
Run the following command to create the necessary database tables the first time you run 

the app:
python app.py
This will create the blog.db file in your project directory.

Running the Application
To start the Flask app, use the following command:
python app.py

By default, the application will be running on:
http://127.0.0.1:5000/
Swagger API Documentation

The app integrates Swagger UI for API documentation. You can access the Swagger UI at:
http://127.0.0.1:5000/

Swagger UI allows you to interact with the API endpoints and test them directly from the web interface.

Endpoints
User Authentication Endpoints
POST /register: Register a new user.
POST /login: Log in with an existing user.
GET /logout: Log out the currently logged-in user.

Blog Operations
GET /: View all blogs (Web interface).
POST /create: Create a new blog.
GET /edit/<int:blog_id>: Edit an existing blog (Web interface).
POST /delete/<int:blog_id>: Delete a specific blog.

Blog API Endpoints
GET /api/blogs: Get all blogs (API).
POST /api/blogs: Create a new blog (API).
GET /api/blogs/<int:id>: Get a specific blog by ID (API).
PUT /api/blogs/<int:id>: Update an existing blog (API).
DELETE /api/blogs/<int:id>: Delete a blog by ID (API).

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributions
Feel free to contribute to this project by creating is