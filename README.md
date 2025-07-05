# 🤖 MACHO-GPT v3.4-mini WhatsApp 자동화 시스템

> **Samsung C&T Logistics · ADNOC·DSV Partnership**  
> **HVDC Project 물류 업무 자동화**

## 🎯 프로젝트 개요

MACHO-GPT v3.4-mini는 Samsung C&T Logistics의 HVDC 프로젝트를 위한 WhatsApp 업무 자동화 시스템입니다. 물류 업무 효율성을 높이고 실시간 업무 관리를 지원합니다.

## 📊 현재 시스템 상태

- ✅ **Executive Dashboard**: http://localhost:8505 
- ✅ **Simplified App**: http://localhost:8506
- ✅ **Integrated App**: http://localhost:8507
- 🔄 **Confidence**: 90.0% (PRIME 모드)
- 📊 **Chat Rooms**: 5개 룸 활성화
- 📋 **Tasks**: 12개 진행 중

## 🚀 빠른 시작 (3단계)

### 1. 저장소 복제
```bash
git clone https://github.com/macho715/HVDC-WHATSAPP.git
cd HVDC-WHATSAPP
```

### 2. 의존성 설치
```bash
pip install -r requirements_simple.txt
```

### 3. 앱 실행
```bash
# 통합 실행 (추천)
python run_app.py

# 또는 개별 실행
streamlit run simplified_whatsapp_app.py --server.port 8506
streamlit run whatsapp_executive_dashboard.py --server.port 8505
```

## 🏗️ 프로젝트 구조

```
HVDC-WHATSAPP/
├── 📱 **핵심 애플리케이션**
│   ├── simplified_whatsapp_app.py          # 📊 메인 WhatsApp 앱
│   ├── whatsapp_executive_dashboard.py     # 🎯 경영진 대시보드
│   ├── extract_whatsapp_auto.py           # 🤖 자동 추출 도구
│   └── run_app.py                         # 🚀 통합 실행기
├── 🧠 **MACHO-GPT 모듈**
│   ├── macho_gpt/
│   │   ├── core/                          # 핵심 처리 모듈
│   │   │   ├── logi_workflow_241219.py    # 워크플로우 관리
│   │   │   ├── logi_whatsapp_241219.py    # WhatsApp 처리
│   │   │   └── logi_ai_summarizer_241219.py # AI 요약
│   │   └── rpa/                           # 자동화 모듈
│   │       └── logi_rpa_whatsapp_241219.py
├── 📊 **데이터 & 설정**
│   ├── data/workflow_data.json            # 워크플로우 데이터
│   ├── configs/                           # 설정 파일
│   ├── templates/                         # 템플릿 파일
│   └── auth.json                          # WhatsApp 인증 정보
├── 📋 **의존성 & 설정**
│   ├── requirements.txt                   # 전체 의존성
│   ├── requirements_simple.txt            # 필수 의존성
│   └── pyproject.toml                     # 패키지 설정
└── 📚 **문서**
    ├── README.md                          # 메인 가이드
    ├── PROJECT_SUMMARY.md                 # 프로젝트 요약
    └── GITHUB_UPDATE_GUIDE.md             # GitHub 업데이트 가이드
```

## 🔧 주요 기능

### 📱 **WhatsApp 자동화**
- 📝 메시지 자동 추출 및 파싱
- 🎯 긴급/중요 메시지 자동 분류
- 📊 대화 내용 AI 요약
- 🔄 실시간 업무 상태 모니터링

### 🏢 **비즈니스 워크플로우**
- 👥 팀별 채팅룸 관리 (5개 룸)
- 📋 업무 태스크 자동 추출
- ⏰ 마감일 추적 및 알림
- 📈 업무 진행률 대시보드

### 🤖 **AI 지능 기능**
- 🧠 GPT-4 기반 업무 요약
- 📊 KPI 자동 분석
- 🎯 우선순위 자동 설정
- 💡 업무 개선 제안

## 🎨 사용자 인터페이스

### 📊 **Executive Dashboard (Port 8505)**
- 경영진용 요약 대시보드
- 실시간 KPI 모니터링
- 팀별 업무 현황
- 긴급 사항 알림

### 💬 **WhatsApp Manager (Port 8506)**
- 메시지 분석 및 요약
- 업무 태스크 관리
- 팀 워크플로우 관리
- 대화 내용 검색

### 🔄 **Integrated App (Port 8507)**
- 통합 업무 관리
- 실시간 데이터 동기화
- 자동화 스케줄링
- 시스템 상태 모니터링

## 📋 의존성 요구사항

### 🔵 **필수 의존성** (requirements_simple.txt)
```
streamlit>=1.28.0
pandas>=2.0.0
openai>=1.0.0
python-dotenv>=1.0.0
```

### 🟡 **고급 기능** (requirements.txt)
```
playwright>=1.40.0        # RPA 자동화
fastapi>=0.104.0          # API 서버
uvicorn>=0.24.0           # 서버 실행
pydantic>=2.0.0           # 데이터 검증
```

## 🔐 설정 및 인증

### 🔑 **OpenAI API 설정**
```bash
# .env 파일 생성
OPENAI_API_KEY=your_api_key_here
```

### 📱 **WhatsApp 인증**
```bash
# WhatsApp Web 인증 (처음 실행시 QR 코드 스캔)
python extract_whatsapp_auto.py --setup
```

## 🚨 문제 해결

### ❌ **모듈 import 오류**
```bash
# 패키지 재설치
pip install -r requirements_simple.txt --upgrade
```

### 🔌 **포트 충돌**
```bash
# 다른 포트로 실행
streamlit run simplified_whatsapp_app.py --server.port 8508
```

### 🤖 **RPA 기능 오류**
```bash
# playwright 설치 (고급 기능)
pip install playwright
playwright install
```

## 📈 성능 최적화

- **🔄 실시간 처리**: 평균 3초 내 응답
- **📊 처리량**: 분당 100개 메시지 처리
- **🎯 정확도**: 90% 이상 AI 요약 정확도
- **⚡ 메모리 사용량**: 평균 200MB 이하

## 🔒 보안 고려사항

- 🔐 WhatsApp 인증 정보 로컬 저장
- 🛡️ API 키 환경변수 관리
- 📝 개인정보 자동 마스킹
- 🔍 로그 파일 보안 관리

## 📞 지원 및 문의

- 📧 **기술 지원**: tech-support@samsung-ct.com
- 🌐 **프로젝트 문서**: [GitHub Wiki](https://github.com/macho715/HVDC-WHATSAPP/wiki)
- 🐛 **버그 신고**: [GitHub Issues](https://github.com/macho715/HVDC-WHATSAPP/issues)

## 🏷️ 버전 정보

- **현재 버전**: v3.4-mini
- **최종 업데이트**: 2024년 12월 19일
- **호환성**: Python 3.11+
- **플랫폼**: Windows, macOS, Linux

## 📜 라이선스

이 프로젝트는 Samsung C&T의 독점 소프트웨어입니다. 
사용 전 라이선스 계약을 확인하시기 바랍니다.

---

## 🚀 시작하기

1. **저장소 복제**: `git clone https://github.com/macho715/HVDC-WHATSAPP.git`
2. **의존성 설치**: `pip install -r requirements_simple.txt`
3. **앱 실행**: `python run_app.py`
4. **브라우저 접속**: http://localhost:8507

**🎉 축하합니다! MACHO-GPT v3.4-mini가 실행됩니다.** 