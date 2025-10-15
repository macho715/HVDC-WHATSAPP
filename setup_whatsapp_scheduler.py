#!/usr/bin/env python3
"""WhatsApp 자동 추출 스케줄러 설정 / WhatsApp auto extraction scheduler setup"""

from __future__ import annotations

import argparse
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


TASK_NAME = "MACHO-GPT-WhatsApp-Auto-Extract"
DEFAULT_TIME = "18:00"
DEFAULT_ROOM = "MR.CHA 전용"


def is_windows() -> bool:
    """Windows OS 여부 확인 / Determine if current OS is Windows."""

    return platform.system().lower().startswith("win")


def validate_time_format(time_value: str) -> str:
    """HH:MM 형식 검증 / Validate HH:MM formatted time string."""

    try:
        datetime.strptime(time_value, "%H:%M")
    except ValueError as exc:  # pragma: no cover - defensive branch
        raise argparse.ArgumentTypeError(
            "시간은 HH:MM 형식이어야 합니다 / Time must follow HH:MM format"
        ) from exc
    return time_value


def create_batch_file(room: str, base_dir: Optional[Path] = None) -> Path:
    """Windows 배치 파일 생성 / Create Windows batch runner file."""

    working_dir = base_dir or Path.cwd()
    python_exe = sys.executable
    safe_room = room.replace('"', "'")
    batch_path = working_dir / "run_whatsapp_auto.bat"
    batch_content = (
        "@echo off\n"
        "chcp 65001 > nul\n"
        f"cd /d \"{working_dir}\"\n"
        "echo MACHO-GPT v3.4-mini WhatsApp 자동 추출 실행...\n"
        "echo 실행 시간: %date% %time%\n"
        f"\"{python_exe}\" extract_whatsapp_auto.py --run --room \"{safe_room}\"\n"
        "if %errorlevel% neq 0 (\n"
        "    echo ❌ 실행 실패: %errorlevel%\n"
        ") else (\n"
        "    echo ✅ 실행 완료\n"
        ")\n"
    )
    batch_path.write_text(batch_content, encoding="utf-8")
    return batch_path


def create_monitor_script(base_dir: Optional[Path] = None) -> Path:
    """PowerShell 모니터 스크립트 생성 / Create PowerShell monitor script."""

    working_dir = base_dir or Path.cwd()
    logs_dir = working_dir / "logs"
    reports_dir = working_dir / "reports" / "whatsapp_runs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    ps_path = working_dir / "monitor_whatsapp_scheduler.ps1"
    log_path = str(logs_dir).replace("\\", "\\\\")
    report_path = str(reports_dir).replace("\\", "\\\\")
    ps_content = f"""
# MACHO-GPT v3.4-mini WhatsApp Scheduler Monitor
$LogFile = "{log_path}\\scheduler_monitor.log"
$ReportDir = "{report_path}"

function Write-Log {{
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = "[$timestamp] $Message"
    Write-Host $entry
    Add-Content -Path $LogFile -Value $entry
}}

Write-Log "WhatsApp 자동 추출 모니터링 시작"

while ($true) {{
    try {{
        $latestReport = Get-ChildItem $ReportDir -Filter "*.json" -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 1

        if ($latestReport) {{
            Write-Log "최신 보고서: $($latestReport.Name)"
        }} else {{
            Write-Log "보고서가 아직 생성되지 않았습니다"
        }}
        Start-Sleep -Seconds 600
    }} catch {{
        Write-Log "모니터링 오류: $($_.Exception.Message)"
        Start-Sleep -Seconds 600
    }}
}}
"""
    ps_path.write_text(ps_content.strip() + "\n", encoding="utf-8")
    return ps_path


def build_task_command(batch_path: Path, run_time: str) -> str:
    """작업 스케줄러 명령 생성 / Build scheduler command string."""

    return (
        f'schtasks /create /tn "{TASK_NAME}" /tr "{batch_path}" '
        f"/sc daily /st {run_time} /f /rl HIGHEST"
    )


def register_scheduler(run_time: str, room: str) -> bool:
    """스케줄러 등록 / Register scheduler task."""

    if not is_windows():
        print("⚠️ Windows 환경에서만 스케줄러를 등록할 수 있습니다.")
        return False

    batch_file = create_batch_file(room)
    create_monitor_script()
    command = build_task_command(batch_file, run_time)

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        print("✅ WhatsApp 자동 추출 스케줄러 등록 완료")
        print(f"   작업 이름: {TASK_NAME}")
        print(f"   실행 시간: {run_time}")
        print(f"   실행 배치: {batch_file}")
        return True

    print("❌ 스케줄러 등록 실패")
    print(result.stderr.strip())
    return False


def show_status() -> bool:
    """스케줄러 상태 확인 / Show scheduler status."""

    if not is_windows():
        print("⚠️ Windows 환경에서만 스케줄러 상태를 확인할 수 있습니다.")
        return False

    command = f'schtasks /query /tn "{TASK_NAME}"'
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        print(result.stdout.strip())
        return True

    print("❌ 스케줄러 조회 실패")
    print(result.stderr.strip())
    return False


def remove_scheduler() -> bool:
    """스케줄러 제거 / Remove scheduler task."""

    if not is_windows():
        print("⚠️ Windows 환경에서만 스케줄러를 제거할 수 있습니다.")
        return False

    command = f'schtasks /delete /tn "{TASK_NAME}" /f'
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        print("✅ 스케줄러 제거 완료")
        return True

    print("❌ 스케줄러 제거 실패")
    print(result.stderr.strip())
    return False


def parse_arguments() -> argparse.Namespace:
    """명령행 인자 파싱 / Parse CLI arguments."""

    parser = argparse.ArgumentParser(
        description="WhatsApp 자동 추출 스케줄러 설정 / WhatsApp scheduler setup"
    )
    parser.add_argument("--setup", action="store_true", help="스케줄러 등록")
    parser.add_argument("--status", action="store_true", help="스케줄러 상태 확인")
    parser.add_argument("--remove", action="store_true", help="스케줄러 제거")
    parser.add_argument(
        "--time",
        type=validate_time_format,
        default=DEFAULT_TIME,
        help="실행 시간 (HH:MM)",
    )
    parser.add_argument(
        "--room",
        type=str,
        default=DEFAULT_ROOM,
        help="대상 채팅방 제목 / Target chat room title",
    )
    return parser.parse_args()


def main() -> None:
    """엔트리 포인트 / Script entry point."""

    args = parse_arguments()

    if args.status:
        show_status()
        return

    if args.remove:
        remove_scheduler()
        return

    if args.setup:
        register_scheduler(args.time, args.room)
        return

    print("ℹ️ 사용법: --setup, --status 또는 --remove 옵션을 지정하세요.")


if __name__ == "__main__":
    main()
