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
    try:
        person_name = face_recognition_using_deep_face(image_name)
        return jsonify({"name": person_name})
    except Exception as e:
        logger.error(f"Error occurred while recognizing face: {e}")
        return jsonify({"error": str(e)}), 500  
    
@bp.route('/email', methods=['GET', 'POST'])
def send_email():
    data = request.json
    subject = data.get("subject")
    body = data.get("body")
    to = data.get("to")
    try:
        send_email(subject, body, to)
        return jsonify({"message": "Email sent successfully"})
    except Exception as e:
        logger.error(f"Error occurred while sending email: {e}")
        return jsonify({"error": str(e)}), 500      
    except Exception as e:
        logger.error(f"Error occurred while recognizing face: {e}")
        return jsonify({"error": str(e)}), 500  