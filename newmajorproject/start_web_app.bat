@echo off
echo 🚀 Starting Productivity Learning App (Web Version)
echo.

echo 📡 Starting Backend Server...
start cmd /k "cd /d %~dp0 && python simple_backend.py"

timeout /t 3 /nobreak > nul

echo 🌐 Starting Web Frontend Server...
start cmd /k "cd /d %~dp0 && python web_server.py"

echo.
echo ✅ Both servers are starting...
echo 📱 Open Chrome and go to: http://127.0.0.1:8000
echo 🎯 Backend runs on port 5000, Frontend on port 8000
echo.
echo Press any key to close this window...
pause > nul