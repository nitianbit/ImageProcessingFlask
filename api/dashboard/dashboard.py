from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

dashboard_routes = Blueprint('dashboard', __name__)

@dashboard_routes.get('/dashboard')
# @jwt_required()
def get_stats():
    try:
        stats_file_path = os.path.abspath('../pmj/stats/stat_24_03_2024.txt')

        if not os.path.exists(stats_file_path):
            return jsonify({"error": "Stats file not found"}), 404

        # Read the stats data from the file
        with open(stats_file_path, 'r') as file:
            stats_data = file.readlines()

        # Prepare the data to be returned
        stats = {}
        for line in stats_data:
            key, value = line.strip().split(': ')
            stats[key] = int(value)

        return jsonify(stats), 200

    except Exception as e:
        return jsonify({"error": "An error occurred."}), 500
