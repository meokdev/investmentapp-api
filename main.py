from flask import Flask, request, jsonify
from urllib.parse import quote_plus
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS on the Flask app

# Setup MongoDB connection
username = 'meok'
password = quote_plus('meok69')  # Use your actual MongoDB password
cluster = 'investmentapp-cluster.vah7y2w.mongodb.net'
database_name = 'investmentapp'
connection_uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName={database_name}"
client = MongoClient(connection_uri)
db = client[database_name]
collection = db['users']

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user = collection.find_one({"username": username})

    if user and user.get("password") == password:
        return jsonify(True)
    else:
        return jsonify(False)

@app.route('/adduser', methods=['POST'])
def add_user():
    data = request.json  # Assuming JSON input
    username = data.get('username')
    password1 = data.get('password1')
    password2 = data.get('password2')

    if not username or not password1 or not password2:
        return jsonify({"error": "Missing data"}), 400

    if password1 != password2:
        return jsonify({"error": "passwords do not match"}), 400

    if collection.find_one({"username": username}):
        return jsonify({"error": "username already taken"}), 400

    try:
        collection.insert_one({"username": username, "password": password1})
        return jsonify("success")
    except DuplicateKeyError:
        return jsonify({"error": "username already taken"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5011)
