#!/usr/bin/env python3
"""
Simple web server to serve the HTML frontend
"""
from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'web_frontend.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("🌐 Starting Web Frontend Server...")
    print("📱 Open your browser and go to: http://127.0.0.1:8000")
    print("🎯 Make sure the backend is also running on port 5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=8000)