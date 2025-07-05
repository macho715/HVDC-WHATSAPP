# 📱 WhatsApp 업무 요약 대시보드

**Samsung C&T Logistics · HVDC Project**  
**MACHO-GPT v3.4-mini**

WhatsApp 채팅 내용을 자동으로 추출하고 AI 요약을 생성하는 멀티 프론트엔드 대시보드 시스템입니다.

### 🎨 Multiple Frontend Options
- **🐍 Streamlit**: Python 기반 즉시 사용 가능한 대시보드
- **⚛️ React**: 모던 웹앱 UI/UX with Tailwind CSS  
- **🔄 FastAPI**: React 연동을 위한 RESTful API 백엔드

---

## 🚀 주요 기능

### 📊 핵심 기능
- **자동 추출**: Playwright RPA를 통한 WhatsApp Web 자동 데이터 추출
- **AI 요약**: OpenAI GPT-4o를 활용한 지능형 대화 요약
- **긴급 분류**: 긴급/중요 키워드 자동 감지 및 하이라이트
- **대시보드**: Streamlit 기반 직관적인 웹 인터페이스
- **자동화**: 스케줄러를 통한 무인 자동 실행

### 🔧 MACHO-GPT 통합
- **다중 모드**: PRIME|ORACLE|ZERO|LATTICE|RHYTHM|COST-GUARD
- **신뢰도 관리**: ≥0.90 신뢰도 보장
- **자동 트리거**: KPI 기반 자동 모드 전환
- **Fail-safe**: 오류 시 자동 ZERO 모드 전환

---

## 📁 프로젝트 구조

```
whatsapp/
├── whatsapp_summary_app.py          # 메인 Streamlit 앱
├── integration_api.py               # FastAPI 백엔드 서버
├── run_macho_gpt.py                # 통합 시스템 런처
├── extract_whatsapp_rpa.py          # RPA 통합 실행 스크립트
├── requirements.txt                 # Python 패키지 의존성
├── requirements_api.txt             # FastAPI 추가 의존성
├── README.md                        # 프로젝트 문서
├── 
├── react_frontend/                  # React 프론트엔드
│   ├── src/
│   │   ├── components/
│   │   │   └── WhatsAppSummaryApp.jsx  # 메인 React 컴포넌트
│   │   ├── services/
│   │   │   └── api.js              # API 통신 서비스
│   │   ├── App.js                  # React 앱 진입점
│   │   └── index.js                # React DOM 렌더링
│   ├── public/
│   │   └── index.html              # HTML 템플릿
│   ├── package.json                # Node.js 의존성
│   ├── tailwind.config.js          # Tailwind CSS 설정
│   └── README.md                   # React 프론트엔드 문서
│
├── macho_gpt/
│   ├── core/
│   │   └── logi_whatsapp_241219.py  # WhatsApp 메시지 처리 모듈
│   └── rpa/
│       └── logi_rpa_whatsapp_241219.py  # RPA 자동화 모듈
│
├── configs/
│   └── config_prime_dev.yaml       # 설정 파일
│
├── logs/                           # 로그 파일
├── data/                          # 데이터 파일
└── templates/                     # 템플릿 파일
```

---

## 🛠️ 설치 및 설정

### 1. 환경 설정

#### Python 환경 (필수)
```bash
# 프로젝트 클론
git clone <repository-url>
cd whatsapp

# 파이썬 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Streamlit 의존성 설치
pip install -r requirements.txt

# FastAPI 의존성 설치 (React 사용 시)
pip install -r requirements_api.txt

# Playwright 브라우저 설치
playwright install
```

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

## 🚀 실행 방법

### 1. Streamlit 대시보드 (추천)

```bash
# Streamlit 앱 실행
streamlit run whatsapp_summary_app.py

# 브라우저에서 http://localhost:8501 접속
```

### 2. React 모던 대시보드 (신규)

```bash
# FastAPI 서버 의존성 설치
pip install -r requirements_api.txt

# 통합 런처로 React + FastAPI 실행
python run_macho_gpt.py --mode react

# 또는 개별 실행
# 1) FastAPI 백엔드 (터미널 1)
python integration_api.py

# 2) React 프론트엔드 (터미널 2)
cd react_frontend
npm install
npm start

# 브라우저에서 접속:
# - React: http://localhost:3000
# - FastAPI: http://localhost:8502
# - API Docs: http://localhost:8502/api/docs
```

### 3. 통합 실행 (모든 서비스)

```bash
# 모든 프론트엔드 동시 실행
python run_macho_gpt.py --mode both

# 사용 가능한 URL:
# - Streamlit: http://localhost:8501
# - React: http://localhost:3000  
# - FastAPI: http://localhost:8502
```

### 4. RPA 자동화 실행

```bash
# 최초 실행 (인증 설정)
python extract_whatsapp_rpa.py --mode PRIME

# 스케줄러 실행
python extract_whatsapp_rpa.py --scheduled --report
```

### 5. 개발 모드 실행

```bash
# 설정 파일 지정
python extract_whatsapp_rpa.py --config configs/config_prime_dev.yaml --mode LATTICE
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

*마지막 업데이트: 2024-12-19*  
*MACHO-GPT v3.4-mini · Samsung C&T Logistics · HVDC Project* 