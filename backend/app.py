from flask_cors import CORS
app = Flask(__name__, static_folder='static')
CORS(app)

from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

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
    app.run(debug=True)
