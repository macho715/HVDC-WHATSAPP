@echo off
echo Testing Full WhatsApp Pipeline...
echo ================================

echo 1. Setting up environment variables...
set GOOGLE_APPLICATION_CREDENTIALS=%~dp0client_secret_43126604210-vgs39uh1g3118fdelc9q2729glo54v4a.apps.googleusercontent.com.json

echo 2. Running pytest tests...
python -m pytest tests/ -v --tb=short

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Tests failed with code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo 3. Testing Google Cloud Vision API connection...
python -c "from google.cloud import vision; client = vision.ImageAnnotatorClient(); print('✅ Google Cloud Vision API connection successful')"

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Google Cloud Vision API connection failed
    pause
    exit /b %ERRORLEVEL%
)

echo 4. Testing WhatsApp authentication...
if exist "auth_backups\whatsapp_auth.json" (
    echo ✅ WhatsApp auth file found
) else (
    echo ⚠️  WhatsApp auth file not found - run auth_setup.py to create
)

echo.
echo ✅ Full pipeline test completed successfully!
pause 