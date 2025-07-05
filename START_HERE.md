# 🚀 MACHO-GPT v3.4-mini 빠른 시작

**환영합니다!** Samsung C&T Logistics의 HVDC 프로젝트용 WhatsApp 자동화 시스템입니다.

## ⚡ 초간단 3단계 실행

### 1️⃣ 의존성 설치
```bash
pip install -r requirements_simple.txt
```

### 2️⃣ 앱 실행 (선택)
```bash
# 🎯 Executive Dashboard (추천)
streamlit run whatsapp_executive_dashboard.py --server.port 8505

# 💬 기본 WhatsApp 앱
streamlit run simplified_whatsapp_app.py --server.port 8506

# 🔄 통합 실행 (모든 앱)
python run_app.py
```

### 3️⃣ 브라우저 접속
- **🎯 Executive Dashboard**: http://localhost:8505 (추천)
- **💬 Simplified App**: http://localhost:8506
- **🔄 Integrated App**: http://localhost:8507

## 🆘 문제가 있나요?

### 빠른 해결
```bash
# 패키지 재설치
pip install streamlit --upgrade

# 포트 변경 (충돌시)
streamlit run simplified_whatsapp_app.py --server.port 8508
```

### 상세한 도움말
- 📘 **자세한 가이드**: [README_QUICK_START.md](./README_QUICK_START.md)
- 📋 **프로젝트 요약**: [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)
- 🌐 **GitHub 리포지토리**: [HVDC-WHATSAPP](https://github.com/macho715/HVDC-WHATSAPP)

---

🎯 **추천**: Executive Dashboard (포트 8505)가 가장 완전한 기능을 제공합니다!

💡 **팁**: 처음 사용자라면 [README_QUICK_START.md](./README_QUICK_START.md)를 먼저 읽어보세요. 