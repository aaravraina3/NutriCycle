from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Backend is running!"})

@app.route('/api/log', methods=['POST'])
def log_compost():
    data = request.get_json()
    weight = data.get('weight')
    location = data.get('location')

    conn = sqlite3.connect('compost.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO compost_logs (weight, location)
        VALUES (?, ?)
    ''', (weight, location))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "weight": weight, "location": location})

@app.route('/api/logs', methods=['GET'])
def get_logs():
    conn = sqlite3.connect('compost.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM compost_logs')
    logs = cursor.fetchall()
    conn.close()

    return jsonify([{
        "id": log[0],
        "weight": log[1],
        "location": log[2],
        "timestamp": log[3]
    } for log in logs])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
