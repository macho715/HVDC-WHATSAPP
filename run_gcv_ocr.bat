@echo off
echo Setting up Google Cloud Vision API credentials...
set GOOGLE_APPLICATION_CREDENTIALS=%~dp0client_secret_43126604210-vgs39uh1g3118fdelc9q2729glo54v4a.apps.googleusercontent.com.json

echo Checking if credentials file exists...
if not exist "%GOOGLE_APPLICATION_CREDENTIALS%" (
    echo ERROR: Credentials file not found at %GOOGLE_APPLICATION_CREDENTIALS%
    echo Please ensure the Google Cloud Vision API credentials file is in the current directory
    pause
    exit /b 1
)

echo Running WhatsApp Media OCR with Google Cloud Vision...
python whatsapp_media_ocr_extractor.py --media-only --ocr-engine gcv %*

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Script execution failed with code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo OCR processing completed successfully!
pause
