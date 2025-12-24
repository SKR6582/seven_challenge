import os
import csv
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import webbrowser
from threading import Timer

app = Flask(__name__)

# --- CONFIGURATION ---
HIDE_NUMBERS = False # True: 3초 후 숫자를 숨김, False: 항상 숫자를 보여줌
CSV_FILE = 'records.csv'
# ---------------------

# Ensure CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'student_id', 'elapsed', 'diff'])

def get_records():
    records = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)

    # Sort by diff (absolute difference from 7.000)
    # We convert to float for proper sorting
    records.sort(key=lambda x: abs(float(x['diff'])))
    return records[:10] # Top 10

@app.route('/')
def index():
    return render_template('index.html', hide_numbers=HIDE_NUMBERS)

@app.route('/records')
def records():
    return jsonify(get_records())

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    elapsed = data.get('elapsed')
    diff = data.get('diff')
    student_id = data.get('student_id', '-')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, student_id, elapsed, diff])

    return jsonify(success=True)

def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    # Use a timer to open the browser after the server starts
    Timer(1, open_browser).start()
    app.run(port=5000)
