@echo off
echo 🚀 Starting Backend Server...
echo 📡 API will be available at: http://127.0.0.1:5000
cd /d %~dp0
python -c "from simple_backend import app; app.run(host='127.0.0.1', port=5000, debug=False)"
pause