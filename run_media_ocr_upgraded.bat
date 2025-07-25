@echo off
REM WhatsApp 미디어 OCR 실행 스크립트 (업그레이드)
REM MACHO-GPT v3.4-mini | Samsung C&T Logistics · HVDC Project

echo.
echo ========================================
echo  WhatsApp 미디어 OCR 분석 모듈 (업그레이드)
echo  MACHO-GPT v3.4-mini
echo ========================================
echo.

REM 환경 확인
echo 🔍 환경 확인 중...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았습니다.
    pause
    exit /b 1
)

REM 디렉토리 생성
if not exist "data" mkdir data
if not exist "downloads" mkdir downloads
if not exist "logs" mkdir logs

REM 의존성 설치 확인
echo 📦 의존성 설치 확인 중...
pip show easyocr >nul 2>&1
if errorlevel 1 (
    echo ⚠️ OCR 라이브러리가 설치되지 않았습니다. 설치를 시작합니다...
    pip install --user -r requirements_media_ocr_upgraded.txt
    if errorlevel 1 (
        echo ❌ 의존성 설치 실패
        pause
        exit /b 1
    )
)

echo ✅ 환경 설정 완료
echo.

REM 메뉴 표시
echo 📋 실행 옵션을 선택하세요:
echo.
echo 1. 기본 미디어 추출 (EasyOCR)
echo 2. AWS Textract 엔진 사용
echo 3. Google Cloud Vision 엔진 사용
echo 4. Naver CLOVA OCR 엔진 사용
echo 5. 모든 채팅방 자동 추출
echo 6. 업그레이드된 대시보드 실행
echo 7. 테스트 실행
echo 8. 종료
echo.

set /p choice="선택 (1-8): "

if "%choice%"=="1" (
    echo.
    echo 🚀 기본 미디어 추출 시작...
    python whatsapp_media_ocr_extractor.py --chat "HVDC 물류팀" --max-media 10
    goto end
)

if "%choice%"=="2" (
    echo.
    echo 🚀 AWS Textract 엔진으로 추출 시작...
    python whatsapp_media_ocr_extractor.py --chat "HVDC 물류팀" --ocr-engine textract --max-media 10
    goto end
)

if "%choice%"=="3" (
    echo.
    echo 🚀 Google Cloud Vision 엔진으로 추출 시작...
    python whatsapp_media_ocr_extractor.py --chat "HVDC 물류팀" --ocr-engine gcv --max-media 10
    goto end
)

if "%choice%"=="4" (
    echo.
    echo 🚀 Naver CLOVA OCR 엔진으로 추출 시작...
    python whatsapp_media_ocr_extractor.py --chat "HVDC 물류팀" --ocr-engine clova --max-media 10
    goto end
)

if "%choice%"=="5" (
    echo.
    echo 🚀 모든 채팅방 자동 추출 시작...
    python whatsapp_media_ocr_extractor.py --auto --max-media 20
    goto end
)

if "%choice%"=="6" (
    echo.
    echo 🚀 업그레이드된 대시보드 실행...
    start http://localhost:8501
    streamlit run whatsapp_media_ocr_dashboard_upgraded.py
    goto end
)

if "%choice%"=="7" (
    echo.
    echo 🧪 테스트 실행...
    python -c "from whatsapp_media_ocr_extractor import MediaOCRProcessor; print('✅ 테스트 성공')"
    goto end
)

if "%choice%"=="8" (
    echo.
    echo 👋 종료합니다.
    exit /b 0
)

echo ❌ 잘못된 선택입니다.
goto end

:end
echo.
echo 🎉 작업 완료!
echo 📁 결과 파일: data/whatsapp_media_ocr_*.json
echo 🌐 대시보드: http://localhost:8501
echo.
pause 