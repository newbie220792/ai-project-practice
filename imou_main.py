from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

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
            host="localhost",
            database="your_db",
            user="your_user",
            password="your_password"
        )
        cur = conn.cursor()
        
        data = request.json
        cur.execute(
            "INSERT INTO imou_camera (data) VALUES (%s)",
            (data,)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "saved"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)