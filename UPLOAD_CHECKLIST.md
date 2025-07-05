# 📋 GitHub 업로드 체크리스트

## 🎯 업로드 대상 파일 (우선순위 순)

### 1단계: 핵심 애플리케이션 파일 ⭐⭐⭐
- [ ] `simplified_whatsapp_app.py` - 포트 8506 (안정 버전)
- [ ] `run_app.py` - 포트 8507 (통합 실행)
- [ ] `whatsapp_executive_dashboard.py` - 포트 8505 (Executive Dashboard)
- [ ] `extract_whatsapp_auto.py` - WhatsApp 자동 추출 RPA

### 2단계: 의존성 및 설정 파일 ⭐⭐
- [ ] `requirements.txt` - 전체 의존성 목록
- [ ] `requirements_simple.txt` - 간단한 의존성 목록
- [ ] `pyproject.toml` - 패키지 설정
- [ ] `.gitignore` - Git 제외 파일 목록

### 3단계: 문서 파일 ⭐⭐
- [ ] `README.md` - 프로젝트 메인 문서 (이미 업로드됨)
- [ ] `PROJECT_SUMMARY.md` - 프로젝트 요약 (이미 업로드됨)
- [ ] `GITHUB_UPDATE_GUIDE.md` - GitHub 업데이트 가이드 (이미 업로드됨)

### 4단계: 모듈 구조 ⭐⭐
- [ ] `macho_gpt/__init__.py` - 메인 모듈
- [ ] `macho_gpt/core/` - 핵심 로직 폴더
- [ ] `macho_gpt/rpa/` - RPA 자동화 폴더
- [ ] `macho_gpt/utils/` - 유틸리티 폴더

### 5단계: 설정 및 템플릿 ⭐
- [ ] `configs/` - 설정 파일 폴더
- [ ] `templates/` - 템플릿 파일 폴더
- [ ] `tests/` - 테스트 파일 폴더

### 6단계: 데이터 파일 (선택사항) ⭐
- [ ] `summaries.json` - 요약 데이터
- [ ] `data/workflow_data.json` - 워크플로우 데이터 (민감 정보 제외)

## ⚠️ 업로드 금지 파일 (보안상 중요)
- [ ] ❌ `auth.json` - WhatsApp 인증 정보
- [ ] ❌ `__pycache__/` - Python 캐시 폴더
- [ ] ❌ `logs/` - 로그 파일 폴더
- [ ] ❌ `temp/` - 임시 파일 폴더

## 🔗 GitHub 업로드 단계별 가이드

### 단계 1: GitHub 저장소 접속
1. 브라우저에서 https://github.com/macho715/HVDC-WHATSAPP 접속
2. 로그인 확인

### 단계 2: 파일 업로드 준비
1. "Add file" 버튼 클릭
2. "Upload files" 선택

### 단계 3: 파일 업로드 (우선순위 순)
1. **핵심 애플리케이션 파일 4개**를 먼저 업로드
2. **의존성 파일 4개**를 두 번째로 업로드
3. **macho_gpt 폴더 전체**를 세 번째로 업로드

### 단계 4: 커밋 메시지 작성
```
feat: Add MACHO-GPT v3.4-mini WhatsApp automation system

- Add simplified_whatsapp_app.py (port 8506 - stable version)
- Add run_app.py (port 8507 - integrated execution)
- Add whatsapp_executive_dashboard.py (port 8505 - executive dashboard)
- Add extract_whatsapp_auto.py (RPA automation)
- Add requirements and configuration files
- Add macho_gpt module structure
- Update project with current operational status

System Status:
- Running services: 3 ports (8505, 8506, 8507)
- Mode: ZERO (safe mode)
- Confidence: 51.0% → Target: 90%+
- Partnership: Samsung C&T Logistics · ADNOC·DSV
```

### 단계 5: 업로드 완료
1. "Commit changes" 버튼 클릭
2. 업로드 확인

## 📊 현재 시스템 상태 요약
- **실행 중인 서비스**: 3개 (포트 8505, 8506, 8507)
- **현재 모드**: ZERO (안전 모드)
- **신뢰도**: 51.0% (목표: 90%+)
- **파트너십**: Samsung C&T Logistics · ADNOC·DSV Partnership
- **프로젝트**: HVDC 프로젝트 통합

## 🔧 업로드 후 확인사항
1. [ ] 모든 핵심 파일이 업로드되었는지 확인
2. [ ] README.md에 현재 상태가 반영되었는지 확인
3. [ ] 보안 파일(auth.json)이 제외되었는지 확인
4. [ ] 의존성 파일들이 정상적으로 업로드되었는지 확인

## 🎯 추천 업로드 순서
1. **1차**: 핵심 애플리케이션 파일 4개
2. **2차**: 의존성 및 설정 파일
3. **3차**: macho_gpt 모듈 구조
4. **4차**: 추가 설정 및 데이터 파일

이 순서대로 업로드하면 각 단계별로 확인하면서 안전하게 진행할 수 있습니다. 