# 🤖 MACHO-GPT v3.4-mini WhatsApp 자동화 시스템

**Samsung C&T Logistics · HVDC Project**  
**ADNOC·DSV Partnership**

WhatsApp 채팅 내용을 자동으로 추출하고 AI 요약을 생성하는 지능형 물류 대시보드 시스템입니다.

## 🎯 **현재 실행 중인 앱들**

### ⭐ **Executive Dashboard** (포트 8505) - 추천
- **파일**: `whatsapp_executive_dashboard.py`
- **스타일**: Discord 스타일 UI
- **기능**: Executive Summary + Bullet To-Do's
- **접속**: http://localhost:8505

### 🔧 **Simplified App** (포트 8506) - 안정 버전
- **파일**: `simplified_whatsapp_app.py`
- **스타일**: 기본 Streamlit UI
- **기능**: 기본 요약 + 안정적 실행
- **접속**: http://localhost:8506

### 🚀 **통합 실행** (포트 8507) - 원클릭
- **파일**: `run_app.py`
- **스타일**: 자동 설정 + 데이터 정리
- **기능**: 원클릭 실행 + 통합 대시보드
- **접속**: http://localhost:8507

---

## 🚀 시스템 특징

### 📊 **핵심 기능**
- **Executive Summary**: DSV 팀 물류 작업 요약
- **Bullet To-Do's**: 10개 주요 액션 아이템 자동 생성
- **AI 요약**: OpenAI GPT-4o 기반 지능형 대화 분석
- **자동화**: Playwright RPA를 통한 WhatsApp Web 자동 추출
- **실시간 모니터링**: 시스템 상태 및 신뢰도 추적

### 🔧 **MACHO-GPT v3.4-mini 통합**
- **6개 모드**: PRIME|ORACLE|ZERO|LATTICE|RHYTHM|COST-GUARD
- **신뢰도 관리**: ≥0.90 신뢰도 보장 (현재 51.0%)
- **자동 트리거**: KPI 기반 자동 모드 전환
- **Fail-safe**: 오류 시 자동 ZERO 모드 전환
- **물류 특화**: 컨테이너 배송, ADNOC 검사, 문서 준비 등

---

## 📁 **현재 프로젝트 구조**

```
whatsapp/
├── 🎯 핵심 실행 파일
│   ├── whatsapp_executive_dashboard.py  # ⭐ Executive Dashboard (포트 8505)
│   ├── simplified_whatsapp_app.py       # 🔧 Simplified App (포트 8506)
│   ├── run_app.py                       # 🚀 통합 실행 (포트 8507)
│   └── extract_whatsapp_auto.py         # 🤖 WhatsApp 자동화 + RPA
│
├── 📋 프로젝트 문서
│   ├── README.md                        # 📖 프로젝트 설명서
│   ├── START_HERE.md                    # 🚀 빠른 시작 가이드
│   ├── PROJECT_SUMMARY.md               # 📊 프로젝트 요약
│   ├── GITHUB_UPDATE_GUIDE.md           # 🔧 GitHub 업로드 가이드
│   └── UPLOAD_NOW.md                    # ⚡ 즉시 업로드 방법
│
├── 🔧 시스템 설정
│   ├── requirements.txt                 # 📦 Python 의존성
│   ├── requirements_simple.txt          # 📦 최소 의존성
│   ├── .gitignore                       # 🔐 보안 파일 제외
│   └── pyproject.toml                   # ⚙️ 프로젝트 설정
│
├── 🤖 MACHO-GPT 모듈
│   ├── macho_gpt/
│   │   ├── __init__.py                  # 모듈 초기화
│   │   ├── core/
│   │   │   ├── logi_whatsapp_241219.py  # WhatsApp 메시지 처리
│   │   │   ├── logi_workflow_241219.py  # 워크플로우 관리
│   │   │   └── logi_ai_summarizer_241219.py  # AI 요약 엔진
│   │   ├── rpa/
│   │   │   └── logi_rpa_whatsapp_241219.py  # RPA 자동화
│   │   └── utils/
│   │       └── logi_logger_241219.py    # 로깅 시스템
│
├── 📊 데이터 및 설정
│   ├── data/
│   │   └── workflow_data.json           # 워크플로우 데이터
│   ├── configs/
│   │   └── config_prime_dev.yaml        # 설정 파일
│   ├── templates/
│   │   └── template_whatsapp_v1.json    # WhatsApp 템플릿
│   └── .streamlit/
│       └── config.toml                  # Streamlit 설정
│
├── 🧪 테스트 및 로그
│   ├── tests/                           # 테스트 파일
│   ├── logs/                           # 로그 파일
│   └── reports/                        # 보고서 파일
│
└── 📱 React 프론트엔드 (옵션)
    └── react_frontend/
        ├── src/components/
        ├── package.json
        └── README.md
```

---

## 🛠️ **빠른 설치 및 실행**

### ⚡ **즉시 실행 (추천)**

```bash
# 1. 프로젝트 다운로드
git clone https://github.com/macho715/HVDC-WHATSAPP.git
cd HVDC-WHATSAPP

# 2. 기본 의존성 설치
pip install -r requirements_simple.txt

# 3. 즉시 실행
python run_app.py
# 브라우저: http://localhost:8507
```

### 🔧 **전체 기능 설치**

```bash
# 전체 의존성 설치 (선택사항)
pip install -r requirements.txt

# Playwright 브라우저 설치 (RPA 기능용)
playwright install chromium

# Executive Dashboard 실행
streamlit run whatsapp_executive_dashboard.py --server.port 8505
# 브라우저: http://localhost:8505
```

### 🎯 **현재 실행 상태**

**✅ 실행 중인 앱들:**
- **포트 8505**: Executive Dashboard (Discord 스타일)
- **포트 8506**: Simplified App (안정 버전)
- **포트 8507**: 통합 실행 (원클릭)

#### React 환경 (선택)
```bash
# Node.js 설치 확인 (v18+ 권장)
node --version
npm --version

# React 의존성 설치
cd react_frontend
npm install

# Tailwind CSS 빌드
npm run build:css

# 개발 서버 테스트
npm start
```

### 2. OpenAI API 키 설정

```bash
# 환경변수 설정
export OPENAI_API_KEY="your-api-key-here"

# 또는 Streamlit secrets 사용
mkdir .streamlit
echo 'OPENAI_API_KEY = "your-api-key-here"' > .streamlit/secrets.toml
```

### 3. 디렉터리 생성

```bash
mkdir -p logs data templates
```

---

## 🚀 **실행 방법**

### ⭐ **방법 1: Executive Dashboard (추천)**

```bash
# Discord 스타일 대시보드 실행
streamlit run whatsapp_executive_dashboard.py --server.port 8505

# 브라우저 접속: http://localhost:8505
```

**특징:**
- **Executive Summary**: DSV 팀 물류 작업 요약
- **Bullet To-Do's**: 10개 주요 액션 아이템
- **Discord 스타일 UI**: 사이드바 + 메인 콘텐츠
- **실시간 모니터링**: 시스템 신뢰도 51.0%

### 🔧 **방법 2: Simplified App (안정)**

```bash
# 기본 기능 중심 안정 버전
streamlit run simplified_whatsapp_app.py --server.port 8506

# 브라우저 접속: http://localhost:8506
```

**특징:**
- **Mock 데이터 지원**: 의존성 없이 실행 가능
- **기본 요약 기능**: AI 요약 + 워크플로우 관리
- **안정적 실행**: 오류 시 graceful degradation

### 🚀 **방법 3: 통합 실행 (원클릭)**

```bash
# 원클릭 실행 + 자동 데이터 정리
python run_app.py

# 브라우저 접속: http://localhost:8507
```

**특징:**
- **자동 설정**: 데이터 정리 + 의존성 확인
- **통합 대시보드**: 모든 기능 한 번에
- **원클릭 실행**: 복잡한 설정 불필요

### 🤖 **WhatsApp 자동화**

```bash
# 최초 설정 (QR 코드 스캔)
python extract_whatsapp_auto.py --setup

# 자동 추출 실행
python extract_whatsapp_auto.py --run

# 스케줄링 설정
python extract_whatsapp_auto.py --schedule daily
```

---

## ⚙️ 설정 파일

### `configs/config_prime_dev.yaml`

```yaml
# 주요 설정 항목
whatsapp:
  chat_title: "MR.CHA 전용"  # 추출할 대화방 이름
  extraction_hours: 24       # 추출 시간 범위

rpa:
  headless: false           # 개발 시 false, 운영 시 true
  timeout: 30000           # 타임아웃 (ms)
  retry_attempts: 3        # 재시도 횟수

scheduler:
  extraction_time: "18:00"  # 매일 추출 시간
  enabled: true
```

---

## 📅 자동화 스케줄링

### Linux/macOS CRON 설정

```bash
# crontab 편집
crontab -e

# 매일 오후 6시 실행
0 18 * * * cd /path/to/whatsapp && python extract_whatsapp_rpa.py --scheduled
```

### Windows 작업 스케줄러

1. **작업 스케줄러** 실행
2. **기본 작업 만들기** 선택
3. **작업 이름**: WhatsApp 자동화
4. **트리거**: 매일 18:00
5. **동작**: 프로그램 시작
   - **프로그램**: `python`
   - **인수**: `extract_whatsapp_rpa.py --scheduled`
   - **시작 위치**: 프로젝트 폴더 경로

---

## 🎯 사용 시나리오

### 시나리오 1: 수동 요약
1. Streamlit 앱 실행
2. WhatsApp 대화 복사/붙여넣기
3. AI 요약 생성 및 확인
4. 긴급/중요 사항 처리

### 시나리오 2: 자동화 (추천)
1. 최초 1회 WhatsApp 로그인 (QR 코드)
2. 스케줄러 등록 (매일 18:00)
3. 자동 추출 → 요약 → DB 저장
4. 다음날 아침 대시보드에서 확인

### 시나리오 3: 팀 운영
1. 공유 드라이브에 프로젝트 배치
2. 팀 구성원별 대화방 설정
3. 순번제 또는 대표자 운영
4. 일일 브리핑 자동 생성

---

## 🔧 MACHO-GPT 명령어

### 기본 명령어
```bash
/logi-master summarize          # 요약 생성
/switch_mode LATTICE           # 모드 전환
/visualize_data --type=timeline # 데이터 시각화
/kpi_monitor message_analysis  # KPI 모니터링
```

### 자동 트리거
- **긴급 메시지 5개 이상**: `/alert_system urgent_threshold_exceeded`
- **참가자 10명 이상**: `/team_coordination large_group_detected`
- **신뢰도 0.90 미만**: `/switch_mode ZERO`

---

## 🧪 테스트

### 단위 테스트
```bash
# 메시지 파싱 테스트
python -m pytest tests/test_whatsapp_processor.py

# RPA 모듈 테스트
python -m pytest tests/test_rpa_extractor.py
```

### 통합 테스트
```bash
# 전체 파이프라인 테스트
python -m pytest tests/test_integration.py

# 또는 MACHO-GPT 명령어 사용
# Ctrl+Shift+F 0  # 전체 파이프라인 실행
```

---

## 📊 KPI 및 모니터링

### 핵심 KPI
- **추출 신뢰도**: ≥0.90
- **처리 시간**: <3초/KB
- **긴급 분류 정확도**: ≥92%
- **자동화 성공률**: ≥95%

### 모니터링 파일
- `logs/whatsapp_rpa.log`: RPA 실행 로그
- `logs/automation_log_YYYYMMDD.json`: 일일 자동화 결과
- `summaries.json`: 요약 데이터베이스

---

## 🔒 보안 및 규정 준수

### 데이터 보호
- **PII 보호**: 개인정보 자동 스크리닝
- **NDA 준수**: 민감 정보 처리 규정
- **로컬 저장**: 데이터 외부 유출 방지

### 인증 관리
- **세션 저장**: `auth.json` 파일 보안 관리
- **API 키 보호**: 환경변수 또는 secrets 사용
- **접근 제어**: 팀 단위 권한 관리

---

## 🚨 문제해결

### 일반적인 오류

**1. QR 코드 스캔 오류**
```bash
# 인증 파일 삭제 후 재시도
rm auth.json
python extract_whatsapp_rpa.py --mode PRIME
```

**2. OpenAI API 오류**
```bash
# API 키 확인
echo $OPENAI_API_KEY
# 또는 secrets 파일 확인
cat .streamlit/secrets.toml
```

**3. 메시지 추출 실패**
```bash
# 로그 확인
tail -f logs/whatsapp_rpa.log
# 수동 모드로 전환
python extract_whatsapp_rpa.py --mode ZERO
```

### 모드별 대응

| 모드 | 문제 상황 | 해결 방법 |
|------|----------|----------|
| PRIME | 일반 오류 | 재시도 (3회) |
| ORACLE | 데이터 검증 실패 | 수동 확인 |
| LATTICE | OCR 신뢰도 부족 | 텍스트 전처리 |
| RHYTHM | KPI 임계값 초과 | 알림 발송 |
| COST-GUARD | 비용 초과 | 승인 대기 |
| ZERO | 모든 자동화 실패 | 수동 개입 |

---

## 🔄 업데이트 로드맵

### Phase 1: 기본 기능 (현재)
- ✅ Streamlit 대시보드
- ✅ RPA 자동화
- ✅ AI 요약
- ✅ 스케줄링

### Phase 2: 고급 기능 (예정)
- 🔄 Supabase 다중 사용자 DB
- 🔄 PowerBI 연동
- 🔄 Email/Slack 알림
- 🔄 모바일 앱

### Phase 3: 기업 통합 (계획)
- 📋 Samsung C&T API 연동
- 📋 ADNOC-DSV 시스템 통합
- 📋 FANR/MOIAT 규정 준수
- 📋 Heat-Stow 분석 연동

---

## 🤝 기여 가이드

### 개발 환경 설정
```bash
# 개발 의존성 설치
pip install -r requirements.txt
pip install pre-commit

# 코드 포맷터 설정
pre-commit install
```

### 코드 스타일
- **TDD**: 테스트 우선 개발
- **MACHO-GPT 규칙**: 신뢰도 ≥0.90
- **명명 규칙**: `logi_[function]_[YYMMDD].py`

---

## 📞 지원 및 문의

### 기술 지원
- **이슈 리포트**: GitHub Issues
- **기능 요청**: Feature Request
- **문서 개선**: Documentation PR

### 연락처
- **프로젝트 관리자**: MR.CHA
- **기술 팀**: Samsung C&T Logistics
- **AI 시스템**: MACHO-GPT v3.4-mini

---

## 📄 라이선스

이 프로젝트는 Samsung C&T Logistics의 내부 프로젝트이며, HVDC 프로젝트의 일부입니다.

**🔧 추천 명령어:**
- `/logi-master --fast predict` [일일 KPI 예측]
- `/switch_mode COST-GUARD` [비용 관리 모드]
- `/visualize_data --type=heatmap` [데이터 시각화]

---

## 🌟 **현재 시스템 상태**

### ✅ **실행 중인 서비스**
- **포트 8505**: Executive Dashboard ⭐ (Discord 스타일)
- **포트 8506**: Simplified App 🔧 (안정 버전)  
- **포트 8507**: 통합 실행 🚀 (원클릭)

### 📊 **시스템 KPI**
- **신뢰도**: 51.0% (목표: ≥90%)
- **현재 모드**: 🔴 ZERO (안전 모드)
- **총 대화방**: 5개
- **완료율**: 진행 중...
- **상태**: ⚠️ 2차 트리거 대기

### 🎯 **추천 명령어**
```bash
/workflow_optimization    # 워크플로우 최적화
/room_health_check       # 대화방 상태 점검  
/task_prioritization     # 작업 우선순위 조정
```

---

## 📞 **지원 및 문의**

- **GitHub Repository**: https://github.com/macho715/HVDC-WHATSAPP
- **프로젝트**: Samsung C&T Logistics · HVDC Project
- **AI 시스템**: MACHO-GPT v3.4-mini
- **파트너십**: ADNOC·DSV Partnership

---

*마지막 업데이트: 2025-07-05*  
*MACHO-GPT v3.4-mini · Samsung C&T Logistics · HVDC Project · ADNOC·DSV Partnership* 