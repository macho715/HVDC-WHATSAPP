# 🚀 MACHO-GPT v3.4-mini 빠른 시작 가이드

## 📋 프로젝트 상태 요약
**MACHO-GPT v3.4-mini WhatsApp 자동화 시스템**이 GitHub에 성공적으로 업로드되었습니다. 다음 가이드를 따라 빠르게 시작하세요.

### ✅ 시스템 정보
- **버전**: v3.4-mini
- **GitHub**: [HVDC-WHATSAPP](https://github.com/macho715/HVDC-WHATSAPP)
- **프로젝트**: Samsung C&T Logistics · HVDC 물류 자동화
- **상태**: ✅ 프로덕션 준비 완료

## 🚀 빠른 시작 (3단계)

### 1단계: 저장소 복제
```bash
git clone https://github.com/macho715/HVDC-WHATSAPP.git
cd HVDC-WHATSAPP
```

### 2단계: 의존성 설치
```bash
# 최소 의존성 설치 (추천)
pip install -r requirements_simple.txt

# 또는 전체 기능 설치
pip install -r requirements.txt
```

### 3단계: 앱 실행
```bash
# 통합 실행기 사용 (가장 쉬움)
python run_app.py

# 또는 개별 앱 실행
streamlit run simplified_whatsapp_app.py --server.port 8506
streamlit run whatsapp_executive_dashboard.py --server.port 8505
```

## 🎯 실행 방법 상세

### 방법 1: 통합 실행기 (권장)
```bash
python run_app.py
```
- 모든 앱을 자동으로 실행
- 포트 충돌 자동 해결
- 브라우저 자동 열기

### 방법 2: 개별 앱 실행
```bash
# Executive Dashboard (경영진용)
streamlit run whatsapp_executive_dashboard.py --server.port 8505

# Simplified App (일반 사용자용)
streamlit run simplified_whatsapp_app.py --server.port 8506
```

### 방법 3: WhatsApp 자동화
```bash
# WhatsApp 인증 설정
python extract_whatsapp_auto.py --setup

# 자동 추출 실행
python extract_whatsapp_auto.py --run
```

## 🔧 고급 설정

### OpenAI API 설정
```bash
# .env 파일 생성
echo OPENAI_API_KEY=your_api_key_here > .env

# 또는 환경변수 설정
set OPENAI_API_KEY=your_api_key_here  # Windows
export OPENAI_API_KEY=your_api_key_here  # Linux/Mac
```

### WhatsApp RPA 설정 (선택사항)
```bash
# Playwright 설치 (고급 기능)
pip install playwright playwright-stealth
python -m playwright install
```

### React 프론트엔드 실행 (선택사항)
```bash
cd react_frontend
npm install
npm start
```

## 📊 접속 URL

| 애플리케이션 | URL | 설명 |
|------------|-----|------|
| **Executive Dashboard** | http://localhost:8505 | 경영진용 종합 대시보드 |
| **Simplified App** | http://localhost:8506 | 일반 사용자용 WhatsApp 앱 |
| **Integrated App** | http://localhost:8507 | 통합 관리 시스템 |
| **React Frontend** | http://localhost:3000 | 모던 웹 인터페이스 |

## 🔍 문제 해결

### 1. 의존성 오류
```bash
# 기본 패키지 재설치
pip install streamlit pandas openai --upgrade

# 가상환경 사용 (권장)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements_simple.txt
```

### 2. 포트 충돌
```bash
# 사용 중인 포트 확인
netstat -ano | findstr :8505
netstat -ano | findstr :8506

# 프로세스 종료
taskkill /PID [PID번호] /F

# 다른 포트 사용
streamlit run simplified_whatsapp_app.py --server.port 8508
```

### 3. 모듈 import 오류
```bash
# Python 경로 확인
python -c "import sys; print(sys.path)"

# 패키지 재설치
pip uninstall streamlit
pip install streamlit
```

### 4. WhatsApp 인증 문제
```bash
# 인증 정보 재설정
python extract_whatsapp_auto.py --setup

# 브라우저 캐시 삭제
python extract_whatsapp_auto.py --clean
```

## 🚨 응급 실행 (최소 설정)

패키지 설치 문제가 있을 경우:
```bash
# Python 기본 라이브러리만 사용
python -c "
import json
from datetime import datetime
print('🤖 MACHO-GPT v3.4-mini 기본 실행 테스트')
print(f'📅 현재 시각: {datetime.now()}')
print('✅ Python 환경 정상 작동')
"

# Streamlit 없이 기본 실행
python simplified_whatsapp_app.py
```

## 📋 시스템 요구사항

### 최소 요구사항
- **Python**: 3.8+
- **RAM**: 2GB 이상
- **저장공간**: 500MB 이상
- **네트워크**: 인터넷 연결 (API 사용시)

### 권장 사양
- **Python**: 3.11+
- **RAM**: 4GB 이상
- **저장공간**: 1GB 이상
- **브라우저**: Chrome/Edge 최신 버전

## 🔧 추천 실행 시퀀스

### 첫 실행시
```bash
# 1. 저장소 복제
git clone https://github.com/macho715/HVDC-WHATSAPP.git
cd HVDC-WHATSAPP

# 2. 가상환경 생성 (권장)
python -m venv venv
venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements_simple.txt

# 4. 앱 실행
python run_app.py
```

### 정기 사용시
```bash
# 1. 가상환경 활성화
venv\Scripts\activate

# 2. 업데이트 확인
git pull origin main

# 3. 앱 실행
python run_app.py
```

## 🎯 성능 최적화

### 메모리 최적화
```bash
# 메모리 사용량 확인
python -c "
import psutil
print(f'사용 가능한 메모리: {psutil.virtual_memory().available / (1024**3):.1f} GB')
"
```

### 캐시 관리
```bash
# Streamlit 캐시 정리
streamlit cache clear

# 임시 파일 정리
python -c "
import tempfile, shutil
temp_dir = tempfile.gettempdir()
print(f'임시 디렉토리: {temp_dir}')
"
```

## 📞 도움말

### 자주 묻는 질문
1. **Q: 앱이 시작되지 않아요**
   - A: `pip install streamlit --upgrade` 실행 후 재시도

2. **Q: WhatsApp이 연결되지 않아요**
   - A: `python extract_whatsapp_auto.py --setup` 실행

3. **Q: 포트 8505가 사용 중이에요**
   - A: `streamlit run simplified_whatsapp_app.py --server.port 8508` 사용

### 추가 지원
- **GitHub Issues**: [문제 신고](https://github.com/macho715/HVDC-WHATSAPP/issues)
- **문서**: [프로젝트 Wiki](https://github.com/macho715/HVDC-WHATSAPP/wiki)
- **업데이트**: [Release Notes](https://github.com/macho715/HVDC-WHATSAPP/releases)

---

## 🎉 성공적인 실행 확인

앱이 정상적으로 실행되면 다음 메시지가 표시됩니다:
```
🤖 MACHO-GPT v3.4-mini 실행 중
📊 Dashboard: http://localhost:8505
💬 WhatsApp App: http://localhost:8506
🔄 시스템 상태: ✅ 정상
```

**🚀 축하합니다! MACHO-GPT v3.4-mini가 성공적으로 실행되었습니다.** 