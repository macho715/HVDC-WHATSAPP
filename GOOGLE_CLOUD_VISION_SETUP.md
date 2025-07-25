# Google Cloud Vision API 설정 가이드
## MACHO-GPT v3.4-mini · Samsung C&T Logistics

---

## 📋 설정 체크리스트

### 1단계: Google Cloud Console 설정

| 단계 | 작업 | 참고 |
|------|------|------|
| ① 프로젝트 선택 | 콘솔 좌측 상단 *프로젝트 선택*에서 올바른 프로젝트 확인 | - |
| ② API 활성화 | **APIs & Services ▸ Library ▸ Cloud Vision API ▸ Enable** | [Google Cloud](https://cloud.google.com/vision/docs/setup) |
| ③ 결제 연결 | **Billing** 메뉴에서 결제 계정 없으면 연결 | [Google Cloud](https://cloud.google.com/vision/docs/setup) |
| ④ 서비스 계정 | **IAM & Admin ▸ Service Accounts ▸ +Create** → **Vision API User** 역할 부여 | [Google Cloud](https://cloud.google.com/docs/authentication/application-default-credentials) |
| ⑤ JSON 키 | **Keys ▸ Add Key ▸ JSON** 다운로드 | [Stack Overflow](https://stackoverflow.com/questions/60203492/how-to-set-google-application-credentials-running-on-gcp-appengine) |
| ⑥ 환경변수 | `setx GOOGLE_APPLICATION_CREDENTIALS "C:\keys\vision-sa.json"` | [Stack Overflow](https://stackoverflow.com/questions/60203492/how-to-set-google-application-credentials-running-on-gcp-appengine) |
| ⑦ 클라이언트 설치 | `pip install google-cloud-vision` 후 예제 호출 성공 | [Stack Overflow](https://stackoverflow.com/questions/74446830/how-to-fix-403-forbidden-errors-with-python-requests-even-with-user-agent-head) |

---

## 🔧 상세 설정 방법

### 1. Google Cloud Console 접속
```
https://console.cloud.google.com/
```

### 2. 프로젝트 선택
- 좌측 상단의 프로젝트 선택 드롭다운에서 올바른 프로젝트 선택
- 프로젝트가 없으면 새로 생성

### 3. Cloud Vision API 활성화
1. **APIs & Services** → **Library** 클릭
2. 검색창에 "Cloud Vision API" 입력
3. **Cloud Vision API** 선택 후 **Enable** 클릭

### 4. 결제 계정 연결
1. **Billing** 메뉴 클릭
2. 결제 계정이 없으면 **Link a billing account** 클릭
3. 신용카드 정보 입력 (무료 크레딧 사용 가능)

### 5. 서비스 계정 생성
1. **IAM & Admin** → **Service Accounts** 클릭
2. **+ CREATE SERVICE ACCOUNT** 클릭
3. 서비스 계정 이름 입력 (예: `vision-api-user`)
4. **CREATE AND CONTINUE** 클릭

### 6. 역할 부여
1. **Select a role** 클릭
2. 검색창에 "Vision" 입력
3. **Cloud Vision API User** 선택
4. **CONTINUE** 클릭
5. **DONE** 클릭

### 7. JSON 키 생성
1. 생성된 서비스 계정 클릭
2. **KEYS** 탭 클릭
3. **ADD KEY** → **Create new key** 클릭
4. **JSON** 선택 후 **CREATE** 클릭
5. `vision-sa.json` 파일이 다운로드됨

### 8. 환경변수 설정

#### Windows (CMD)
```cmd
setx GOOGLE_APPLICATION_CREDENTIALS "C:\keys\vision-sa.json"
```

#### Windows (PowerShell)
```powershell
[Environment]::SetEnvironmentVariable('GOOGLE_APPLICATION_CREDENTIALS', 'C:\keys\vision-sa.json', 'User')
```

#### macOS/Linux
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/home/user/keys/vision-sa.json"
```

### 9. 패키지 설치
```bash
pip install google-cloud-vision
```

---

## 🧪 설정 테스트

### 1. 환경변수 확인
```bash
echo %GOOGLE_APPLICATION_CREDENTIALS%
```

### 2. 파일 존재 확인
```bash
dir "C:\keys\vision-sa.json"
```

### 3. Python 테스트
```python
from google.cloud import vision
client = vision.ImageAnnotatorClient()
print("✅ Google Cloud Vision 클라이언트 생성 성공")
```

### 4. MACHO-GPT 테스트
```bash
python test_gcv_setup.py
```

---

## 🚨 일반적인 오류 및 해결방법

| 오류 메시지 | 원인 | 해결방법 |
|------------|------|----------|
| `UNAUTHENTICATED` | JSON 키 경로 미설정·오타 | 환경변수 확인, 새 터미널 재실행 |
| `PERMISSION_DENIED` | 서비스 계정에 Vision 역할 없음 | IAM > Role: Vision API User 부여 |
| `quotaExceeded` | 월 1,000 무료 요청 초과 | 가격표 확인·쿼터 상향 신청 |
| `400 PDF size too large` | 20 MB+ PDF | PyMuPDF 분할 후 페이지별 OCR |

---

## 💰 비용 최적화 팁

### 1. 무료 할당량
- **월 1,000회** 무료 API 호출
- **텍스트 감지**: 무료
- **문서 텍스트 감지**: $1.50/1,000 페이지

### 2. 비용 절약 방법
- **PyMuPDF 텍스트 레이어 검사**: PDF에 텍스트 레이어가 있으면 GCV 호출 생략
- **이미지 크기 최적화**: 5MB 이하로 압축
- **배치 처리**: 여러 이미지를 한 번에 처리

### 3. 모니터링
- **Google Cloud Console** → **APIs & Services** → **Dashboard**에서 사용량 확인
- **Billing** → **Reports**에서 비용 추적

---

## 🔗 관련 링크

- [Cloud Vision API 문서](https://cloud.google.com/vision/docs)
- [인증 가이드](https://cloud.google.com/vision/docs/authentication)
- [가격표](https://cloud.google.com/vision/pricing)
- [API 할당량](https://cloud.google.com/vision/quotas)

---

## 📞 지원

설정 중 문제가 발생하면:
1. 오류 메시지 전체 복사
2. `test_gcv_setup.py` 실행 결과
3. 환경변수 설정 상태

위 정보와 함께 문의해주세요. 