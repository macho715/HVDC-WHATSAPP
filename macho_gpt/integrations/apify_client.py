"""Apify Dataset 연동 클라이언트/Apify dataset integration client."""

from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence
from urllib import error, request


class ApifyDatasetClientError(RuntimeError):
    """Apify Dataset 오류/Apify dataset error."""


@dataclass
class ApifyDatasetClient:
    """Apify Dataset 전송 클라이언트/Apify dataset push client."""

    token: str | None = None
    base_url: str = "https://api.apify.com/v2"
    timeout: int = 30

    def __post_init__(self) -> None:
        """토큰 초기화 및 기본 URL 정리/Initialize token and base URL."""
        if not self.token:
            self.token = os.getenv("APIFY_TOKEN")
        if not self.token:
            raise ValueError("Apify API token is required")
        self.base_url = self.base_url.rstrip("/")

    async def push_items(
        self,
        dataset_id: str,
        items: Sequence[Mapping[str, Any]] | Iterable[Mapping[str, Any]],
    ) -> None:
        """Dataset에 아이템 푸시/Push items to Apify dataset."""
        dataset = dataset_id.strip()
        if not dataset:
            raise ValueError("dataset_id must not be empty")

        payload_items = [dict(item) for item in items]
        if not payload_items:
            return

        url = f"{self.base_url}/datasets/{dataset}/items?token={self.token}"
        payload = json.dumps(payload_items, ensure_ascii=False).encode("utf-8")

        await asyncio.to_thread(self._send_request, url, payload)

    def _send_request(self, url: str, payload: bytes) -> None:
        """HTTP POST 요청 전송/Send HTTP POST request."""
        request_obj = request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(request_obj, timeout=self.timeout) as response:
                if response.status >= 400:
                    raise ApifyDatasetClientError(
                        f"Failed to push items to Apify dataset: {response.status}"
                    )
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore") if exc.fp else ""
            raise ApifyDatasetClientError(
                f"HTTP error pushing items to Apify dataset: {exc.code} {detail}"
            ) from exc
        except error.URLError as exc:
            raise ApifyDatasetClientError(
                f"Network error pushing items to Apify dataset: {exc.reason}"
            ) from exc
