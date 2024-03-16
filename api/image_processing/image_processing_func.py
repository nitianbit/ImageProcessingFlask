from PIL import Image, ImageEnhance
from pyzbar.pyzbar import decode
import cv2
import os

def add_logo(image_path, output_path):
    """
    Add a logo to the top right corner of the image.
    
    :param image_path: Path to the input image file.
    :param logo_path: Path to the logo image file.
    :param output_path: Path to save the output image file.
    """
    try:
        # Open the input image and the logo image
        image = Image.open(image_path)

        current_directory = os.getcwd()
        image_directory = os.path.join(current_directory, 'images','logo.png')
        logo = Image.open(image_directory)

        # Resize the logo to fit in the top right corner
        logo_width, logo_height = logo.size
        image_width, image_height = image.size
        ratio = min((image_width / 8) / logo_width, (image_height / 8) / logo_height)
        new_logo_width = int(logo_width * ratio)
        new_logo_height = int(logo_height * ratio)
        logo = logo.resize((new_logo_width, new_logo_height))

        # Calculate the position to place the logo (top right corner)
        position = (image_width - new_logo_width, 0)

        # Paste the logo onto the image
        image.paste(logo, position, logo)

        # Save the modified image
        image.save(output_path)

        return True
    except Exception as e:
        print(f"Error adding logo: {e}")
        return False

def increased_image_quality(image_path):
    """
    Preprocess the image to enhance QR code visibility.
    """
    try:
        img = Image.open(image_path)

        # Enhance image contrast and sharpness
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)  
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2.0)  

        img = img.convert('L')
        img = img.convert('RGB')

        return img

    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def preprocess(image):
	# load the image
	image = cv2.imread(args["image"])

	#resize image
	image = cv2.resize(image,None,fx=0.7, fy=0.7, interpolation = cv2.INTER_CUBIC)

	#convert to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	#calculate x & y gradient
	gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
	gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)

	# subtract the y-gradient from the x-gradient
	gradient = cv2.subtract(gradX, gradY)
	gradient = cv2.convertScaleAbs(gradient)

	# blur the image
	blurred = cv2.blur(gradient, (3, 3))

	# threshold the image
	(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
	thresh = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	return thresh

def resize_image(image_path, output_path):
    """
    Resize image to less than 1 MB.
    """
    try:
        img = Image.open(image_path)
        img.thumbnail((1024, 1024))  # Resize image to 1024x1024 pixels
        img.save(output_path, optimize=True, quality=95)  # Save with high quality
    except Exception as e:
        print(f"Error resizing image: {e}")


def extract_barcode(image_path):
    """
    Extract barcode from image.
    """
    try:
        barcode_data = []
        processed_img = increased_image_quality(image_path)
        if processed_img:
            decoded_objects = decode(processed_img)
            for obj in decoded_objects:
                barcode_data.append(obj.data.decode('utf-8'))
        return barcode_data
    except Exception as e:
        print(f"Error extracting barcode: {e}")
        return []

def update_stats_file(uploaded_count, compressed_count, copied_count, failed_count):
    """
    Update the statistics file with the new counts.
    """
    stats_file_path = os.path.abspath('stats.txt')

    if not os.path.exists(stats_file_path):
        # Create the file and write the initial data
        with open(stats_file_path, 'w') as file:
            file.write(f"Uploaded: {uploaded_count}\n")
            file.write(f"Compressed: {compressed_count}\n")
            file.write(f"Copied: {copied_count}\n")
            file.write(f"Failed: {failed_count}\n")
    else:
        # Read the existing data, update it, and rewrite the file
        with open(stats_file_path, 'r') as file:
            lines = file.readlines()

        # Update the counts
        lines[0] = f"Uploaded: {int(lines[0].split(':')[1]) + uploaded_count}\n"
        lines[1] = f"Compressed: {int(lines[1].split(':')[1]) + compressed_count}\n"
        lines[2] = f"Copied: {int(lines[2].split(':')[1]) + copied_count}\n"
        lines[3] = f"Failed: {int(lines[3].split(':')[1]) + failed_count}\n"

        # Rewrite the file with updated data
        with open(stats_file_path, 'w') as file:
            file.writelines(lines)

def scanned_barcodes_txt(scanned_barcode):
    for barcode in scanned_barcode:
        f.write(f"{barcode}\n")




#
# def extract_barcode(image_path):
#     """
#     Extract barcode from image.
#     """
#     with open(image_path, 'rb') as image_file:
#         decoded_objects = decode(Image.open(image_file))
#         if decoded_objects:
#             barcode_data = decoded_objects[0].data.decode('utf-8')
#             return barcode_data
#         else:
#             return None


