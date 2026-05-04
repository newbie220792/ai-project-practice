from flask import Blueprint, jsonify, request
from app import logger
from app.services import post_data

bp = Blueprint("api", __name__)

@bp.route('/callback', methods=['POST','GET', 'PUT', 'DELETE','OPTIONS'])
def callback():
    data = request.json  # nhận JSON từ server gửi tới
    return  post_data(data)

@bp.route('/', methods=['GET'])
def get_data():
    logger.error("This is an error message from the main app")  # Example of logging an error message
    logger.warning("This is a warning message from the main app")  # Example of logging a warning
    logger.info("This is an info message from the main app")  # Example of logging an info message
    logger.critical("This is a critical message from the main app")  # Example of logging a critical message
    return jsonify({"data": "Hello, World!"})