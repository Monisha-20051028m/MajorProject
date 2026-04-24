#!/usr/bin/env python3
"""
Test script to check if the main backend can start
"""
try:
    from backend.app import app
    print("✅ Backend imports successfully")

    # Test the test endpoint
    with app.test_client() as client:
        response = client.get('/test')
        if response.status_code == 200:
            print("✅ Test endpoint works")
            print("Response:", response.get_json())
        else:
            print("❌ Test endpoint failed:", response.status_code)

    # Test the realtime endpoint
    with app.test_client() as client:
        response = client.get('/realtime')
        if response.status_code == 200:
            print("✅ Real-time endpoint works")
            data = response.get_json()
            print(f"Returned {len(data)} items")
        else:
            print("❌ Real-time endpoint failed:", response.status_code)
            print("Response:", response.get_data(as_text=True))

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()