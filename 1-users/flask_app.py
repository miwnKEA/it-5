import os
import sqlite3
from flask import Flask, render_template, redirect, request, jsonify

app = Flask(__name__)

# get the path to the database file
dir = os.path.dirname(__file__)
db = os.path.join(dir, 'users.db')

# create table users if not exists
with sqlite3.connect(db) as conn:
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT)")

# create a get route for the index page
@app.route('/')
def index():
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()

    return render_template('index.html', users=users)

# create a post route to receive the create form data and add a new person to the database
@app.route('/create_user', methods=['POST'])
def create():
    email = request.form.get('email')
    password = request.form.get('password')
    data = (email, password)
    try:
        with sqlite3.connect(db) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (email, password) VALUES (?, ?)", data)
    except:
        return redirect('/')
    
    return redirect('/')

# create a POST request to only show page if login is succesful
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    data = (email, password)

    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", data)
        user = c.fetchone()

    # return user page if user exists or redirect to index page
    if user:
        return render_template('user.html', user=user)
    else:
        return redirect('/')

# create a GET request to show all users in JSON
@app.route('/api/users', methods=['GET'])
def users():
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()

    # Check if there are any users
    if users:
        response = {'users': users}
        return jsonify(response), 200
    else:
        response = {'message': 'No users found'}
        return jsonify(response), 404

# create a GET request to show a specific user in JSON
@app.route('/api/users/<int:id>', methods=['GET'])
def user(id):
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id=?", (id,))
        user = c.fetchone()

    # Check if the user exists
    if user:
        response = {'user': user}
        return jsonify(response), 200
    else:
        response = {'message': 'User not found'}
        return jsonify(response), 404

# create a POST request to create a new user
@app.route('/api/users', methods=['POST'])
def api_create():
    email = request.json.get('email')
    password = request.json.get('password')
    data = (email, password)
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", data)

    # Check if the POST operation affected any rows
    if c.rowcount > 0:
        response = {
            "message": "Resource was created.",
            "status": "Created"
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Resource was not created.",
            "status": "Bad Request"
        }
        return jsonify(response), 400

# create a PUT request to update a user
@app.route('/api/users/<int:id>', methods=['PUT'])
def api_update(id):
    email = request.json.get('email')
    password = request.json.get('password')
    data = (email, password, id)

    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET email=?, password=? WHERE id=?", data)

    # Check if the PUT operation affected any rows
    if c.rowcount > 0:
        response = {
            "message": f"Resource with ID {id} was updated.",
            "status": "OK"
        }
        return jsonify(response), 200
    else:
        response = {
            "message": f"Resource with ID {id} was not found.",
            "status": "Not Found"
        }
        return jsonify(response), 404

# create a DELETE request to delete a user
@app.route('/api/users/<int:id>', methods=['DELETE'])
def api_delete(id):
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (id,))

    # Check if the DELETE operation affected any rows
    if c.rowcount > 0:
        response = {
            "message": f"Resource with ID {id} was deleted.",
            "status": "OK"
        }
        return jsonify(response), 200
    else:
        response = {
            "message": f"Resource with ID {id} was not found or already deleted.",
            "status": "Not Found"
        }
        return jsonify(response), 404

# run the app
if __name__ == '__main__':
    app.run()