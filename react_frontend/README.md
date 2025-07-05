# MACHO-GPT v3.4-mini React Frontend

## 🚀 HVDC Project - Samsung C&T Logistics Integration

WhatsApp 업무 요약 시스템의 React 기반 프론트엔드 애플리케이션입니다.

## 📋 주요 기능

### 🎯 MACHO-GPT 핵심 기능
- **6개 Containment 모드**: PRIME, ORACLE, ZERO, LATTICE, RHYTHM, COST-GUARD
- **신뢰도 ≥90% 보장**: 다중 소스 검증 시스템
- **자동 Fail-Safe**: 오류 발생 시 ZERO 모드 자동 전환
- **실시간 KPI 모니터링**: 성공률, 처리시간, 오류율 추적
- **자동 트리거 시스템**: 상황별 명령어 자동 추천

### 💼 비즈니스 기능
- **WhatsApp 대화 분석**: AI 기반 메시지 요약 및 분류
- **긴급도 자동 분류**: 키워드 기반 우선순위 설정
- **팀별 활동 요약**: 부서별 주요 업무 내용 정리
- **대화방 관리**: 활성/비활성 상태 관리 및 우선순위 설정
- **명령어 추천**: 상황에 맞는 MACHO-GPT 명령어 제안

## 🛠️ 기술 스택

### Frontend
- **React 18.2.0**: 모던 React 훅 기반 개발
- **Tailwind CSS 3.3.6**: 유틸리티 퍼스트 CSS 프레임워크
- **Lucide React**: 아이콘 라이브러리
- **Axios**: HTTP 클라이언트

### MACHO-GPT 통합
- **API 서비스**: 백엔드 통신 레이어
- **모드 시스템**: 6개 containment 모드 지원
- **신뢰도 시스템**: 실시간 신뢰도 모니터링
- **자동 트리거**: 상황별 자동 명령어 생성

## 🚀 시작하기

### 1. 프로젝트 설치
```bash
# 프로젝트 루트 디렉토리에서
cd react_frontend

# 의존성 설치
npm install

# 개발 서버 시작
npm start
```

### 2. 환경 설정
```bash
# .env 파일 생성
REACT_APP_API_URL=http://localhost:8501
REACT_APP_MACHO_GPT_VERSION=3.4-mini
REACT_APP_PROJECT=HVDC_SAMSUNG_CT
```

### 3. 백엔드 연동
```bash
# 백엔드 Streamlit 애플리케이션 실행 (별도 터미널)
cd ..
streamlit run whatsapp_summary_app.py
```

## 📁 프로젝트 구조

```
react_frontend/
├── public/
│   ├── index.html              # HTML 템플릿
│   └── manifest.json           # PWA 매니페스트
├── src/
│   ├── components/
│   │   └── WhatsAppSummaryApp.jsx  # 메인 컴포넌트
│   ├── services/
│   │   └── api.js              # API 서비스
│   ├── App.js                  # 앱 진입점
│   ├── App.css                 # 앱 스타일
│   ├── index.js                # React 진입점
│   └── index.css               # 글로벌 스타일
├── package.json                # 프로젝트 설정
├── tailwind.config.js          # Tailwind 설정
└── README.md                   # 문서
```

## 🎨 UI/UX 특징

### 디자인 시스템
- **Samsung C&T 브랜드 컬러**: 일관된 브랜드 경험
- **반응형 디자인**: 모바일/데스크톱 최적화
- **다크/라이트 모드**: 사용자 선호도 지원
- **애니메이션**: 부드러운 전환 효과

### 컴포넌트 구조
- **모듈화 설계**: 재사용 가능한 컴포넌트
- **상태 관리**: React 훅 기반 상태 관리
- **에러 바운더리**: 안정적인 에러 처리
- **성능 최적화**: 메모이제이션 및 지연 로딩

## 🔧 MACHO-GPT 명령어

### 기본 명령어
```bash
/logi_master                   # 물류 마스터 작업 실행
/switch_mode [MODE]            # 모드 전환 (PRIME, ORACLE, ZERO, LATTICE, RHYTHM, COST-GUARD)
/kpi_monitor                   # KPI 모니터링 실행
/visualize_data                # 데이터 시각화 생성
/urgent_processor              # 긴급 처리 시스템 활성화
```

### 고급 명령어
```bash
/automate whatsapp_summary     # WhatsApp 요약 자동화
/test_confidence [THRESHOLD]   # 신뢰도 테스트
/optimize_processing          # 처리 성능 최적화
/generate_report              # 보고서 생성
```

## 📊 성능 지표

### 목표 KPI
- **신뢰도**: ≥90% (MACHO-GPT 표준)
- **처리 시간**: <3초 (평균 응답 시간)
- **성공률**: ≥95% (처리 성공률)
- **오류율**: <5% (시스템 오류율)

### 모니터링
- **실시간 대시보드**: KPI 실시간 추적
- **자동 알림**: 임계값 초과 시 알림
- **성능 분석**: 처리 시간 및 리소스 사용량 분석

## 🔐 보안 및 컴플라이언스

### 데이터 보안
- **PII 보호**: 개인정보 자동 마스킹
- **NDA 준수**: 기밀 정보 보호
- **로컬 저장**: 민감 데이터 로컬 처리

### 규제 준수
- **FANR 준수**: 원자력 규제 요구사항
- **MOIAT 준수**: 교통부 규제 요구사항
- **Samsung C&T 정책**: 내부 보안 정책

## 🧪 테스트

### 테스트 실행
```bash
# 단위 테스트
npm test

# 커버리지 테스트
npm run macho-test

# 빌드 테스트
npm run build
```

### 테스트 커버리지
- **컴포넌트 테스트**: 90% 이상
- **API 테스트**: 95% 이상
- **통합 테스트**: 85% 이상

## 📦 배포

### 개발 빌드
```bash
npm run build
```

### 프로덕션 배포
```bash
# 최적화된 빌드 (소스맵 제외)
npm run macho-build

# 배포 디렉토리: build/
```

## 🤝 기여하기

### 코드 스타일
- **TDD 방법론**: 테스트 우선 개발
- **Tidy First**: 구조적/행위적 변경 분리
- **MACHO-GPT 표준**: 신뢰도 ≥90% 유지

### 커밋 메시지
```bash
[STRUCT] Extract component logic into separate hooks
[FEAT] Add real-time KPI monitoring dashboard
[FIX] Resolve confidence calculation accuracy issue
[PERF] Optimize React component rendering performance
```

## 📞 지원

### 문의사항
- **개발팀**: MACHO-GPT v3.4-mini 개발팀
- **이슈 리포트**: GitHub Issues
- **기술 문서**: README.md 및 코드 주석

### 참고 자료
- **MACHO-GPT 매뉴얼**: 시스템 사용 가이드
- **Samsung C&T 가이드라인**: 개발 표준
- **React 공식 문서**: React 개발 가이드

---

**MACHO-GPT v3.4-mini** | Samsung C&T Logistics | HVDC Project Integration 