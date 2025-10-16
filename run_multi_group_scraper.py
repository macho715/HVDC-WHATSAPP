#!/usr/bin/env python3
"""MACHO-GPT v3.4-mini Multi-Group WhatsApp Scraper CLI
멀티 그룹 스크래핑 실행 스크립트/Multigroup scraping runner script."""

import argparse
import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가/Add project root to import path.
sys.path.insert(0, str(Path(__file__).parent))

from macho_gpt.async_scraper.group_config import MultiGroupConfig
from macho_gpt.async_scraper.multi_group_manager import MultiGroupManager

DEFAULT_LOG_PATH = Path("logs") / "multi_group_scraper.log"

logger = logging.getLogger(__name__)


def setup_logging(log_file: Path = DEFAULT_LOG_PATH) -> logging.Logger:
    """로그 설정 초기화/Initialize logging configuration."""

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)
        handler.close()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)

    module_logger = logging.getLogger(__name__)
    module_logger.setLevel(logging.INFO)
    return module_logger


def print_banner() -> None:
    """배너 출력/Print CLI banner."""
    banner = """
===============================================================
                                                              
         MACHO-GPT v3.4-mini Multi-Group WhatsApp Scraper    
                                                              
     Samsung C&T Logistics · HVDC Project · ADNOC·DSV Partnership    
                                                              
===============================================================
    """
    print(banner)


def print_config_summary(config: MultiGroupConfig) -> None:
    """설정 요약 출력/Print configuration summary."""
    print("\n**Multi-Group Configuration Summary**")
    print(f"   총 그룹 수: {len(config.whatsapp_groups)}")
    print(f"   최대 병렬 처리: {config.scraper_settings.max_parallel_groups}")
    print(f"   헤드리스 모드: {config.scraper_settings.headless}")
    print(f"   AI 통합: {'활성화' if config.ai_integration.enabled else '비활성화'}")

    print("\n**Groups to Scrape:**")
    for idx, group in enumerate(config.whatsapp_groups, 1):
        priority_icon = {"HIGH": "[HIGH]", "MEDIUM": "[MED]", "LOW": "[LOW]"}.get(
            group.priority, "[N/A]"
        )
        print(
            f"   {idx}. {priority_icon} {group.name} (간격: {group.scrape_interval}초, 우선순위: {group.priority})"
        )


def print_results(results: list) -> None:
    """실행 결과 출력/Print execution results."""
    print("\n" + "=" * 80)
    print("**Scraping Results Summary**")
    print("=" * 80)

    total_groups = len(results)
    successful = sum(1 for r in results if r.get("success"))
    failed = total_groups - successful
    total_messages = sum(r.get("messages_scraped", 0) for r in results)

    print(f"\n[SUCCESS] 총 그룹 수: {total_groups}")
    print(f"[SUCCESS] 성공: {successful}")
    print(f"[FAILED] 실패: {failed}")
    print(f"[INFO] 총 메시지 수: {total_messages}")

    print("\n" + "-" * 80)
    print("**Detailed Results:**")
    print("-" * 80)

    for idx, result in enumerate(results, 1):
        status_icon = "[SUCCESS]" if result.get("success") else "[FAILED]"
        group_name = result.get("group_name", "Unknown")
        messages = result.get("messages_scraped", 0)
        error = result.get("error", "")

        print(f"\n{idx}. {status_icon} {group_name}")
        print(f"   메시지: {messages}개")

        if error:
            print(f"   [WARNING] 오류: {error}")

        if result.get("ai_summary"):
            print(f"   [AI] AI 요약 생성 완료")


async def main() -> int:
    """메인 실행 함수/Run CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="MACHO-GPT Multi-Group WhatsApp Scraper"
    )
    parser.add_argument(
        "--config",
        "-c",
        default="configs/multi_group_config.yaml",
        help="YAML 설정 파일 경로 (기본: configs/multi_group_config.yaml)",
    )
    parser.add_argument(
        "--limited-parallel",
        action="store_true",
        help="제한된 병렬 처리 모드 (배치 단위 실행)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="설정만 확인하고 실행하지 않음",
    )

    args = parser.parse_args()

    # 로깅 초기화
    setup_logging()

    # 배너 출력
    print_banner()

    try:
        # 설정 로드
        logger.info(f"Loading configuration from: {args.config}")
        config = MultiGroupConfig.load_from_yaml(args.config)

        # 설정 검증
        config.validate()
        logger.info("Configuration validated successfully")

        # 설정 요약 출력
        print_config_summary(config)

        # Dry-run 모드
        if args.dry_run:
            print("\n[SUCCESS] Dry-run completed successfully (no actual scraping)")
            return 0

        # 매니저 생성
        logger.info("Creating MultiGroupManager...")
        manager = MultiGroupManager(
            group_configs=config.whatsapp_groups,
            max_parallel_groups=config.scraper_settings.max_parallel_groups,
            ai_integration=config.ai_integration,
            scraper_settings=config.scraper_settings,
        )

        # 실행
        print(
            f"\n[START] Starting scraping at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}..."
        )
        print("   (Press Ctrl+C to stop)\n")

        if args.limited_parallel:
            logger.info("Running in limited parallel mode")
            results = await manager.run_limited_parallel()
        else:
            logger.info("Running in full parallel mode")
            results = await manager.run_all_groups()

        # 결과 출력
        print_results(results)

        # 통계 출력
        stats = manager.get_stats()
        print("\n" + "=" * 80)
        print("**System Statistics**")
        print("=" * 80)
        print(f"실행 시간: {stats.get('runtime_seconds', 0):.1f}초")
        print(f"완료된 사이클: {stats.get('completed_cycles', 0)}")
        print(f"총 메시지: {stats.get('total_messages', 0)}")
        print(f"오류 횟수: {stats.get('errors', 0)}")

        print("\n[SUCCESS] **Multi-group scraping completed successfully!**\n")

        return 0

    except KeyboardInterrupt:
        print("\n\n[WARNING] Scraping interrupted by user")
        logger.info("Scraping interrupted by user")
        return 130

    except FileNotFoundError:
        print(f"\n[ERROR] **Error:** Configuration file not found: {args.config}")
        print("   Please create a configuration file or specify a valid path.")
        logger.error(f"Configuration file not found: {args.config}")
        return 1

    except ValueError as e:
        print(f"\n[ERROR] **Configuration Error:** {e}")
        print("   Please check your configuration file for errors.")
        logger.error(f"Configuration validation error: {e}")
        return 1

    except Exception as e:
        print(f"\n[ERROR] **Fatal Error:** {e}")
        logger.exception("Fatal error in multi-group scraper")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
