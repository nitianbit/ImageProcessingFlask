from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from datetime import datetime

dashboard_routes = Blueprint('dashboard', __name__)

@dashboard_routes.get('/dashboard')
# @jwt_required()
def get_stats():
    try:
        stat_folder_path = os.path.abspath('../pmj/stats')

        current_date = datetime.now().strftime('%d_%m_%Y')
        stats_file_path = os.path.join(stat_folder_path, f'stat_{current_date}.txt')

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
