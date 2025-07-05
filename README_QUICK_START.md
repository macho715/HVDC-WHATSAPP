# 🚀 MACHO-GPT v3.4-mini 빠른 시작 가이드

## 📋 현재 상황 요약
터미널에서 여러 ModuleNotFoundError가 발생하고 있습니다. 이를 해결하기 위해 다음과 같은 작업을 완료했습니다:

### ✅ 완료된 수정사항
1. **Graceful Import 적용** - `macho_gpt/__init__.py` 수정
2. **Pyright 설정** - `pyproject.toml` 생성 ([Microsoft Pyright 문서](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportMissingImports) 참고)
3. **Simplified App 생성** - 의존성 문제 없는 `simplified_whatsapp_app.py`
4. **통합 실행 스크립트** - `fix_and_run.py`

## 🔧 실행 방법

### 방법 1: 간단한 모드 (권장)
```bash
# 최소 패키지만 설치
pip install streamlit

# 간단한 앱 실행
streamlit run simplified_whatsapp_app.py
```

### 방법 2: 전체 패키지 설치
```bash
# 모든 패키지 설치 (순서대로)
pip install streamlit openai pandas
pip install playwright fastapi uvicorn pydantic python-multipart
pip install playwright-stealth

# Playwright 브라우저 설치
python -m playwright install

# 전체 앱 실행
streamlit run whatsapp_summary_app.py --server.port 8505
```

### 방법 3: 통합 스크립트 사용
```bash
# 모든 문제를 자동으로 해결하는 스크립트
python fix_and_run.py
```

## 🔍 문제 해결

### ModuleNotFoundError 발생시
1. **playwright 오류**: `pip install playwright && python -m playwright install`
2. **fastapi 오류**: `pip install fastapi uvicorn`
3. **MACHO-GPT 모듈 오류**: `simplified_whatsapp_app.py` 사용

### AttributeError: 'str' object has no attribute 'value'
1. 기존 데이터 삭제: `rm data/workflow_data.json`
2. 앱 재시작

### 포트 충돌 오류
```bash
# 프로세스 확인 및 종료
netstat -ano | findstr :8505
taskkill /PID [PID번호] /F

# 다른 포트 사용
streamlit run simplified_whatsapp_app.py --server.port 8506
```

## 📊 기능별 실행 상태

| 기능 | 필수 패키지 | 상태 | 대안 |
|------|-------------|------|------|
| 기본 대시보드 | streamlit | ✅ | - |
| AI 요약 | openai | ⚠️ | Mock 요약 |
| 워크플로우 | macho_gpt | ⚠️ | Mock 데이터 |
| WhatsApp RPA | playwright | ❌ | 수동 입력 |
| FastAPI | fastapi | ❌ | Streamlit만 사용 |

## 🎯 권장 실행 단계

### 1단계: 기본 앱 테스트
```bash
pip install streamlit
streamlit run simplified_whatsapp_app.py
```
→ http://localhost:8501 접속

### 2단계: OpenAI 연동 (선택)
```bash
# OpenAI API 키 설정
set OPENAI_API_KEY=your_api_key_here

# 또는 환경변수 파일 생성
echo OPENAI_API_KEY=your_api_key_here > .env
```

### 3단계: WhatsApp 자동화 (선택)
```bash
pip install playwright playwright-stealth
python -m playwright install
python extract_whatsapp_auto.py --setup
```

## 🚨 응급 실행 방법

패키지 설치가 안 되는 경우:
```bash
# Python 환경 확인
python --version
pip --version

# 기본 라이브러리만으로 실행
python -c "
import json
from datetime import datetime
print('MACHO-GPT v3.4-mini 기본 실행 테스트')
print(f'현재 시각: {datetime.now()}')
print('✅ Python 환경 정상')
"
```

## 📱 접속 URL
- **Simplified App**: http://localhost:8501
- **Full App**: http://localhost:8505  
- **FastAPI Docs**: http://localhost:8503/docs

## 🔧 추천 명령어 시퀀스
```bash
# 1. 환경 확인
python --version

# 2. 기본 패키지 설치
pip install streamlit

# 3. 앱 실행
streamlit run simplified_whatsapp_app.py

# 4. WhatsApp 자동화 (선택)
python extract_whatsapp_auto.py --setup
python extract_whatsapp_auto.py
```

---
💡 **팁**: 문제가 계속 발생하면 `simplified_whatsapp_app.py`를 사용하세요. 이 버전은 모든 의존성 문제를 gracefully 처리합니다. 