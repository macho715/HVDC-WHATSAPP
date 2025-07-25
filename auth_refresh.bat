@echo off
echo 🔄 WhatsApp 세션 자동 갱신 스크립트
echo ======================================

REM 현재 날짜 확인
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "datestamp=%YYYY%-%MM%-%DD%"
set "timestamp=%HH%:%Min%:%Sec%"

echo 📅 실행 시간: %datestamp% %timestamp%

REM 기존 auth.json 백업
if exist "auth_backups\auth.json" (
    echo 📦 기존 세션 백업 중...
    copy "auth_backups\auth.json" "auth_backups\auth_backup_%datestamp%_%HH%%Min%%Sec%.json" >nul
    echo ✅ 백업 완료: auth_backup_%datestamp%_%HH%%Min%%Sec%.json
) else (
    echo ℹ️ 기존 세션 파일이 없습니다.
)

REM 새 세션 생성
echo 🔐 새 WhatsApp 세션 생성 중...
echo.
echo 📱 QR 코드를 스캔해주세요...
echo.

python auth_setup.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ WhatsApp 세션 갱신 완료!
    echo 📁 새 세션 파일: auth_backups\auth.json
) else (
    echo.
    echo ❌ 세션 갱신 실패
    echo 🔄 백업 파일에서 복원 중...
    if exist "auth_backups\auth_backup_%datestamp%_%HH%%Min%%Sec%.json" (
        copy "auth_backups\auth_backup_%datestamp%_%HH%%Min%%Sec%.json" "auth_backups\auth.json" >nul
        echo ✅ 백업에서 복원 완료
    )
)

echo.
echo 📊 세션 상태 확인...
if exist "auth_backups\auth.json" (
    echo ✅ auth.json 파일 존재
    for %%A in ("auth_backups\auth.json") do echo 📏 파일 크기: %%~zA bytes
) else (
    echo ❌ auth.json 파일 없음
)

echo.
echo 🔄 세션 갱신 완료
pause 