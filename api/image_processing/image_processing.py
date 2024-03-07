from flask import Blueprint, request, jsonify
import os
import shutil
import logging
from .image_processing_func import extract_barcode, resize_image, scanned_barcodes_txt, increased_image_quality
image_processing_routes = Blueprint('image_processing', __name__)

@image_processing_routes.post('/process_image')
def process_image():
    """
    Process images in the input folder and save them to the output folder.
    """
    try:
        input_folder_path = os.path.abspath('/NitianBit/PROCESSEDIMAGES/input')
        output_folder_path = os.path.abspath('/NitianBit/PROCESSEDIMAGES/output')
        temp_folder_path = os.path.abspath('/NitianBit/PROCESSEDIMAGES/temp')
        failed_folder_path = os.path.abspath('/NitianBit/PROCESSEDIMAGES/failed')

        if not os.path.exists(input_folder_path):
            return jsonify({"error": "Input folder not found."}), 404

        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
        
        if not os.path.exists(failed_folder_path):
            os.makedirs(failed_folder_path)

        uploaded_count = 0
        compressed_count = 0
        copied_count = 0
        failed_count = 0

        scanned_barcodes = []

        for filename in os.listdir(input_folder_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.img')):
                image_path = os.path.join(input_folder_path, filename)

                uploaded_count += 1

                barcodes = extract_barcode(image_path)

                if barcodes:
                    for idx, code in enumerate(barcodes):
                        file_ext = filename.split('.')[-1].lower()
                        output_filename = f"{code}_{idx}"  
                        output_path = os.path.join(output_folder_path, f"{output_filename}.{file_ext}")
                        resize_image(image_path, output_path)
                        compressed_count += 1
                        scanned_barcodes.append(code)
                        temp_output_path = os.path.join(temp_folder_path, filename)
                        shutil.copy(image_path, temp_output_path)
                        copied_count += 1
                else:
                    failed_path = os.path.join(failed_folder_path, filename)
                    shutil.move(image_path, failed_path)
                    failed_count += 1
                
                
                # try:
                #     shutil.copy(image_path, temp_output_path)
                #     copied_count += 1
                # except Exception as e:
                #     logging.error(f"Error copying image: {e}")
                #     # Handle the error as needed, such as returning an error response
                #     return jsonify({"error": "Failed to copy image."}), 500
        logging.info(f"Number of pictures uploaded today: {uploaded_count}")
        logging.info(f"Count of compressed images: {compressed_count}")
        logging.info(f"Quantity of images copied to the temporary folder: {copied_count}")
        logging.info(f"Number of failed instances: {failed_count}")

        scanned_barcodes_txt(scanned_barcodes)


        return jsonify({
            "data":{
                uploaded_count,
                compressed_count,
                copied_count,
                failed_count
            },
            "message":"image processed completed with following data",
            "code":200
        }), 200

    except FileNotFoundError:
        return jsonify({"error": "Output folder not found."}), 500
    except Exception as e:
        print(f"Error processing images:")
        return jsonify({"message": "An error occurred while processing images.{e}"}), 500