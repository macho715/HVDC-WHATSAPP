# 🔧 시스템 정리 및 Git 업로드 복구 가이드

## 🚨 현재 문제 상황
- 다중 Streamlit 프로세스 실행 중 (포트 8505, 8506, 8507)
- 삭제된 파일(`integration_api.py`) 참조 오류
- Git 미설치로 인한 터미널 명령어 실행 실패
- PowerShell 실행 정책 제한

## 🔄 단계별 해결 방법

### 1단계: 실행 중인 프로세스 정리
```powershell
# PowerShell 관리자 권한으로 실행
# 포트 사용 중인 프로세스 확인
netstat -ano | findstr :8505
netstat -ano | findstr :8506  
netstat -ano | findstr :8507

# 프로세스 종료 (PID 확인 후)
taskkill /PID [PID번호] /F
```

### 2단계: Python 프로세스 완전 정리
```powershell
# 모든 Python 프로세스 종료
taskkill /IM python.exe /F
taskkill /IM streamlit.exe /F

# 프로세스 확인
tasklist | findstr python
```

### 3단계: Git 설치
```powershell
# winget으로 Git 설치
winget install --id Git.Git -e --source winget

# 또는 직접 다운로드
# https://git-scm.com/download/win
```

### 4단계: PowerShell 실행 정책 변경
```powershell
# 관리자 권한으로 PowerShell 실행
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 또는 우회 실행
powershell -ExecutionPolicy Bypass -File "script.ps1"
```

### 5단계: 캐시 정리
```powershell
# Python 캐시 정리
Remove-Item -Recurse -Force __pycache__
Remove-Item -Recurse -Force .streamlit/cache

# 임시 파일 정리
Remove-Item -Recurse -Force temp/
```

## 🎯 권장 업로드 순서

### A. 즉시 실행 (웹 브라우저 사용)
1. **GitHub 웹 인터페이스** 사용
2. **핵심 4개 파일** 먼저 업로드
3. **macho_gpt 모듈** 폴더 업로드
4. **의존성 파일** 업로드

### B. 시스템 정리 후 Git 사용
1. **모든 프로세스 종료**
2. **Git 설치 및 설정**
3. **자동 스크립트 실행**
4. **GitHub 푸시**

## 🔧 추천 명령어 실행 순서

```bash
# 1. 프로세스 정리
Ctrl + C (실행 중인 앱들 종료)

# 2. 새 터미널 세션 시작
# 새 PowerShell 창 열기

# 3. Git 설치 확인
git --version

# 4. 업로드 스크립트 실행
python git_direct_upload.py
```

## ⚠️ 주의사항
- **auth.json** 파일은 업로드하지 않음 (보안)
- **__pycache__** 폴더 제외
- **logs/** 폴더 제외
- **temp/** 폴더 제외

## 🎉 성공 기준
- ✅ GitHub에 핵심 4개 앱 파일 업로드
- ✅ macho_gpt 모듈 구조 업로드
- ✅ 의존성 파일 업로드
- ✅ 보안 파일 제외 확인 