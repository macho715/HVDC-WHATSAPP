# 🚀 GitHub 업로드 가이드 - 웹 인터페이스

## 📋 업로드 순서

### 1단계: 핵심 Python 파일 업로드
1. https://github.com/macho715/HVDC-WHATSAPP 접속
2. "Add file" → "Upload files" 클릭
3. 다음 파일들을 드래그 앤 드롭:

**핵심 애플리케이션 파일:**
- `simplified_whatsapp_app.py` (포트 8506 - 안정 버전)
- `run_app.py` (포트 8507 - 통합 실행)
- `whatsapp_executive_dashboard.py` (포트 8505 - Executive Dashboard)
- `extract_whatsapp_auto.py` (WhatsApp 자동 추출)

### 2단계: 의존성 및 설정 파일
- `requirements.txt` (전체 의존성)
- `requirements_simple.txt` (간단한 의존성)
- `pyproject.toml` (패키지 설정)

### 3단계: 데이터 파일 (선택사항)
- `summaries.json` (요약 데이터)
- `data/` 폴더 (워크플로우 데이터)

## ⚠️ 업로드 제외 파일 (보안상 중요)
- `auth.json` (WhatsApp 인증 정보)
- `__pycache__/` (Python 캐시)
- `logs/` (로그 파일)

## 🔧 커밋 메시지 예시
```
feat: Add MACHO-GPT v3.4-mini WhatsApp automation system

- Add simplified_whatsapp_app.py (port 8506)
- Add run_app.py (port 8507) 
- Add whatsapp_executive_dashboard.py (port 8505)
- Add extract_whatsapp_auto.py (RPA automation)
- Update requirements with all dependencies
- Add macho_gpt module structure
```

## 📊 현재 시스템 상태
- **실행 중인 서비스**: 3개 (포트 8505, 8506, 8507)
- **모드**: ZERO (안전 모드)
- **신뢰도**: 51.0% → 목표 90%
- **상태**: 운영 중

## 🎯 업로드 후 확인사항
1. README.md 최신 업데이트 확인
2. 실행 가능한 앱들 동작 확인
3. 의존성 설치 가이드 업데이트
4. 보안 파일 제외 확인 