#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini Manual Morning Report Scheduler
Samsung C&T Logistics · HVDC Project

수동으로 실행할 수 있는 아침 보고서 스케줄러
"""

import schedule
import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_morning_report():
    """아침 보고서 실행 / Run morning report"""
    try:
        print(f"[{datetime.now()}] 아침 보고서 생성 시작...")
        
        # Python 스크립트 실행
        script_path = Path(__file__).parent / "morning_report_system.py"
        result = subprocess.run([
            sys.executable, str(script_path), "--test"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[{datetime.now()}] 아침 보고서 생성 성공!")
        else:
            print(f"[{datetime.now()}] 아침 보고서 생성 실패: {result.stderr}")
            
    except Exception as e:
        print(f"[{datetime.now()}] 아침 보고서 실행 오류: {e}")

def main():
    """메인 함수 / Main function"""
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
            print("\n👋 스케줄러를 종료합니다.")
            break
        except Exception as e:
            print(f"스케줄러 오류: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
