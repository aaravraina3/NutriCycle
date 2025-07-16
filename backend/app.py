from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Backend is running!"})

@app.route('/report')
def serve_pdf():
    return app.send_static_file('NutriCycle.pdf')

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



@app.route('/api/logs/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    try:
        conn = sqlite3.connect('compost.db')
        cursor = conn.cursor()
        
        # Check if log exists
        cursor.execute('SELECT * FROM compost_logs WHERE id = ?', (log_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"status": "error", "message": "Log not found"}), 404
        
        # Delete the log
        cursor.execute('DELETE FROM compost_logs WHERE id = ?', (log_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Log deleted"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # THIS IS THE KEY CHANGE - USE PORT FROM ENVIRONMENT OR 8000
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
