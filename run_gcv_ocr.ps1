# Google Cloud Vision OCR 실행 스크립트 (PowerShell)
# MACHO-GPT v3.4-mini

Write-Host "🤖 MACHO-GPT v3.4-mini Google Cloud Vision OCR 실행기" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# 환경변수 확인
$credentialsPath = $env:GOOGLE_APPLICATION_CREDENTIALS
if (-not $credentialsPath) {
    Write-Host "❌ ERROR: GOOGLE_APPLICATION_CREDENTIALS 환경변수가 설정되지 않았습니다." -ForegroundColor Red
    Write-Host ""
    Write-Host "📋 설정 방법:" -ForegroundColor Yellow
    Write-Host "1. Google Cloud Console에서 서비스 계정 JSON 키 다운로드"
    Write-Host "2. 환경변수 설정: [Environment]::SetEnvironmentVariable('GOOGLE_APPLICATION_CREDENTIALS', 'C:\path\to\vision-sa.json', 'User')"
    Write-Host "3. 새 PowerShell에서 다시 실행"
    Write-Host ""
    Read-Host "아무 키나 누르면 종료"
    exit 1
}

# 파일 존재 확인
if (-not (Test-Path $credentialsPath)) {
    Write-Host "❌ ERROR: 서비스 계정 JSON 파일을 찾을 수 없습니다." -ForegroundColor Red
    Write-Host "파일 경로: $credentialsPath" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "아무 키나 누르면 종료"
    exit 1
}

Write-Host "✅ 환경변수 확인 완료: $credentialsPath" -ForegroundColor Green
Write-Host ""

# Python 실행
Write-Host "🚀 WhatsApp 미디어 OCR 추출 시작..." -ForegroundColor Green
python whatsapp_media_ocr_extractor.py --media-only --ocr-engine gcv $args

Write-Host ""
Write-Host "✅ 실행 완료" -ForegroundColor Green
Read-Host "아무 키나 누르면 종료" 

