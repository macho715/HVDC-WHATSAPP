
# MACHO-GPT v3.4-mini Morning Report Monitor
# Samsung C&T Logistics · HVDC Project

$LogFile = "C:\cursor-mcp\whatsapp\logs\scheduler_monitor.log"
$ReportDir = "C:\cursor-mcp\whatsapp\reports\morning_reports"

# 로그 디렉토리 생성
if (!(Test-Path "C:\cursor-mcp\whatsapp\logs")) {
    New-Item -ItemType Directory -Path "C:\cursor-mcp\whatsapp\logs" -Force
}

# 로그 함수
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    Write-Host $logMessage
    Add-Content -Path $LogFile -Value $logMessage
}

# 모니터링 시작
Write-Log "MACHO-GPT v3.4-mini 아침 보고서 모니터링 시작"

while ($true) {
    try {
        $currentTime = Get-Date
        $morningTime = Get-Date "07:00"
        
        # 아침 7시에 실행
        if ($currentTime.Hour -eq 7 -and $currentTime.Minute -eq 0) {
            Write-Log "아침 보고서 생성 시작"
            
            # Python 스크립트 실행
            $pythonExe = "C:\Users\minky\anaconda3\python.exe"
            $scriptPath = "C:\cursor-mcp\whatsapp\scripts\morning_report_system.py"
            
            $result = & $pythonExe $scriptPath --test
            
            if ($LASTEXITCODE -eq 0) {
                Write-Log "아침 보고서 생성 성공"
                
                # 최신 보고서 확인
                $latestReport = Get-ChildItem $ReportDir -Filter "*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
                if ($latestReport) {
                    Write-Log "최신 보고서: $($latestReport.Name)"
                }
            } else {
                Write-Log "아침 보고서 생성 실패"
            }
        }
        
        # 1분 대기
        Start-Sleep -Seconds 60
        
    } catch {
        Write-Log "모니터링 오류: $($_.Exception.Message)"
        Start-Sleep -Seconds 60
    }
}
