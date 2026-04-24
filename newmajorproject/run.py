#!/usr/bin/env python3
"""
Productivity Hub Launcher
Starts both backend and frontend services
"""

import subprocess
import time
import sys
import os

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting backend server...")
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    return subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

def start_frontend():
    """Start the Kivy frontend application"""
    print("📱 Starting frontend application...")
    return subprocess.Popen(
        [sys.executable, 'main.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

def main():
    print("🎯 Productivity Hub - Starting all services...")

    # Start backend
    backend_process = start_backend()

    # Wait a moment for backend to initialize
    print("⏳ Waiting for backend to initialize...")
    time.sleep(3)

    # Check if backend is running
    if backend_process.poll() is None:
        print("✅ Backend started successfully")
    else:
        print("❌ Backend failed to start")
        stdout, stderr = backend_process.communicate()
        print("Backend stdout:", stdout.decode())
        print("Backend stderr:", stderr.decode())
        return

    # Start frontend
    frontend_process = start_frontend()

    # Wait a moment for frontend to initialize
    time.sleep(2)

    if frontend_process.poll() is None:
        print("✅ Frontend started successfully")
        print("\n🎉 Productivity Hub is now running!")
        print("📋 Backend: http://127.0.0.1:5000")
        print("🖥️  Frontend: Kivy desktop application")
        print("\nPress Ctrl+C to stop all services")
    else:
        print("❌ Frontend failed to start")
        stdout, stderr = frontend_process.communicate()
        print("Frontend stdout:", stdout.decode())
        print("Frontend stderr:", stderr.decode())
        backend_process.terminate()
        return

    try:
        # Keep running until user interrupts
        while True:
            time.sleep(1)
            if backend_process.poll() is not None:
                print("⚠️  Backend process ended unexpectedly")
                break
            if frontend_process.poll() is not None:
                print("⚠️  Frontend process ended unexpectedly")
                break

    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")

    finally:
        # Clean up processes
        if backend_process.poll() is None:
            backend_process.terminate()
            print("✅ Backend stopped")

        if frontend_process.poll() is None:
            frontend_process.terminate()
            print("✅ Frontend stopped")

        print("👋 Productivity Hub stopped")

if __name__ == "__main__":
    main()