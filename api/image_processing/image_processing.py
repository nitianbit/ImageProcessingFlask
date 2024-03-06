from flask import Blueprint, request, jsonify
import os
from .image_processing_func import extract_barcode, resize_image
# from .image_processing_func
image_processing_routes = Blueprint('image_processing', __name__)

# @image_processing_routes.post('/process_image')
# def process_image():
#     # input_folder_path = os.getenv('INPUT_FOLDER')
#     input_folder_path = '/NitianBit/PROCESSEDIMAGES/input'
#     # output_folder_path = os.getenv('OUTPUT_FOLDER')
#     output_folder_path = '/NitianBit/PROCESSEDIMAGES/output'
#     input_folder_path = os.path.abspath(input_folder_path)
#     print(image_processing_routes)
#     output_folder_path = os.path.abspath(output_folder_path)
#     if not os.path.exists(output_folder_path):
#         os.makedirs(output_folder_path)
#
#     for filename in os.listdir(input_folder_path):
#         if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.img')):
#             image_path = os.path.join(input_folder_path, filename)
#
#             barcode = extract_barcode(image_path)
#             # Resize image
#             if barcode:
#                 output_path = os.path.join(output_folder_path, f"{barcode}.jpg")
#             else:
#                 output_path = os.path.join(output_folder_path, filename)  # Keep original filename if no barcode
#
#             resize_image(image_path, output_path)
#
#     return jsonify({"message": "Images processed successfully."}), 200
#     return

@image_processing_routes.post('/process_image')
def process_image():
    """
    Process images in the input folder and save them to the output folder.
    """
    try:
        input_folder_path = os.path.abspath('/NitianBit/PROCESSEDIMAGES/input')
        output_folder_path = os.path.abspath('/NitianBit/PROCESSEDIMAGES/output')

        if not os.path.exists(input_folder_path):
            return jsonify({"error": "Input folder not found."}), 404

        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
        
        processed_count = 0
        error_count = 0

        for filename in os.listdir(input_folder_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.img')):
                image_path = os.path.join(input_folder_path, filename)

                barcodes = extract_barcode(image_path)

                if barcodes:
                    for idx, code in enumerate(barcodes):
                        file_ext = filename.split('.')[-1].lower()
                        output_filename = f"{code}_{idx}"  
                        output_path = os.path.join(output_folder_path, f"{output_filename}.{file_ext}")
                        resize_image(image_path, output_path)
                        processed_count += 1
                else:
                    file_ext = filename.split('.')[-1].lower()
                    output_path = os.path.join(output_folder_path, filename)
                    resize_image(image_path, output_path)
                    processed_count += 1
        if processed_count == 0:
            return jsonify({"message": "No images found in the input folder."}), 200
        elif error_count == 0:
            return jsonify({"message": f"All {processed_count} images processed successfully."}), 200
        else:
            return jsonify({"message": f"Some images processed successfully, but {error_count} encountered errors."}), 200

    except FileNotFoundError:
        return jsonify({"error": "Output folder not found."}), 500
    except Exception as e:
        print(f"Error processing images:")
        error_count += 1
        return jsonify({"message": "An error occurred while processing images."}), 500