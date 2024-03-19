from flask import Blueprint, request, jsonify
import os
import shutil
import logging
from collections import defaultdict
from flask_jwt_extended import jwt_required, get_jwt_identity
from .image_processing_func import extract_and_enhance_barcode, resize_image, add_logo, update_stats_file
image_processing_routes = Blueprint('image_processing', __name__)

@image_processing_routes.post('/process_image')
def process_image():
    try:
        # input_folder_path = '/path/to/input'
        # output_folder_path = '/path/to/output'
        # temp_folder_path = '/path/to/temp'
        # failed_folder_path = '/path/to/failed'

        input_folder_path = os.path.abspath('/NitianBit/PROCESSEDIMAGES/input')
        output_folder_path = os.path.abspath('/NitianBit/PROCESSEDIMAGES/output')
        temp_folder_path = os.path.abspath('/NitianBit/PROCESSEDIMAGES/temp')
        failed_folder_path = os.path.abspath('/NitianBit/PROCESSEDIMAGES/failed')

        uploaded_count = 0
        compressed_count = 0
        copied_count = 0
        failed_count = 0

        for filename in os.listdir(input_folder_path):
            if filename.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff')):
                image_path = os.path.join(input_folder_path, filename)
                output_path = os.path.join(output_folder_path, filename)

                uploaded_count += 1

                barcodes = extract_and_enhance_barcode(image_path)
                if barcodes:
                      for idx, barcode in enumerate(barcodes): 
                            file_ext = filename.split('.')[-1].lower()
                            output_filename = f"{barcode}_{idx}"
                            output_path = os.path.join(output_folder_path, f"{output_filename}.{file_ext}")
                            resize_image(image_path, output_path)
                            add_logo(output_path, output_path) 
                            shutil.copy(output_path, temp_folder_path)
                            compressed_count += 1
                            copied_count += 1
                else:
                      shutil.move(image_path, failed_folder_path)
                      failed_count += 1
                os.remove(image_path)

        update_stats_file(uploaded_count, compressed_count, copied_count, failed_count)

        return jsonify({
            "Uploaded": uploaded_count,
            "Compressed": compressed_count,
            "Copied": copied_count,
            "Failed": failed_count
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @image_processing_routes.post('/process_image')
# @jwt_required()
# def process_image():
#     """
#     Process images in the input folder and save them to the output folder.
#     """
#     try:
#         input_folder_path = os.path.abspath('/NitianBit/PROCESSEDIMAGES/input')
#         output_folder_path = os.path.abspath('/NitianBit/PROCESSEDIMAGES/output')
#         temp_folder_path = os.path.abspath('/NitianBit/PROCESSEDIMAGES/temp')
#         failed_folder_path = os.path.abspath('/NitianBit/PROCESSEDIMAGES/failed')

#         if not os.path.exists(input_folder_path):
#             return jsonify({"error": "Input folder not found."}), 404

#         if not os.path.exists(output_folder_path):
#             os.makedirs(output_folder_path)
        
#         if not os.path.exists(failed_folder_path):
#             os.makedirs(failed_folder_path)

#         uploaded_count = 0
#         compressed_count = 0
#         copied_count = 0
#         failed_count = 0

#         scanned_barcodes = defaultdict(list)

#         num_images = sum(1 for filename in os.listdir(input_folder_path)
#                          if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.img')))
#         if num_images <= 0:
#             return jsonify({"error": "No images are there"}), 500

#         for filename in os.listdir(input_folder_path):
#             if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.img')):
#                 image_path = os.path.join(input_folder_path, filename)

#                 uploaded_count += 1

#                 barcodes = extract_barcode(image_path)

#                 if barcodes:
#                     for idx, code in enumerate(barcodes):
#                         file_ext = filename.split('.')[-1].lower()
#                         output_filename = f"{code}_{idx}"  
#                         output_path = os.path.join(output_folder_path, f"{output_filename}.{file_ext}")
#                         resize_image(image_path, output_path)
#                         compressed_count += 1
#                         scanned_barcodes[code].append(filename)  # Add filename to barcode entry
#                         temp_output_path = os.path.join(temp_folder_path, filename)
#                         shutil.copy(image_path, temp_output_path)
#                         add_logo(image_path, output_path)
#                         copied_count += 1
#                 else:
#                     failed_path = os.path.join(failed_folder_path, filename)
#                     shutil.move(image_path, failed_path)
#                     failed_count += 1
        
#         # Calculate duplicate image count
#         duplicate_count = sum(len(filenames) - 1 for filenames in scanned_barcodes.values() if len(filenames) > 1)
        
#         update_stats_file(uploaded_count, compressed_count, copied_count, failed_count)
#         return jsonify({
#             "data": {
#                 "Uploaded": uploaded_count,
#                 "Compressed": compressed_count,
#                 "Copied": copied_count,
#                 "Failed": failed_count,
#                 "Duplicates": duplicate_count  # Include count of duplicate images
#             },
#             "message": "Image processing completed with the following data",
#             "code": 200
#         }), 200

#     except FileNotFoundError:
#         return jsonify({"error": "Output folder not found."}), 500
#     except Exception as e:
#         print(f"Error processing images: {e}")
#         return jsonify({"message": f"An error occurred while processing images: {e}"}), 500
