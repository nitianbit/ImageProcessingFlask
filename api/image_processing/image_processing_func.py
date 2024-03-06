from PIL import Image
from pyzbar.pyzbar import decode

# def resize_image(image_path, output_path):
#     """
#     Resize image to less than 1 MB.
#     """
#     img = Image.open(image_path)
#     img.thumbnail((1024, 1024))  # Resize image to 1024x1024 pixels
#     img.save(output_path, optimize=True, quality=95)  # Save with high quality


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
        with open(image_path, 'rb') as image_file:
            decoded_objects = decode(Image.open(image_file))
            for obj in decoded_objects:
                barcode_data.append(obj.data.decode('utf-8'))

        return barcode_data
    except Exception as e:
        print(f"Error extracting barcode: {e}")

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


