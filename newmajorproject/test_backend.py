#!/usr/bin/env python3
"""
Test script to run the backend and check if it starts properly
"""

import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from simple_backend import app
    print("✓ Backend imported successfully")

    # Test the content endpoint
    with app.test_client() as client:
        response = client.get('/api/content')
        if response.status_code == 200:
            data = response.get_json()
            print(f"✓ Content API returned {len(data)} items")
            print("✓ Backend is working correctly!")
        else:
            print(f"✗ Content API failed with status {response.status_code}")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()