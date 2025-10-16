"""Apify 클라이언트 도우미 / Apify client helper utilities."""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv

try:  # pragma: no cover - optional dependency import
    from apify_client import ApifyClient as LoadedApifyClient
except ImportError:  # pragma: no cover - optional dependency import
    LoadedApifyClient = None


logger = logging.getLogger(__name__)


def actor_call(
    actor_id: str,
    input_payload: Dict[str, Any],
    *,
    token_env: str = "APIFY_TOKEN",
    timeout_seconds: Optional[int] = None,
) -> Dict[str, Any]:
    """Apify 액터 호출 / Invoke Apify actor and return run metadata with dataset."""

    load_dotenv()
    token = os.getenv(token_env)
    if not token:
        raise ValueError(f"환경변수 {token_env}에 Apify 토큰이 설정되지 않았습니다")

    if LoadedApifyClient is None:
        raise ImportError(
            "apify-client 패키지가 필요합니다. 'pip install apify-client'로 설치하세요."
        )

    client = LoadedApifyClient(token)
    logger.info("Calling Apify actor %s", actor_id)

    run = client.actor(actor_id).call(
        run_input=input_payload,
        wait_for_finish=True,
        timeout_secs=timeout_seconds,
    )

    dataset_items = []
    dataset_id = run.get("defaultDatasetId")
    if dataset_id:
        dataset = client.dataset(dataset_id)
        dataset_items = list(dataset.iterate_items())

    logger.info("Apify actor %s completed with status %s", actor_id, run.get("status"))

    return {"run": run, "items": dataset_items}
