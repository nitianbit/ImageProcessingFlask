from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    CORS(app)
    load_dotenv()

    from .image_processing.image_processing import image_processing_routes

    app.register_blueprint(image_processing_routes, url_prefix="/api/image")


    return app