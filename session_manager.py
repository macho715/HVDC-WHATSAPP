# session_manager.py
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, BrowserContext

class _GlobalSession:
    """Playwright PersistentContext 싱글턴"""
    _instance: BrowserContext | None = None
    _playwright = None

    @classmethod
    async def get(cls) -> BrowserContext:
        if cls._instance and not cls._instance.is_closed():
            return cls._instance      # 이미 열려있으면 재사용

        # Playwright 인스턴스 시작
        cls._playwright = await async_playwright().start()
        
        # 공유 세션 디렉토리 생성
        shared_dir = Path("browser_data/shared_session")
        shared_dir.mkdir(parents=True, exist_ok=True)
        
        cls._instance = await cls._playwright.chromium.launch_persistent_context(
            user_data_dir=str(shared_dir),
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1280, "height": 900},
            timeout=300_000  # 5분
        )
        # 기본 타임아웃
        cls._instance.set_default_timeout(60_000)
        
        print(f"✅ 공유 세션 생성 완료: {shared_dir}")
        return cls._instance

    @classmethod
    async def close(cls):
        """세션 종료"""
        if cls._instance and not cls._instance.is_closed():
            await cls._instance.close()
            cls._instance = None
            print("✅ 공유 세션 종료 완료")
        
        if cls._playwright:
            await cls._playwright.stop()
            cls._playwright = None
            print("✅ Playwright 인스턴스 종료 완료")

# 편의 함수들
async def get_shared_session() -> BrowserContext:
    """공유 세션 가져오기"""
    return await _GlobalSession.get()

async def close_shared_session():
    """공유 세션 종료"""
    await _GlobalSession.close() 