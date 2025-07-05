# 🤖 MACHO-GPT WhatsApp 자동화 워크플로 v3.4-mini

## 📋 Executive Summary

**완전 자동화된 WhatsApp 채팅 추출 및 분석 시스템**을 구현했습니다. 매일 18:00에 자동으로 WhatsApp Web에서 대화 내용을 추출하고, AI 요약을 생성하며, 워크플로 매니저와 연동하여 태스크를 자동 생성합니다.

## 🎯 주요 기능

- 🔄 **완전 자동화**: 매일 18:00 자동 실행 (Windows 작업 스케줄러)
- 🤖 **Playwright RPA**: WhatsApp Web 자동 제어
- 🧠 **AI 요약**: OpenAI GPT-4o-mini 기반 스마트 분석
- 📋 **워크플로 연동**: 자동 태스크 생성 및 관리
- 📊 **실시간 대시보드**: Streamlit 기반 통합 모니터링
- 🚨 **긴급/중요 분류**: 키워드 기반 자동 우선순위 설정

## 🛠️ 시스템 구조

```
whatsapp/
├── extract_whatsapp_auto.py      # 🤖 메인 자동화 스크립트
├── setup_whatsapp_scheduler.py   # ⏰ 스케줄러 설정 도구
├── whatsapp_summary_app.py       # 🖥️ Streamlit 대시보드
├── integration_api.py            # 🌐 REST API 서버
├── run_whatsapp_auto.bat         # 📁 자동 생성 배치 파일
├── monitor_whatsapp_scheduler.ps1 # 📊 모니터링 스크립트
├── whatsapp_auth.json            # 🔑 인증 정보 (자동 생성)
├── summaries.json                # 💾 요약 데이터베이스
└── logs/                         # 📝 로그 파일들
```

## 🚀 완전 설정 가이드

### 1단계: 환경 준비

```bash
# 필수 패키지 설치
pip install playwright fastapi uvicorn streamlit openai pandas pydantic

# Playwright 브라우저 드라이버 설치
playwright install
```

### 2단계: OpenAI API 키 설정

```bash
# Windows 환경변수 설정
set OPENAI_API_KEY=your_openai_api_key_here

# 또는 PowerShell에서
$env:OPENAI_API_KEY="your_openai_api_key_here"
```

### 3단계: WhatsApp 인증 설정 (최초 1회)

```bash
# WhatsApp Web 인증 설정
python extract_whatsapp_auto.py --setup
```

1. 브라우저가 자동으로 열리고 WhatsApp Web으로 이동
2. 휴대폰으로 QR 코드 스캔
3. 로그인 완료 후 인증 정보 자동 저장 (`whatsapp_auth.json`)

### 4단계: 스케줄러 등록 (매일 18:00 자동 실행)

```bash
# 관리자 권한으로 실행 권장
python setup_whatsapp_scheduler.py --setup
```

설정 완료 후 생성되는 파일들:
- `run_whatsapp_auto.bat`: 실행 배치 파일
- `monitor_whatsapp_scheduler.ps1`: 모니터링 스크립트
- Windows 작업 스케줄러에 태스크 등록

### 5단계: 시스템 실행 및 모니터링

```bash
# Streamlit 대시보드 실행
streamlit run whatsapp_summary_app.py --server.port 8504

# API 서버 실행 (선택사항)
python integration_api.py

# 수동 추출 테스트
python extract_whatsapp_auto.py --run --room "MR.CHA 전용"
```

### 6단계: 모니터링 및 관리

```bash
# 스케줄러 상태 확인
python setup_whatsapp_scheduler.py --status

# PowerShell 모니터링
.\monitor_whatsapp_scheduler.ps1

# 스케줄러 제거 (필요시)
python setup_whatsapp_scheduler.py --remove
```

## 📊 접속 주소

| 서비스 | 주소 | 설명 |
|--------|------|------|
| 📱 **메인 대시보드** | http://localhost:8504 | Streamlit 통합 대시보드 |
| 🌐 **API 서버** | http://localhost:8503 | REST API 서버 |
| 📖 **API 문서** | http://localhost:8503/api/docs | Swagger UI 문서 |

## 🔧 설정 옵션

### 대화방 설정

기본 대화방: `"MR.CHA 전용"`

다른 대화방 사용시:
```bash
python extract_whatsapp_auto.py --run --room "다른대화방이름"
```

### 실행 시간 변경

`setup_whatsapp_scheduler.py`에서 수정:
```python
"/st", "18:00",  # 원하는 시간으로 변경 (예: "09:00")
```

### 추출 시간 범위 설정

`extract_whatsapp_auto.py`에서 수정:
```python
self.extraction_hours = 24  # 24시간 → 원하는 시간으로 변경
```

## 📋 워크플로 매니저 연동

### 자동 태스크 생성

추출된 요약에서 자동으로 태스크가 생성됩니다:

- 🚨 **긴급**: `긴급`, `urgent`, `ASAP` 키워드 → `URGENT` 우선순위
- ⭐ **중요**: `중요`, `important`, `승인` 키워드 → `HIGH` 우선순위
- 📋 **일반**: 나머지 태스크 → `MEDIUM` 우선순위

### 대화방 연동

워크플로 매니저의 대화방과 연동하여 태스크를 자동 할당:

```python
# 대화방 이름으로 연동
python extract_whatsapp_auto.py --run --room "MR.CHA 전용"
```

## 🔍 트러블슈팅

### 일반적인 문제들

**Q: Playwright 설치 후에도 "playwright not found" 오류**
```bash
# 해결방법
pip uninstall playwright
pip install playwright
playwright install
```

**Q: WhatsApp Web 로그인이 안 됨**
```bash
# 해결방법
1. 기존 auth.json 파일 삭제
2. python extract_whatsapp_auto.py --setup 재실행
3. 새 QR 코드로 재인증
```

**Q: 스케줄러 등록 실패**
```bash
# 해결방법
1. 관리자 권한으로 PowerShell 실행
2. python setup_whatsapp_scheduler.py --setup 재실행
```

**Q: OpenAI API 오류**
```bash
# 해결방법
1. OPENAI_API_KEY 환경변수 확인
2. API 키 유효성 및 크레딧 확인
3. 네트워크 연결 상태 확인
```

### 로그 확인 방법

```bash
# 자동화 로그
type logs\whatsapp_auto.log

# 스케줄러 로그
type logs\scheduler.log

# Streamlit 로그
# 콘솔에서 직접 확인 가능
```

## 🎯 MACHO-GPT v3.4-mini 통합

### 지원 모드

- **PRIME**: 기본 모드 (신뢰도 ≥95%)
- **ZERO**: 실패 시 안전 모드 전환
- **LATTICE**: 고급 텍스트 분석 모드

### 자동 트리거 생성

```python
# 자동 생성되는 트리거 예시
"/alert urgent_items 5개 긴급 항목 발견"
"/workflow escalate 10개 중요 항목 처리 필요"
"/team workload_balance 대량 태스크 발생으로 업무 분산 필요"
```

### KPI 모니터링

- 📊 **신뢰도**: AI 요약 정확도 (≥90% 목표)
- 🎯 **성공률**: 자동 추출 성공률 (≥95% 목표)
- ⚡ **실행시간**: 전체 프로세스 소요 시간
- 🚨 **긴급도**: 긴급/중요 항목 비율

## 📈 성능 최적화

### 권장 설정

```python
# 고성능 설정
config = {
    'headless': True,           # 헤드리스 모드로 빠른 실행
    'timeout': 30000,           # 30초 타임아웃
    'extraction_hours': 24,     # 24시간 추출 범위
    'scroll_delay': 500,        # 스크롤 지연 최소화
}
```

### 리소스 사용량

- **메모리**: 평균 200-300MB
- **CPU**: 추출 시 일시적 사용량 증가
- **디스크**: 로그 및 DB 파일 약 10-50MB
- **네트워크**: OpenAI API 호출 시에만 사용

## 🔐 보안 고려사항

### 인증 정보 보호

- `whatsapp_auth.json`: 중요한 인증 정보 포함
- 해당 파일을 버전 관리에 포함하지 말 것
- 정기적인 인증 정보 갱신 권장

### API 키 보안

- 환경변수 사용 권장
- 코드에 직접 하드코딩 금지
- API 키 사용량 모니터링

## 🔧 확장 가능성

### 추가 기능 구현

1. **Slack/Teams 연동**: 다른 메신저 플랫폼 지원
2. **이메일 알림**: 긴급 항목 발견 시 자동 알림
3. **데이터베이스 연동**: PostgreSQL, MongoDB 등 지원
4. **클라우드 배포**: AWS, Azure 등 클라우드 환경 지원

### API 확장

```python
# 추가 API 엔드포인트 예시
@app.get("/api/v1/extraction/history")
async def get_extraction_history():
    # 추출 이력 조회
    pass

@app.post("/api/v1/extraction/manual")
async def manual_extraction(room_name: str):
    # 수동 추출 실행
    pass
```

---

## 🎉 완성된 기능

✅ **Playwright 기반 WhatsApp Web 자동화**
✅ **OpenAI GPT-4o-mini AI 요약**
✅ **Windows 작업 스케줄러 통합**
✅ **워크플로 매니저 연동**
✅ **Streamlit 대시보드**
✅ **FastAPI REST API**
✅ **자동 태스크 생성**
✅ **실시간 모니터링**
✅ **에러 처리 및 로깅**
✅ **완전 자동화 워크플로**

## 🔧 추천 명령어

```bash
/logi_master daily_summary      # 일일 요약 조회
/workflow check_status          # 워크플로 상태 확인
/automate schedule_check        # 스케줄러 상태 모니터링
```

**🎯 이제 완전히 자동화된 WhatsApp 업무 요약 시스템이 준비되었습니다!**

매일 18:00에 자동으로 대화 내용을 추출하고, AI 요약을 생성하며, 중요한 태스크를 자동으로 워크플로에 등록하는 완전 자동화 시스템입니다. 