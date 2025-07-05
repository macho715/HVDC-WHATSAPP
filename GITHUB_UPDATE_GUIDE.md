# 🚀 GitHub 저장소 업데이트 가이드

## 📋 저장소 정보
- **Repository**: https://github.com/macho715/HVDC-WHATSAPP.git
- **Status**: 현재 비어있음 (Empty repository)
- **프로젝트**: MACHO-GPT v3.4-mini WhatsApp 자동화 시스템

## 🔧 방법 1: Git 명령줄 사용 (추천)

### 1️⃣ Git 설치 확인
```bash
# Git 버전 확인
git --version

# Git이 없다면 설치 필요
# Windows: https://git-scm.com/download/win
# 또는 Chocolatey: choco install git
```

### 2️⃣ Git 초기화 및 설정
```bash
# Git 저장소 초기화
git init

# 사용자 정보 설정 (최초 1회)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 원격 저장소 연결
git remote add origin https://github.com/macho715/HVDC-WHATSAPP.git
```

### 3️⃣ 파일 추가 및 커밋
```bash
# .gitignore 파일 생성 (선택사항)
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "auth.json" >> .gitignore
echo "logs/" >> .gitignore

# 모든 파일 추가
git add .

# 첫 번째 커밋 (MACHO-GPT 규칙에 따라)
git commit -m "[FEAT] Initial MACHO-GPT v3.4-mini WhatsApp automation system"
```

### 4️⃣ GitHub에 푸시
```bash
# 기본 브랜치 설정
git branch -M main

# GitHub에 푸시
git push -u origin main
```

## 🔧 방법 2: GitHub Desktop 사용 (GUI)

### 1️⃣ GitHub Desktop 다운로드
- https://desktop.github.com/

### 2️⃣ 저장소 클론
1. GitHub Desktop 실행
2. "Clone a repository from the Internet" 선택
3. URL 입력: `https://github.com/macho715/HVDC-WHATSAPP.git`
4. 로컬 경로 설정

### 3️⃣ 파일 복사 및 커밋
1. 현재 프로젝트 파일들을 클론된 폴더로 복사
2. GitHub Desktop에서 변경사항 확인
3. 커밋 메시지 입력: `Initial MACHO-GPT v3.4-mini system`
4. "Publish branch" 클릭

## 🔧 방법 3: 웹 브라우저 업로드

### 1️⃣ GitHub 웹사이트 접속
- https://github.com/macho715/HVDC-WHATSAPP

### 2️⃣ 파일 업로드
1. "uploading an existing file" 클릭
2. 파일 드래그 앤 드롭 또는 선택
3. 커밋 메시지 입력
4. "Commit changes" 클릭

## 📁 업로드할 핵심 파일들

### ✅ 필수 파일들
- `START_HERE.md` - 빠른 시작 가이드
- `PROJECT_SUMMARY.md` - 프로젝트 요약
- `whatsapp_executive_dashboard.py` - 메인 대시보드
- `simplified_whatsapp_app.py` - 기본 앱
- `run_app.py` - 통합 실행
- `extract_whatsapp_auto.py` - WhatsApp 자동화
- `requirements.txt` - Python 의존성
- `README.md` - 프로젝트 설명

### ✅ 디렉토리 구조
```
HVDC-WHATSAPP/
├── START_HERE.md
├── PROJECT_SUMMARY.md
├── whatsapp_executive_dashboard.py
├── simplified_whatsapp_app.py
├── run_app.py
├── extract_whatsapp_auto.py
├── requirements.txt
├── README.md
├── macho_gpt/
│   ├── __init__.py
│   ├── core/
│   ├── rpa/
│   └── utils/
├── data/
├── configs/
├── templates/
├── tests/
└── docs/
```

### ⚠️ 제외할 파일들
- `auth.json` - 인증 정보 (보안)
- `__pycache__/` - Python 캐시
- `logs/` - 로그 파일
- `*.pyc` - 컴파일된 Python 파일

## 🎯 업데이트 후 확인사항

1. **README.md 업데이트**
   - 프로젝트 설명 최신화
   - 실행 방법 안내
   - 스크린샷 추가

2. **라이센스 추가**
   - LICENSE 파일 생성
   - 적절한 라이센스 선택

3. **GitHub Pages 활성화** (선택사항)
   - Settings > Pages
   - 문서 사이트 자동 생성

4. **Actions 설정** (선택사항)
   - CI/CD 파이프라인 구축
   - 자동 테스트 실행

## 🔧 Git 명령어 빠른 참조

```bash
# 상태 확인
git status

# 변경사항 추가
git add .

# 커밋 (MACHO-GPT 규칙)
git commit -m "[FEAT] Add new feature"
git commit -m "[FIX] Fix bug in component"
git commit -m "[STRUCT] Refactor code structure"

# 푸시
git push

# 브랜치 관리
git branch -a
git checkout -b feature/new-feature
git merge feature/new-feature
```

## 🚨 주의사항

1. **인증 정보 보안**
   - `auth.json` 파일은 업로드하지 마세요
   - API 키나 비밀번호 포함 금지

2. **파일 크기 제한**
   - GitHub은 100MB 이상 파일 업로드 제한
   - 대용량 파일은 Git LFS 사용

3. **커밋 메시지 규칙**
   - MACHO-GPT 표준 준수
   - 명확하고 구체적인 설명

---

🔧 **추천 명령어:**
/git_setup [Git 설치 및 초기 설정]
/github_deploy [GitHub 저장소 자동 배포]
/project_documentation [프로젝트 문서화 완성] 