from flask import Flask, jsonify, request
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

@app.route('/callback', methods=['POST','GET', 'PUT', 'DELETE'])
def callback():
    data = request.json  # nhận JSON từ server gửi tới
    print("Received body:", data)  # in ra phần body của JSON

    post_data(data)
    # xử lý logic ở đây
    return jsonify({"status": "ok"}), 200

@app.route('/', methods=['GET'])
def get_data():
    return jsonify({"data": "Hello, World!"})


def post_data(data):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO imou_camera (alarm_id, dname, msg_type, thumb_url, data) VALUES (%s, %s, %s, %s, %s)",
            (
                data.get("alarm_id"),
                data.get("dname"),
                data.get("msg_type"),
                data.get("thumbUrl"),
                data
            )
        )
        
        conn.commit()
        cur.close()
        conn.close()
        # print({"DB_HOST": os.getenv("DB_HOST"), "DB_NAME": os.getenv("DB_NAME"), "DB_USER": os.getenv("DB_USER"), "DB_PASSWORD": os.getenv("DB_PASSWORD")})
        return jsonify({"status": "saved"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)