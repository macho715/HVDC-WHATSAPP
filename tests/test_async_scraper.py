"""AsyncGroupScraper 저장 로직 테스트/AsyncGroupScraper save logic tests."""

import json
from pathlib import Path
from types import SimpleNamespace
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


@pytest.mark.asyncio
async def test_initialize_uses_storage_state_when_available(tmp_path):
    """스토리지 상태 사용 여부 확인/Ensure storage_state is applied when provided."""

    state_path = tmp_path / "auth.json"
    state_payload = {"cookies": [{"name": "wa_ul", "value": "token"}], "origins": []}
    state_path.write_text(json.dumps(state_payload), encoding="utf-8")

    config = GroupConfig(name="State Group", save_file=str(tmp_path / "messages.json"))
    scraper = AsyncGroupScraper(
        config,
        storage_state_path=str(state_path),
    )

    browser = AsyncMock()
    browser.close = AsyncMock()
    context = AsyncMock()
    context.close = AsyncMock()
    page = AsyncMock()
    page.close = AsyncMock()
    page.goto = AsyncMock()
    chromium = SimpleNamespace(launch=AsyncMock(return_value=browser))
    playwright = SimpleNamespace(
        chromium=chromium,
        stop=AsyncMock(),
    )
    context.new_page = AsyncMock(return_value=page)
    browser.new_context = AsyncMock(return_value=context)
    manager = SimpleNamespace(start=AsyncMock(return_value=playwright))

    with patch(
        "macho_gpt.async_scraper.async_scraper.async_playwright", return_value=manager
    ):
        await scraper.initialize()

    kwargs = browser.new_context.await_args.kwargs
    assert "storage_state" in kwargs
    assert kwargs["storage_state"]["cookies"][0]["name"] == "wa_ul"


@pytest.mark.asyncio
async def test_initialize_normalizes_legacy_cookie_format(tmp_path):
    """레거시 쿠키 포맷 정규화 확인/Normalize legacy cookie list format."""

    state_path = tmp_path / "auth.json"
    legacy_payload = [
        {"name": "wa_ul", "value": "token", "domain": ".web.whatsapp.com"}
    ]
    state_path.write_text(json.dumps(legacy_payload), encoding="utf-8")

    config = GroupConfig(name="Legacy Group", save_file=str(tmp_path / "messages.json"))
    scraper = AsyncGroupScraper(
        config,
        storage_state_path=str(state_path),
    )

    browser = AsyncMock()
    browser.close = AsyncMock()
    context = AsyncMock()
    context.close = AsyncMock()
    page = AsyncMock()
    page.close = AsyncMock()
    page.goto = AsyncMock()
    chromium = SimpleNamespace(launch=AsyncMock(return_value=browser))
    playwright = SimpleNamespace(
        chromium=chromium,
        stop=AsyncMock(),
    )
    context.new_page = AsyncMock(return_value=page)
    browser.new_context = AsyncMock(return_value=context)
    manager = SimpleNamespace(start=AsyncMock(return_value=playwright))

    with patch(
        "macho_gpt.async_scraper.async_scraper.async_playwright", return_value=manager
    ):
        await scraper.initialize()

    normalized = json.loads(state_path.read_text(encoding="utf-8"))
    assert isinstance(normalized, dict)
    assert normalized["origins"] == []
    assert normalized["cookies"][0]["name"] == "wa_ul"
