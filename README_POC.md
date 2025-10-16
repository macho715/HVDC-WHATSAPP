# HVDC WhatsApp Baileys Actor (PoC)

## 개요

Baileys(WhatsApp Web API) 기반 WhatsApp 메시지 수집을 위한 Apify Actor입니다. Playwright 기반 시스템의 post_logout 문제에 대한 대안으로 구현되었습니다.

## 빠른 시작

### 1. Apify Console에서 빌드

1. **Actor 생성**: Apify Console에서 새 Actor 생성
2. **소스 연결**: Git 저장소 연결 (이 프로젝트)
3. **빌드 실행**: "Build now" 클릭

### 2. 환경변수 설정

**Secrets** (Environment Variables):
- `WEBHOOK_URL`: @pocWebhookUrl (웹훅 URL을 Secret으로 등록)
- `SESSION_KV_KEY`: baileys_session (기본값)
- `PAIR_MODE`: qr (기본값)

**Secret 등록 방법**:
```bash
apify secrets add pocWebhookUrl https://your-webhook-endpoint.com/webhook
```

### 3. Input 설정

**콘솔 Input 폼**:
- `allowedGroupIds`: 수집 허용 그룹 JID (콤마 구분)
  - 예: `1203631xxxxxx@g.us,1203632yyyyyy@g.us`
- `keywordFilter`: 키워드 필터 (정규식, 선택사항)
  - 예: `(ETA|gate pass|invoice)`
- `forwardToWebhook`: 웹훅 전송 여부 (기본: true)

### 4. 실행 및 로그인

1. **Run 실행**: "Start" 버튼 클릭
2. **QR 스캔**: 로그에서 QR 코드 확인 후 WhatsApp으로 스캔
3. **연결 확인**: "WhatsApp connected" 메시지 확인
4. **메시지 수집**: 그룹 메시지가 Dataset에 저장되는지 확인

## 메시지 데이터 형식

```json
{
  "groupId": "1203631xxxxxx@g.us",
  "messageId": "3EB0C767D26A4A4A4A4A",
  "from": "971507529355@c.us",
  "ts": 1760631670.552,
  "text": "ETA for vessel ABC123 is 14:30",
  "hasMedia": false
}
```

## 웹훅 설정

### Integrations → Webhooks

1. **Run Succeeded**: 성공 시 알림
2. **Run Failed**: 실패 시 알림
3. **Ad-hoc Webhook**: 런별 커스텀 알림

### 웹훅 페이로드

```json
{
  "event": "wa.message",
  "data": {
    "groupId": "1203631xxxxxx@g.us",
    "messageId": "3EB0C767D26A4A4A4A4A",
    "from": "971507529355@c.us",
    "ts": 1760631670.552,
    "text": "ETA for vessel ABC123 is 14:30",
    "hasMedia": false
  }
}
```

## 스케줄 설정

### Console Schedules

1. **업무시간 실행**: `0 9-17 * * 1-5` (월-금 9-17시)
2. **실시간 모니터링**: `*/5 * * * *` (5분마다)
3. **야간 백업**: `0 2 * * *` (매일 새벽 2시)

### API로 스케줄 생성

```bash
curl -X POST "https://api.apify.com/v2/schedules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "actorId": "YOUR_ACTOR_ID",
    "cron": "0 9-17 * * 1-5",
    "title": "HVDC WhatsApp Business Hours"
  }'
```

## 로컬 개발

### 의존성 설치

```bash
cd apify_actor
npm install
```

### 빌드

```bash
npm run build
```

### 로컬 실행 (Apify CLI 필요)

```bash
apify run
```

## 문제 해결

### QR 코드가 나타나지 않는 경우

1. 환경변수 `PAIR_MODE=qr` 확인
2. 로그 레벨을 `DEBUG`로 변경
3. Actor 재시작

### 메시지가 수집되지 않는 경우

1. `allowedGroupIds`에 올바른 JID 입력 확인
2. 그룹 JID 형식: `숫자@g.us`
3. 키워드 필터가 너무 제한적인지 확인

### 연결이 자주 끊어지는 경우

1. `SESSION_KV_KEY`로 세션 상태 저장 확인
2. 네트워크 안정성 확인
3. WhatsApp 정책 준수 확인

## Playwright와의 통합

### Fallback 전략

1. **Primary**: Playwright (UI 자동화, 안정성)
2. **Fallback**: Baileys (API 기반, post_logout 회피)
3. **Switch 조건**: Playwright post_logout 감지 시

### 통합 예시

```python
# Python에서 Apify Actor 호출
import requests

def fallback_to_baileys():
    response = requests.post(
        "https://api.apify.com/v2/acts/YOUR_ACTOR_ID/runs",
        headers={"Authorization": "Bearer YOUR_API_TOKEN"},
        json={
            "allowedGroupIds": "1203631xxxxxx@g.us",
            "keywordFilter": "(ETA|gate pass|invoice)",
            "forwardToWebhook": True
        }
    )
    return response.json()
```

## 모니터링

### Apify Console

- **Runs**: 실행 이력 및 상태
- **Logs**: 실시간 로그 확인
- **Dataset**: 수집된 메시지 데이터
- **Key-Value Store**: 세션 상태 저장

### 메트릭

- **성공률**: Run 성공/실패 비율
- **메시지 수**: 수집된 메시지 개수
- **연결 시간**: WhatsApp 연결 유지 시간
- **에러율**: 메시지 처리 에러 비율

## 보안 고려사항

1. **Secret 관리**: 웹훅 URL을 Secret으로 안전하게 저장
2. **세션 보호**: Key-Value Store의 세션 데이터 암호화
3. **접근 제어**: 허용된 그룹만 수집 (화이트리스트)
4. **데이터 보존**: GDPR/개인정보보호법 준수

## 제한사항

1. **WhatsApp 정책**: 자동화 도구 사용 시 정책 위반 가능성
2. **초기 인증**: QR 스캔 수동 필요
3. **세션 관리**: Key-Value Store 의존성
4. **Node.js 전용**: Python 생태계와 분리

## 지원

- **문서**: [Baileys Wiki](https://baileys.wiki/)
- **Apify**: [Apify Documentation](https://docs.apify.com/)
- **이슈**: GitHub Issues 또는 HVDC 운영팀 문의
