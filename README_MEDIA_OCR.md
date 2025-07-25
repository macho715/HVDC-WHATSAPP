# 📱 WhatsApp 미디어 OCR 분석 모듈

**MACHO-GPT v3.4-mini** | Samsung C&T Logistics · HVDC Project

## 🎯 **개요**

WhatsApp Web에서 미디어 메시지를 자동으로 수집하고 OCR(광학 문자 인식)을 통해 텍스트를 추출하는 고급 분석 모듈입니다.

### ✨ **주요 기능**

- 🔍 **자동 미디어 감지**: WhatsApp Web에서 이미지, PDF 등 미디어 메시지 자동 탐지
- 📄 **다국어 OCR**: EasyOCR + Google Cloud Vision API를 통한 다국어 텍스트 추출
- 🔒 **보안 강화**: 민감 정보 자동 감지 및 익명화
- 📊 **실시간 분석**: Streamlit 기반 대시보드로 결과 시각화
- ⚡ **성능 최적화**: 배치 처리, 캐싱, 중복 제거

## 🚀 **빠른 시작**

### 1. **의존성 설치**

```bash
# 미디어 OCR 전용 라이브러리 설치
pip install -r requirements_media_ocr.txt

# 또는 개별 설치
pip install easyocr PyMuPDF pdf2image pytesseract pillow
pip install google-cloud-vision google-cloud-documentai
```

### 2. **기본 실행**

```bash
# HVDC 물류팀 채팅방에서 미디어 추출 (최대 10개)
python whatsapp_media_ocr_extractor.py

# 특정 채팅방 지정
python whatsapp_media_ocr_extractor.py --chat "HVDC 물류팀" --max-media 20

# 모든 기본 채팅방 자동 추출
python whatsapp_media_ocr_extractor.py --auto
```

### 3. **대시보드 실행**

```bash
# 미디어 OCR 결과 대시보드
streamlit run whatsapp_media_ocr_dashboard.py
```

## 📋 **사용법**

### **명령행 옵션**

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--chat` | 추출할 채팅방 제목 | `--chat "HVDC 물류팀"` |
| `--auto` | 모든 기본 채팅방 자동 추출 | `--auto` |
| `--max-media` | 최대 미디어 처리 개수 | `--max-media 50` |
| `--media-only` | 미디어만 처리 (텍스트 메시지 제외) | `--media-only` |
| `--detect-objects` | 객체 감지 활성화 | `--detect-objects` |

### **실행 예시**

```bash
# 1. 단일 채팅방 미디어 추출
python whatsapp_media_ocr_extractor.py --chat "Abu Dhabi Logistics" --max-media 15

# 2. 전체 자동 추출 (모든 기본 채팅방)
python whatsapp_media_ocr_extractor.py --auto --max-media 30

# 3. 미디어 전용 추출 (객체 감지 포함)
python whatsapp_media_ocr_extractor.py --media-only --detect-objects
```

## 🔧 **설정**

### **환경 변수 (필수 - Google Cloud Vision API)**

Google Cloud Vision API 사용 시:

#### **1. Google Cloud Console 설정**
1. **Cloud Console → APIs & Services ▸ Library** → "Cloud Vision API" 검색 후 **Enable**
2. **IAM & Admin ▸ Service Accounts** → **+ Create Service Account**
3. **Role** 검색창에 *Vision* 입력 → **Vision API User** 선택
4. **Keys 탭 ▸ Add Key ▸ JSON** → `vision-sa.json` 다운로드

#### **2. 환경변수 등록**

```powershell
# Windows
setx GOOGLE_APPLICATION_CREDENTIALS "C:\keys\vision-sa.json"
```

```bash
# macOS / Linux
export GOOGLE_APPLICATION_CREDENTIALS="/home/user/keys/vision-sa.json"
```

#### **3. 설정 테스트**
```bash
# 설정 확인
python test_gcv_setup.py
```

#### **4. 배치 스크립트 실행**
```bash
# Windows (CMD)
run_gcv_ocr.bat

# Windows (PowerShell)
.\run_gcv_ocr.ps1

# 또는 직접 실행
python whatsapp_media_ocr_extractor.py --chat "HVDC 물류팀" --ocr-engine gcv
```

### **설정 파일**

`configs/media_ocr_config.yaml`:

```yaml
# 미디어 처리 설정
media_processing:
  max_file_size_mb: 5
  supported_formats: ['.jpg', '.jpeg', '.png', '.pdf']
  download_timeout: 30

# OCR 설정
ocr:
  engines: ['easyocr', 'gcv']
  languages: ['en', 'ko']
  confidence_threshold: 0.7

# 보안 설정
security:
  enable_anonymization: true
  sensitive_patterns:
    - phone_number
    - email
    - credit_card
```

## 📊 **결과 분석**

### **출력 파일**

- **위치**: `data/whatsapp_media_ocr_YYYYMMDD_HHMMSS.json`
- **형식**: JSON 구조화된 데이터

### **결과 구조**

```json
{
  "chat_title": "HVDC 물류팀",
  "status": "SUCCESS",
  "media_count": 15,
  "processed_count": 12,
  "media_results": [
    {
      "file_name": "invoice_20241219.pdf",
      "file_type": ".pdf",
      "file_size": 2048576,
      "ocr_result": {
        "text": "추출된 텍스트 내용...",
        "confidence": 0.85,
        "engine": "easyocr",
        "bounding_boxes": []
      },
      "processed_at": "2024-12-19T10:30:00"
    }
  ],
  "extraction_time": "2024-12-19T10:30:00"
}
```

### **대시보드 기능**

1. **📁 파일 형식별 분포**: 파이 차트로 미디어 형식 분석
2. **🔍 OCR 엔진별 성능**: 박스플롯으로 엔진 성능 비교
3. **📊 신뢰도 분포**: 히스토그램으로 OCR 품질 분석
4. **📝 텍스트 길이 분포**: 추출된 텍스트 길이 통계
5. **⏰ 처리 시간 타임라인**: 시간별 처리 현황
6. **🔒 민감 정보 분석**: 감지된 민감 정보 현황

## 🛠️ **고급 기능**

### **객체 감지 (YOLO)**

```bash
# 객체 감지 활성화
python whatsapp_media_ocr_extractor.py --detect-objects

# 감지 가능한 객체:
# - 크레인, 트레일러, 컨테이너
# - 파손, 누수, 안전 위험
# - 인증서, 문서, 서명
```

### **배치 처리**

```bash
# 대량 미디어 처리
python whatsapp_media_ocr_extractor.py --auto --max-media 100

# 백그라운드 실행
nohup python whatsapp_media_ocr_extractor.py --auto > media_ocr.log 2>&1 &
```

### **API 연동**

```python
# 프로그래밍 방식 사용
from whatsapp_media_ocr_extractor import WhatsAppMediaOCRExtractor

extractor = WhatsAppMediaOCRExtractor()
result = await extractor.extract_media_from_chat("채팅방명", max_media=10)
```

## 🔒 **보안 및 개인정보 보호**

### **자동 익명화**

- **전화번호**: `010-1234-5678` → `[REDACTED]`
- **이메일**: `user@example.com` → `[REDACTED]`
- **신용카드**: `1234-5678-9012-3456` → `[REDACTED]`
- **주민번호**: `123456-7890123` → `[REDACTED]`

### **데이터 보호**

- 모든 임시 파일은 처리 후 자동 삭제
- 파일 해시 기반 중복 처리로 저장 공간 절약
- 민감 정보는 추출 단계에서 즉시 익명화

## 📈 **성능 최적화**

### **처리 속도**

- **이미지 (1MB)**: ~3초
- **PDF (5페이지)**: ~10초
- **배치 처리 (10개)**: ~30초

### **메모리 사용량**

- **최대 파일 크기**: 5MB
- **동시 처리**: 1개 (순차 처리)
- **캐시 크기**: 처리된 파일 해시만 저장

### **요금 최적화 팁**

- **정확도 평가**: EasyOCR(로컬)·Vision(GCV) 모두 결과에 `confidence` 값을 반환
- **요금 최적화**: 먼저 PyMuPDF `page.get_text()` 로 *텍스트 레이어 존재 여부*를 검사하고, 없을 때만 GCV 호출 (PDF 비용 최대 40%↓)
- **DOM 변경 대응**: `MEDIA_SELECTORS` 리스트에 `div[data-testid^="media"]` / `img[src^="blob:"]` 추가 완료

## 🐛 **문제 해결**

### **일반적인 오류**

1. **ImportError: No module named 'easyocr'**
   ```bash
   pip install easyocr
   ```

2. **PDF 처리 오류**
   ```bash
   # Windows
   pip install pdf2image
   # poppler 설치 필요
   ```

3. **Google Cloud Vision API 오류**

| 오류 메시지 | 원인 | 해결 |
|------------|------|------|
| `UNAUTHENTICATED` | JSON 키 경로 미설정·오타 | 환경변수 확인, 새 터미널 재실행 |
| `PERMISSION_DENIED` | 서비스 계정에 Vision 역할 없음 | IAM > Role: Vision API User 부여 |
| `quotaExceeded` | 월 1,000 무료 요청 초과 | 가격표 확인·쿼터 상향 신청 |
| `400 PDF size too large` | 20 MB+ PDF | PyMuPDF 분할 후 페이지별 OCR |

```bash
# 환경 변수 확인
echo $GOOGLE_APPLICATION_CREDENTIALS
```

### **로그 확인**

```bash
# 실시간 로그 모니터링
tail -f logs/whatsapp_media_ocr.log

# 오류 로그 필터링
grep "ERROR" logs/whatsapp_media_ocr.log
```

## 📞 **지원**

### **문서**

- [MACHO-GPT v3.4-mini 가이드](../README.md)
- [WhatsApp RPA 가이드](README_WHATSAPP_AUTOMATION.md)
- [업그레이드 계획](docs/WHATSAPP_MEDIA_OCR_UPGRADE_PLAN.md)

### **연락처**

- **프로젝트**: Samsung C&T Logistics · HVDC Project
- **기술 지원**: MACHO-GPT 개발팀
- **문서**: [GitHub Wiki](https://github.com/your-repo/wiki)

---

**🤖 MACHO-GPT v3.4-mini** | **📱 WhatsApp 미디어 OCR 분석 모듈**

*Samsung C&T Logistics · HVDC Project · 2024* 