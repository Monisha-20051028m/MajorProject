@echo off
echo 🚀 Starting Productivity Learning App...
echo.

echo 📡 Starting Flask backend server...
start "Backend Server" python simple_backend.py

echo 🌐 Starting web frontend server...
start "Web Server" python web_server.py

timeout /t 5 /nobreak > nul

echo.
echo ✅ App started successfully!
echo 📡 Backend API: http://127.0.0.1:5000
echo 🌐 Web Interface: http://127.0.0.1:8000
echo.
echo Close the command windows to stop the servers
pause