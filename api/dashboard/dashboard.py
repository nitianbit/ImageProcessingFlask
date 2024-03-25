from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from datetime import datetime
from utils.constant import (
    current_date_barcode_txt_path_constant,
    current_iteration_barcode_txt_path_constant
)

dashboard_routes = Blueprint('dashboard', __name__)

@dashboard_routes.get('/dashboard')
# @jwt_required()
def get_stats():
    try:
        stat_folder_path = os.path.abspath(current_date_barcode_txt_path_constant)
        current_stat_folder_path =  os.path.abspath(current_iteration_barcode_txt_path_constant)

        current_date = datetime.now().strftime('%d_%m_%Y')
        stats_file_path = os.path.join(stat_folder_path, f'stat_{current_date}.txt')
        current_iteration_file_path = os.path.join(current_stat_folder_path, f'current_iteration.txt')

        if not os.path.exists(stats_file_path):
            return jsonify({"error": "Stats file not found"}), 404
        
        if not os.path.exists(current_iteration_file_path):
            return jsonify({"error": "Current iteration Stats file not found"}), 404

        # Read the stats data from the file
        with open(stats_file_path, 'r') as file:
            stats_data = file.readlines()
        
        with open(current_iteration_file_path, 'r') as file:
            current_iteration_stats_data = file.readlines()
        # Prepare the data to be returned
        stats = {}
        for line in stats_data:
            key, value = line.strip().split(': ')
            stats[key] = int(value)
        
        current_stats = {}
        for line in current_iteration_stats_data:
            key, value = line.strip().split(': ')
            current_stats[key] = int(value)

        return jsonify({"globalData":stats,
                        "currentData":current_stats}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred."}), 500
