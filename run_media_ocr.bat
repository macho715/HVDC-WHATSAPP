@echo off
REM WhatsApp 미디어 OCR 실행 스크립트
REM MACHO-GPT v3.4-mini | Samsung C&T Logistics · HVDC Project

echo.
echo ========================================
echo  WhatsApp 미디어 OCR 분석 모듈
echo  MACHO-GPT v3.4-mini
echo ========================================
echo.

REM 현재 디렉토리 확인
cd /d "%~dp0"
echo 현재 작업 디렉토리: %CD%
echo.

REM Python 환경 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았습니다.
    echo 💡 Python 3.8+ 설치 후 다시 시도하세요.
    pause
    exit /b 1
)

echo ✅ Python 환경 확인 완료
echo.

REM 가상환경 활성화 (있는 경우)
if exist "venv\Scripts\activate.bat" (
    echo 🔄 가상환경 활성화 중...
    call venv\Scripts\activate.bat
    echo ✅ 가상환경 활성화 완료
    echo.
)

REM 필요한 디렉토리 생성
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "downloads" mkdir downloads
if not exist "auth_backups" mkdir auth_backups

echo 📁 필요한 디렉토리 생성 완료
echo.

REM 의존성 설치 확인
echo 🔍 미디어 OCR 라이브러리 확인 중...
python -c "import easyocr, fitz, PIL" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 미디어 OCR 라이브러리가 설치되지 않았습니다.
    echo 💡 설치를 진행합니다...
    echo.
    
    REM requirements 파일 확인
    if exist "requirements_media_ocr.txt" (
        echo 📦 미디어 OCR 라이브러리 설치 중...
        pip install -r requirements_media_ocr.txt
        if errorlevel 1 (
            echo ❌ 라이브러리 설치 실패
            echo 💡 수동으로 설치하세요: pip install easyocr PyMuPDF pdf2image pytesseract pillow
            pause
            exit /b 1
        )
    ) else (
        echo ❌ requirements_media_ocr.txt 파일을 찾을 수 없습니다.
        pause
        exit /b 1
    )
    echo ✅ 라이브러리 설치 완료
    echo.
) else (
    echo ✅ 미디어 OCR 라이브러리 확인 완료
    echo.
)

REM 메뉴 표시
echo 📋 실행 옵션을 선택하세요:
echo.
echo 1. HVDC 물류팀 미디어 추출 (기본)
echo 2. 특정 채팅방 미디어 추출
echo 3. 모든 채팅방 자동 추출
echo 4. 미디어 OCR 대시보드 실행
echo 5. 테스트 실행
echo 6. 종료
echo.

set /p choice="선택 (1-6): "

if "%choice%"=="1" goto basic_extraction
if "%choice%"=="2" goto specific_extraction
if "%choice%"=="3" goto auto_extraction
if "%choice%"=="4" goto dashboard
if "%choice%"=="5" goto run_tests
if "%choice%"=="6" goto exit
goto invalid_choice

:basic_extraction
echo.
echo 🔄 HVDC 물류팀 미디어 추출 시작...
echo.
python whatsapp_media_ocr_extractor.py
echo.
echo ✅ 기본 추출 완료
pause
goto end

:specific_extraction
echo.
set /p chat_name="채팅방 이름을 입력하세요: "
set /p max_media="최대 미디어 개수 (기본: 10): "
if "%max_media%"=="" set max_media=10

echo.
echo 🔄 %chat_name% 채팅방 미디어 추출 시작...
echo.
python whatsapp_media_ocr_extractor.py --chat "%chat_name%" --max-media %max_media%
echo.
echo ✅ 특정 채팅방 추출 완료
pause
goto end

:auto_extraction
echo.
set /p max_media="최대 미디어 개수 (기본: 30): "
if "%max_media%"=="" set max_media=30

echo.
echo 🔄 모든 채팅방 자동 추출 시작...
echo.
python whatsapp_media_ocr_extractor.py --auto --max-media %max_media%
echo.
echo ✅ 자동 추출 완료
pause
goto end

:dashboard
echo.
echo 📊 미디어 OCR 대시보드 실행 중...
echo 🌐 브라우저에서 http://localhost:8501 접속
echo.
streamlit run whatsapp_media_ocr_dashboard.py
echo.
echo ✅ 대시보드 종료
pause
goto end

:run_tests
echo.
echo 🧪 미디어 OCR 테스트 실행 중...
echo.
python -m pytest tests/test_media_ocr.py -v
echo.
echo ✅ 테스트 완료
pause
goto end

:invalid_choice
echo.
echo ❌ 잘못된 선택입니다. 1-6 중에서 선택하세요.
echo.
pause
goto end

:exit
echo.
echo 👋 프로그램을 종료합니다.
exit /b 0

:end
echo.
echo ========================================
echo  실행 완료
echo ========================================
echo.
echo 📁 결과 파일 위치:
echo   - 미디어 OCR 결과: data/whatsapp_media_ocr_*.json
echo   - 로그 파일: logs/whatsapp_media_ocr.log
echo   - 다운로드 파일: downloads/
echo.
echo 🔧 다음 명령어로 대시보드를 실행할 수 있습니다:
echo   streamlit run whatsapp_media_ocr_dashboard.py
echo.
pause 