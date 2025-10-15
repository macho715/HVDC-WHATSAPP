"""setup_whatsapp_scheduler.py 테스트 / Tests for setup_whatsapp_scheduler.py"""

import argparse
from pathlib import Path

import pytest

from setup_whatsapp_scheduler import (
    TASK_NAME,
    build_task_command,
    create_batch_file,
    create_monitor_script,
    validate_time_format,
)


def test_validate_time_format_accepts_valid_time() -> None:
    """유효한 시간 형식 통과 / Accept valid HH:MM time."""

    assert validate_time_format("18:00") == "18:00"


def test_validate_time_format_rejects_invalid_time() -> None:
    """잘못된 시간 형식 예외 / Raise error on invalid time format."""

    with pytest.raises(argparse.ArgumentTypeError):
        validate_time_format("invalid")


def test_create_batch_file_writes_expected_content(tmp_path: Path) -> None:
    """배치 파일 내용 검증 / Ensure batch file contains run command."""

    batch_path = create_batch_file("테스트룸", base_dir=tmp_path)
    content = batch_path.read_text(encoding="utf-8")
    assert "extract_whatsapp_auto.py --run --room" in content
    assert "테스트룸" in content


def test_create_monitor_script_generates_files(tmp_path: Path) -> None:
    """모니터 스크립트와 디렉토리 생성 / Create monitor script and directories."""

    ps_path = create_monitor_script(base_dir=tmp_path)
    assert ps_path.exists()
    assert (tmp_path / "logs").is_dir()
    assert (tmp_path / "reports" / "whatsapp_runs").is_dir()


def test_build_task_command_contains_task_name(tmp_path: Path) -> None:
    """스케줄러 명령 텍스트 확인 / Ensure task command references task name."""

    batch_path = tmp_path / "run_whatsapp_auto.bat"
    batch_path.write_text("echo test", encoding="utf-8")
    command = build_task_command(batch_path, "18:00")
    assert TASK_NAME in command
    assert "18:00" in command
