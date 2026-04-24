#!/usr/bin/env python3
"""
Test script to verify the productivity app components work
"""

def test_imports():
    """Test if all required imports work"""
    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False

    try:
        import pymongo
        print("✓ PyMongo imported successfully")
    except ImportError as e:
        print(f"✗ PyMongo import failed: {e}")
        return False

    try:
        import kivy
        print("✓ Kivy imported successfully")
    except ImportError as e:
        print(f"✗ Kivy import failed: {e}")
        return False

    try:
        import transformers
        print("✓ Transformers imported successfully")
    except ImportError as e:
        print(f"✗ Transformers import failed: {e}")
        return False

    try:
        import openai
        print("✓ OpenAI imported successfully")
    except ImportError as e:
        print(f"✗ OpenAI import failed: {e}")
        return False

    return True

def test_backend_components():
    """Test backend components"""
    try:
        from backend.db import collection
        print("✓ Database connection successful")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

    try:
        from backend.utils.filter import is_useful
        # Test with sample data
        test_item = {"title": "Machine Learning Basics", "description": "Learn ML fundamentals"}
        result = is_useful(test_item)
        print(f"✓ Content filter working: {result}")
    except Exception as e:
        print(f"✗ Content filter failed: {e}")
        return False

    return True

def test_fetch_functions():
    """Test fetch functions"""
    try:
        from backend.fetch.youtube import fetch_youtube
        data = fetch_youtube()
        print(f"✓ YouTube fetch working: {len(data)} items")
    except Exception as e:
        print(f"✗ YouTube fetch failed: {e}")

    try:
        from backend.fetch.news import fetch_news
        data = fetch_news()
        print(f"✓ News fetch working: {len(data)} items")
    except Exception as e:
        print(f"✗ News fetch failed: {e}")

    try:
        from backend.fetch.rss import fetch_rss
        data = fetch_rss()
        print(f"✓ RSS fetch working: {len(data)} items")
    except Exception as e:
        print(f"✗ RSS fetch failed: {e}")

if __name__ == "__main__":
    print("Testing Productivity App Components")
    print("=" * 40)

    print("\n1. Testing imports...")
    imports_ok = test_imports()

    if imports_ok:
        print("\n2. Testing backend components...")
        backend_ok = test_backend_components()

        print("\n3. Testing fetch functions...")
        test_fetch_functions()

        print("\n" + "=" * 40)
        print("✓ All tests completed!")
        print("\nTo run the app:")
        print("1. Backend: cd backend && python app.py")
        print("2. Frontend: python main.py")
    else:
        print("\n✗ Import tests failed. Please install missing dependencies:")
        print("pip install -r requirements.txt")