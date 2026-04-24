#!/usr/bin/env python3
"""
Run the backend server
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from simple_backend import app

if __name__ == '__main__':
    print("🚀 Starting Backend Server...")
    print("📡 API will be available at: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    app.run(host='127.0.0.1', port=5000, debug=False)