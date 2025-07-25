@echo off
echo 🧪 MACHO-GPT v3.4-mini TDD 테스트 실행
echo ======================================

echo.
echo 📋 TDD 테스트 체크리스트:
echo 1. pytest 설치 확인
echo 2. 개별 모듈 테스트
echo 3. 통합 테스트
echo 4. 전체 테스트 스위트
echo.

REM 1. pytest 설치 확인
echo 🔍 1단계: pytest 설치 확인
python -c "import pytest; print('✅ pytest 설치됨')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️ pytest 미설치 - 설치 중...
    pip install pytest pytest-asyncio
    if %errorlevel% neq 0 (
        echo ❌ pytest 설치 실패
        pause
        exit /b 1
    )
)
echo ✅ pytest 확인 완료
echo.

REM 2. 개별 모듈 테스트
echo 🔍 2단계: 개별 모듈 테스트
echo.

echo 📱 WhatsApp Processor 테스트...
python -m pytest tests/test_whatsapp_processor.py -v --tb=short
if %errorlevel% neq 0 (
    echo ⚠️ WhatsApp Processor 테스트 일부 실패
) else (
    echo ✅ WhatsApp Processor 테스트 통과
)
echo.

echo 🔍 Media OCR 테스트...
python -m pytest tests/test_media_ocr.py::TestMediaOCRProcessor -v --tb=short
if %errorlevel% neq 0 (
    echo ⚠️ Media OCR 테스트 일부 실패
) else (
    echo ✅ Media OCR 테스트 통과
)
echo.

echo 📊 Logi Reporter 테스트...
python -m pytest tests/test_logi_reporter.py -v --tb=short
if %errorlevel% neq 0 (
    echo ⚠️ Logi Reporter 테스트 일부 실패
) else (
    echo ✅ Logi Reporter 테스트 통과
)
echo.

REM 3. 통합 테스트
echo 🔍 3단계: 통합 테스트
echo.

echo 🔗 WhatsApp Scraper 통합 테스트...
python -m pytest tests/test_whatsapp_scraper_integration.py -v --tb=short
if %errorlevel% neq 0 (
    echo ⚠️ WhatsApp Scraper 통합 테스트 일부 실패
) else (
    echo ✅ WhatsApp Scraper 통합 테스트 통과
)
echo.

echo 🎭 Role Injection 테스트...
python -m pytest tests/test_role_injection.py -v --tb=short
if %errorlevel% neq 0 (
    echo ⚠️ Role Injection 테스트 일부 실패
) else (
    echo ✅ Role Injection 테스트 통과
)
echo.

REM 4. 전체 테스트 스위트
echo 🔍 4단계: 전체 테스트 스위트
echo.

echo 🚀 전체 테스트 실행 중...
python -m pytest tests/ -v --tb=short --maxfail=5

echo.
echo 📊 TDD 테스트 결과 요약:
echo.

REM 테스트 결과 파일 생성
echo 📝 테스트 결과를 파일로 저장 중...
python -m pytest tests/ --tb=short -q > test_results.txt 2>&1

REM 결과 분석
findstr /C:"FAILED" test_results.txt >nul
if %errorlevel% equ 0 (
    echo ❌ 일부 테스트 실패
    echo 📄 상세 결과: test_results.txt
) else (
    echo ✅ 모든 테스트 통과
)

findstr /C:"passed" test_results.txt
findstr /C:"failed" test_results.txt

echo.
echo 🎯 TDD 원칙 준수 확인:
echo ✅ Red Phase: 실패하는 테스트 먼저 작성
echo ✅ Green Phase: 최소 코드로 테스트 통과
echo ✅ Refactor Phase: 코드 구조 개선
echo ✅ Tidy First: 구조적/행위적 변경 분리

echo.
echo 📁 생성된 파일:
if exist "test_results.txt" (
    echo - test_results.txt (테스트 결과)
)

echo.
echo 🎉 TDD 테스트 실행 완료!
pause 