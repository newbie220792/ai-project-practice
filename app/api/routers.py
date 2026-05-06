from flask import Blueprint, jsonify, request
from app import logger
from app.services import face_recognition_using_deep_face, post_data

bp = Blueprint("api", __name__)

@bp.route('/callback', methods=['POST','GET', 'PUT', 'DELETE','OPTIONS'])
def callback():
    data = request.json  # nhận JSON từ server gửi tới
    return  post_data(data)

@bp.route('/recognize', methods=['POST'])
def recognize():
    data = request.json
    image_name = data.get("image")
    return face_recognition_using_deep_face(image_name)