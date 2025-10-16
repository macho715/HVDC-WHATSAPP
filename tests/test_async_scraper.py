"""AsyncGroupScraper 저장 로직 테스트/AsyncGroupScraper save logic tests."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from macho_gpt.async_scraper.async_scraper import AsyncGroupScraper
from macho_gpt.async_scraper.group_config import GroupConfig


@pytest.mark.asyncio
async def test_save_messages_pushes_to_apify_when_configured(tmp_path):
    """Dataset ID 설정 시 Apify 전송 확인/Ensure Apify push occurs when dataset configured."""
    save_path = tmp_path / "messages.json"
    config = GroupConfig(
        name="Logistics Room",
        save_file=str(save_path),
        apify_dataset_id="datasetXYZ",
    )
    scraper = AsyncGroupScraper(config)
    messages = [{"id": "1", "text": "hello"}]

    client_instance = AsyncMock()
    client_instance.push_items = AsyncMock()

    with patch(
        "macho_gpt.async_scraper.async_scraper.ApifyDatasetClient",
        return_value=client_instance,
    ) as client_cls:
        await scraper.save_messages(messages)

    client_cls.assert_called_once()
    client_instance.push_items.assert_awaited_once_with("datasetXYZ", messages)
    stored = json.loads(Path(save_path).read_text(encoding="utf-8"))
    assert stored == messages


@pytest.mark.asyncio
async def test_save_messages_skips_apify_when_not_configured(tmp_path):
    """Dataset ID 미설정 시 Apify 전송 스킵/Ensure Apify push skipped without dataset ID."""
    save_path = tmp_path / "messages.json"
    config = GroupConfig(
        name="General Room",
        save_file=str(save_path),
    )
    scraper = AsyncGroupScraper(config)
    messages = [{"id": "1", "text": "hello"}]

    with patch(
        "macho_gpt.async_scraper.async_scraper.ApifyDatasetClient"
    ) as client_cls:
        await scraper.save_messages(messages)

    client_cls.assert_not_called()
    stored = json.loads(Path(save_path).read_text(encoding="utf-8"))
    assert stored == messages
