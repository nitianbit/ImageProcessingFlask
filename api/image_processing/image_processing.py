from flask import Blueprint, request, jsonify
import os
from .image_processing_func import extract_barcode, resize_image
# from .image_processing_func
image_processing_routes = Blueprint('image_processing', __name__)

@image_processing_routes.post('/process_image')
def process_image():
    # input_folder_path = os.getenv('INPUT_FOLDER')
    input_folder_path = '/NitianBit/PROCESSEDIMAGES/input'
    # output_folder_path = os.getenv('OUTPUT_FOLDER')
    output_folder_path = '/NitianBit/PROCESSEDIMAGES/output'
    input_folder_path = os.path.abspath(input_folder_path)
    print(image_processing_routes)
    output_folder_path = os.path.abspath(output_folder_path)
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(input_folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.img')):
            image_path = os.path.join(input_folder_path, filename)

            barcode = extract_barcode(image_path)
            # Resize image
            if barcode:
                output_path = os.path.join(output_folder_path, f"{barcode}.jpg")
            else:
                output_path = os.path.join(output_folder_path, filename)  # Keep original filename if no barcode

            resize_image(image_path, output_path)

    return jsonify({"message": "Images processed successfully."}), 200
    return
