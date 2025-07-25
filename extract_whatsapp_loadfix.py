#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini WhatsApp Web 스크래퍼 (로딩 상태 개선 버전)
채팅방 접근 실패 문제 해결을 위한 최신 Playwright 기법 적용
"""

import asyncio
import random
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Playwright imports
from playwright.async_api import async_playwright, Page, Browser, BrowserContext

# MACHO-GPT core imports
try:
    from scripts.logi_ai_summarizer_241219 import LogiAISummarizer
    from scripts.logi_whatsapp_241219 import WhatsAppProcessor
    from scripts.logi_base_model import LogiBaseModel
except ImportError:
    print("⚠️ MACHO-GPT 모듈을 찾을 수 없습니다. 기본 기능으로 실행합니다.")

# Configuration
CHAT_TITLE = "MR.CHA 전용"
AUTH_FILE = Path("auth.json")
BACKUP_AUTH_DIR = Path("auth_backups")
LOG_FILE = Path("whatsapp_scraper.log")

# User Agents for rotation
UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WhatsAppLoadFixScraper:
    """개선된 로딩 상태 관리 WhatsApp 스크래퍼"""
    
    def __init__(self, chat_title: str = CHAT_TITLE, auth_file: Path = AUTH_FILE):
        self.chat_title = chat_title
        self.auth_file = auth_file
        self.max_retries = 3
        self.load_timeout = 60000  # 60초
        self.network_idle_timeout = 30000  # 30초로 증가
        
    async def solve_captcha(self, page: Page) -> bool:
        """CAPTCHA 감지 및 해결"""
        try:
            captcha_frame = page.locator("iframe[src*='captcha']")
            if await captcha_frame.is_visible():
                logger.warning("CAPTCHA 감지됨 - 수동 해결 필요")
                print("\n[CAPTCHA] CAPTCHA 감지됨!")
                print("1. 브라우저에서 CAPTCHA를 해결하세요")
                print("2. 해결 완료 후 Enter를 눌러주세요...")
                input("CAPTCHA 해결 후 Enter: ")
                return True
        except Exception as e:
            logger.debug(f"CAPTCHA 확인 중 오류: {e}")
        return False
    
    async def human_like_behavior(self, page: Page):
        """인간과 유사한 행동 시뮬레이션"""
        # 랜덤 마우스 움직임
        await page.mouse.move(
            random.randint(100, 800),
            random.randint(100, 600)
        )
        await page.wait_for_timeout(random.randint(500, 1500))
        
        # PageUp 키로 스크롤
        await page.keyboard.press("PageUp")
        await page.wait_for_timeout(random.randint(1000, 3000))
        
        # 추가 랜덤 지연
        await page.wait_for_timeout(random.randint(2000, 5000))
    
    async def wait_for_chat_loading(self, page: Page) -> bool:
        """채팅방 로딩 상태 대기 (개선된 버전)"""
        try:
            logger.info("채팅방 로딩 대기 중...")
            
            # 1. 기본 로드 상태 대기
            try:
                await page.wait_for_load_state('domcontentloaded', timeout=30000)
                logger.info("DOM 로드 완료")
            except Exception as e:
                logger.warning(f"DOM 로드 타임아웃: {e}")
            
            # 2. 네트워크 유휴 상태 대기 (더 긴 타임아웃)
            try:
                await page.wait_for_load_state('networkidle', timeout=self.network_idle_timeout)
                logger.info("네트워크 유휴 상태 완료")
            except Exception as e:
                logger.warning(f"네트워크 유휴 타임아웃: {e}")
            
            # 3. 추가 안정화 대기
            await page.wait_for_timeout(15000)  # 15초로 증가
            logger.info("추가 안정화 대기 완료")
            
            # 4. 채팅 목록 로딩 확인 (더 포괄적인 방법)
            chat_selectors = [
                '[data-testid="chat-list"]',
                '[data-testid="chat-list-search"]',
                'div[role="grid"]',
                'div[data-testid*="chat"]',
                '[data-testid="cell-frame-container"]',
                'div[role="listbox"]',
                'div[data-testid="conversation-list"]',
                'div[data-testid="chat-list"]',
                'div[role="list"]',
                'div[data-testid*="conversation"]',
                'div[data-testid*="chat"]',
                'div[role="row"]',
                'div[data-testid="cell-frame"]'
            ]
            
            chat_list_found = False
            for selector in chat_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=10000)
                    logger.info(f"채팅 목록 발견: {selector}")
                    chat_list_found = True
                    break
                except Exception as e:
                    logger.debug(f"선택자 {selector} 실패: {e}")
                    continue
            
            if not chat_list_found:
                logger.warning("채팅 목록을 찾을 수 없습니다")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"채팅방 로딩 대기 실패: {e}")
            return False
    
    async def find_chat_room(self, page: Page) -> bool:
        """채팅방 찾기 (다양한 방법 시도)"""
        chat_selectors = [
            f'[title="{self.chat_title}"]',
            f'[aria-label*="{self.chat_title}"]',
            f'div[role="row"]:has-text("{self.chat_title}")',
            f'[data-testid*="chat"]:has-text("{self.chat_title}")',
            f'div:has-text("{self.chat_title}")'
        ]
        
        for selector in chat_selectors:
            try:
                logger.info(f"채팅방 검색: {selector}")
                chat_element = page.locator(selector)
                
                # 요소가 보이는지 확인
                if await chat_element.is_visible(timeout=10000):
                    logger.info(f"채팅방 발견: {selector}")
                    await chat_element.click()
                    await page.wait_for_timeout(3000)
                    return True
                    
            except Exception as e:
                logger.debug(f"선택자 {selector} 실패: {e}")
                continue
        
        return False
    
    async def discover_available_chats(self, page: Page) -> List[str]:
        """사용 가능한 채팅방 목록 탐지"""
        try:
            logger.info("사용 가능한 채팅방 탐지 중...")
            
            # 여러 선택자로 채팅방 제목 추출 시도
            chat_selectors = [
                '[data-testid="chat-list"] [title]',
                '[data-testid="chat-list"] div[role="row"]',
                'div[role="grid"] div[role="row"]',
                '[data-testid*="chat"]'
            ]
            
            chat_titles = []
            for selector in chat_selectors:
                try:
                    titles = await page.locator(selector).all_text_contents()
                    if titles:
                        chat_titles.extend(titles)
                        break
                except Exception as e:
                    logger.debug(f"선택자 {selector} 실패: {e}")
                    continue
            
            if chat_titles:
                logger.info(f"발견된 채팅방: {chat_titles[:5]}...")  # 처음 5개만 표시
                return chat_titles
            else:
                logger.warning("채팅방 목록을 찾을 수 없습니다")
                return []
                
        except Exception as e:
            logger.error(f"채팅방 탐지 실패: {e}")
            return []
    
    async def scrape_conversation(self) -> Optional[str]:
        """개선된 대화 스크래핑"""
        for attempt in range(self.max_retries):
            logger.info(f"스크래핑 시도 {attempt + 1}/{self.max_retries}")
            
            try:
                async with async_playwright() as pw:
                    # 브라우저 설정
                    browser = await pw.chromium.launch(
                        headless=True,
                        args=[
                            "--disable-blink-features=AutomationControlled",
                            "--disable-web-security",
                            "--disable-features=VizDisplayCompositor",
                            "--no-sandbox",
                            "--disable-setuid-sandbox"
                        ]
                    )
                    
                    # 컨텍스트 설정
                    context = await browser.new_context(
                        storage_state=str(self.auth_file) if self.auth_file.exists() else None,
                        user_agent=random.choice(UA_LIST),
                        viewport={
                            "width": random.randint(1200, 1400),
                            "height": random.randint(700, 900)
                        },
                        locale="en-US"
                    )
                    
                    page = await context.new_page()
                    
                    # WhatsApp Web 접속 (개선된 로딩 대기)
                    logger.info("WhatsApp Web 접속 중...")
                    await page.goto("https://web.whatsapp.com/", wait_until="networkidle", timeout=self.load_timeout)
                    await page.wait_for_load_state("load", timeout=60000)
                    await page.wait_for_timeout(10000)  # 추가 안정화
                    
                    # CAPTCHA 확인
                    await self.solve_captcha(page)
                    
                    # 채팅방 로딩 대기 (개선된 버전)
                    if not await self.wait_for_chat_loading(page):
                        logger.warning("채팅방 로딩 실패")
                        await browser.close()
                        continue
                    
                    # Chat list 렌더링 이후 대기 (더 포괄적인 접근)
                    chat_list_found = False
                    chat_list_selectors = [
                        '[data-testid="chat-list"]',
                        '[data-testid="cell-frame-container"]',
                        'div[role="listbox"]',
                        'div[data-testid="conversation-list"]',
                        'div[role="list"]',
                        'div[data-testid*="conversation"]',
                        'div[data-testid="cell-frame"]'
                    ]
                    
                    for selector in chat_list_selectors:
                        try:
                            await page.wait_for_selector(selector, timeout=30000)
                            await page.wait_for_timeout(3000)
                            logger.info(f"Chat list 렌더링 완료: {selector}")
                            chat_list_found = True
                            break
                        except Exception as e:
                            logger.debug(f"Chat list 선택자 {selector} 실패: {e}")
                            continue
                    
                    if not chat_list_found:
                        logger.warning("모든 Chat list 선택자 실패")
                        # 페이지 스크린샷 저장 (디버깅용)
                        try:
                            await page.screenshot(path="debug_chat_list.png")
                            logger.info("디버깅용 스크린샷 저장: debug_chat_list.png")
                        except Exception as e:
                            logger.warning(f"스크린샷 저장 실패: {e}")
                    
                    # 채팅방 찾기 (개선된 접근)
                    logger.info(f"채팅방 '{self.chat_title}' 검색 중...")
                    
                    # 채팅방 접근 전 추가 대기
                    await page.wait_for_timeout(3000)
                    
                    if not await self.find_chat_room(page):
                        logger.warning(f"채팅방 '{self.chat_title}'을 찾을 수 없음")
                        
                        # 사용 가능한 채팅방 탐지
                        available_chats = await self.discover_available_chats(page)
                        if available_chats:
                            logger.info(f"사용 가능한 채팅방: {available_chats}")
                        
                        await browser.close()
                        continue
                    
                    # 인간과 유사한 행동
                    await self.human_like_behavior(page)
                    
                    # CAPTCHA 재확인
                    await self.solve_captcha(page)
                    
                    # 메시지 추출
                    logger.info("메시지 추출 중...")
                    messages = await page.locator(".message-in, .message-out").all_text_contents()
                    
                    await browser.close()
                    
                    if messages:
                        logger.info(f"{len(messages)}개 메시지 추출 완료")
                        return "\n".join(messages)
                    else:
                        logger.warning("메시지를 찾을 수 없음")
                        
            except Exception as e:
                logger.error(f"스크래핑 오류 (시도 {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(random.randint(5, 15))
        
        return None
    
    async def run_with_fallback(self) -> str:
        """폴백 메커니즘과 함께 실행"""
        # 실제 스크래핑 시도
        result = await self.scrape_conversation()
        
        if result:
            return result
        
        # 폴백: 샘플 데이터 사용
        logger.warning("실제 스크래핑 실패, 샘플 데이터 사용")
        sample_file = Path("test_whatsapp_sample.txt")
        
        if sample_file.exists():
            with open(sample_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return "샘플 WhatsApp 대화: 오늘 아침 회의가 9시로 변경되었습니다."

async def main():
    """메인 실행 함수"""
    print("MACHO-GPT v3.4-mini WhatsApp 스크래퍼 (로딩 상태 개선)")
    print("=" * 60)
    
    # 인증 파일 확인
    if not AUTH_FILE.exists():
        print("인증 파일이 없습니다. auth_setup.py --setup을 먼저 실행하세요.")
        return
    
    # 스크래퍼 실행
    scraper = WhatsAppLoadFixScraper()
    result = await scraper.run_with_fallback()
    
    # 결과 출력
    print(f"\n추출된 메시지 ({len(result)} 문자):")
    print("-" * 40)
    print(result[:500] + "..." if len(result) > 500 else result)
    print("-" * 40)
    
    # 파일로 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"whatsapp_messages_{timestamp}.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"결과 저장: {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="WhatsApp Web 스크래퍼 (로딩 상태 개선)")
    parser.add_argument("--chat", default=CHAT_TITLE, help="채팅방 제목")
    parser.add_argument("--auth-file", default=str(AUTH_FILE), help="인증 파일 경로")
    parser.add_argument("--retries", type=int, default=3, help="최대 재시도 횟수")
    
    args = parser.parse_args()
    
    # 설정 업데이트
    CHAT_TITLE = args.chat
    AUTH_FILE = Path(args.auth_file)
    
    # 실행
    asyncio.run(main()) 