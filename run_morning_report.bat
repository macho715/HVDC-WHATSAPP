@echo off
cd /d "C:\cursor-mcp\whatsapp"
echo MACHO-GPT v3.4-mini 아침 보고서 실행 중...
echo 실행 시간: %date% %time%
"C:\Users\minky\anaconda3\python.exe" scripts/morning_report_system.py --test
echo 아침 보고서 생성 완료: %date% %time%
pause
