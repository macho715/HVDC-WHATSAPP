"""
멀티 그룹 병렬 처리 매니저
여러 WhatsApp 그룹을 동시에 스크래핑
"""

import asyncio
import logging
import signal
import sys
from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from integrations.apify_client import actor_call

from .async_scraper import AsyncGroupScraper
from .group_config import (
    ApifyFallbackSettings,
    GroupConfig,
    MultiGroupConfig,
    ScraperSettings,
)

logger = logging.getLogger(__name__)


class MultiGroupManager:
    """
    멀티 그룹 병렬 스크래핑 매니저

    Features:
    - 여러 그룹 동시 스크래핑
    - 개별 그룹별 설정
    - 통합 에러 핸들링
    - AI 요약 통합
    - Graceful shutdown
    """

    def __init__(
        self,
        group_configs: List[GroupConfig],
        max_parallel_groups: int = 5,
        ai_integration: Optional[Dict[str, Any]] = None,
        apify_fallback: Optional[ApifyFallbackSettings] = None,
        scraper_settings: Optional[ScraperSettings] = None,
    ):
        """
        Args:
            group_configs: 스크래핑할 그룹 설정 리스트 / Group configuration list.
            max_parallel_groups: 최대 병렬 처리 그룹 수 / Max parallel groups.
            ai_integration: AI 통합 설정 / AI integration options.
            apify_fallback: Apify 폴백 설정 / Apify fallback settings.
            scraper_settings: 스크래퍼 설정 / Scraper settings.
        """
        self.group_configs = group_configs
        self.scraper_settings = (
            scraper_settings
            if scraper_settings is not None
            else ScraperSettings(max_parallel_groups=max_parallel_groups)
        )
        self.max_parallel_groups = min(
            self.scraper_settings.max_parallel_groups, len(group_configs)
        )
        if ai_integration is None:
            self.ai_integration: Dict[str, Any] = {}
        elif is_dataclass(ai_integration):
            self.ai_integration = asdict(ai_integration)
        else:
            self.ai_integration = dict(ai_integration)
        self.apify_fallback = apify_fallback or ApifyFallbackSettings()

        # 스크래퍼 인스턴스들
        self.scrapers: Dict[str, AsyncGroupScraper] = {}

        # 상태 관리
        self.is_running = False
        self.tasks: List[asyncio.Task[Any]] = []

        # 통계
        self.stats = {
            "total_groups": len(group_configs),
            "active_groups": 0,
            "completed_cycles": 0,
            "total_messages": 0,
            "errors": 0,
            "start_time": None,
        }

        logger.info(f"MultiGroupManager initialized with {len(group_configs)} groups")

    def _create_scraper(self, group_config: GroupConfig) -> AsyncGroupScraper:
        """
        개별 그룹용 스크래퍼 생성

        Args:
            group_config: 그룹 설정

        Returns:
            AsyncGroupScraper: 스크래퍼 인스턴스
        """
        scraper = AsyncGroupScraper(
            group_config=group_config,
            chrome_data_dir=self.scraper_settings.chrome_data_dir,
            headless=self.scraper_settings.headless,
            timeout=self.scraper_settings.timeout,
            ai_integration=self.ai_integration,
            storage_state_path=self.scraper_settings.auth_state_path,
        )

        return scraper

    async def _scrape_group(self, group_config: GroupConfig) -> Dict[str, Any]:
        """
        단일 그룹 스크래핑 (독립 태스크)

        Args:
            group_config: 그룹 설정

        Returns:
            Dict: 실행 결과
        """
        result = {
            "group_name": group_config.name,
            "success": False,
            "messages_scraped": 0,
            "ai_summary": None,
            "error": None,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
        }

        scraper = None

        try:
            # 스크래퍼 생성
            scraper = self._create_scraper(group_config)
            self.scrapers[group_config.name] = scraper

            logger.info(f"Starting scraper for group: {group_config.name}")
            self.stats["active_groups"] += 1

            # 스크래핑 실행
            await scraper.run()

            result["success"] = True
            logger.info(
                f"Scraper completed successfully for group: {group_config.name}"
            )

        except asyncio.CancelledError:
            logger.info(f"Scraper cancelled for group: {group_config.name}")
            result["error"] = "cancelled"

        except Exception as e:
            logger.error(
                "Error scraping group %s: %s", group_config.name, e, exc_info=True
            )
            result["error"] = str(e)
            self.stats["errors"] += 1

            fallback_result = await self._handle_apify_fallback(group_config, e)
            if fallback_result:
                result.update(fallback_result)

        finally:
            # 클린업
            if scraper:
                await scraper.close()

            if group_config.name in self.scrapers:
                del self.scrapers[group_config.name]

            self.stats["active_groups"] -= 1
            result["end_time"] = datetime.now().isoformat()

        return result

    async def _handle_apify_fallback(
        self, group_config: GroupConfig, original_error: Exception
    ) -> Dict[str, Any]:
        """Apify 폴백 처리 / Handle Apify fallback invocation."""

        if not self.apify_fallback.enabled:
            return {}

        if not self.apify_fallback.actor_id:
            logger.warning(
                "Apify fallback requested for %s but actor_id is missing",
                group_config.name,
            )
            return {}

        logger.info(
            "Attempting Apify fallback for group %s via actor %s",
            group_config.name,
            self.apify_fallback.actor_id,
        )

        payload = self._build_apify_payload(group_config, original_error)

        try:
            fallback_output = await asyncio.to_thread(
                actor_call,
                self.apify_fallback.actor_id,
                payload,
                token_env=self.apify_fallback.token_env,
                timeout_seconds=self.apify_fallback.timeout_seconds,
            )
        except Exception as fallback_error:  # pragma: no cover - network interaction
            logger.error(
                "Apify fallback failed for group %s: %s",
                group_config.name,
                fallback_error,
                exc_info=True,
            )
            return {}

        remote_messages = self._extract_remote_messages(
            fallback_output.get("items", [])
        )

        logger.info(
            "Apify fallback succeeded for group %s with %d messages",
            group_config.name,
            len(remote_messages),
        )

        return {
            "success": True,
            "fallback_used": "apify",
            "remote_messages": remote_messages,
            "messages_scraped": len(remote_messages),
            "apify_run": {
                "actor_id": self.apify_fallback.actor_id,
                "run_id": fallback_output.get("run", {}).get("id"),
                "status": fallback_output.get("run", {}).get("status"),
                "dataset_items": len(fallback_output.get("items", [])),
            },
            "original_error": str(original_error),
        }

    def _build_apify_payload(
        self, group_config: GroupConfig, original_error: Exception
    ) -> Dict[str, Any]:
        """Apify 입력 구성 / Build Apify input payload."""

        payload = {
            "group_name": group_config.name,
            "save_file": group_config.save_file,
            "requested_at": datetime.utcnow().isoformat() + "Z",
            "error_message": str(original_error),
        }
        payload.update(self.apify_fallback.input_overrides)
        return payload

    @staticmethod
    def _extract_remote_messages(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apify 데이터셋 메시지 추출 / Normalize remote dataset messages."""

        messages: List[Dict[str, Any]] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            if "messages" in item and isinstance(item["messages"], list):
                messages.extend(
                    msg for msg in item["messages"] if isinstance(msg, dict)
                )
            else:
                messages.append(item)
        return messages

    async def start_all_scrapers(self) -> None:
        """모든 스크래퍼 시작"""
        logger.info(f"Starting all scrapers for {len(self.group_configs)} groups")

        for group_config in self.group_configs:
            scraper = self._create_scraper(group_config)
            self.scrapers[group_config.name] = scraper
            logger.info(f"Created scraper for group: {group_config.name}")

    async def run_all_scrapers(self) -> List[Dict[str, Any]]:
        """모든 스크래퍼 실행 (run_all_groups의 별칭)"""
        return await self.run_all_groups()

    async def run_all_groups(self) -> List[Dict[str, Any]]:
        """
        모든 그룹을 병렬로 스크래핑

        Returns:
            List[Dict]: 각 그룹의 실행 결과
        """
        logger.info(f"Starting parallel scraping for {len(self.group_configs)} groups")
        self.is_running = True
        self.stats["start_time"] = datetime.now().isoformat()

        try:
            # 모든 그룹에 대한 태스크 생성
            tasks = []
            for group_config in self.group_configs:
                task = asyncio.create_task(self._scrape_group(group_config))
                tasks.append(task)
                self.tasks.append(task)

            # 모든 태스크 병렬 실행
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # 결과 처리
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    processed_results.append(
                        {
                            "group_name": self.group_configs[i].name,
                            "success": False,
                            "error": str(result),
                            "start_time": datetime.now().isoformat(),
                            "end_time": datetime.now().isoformat(),
                        }
                    )
                    self.stats["errors"] += 1
                else:
                    processed_results.append(result)
                    if result.get("success"):
                        self.stats["completed_cycles"] += 1
                        self.stats["total_messages"] += result.get(
                            "messages_scraped", 0
                        )

            return processed_results

        except KeyboardInterrupt:
            logger.info("Multi-group scraping interrupted by user")
            return []

        except Exception as e:
            logger.error(f"Fatal error in multi-group scraping: {e}")
            raise

        finally:
            self.is_running = False
            await self.cleanup()

    async def run_limited_parallel(self) -> List[Dict[str, Any]]:
        """
        제한된 병렬 처리로 그룹 스크래핑

        Returns:
            List[Dict]: 각 그룹의 실행 결과
        """
        logger.info(
            f"Starting limited parallel scraping (max {self.max_parallel_groups} groups)"
        )
        self.is_running = True
        self.stats["start_time"] = datetime.now().isoformat()

        results = []

        try:
            # 그룹을 배치로 나누어 처리
            for i in range(0, len(self.group_configs), self.max_parallel_groups):
                batch_end = i + self.max_parallel_groups
                batch = self.group_configs[i:batch_end]

                logger.info(
                    f"Processing batch {i//self.max_parallel_groups + 1}: {[g.name for g in batch]}"
                )

                # 배치 내 그룹들을 병렬 처리
                batch_tasks = [
                    asyncio.create_task(self._scrape_group(group)) for group in batch
                ]
                batch_results = await asyncio.gather(
                    *batch_tasks, return_exceptions=True
                )

                # 결과 처리
                for j, result in enumerate(batch_results):
                    if isinstance(result, Exception):
                        results.append(
                            {
                                "group_name": batch[j].name,
                                "success": False,
                                "error": str(result),
                                "start_time": datetime.now().isoformat(),
                                "end_time": datetime.now().isoformat(),
                            }
                        )
                        self.stats["errors"] += 1
                    else:
                        results.append(result)
                        if result.get("success"):
                            self.stats["completed_cycles"] += 1
                            self.stats["total_messages"] += result.get(
                                "messages_scraped", 0
                            )

                # 배치 간 대기 (리소스 정리)
                if i + self.max_parallel_groups < len(self.group_configs):
                    await asyncio.sleep(2)

            return results

        except KeyboardInterrupt:
            logger.info("Limited parallel scraping interrupted by user")
            return results

        except Exception as e:
            logger.error(f"Fatal error in limited parallel scraping: {e}")
            raise

        finally:
            self.is_running = False
            await self.cleanup()

    async def stop_all(self) -> None:
        """모든 스크래퍼 중지"""
        logger.info("Stopping all scrapers...")
        self.is_running = False

        # 모든 태스크 취소
        for task in self.tasks:
            if not task.done():
                task.cancel()

        # 모든 스크래퍼 중지
        for group_name, scraper in self.scrapers.items():
            try:
                scraper.stop()
                await scraper.close()
                logger.info(f"Stopped scraper for: {group_name}")
            except Exception as e:
                logger.error(f"Error stopping scraper {group_name}: {e}")

        # 태스크 정리
        self.tasks.clear()
        self.scrapers.clear()

    async def shutdown(self) -> None:
        """시스템 종료 (cleanup의 별칭)"""
        await self.cleanup()

    async def cleanup(self) -> None:
        """리소스 정리"""
        try:
            await self.stop_all()
            logger.info("MultiGroupManager cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """현재 통계 반환"""
        current_time = datetime.now()
        if self.stats["start_time"]:
            start_time = datetime.fromisoformat(self.stats["start_time"])
            self.stats["runtime_seconds"] = (current_time - start_time).total_seconds()
        else:
            self.stats["runtime_seconds"] = 0

        return self.stats.copy()

    def get_status(self) -> Dict[str, Any]:
        """현재 상태 반환"""
        return {
            "is_running": self.is_running,
            "active_groups": len(self.scrapers),
            "total_groups": len(self.group_configs),
            "stats": self.get_stats(),
        }


async def main():
    """CLI 실행 예제"""
    import argparse
    import json

    from .group_config import MultiGroupConfig

    parser = argparse.ArgumentParser(description="Multi-Group WhatsApp Scraper")
    parser.add_argument(
        "--config", "-c", required=True, help="YAML config file with group settings"
    )
    parser.add_argument(
        "--max-parallel", type=int, default=5, help="Maximum parallel groups"
    )
    parser.add_argument(
        "--limited-parallel",
        action="store_true",
        help="Use limited parallel processing",
    )

    args = parser.parse_args()

    try:
        # 설정 로드
        config = MultiGroupConfig.load_from_yaml(args.config)
        config.validate()

        # 매니저 생성
        manager = MultiGroupManager(
            group_configs=config.whatsapp_groups,
            max_parallel_groups=args.max_parallel,
            ai_integration=config.ai_integration.__dict__,
        )

        # 시그널 핸들러 설정
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down...")
            asyncio.create_task(manager.stop_all())

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # 실행
        if args.limited_parallel:
            results = await manager.run_limited_parallel()
        else:
            results = await manager.run_all_groups()

        # 결과 출력
        print(f"\n=== Scraping Results ===")
        print(f"Total groups: {len(results)}")
        print(f"Successful: {sum(1 for r in results if r.get('success'))}")
        print(f"Failed: {sum(1 for r in results if not r.get('success'))}")
        print(f"Total messages: {sum(r.get('messages_scraped', 0) for r in results)}")

        # 통계 출력
        stats = manager.get_stats()
        print(f"\n=== Statistics ===")
        print(f"Runtime: {stats.get('runtime_seconds', 0):.2f} seconds")
        print(f"Completed cycles: {stats.get('completed_cycles', 0)}")
        print(f"Total messages: {stats.get('total_messages', 0)}")
        print(f"Errors: {stats.get('errors', 0)}")

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        if "manager" in locals():
            await manager.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
