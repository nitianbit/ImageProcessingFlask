from flask import Blueprint, request, jsonify
import json
from .loginData import loginData
login_routes = Blueprint('login', __name__)


@login_routes.post('')
def login():
    try:
        data = request.json

        if 'username' in data and 'password' in data:
            username = data['username']
            password = data['password']

            # Check if the provided credentials match
            if username == loginData['username'] and password == loginData['password']:
                return jsonify({"message": "Login successful"})
            else:
                return jsonify({"error": "Invalid username or password"}), 401
        else:
            return jsonify({"error": "Missing username or password"}), 400

    except Exception as e:
        return jsonify({"message": "An error occurred."}), 500

