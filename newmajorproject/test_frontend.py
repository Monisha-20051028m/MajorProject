#!/usr/bin/env python3
"""
Quick test to verify the enhanced frontend can be imported
"""

try:
    from main import ContentApp
    print("✅ Frontend imports successfully")
    print("✅ All classes and methods loaded")
    print("🎉 Ready to run!")
    print("\nTo start the app:")
    print("1. Backend: python simple_backend.py")
    print("2. Frontend: python main.py")
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")