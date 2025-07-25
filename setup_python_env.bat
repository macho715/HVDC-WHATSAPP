@echo off
echo 🔧 Python 환경 설정 스크립트
echo ================================

echo.
echo 1. 현재 PATH 확인...
echo %PATH%

echo.
echo 2. Python 설치 경로 찾기...
for /f "tokens=*" %%i in ('dir /b /s "C:\Python*" 2^>nul') do (
    if exist "%%i\python.exe" (
        echo 발견: %%i
        set PYTHON_PATH=%%i
        goto :found_python
    )
)

for /f "tokens=*" %%i in ('dir /b /s "C:\Users\%USERNAME%\AppData\Local\Programs\Python*" 2^>nul') do (
    if exist "%%i\python.exe" (
        echo 발견: %%i
        set PYTHON_PATH=%%i
        goto :found_python
    )
)

echo ❌ Python을 찾을 수 없습니다.
echo Python을 설치하거나 PATH를 수동으로 설정해주세요.
pause
exit /b 1

:found_python
echo.
echo 3. PATH에 Python 경로 추가...
setx PATH "%PATH%;%PYTHON_PATH%;%PYTHON_PATH%\Scripts"

echo.
echo 4. 환경변수 설정 확인...
echo PYTHON_PATH=%PYTHON_PATH%
echo.

echo ✅ Python 환경 설정 완료!
echo 새 터미널을 열고 'python --version'을 실행해보세요.
pause 