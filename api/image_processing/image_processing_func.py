from PIL import Image, ImageEnhance
from pyzbar.pyzbar import decode

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


