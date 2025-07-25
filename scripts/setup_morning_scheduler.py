#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini Morning Report Scheduler Setup
Samsung C&T Logistics · HVDC Project

Windows 작업 스케줄러에 아침 보고서 시스템을 등록하는 스크립트
"""

import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def create_batch_file():
    """배치 파일 생성 / Create batch file"""
    try:
        # 현재 디렉토리 경로
        current_dir = Path.cwd()
        python_exe = sys.executable
        
        # 배치 파일 내용
        batch_content = f"""@echo off
cd /d "{current_dir}"
echo MACHO-GPT v3.4-mini 아침 보고서 실행 중...
echo 실행 시간: %date% %time%
"{python_exe}" scripts/morning_report_system.py --test
echo 아침 보고서 생성 완료: %date% %time%
pause
"""
        
        # 배치 파일 저장
        batch_file = current_dir / "run_morning_report.bat"
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"✅ 배치 파일 생성 완료: {batch_file}")
        return str(batch_file)
        
    except Exception as e:
        print(f"❌ 배치 파일 생성 오류: {e}")
        return None


def create_powershell_script():
    """PowerShell 스크립트 생성 / Create PowerShell script"""
    try:
        current_dir = Path.cwd()
        
        ps_content = f"""
# MACHO-GPT v3.4-mini Morning Report Monitor
# Samsung C&T Logistics · HVDC Project

$LogFile = "{current_dir}\\logs\\scheduler_monitor.log"
$ReportDir = "{current_dir}\\reports\\morning_reports"

# 로그 디렉토리 생성
if (!(Test-Path "{current_dir}\\logs")) {{
    New-Item -ItemType Directory -Path "{current_dir}\\logs" -Force
}}

# 로그 함수
function Write-Log {{
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    Write-Host $logMessage
    Add-Content -Path $LogFile -Value $logMessage
}}

# 모니터링 시작
Write-Log "MACHO-GPT v3.4-mini 아침 보고서 모니터링 시작"

while ($true) {{
    try {{
        $currentTime = Get-Date
        $morningTime = Get-Date "07:00"
        
        # 아침 7시에 실행
        if ($currentTime.Hour -eq 7 -and $currentTime.Minute -eq 0) {{
            Write-Log "아침 보고서 생성 시작"
            
            # Python 스크립트 실행
            $pythonExe = "{sys.executable}"
            $scriptPath = "{current_dir}\\scripts\\morning_report_system.py"
            
            $result = & $pythonExe $scriptPath --test
            
            if ($LASTEXITCODE -eq 0) {{
                Write-Log "아침 보고서 생성 성공"
                
                # 최신 보고서 확인
                $latestReport = Get-ChildItem $ReportDir -Filter "*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
                if ($latestReport) {{
                    Write-Log "최신 보고서: $($latestReport.Name)"
                }}
            }} else {{
                Write-Log "아침 보고서 생성 실패"
            }}
        }}
        
        # 1분 대기
        Start-Sleep -Seconds 60
        
    }} catch {{
        Write-Log "모니터링 오류: $($_.Exception.Message)"
        Start-Sleep -Seconds 60
    }}
}}
"""
        
        ps_file = current_dir / "monitor_morning_report.ps1"
        with open(ps_file, 'w', encoding='utf-8') as f:
            f.write(ps_content)
        
        print(f"✅ PowerShell 스크립트 생성 완료: {ps_file}")
        return str(ps_file)
        
    except Exception as e:
        print(f"❌ PowerShell 스크립트 생성 오류: {e}")
        return None


def setup_windows_scheduler():
    """Windows 작업 스케줄러 설정 / Setup Windows Task Scheduler"""
    try:
        print("🔄 Windows 작업 스케줄러 설정 중...")
        
        # 배치 파일 생성
        batch_file = create_batch_file()
        if not batch_file:
            return False
        
        # 작업 스케줄러 명령어
        task_name = "MACHO-GPT-Morning-Report"
        task_command = f'schtasks /create /tn "{task_name}" /tr "{batch_file}" /sc daily /st 07:00 /ru System /f'
        
        print(f"📋 작업 스케줄러 명령어:")
        print(f"   {task_command}")
        
        # 사용자에게 실행 여부 확인
        response = input("\n작업 스케줄러에 등록하시겠습니까? (y/n): ").lower().strip()
        
        if response == 'y':
            # 관리자 권한으로 실행
            result = subprocess.run(task_command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 작업 스케줄러 등록 성공!")
                print(f"📅 작업 이름: {task_name}")
                print(f"⏰ 실행 시간: 매일 오전 7시")
                print(f"📁 실행 파일: {batch_file}")
                return True
            else:
                print(f"❌ 작업 스케줄러 등록 실패:")
                print(f"   오류: {result.stderr}")
                return False
        else:
            print("ℹ️ 작업 스케줄러 등록을 건너뜁니다.")
            return False
            
    except Exception as e:
        print(f"❌ Windows 스케줄러 설정 오류: {e}")
        return False


def create_manual_scheduler():
    """수동 스케줄러 생성 / Create manual scheduler"""
    try:
        current_dir = Path.cwd()
        python_exe = sys.executable
        
        scheduler_content = f"""#!/usr/bin/env python3
\"\"\"
MACHO-GPT v3.4-mini Manual Morning Report Scheduler
Samsung C&T Logistics · HVDC Project

수동으로 실행할 수 있는 아침 보고서 스케줄러
\"\"\"

import schedule
import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_morning_report():
    \"\"\"아침 보고서 실행 / Run morning report\"\"\"
    try:
        print(f"[{{datetime.now()}}] 아침 보고서 생성 시작...")
        
        # Python 스크립트 실행
        script_path = Path(__file__).parent / "morning_report_system.py"
        result = subprocess.run([
            sys.executable, str(script_path), "--test"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[{{datetime.now()}}] 아침 보고서 생성 성공!")
        else:
            print(f"[{{datetime.now()}}] 아침 보고서 생성 실패: {{result.stderr}}")
            
    except Exception as e:
        print(f"[{{datetime.now()}}] 아침 보고서 실행 오류: {{e}}")

def main():
    \"\"\"메인 함수 / Main function\"\"\"
    print("🤖 MACHO-GPT v3.4-mini 수동 스케줄러 시작")
    print("📅 매일 오전 7시에 아침 보고서를 생성합니다.")
    print("⏹️  종료하려면 Ctrl+C를 누르세요.")
    
    # 매일 오전 7시에 실행
    schedule.every().day.at("07:00").do(run_morning_report)
    
    # 테스트용: 1분 후 실행
    schedule.every(1).minutes.do(run_morning_report)
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except KeyboardInterrupt:
            print("\\n👋 스케줄러를 종료합니다.")
            break
        except Exception as e:
            print(f"스케줄러 오류: {{e}}")
            time.sleep(60)

if __name__ == "__main__":
    main()
"""
        
        scheduler_file = current_dir / "scripts" / "manual_morning_scheduler.py"
        with open(scheduler_file, 'w', encoding='utf-8') as f:
            f.write(scheduler_content)
        
        print(f"✅ 수동 스케줄러 생성 완료: {scheduler_file}")
        return str(scheduler_file)
        
    except Exception as e:
        print(f"❌ 수동 스케줄러 생성 오류: {e}")
        return None


def show_usage_instructions():
    """사용법 안내 / Show usage instructions"""
    print("\n" + "="*60)
    print("📋 MACHO-GPT v3.4-mini 아침 보고서 스케줄러 사용법")
    print("="*60)
    
    print("\n🚀 방법 1: Windows 작업 스케줄러 (권장)")
    print("   1. 관리자 권한으로 PowerShell 실행")
    print("   2. python scripts/setup_morning_scheduler.py 실행")
    print("   3. 'y' 입력하여 스케줄러 등록")
    print("   4. 매일 오전 7시 자동 실행")
    
    print("\n🖥️ 방법 2: 수동 스케줄러")
    print("   1. python scripts/manual_morning_scheduler.py 실행")
    print("   2. 백그라운드에서 계속 실행")
    print("   3. 매일 오전 7시 자동 실행")
    
    print("\n⚡ 방법 3: 즉시 실행")
    print("   1. python scripts/morning_report_system.py --test")
    print("   2. 즉시 아침 보고서 생성")
    
    print("\n📊 생성되는 파일:")
    print("   - reports/morning_reports/morning_report_YYYYMMDD_HHMMSS.json")
    print("   - reports/morning_reports/morning_report_YYYYMMDD_HHMMSS.html")
    print("   - logs/morning_report.log")
    
    print("\n🔧 설정 옵션:")
    print("   - 이메일 전송: 환경변수 SENDER_EMAIL, SENDER_PASSWORD 설정")
    print("   - 채팅방 변경: scripts/morning_report_system.py에서 target_chats 수정")
    print("   - 실행 시간 변경: 스케줄러 설정에서 시간 수정")
    
    print("\n" + "="*60)


def main():
    """메인 함수 / Main function"""
    print("🤖 MACHO-GPT v3.4-mini 아침 보고서 스케줄러 설정")
    print("Samsung C&T Logistics · HVDC Project")
    print("="*50)
    
    # 필요한 디렉토리 생성
    Path("logs").mkdir(exist_ok=True)
    Path("reports/morning_reports").mkdir(parents=True, exist_ok=True)
    Path("data/conversations").mkdir(parents=True, exist_ok=True)
    
    print("✅ 필요한 디렉토리 생성 완료")
    
    # 배치 파일 생성
    batch_file = create_batch_file()
    
    # PowerShell 스크립트 생성
    ps_file = create_powershell_script()
    
    # 수동 스케줄러 생성
    scheduler_file = create_manual_scheduler()
    
    # Windows 작업 스케줄러 설정
    if os.name == 'nt':  # Windows 환경
        setup_windows_scheduler()
    else:
        print("ℹ️ Windows가 아닌 환경입니다. 수동 스케줄러를 사용하세요.")
    
    # 사용법 안내
    show_usage_instructions()
    
    print("\n🎉 스케줄러 설정 완료!")
    print("📧 문의사항: tech-support@samsung-ct.com")


if __name__ == "__main__":
    main() 