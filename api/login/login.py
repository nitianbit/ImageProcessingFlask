from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
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
                access_token = create_access_token(identity=username)
                return jsonify({"access_token": access_token}), 200
            else:
                return jsonify({"error": "Invalid username or password"}), 401
        else:
            return jsonify({"error": "Missing username or password"}), 400

    except Exception as e:
        return jsonify({"message": "An error occurred."}), 500

