from flask import Flask, jsonify, request
import psycopg2
# import mysql.connector
import os
from dotenv import load_dotenv
from psycopg2.extras import Json

app = Flask(__name__)

load_dotenv()

BLACKLIST_CAMERAS = set(['Nhà 2', 'Nhà 1'])  # Danh sách đen để lưu trữ các IP đã bị chặn

@app.route('/callback', methods=['POST','GET', 'PUT', 'DELETE'])
def callback():
    data = request.json  # nhận JSON từ server gửi tới
    # print("Received body:", data)  # in ra phần body của JSON

    return  post_data(data)
    # xử lý logic ở đây

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
        # raw_data  = Json(data);
        alarmId= data.get("alarmId");
        dname= data.get("dname");
        msgType = data.get("msgType");
        thumbUrl = data.get("thumbUrl");
        time = data.get("time");

        if dname in BLACKLIST_CAMERAS:
            print(f"Camera {dname} is blacklisted. Skipping save.")
            return jsonify({"status": f"Camera '{dname}' is blacklisted. Skipping save."}), 200
        
        cur.execute(
            "INSERT INTO imou_camera_log (alarm_id, dname, msg_type, thumb_url, data, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                alarmId,
                dname,
                msgType,
                thumbUrl,
                Json(data),
                time
            )
        )
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "saved"}), 200
    except Exception as e:
        print(str(e));
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)