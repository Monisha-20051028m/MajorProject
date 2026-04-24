@echo off
echo 🤖 OpenAI API Key Setup for AI Summaries
echo.
echo This will enable GPT-powered intelligent summaries instead of basic text extraction.
echo.
echo 1. Get your API key from: https://platform.openai.com/api-keys
echo 2. Enter your API key below (it will be saved as an environment variable)
echo.
set /p API_KEY="Enter your OpenAI API Key: "
if "%API_KEY%"=="" (
    echo ❌ No API key entered. AI summaries will use basic text extraction.
    pause
    exit /b 1
)

echo Setting OPENAI_API_KEY environment variable...
setx OPENAI_API_KEY "%API_KEY%" /M
echo ✅ OpenAI API key configured!
echo.
echo 🔄 Restart the backend server for changes to take effect.
echo.
echo To test: Run the app and click "AI Summary" on any content card.
echo.
pause